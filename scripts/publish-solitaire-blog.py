"""
Auric Jewels — Solitaire Blog Publisher (April 29, 2026 Session)
================================================================
Publishes: Solitaire Diamond Rings in Gurgaon — The 2026 Connoisseur's Guide

Run from the project root:
    python scripts/publish-solitaire-blog.py   (Mac/Linux)
    python scripts\\publish-solitaire-blog.py  (Windows)

No pip install needed — uses only Python stdlib.
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
    "title": "Solitaire Diamond Rings in Gurgaon — The 2026 Connoisseur's Guide",
    "slug": "solitaire-diamond-rings-gurgaon-2026-guide",
    "metaTitle": "Solitaire Diamond Rings in Gurgaon — 2026 Price & Buying Guide | Auric Jewels",
    "metaDescription": (
        "Planning to buy a solitaire diamond ring in Gurgaon? Auric Jewels offers "
        "IGI/GIA certified solitaires in round, oval, cushion and emerald cuts. "
        "Explore our 2026 solitaire buying guide."
    ),
    "contentFile": os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "content",
        "blog-solitaire-diamond-rings-gurgaon-2026.html",
    ),
    "channel": "franchise1",
}


def gql(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    req = urllib.request.Request(
        API_ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AUTH_TOKEN}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"  HTTP {e.code}: {e.reason}")
        if body:
            print(f"  Response: {body[:400]}")
        return {"error": f"HTTP {e.code}", "body": body}
    except urllib.error.URLError as e:
        print(f"  Connection error: {e.reason}")
        return {"error": str(e.reason)}


def publish():
    content_path = ARTICLE["contentFile"]
    if not os.path.exists(content_path):
        print(f"  ERROR: Content file not found: {content_path}")
        sys.exit(1)

    with open(content_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    print(f"  Title  : {ARTICLE['title']}")
    print(f"  Slug   : {ARTICLE['slug']}")
    print(f"  Content: {len(html_content):,} characters")
    print()

    editor_content = json.dumps({
        "blocks": [{"type": "rawHtml", "data": {"html": html_content}}]
    })

    mutation = """
    mutation PageCreate($input: PageCreateInput!) {
      pageCreate(input: $input) {
        page {
          id
          title
          slug
          isPublished
          url
        }
        errors {
          field
          message
          code
        }
      }
    }
    """

    variables = {
        "input": {
            "title": ARTICLE["title"],
            "slug": ARTICLE["slug"],
            "pageType": PAGE_TYPE_ID,
            "isPublished": True,
            "content": editor_content,
            "seo": {
                "title": ARTICLE["metaTitle"],
                "description": ARTICLE["metaDescription"],
            },
        }
    }

    print("  Calling Saleor pageCreate...")
    result = gql(mutation, variables)

    if "error" in result:
        print(f"  FAILED: {result['error']}")
        return False

    if result.get("errors"):
        print("  GraphQL top-level errors:")
        for e in result["errors"]:
            print(f"    - {e.get('message')}")
        return False

    page_data = result.get("data", {}).get("pageCreate", {})
    page_errors = page_data.get("errors", [])
    if page_errors:
        print("  pageCreate errors:")
        for e in page_errors:
            print(f"    - [{e.get('field')}] {e.get('message')} ({e.get('code')})")
        return False

    page = page_data.get("page", {})
    if page:
        print()
        print("  SUCCESS — Blog post published!")
        print(f"  Page ID   : {page.get('id')}")
        print(f"  Slug      : {page.get('slug')}")
        print(f"  Published : {page.get('isPublished')}")
        url = page.get("url") or f"https://www.auricjewels.com/blog/{ARTICLE['slug']}"
        print(f"  URL       : {url}")
        return True

    print("  Unexpected response:")
    print(f"  {json.dumps(result, indent=2)[:500]}")
    return False


def main():
    print()
    print("=" * 60)
    print("  Auric Jewels — Solitaire Blog Publisher")
    print("  Session: April 29, 2026")
    print("=" * 60)
    print()

    success = publish()

    print()
    if success:
        print("  Done. Blog is live at:")
        print(f"  https://www.auricjewels.com/blog/{ARTICLE['slug']}")
    else:
        print("  Publishing failed. Run this script from your local machine")
        print("  where the Saleor API is accessible.")
        print()
        print("  Alternatively, publish manually via the Saleor admin panel:")
        print(f"  Content file: content/blog-solitaire-diamond-rings-gurgaon-2026.html")
        print(f"  Page Type ID: {PAGE_TYPE_ID}")
        print(f"  Channel     : {ARTICLE['channel']}")
    print()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
