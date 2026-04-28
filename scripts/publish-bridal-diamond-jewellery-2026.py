"""
Auric Jewels — Publish: Bridal Diamond Jewellery Gurgaon 2026
=============================================================
Target keyword : bridal diamond jewellery Gurgaon 2026
Blog file      : content/blog-bridal-diamond-jewellery-gurgaon-2026.html
Saleor endpoint: https://auric.thecodemesh.online/graphql/
Channel        : franchise1
Page Type ID   : UGFnZVR5cGU6Ng==

NOTE: Run this from your LOCAL machine — the Saleor API blocks
      requests from the CI/sandbox environment by IP allowlist.

USAGE:
    python3 scripts/publish-bridal-diamond-jewellery-2026.py
"""

import json
import os
import sys
import urllib.request
import urllib.error

API_ENDPOINT = "https://auric.thecodemesh.online/graphql/"
AUTH_TOKEN   = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
CHANNEL      = "franchise1"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

BLOG = {
    "title": (
        "The 2026 Bridal Diamond Jewellery Edit: "
        "What Gurgaon's Most Refined Brides Are Wearing This Wedding Season"
    ),
    "slug": "bridal-diamond-jewellery-gurgaon-2026",
    "seo_title": "Bridal Diamond Jewellery Gurgaon 2026 | Auric Jewels",
    "seo_description": (
        "Discover the most exquisite bridal diamond jewellery trends for 2026 "
        "at Auric Jewels, Gurgaon. Toi et moi rings, oval solitaires, diamond "
        "chokers and curated bridal sets — for the discerning bride."
    ),
    "content_file": os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "content",
        "blog-bridal-diamond-jewellery-gurgaon-2026.html",
    ),
}


def gql(query, variables=None):
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
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        print(f"  HTTP {e.code}: {e.reason}  {body[:300]}")
        return None
    except urllib.error.URLError as e:
        print(f"  Connection error: {e.reason}")
        return None


def build_editorjs_content(html_content):
    """
    Wrap the raw HTML in an EditorJS-compatible JSON structure.
    Saleor accepts raw HTML in the content field for rich text attributes.
    """
    blocks = []
    import re

    # Split on block-level tags and build paragraph blocks
    # Simple approach: one paragraph block per <p> tag, headers for <h2>/<h3>
    h2_parts = re.split(r'(<h2[^>]*>.*?</h2>)', html_content, flags=re.DOTALL)
    for part in h2_parts:
        part = part.strip()
        if not part:
            continue
        if part.startswith("<h2"):
            text = re.sub(r'<[^>]+>', '', part).strip()
            blocks.append({"id": f"h2_{len(blocks)}", "type": "header", "data": {"text": text, "level": 2}})
        else:
            # Extract paragraphs
            paras = re.findall(r'<p[^>]*>(.*?)</p>', part, flags=re.DOTALL)
            for para in paras:
                para = para.strip()
                if para:
                    blocks.append({"id": f"p_{len(blocks)}", "type": "paragraph", "data": {"text": para}})

    if not blocks:
        blocks.append({"id": "p_0", "type": "paragraph", "data": {"text": html_content[:500]}})

    return json.dumps({"time": 1745827200000, "blocks": blocks, "version": "2.26.5"})


def publish():
    content_path = BLOG["content_file"]
    if not os.path.exists(content_path):
        print(f"ERROR: Content file not found: {content_path}")
        sys.exit(1)

    with open(content_path, "r", encoding="utf-8") as f:
        raw_html = f.read()

    editorjs_content = build_editorjs_content(raw_html)

    print(f"Title : {BLOG['title']}")
    print(f"Slug  : {BLOG['slug']}")
    print(f"Chars : {len(raw_html)}")
    print()

    mutation = """
    mutation CreatePage($input: PageCreateInput!) {
      pageCreate(input: $input) {
        page {
          id
          title
          slug
          isPublished
          publicationDate
        }
        errors {
          field
          code
          message
        }
      }
    }
    """

    variables = {
        "input": {
            "title": BLOG["title"],
            "slug": BLOG["slug"],
            "pageType": PAGE_TYPE_ID,
            "content": editorjs_content,
            "isPublished": True,
            "seo": {
                "title": BLOG["seo_title"],
                "description": BLOG["seo_description"],
            },
        }
    }

    print("Calling pageCreate mutation...")
    result = gql(mutation, variables)

    if not result:
        print("No response from API. Is this running from your local machine?")
        sys.exit(1)

    if "errors" in result:
        print("GraphQL errors:")
        for err in result["errors"]:
            print(f"  {err.get('message')}")
        sys.exit(1)

    page_data = result.get("data", {}).get("pageCreate", {})
    page_errors = page_data.get("errors", [])
    if page_errors:
        print("Mutation errors:")
        for err in page_errors:
            print(f"  [{err.get('field')}] {err.get('code')}: {err.get('message')}")
        sys.exit(1)

    page = page_data.get("page", {})
    print()
    print("SUCCESS — Blog post published to Saleor CMS")
    print(f"  ID          : {page.get('id')}")
    print(f"  Slug        : {page.get('slug')}")
    print(f"  Published   : {page.get('isPublished')}")
    print()
    print(f"  Live URL    : https://www.auricjewels.com/blog/{BLOG['slug']}")


if __name__ == "__main__":
    publish()
