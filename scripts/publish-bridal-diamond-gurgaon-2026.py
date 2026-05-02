#!/usr/bin/env python3
"""
Auric Jewels — Publish: Bridal Diamond Jewellery Gurgaon 2026
=============================================================
Session: 2026-05-02
Target keyword: bridal diamond jewellery Gurgaon 2026
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
    "title": "Bridal Diamond Jewellery in Gurgaon 2026 — The Complete Trousseau Guide",
    "slug": "bridal-diamond-jewellery-gurgaon-2026",
    "metaTitle": "Bridal Diamond Jewellery Gurgaon 2026 — Complete Trousseau Guide | Auric Jewels",
    "metaDescription": (
        "Discover the finest bridal diamond jewellery in Gurgaon for 2026. "
        "Solitaire sets, polki-diamond hybrids, emerald combinations & layered "
        "necklaces. Private bridal consultations at Auric Jewels, Sector 45."
    ),
    "contentFile": "blog-bridal-diamond-jewellery-gurgaon-2026.html",
}

CONTENT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "content",
)


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


def create_page(content):
    editor_content = json.dumps({
        "blocks": [{"type": "rawHtml", "data": {"html": content}}]
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

    return graphql_request(mutation, variables)


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
    return graphql_request(mutation, variables)


def main():
    print()
    print("=" * 60)
    print("  Auric Jewels — Publish Bridal Diamond Blog (May 2026)")
    print("=" * 60)
    print(f"  Title: {ARTICLE['title']}")
    print(f"  Slug:  {ARTICLE['slug']}")
    print()

    content_path = os.path.join(CONTENT_DIR, ARTICLE["contentFile"])
    if not os.path.exists(content_path):
        print(f"  ERROR: Content file not found: {content_path}")
        sys.exit(1)

    with open(content_path, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"  Content: {len(content):,} characters")
    print()

    print("  Creating page via Saleor pageCreate...")
    result = create_page(content)

    if not result:
        print("  ERROR: No response from API.")
        sys.exit(1)

    if "errors" in result and result["errors"]:
        print(f"  ERROR: {result['errors'][0].get('message', result['errors'])}")
        sys.exit(1)

    page_create = result.get("data", {}).get("pageCreate", {})
    if page_create.get("errors"):
        err = page_create["errors"][0]
        print(f"  ERROR: {err.get('field', '?')}: {err.get('message', '?')} ({err.get('code', '?')})")
        sys.exit(1)

    page = page_create.get("page")
    if not page:
        print(f"  ERROR: Unexpected response: {json.dumps(result)[:300]}")
        sys.exit(1)

    page_id = page["id"]
    print(f"  SUCCESS — Page created (ID: {page_id})")
    print()

    print("  Adding metadata type=blog...")
    meta_result = add_blog_metadata(page_id)
    if meta_result:
        meta_update = meta_result.get("data", {}).get("updateMetadata", {})
        if meta_update and not meta_update.get("errors"):
            print("  Metadata added successfully.")
        else:
            errs = (meta_update or {}).get("errors", [])
            print(f"  Metadata warning: {errs}")
    else:
        print("  Metadata: no response (non-fatal).")

    print()
    print("=" * 60)
    url = f"https://www.auricjewels.com/blog/{ARTICLE['slug']}"
    print(f"  PUBLISHED: {url}")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
