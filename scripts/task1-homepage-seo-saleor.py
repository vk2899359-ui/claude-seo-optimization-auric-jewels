#!/usr/bin/env python3
"""
Auric Jewels — Task 1: Update Homepage SEO in Saleor CMS
=========================================================
Run from your Windows machine: python scripts/task1-homepage-seo-saleor.py

Finds the page with slug 'home' (or lists all pages so you can pick),
then updates its SEO title + description via pageUpdate mutation.
"""
import json, urllib.request, urllib.error, sys

API   = "https://auric.thecodemesh.online/graphql/"
TOKEN = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"

SEO_TITLE = "Auric Jewels Gurgaon | BIS Hallmarked Gold & IGI Certified Diamond Jewellery"
SEO_DESC  = (
    "Shop BIS hallmarked gold and IGI/GIA certified diamond jewellery at Auric Jewels, "
    "Sector 45 Gurgaon. Bridal, daily wear & gifting collections. Visit showroom or WhatsApp "
    "for expert guidance."
)


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
        return {"httpError": e.code, "body": body[:400]}
    except Exception as e:
        return {"error": str(e)}


def find_homepage():
    """Query pages list to find the homepage."""
    r = gql("""
    {
      pages(first: 30) {
        edges {
          node { id slug title seoTitle seoDescription }
        }
      }
    }
    """)

    if "httpError" in r or "error" in r:
        print(f"API error: {r}")
        return None

    pages = (r.get("data") or {}).get("pages", {}).get("edges", [])
    print(f"Found {len(pages)} pages:")
    homepage_id = None
    for e in pages:
        n = e["node"]
        marker = " <-- HOMEPAGE CANDIDATE" if n["slug"] in ("home", "homepage", "") else ""
        print(f"  id={n['id']}  slug={n['slug']!r}  title={n['title']!r}{marker}")
        if n["slug"] in ("home", "homepage"):
            homepage_id = n["id"]

    return homepage_id


def update_seo(page_id):
    mutation = """
    mutation PageUpdate($id: ID!, $input: PageInput!) {
        pageUpdate(id: $id, input: $input) {
            page { id slug seoTitle seoDescription }
            errors { field message code }
        }
    }"""
    variables = {
        "id": page_id,
        "input": {
            "seo": {
                "title":       SEO_TITLE,
                "description": SEO_DESC,
            }
        },
    }
    r = gql(mutation, variables)
    if "httpError" in r or "error" in r:
        print(f"  FAILED: {r}")
        return False
    pu = (r.get("data") or {}).get("pageUpdate", {})
    if pu.get("errors"):
        print(f"  SALEOR ERROR: {pu['errors']}")
        return False
    page = pu.get("page")
    print(f"  Updated page id={page['id']}")
    print(f"  seoTitle: {page['seoTitle']}")
    print(f"  seoDescription: {page['seoDescription'][:80]}...")
    return True


if __name__ == "__main__":
    print("=== Task 1: Update Homepage SEO in Saleor ===\n")

    page_id = find_homepage()

    if not page_id:
        print("\nNo page with slug 'home' or 'homepage' found.")
        print("Please copy a page ID from the list above and run:")
        print("  python -c \"")
        print("  import sys; sys.argv = ['', '<PAGE_ID>']")
        print("  exec(open('scripts/task1-homepage-seo-saleor.py').read())")
        print("  \"")
        print("\nOr update PAGE_ID manually in this script and re-run.")
        # If a page ID is passed as argument, use it
        if len(sys.argv) > 1:
            page_id = sys.argv[1]
            print(f"\nUsing provided page_id: {page_id}")
        else:
            sys.exit(0)

    print(f"\nUpdating SEO for page id={page_id} ...")
    ok = update_seo(page_id)
    if ok:
        print("\nDone. Homepage SEO updated in Saleor CMS.")
    else:
        print("\nFailed. Check errors above.")
        sys.exit(1)
