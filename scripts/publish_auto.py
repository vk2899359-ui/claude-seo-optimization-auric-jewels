"""
Auric Jewels — One-Shot Blog Publisher
=======================================
Gets JWT token automatically + publishes all 30 blogs as DRAFT.
Just run: python3 scripts/publish_auto.py
"""
import json, os, re, sys, time, urllib.request, urllib.error

API = "https://auric.thecodemesh.online/graphql/"
EMAIL = "r@yopmail.com"
PASSWORD = "r"
CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "content")

EXCLUDE = ["blog-01-","blog-gold-jewellery-investment-2026","blog-lab-grown-vs-natural-diamonds",
           "blog-jewellery-trends-india-2026","blog-layered-necklace-styling",
           "blog-lightweight-gold-jewellery","blog-platinum-jewellery-men"]

def gql(query, variables=None, token=None):
    payload = json.dumps({"query": query, **({"variables": variables} if variables else {})}).encode()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(API, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        return {"errors": [{"message": f"HTTP {e.code}: {body[:300]}"}]}
    except Exception as e:
        return {"errors": [{"message": str(e)}]}

def get_token():
    print("  Getting JWT token...")
    r = gql(f'mutation{{tokenCreate(email:"{EMAIL}",password:"{PASSWORD}"){{token errors{{field message}}}}}}')
    token = (r.get("data") or {}).get("tokenCreate", {}).get("token")
    errors = (r.get("data") or {}).get("tokenCreate", {}).get("errors", [])
    if token:
        print(f"  Token: {token[:20]}...")
        return token
    if errors:
        print(f"  ERROR: {errors[0].get('message')}")
    else:
        print(f"  ERROR: {r}")
    sys.exit(1)

def find_page_type(token):
    print("  Finding page types...")
    r = gql("{pageTypes(first:20){edges{node{id name slug}}}}", token=token)
    edges = (r.get("data") or {}).get("pageTypes", {}).get("edges", [])
    if not edges:
        print("  No page types found, continuing without...")
        return None
    best = None
    for e in edges:
        n = e["node"]
        combined = (n.get("name","") + n.get("slug","")).lower()
        if any(k in combined for k in ["seo","blog","article","post","content"]):
            best = n
    if not best:
        best = edges[0]["node"]
    print(f'  Using: "{best["name"]}" ({best["id"]})')
    return best["id"]

def get_blog_files():
    files = []
    for f in sorted(os.listdir(CONTENT_DIR)):
        if not f.startswith("blog-") or not f.endswith(".html"):
            continue
        if any(f.startswith(ex) for ex in EXCLUDE):
            continue
        files.append(f)
    return files

def extract_h1(html):
    m = re.search(r"<h1>(.*?)</h1>", html, re.DOTALL)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else None

def extract_meta(html):
    m = re.search(r"<p>(.*?)</p>", html, re.DOTALL)
    if not m: return ""
    t = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return t[:152].rsplit(" ",1)[0]+"..." if len(t)>155 else t

def publish(article, page_type_id, token):
    inp = {"slug":article["slug"],"title":article["title"],"isPublished":False,
           "seo":{"title":(article["title"]+" | Auric Jewels")[:70],"description":article["meta"]}}
    if article.get("content"):
        inp["content"] = json.dumps({"blocks":[{"type":"rawHtml","data":{"html":article["content"]}}]})
    if page_type_id:
        inp["pageType"] = page_type_id

    mut = "mutation P($input:PageCreateInput!){pageCreate(input:$input){page{id slug title}errors{field message code}}}"
    r = gql(mut, {"input": inp}, token=token)

    if r.get("errors"):
        return None, r["errors"][0].get("message","?")

    data = (r.get("data") or {}).get("pageCreate", {})
    page = data.get("page")
    errs = data.get("errors", [])

    if page and not errs:
        return page, None

    if errs and errs[0].get("field") == "content":
        del inp["content"]
        r2 = gql(mut, {"input": inp}, token=token)
        d2 = (r2.get("data") or {}).get("pageCreate", {})
        if d2.get("page") and not d2.get("errors", []):
            return d2["page"], None
        if d2.get("errors"):
            return None, d2["errors"][0].get("message","?")

    if errs:
        return None, f'{errs[0].get("field")}: {errs[0].get("message")} ({errs[0].get("code")})'
    return None, "Unknown error"

def main():
    print()
    print("=" * 55)
    print("  Auric Jewels — Auto Blog Publisher (30 Posts)")
    print("=" * 55)
    print()

    token = get_token()
    page_type_id = find_page_type(token)
    files = get_blog_files()
    total = len(files)
    print(f"  Found {total} blog files")
    print()
    print("=" * 55)

    ok, fail = 0, 0
    results = []

    for i, fname in enumerate(files, 1):
        path = os.path.join(CONTENT_DIR, fname)
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        title = extract_h1(html) or fname.replace(".html","").replace("-"," ").title()
        slug = fname.replace(".html","")
        if slug.startswith("blog-"): slug = slug[5:]
        meta = extract_meta(html)

        article = {"title":title,"slug":slug,"meta":meta,"content":html}
        short = title[:50]+"..." if len(title)>50 else title
        print(f"  [{i}/{total}] {short}")

        page, err = publish(article, page_type_id, token)
        if page:
            pid = page.get("id","?")
            print(f"    OK  Pushed {i}/{total}  ID: {pid}")
            ok += 1
            results.append({"slug":slug,"id":pid})
        else:
            print(f"    FAIL  {err[:120]}")
            fail += 1

        time.sleep(0.6)

    print()
    print("=" * 55)
    print(f"  DONE: {ok} pushed, {fail} failed out of {total}")
    print("=" * 55)

    if results:
        print()
        print("  Saleor Page IDs:")
        for r in results:
            print(f"    {r['slug']}  ->  {r['id']}")
        print()
        print("  All pages are DRAFT. Publish from Saleor dashboard.")

if __name__ == "__main__":
    main()
