"""
Auric Jewels — Publish Polki Bridal Blog Post (2026-05-05)
==========================================================

Run from any machine with internet access to the Saleor endpoint:

    python3 scripts/publish-polki-blog.py

Target keyword : polki jewellery set for brides 2026
Blog URL       : https://www.auricjewels.com/blog/polki-jewellery-set-brides-2026
Page Type ID   : UGFnZVR5cGU6Ng==
Channel        : franchise1
"""

import json
import os
import sys
import urllib.request
import urllib.error

API = "https://auric.thecodemesh.online/graphql/"
TOKEN = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"

BLOG_TITLE = "Polki Jewellery Sets for Brides 2026 — Where Ancient Craft Meets Modern Royalty"
BLOG_SLUG = "polki-jewellery-set-brides-2026"
META_TITLE = "Polki Jewellery Sets for Brides 2026 | Luxury Bridal Jewellery | Auric Jewels Gurgaon"
META_DESCRIPTION = (
    "Discover exquisite Polki jewellery sets for brides in 2026 at Auric Jewels, Gurugram. "
    "Jadau craftsmanship, uncut diamonds & pastel meenakari for the modern maharani."
)
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

CONTENT_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "content",
    "blog-polki-jewellery-set-brides-2026.html",
)


def graphql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = urllib.request.Request(
        API,
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"  HTTP {e.code}: {e.reason} — {body[:300]}")
        return None
    except Exception as ex:
        print(f"  Error: {ex}")
        return None


def html_to_editorjs(html_content):
    """Minimal HTML → EditorJS JSON conversion for Saleor content field."""
    import re, time

    blocks = []
    # Strip <article> wrapper
    html_content = re.sub(r"</?article>", "", html_content).strip()

    # Split on block-level tags
    parts = re.split(r"(<h[1-6][^>]*>.*?</h[1-6]>|<p[^>]*>.*?</p>|<ul>.*?</ul>)", html_content, flags=re.DOTALL)

    def clean(text):
        return re.sub(r"\s+", " ", text).strip()

    for part in parts:
        part = part.strip()
        if not part:
            continue
        m = re.match(r"<h([1-6])[^>]*>(.*?)</h[1-6]>", part, re.DOTALL)
        if m:
            level = int(m.group(1))
            text = clean(re.sub(r"<[^>]+>", "", m.group(2)))
            blocks.append({"type": "header", "data": {"text": text, "level": level}})
            continue
        m = re.match(r"<p[^>]*>(.*?)</p>", part, re.DOTALL)
        if m:
            text = clean(m.group(1))
            if text:
                blocks.append({"type": "paragraph", "data": {"text": text}})
            continue
        m = re.match(r"<ul>(.*?)</ul>", part, re.DOTALL)
        if m:
            items = re.findall(r"<li[^>]*>(.*?)</li>", m.group(1), re.DOTALL)
            items = [clean(re.sub(r"<[^>]+>", "", i)) for i in items if clean(re.sub(r"<[^>]+>", "", i))]
            if items:
                blocks.append({"type": "list", "data": {"style": "unordered", "items": items}})
            continue

    return json.dumps({"time": int(time.time() * 1000), "blocks": blocks, "version": "2.26.5"})


def publish():
    print("\n  Auric Jewels — Polki Blog Publisher")
    print(f"  Endpoint : {API}")
    print(f"  Title    : {BLOG_TITLE}")
    print(f"  Slug     : {BLOG_SLUG}\n")

    if not os.path.exists(CONTENT_FILE):
        print(f"  Content file not found: {CONTENT_FILE}")
        sys.exit(1)

    with open(CONTENT_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    editorjs_content = html_to_editorjs(html)
    print(f"  Content  : {len(html)} chars HTML → {len(editorjs_content)} chars EditorJS JSON\n")

    mutation = """
    mutation CreatePage($input: PageCreateInput!) {
      pageCreate(input: $input) {
        page {
          id
          title
          slug
          isPublished
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
            "title": BLOG_TITLE,
            "slug": BLOG_SLUG,
            "pageType": PAGE_TYPE_ID,
            "isPublished": True,
            "content": editorjs_content,
            "seo": {
                "title": META_TITLE,
                "description": META_DESCRIPTION,
            },
        }
    }

    print("  Sending pageCreate mutation...")
    result = graphql(mutation, variables)

    if not result:
        print("\n  FAILED — no response from API.")
        print("  Note: The Saleor endpoint may have an IP allowlist.")
        print("  Run this script from your local machine or a whitelisted server.")
        sys.exit(1)

    if "errors" in result:
        print("\n  GraphQL errors:")
        for e in result["errors"]:
            print(f"    - {e.get('message')}")
        sys.exit(1)

    page_data = result.get("data", {}).get("pageCreate", {})
    user_errors = page_data.get("errors", [])
    if user_errors:
        print("\n  User errors:")
        for e in user_errors:
            print(f"    [{e.get('field')}] {e.get('message')} ({e.get('code')})")
        sys.exit(1)

    page = page_data.get("page", {})
    print("\n  SUCCESS!")
    print(f"  ID         : {page.get('id')}")
    print(f"  Title      : {page.get('title')}")
    print(f"  Published  : {page.get('isPublished')}")
    print(f"  URL        : https://www.auricjewels.com/blog/{page.get('slug')}")


if __name__ == "__main__":
    publish()
