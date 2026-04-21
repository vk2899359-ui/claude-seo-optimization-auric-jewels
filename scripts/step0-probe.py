"""Step 0 — Probe Saleor: list first 20 pages and find homepage."""
import json, urllib.request, urllib.error

API   = "https://auric.thecodemesh.online/graphql/"
TOKEN = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"

def gql(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    req = urllib.request.Request(
        API,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        return {"httpError": e.code, "body": body[:600]}
    except Exception as e:
        return {"error": str(e)}

# 1. List first 20 pages
print("=== First 20 Pages ===")
r = gql("""
{
  pages(first: 20) {
    edges {
      node {
        id
        slug
        title
        seoTitle
        seoDescription
        pageType { id name }
      }
    }
  }
}
""")
pages = (r.get("data") or {}).get("pages", {}).get("edges", [])
if pages:
    for e in pages:
        n = e["node"]
        print(f"  id={n['id']}  slug={n['slug']!r}")
        print(f"    title={n['title']!r}")
        print(f"    seoTitle={n.get('seoTitle')!r}")
        print(f"    seoDesc={n.get('seoDescription','')[:80]!r}")
        print(f"    pageType={n.get('pageType')}")
        print()
else:
    print("  No pages found or error:", json.dumps(r, indent=2)[:400])

# 2. Check if there's a "shop" object with SEO (for storefront homepage)
print("=== Shop / Storefront SEO ===")
r2 = gql("{ shop { name description } }")
print(json.dumps(r2, indent=2)[:400])
