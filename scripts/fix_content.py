"""
Auric Jewels — Fix Blog Content Format
========================================
Converts HTML blog content to EditorJS JSON format
and updates all 30 pages in Saleor via pageUpdate.

Run: python3 scripts/fix_content.py
"""
import json, os, re, sys, time, urllib.request

API = "https://auric.thecodemesh.online/graphql/"
EMAIL = "r@yopmail.com"
PASSWORD = "r"
CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content")
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/json",
    "Origin": "https://auric.thecodemesh.online",
    "Referer": "https://auric.thecodemesh.online/dashboard/",
}

EXCLUDE = ["blog-01-","blog-gold-jewellery-investment-2026","blog-lab-grown-vs-natural-diamonds",
           "blog-jewellery-trends-india-2026","blog-layered-necklace-styling",
           "blog-lightweight-gold-jewellery","blog-platinum-jewellery-men"]


def gql(query, variables=None, token=None):
    payload = json.dumps({"query": query, **({"variables": variables} if variables else {})}).encode()
    h = dict(HEADERS)
    if token:
        h["Authorization"] = "Bearer " + token
    req = urllib.request.Request(API, data=payload, headers=h, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def html_to_editorjs(html):
    """Convert blog HTML to Saleor EditorJS JSON format."""
    blocks = []
    # Remove <article> wrapper
    html = re.sub(r'</?article>', '', html).strip()

    # Split into meaningful HTML elements
    parts = re.split(r'(<h[1-6][^>]*>.*?</h[1-6]>|<p>.*?</p>|<table>.*?</table>|<ul>.*?</ul>|<ol>.*?</ol>)', html, flags=re.DOTALL)

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Headers
        hm = re.match(r'<h([1-6])[^>]*>(.*?)</h[1-6]>', part, re.DOTALL)
        if hm:
            level = int(hm.group(1))
            text = hm.group(2).strip()
            blocks.append({
                "id": _block_id(),
                "type": "header",
                "data": {"text": text, "level": level}
            })
            continue

        # Paragraphs
        pm = re.match(r'<p>(.*?)</p>', part, re.DOTALL)
        if pm:
            text = pm.group(1).strip()
            if text:
                blocks.append({
                    "id": _block_id(),
                    "type": "paragraph",
                    "data": {"text": text}
                })
            continue

        # Tables
        if part.startswith('<table'):
            rows = []
            # Extract header row
            thead = re.search(r'<thead>(.*?)</thead>', part, re.DOTALL)
            if thead:
                ths = re.findall(r'<th>(.*?)</th>', thead.group(1), re.DOTALL)
                if ths:
                    rows.append(ths)
            # Extract body rows
            tbody = re.search(r'<tbody>(.*?)</tbody>', part, re.DOTALL)
            if tbody:
                for tr in re.findall(r'<tr>(.*?)</tr>', tbody.group(1), re.DOTALL):
                    tds = re.findall(r'<td>(.*?)</td>', tr, re.DOTALL)
                    if tds:
                        rows.append(tds)
            if rows:
                blocks.append({
                    "id": _block_id(),
                    "type": "table",
                    "data": {"withHeadings": bool(thead), "content": rows}
                })
            continue

        # Unordered lists
        if part.startswith('<ul'):
            items = re.findall(r'<li>(.*?)</li>', part, re.DOTALL)
            if items:
                blocks.append({
                    "id": _block_id(),
                    "type": "list",
                    "data": {"style": "unordered", "items": [i.strip() for i in items]}
                })
            continue

        # Ordered lists
        if part.startswith('<ol'):
            items = re.findall(r'<li>(.*?)</li>', part, re.DOTALL)
            if items:
                blocks.append({
                    "id": _block_id(),
                    "type": "list",
                    "data": {"style": "ordered", "items": [i.strip() for i in items]}
                })
            continue

    if not blocks:
        # Fallback: put entire HTML as one paragraph
        clean = re.sub(r'<[^>]+>', ' ', html).strip()
        clean = re.sub(r'\s+', ' ', clean)
        blocks.append({
            "id": _block_id(),
            "type": "paragraph",
            "data": {"text": html}
        })

    return json.dumps({"time": int(time.time() * 1000), "blocks": blocks, "version": "2.24.3"})


_counter = [0]
def _block_id():
    _counter[0] += 1
    return f"blk{_counter[0]:04d}"


def get_blog_files():
    files = []
    for f in sorted(os.listdir(CONTENT_DIR)):
        if not f.startswith("blog-") or not f.endswith(".html"):
            continue
        if any(f.startswith(ex) for ex in EXCLUDE):
            continue
        files.append(f)
    return files


def filename_to_slug(fname):
    slug = fname.replace(".html", "")
    if slug.startswith("blog-"):
        slug = slug[5:]
    return slug


def main():
    print()
    print("=" * 55)
    print("  Auric Jewels — Fix Blog Content (EditorJS format)")
    print("=" * 55)
    print()

    # Get token
    print("  Getting token...")
    r = gql('mutation{tokenCreate(email:"'+EMAIL+'",password:"'+PASSWORD+'"){token errors{field message}}}')
    token = r["data"]["tokenCreate"]["token"]
    print("  Token OK")

    # Get all pages from Saleor
    print("  Fetching pages from Saleor...")
    r = gql("{pages(first:60){edges{node{id slug title}}}}", token=token)
    saleor_pages = {e["node"]["slug"]: e["node"] for e in r["data"]["pages"]["edges"]}
    print(f"  Found {len(saleor_pages)} pages in Saleor")

    # Get blog files
    files = get_blog_files()
    print(f"  Found {len(files)} blog HTML files")
    print()

    # Match and update
    ok = 0
    fail = 0
    skip = 0
    total = len(files)

    for i, fname in enumerate(files, 1):
        slug = filename_to_slug(fname)
        short_slug = slug[:50] + "..." if len(slug) > 50 else slug

        if slug not in saleor_pages:
            print(f"  [{i}/{total}] {short_slug} -> SKIP (not in Saleor)")
            skip += 1
            continue

        page_id = saleor_pages[slug]["id"]

        # Read HTML and convert to EditorJS
        filepath = os.path.join(CONTENT_DIR, fname)
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()

        editorjs_content = html_to_editorjs(html)

        # Update page content
        mutation = """mutation PageUpdate($id: ID!, $input: PageInput!) {
            pageUpdate(id: $id, input: $input) {
                page { id slug }
                errors { field message }
            }
        }"""
        variables = {"id": page_id, "input": {"content": editorjs_content}}

        try:
            r2 = gql(mutation, variables, token=token)
            page = r2.get("data", {}).get("pageUpdate", {}).get("page")
            errs = r2.get("data", {}).get("pageUpdate", {}).get("errors", [])
            if page and not errs:
                print(f"  [{i}/{total}] {short_slug} -> UPDATED (ID: {page_id})")
                ok += 1
            else:
                msg = errs[0]["message"] if errs else "Unknown"
                print(f"  [{i}/{total}] {short_slug} -> FAILED: {msg}")
                fail += 1
        except Exception as e:
            print(f"  [{i}/{total}] {short_slug} -> ERROR: {e}")
            fail += 1

        time.sleep(0.4)

    print()
    print("=" * 55)
    print(f"  DONE: {ok} updated, {fail} failed, {skip} skipped")
    print("=" * 55)
    print()
    if ok > 0:
        print("  Content is now in EditorJS format.")
        print("  Refresh auricjewels.com/blog to see the content!")


if __name__ == "__main__":
    main()
