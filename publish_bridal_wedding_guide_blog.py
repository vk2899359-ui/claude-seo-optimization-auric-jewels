#!/usr/bin/env python3
"""
Publish: Bridal Jewellery in Gurgaon — Complete Wedding Guide 2026
-------------------------------------------------------------------
Slug: bridal-jewellery-wedding-guide-gurgaon-2026
Target: Google AI Overview for "bridal jewellery gurgaon"

Run: python publish_bridal_wedding_guide_blog.py
"""

import requests
import json
import sys
import random
import string

# ── CONFIG ───────────────────────────────────────────────────────────────────
API          = "https://auric.thecodemesh.online/graphql/"
TOKEN        = "xqsa4N4h2OVV5Apipr9mNs9zFYijnx"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

SLUG             = "bridal-jewellery-wedding-guide-gurgaon-2026"
TITLE            = "Bridal Jewellery in Gurgaon: Complete Wedding Guide 2026"
SEO_TITLE        = "Bridal Jewellery in Gurgaon: Complete Wedding Guide 2026 | Auric Jewels"
META_DESCRIPTION = (
    "Shop certified diamond & BIS hallmarked gold bridal sets at Auric Jewels Gurgaon, "
    "Sector 45. Expert bridal consultation available. Visit or WhatsApp today."
)

# ── BLOG HTML CONTENT ─────────────────────────────────────────────────────────
import os
_content_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "content",
    "blog-bridal-jewellery-wedding-guide-gurgaon-2026.html"
)
with open(_content_file, "r", encoding="utf-8") as _f:
    BLOG_HTML = _f.read()


# ── FORMAT CONVERSION ─────────────────────────────────────────────────────────
def uid():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


def html_to_paragraph_blocks(raw_html):
    blocks = []
    for line in raw_html.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        encoded = stripped.replace("<", "&lt;").replace(">", "&gt;")
        blocks.append({
            "id":   uid(),
            "type": "paragraph",
            "data": {"text": encoded}
        })
    return blocks


# ── GRAPHQL ───────────────────────────────────────────────────────────────────
CREATE_MUTATION = """
mutation PageCreate($input: PageCreateInput!) {
  pageCreate(input: $input) {
    page {
      id
      slug
      title
      isPublished
      pageType { id name }
    }
    errors { field message code }
  }
}
"""

UPDATE_MUTATION = """
mutation PageUpdate($id: ID!, $input: PageInput!) {
  pageUpdate(id: $id, input: $input) {
    page {
      id
      slug
      title
      isPublished
    }
    errors { field message code }
  }
}
"""

FIND_PAGE_QUERY = """
query FindPage($slug: String!) {
  page(slug: $slug) {
    id
    slug
    title
    isPublished
  }
}
"""


def find_existing_page():
    resp = requests.post(
        API,
        headers=HEADERS,
        json={"query": FIND_PAGE_QUERY, "variables": {"slug": SLUG}},
        timeout=30
    )
    if resp.status_code != 200:
        return None
    data = resp.json()
    return (data.get("data") or {}).get("page")


def publish():
    print()
    print("=" * 62)
    print("  Auric Jewels — Bridal Wedding Guide Blog Publisher")
    print(f"  Slug : {SLUG}")
    print(f"  Title: {TITLE}")
    print("=" * 62)
    print()

    blocks = html_to_paragraph_blocks(BLOG_HTML)
    doc = {
        "time":    1775718786125,
        "version": "2.24.3",
        "blocks":  blocks
    }
    content_str = json.dumps(doc, ensure_ascii=False)
    print(f"  Blocks : {len(blocks)}")
    print(f"  Size   : {len(content_str):,} chars")
    print()

    # Check if page already exists — update instead of create
    existing = find_existing_page()

    if existing:
        print(f"  Page exists (ID: {existing['id']}) — updating...")
        variables = {
            "id": existing["id"],
            "input": {
                "title":       TITLE,
                "isPublished": True,
                "content":     content_str,
                "seo": {
                    "title":       SEO_TITLE,
                    "description": META_DESCRIPTION
                }
            }
        }
        resp = requests.post(
            API,
            headers=HEADERS,
            json={"query": UPDATE_MUTATION, "variables": variables},
            timeout=30
        )
        result_key = "pageUpdate"
    else:
        print("  Page not found — creating new page...")
        variables = {
            "input": {
                "title":       TITLE,
                "slug":        SLUG,
                "pageType":    PAGE_TYPE_ID,
                "isPublished": True,
                "content":     content_str,
                "seo": {
                    "title":       SEO_TITLE,
                    "description": META_DESCRIPTION
                }
            }
        }
        resp = requests.post(
            API,
            headers=HEADERS,
            json={"query": CREATE_MUTATION, "variables": variables},
            timeout=30
        )
        result_key = "pageCreate"

    if resp.status_code != 200:
        print(f"  HTTP error: {resp.status_code} — {resp.text[:300]}")
        sys.exit(1)

    data   = resp.json()
    gql_e  = data.get("errors", [])
    if gql_e:
        print(f"  GraphQL error: {gql_e}")
        sys.exit(1)

    result = (data.get("data") or {}).get(result_key, {})
    errs   = result.get("errors", [])
    if errs:
        for e in errs:
            print(f"  Error [{e.get('field')}] {e.get('code')}: {e.get('message')}")
        sys.exit(1)

    page = result.get("page", {})
    if not page:
        print(f"  No page returned. Full response:\n{json.dumps(data, indent=2)}")
        sys.exit(1)

    print()
    print("=" * 62)
    print("  PUBLISHED SUCCESSFULLY")
    print(f"  ID        : {page['id']}")
    print(f"  Slug      : {page['slug']}")
    print(f"  Published : {page['isPublished']}")
    print(f"  Live URL  : https://www.auricjewels.com/blog/{page['slug']}")
    print("=" * 62)
    print()


if __name__ == "__main__":
    publish()
