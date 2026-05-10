#!/usr/bin/env python3
"""
Auric Jewels — Publish Polki & Jadau Bridal Jewellery Blog (May 2026)
======================================================================

USAGE:
    python3 scripts/publish-polki-jadau-blog.py

This script:
  1. Reads the HTML blog file from content/
  2. Publishes via Saleor pageCreate GraphQL mutation
  3. Adds type=blog metadata so it appears on /blog listing
  4. Reports the published URL

API: https://auric.thecodemesh.online/graphql/
Page Type ID: UGFnZVR5cGU6Ng==
"""

import json
import os
import sys
import urllib.request
import urllib.error

API_ENDPOINT = "https://auric.thecodemesh.online/graphql/"
AUTH_TOKEN = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

CONTENT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "content",
)

ARTICLE = {
    "title": "Polki & Jadau Bridal Jewellery in Gurgaon — The Art of Royal Adornment",
    "slug": "polki-jadau-bridal-jewellery-gurgaon",
    "metaTitle": "Polki & Jadau Bridal Jewellery in Gurgaon — The Art of Royal Adornment | Auric Jewels",
    "metaDescription": (
        "Discover the finest Polki and Jadau bridal jewellery in Gurgaon at Auric Jewels. "
        "Curated heirloom sets for the discerning bride — uncut diamonds, handcrafted Jadau, "
        "and heritage craftsmanship. Visit our Gurugram showroom."
    ),
    "contentFile": "blog-polki-jadau-bridal-jewellery-gurgaon.html",
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
        print(f"    HTTP {e.code}: {e.reason}")
        if body:
            print(f"    Response: {body[:500]}")
        return None
    except urllib.error.URLError as e:
        print(f"    Connection error: {e.reason}")
        return None


def create_page(article, content):
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
    mutation = """mutation UpdateMetadata($id: ID!, $input: [MetadataInput!]!) {
        updateMetadata(id: $id, input: $input) {
            item {
                metadata { key value }
            }
            errors { field message }
        }
    }"""
    result = graphql_request(mutation, {
        "id": page_id,
        "input": [{"key": "type", "value": "blog"}],
    })
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
    print("  Auric Jewels — Publish Polki & Jadau Bridal Blog")
    print("  Saleor CMS via GraphQL API")
    print("=" * 60)
    print()
    print(f"  API:  {API_ENDPOINT}")
    print(f"  Slug: {ARTICLE['slug']}")
    print()

    content_path = os.path.join(CONTENT_DIR, ARTICLE["contentFile"])
    if not os.path.exists(content_path):
        print(f"  ERROR: Content file not found: {content_path}")
        sys.exit(1)

    with open(content_path, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"  Content: {len(content):,} characters loaded")
    print(f"  Creating page...")

    page, error = create_page(ARTICLE, content)

    if error:
        print(f"  First attempt failed: {error}")
        print(f"  Retrying with plain HTML content...")
        input_data = {
            "slug": ARTICLE["slug"],
            "title": ARTICLE["title"],
            "pageType": PAGE_TYPE_ID,
            "isPublished": True,
            "content": content,
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
        if result:
            pc = result.get("data", {}).get("pageCreate", {})
            if pc.get("page") and not pc.get("errors"):
                page = pc["page"]
                error = None
            elif pc.get("errors"):
                err = pc["errors"][0]
                error = f"{err.get('field')}: {err.get('message')}"

    if not page:
        print(f"  FAILED to create page: {error}")
        sys.exit(1)

    print(f"  Page created: {page['id']}")

    print(f"  Adding blog metadata...")
    ok, meta_error = add_blog_metadata(page["id"])
    if ok:
        print(f"  Metadata added (type=blog)")
    else:
        print(f"  Metadata warning: {meta_error}")

    print()
    print("  SUCCESS!")
    print(f"  Title: {page['title']}")
    print(f"  URL:   https://www.auricjewels.com/blog/{page['slug']}")
    print()


if __name__ == "__main__":
    main()
