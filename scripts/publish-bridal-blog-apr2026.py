#!/usr/bin/env python3
"""
Auric Jewels — Publish Bridal Diamond Jewellery Blog (April 2026)
==================================================================
Session: 2026-04-24
Target Keyword: bridal diamond jewellery Gurgaon

USAGE:
    python3 scripts/publish-bridal-blog-apr2026.py
"""

import json
import os
import sys
import urllib.request
import urllib.error

API_ENDPOINT = "https://auric.thecodemesh.online/graphql/"
AUTH_TOKEN = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

ARTICLE = {
    "title": "Bridal Diamond Jewellery Gurgaon — The Complete Guide for the 2026 Bride",
    "slug": "bridal-diamond-jewellery-gurgaon",
    "metaTitle": "Bridal Diamond Jewellery Gurgaon | Auric Jewels — Wedding Jewellery Atelier",
    "metaDescription": (
        "Discover Gurgaon's most distinguished bridal diamond jewellery at Auric Jewels. "
        "GIA-certified solitaires, diamond chokers, heritage bridal sets — "
        "curated for the discerning 2026 bride."
    ),
    "contentFile": os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "content",
        "blog-bridal-diamond-jewellery-gurgaon.html",
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
            print(f"  Response: {body[:500]}")
        return None
    except urllib.error.URLError as e:
        print(f"  Connection error: {e.reason}")
        return None


def create_page(html_content):
    editor_content = json.dumps({
        "blocks": [{"type": "rawHtml", "data": {"html": html_content}}]
    })

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

    variables = {
        "input": {
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
    }

    result = graphql_request(mutation, variables)
    if not result:
        return None, "No response from API"

    if "errors" in result and result["errors"]:
        return None, result["errors"][0].get("message", str(result["errors"]))

    pc = result.get("data", {}).get("pageCreate", {})
    if pc.get("errors"):
        err = pc["errors"][0]
        return None, f"{err.get('field', '?')}: {err.get('message', '?')} ({err.get('code', '?')})"

    page = pc.get("page")
    if page:
        return page, None

    return None, f"Unexpected response: {json.dumps(result)[:300]}"


def add_blog_metadata(page_id):
    mutation = """mutation UpdateMetadata($id: ID!, $input: [MetadataInput!]!) {
        updateMetadata(id: $id, input: $input) {
            item {
                metadata { key value }
            }
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
    if "errors" in result and result["errors"]:
        return False, result["errors"][0].get("message", "Unknown error")
    update = result.get("data", {}).get("updateMetadata", {})
    if update and update.get("errors"):
        err = update["errors"][0]
        return False, f"{err.get('field')}: {err.get('message')}"
    return True, None


def main():
    print()
    print("=" * 60)
    print("  Auric Jewels — Bridal Blog Publisher (April 2026)")
    print("=" * 60)
    print(f"  Title : {ARTICLE['title']}")
    print(f"  Slug  : {ARTICLE['slug']}")
    print()

    content_path = ARTICLE["contentFile"]
    if not os.path.exists(content_path):
        print(f"  ERROR: Content file not found: {content_path}")
        sys.exit(1)

    with open(content_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    print(f"  Content: {len(html_content):,} characters")

    print("  Publishing via Saleor pageCreate...")
    page, error = create_page(html_content)

    if error:
        print(f"  FAILED: {error}")
        sys.exit(1)

    page_id = page["id"]
    print(f"  SUCCESS — Page ID: {page_id}")
    print(f"  URL: https://www.auricjewels.com/blog/{ARTICLE['slug']}")

    print("  Adding type=blog metadata...")
    ok, meta_err = add_blog_metadata(page_id)
    if ok:
        print("  Metadata added.")
    else:
        print(f"  Metadata warning: {meta_err}")

    print()
    print("  Published: https://www.auricjewels.com/blog/bridal-diamond-jewellery-gurgaon")
    print()
    sys.exit(0)


if __name__ == "__main__":
    main()
