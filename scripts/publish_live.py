"""
Auric Jewels — Publish All DRAFT Pages to LIVE
================================================
Run: python3 scripts/publish_live.py
"""
import json, sys, time, urllib.request

API = "https://auric.thecodemesh.online/graphql/"
EMAIL = "r@yopmail.com"
PASSWORD = "r"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/json",
    "Origin": "https://auric.thecodemesh.online",
    "Referer": "https://auric.thecodemesh.online/dashboard/",
}

def gql(query, variables=None, token=None):
    payload = json.dumps({"query": query, **({"variables": variables} if variables else {})}).encode()
    h = dict(HEADERS)
    if token:
        h["Authorization"] = "Bearer " + token
    req = urllib.request.Request(API, data=payload, headers=h, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

print()
print("=" * 50)
print("  Making all DRAFT pages LIVE")
print("=" * 50)
print()

# Get token
print("  Getting token...")
r = gql('mutation{tokenCreate(email:"' + EMAIL + '",password:"' + PASSWORD + '"){token errors{field message}}}')
token = r["data"]["tokenCreate"]["token"]
print("  Token OK")
print()

# Get all pages
r = gql("{pages(first:50){edges{node{id slug isPublished}}}}", token=token)
all_pages = r["data"]["pages"]["edges"]
drafts = [e["node"] for e in all_pages if not e["node"]["isPublished"]]

print(f"  Total pages: {len(all_pages)}")
print(f"  Drafts to publish: {len(drafts)}")
print()

if not drafts:
    print("  No drafts found. Everything is already LIVE!")
    sys.exit(0)

# Publish each draft
ok = 0
fail = 0
for i, page in enumerate(drafts, 1):
    slug = page["slug"]
    pid = page["id"]
    short = slug[:50] + "..." if len(slug) > 50 else slug

    mutation = """mutation PageUpdate($id: ID!, $input: PageInput!) {
        pageUpdate(id: $id, input: $input) {
            page { id slug }
            errors { field message }
        }
    }"""
    variables = {"id": pid, "input": {"isPublished": True}}

    try:
        r2 = gql(mutation, variables, token=token)
        p = r2.get("data", {}).get("pageUpdate", {}).get("page")
        errs = r2.get("data", {}).get("pageUpdate", {}).get("errors", [])
        if p and not errs:
            print(f"  [{i}/{len(drafts)}] {short} -> LIVE")
            ok += 1
        else:
            msg = errs[0]["message"] if errs else "Unknown"
            print(f"  [{i}/{len(drafts)}] {short} -> FAILED: {msg}")
            fail += 1
    except Exception as e:
        print(f"  [{i}/{len(drafts)}] {short} -> ERROR: {e}")
        fail += 1

    time.sleep(0.3)

print()
print("=" * 50)
print(f"  DONE: {ok} LIVE, {fail} failed out of {len(drafts)}")
print("=" * 50)
