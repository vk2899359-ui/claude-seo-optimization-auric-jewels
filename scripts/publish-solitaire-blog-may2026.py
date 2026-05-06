#!/usr/bin/env python3
"""
Auric Jewels — Publish: Solitaire Diamond Ring Gurgaon 2026
============================================================
Session date : 06 May 2026
Target keyword: solitaire diamond ring Gurgaon
Blog URL (when live): https://www.auricjewels.com/blog/solitaire-diamond-ring-gurgaon-2026

USAGE (Mac/Linux):
    python3 scripts/publish-solitaire-blog-may2026.py

USAGE (Windows PowerShell):
    python scripts/publish-solitaire-blog-may2026.py

Requires: Python 3.6+ (no pip installs needed — stdlib only)
"""

import json
import os
import sys
import urllib.request
import urllib.error

# ── Configuration ────────────────────────────────────────────
API_ENDPOINT  = "https://auric.thecodemesh.online/graphql/"
AUTH_TOKEN    = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID  = "UGFnZVR5cGU6Ng=="
CHANNEL       = "franchise1"

ARTICLE = {
    "title":       "Solitaire Diamond Ring Gurgaon — The 2026 Guide to the Perfect Proposal Stone",
    "slug":        "solitaire-diamond-ring-gurgaon-2026",
    "metaTitle":   "Solitaire Diamond Ring Gurgaon — 2026 Guide | Auric Jewels",
    "metaDescription": (
        "Find the perfect certified solitaire diamond ring in Gurgaon. "
        "Expert guide on cut, clarity, carat & setting for 2026 proposals. "
        "IGI/GIA certified at Auric Jewels Sector 45."
    ),
    "contentFile": os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "content",
        "blog-solitaire-diamond-ring-gurgaon-2026.html",
    ),
}


def graphql_request(query, variables=None):
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
        print(f"  HTTP {e.code}: {e.reason}")
        if body:
            print(f"  Body: {body[:600]}")
        return None
    except urllib.error.URLError as e:
        print(f"  Connection error: {e.reason}")
        return None


def create_page(content):
    editor_content = json.dumps({
        "blocks": [{"type": "rawHtml", "data": {"html": content}}]
    })

    mutation = """mutation PageCreate($input: PageCreateInput!) {
        pageCreate(input: $input) {
            page { id slug title }
            errors { field message code }
        }
    }"""

    variables = {
        "input": {
            "slug":       ARTICLE["slug"],
            "title":      ARTICLE["title"],
            "pageType":   PAGE_TYPE_ID,
            "isPublished": True,
            "content":    editor_content,
            "seo": {
                "title":       ARTICLE["metaTitle"],
                "description": ARTICLE["metaDescription"],
            },
        }
    }

    result = graphql_request(mutation, variables)
    if not result:
        return None, "No response from API"

    if result.get("errors"):
        return None, result["errors"][0].get("message", str(result["errors"]))

    pc = result.get("data", {}).get("pageCreate", {})
    if pc.get("errors"):
        err = pc["errors"][0]
        return None, f"{err.get('field')}: {err.get('message')} ({err.get('code')})"

    page = pc.get("page")
    if page:
        return page, None

    return None, f"Unexpected response: {json.dumps(result)[:300]}"


def add_blog_metadata(page_id):
    mutation = """mutation UpdateMetadata($id: ID!, $input: [MetadataInput!]!) {
        updateMetadata(id: $id, input: $input) {
            item { metadata { key value } }
            errors { field message }
        }
    }"""
    result = graphql_request(mutation, {
        "id": page_id,
        "input": [{"key": "type", "value": "blog"}],
    })
    if not result:
        return False, "No response"
    update = result.get("data", {}).get("updateMetadata", {})
    if update and update.get("errors"):
        err = update["errors"][0]
        return False, f"{err.get('field')}: {err.get('message')}"
    return True, None


def main():
    print()
    print("=" * 60)
    print("  Auric Jewels — Session: 06 May 2026")
    print("  Publishing: Solitaire Diamond Ring Gurgaon 2026")
    print("=" * 60)
    print()

    # Read HTML content
    if not os.path.exists(ARTICLE["contentFile"]):
        print(f"  ERROR: Content file not found:")
        print(f"    {ARTICLE['contentFile']}")
        sys.exit(1)

    with open(ARTICLE["contentFile"], "r", encoding="utf-8") as f:
        content = f.read()

    print(f"  Title   : {ARTICLE['title']}")
    print(f"  Slug    : {ARTICLE['slug']}")
    print(f"  Content : {len(content):,} characters")
    print()

    # Create page
    print("  Creating page in Saleor...")
    page, error = create_page(content)

    if error:
        print(f"  First attempt failed: {error}")
        print("  Retrying with plain HTML content (no EditorJS wrapper)...")

        mutation = """mutation PageCreate($input: PageCreateInput!) {
            pageCreate(input: $input) {
                page { id slug title }
                errors { field message code }
            }
        }"""
        result = graphql_request(mutation, {
            "input": {
                "slug":        ARTICLE["slug"],
                "title":       ARTICLE["title"],
                "pageType":    PAGE_TYPE_ID,
                "isPublished": True,
                "content":     content,
                "seo": {
                    "title":       ARTICLE["metaTitle"],
                    "description": ARTICLE["metaDescription"],
                },
            }
        })
        if result:
            pc = result.get("data", {}).get("pageCreate", {})
            if pc.get("page") and not pc.get("errors"):
                page = pc["page"]
                error = None
            elif pc.get("errors"):
                err = pc["errors"][0]
                error = f"{err.get('field')}: {err.get('message')}"

    if error:
        print(f"  FAILED: {error}")
        print()
        print("  Manual publishing steps:")
        print("    1. Log in to Saleor admin at https://auric.thecodemesh.online/dashboard/")
        print("    2. Go to Pages > Create Page")
        print(f"    3. Select page type with ID: {PAGE_TYPE_ID}")
        print(f"    4. Set slug to: {ARTICLE['slug']}")
        print(f"    5. Paste HTML content from: content/blog-solitaire-diamond-ring-gurgaon-2026.html")
        print(f"    6. Set SEO title: {ARTICLE['metaTitle']}")
        print(f"    7. Set SEO description: {ARTICLE['metaDescription']}")
        print("    8. Publish and add metadata key=type value=blog")
        sys.exit(1)

    page_id = page["id"]
    print(f"  Page created  (ID: {page_id})")

    # Add blog metadata
    meta_ok, meta_err = add_blog_metadata(page_id)
    if meta_ok:
        print("  Metadata type=blog added")
    else:
        print(f"  Metadata warning: {meta_err}")

    print()
    print("=" * 60)
    print("  PUBLISHED SUCCESSFULLY")
    print(f"  URL: https://www.auricjewels.com/blog/{ARTICLE['slug']}")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
