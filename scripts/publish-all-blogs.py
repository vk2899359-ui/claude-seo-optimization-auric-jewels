"""
Auric Jewels — Bulk Blog Publisher (All 14 Articles)
=====================================================
Run on your Windows machine:  python scripts/publish-all-blogs.py
No pip install needed — uses only Python stdlib.
"""

import json
import urllib.request
import urllib.error
import sys
import time

API = "https://auric.thecodemesh.online/graphql/"
TOKEN = "fAPR16BVrzI4thcLtj8c4tUUG1wGU6"

ARTICLES = [
    {
        "title": "Solitaire Ring Buying Guide Gurgaon \u2014 Cuts, Clarity & Price 2026",
        "slug": "solitaire-ring-buying-guide-gurgaon",
        "metaTitle": "Solitaire Ring Buying Guide Gurgaon \u2014 Cuts, Clarity & Price 2026 | Auric Jewels",
        "metaDescription": "Complete solitaire ring buying guide for Gurgaon. Learn about diamond cuts, clarity grades, price ranges & what to ask your jeweller. IGI/GIA certified at Auric Jewels.",
    },
    {
        "title": "Luxury Bridal Gold Jewellery in Gurgaon \u2014 Complete Wedding Set Guide",
        "slug": "luxury-bridal-gold-jewellery-gurgaon",
        "metaTitle": "Luxury Bridal Gold Jewellery in Gurgaon \u2014 Complete Wedding Set Guide | Auric Jewels",
        "metaDescription": "Complete bridal gold jewellery guide for Gurgaon brides. Wedding set checklist, 22K vs 18K gold, budget planning & timeline. Visit Auric Jewels showroom.",
    },
    {
        "title": "How to Choose a Diamond Mangalsutra \u2014 Modern Designs 2026",
        "slug": "diamond-mangalsutra-modern-designs",
        "metaTitle": "How to Choose a Diamond Mangalsutra \u2014 Modern Designs 2026 | Auric Jewels",
        "metaDescription": "Guide to choosing a modern diamond mangalsutra. Single-line, dual-chain & bracelet styles. Sizing tips, certified diamonds. Shop at Auric Jewels Gurgaon.",
    },
    {
        "title": "Gold Rate Today in Gurgaon \u2014 Smart Buying Tips",
        "slug": "gold-rate-today-gurgaon-buying-tips",
        "metaTitle": "Gold Rate Today in Gurgaon \u2014 Smart Buying Tips for Jewellery Buyers | Auric Jewels",
        "metaDescription": "Understand gold rates in Gurgaon before buying jewellery. Learn what drives prices, 22K vs 18K costs, making charges & how to buy smart. Auric Jewels guide.",
    },
    {
        "title": "Custom Diamond Jewellery in Gurgaon \u2014 From Design to Delivery",
        "slug": "custom-diamond-jewellery-gurgaon",
        "metaTitle": "Custom Diamond Jewellery in Gurgaon \u2014 From Design to Delivery | Auric Jewels",
        "metaDescription": "Create bespoke diamond jewellery at Auric Jewels Gurgaon. Custom engagement rings, bridal sets & heirloom redesigns. From sketch to certified piece.",
    },
    {
        "title": "Polki vs Kundan vs Diamond \u2014 Which Bridal Set for Your Wedding?",
        "slug": "polki-vs-kundan-vs-diamond-bridal-set",
        "metaTitle": "Polki vs Kundan vs Diamond \u2014 Which Bridal Set for Your Wedding? | Auric Jewels",
        "metaDescription": "Compare polki, kundan & diamond bridal jewellery. Brilliance, durability, price & which suits each wedding ceremony. Expert guide from Auric Jewels Gurgaon.",
    },
    {
        "title": "Best Anniversary Gift Jewellery in Gurgaon \u2014 Luxury Options for Her",
        "slug": "anniversary-gift-jewellery-gurgaon",
        "metaTitle": "Best Anniversary Gift Jewellery in Gurgaon \u2014 Luxury Options for Her | Auric Jewels",
        "metaDescription": "Find the perfect anniversary jewellery gift at Auric Jewels Gurgaon. Ideas by milestone year, top-gifted pieces & personalisation options. Free gift wrapping.",
    },
    {
        "title": "Hallmark Gold Jewellery \u2014 How to Check Purity Before Buying in Gurgaon",
        "slug": "hallmark-gold-jewellery-purity-guide-gurgaon",
        "metaTitle": "Hallmark Gold Jewellery \u2014 How to Check Purity Before Buying in Gurgaon | Auric Jewels",
        "metaDescription": "Learn how to verify BIS hallmark & HUID on gold jewellery. Step-by-step guide to checking gold purity before buying in Gurgaon. Auric Jewels guide.",
    },
    {
        "title": "Karva Chauth 2026 \u2014 Premium Gold Jewellery Sets in Gurgaon",
        "slug": "karva-chauth-gold-jewellery-gurgaon-2026",
        "metaTitle": "Karva Chauth 2026 \u2014 Premium Gold Jewellery Sets in Gurgaon | Auric Jewels",
        "metaDescription": "Shop Karva Chauth jewellery gifts at Auric Jewels Gurgaon. Diamond pendants, gold bangles, mangalsutra upgrades & trending styles 2026. Free gift wrapping.",
    },
    {
        "title": "Solitaire vs Diamond Ring \u2014 What's the Difference & Which to Buy?",
        "slug": "solitaire-vs-diamond-ring-difference",
        "metaTitle": "Solitaire vs Diamond Ring \u2014 What's the Difference & Which to Buy? | Auric Jewels",
        "metaDescription": "Understand the difference between solitaire and diamond rings. Compare styles, sparkle, price & occasions. Expert guide from Auric Jewels Gurgaon.",
    },
    {
        "title": "Men's Diamond Studs & Platinum Chains \u2014 Trending in Gurgaon 2026",
        "slug": "mens-diamond-jewellery-gurgaon-2026",
        "metaTitle": "Men's Diamond Studs & Platinum Chains \u2014 Trending in Gurgaon 2026 | Auric Jewels",
        "metaDescription": "Discover men's gold & diamond jewellery trending in Gurgaon. Diamond studs, platinum chains, bracelets & rings for men. Shop at Auric Jewels.",
    },
    {
        "title": "Engagement Ring Shopping in Gurgaon \u2014 Complete Guide for Couples",
        "slug": "engagement-ring-shopping-gurgaon",
        "metaTitle": "Engagement Ring Shopping in Gurgaon \u2014 Complete Guide for Couples | Auric Jewels",
        "metaDescription": "Complete engagement ring shopping guide for Gurgaon couples. Budget tips, diamond quality, ring styles & what to ask your jeweller. Auric Jewels guide.",
    },
    {
        "title": "Diamond Earrings for Daily Wear \u2014 Best Designs Under \u20b950,000",
        "slug": "diamond-earrings-daily-wear-under-50000",
        "metaTitle": "Diamond Earrings for Daily Wear \u2014 Best Designs Under \u20b950,000 | Auric Jewels",
        "metaDescription": "Shop daily wear diamond earrings under Rs 50,000 at Auric Jewels Gurgaon. Studs, hoops & drops in 18K gold. Certified diamonds. Free shipping.",
    },
    {
        "title": "Why BIS Hallmark Matters \u2014 Gold Jewellery Buying Guide Gurgaon",
        "slug": "bis-hallmark-gold-jewellery-buying-guide",
        "metaTitle": "Why BIS Hallmark Matters \u2014 Gold Jewellery Buying Guide Gurgaon | Auric Jewels",
        "metaDescription": "Why BIS hallmark is essential when buying gold jewellery in Gurgaon. What HUID means, how to verify purity & red flags to avoid. Auric Jewels guide.",
    },
]


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
        return {"error": f"HTTP {e.code}", "body": body[:300]}
    except Exception as e:
        return {"error": str(e)}


def introspect():
    print("=" * 60)
    print("STEP 1: Introspecting GraphQL schema")
    print("=" * 60)
    r = gql("{ __schema { mutationType { fields { name args { name type { name kind ofType { name kind ofType { name } } } } } } } }")
    if "error" in r:
        print(f"  ERROR: {r}")
        return None
    mutations = (r.get("data") or {}).get("__schema", {}).get("mutationType", {})
    fields = (mutations or {}).get("fields", [])
    if not fields:
        print("  No mutations found.")
        print(f"  Raw response: {json.dumps(r, indent=2)[:500]}")
        return None
    print(f"  Found {len(fields)} mutations:")
    blog_mutation = None
    for f in fields:
        args = ", ".join(a["name"] for a in f.get("args", []))
        print(f"    {f['name']}({args})")
        name = f["name"].lower()
        if any(k in name for k in ["blog", "post", "article", "page"]):
            blog_mutation = f
    if blog_mutation:
        print(f"\n  Blog mutation found: {blog_mutation['name']}")
    return fields


def try_publish(article, mutation_name="createBlog"):
    """Try multiple mutation patterns to publish an article."""
    patterns = [
        # Pattern 1: input object
        (
            f'mutation($input: CreateBlogInput!) {{ {mutation_name}(input: $input) {{ id slug title }} }}',
            {"input": {
                "title": article["title"], "slug": article["slug"],
                "metaTitle": article["metaTitle"], "metaDescription": article["metaDescription"],
                "status": "published",
            }},
        ),
        # Pattern 2: direct args
        (
            f'mutation {{ {mutation_name}(title: {json.dumps(article["title"])}, slug: {json.dumps(article["slug"])}, metaTitle: {json.dumps(article["metaTitle"])}, metaDescription: {json.dumps(article["metaDescription"])}, status: "published") {{ id slug title }} }}',
            None,
        ),
        # Pattern 3: data input
        (
            f'mutation($data: BlogInput!) {{ {mutation_name}(data: $data) {{ id slug title }} }}',
            {"data": {
                "title": article["title"], "slug": article["slug"],
                "metaTitle": article["metaTitle"], "metaDescription": article["metaDescription"],
                "status": "published",
            }},
        ),
    ]

    for i, (query, variables) in enumerate(patterns):
        r = gql(query, variables)
        if "error" in r:
            return r
        if r.get("data") and not r.get("errors"):
            return r
        if r.get("errors"):
            msg = r["errors"][0].get("message", "")
            if i < len(patterns) - 1:
                continue
            return r
    return {"error": "All patterns failed"}


def main():
    fields = introspect()
    if fields is None:
        print("\nCannot connect to API. Exiting.")
        sys.exit(1)

    # Find the best mutation name
    mutation_name = "createBlog"
    for f in fields:
        name = f["name"].lower()
        if "createblog" in name or "addblog" in name:
            mutation_name = f["name"]
            break
        if "createpost" in name or "addpost" in name:
            mutation_name = f["name"]
        if "createarticle" in name or "addarticle" in name:
            mutation_name = f["name"]

    print(f"\n  Using mutation: {mutation_name}")

    print()
    print("=" * 60)
    print(f"STEP 2: Publishing {len(ARTICLES)} articles")
    print("=" * 60)

    success = 0
    failed = 0

    for i, article in enumerate(ARTICLES, 1):
        print(f"\n  [{i}/{len(ARTICLES)}] {article['title'][:60]}...")
        r = try_publish(article, mutation_name)

        if "error" in r:
            print(f"    FAILED: {r['error']}")
            if "body" in r:
                print(f"    Body: {r['body'][:200]}")
            failed += 1
        elif r.get("errors"):
            print(f"    FAILED: {r['errors'][0].get('message', 'Unknown error')[:150]}")
            failed += 1
        else:
            data = r.get("data", {})
            print(f"    SUCCESS -> https://www.auricjewels.com/blog/{article['slug']}")
            success += 1

        time.sleep(0.5)  # Be gentle on the API

    print()
    print("=" * 60)
    print(f"DONE: {success} published, {failed} failed out of {len(ARTICLES)}")
    print("=" * 60)

    if failed > 0:
        print("\nFor failed articles, try publishing manually via your CMS admin panel.")
        print("The HTML content for each article is in the content/ directory.")


if __name__ == "__main__":
    main()
