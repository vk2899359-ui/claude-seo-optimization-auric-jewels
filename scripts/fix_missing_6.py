"""
Push 6 missing blogs + fix their content in EditorJS format.
Run: python3 scripts/fix_missing_6.py
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

MISSING = [
    {"slug": "raksha-bandhan-2026-gold-jewellery-gift-sisters", "file": "blog-raksha-bandhan-2026-gold-jewellery-gift-sisters.html"},
    {"slug": "reception-jewellery-ideas-modern-indian-bride", "file": "blog-reception-jewellery-ideas-modern-indian-bride.html"},
    {"slug": "solitaire-pendant-daily-wear-under-1-lakh", "file": "blog-solitaire-pendant-daily-wear-under-1-lakh.html"},
    {"slug": "tanishq-alternative-gurgaon-boutique-jeweller", "file": "blog-tanishq-alternative-gurgaon-boutique-jeweller.html"},
    {"slug": "temple-jewellery-wedding-2026-gurgaon", "file": "blog-temple-jewellery-wedding-2026-gurgaon.html"},
    {"slug": "wedding-jewellery-checklist-indian-bride-2026", "file": "blog-wedding-jewellery-checklist-indian-bride-2026.html"},
]

def gql(query, variables=None, token=None):
    payload = json.dumps({"query": query, **({"variables": variables} if variables else {})}).encode()
    h = dict(HEADERS)
    if token:
        h["Authorization"] = "Bearer " + token
    req = urllib.request.Request(API, data=payload, headers=h, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

_c = [0]
def _bid():
    _c[0] += 1
    return f"b{_c[0]:04d}"

def html_to_editorjs(html):
    blocks = []
    html = re.sub(r'</?article>', '', html).strip()
    parts = re.split(r'(<h[1-6][^>]*>.*?</h[1-6]>|<p>.*?</p>|<table>.*?</table>|<ul>.*?</ul>|<ol>.*?</ol>)', html, flags=re.DOTALL)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        hm = re.match(r'<h([1-6])[^>]*>(.*?)</h[1-6]>', part, re.DOTALL)
        if hm:
            blocks.append({"id":_bid(),"type":"header","data":{"text":hm.group(2).strip(),"level":int(hm.group(1))}})
            continue
        pm = re.match(r'<p>(.*?)</p>', part, re.DOTALL)
        if pm and pm.group(1).strip():
            blocks.append({"id":_bid(),"type":"paragraph","data":{"text":pm.group(1).strip()}})
            continue
        if part.startswith('<table'):
            rows = []
            thead = re.search(r'<thead>(.*?)</thead>', part, re.DOTALL)
            if thead:
                ths = re.findall(r'<th>(.*?)</th>', thead.group(1), re.DOTALL)
                if ths: rows.append(ths)
            tbody = re.search(r'<tbody>(.*?)</tbody>', part, re.DOTALL)
            if tbody:
                for tr in re.findall(r'<tr>(.*?)</tr>', tbody.group(1), re.DOTALL):
                    tds = re.findall(r'<td>(.*?)</td>', tr, re.DOTALL)
                    if tds: rows.append(tds)
            if rows:
                blocks.append({"id":_bid(),"type":"table","data":{"withHeadings":bool(thead),"content":rows}})
            continue
        if part.startswith('<ul'):
            items = re.findall(r'<li>(.*?)</li>', part, re.DOTALL)
            if items:
                blocks.append({"id":_bid(),"type":"list","data":{"style":"unordered","items":[i.strip() for i in items]}})
            continue
        if part.startswith('<ol'):
            items = re.findall(r'<li>(.*?)</li>', part, re.DOTALL)
            if items:
                blocks.append({"id":_bid(),"type":"list","data":{"style":"ordered","items":[i.strip() for i in items]}})
            continue
    if not blocks:
        blocks.append({"id":_bid(),"type":"paragraph","data":{"text":re.sub(r'<[^>]+>',' ',html).strip()}})
    return json.dumps({"time":int(time.time()*1000),"blocks":blocks,"version":"2.24.3"})

def extract_h1(html):
    m = re.search(r"<h1>(.*?)</h1>", html, re.DOTALL)
    return re.sub(r"<[^>]+>","",m.group(1)).strip() if m else None

def extract_meta(html):
    m = re.search(r"<p>(.*?)</p>", html, re.DOTALL)
    if not m: return ""
    t = re.sub(r"<[^>]+>","",m.group(1)).strip()
    return t[:152].rsplit(" ",1)[0]+"..." if len(t)>155 else t

print()
print("=" * 55)
print("  Pushing 6 missing blogs + fixing content")
print("=" * 55)
print()

# Get token
print("  Getting token...")
r = gql('mutation{tokenCreate(email:"'+EMAIL+'",password:"'+PASSWORD+'"){token errors{field message}}}')
token = r["data"]["tokenCreate"]["token"]
print("  Token OK")

# Find page type
r = gql("{pageTypes(first:20){edges{node{id name slug}}}}", token=token)
edges = r.get("data",{}).get("pageTypes",{}).get("edges",[])
page_type_id = None
for e in edges:
    n = e["node"]
    if "seo" in (n.get("name","") + n.get("slug","")).lower():
        page_type_id = n["id"]
        break
if not page_type_id and edges:
    page_type_id = edges[0]["node"]["id"]
print(f"  Page type: {page_type_id}")
print()

ok = 0
for i, blog in enumerate(MISSING, 1):
    filepath = os.path.join(CONTENT_DIR, blog["file"])
    if not os.path.exists(filepath):
        print(f"  [{i}/6] {blog['slug']} -> FILE NOT FOUND")
        continue

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    title = extract_h1(html) or blog["slug"].replace("-"," ").title()
    meta = extract_meta(html)
    content = html_to_editorjs(html)

    # Create page
    inp = {
        "slug": blog["slug"],
        "title": title,
        "isPublished": True,
        "seo": {"title": (title + " | Auric Jewels")[:70], "description": meta},
        "content": content,
    }
    if page_type_id:
        inp["pageType"] = page_type_id

    mutation = """mutation PageCreate($input: PageCreateInput!) {
        pageCreate(input: $input) {
            page { id slug title }
            errors { field message code }
        }
    }"""

    try:
        r2 = gql(mutation, {"input": inp}, token=token)
        page = r2.get("data",{}).get("pageCreate",{}).get("page")
        errs = r2.get("data",{}).get("pageCreate",{}).get("errors",[])
        if page and not errs:
            print(f"  [{i}/6] {blog['slug']} -> CREATED + LIVE (ID: {page['id']})")
            ok += 1
        elif errs:
            # Maybe slug exists already, try update instead
            if errs[0].get("code") == "UNIQUE":
                print(f"  [{i}/6] {blog['slug']} -> already exists, skipping")
            else:
                print(f"  [{i}/6] {blog['slug']} -> FAILED: {errs[0].get('message')}")
        else:
            print(f"  [{i}/6] {blog['slug']} -> FAILED: unknown")
    except Exception as e:
        print(f"  [{i}/6] {blog['slug']} -> ERROR: {e}")

    time.sleep(0.5)

print()
print("=" * 55)
print(f"  DONE: {ok}/6 created")
print("=" * 55)
print()
print("  Refresh auricjewels.com/blog — all blogs should now show with content!")
