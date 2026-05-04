"""
Auric Jewels — Solitaire Ring Blog Publisher
=============================================
Publishes: blog-solitaire-ring-buying-guide-gurgaon-2026.html
Target URL: https://www.auricjewels.com/blog/solitaire-ring-buying-guide-gurgaon-2026

Run from an IP that is whitelisted for the Saleor API:
    python3 scripts/publish-solitaire-blog-2026.py
"""

import json, os, sys, time, urllib.request, urllib.error

API      = "https://auric.thecodemesh.online/graphql/"
TOKEN    = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
CHANNEL  = "franchise1"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

BLOG = {
    "title": "Solitaire Ring Buying Guide for Gurgaon — Cuts, Clarity & Choosing the Right Natural Diamond in 2026",
    "slug":  "solitaire-ring-buying-guide-gurgaon-2026",
    "seo_title": "Solitaire Ring Buying Guide Gurgaon — Cuts, Clarity & Price 2026 | Auric Jewels",
    "seo_description": (
        "Complete solitaire ring buying guide for Gurgaon. Learn about diamond cuts, "
        "clarity grades, 4Cs selection, and what to look for in a certified natural diamond. "
        "IGI/GIA certified solitaires at Auric Jewels, Gurugram."
    ),
    "content_file": os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "content",
        "blog-solitaire-ring-buying-guide-gurgaon-2026.html",
    ),
}


def gql(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    req = urllib.request.Request(
        API,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"  HTTP {e.code}: {e.reason}")
        print(f"  Body: {body[:400]}")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None


def html_to_editorjs(html_content):
    """Convert basic HTML to Saleor-compatible EditorJS JSON format."""
    import re
    blocks = []

    def clean(text):
        text = re.sub(r"<[^>]+>", "", text)
        text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&#39;", "'")
        return text.strip()

    def make_id():
        import random, string
        return "".join(random.choices(string.ascii_letters + string.digits, k=10))

    # Extract <h1> — becomes header level 1
    h1 = re.search(r"<h1>(.*?)</h1>", html_content, re.DOTALL)
    if h1:
        blocks.append({"id": make_id(), "type": "header", "data": {"text": clean(h1.group(1)), "level": 1}})

    # Extract all content in order: h2, h3, p, ul/li
    tag_pattern = re.compile(
        r"(<h2>(.*?)</h2>|<h3>(.*?)</h3>|<p>(.*?)</p>|<ul>(.*?)</ul>)",
        re.DOTALL,
    )
    for match in tag_pattern.finditer(html_content):
        full = match.group(0)
        if full.startswith("<h2>"):
            text = clean(re.search(r"<h2>(.*?)</h2>", full, re.DOTALL).group(1))
            blocks.append({"id": make_id(), "type": "header", "data": {"text": text, "level": 2}})
        elif full.startswith("<h3>"):
            text = clean(re.search(r"<h3>(.*?)</h3>", full, re.DOTALL).group(1))
            blocks.append({"id": make_id(), "type": "header", "data": {"text": text, "level": 3}})
        elif full.startswith("<p>"):
            text = clean(re.search(r"<p>(.*?)</p>", full, re.DOTALL).group(1))
            if text:
                blocks.append({"id": make_id(), "type": "paragraph", "data": {"text": text}})
        elif full.startswith("<ul>"):
            items = [clean(li) for li in re.findall(r"<li>(.*?)</li>", full, re.DOTALL) if clean(li)]
            if items:
                blocks.append({"id": make_id(), "type": "list", "data": {"style": "unordered", "items": items}})

    return json.dumps({"time": int(time.time() * 1000), "blocks": blocks, "version": "2.26.5"})


def publish():
    print("\nAuric Jewels — Solitaire Ring Blog Publisher")
    print("=" * 50)

    # Read HTML content
    if not os.path.exists(BLOG["content_file"]):
        print(f"Content file not found: {BLOG['content_file']}")
        sys.exit(1)

    with open(BLOG["content_file"], "r", encoding="utf-8") as f:
        html = f.read()

    content_json = html_to_editorjs(html)
    print(f"Title : {BLOG['title']}")
    print(f"Slug  : {BLOG['slug']}")
    print(f"Blocks: {len(json.loads(content_json)['blocks'])} EditorJS blocks")
    print()

    # pageCreate mutation — Saleor CMS standard
    mutation = """
    mutation PageCreate($input: PageCreateInput!) {
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
            "title":       BLOG["title"],
            "slug":        BLOG["slug"],
            "pageType":    PAGE_TYPE_ID,
            "isPublished": True,
            "content":     content_json,
            "seo": {
                "title":       BLOG["seo_title"],
                "description": BLOG["seo_description"],
            },
        }
    }

    print("Calling pageCreate mutation...")
    result = gql(mutation, variables)

    if not result:
        print("No response from API — check network / IP allowlist.")
        sys.exit(1)

    if "errors" in result and result["errors"]:
        print("GraphQL errors:")
        for e in result["errors"]:
            print(f"  {e.get('message', e)}")
        sys.exit(1)

    page_data = (result.get("data") or {}).get("pageCreate") or {}
    errs = page_data.get("errors") or []
    if errs:
        print("pageCreate errors:")
        for e in errs:
            print(f"  [{e.get('field')}] {e.get('code')}: {e.get('message')}")
        sys.exit(1)

    page = page_data.get("page") or {}
    print()
    print("SUCCESS — Blog published!")
    print(f"  Saleor ID : {page.get('id')}")
    print(f"  Slug      : {page.get('slug')}")
    print(f"  Published : {page.get('isPublished')}")
    print(f"  Live URL  : https://www.auricjewels.com/blog/{page.get('slug')}")


if __name__ == "__main__":
    publish()
