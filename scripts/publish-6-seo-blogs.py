#!/usr/bin/env python3
"""
Auric Jewels — Publish 6 New SEO Blog Articles (April 2026)
============================================================

USAGE:
    python3 scripts/publish-6-seo-blogs.py

This script:
  1. Reads 6 blog article HTML files from content/
  2. Publishes each via Saleor pageCreate GraphQL mutation
  3. Adds metadata type=blog to each page (for /blog listing)
  4. Reports all published URLs

API: https://auric.thecodemesh.online/graphql/
Page Type ID: UGFnZVR5cGU6Ng== (SEO Page)
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

# ── Configuration ────────────────────────────────────────────
API_ENDPOINT = "https://auric.thecodemesh.online/graphql/"
AUTH_TOKEN = "DpDjidKqKWNnsr9zQarZKsVqnDT97D"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

CONTENT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "content",
)

# ── Article Definitions ─────────────────────────────────────
ARTICLES = [
    {
        "title": "Lightweight Gold Jewellery for Working Women — Daily Wear Guide 2026",
        "slug": "lightweight-gold-jewellery-working-women-daily-wear",
        "metaTitle": "Lightweight Gold Jewellery Working Women | Auric Jewels Gurgaon",
        "metaDescription": "Discover the best lightweight gold jewellery for working women — daily wear studs, chains, pendants & bangles in 18K/22K gold. Visit Auric Jewels Gurgaon.",
        "contentFile": "blog-lightweight-gold-jewellery-working-women.html",
    },
    {
        "title": "Lab-Grown vs Natural Diamonds — Complete Comparison Guide India 2026",
        "slug": "lab-grown-vs-natural-diamonds-comparison-india",
        "metaTitle": "Lab-Grown vs Natural Diamonds India 2026 | Auric Jewels Gurgaon",
        "metaDescription": "Lab-grown vs natural diamonds — price, resale value, certification & which to choose. Complete 2026 comparison guide. Certified diamonds at Auric Jewels.",
        "contentFile": "blog-lab-grown-vs-natural-diamonds-comparison-india.html",
    },
    {
        "title": "Top 10 Jewellery Trends in India 2026 — What Every Woman Should Own",
        "slug": "jewellery-trends-india-2026",
        "metaTitle": "Top 10 Jewellery Trends India 2026 | Auric Jewels Gurgaon",
        "metaDescription": "Discover the top 10 jewellery trends in India for 2026 — layered necklaces, sculptural earrings, Polki revival & more. Explore trending designs at Auric Jewels.",
        "contentFile": "blog-jewellery-trends-india-2026.html",
    },
    {
        "title": "Gold Jewellery as Investment in 2026 — Why Smart Families Buy Gold in Gurgaon",
        "slug": "gold-jewellery-investment-2026-gurgaon",
        "metaTitle": "Gold Jewellery Investment 2026 Gurgaon | Auric Jewels Gurgaon",
        "metaDescription": "Gold jewellery as investment in 2026 — price trends, BIS hallmark, making charges, resale value & buying guide. Trusted gold jeweller Auric Jewels Gurgaon.",
        "contentFile": "blog-gold-jewellery-investment-2026-gurgaon.html",
    },
    {
        "title": "Platinum Jewellery for Men — Chains, Bracelets & Rings Guide Gurgaon",
        "slug": "platinum-jewellery-men-gurgaon",
        "metaTitle": "Platinum Jewellery Men Chains Rings | Auric Jewels Gurgaon",
        "metaDescription": "Explore platinum jewellery for men — chains, bracelets, rings & cufflinks. Durable, hypoallergenic & sophisticated. Shop men's platinum at Auric Jewels Gurgaon.",
        "contentFile": "blog-platinum-jewellery-men-gurgaon.html",
    },
    {
        "title": "How to Style Layered Necklaces — Trending Jewellery Looks for Indian Women 2026",
        "slug": "layered-necklace-styling-guide-indian-women",
        "metaTitle": "Layered Necklace Styling Guide India | Auric Jewels Gurgaon",
        "metaDescription": "Master layered necklace styling — rules, combinations, Indian & Western looks. Gold & diamond layering tips for 2026. Shop necklaces at Auric Jewels Gurgaon.",
        "contentFile": "blog-layered-necklace-styling-guide-indian-women.html",
    },
]


def graphql_request(query, variables=None):
    """Send a GraphQL request and return the parsed JSON response."""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_ENDPOINT,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AUTH_TOKEN}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        print(f"    HTTP {e.code}: {e.reason}")
        if body:
            print(f"    Response: {body[:500]}")
        return None
    except urllib.error.URLError as e:
        print(f"    Connection error: {e.reason}")
        return None


def read_content(filename):
    """Read HTML content from the content directory."""
    filepath = os.path.join(CONTENT_DIR, filename)
    if not os.path.exists(filepath):
        print(f"    File not found: {filepath}")
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def create_page(article, content):
    """Create a page via Saleor pageCreate mutation."""
    # Saleor EditorJS content format
    editor_content = json.dumps({
        "blocks": [{"type": "rawHtml", "data": {"html": content}}]
    })

    input_data = {
        "slug": article["slug"],
        "title": article["title"],
        "pageType": PAGE_TYPE_ID,
        "isPublished": True,
        "content": editor_content,
        "seo": {
            "title": article["metaTitle"],
            "description": article["metaDescription"],
        },
    }

    mutation = """mutation PageCreate($input: PageCreateInput!) {
        pageCreate(input: $input) {
            page {
                id
                slug
                title
            }
            errors {
                field
                message
                code
            }
        }
    }"""

    result = graphql_request(mutation, {"input": input_data})
    if not result:
        return None, "No response from API"

    if "errors" in result and result["errors"]:
        return None, result["errors"][0].get("message", str(result["errors"]))

    page_create = result.get("data", {}).get("pageCreate", {})
    if page_create.get("errors"):
        err = page_create["errors"][0]
        return None, f"{err.get('field', '?')}: {err.get('message', '?')} ({err.get('code', '?')})"

    page = page_create.get("page")
    if page:
        return page, None

    return None, f"Unexpected response: {json.dumps(result)[:200]}"


def add_blog_metadata(page_id):
    """Add type=blog metadata to a page so it shows on /blog listing."""
    mutation = """mutation UpdateMetadata($id: ID!, $input: [MetadataInput!]!) {
        updateMetadata(id: $id, input: $input) {
            item {
                metadata {
                    key
                    value
                }
            }
            errors {
                field
                message
            }
        }
    }"""

    variables = {
        "id": page_id,
        "input": [{"key": "type", "value": "blog"}],
    }

    result = graphql_request(mutation, variables)
    if not result:
        return False, "No response from API"

    if "errors" in result and result["errors"]:
        return False, result["errors"][0].get("message", str(result["errors"]))

    update = result.get("data", {}).get("updateMetadata", {})
    if update and update.get("errors"):
        err = update["errors"][0]
        return False, f"{err.get('field', '?')}: {err.get('message', '?')}"

    return True, None


def main():
    print()
    print("=" * 60)
    print("  Auric Jewels — Publish 6 New SEO Blog Articles")
    print("  Saleor CMS via GraphQL API")
    print("=" * 60)
    print()
    print(f"  API: {API_ENDPOINT}")
    print(f"  Page Type: {PAGE_TYPE_ID}")
    print(f"  Content Dir: {CONTENT_DIR}")
    print()

    published = []
    failed = []

    for i, article in enumerate(ARTICLES, 1):
        print(f"[{i}/{len(ARTICLES)}] {article['title'][:65]}...")
        print(f"    Slug: {article['slug']}")

        # Read content
        content = read_content(article["contentFile"])
        if not content:
            failed.append((article, "Content file not found"))
            print(f"    ✘ SKIPPED — content file missing")
            print()
            continue

        print(f"    Content: {len(content):,} characters")

        # Create page
        print(f"    Creating page...")
        page, error = create_page(article, content)

        if error:
            # Try without EditorJS wrapper (plain HTML)
            print(f"    First attempt failed: {error}")
            print(f"    Retrying with plain HTML content...")

            input_data = {
                "slug": article["slug"],
                "title": article["title"],
                "pageType": PAGE_TYPE_ID,
                "isPublished": True,
                "content": content,
                "seo": {
                    "title": article["metaTitle"],
                    "description": article["metaDescription"],
                },
            }

            mutation = """mutation PageCreate($input: PageCreateInput!) {
                pageCreate(input: $input) {
                    page { id slug title }
                    errors { field message code }
                }
            }"""

            result = graphql_request(mutation, {"input": input_data})
            if result:
                pc = result.get("data", {}).get("pageCreate", {})
                if pc.get("page") and not pc.get("errors"):
                    page = pc["page"]
                    error = None
                elif pc.get("errors"):
                    err = pc["errors"][0]
                    error = f"{err.get('field')}: {err.get('message')}"

        if error:
            failed.append((article, error))
            print(f"    ✘ FAILED: {error}")
            print()
            continue

        page_id = page["id"]
        print(f"    ✔ Created (ID: {page_id})")

        # Add metadata type=blog
        print(f"    Adding metadata type=blog...")
        meta_ok, meta_err = add_blog_metadata(page_id)
        if meta_ok:
            print(f"    ✔ Metadata added")
        else:
            print(f"    ⚠ Metadata failed: {meta_err}")

        published.append(article)
        print(f"    → https://www.auricjewels.com/blog/{article['slug']}")
        print()

        # Small delay between requests
        if i < len(ARTICLES):
            time.sleep(1)

    # ── Summary ──────────────────────────────────────────────
    print("=" * 60)
    print(f"  RESULTS: {len(published)} published, {len(failed)} failed")
    print("=" * 60)
    print()

    if published:
        print("  Published URLs:")
        for a in published:
            print(f"    ✔ https://www.auricjewels.com/blog/{a['slug']}")
        print()

    if failed:
        print("  Failed:")
        for a, err in failed:
            print(f"    ✘ {a['slug']}: {err}")
        print()

    print("  Done.")
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
