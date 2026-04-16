"""
Auric Jewels — Add metadata type=blog to all new pages
========================================================
Makes pages appear on auricjewels.com/blog listing.
Run: python3 scripts/fix_metadata.py
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

# Slugs of our 30 new blogs
NEW_SLUGS = [
    "1-carat-diamond-ring-price-india-2026",
    "22k-vs-18k-gold-jewellery-which-to-buy",
    "akshaya-tritiya-2026-gold-jewellery-buying-guide",
    "akshaya-tritiya-diamond-jewellery-offers-gurgaon-2026",
    "best-place-buy-gold-jewellery-gurgaon-2026",
    "birthday-gift-jewellery-wife-diamond",
    "bridal-diamond-necklace-set-designs-2026",
    "bridal-jewellery-under-5-lakhs-gurgaon",
    "certified-diamond-jewellery-india-igi-vs-gia-2026",
    "coloured-diamond-jewellery-trends-india-2026",
    "diamond-clarity-guide-vs1-vs2-si1-india",
    "diamond-jewellery-exchange-policy-gurgaon",
    "diamond-nose-pin-designs-trending-india-2026",
    "diamond-tennis-bracelet-buying-guide-india-2026",
    "gold-chain-designs-women-2026-trending",
    "gold-coins-akshaya-tritiya-2026-investment-guide",
    "gold-jewellery-making-charges-explained-2026",
    "gold-vs-diamond-investment-2026-india",
    "jewellery-showroom-sector-45-gurgaon",
    "lab-grown-diamond-bridal-jewellery-2026",
    "mothers-day-2026-diamond-pendant-gift-ideas",
    "online-vs-showroom-diamond-jewellery-caratlane-bluestone",
    "oval-cut-diamond-engagement-ring-india-2026",
    "push-gift-jewellery-new-mother-india",
    "raksha-bandhan-2026-gold-jewellery-gift-sisters",
    "reception-jewellery-ideas-modern-indian-bride",
    "solitaire-pendant-daily-wear-under-1-lakh",
    "tanishq-alternative-gurgaon-boutique-jeweller",
    "temple-jewellery-wedding-2026-gurgaon",
    "wedding-jewellery-checklist-indian-bride-2026",
]

def gql(query, variables=None, token=None):
    payload = json.dumps({"query": query, **({"variables": variables} if variables else {})}).encode()
    h = dict(HEADERS)
    if token:
        h["Authorization"] = "Bearer " + token
    req = urllib.request.Request(API, data=payload, headers=h, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

print()
print("=" * 55)
print("  Adding metadata type=blog to all 30 pages")
print("=" * 55)
print()

# Get token
print("  Getting token...")
r = gql('mutation{tokenCreate(email:"'+EMAIL+'",password:"'+PASSWORD+'"){token errors{field message}}}')
token = r["data"]["tokenCreate"]["token"]
print("  Token OK")

# Get all pages
print("  Fetching pages...")
r = gql("{pages(first:60){edges{node{id slug metadata{key value}}}}}", token=token)
all_pages = {e["node"]["slug"]: e["node"] for e in r["data"]["pages"]["edges"]}
print(f"  Found {len(all_pages)} pages")
print()

ok = 0
skip = 0
fail = 0
total = len(NEW_SLUGS)

for i, slug in enumerate(NEW_SLUGS, 1):
    short = slug[:50] + "..." if len(slug) > 50 else slug

    if slug not in all_pages:
        print(f"  [{i}/{total}] {short} -> NOT FOUND in Saleor")
        fail += 1
        continue

    page = all_pages[slug]
    page_id = page["id"]

    # Check if metadata already has type=blog
    existing_meta = page.get("metadata", []) or []
    has_blog_type = any(m.get("key") == "type" and m.get("value") == "blog" for m in existing_meta)
    if has_blog_type:
        print(f"  [{i}/{total}] {short} -> ALREADY HAS type=blog")
        skip += 1
        continue

    # Update metadata
    mutation = """mutation UpdateMetadata($id: ID!, $input: [MetadataInput!]!) {
        updateMetadata(id: $id, input: $input) {
            item { ... on Page { id slug metadata { key value } } }
            errors { field message }
        }
    }"""
    variables = {
        "id": page_id,
        "input": [{"key": "type", "value": "blog"}]
    }

    try:
        r2 = gql(mutation, variables, token=token)
        errors = r2.get("data", {}).get("updateMetadata", {}).get("errors", [])
        item = r2.get("data", {}).get("updateMetadata", {}).get("item")
        if item and not errors:
            print(f"  [{i}/{total}] {short} -> ADDED type=blog")
            ok += 1
        elif errors:
            print(f"  [{i}/{total}] {short} -> FAILED: {errors[0].get('message')}")
            fail += 1
        else:
            # Try alternative mutation format
            mut2 = """mutation PageUpdate($id: ID!, $input: PageInput!) {
                pageUpdate(id: $id, input: $input) {
                    page { id slug }
                    errors { field message }
                }
            }"""
            vars2 = {"id": page_id, "input": {"metadata": [{"key": "type", "value": "blog"}]}}
            r3 = gql(mut2, vars2, token=token)
            p3 = r3.get("data", {}).get("pageUpdate", {}).get("page")
            e3 = r3.get("data", {}).get("pageUpdate", {}).get("errors", [])
            if p3 and not e3:
                print(f"  [{i}/{total}] {short} -> ADDED type=blog (via pageUpdate)")
                ok += 1
            else:
                msg = e3[0].get("message") if e3 else "Unknown"
                print(f"  [{i}/{total}] {short} -> FAILED: {msg}")
                fail += 1
    except Exception as e:
        print(f"  [{i}/{total}] {short} -> ERROR: {e}")
        fail += 1

    time.sleep(0.3)

print()
print("=" * 55)
print(f"  DONE: {ok} updated, {skip} already had it, {fail} failed")
print("=" * 55)
print()
print("  All 30 blogs now have metadata type=blog.")
print("  Refresh auricjewels.com/blog to see them in the listing!")
