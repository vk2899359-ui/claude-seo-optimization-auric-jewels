#!/usr/bin/env python3
"""
Auric Jewels - Sitemap submission to Google Search Console and Bing.

Why not just "ping" sitemaps?
  Google deprecated the anonymous /ping?sitemap= endpoint in June 2023.
  Bing deprecated theirs too. The modern, supported paths are:

    Google: Search Console API -- webmasters.sitemaps.submit
            (uses the same service account as bulk-index.py, which must
             be added as an Owner of the property in Search Console)

    Bing:   Bing Webmaster URL submission API
            (requires an API key from https://www.bing.com/webmasters/,
             set via BING_WEBMASTER_KEY env var)

Usage:
  python sitemap-submit.py              # submits to Google + Bing if configured
  python sitemap-submit.py --google     # Google only
  python sitemap-submit.py --bing       # Bing only

Requires:
  pip install google-auth google-auth-httplib2 requests
"""

import argparse
import os
import sys
from urllib.parse import quote

import requests
from google.auth.transport.requests import Request as GoogleAuthRequest
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_FILE", "service-account.json")
SITE_URL = "https://www.auricjewels.com/"
SITEMAP_URL = "https://www.auricjewels.com/sitemap.xml"
GSC_SCOPES = ["https://www.googleapis.com/auth/webmasters"]
BING_KEY = os.environ.get("BING_WEBMASTER_KEY")


def submit_to_google() -> bool:
    if not os.path.isfile(SERVICE_ACCOUNT_FILE):
        print(f"[x] Google: service account key not found at {SERVICE_ACCOUNT_FILE}")
        return False

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=GSC_SCOPES
    )
    creds.refresh(GoogleAuthRequest())

    # Endpoint: PUT /webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}
    endpoint = (
        "https://www.googleapis.com/webmasters/v3/sites/"
        f"{quote(SITE_URL, safe='')}/sitemaps/{quote(SITEMAP_URL, safe='')}"
    )
    resp = requests.put(
        endpoint,
        headers={"Authorization": f"Bearer {creds.token}"},
        timeout=30,
    )
    if resp.status_code in (200, 204):
        print(f"[ok] Google Search Console: sitemap submitted ({resp.status_code})")
        return True
    print(f"[x] Google Search Console: HTTP {resp.status_code} -- {resp.text[:400]}")
    return False


def submit_to_bing() -> bool:
    if not BING_KEY:
        print("[-] Bing: skipping (set BING_WEBMASTER_KEY env var to enable)")
        return True  # not a failure, just skipped

    endpoint = f"https://ssl.bing.com/webmaster/api.svc/json/SubmitFeed?apikey={BING_KEY}"
    payload = {"siteUrl": SITE_URL.rstrip("/"), "feedUrl": SITEMAP_URL}
    resp = requests.post(
        endpoint,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    if resp.status_code == 200:
        print(f"[ok] Bing Webmaster: sitemap submitted")
        return True
    print(f"[x] Bing Webmaster: HTTP {resp.status_code} -- {resp.text[:400]}")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit sitemap to Google + Bing.")
    parser.add_argument("--google", action="store_true", help="Only submit to Google.")
    parser.add_argument("--bing", action="store_true", help="Only submit to Bing.")
    args = parser.parse_args()

    do_google = args.google or not args.bing
    do_bing = args.bing or not args.google

    print(f"Site:    {SITE_URL}")
    print(f"Sitemap: {SITEMAP_URL}\n")

    ok = True
    if do_google:
        ok = submit_to_google() and ok
    if do_bing:
        ok = submit_to_bing() and ok
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
