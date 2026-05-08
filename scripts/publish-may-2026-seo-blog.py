#!/usr/bin/env python3
"""
Auric Jewels — Publish May 2026 SEO Blog Article
=================================================
Target keyword: diamond choker necklace bridal Gurgaon

USAGE:
    python3 scripts/publish-may-2026-seo-blog.py

API: https://auric.thecodemesh.online/graphql/
Auth token: rlcLjvXb3wMMHMf1PBsePS8UdTmOBb
Channel: franchise1
Page Type ID: UGFnZVR5cGU6Ng==
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

API_ENDPOINT = "https://auric.thecodemesh.online/graphql/"
AUTH_TOKEN = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="
CHANNEL = "franchise1"

CONTENT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "content",
)

ARTICLE = {
    "title": "Diamond Choker Necklaces for the 2026 Bride: The Statement Piece Every Gurugram Wedding Demands",
    "slug": "diamond-choker-necklace-bridal-gurgaon-2026",
    "metaTitle": "Diamond Choker Necklace Bridal Gurgaon 2026 | Auric Jewels",
    "metaDescription": "Discover why the diamond choker necklace is the #1 bridal jewellery piece for 2026 brides in Gurugram. IGI/GIA certified diamonds, rivière & sculpted styles. Book your bridal consultation at Auric Jewels, Sector 45, Gurugram.",
    "contentFile": "blog-diamond-choker-necklace-bridal-gurgaon-2026.html",
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
            print(f"  Response: {body[:500]}")
        return None
    except urllib.error.URLError as e:
        print(f"  Connection error: {e.reason}")
        return None


def create_page(html_content):
    editor_content = json.dumps({
        "blocks": [{"type": "rawHtml", "data": {"html": html_content}}]
    })

    input_data = {
        "slug": ARTICLE["slug"],
        "title": ARTICLE["title"],
        "pageType": PAGE_TYPE_ID,
        "isPublished": True,
        "content": editor_content,
        "seo": {
            "title": ARTICLE["metaTitle"],
            "description": ARTICLE["metaDescription"],
        },
    }

    mutation = """mutation PageCreate($input: PageCreateInput!) {
        pageCreate(input: $input) {
            page { id slug title }
            errors { field message code }
        }
    }"""

    result = graphql_request(mutation, {"input": input_data})
    if not result:
        return None, "No response from API"

    if "errors" in result and result["errors"]:
        return None, result["errors"][0].get("message", str(result["errors"]))

    pc = result.get("data", {}).get("pageCreate", {})
    if pc.get("errors"):
        err = pc["errors"][0]
        return None, f"{err.get('field')}: {err.get('message')} ({err.get('code')})"

    page = pc.get("page")
    if page:
        return page, None

    # Fallback: try plain HTML content
    return None, f"Unexpected response: {json.dumps(result)[:300]}"


def create_page_plain(html_content):
    """Fallback: publish with plain HTML string as content."""
    input_data = {
        "slug": ARTICLE["slug"],
        "title": ARTICLE["title"],
        "pageType": PAGE_TYPE_ID,
        "isPublished": True,
        "content": html_content,
        "seo": {
            "title": ARTICLE["metaTitle"],
            "description": ARTICLE["metaDescription"],
        },
    }

    mutation = """mutation PageCreate($input: PageCreateInput!) {
        pageCreate(input: $input) {
            page { id slug title }
            errors { field message code }
        }
    }"""

    result = graphql_request(mutation, {"input": input_data})
    if not result:
        return None, "No response (plain fallback)"

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
    variables = {
        "id": page_id,
        "input": [{"key": "type", "value": "blog"}],
    }
    result = graphql_request(mutation, variables)
    if not result:
        return False, "No response"
    update = result.get("data", {}).get("updateMetadata", {})
    if update and update.get("errors"):
        err = update["errors"][0]
        return False, f"{err.get('field')}: {err.get('message')}"
    return True, None


def main():
    print()
    print("=" * 65)
    print("  Auric Jewels — May 2026 SEO Blog Publisher")
    print("  Target: diamond choker necklace bridal Gurgaon")
    print("=" * 65)
    print()

    # Read content
    content_path = os.path.join(CONTENT_DIR, ARTICLE["contentFile"])
    if not os.path.exists(content_path):
        print(f"  ERROR: Content file not found: {content_path}")
        sys.exit(1)

    with open(content_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    print(f"  Title:   {ARTICLE['title'][:65]}...")
    print(f"  Slug:    {ARTICLE['slug']}")
    print(f"  Content: {len(html_content):,} characters")
    print()

    # Attempt 1: EditorJS wrapper
    print("  [1/2] Publishing with EditorJS content format...")
    page, error = create_page(html_content)

    if error:
        print(f"  First attempt: {error}")
        print("  [2/2] Retrying with plain HTML content...")
        page, error = create_page_plain(html_content)

    if error:
        print(f"  FAILED: {error}")
        print()
        print("  Manual publish instructions:")
        print(f"  1. Open: https://auric.thecodemesh.online/dashboard/pages/add")
        print(f"  2. Page type: SEO Page (UGFnZVR5cGU6Ng==)")
        print(f"  3. Paste content from: {content_path}")
        print(f"  4. Slug: {ARTICLE['slug']}")
        sys.exit(1)

    page_id = page["id"]
    print(f"  Created page ID: {page_id}")

    # Add blog metadata
    print("  Adding metadata type=blog...")
    meta_ok, meta_err = add_blog_metadata(page_id)
    if meta_ok:
        print("  Metadata: OK")
    else:
        print(f"  Metadata warning: {meta_err}")

    print()
    print("=" * 65)
    print("  PUBLISHED SUCCESSFULLY")
    print(f"  URL: https://www.auricjewels.com/blog/{ARTICLE['slug']}")
    print("=" * 65)
    print()


if __name__ == "__main__":
    main()
