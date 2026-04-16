"""
Auric Jewels — Bulk Saleor Publisher (30 Trending Blog Posts)
=============================================================
Reads all blog-*.html files from content/, extracts title + slug from
the HTML <h1> and filename, then pushes each as a DRAFT page to Saleor
via the pageCreate GraphQL mutation.

USAGE:
    export SALEOR_TOKEN="your-saleor-token-here"
    python3 scripts/publish_all.py

    # Or pass token directly:
    SALEOR_TOKEN=abc123 python3 scripts/publish_all.py
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

# ── Configuration ────────────────────────────────────────────
API_ENDPOINT = "https://auric.thecodemesh.online/graphql/"
CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content")

# Token from environment variable
TOKEN = os.environ.get("SALEOR_TOKEN", "")

# These are the 30 NEW blog files (exclude pre-existing ones)
EXCLUDE_PREFIXES = [
    "blog-01-",
    "blog-gold-jewellery-investment-2026",
    "blog-lab-grown-vs-natural-diamonds",
    "blog-jewellery-trends-india-2026",
    "blog-layered-necklace-styling",
    "blog-lightweight-gold-jewellery",
    "blog-platinum-jewellery-men",
]


def get_token():
    """Get the Saleor auth token."""
    if TOKEN:
        return TOKEN
    print("ERROR: SALEOR_TOKEN environment variable not set.")
    print("  export SALEOR_TOKEN='your-token-here'")
    sys.exit(1)


def gql(query, variables=None, token=None):
    """Send a GraphQL request to Saleor."""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_ENDPOINT,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        return {"errors": [{"message": f"HTTP {e.code}: {body[:300]}"}]}
    except urllib.error.URLError as e:
        return {"errors": [{"message": f"Connection error: {e.reason}"}]}
    except Exception as e:
        return {"errors": [{"message": str(e)}]}


def find_page_type(token):
    """Discover the best page type ID from Saleor."""
    print("  Finding page types...")
    r = gql("{pageTypes(first:20){edges{node{id name slug}}}}", token=token)
    if "errors" in r and r["errors"]:
        msg = r["errors"][0].get("message", "")
        if "permission" in msg.lower() or "MANAGE_PAGES" in msg:
            print(f"  PERMISSION ERROR: {msg}")
            print("  Your token lacks MANAGE_PAGES permission. Stop.")
            sys.exit(2)
        print(f"  Warning: {msg}")
        return None

    types = []
    edges = (r.get("data") or {}).get("pageTypes", {}).get("edges", [])
    for edge in edges:
        node = edge.get("node", {})
        types.append(node)
        print(f"    Page type: {node.get('name')} (ID: {node.get('id')})")

    if not types:
        print("  No page types found. Will try without pageType.")
        return None

    # Prefer a blog/seo/article type, fallback to first
    for t in types:
        combined = (t.get("name", "") + t.get("slug", "")).lower()
        if any(kw in combined for kw in ["seo", "blog", "article", "post", "content"]):
            print(f"  Using: {t['name']} ({t['id']})")
            return t["id"]

    print(f"  Using first type: {types[0]['name']} ({types[0]['id']})")
    return types[0]["id"]


def extract_h1(html_content):
    """Extract the first <h1> text from HTML content."""
    match = re.search(r"<h1>(.*?)</h1>", html_content, re.DOTALL)
    if match:
        # Strip any HTML tags inside the h1
        text = re.sub(r"<[^>]+>", "", match.group(1))
        return text.strip()
    return None


def filename_to_slug(filename):
    """Convert a blog filename to a URL slug."""
    # blog-akshaya-tritiya-2026-gold-jewellery-buying-guide.html -> akshaya-tritiya-2026-gold-jewellery-buying-guide
    slug = filename.replace(".html", "")
    if slug.startswith("blog-"):
        slug = slug[5:]
    return slug


def build_meta_description(html_content):
    """Extract first <p> as meta description, truncated to 155 chars."""
    match = re.search(r"<p>(.*?)</p>", html_content, re.DOTALL)
    if match:
        text = re.sub(r"<[^>]+>", "", match.group(1)).strip()
        if len(text) > 155:
            text = text[:152].rsplit(" ", 1)[0] + "..."
        return text
    return ""


def discover_blog_files():
    """Find all 30 new blog HTML files in the content directory."""
    files = []
    for fname in sorted(os.listdir(CONTENT_DIR)):
        if not fname.startswith("blog-") or not fname.endswith(".html"):
            continue
        # Skip pre-existing blogs
        if any(fname.startswith(prefix) for prefix in EXCLUDE_PREFIXES):
            continue
        files.append(fname)
    return files


def publish_page(article, page_type_id, token):
    """Push a single article to Saleor as a DRAFT page."""
    input_data = {
        "slug": article["slug"],
        "title": article["title"],
        "isPublished": False,  # DRAFT mode
        "seo": {
            "title": article["metaTitle"],
            "description": article["metaDescription"],
        },
    }

    # Add content as EditorJS JSON with rawHtml block
    if article.get("content"):
        input_data["content"] = json.dumps({
            "blocks": [{"type": "rawHtml", "data": {"html": article["content"]}}]
        })

    if page_type_id:
        input_data["pageType"] = page_type_id

    mutation = """mutation PageCreate($input: PageCreateInput!) {
        pageCreate(input: $input) {
            page { id slug title }
            errors { field message code }
        }
    }"""

    r = gql(mutation, {"input": input_data}, token=token)

    # Check for top-level GraphQL errors
    if r.get("errors"):
        msg = r["errors"][0].get("message", "Unknown error")
        if "permission" in msg.lower() or "MANAGE_PAGES" in msg.upper():
            return {"ok": False, "error": msg, "permission_error": True}
        return {"ok": False, "error": msg}

    data = r.get("data", {}).get("pageCreate", {})
    page = data.get("page")
    errors = data.get("errors", [])

    if page and not errors:
        return {"ok": True, "data": page}

    if errors:
        err = errors[0]
        msg = f"{err.get('field', '?')}: {err.get('message', '?')} ({err.get('code', '?')})"
        if "permission" in msg.lower():
            return {"ok": False, "error": msg, "permission_error": True}
        # If content field fails, retry without content
        if err.get("field") == "content":
            del input_data["content"]
            r2 = gql(mutation, {"input": input_data}, token=token)
            data2 = r2.get("data", {}).get("pageCreate", {})
            page2 = data2.get("page")
            errors2 = data2.get("errors", [])
            if page2 and not errors2:
                return {"ok": True, "data": page2, "note": "published without content (add via CMS)"}
            if errors2:
                return {"ok": False, "error": f"{errors2[0].get('field')}: {errors2[0].get('message')}"}
        return {"ok": False, "error": msg}

    return {"ok": False, "error": "Unknown response structure"}


def main():
    print()
    print("=" * 60)
    print("  Auric Jewels — Bulk Blog Publisher (30 Trending Posts)")
    print("  Saleor CMS — DRAFT mode")
    print("=" * 60)
    print()

    token = get_token()
    print(f"  API: {API_ENDPOINT}")
    print(f"  Token: {token[:8]}...{token[-4:]}")
    print()

    # Step 1: Find page type
    page_type_id = find_page_type(token)
    print()

    # Step 2: Discover blog files
    blog_files = discover_blog_files()
    total = len(blog_files)
    print(f"  Found {total} new blog files to publish")
    if total == 0:
        print("  No new blog files found in content/ directory.")
        sys.exit(0)
    print()

    # Step 3: Publish each
    print("=" * 60)
    print(f"  Publishing {total} articles as DRAFTS")
    print("=" * 60)
    print()

    success = 0
    failed = 0
    results = []

    for i, fname in enumerate(blog_files, 1):
        filepath = os.path.join(CONTENT_DIR, fname)
        with open(filepath, "r", encoding="utf-8") as f:
            html_content = f.read()

        title = extract_h1(html_content) or fname.replace(".html", "").replace("-", " ").title()
        slug = filename_to_slug(fname)
        meta_desc = build_meta_description(html_content)
        meta_title = f"{title} | Auric Jewels"

        article = {
            "title": title,
            "slug": slug,
            "metaTitle": meta_title[:70] if len(meta_title) > 70 else meta_title,
            "metaDescription": meta_desc,
            "content": html_content,
        }

        short_title = title[:55] + "..." if len(title) > 55 else title
        print(f"  [{i}/{total}] {short_title}")

        result = publish_page(article, page_type_id, token)

        if result.get("permission_error"):
            print(f"    PERMISSION ERROR: {result['error']}")
            print()
            print("  STOPPED: Your token lacks MANAGE_PAGES permission.")
            print("  Fix the token permissions in Saleor dashboard and retry.")
            sys.exit(2)

        if result["ok"]:
            page_id = result["data"].get("id", "?")
            note = result.get("note", "")
            print(f"    OK — Pushed {i}/{total} — ID: {page_id} — slug: {slug}")
            if note:
                print(f"    Note: {note}")
            success += 1
            results.append({"slug": slug, "id": page_id, "status": "ok"})
        else:
            print(f"    FAILED — {result['error'][:150]}")
            failed += 1
            results.append({"slug": slug, "id": None, "status": "failed", "error": result["error"][:100]})

        # Be gentle on the API
        time.sleep(0.8)

    # Summary
    print()
    print("=" * 60)
    print(f"  DONE: {success} pushed, {failed} failed out of {total}")
    print("=" * 60)
    print()

    if success > 0:
        print("  Successfully pushed pages:")
        for r in results:
            if r["status"] == "ok":
                print(f"    {r['slug']} -> ID: {r['id']}")
        print()
        print("  All pages are in DRAFT mode.")
        print("  Go to Saleor dashboard to review and publish them.")

    if failed > 0:
        print()
        print("  Failed pages:")
        for r in results:
            if r["status"] == "failed":
                print(f"    {r['slug']} -> {r.get('error', '?')}")

    # Write results to JSON for CI artifact
    results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "publish_results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump({"success": success, "failed": failed, "total": total, "results": results}, f, indent=2)
    print(f"\n  Results saved to: {results_path}")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
