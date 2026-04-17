#!/usr/bin/env python3
"""
Auric Jewels - IndexNow bulk submit.

IndexNow is the open protocol adopted by Bing, Yandex, Seznam, Naver, and Yep.
Google does NOT consume IndexNow directly but still reads the sitemap via
Search Console (see sitemap-ping.py). IndexNow is the correct, sanctioned
path for accelerating indexing of e-commerce/blog pages on the engines that
support it.

How it works:
  1. You generate a random key (32-128 hex chars) and host it at
     https://www.auricjewels.com/<KEY>.txt with the key as the body.
  2. You POST up to 10,000 URLs per call to the IndexNow endpoint.
  3. Bing/Yandex/etc. verify the key by fetching the txt file, then crawl.

Key hosting:
  Put the key file at public/<KEY>.txt in this Next.js repo -- it will be
  served at https://www.auricjewels.com/<KEY>.txt automatically. This
  script can create the key file for you with --create-key.

Usage:
  # First time -- generate key and write it to public/
  python indexnow-submit.py --create-key

  # Deploy the site so the key file is live, THEN submit:
  python indexnow-submit.py

  # Or submit with a specific key (skip auto-discovery):
  INDEXNOW_KEY=abc123... python indexnow-submit.py

  # Dry run to see URL set without submitting:
  python indexnow-submit.py --dry-run
"""

import argparse
import os
import secrets
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable

import requests

HOST = "www.auricjewels.com"
SITEMAP_URL = f"https://{HOST}/sitemap.xml"
# api.indexnow.org fans out to all participating engines. Bing and Yandex
# also expose direct endpoints; listing both avoids a single point of failure.
INDEXNOW_ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
    "https://yandex.com/indexnow",
]
BATCH_SIZE = 10_000  # IndexNow spec max per request
PUBLIC_DIR = Path(__file__).resolve().parents[2] / "public"
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def fetch_sitemap_urls(sitemap_url: str) -> list[str]:
    urls: list[str] = []
    try:
        resp = requests.get(sitemap_url, timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        print(f"[!] Could not fetch {sitemap_url}: {exc}")
        return urls
    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as exc:
        print(f"[!] Could not parse sitemap XML: {exc}")
        return urls
    tag = root.tag.split("}", 1)[-1]
    if tag == "sitemapindex":
        for sm in root.findall("sm:sitemap/sm:loc", SITEMAP_NS):
            if sm.text:
                urls.extend(fetch_sitemap_urls(sm.text.strip()))
    elif tag == "urlset":
        for loc in root.findall("sm:url/sm:loc", SITEMAP_NS):
            if loc.text:
                urls.append(loc.text.strip())
    return urls


def dedupe(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def find_existing_key() -> str | None:
    """Look for an existing <key>.txt in public/."""
    if not PUBLIC_DIR.is_dir():
        return None
    for entry in PUBLIC_DIR.iterdir():
        if not entry.is_file() or entry.suffix != ".txt":
            continue
        stem = entry.stem
        if len(stem) < 32 or not all(c in "0123456789abcdefABCDEF" for c in stem):
            continue
        body = entry.read_text().strip()
        if body == stem:
            return stem
    return None


def create_key() -> str:
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    key = secrets.token_hex(32)  # 64 hex chars, within spec
    key_file = PUBLIC_DIR / f"{key}.txt"
    key_file.write_text(key)
    print(f"[ok] Wrote key file: {key_file}")
    print(f"[ok] After deploy it will be live at: https://{HOST}/{key}.txt")
    return key


def submit_batch(endpoint: str, key: str, urls: list[str]) -> tuple[int, str]:
    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": f"https://{HOST}/{key}.txt",
        "urlList": urls,
    }
    try:
        resp = requests.post(
            endpoint,
            json=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=60,
        )
    except requests.RequestException as exc:
        return 0, f"network error: {exc}"
    return resp.status_code, resp.text[:400]


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit URLs via IndexNow.")
    parser.add_argument("--create-key", action="store_true",
                        help="Generate a new IndexNow key and write it to public/.")
    parser.add_argument("--dry-run", action="store_true",
                        help="List URLs without submitting.")
    parser.add_argument("--from-sitemap", default=SITEMAP_URL,
                        help=f"Sitemap URL (default: {SITEMAP_URL}).")
    args = parser.parse_args()

    if args.create_key:
        create_key()
        print("\nNext: deploy the site, then re-run without --create-key to submit.")
        return 0

    key = os.environ.get("INDEXNOW_KEY") or find_existing_key()
    if not key:
        print("[x] No IndexNow key found.")
        print("    Run `python indexnow-submit.py --create-key` first, deploy, then retry.")
        return 1
    print(f"[*] Using IndexNow key: {key[:8]}... (file at public/{key}.txt)")

    print(f"[*] Fetching sitemap: {args.from_sitemap}")
    urls = dedupe(fetch_sitemap_urls(args.from_sitemap))
    print(f"[*] Total unique URLs: {len(urls)}\n")

    if not urls:
        print("[x] No URLs to submit.")
        return 1

    if args.dry_run:
        for u in urls:
            print(u)
        return 0

    failed_any = False
    for endpoint in INDEXNOW_ENDPOINTS:
        print(f"[*] Submitting to {endpoint}")
        for i in range(0, len(urls), BATCH_SIZE):
            batch = urls[i : i + BATCH_SIZE]
            status, body = submit_batch(endpoint, key, batch)
            if 200 <= status < 300:
                print(f"    OK  batch {i // BATCH_SIZE + 1}: {len(batch)} URLs (HTTP {status})")
            else:
                failed_any = True
                print(f"    FAIL batch {i // BATCH_SIZE + 1}: HTTP {status} -- {body}")
        print()

    print("=" * 60)
    print("  IndexNow submission complete." if not failed_any
          else "  IndexNow submission finished with errors.")
    print("=" * 60)
    return 0 if not failed_any else 2


if __name__ == "__main__":
    sys.exit(main())
