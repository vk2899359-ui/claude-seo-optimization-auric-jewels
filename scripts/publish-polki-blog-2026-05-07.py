#!/usr/bin/env python3
"""
Auric Jewels — Publish: Polki Bridal Jewellery Gurgaon 2026
============================================================
Session date : 2026-05-07
Keyword target: polki bridal jewellery gurgaon 2026
Blog slug     : polki-bridal-jewellery-gurgaon-2026

RUN:
    python3 scripts/publish-polki-blog-2026-05-07.py

No pip install needed — stdlib only.
"""

import json
import os
import sys
import urllib.request
import urllib.error

API_ENDPOINT = "https://auric.thecodemesh.online/graphql/"
AUTH_TOKEN   = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

ARTICLE = {
    "title"           : "Polki Bridal Jewellery in Gurgaon — The 2026 Bride’s Guide to Uncut Diamond Grandeur",
    "slug"            : "polki-bridal-jewellery-gurgaon-2026",
    "metaTitle"       : "Polki Bridal Jewellery in Gurgaon 2026 | Uncut Diamond Sets | Auric Jewels",
    "metaDescription" : "Discover the finest Polki bridal jewellery in Gurgaon. Auric Jewels presents handcrafted uncut diamond Polki sets in 22K gold — heirloom-quality bridal parures for 2026 weddings.",
    "contentFile"     : os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "content",
        "blog-polki-bridal-jewellery-gurgaon-2026.html",
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
            "Content-Type" : "application/json",
            "Authorization": f"Bearer {AUTH_TOKEN}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        print(f"  HTTP {e.code}: {e.reason}")
        if body:
            print(f"  Body: {body[:400]}")
        return None
    except urllib.error.URLError as e:
        print(f"  Connection error: {e.reason}")
        return None


def create_page(content_html):
    editor_content = json.dumps({
        "blocks": [{"type": "rawHtml", "data": {"html": content_html}}]
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
            "slug"       : ARTICLE["slug"],
            "title"      : ARTICLE["title"],
            "pageType"   : PAGE_TYPE_ID,
            "isPublished": True,
            "content"    : editor_content,
            "seo"        : {
                "title"      : ARTICLE["metaTitle"],
                "description": ARTICLE["metaDescription"],
            },
        }
    }
    return graphql_request(mutation, variables)


def add_blog_metadata(page_id):
    mutation = """mutation UpdateMetadata($id: ID!, $input: [MetadataInput!]!) {
        updateMetadata(id: $id, input: $input) {
            item { metadata { key value } }
            errors { field message }
        }
    }"""
    return graphql_request(mutation, {
        "id"   : page_id,
        "input": [{"key": "type", "value": "blog"}],
    })


def main():
    print()
    print("=" * 60)
    print("  Auric Jewels — SEO Blog Publisher")
    print("  2026-05-07 | Polki Bridal Jewellery Gurgaon")
    print("=" * 60)

    # Read HTML content
    content_path = ARTICLE["contentFile"]
    if not os.path.exists(content_path):
        print(f"\n  ERROR: Content file not found:\n  {content_path}")
        sys.exit(1)

    with open(content_path, "r", encoding="utf-8") as f:
        content_html = f.read()

    print(f"\n  Title   : {ARTICLE['title']}")
    print(f"  Slug    : {ARTICLE['slug']}")
    print(f"  Content : {len(content_html)} chars")
    print()

    # Publish
    print("  Publishing via pageCreate …")
    result = create_page(content_html)

    if not result:
        print("  FAILED — no response. Check your network & token.")
        sys.exit(1)

    if result.get("errors"):
        print(f"  GraphQL errors: {result['errors']}")
        sys.exit(1)

    page_create = result.get("data", {}).get("pageCreate", {})
    if page_create.get("errors"):
        errs = page_create["errors"]
        print(f"  pageCreate errors: {errs}")
        sys.exit(1)

    page = page_create.get("page")
    if not page:
        print(f"  Unexpected response: {json.dumps(result)[:300]}")
        sys.exit(1)

    page_id = page["id"]
    print(f"  Published! ID: {page_id}")
    print(f"  URL: https://www.auricjewels.com/blog/{ARTICLE['slug']}")

    # Tag as blog
    print("\n  Adding blog metadata tag …")
    meta_result = add_blog_metadata(page_id)
    if meta_result and not (meta_result.get("errors") or {}):
        print("  Metadata updated: type=blog")
    else:
        print(f"  Metadata note: {meta_result}")

    print()
    print("  Done! Blog post is live.")
    print(f"  https://www.auricjewels.com/blog/{ARTICLE['slug']}")
    print()


if __name__ == "__main__":
    main()
