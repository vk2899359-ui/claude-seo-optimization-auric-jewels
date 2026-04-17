#!/usr/bin/env python3
"""
Auric Jewels - Bulk Google Indexing API Script

Submits URLs to the Google Indexing API with type=URL_UPDATED.

POLICY WARNING (read before running):
  Google officially restricts the Indexing API to pages containing
  JobPosting or BroadcastEvent structured data. See:
    https://developers.google.com/search/apis/indexing-api/v3/quickstart
  Submitting non-qualifying pages can result in the service account
  being rate-limited, rejected, or flagged. For e-commerce/blog pages
  the sanctioned path is sitemap submission + IndexNow (see the sibling
  scripts sitemap-ping.py and indexnow-submit.py).

  This script is kept because the user explicitly requested it.

Usage:
  python bulk-index.py [--dry-run] [--from-sitemap URL]

Requires:
  pip install google-auth google-auth-httplib2 requests
  Service account key file at ./service-account.json (or set
  SERVICE_ACCOUNT_FILE env var). The service account must be added
  as an Owner of the property in Google Search Console.
"""

import argparse
import os
import sys
import time
import xml.etree.ElementTree as ET
from typing import Iterable

import requests
from google.auth.transport.requests import Request as GoogleAuthRequest
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_FILE", "service-account.json")
SCOPES = ["https://www.googleapis.com/auth/indexing"]
API_URL = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SITEMAP_URL = "https://www.auricjewels.com/sitemap.xml"
REQUEST_DELAY_SECONDS = 0.6  # ~1.6 req/s, under the 200/day + QPS limits

FALLBACK_URLS = [
    "https://www.auricjewels.com/",
    "https://www.auricjewels.com/categories/rings",
    "https://www.auricjewels.com/categories/earrings",
    "https://www.auricjewels.com/categories/necklaces",
    "https://www.auricjewels.com/categories/bangles",
    "https://www.auricjewels.com/categories/bracelets",
    "https://www.auricjewels.com/categories/pendants",
    "https://www.auricjewels.com/categories/chains",
    "https://www.auricjewels.com/categories/mangalsutra",
    "https://www.auricjewels.com/collections/all",
    "https://www.auricjewels.com/blog",
    "https://www.auricjewels.com/blog/best-diamond-jewellery-showroom-gurgaon",
    "https://www.auricjewels.com/blog/best-bridal-jewellery-gurgaon",
    "https://www.auricjewels.com/blog/solitaire-ring-buying-guide-gurgaon",
    "https://www.auricjewels.com/blog/diamond-jewellery-gurgaon",
    "https://www.auricjewels.com/blog/bridal-jewellery-gurgaon",
    "https://www.auricjewels.com/blog/gold-rate-today-gurgaon",
    "https://www.auricjewels.com/blog/gold-jewellery-designs-gurgaon",
    "https://www.auricjewels.com/blog/diamond-ring-price-gurgaon",
    "https://www.auricjewels.com/blog/mangalsutra-designs-gold-diamond",
    "https://www.auricjewels.com/blog/gold-necklace-designs-gurgaon",
    "https://www.auricjewels.com/blog/diamond-earrings-women-gurgaon",
    "https://www.auricjewels.com/blog/gold-bangles-designs-gurgaon",
    "https://www.auricjewels.com/blog/platinum-rings-men-women-gurgaon",
    "https://www.auricjewels.com/blog/engagement-ring-guide-gurgaon",
    "https://www.auricjewels.com/blog/gold-chain-designs-men-women",
    "https://www.auricjewels.com/blog/lab-grown-diamond-jewellery-guide",
    "https://www.auricjewels.com/blog/gold-exchange-program-gurgaon",
    "https://www.auricjewels.com/blog/diamond-pendant-designs-women",
    "https://www.auricjewels.com/blog/lightweight-gold-jewellery-daily-wear",
    "https://www.auricjewels.com/blog/karva-chauth-jewellery-guide",
    "https://www.auricjewels.com/blog/jewellery-care-tips-gold-diamond",
    "https://www.auricjewels.com/blog/anniversary-gift-jewellery-ideas",
    "https://www.auricjewels.com/blog/mens-jewellery-guide-gold-platinum",
    "https://www.auricjewels.com/blog/diamond-bracelet-designs-women",
    "https://www.auricjewels.com/blog/gold-jewellery-investment-guide",
    "https://www.auricjewels.com/blog/wedding-jewellery-trends-2026",
    "https://www.auricjewels.com/blog/solitaire-pendant-buying-guide",
    "https://www.auricjewels.com/blog/gold-earring-designs-daily-wear",
    "https://www.auricjewels.com/blog/diamond-mangalsutra-modern-designs",
    "https://www.auricjewels.com/blog/best-jewellery-shop-sector-45-gurgaon",
    "https://www.auricjewels.com/blog/bridal-jewellery-trends-north-india",
    "https://www.auricjewels.com/blog/gold-coin-buying-guide-investment",
    "https://www.auricjewels.com/blog/diamond-necklace-set-designs",
    "https://www.auricjewels.com/blog/platinum-band-engagement-ring",
    "https://www.auricjewels.com/blog/temple-jewellery-gold-designs",
    "https://www.auricjewels.com/blog/cocktail-ring-designs-women",
    "https://www.auricjewels.com/blog/gold-jewellery-hallmark-guide-bis",
    "https://www.auricjewels.com/blog/diamond-stud-earrings-guide",
    "https://www.auricjewels.com/blog/ruby-emerald-gemstone-jewellery",
    "https://www.auricjewels.com/blog/baby-kids-gold-jewellery-designs",
    "https://www.auricjewels.com/blog/polki-kundan-jewellery-bridal",
    "https://www.auricjewels.com/blog/nose-pin-nath-designs-gold-diamond",
    "https://www.auricjewels.com/blog/antique-jewellery-designs-gold",
    "https://www.auricjewels.com/blog/office-wear-jewellery-minimalist",
    "https://www.auricjewels.com/page/who-we-are",
    "https://www.auricjewels.com/page/our-story",
    "https://www.auricjewels.com/page/policies",
    "https://www.auricjewels.com/page/akshaya-tritiya-gold-jewellery-gurgaon-2026",
]

SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def fetch_sitemap_urls(sitemap_url: str) -> list[str]:
    """Fetch a sitemap (or sitemap index) and return every <loc> URL found."""
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


def get_access_token() -> str:
    if not os.path.isfile(SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError(
            f"Service account key not found at {SERVICE_ACCOUNT_FILE}. "
            "Set SERVICE_ACCOUNT_FILE env var or place the JSON key next to this script."
        )
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    credentials.refresh(GoogleAuthRequest())
    return credentials.token


def submit_url(url: str, access_token: str, action: str = "URL_UPDATED"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    payload = {"url": url, "type": action}
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    try:
        body = resp.json()
    except ValueError:
        body = {"raw": resp.text}
    return resp.status_code, body


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit URLs to Google Indexing API.")
    parser.add_argument("--dry-run", action="store_true", help="List URLs without submitting.")
    parser.add_argument(
        "--from-sitemap",
        default=SITEMAP_URL,
        help=f"Sitemap URL to pull live URLs from (default: {SITEMAP_URL}).",
    )
    parser.add_argument(
        "--no-sitemap",
        action="store_true",
        help="Skip live sitemap fetch; use only the hardcoded fallback list.",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  AURIC JEWELS - Google Indexing API bulk submit")
    print("=" * 60)

    urls: list[str] = []
    if not args.no_sitemap:
        print(f"[*] Fetching sitemap: {args.from_sitemap}")
        live = fetch_sitemap_urls(args.from_sitemap)
        print(f"[*] Live sitemap URLs: {len(live)}")
        urls.extend(live)
    urls.extend(FALLBACK_URLS)
    urls = dedupe(urls)
    print(f"[*] Total unique URLs to submit: {len(urls)}\n")

    if args.dry_run:
        for u in urls:
            print(u)
        return 0

    print("[*] Getting OAuth2 access token...")
    try:
        token = get_access_token()
    except Exception as exc:
        print(f"[x] Failed to get token: {exc}")
        return 1
    print("[ok] Token acquired.\n")

    success = 0
    failed = 0
    errors: list[tuple[str, str]] = []

    for i, url in enumerate(urls, 1):
        try:
            status, result = submit_url(url, token)
        except requests.RequestException as exc:
            failed += 1
            errors.append((url, f"network error: {exc}"))
            print(f"  [{i}/{len(urls)}] FAIL {url} -- network error: {exc}")
            time.sleep(REQUEST_DELAY_SECONDS)
            continue

        if status == 200:
            success += 1
            print(f"  [{i}/{len(urls)}] OK   {url}")
        else:
            failed += 1
            err = result.get("error", {}).get("message", f"HTTP {status}")
            errors.append((url, err))
            print(f"  [{i}/{len(urls)}] FAIL {url} -- {err}")

        time.sleep(REQUEST_DELAY_SECONDS)

    print()
    print("=" * 60)
    print(f"  DONE.  Success: {success}  Failed: {failed}")
    print("=" * 60)

    if errors:
        print("\nFailed URLs:")
        for url, err in errors:
            print(f"  - {url}: {err}")

    print("\nCheck Search Console: https://search.google.com/search-console/")
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
