#!/usr/bin/env python3
"""
Auric Jewels — Publish Session Blog: 27 April 2026
===================================================
Run from a host whitelisted by the Saleor API:
    python3 scripts/publish-session-2026-04-27.py

API: https://auric.thecodemesh.online/graphql/
Channel: franchise1
Page Type: UGFnZVR5cGU6Ng==
"""

import json, os, sys, urllib.request, urllib.error

API = "https://auric.thecodemesh.online/graphql/"
TOKEN = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

ARTICLE = {
    "title": "Choosing the Perfect Solitaire Diamond Ring for Your Wedding — A Luxury Guide for the 2026 Bride",
    "slug": "solitaire-diamond-ring-wedding-2026-guide",
    "metaTitle": "Perfect Solitaire Diamond Ring for Wedding 2026 | Auric Jewels Gurgaon",
    "metaDescription": "Expert guide to choosing a solitaire diamond ring for your wedding. IGI/GIA certified solitaires, cut, clarity & setting advice from Auric Jewels Gurugram.",
    "contentFile": os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "content", "blog-solitaire-diamond-ring-wedding-2026-guide.html",
    ),
}


def gql(query, variables=None):
    payload = json.dumps({"query": query, **({"variables": variables} if variables else {})}).encode()
    req = urllib.request.Request(
        API, data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"HTTP {e.code}: {e.reason}\n{body[:400]}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    print("Auric Jewels — Session Blog Publisher (27 Apr 2026)")
    print("=" * 55)

    with open(ARTICLE["contentFile"], "r", encoding="utf-8") as f:
        html = f.read()

    print(f"Title : {ARTICLE['title'][:65]}...")
    print(f"Slug  : {ARTICLE['slug']}")
    print(f"Size  : {len(html):,} chars")
    print()

    editor_content = json.dumps({"blocks": [{"type": "rawHtml", "data": {"html": html}}]})

    result = gql(
        """mutation PageCreate($input: PageCreateInput!) {
            pageCreate(input: $input) {
                page { id slug title }
                errors { field message code }
            }
        }""",
        {"input": {
            "slug": ARTICLE["slug"],
            "title": ARTICLE["title"],
            "pageType": PAGE_TYPE_ID,
            "isPublished": True,
            "content": editor_content,
            "seo": {"title": ARTICLE["metaTitle"], "description": ARTICLE["metaDescription"]},
        }},
    )

    if not result:
        print("No response from API.")
        sys.exit(1)

    pc = result.get("data", {}).get("pageCreate", {})
    errors = pc.get("errors", [])
    page = pc.get("page")

    if errors:
        print(f"ERRORS: {errors}")
        sys.exit(1)

    if not page:
        print(f"Unexpected response: {json.dumps(result)[:300]}")
        sys.exit(1)

    print(f"PUBLISHED: https://www.auricjewels.com/blog/{page['slug']}")
    print(f"Page ID  : {page['id']}")

    # Add metadata type=blog
    meta = gql(
        """mutation UpdateMetadata($id: ID!, $input: [MetadataInput!]!) {
            updateMetadata(id: $id, input: $input) {
                item { metadata { key value } }
                errors { field message }
            }
        }""",
        {"id": page["id"], "input": [{"key": "type", "value": "blog"}]},
    )
    if meta and not (meta.get("data", {}).get("updateMetadata", {}).get("errors") or []):
        print("Metadata : type=blog added")
    else:
        print(f"Metadata : failed — {meta}")

    print("\nDone.")


if __name__ == "__main__":
    main()
