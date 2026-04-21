#!/usr/bin/env python3
"""
Auric Jewels — Create SEO Collection Page #1
Slug: bestsellers-jewellery-gurgaon
Run: python scripts/page-01-bestsellers.py
"""
import json, urllib.request, urllib.error, sys

API            = "https://auric.thecodemesh.online/graphql/"
TOKEN          = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID   = "UGFnZVR5cGU6Ng=="

PAGE = {
    "slug": "bestsellers-jewellery-gurgaon",
    "title": "Bestselling Jewellery in Gurgaon | Auric Jewels",
    "seoTitle": "Bestselling Jewellery Gurgaon | Gold & Diamond | Auric Jewels",
    "seoDescription": (
        "Explore bestselling gold & diamond jewellery at Auric Jewels, Sector 45 Gurgaon. "
        "BIS hallmarked, IGI/GIA certified. Solitaire rings, diamond earrings & bridal sets — "
        "our most-loved pieces for every occasion."
    ),
    "content": """
<h1>Bestselling Jewellery in Gurgaon | Auric Jewels</h1>

<p>When discerning jewellery buyers in Gurgaon ask what the rest of the city is wearing, the answer is consistent: the pieces that have earned a permanent place in our bestsellers showcase at <strong>Auric Jewels, Sector 45</strong>. These are not fleeting trends — they are timeless designs that combine flawless craftsmanship, certified quality, and enduring elegance. Every piece featured here carries either a BIS hallmark on gold or IGI/GIA certification on diamonds, so your investment is protected from the moment you leave our showroom.</p>

<h2>Our Most-Loved Gold Jewellery</h2>

<p>Gold jewellery in 22-karat (for traditional pieces) and 18-karat (for diamond-set designs) forms the backbone of our bestseller list. Among the most sought-after are our <strong>lightweight chain-link bracelets</strong> in 22K yellow gold — wearable every day yet sophisticated enough for festive occasions. Our <strong>temple-work bangles</strong> continue to sell out season after season, loved for their intricate hand-engraved motifs and solid feel. Customers planning weddings regularly begin their trousseau journey here, and many return for anniversary and gifting purchases year after year.</p>

<p>Our <strong>BIS HUID-stamped gold chains</strong> — available in box, rope, and Figaro styles — are consistently among our top sellers for gifting. Lightweight enough for daily wear yet substantial enough to layer for special occasions, these chains represent excellent value at today's gold rates. Read our guide on <a href="/blog/gold-rate-today-gurgaon-buying-tips">smart buying tips when gold rates fluctuate</a> before making your purchase.</p>

<h2>Diamond Jewellery That Customers Return For</h2>

<p>Our <strong>diamond solitaire earrings in 18K white gold</strong> hold the top spot in diamond jewellery sales — and it is easy to see why. A pair of round-brilliant solitaire studs in certified VS-clarity diamonds is the one piece every woman eventually adds to her collection. Whether for a corporate presentation or a wedding reception, they transition effortlessly. Each pair comes with individual IGI/GIA lab certificates verifying cut, colour, clarity, and carat.</p>

<p>Close behind are our <strong>diamond tennis bracelets</strong> — a single row of graduated round diamonds set in 18K gold — and our <strong>solitaire pendants</strong> that pair beautifully with the chains described above. For those considering a significant milestone gift, our <a href="/blog/solitaire-ring-buying-guide-gurgaon">complete solitaire ring buying guide</a> walks you through exactly what to look for in cuts, clarity grades, and price ranges before visiting our showroom.</p>

<h2>Bridal Bestsellers</h2>

<p>Every bridal season reinforces which sets stand above the rest. Our <strong>Kundan-polki neckpiece with matching maang tikka and jhumkas</strong> remains the centrepiece of numerous Gurgaon weddings. For the modern bride who prefers a lighter, diamond-forward look, our <strong>18K white-and-yellow gold bridal sets</strong> — combining a statement necklace with matching earrings and a delicate bracelet — have earned rave reviews from families across sectors 40–55.</p>

<p>Planning a wedding? Read our in-depth article on <a href="/blog/luxury-bridal-gold-jewellery-gurgaon">selecting a luxury bridal gold jewellery set in Gurgaon</a> to understand your options across price points and traditions.</p>

<h2>Why These Pieces Become Bestsellers</h2>

<p>Three things distinguish a bestselling piece at Auric Jewels from an average one:</p>
<ul>
  <li><strong>Versatility</strong> — it works across occasions without looking out of place.</li>
  <li><strong>Certified quality</strong> — every gold item is BIS hallmarked and every diamond is individually certified.</li>
  <li><strong>Enduring design</strong> — the silhouette does not look dated after two or three seasons.</li>
</ul>

<p>Our in-store stylists are trained to help you identify which pieces from this collection align with your lifestyle, wardrobe, and long-term collection goals. There is no pressure — only expert guidance.</p>

<h2>Visit Our Showroom or WhatsApp Us</h2>

<p><strong>Auric Jewels</strong> is located at <strong>Sector 45, Gurugram</strong>, with ample parking and a relaxed, appointment-friendly environment. Our showroom is open seven days a week. You can also reach our jewellery consultants on WhatsApp for photos, pricing, and availability before you visit.</p>

<p>Whether you are buying your first diamond piece or adding to a curated family collection, our bestsellers showcase is the ideal place to begin. Every piece is in stock, hallmarked or certified, and available with complimentary gift packaging.</p>
""",
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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://auric.thecodemesh.online",
            "Referer": "https://auric.thecodemesh.online/",
        },
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



def find_page_by_slug(slug):
    """Return existing page ID for a slug, or None."""
    r = gql('{ pages(first: 100) { edges { node { id slug } } } }')
    edges = ((r.get("data") or {}).get("pages") or {}).get("edges", [])
    for e in edges:
        if e["node"]["slug"] == slug:
            return e["node"]["id"]
    return None


def update_page(page_id, content_json):
    mutation = """
    mutation PageUpdate($id: ID!, $input: PageInput!) {
        pageUpdate(id: $id, input: $input) {
            page { id slug title }
            errors { field message code }
        }
    }"""
    variables = {"id": page_id, "input": {
        "title":       PAGE["title"],
        "isPublished": True,
        "content":     content_json,
        "seo": {"title": PAGE["seoTitle"], "description": PAGE["seoDescription"]},
    }}
    r = gql(mutation, variables)
    if "httpError" in r or "error" in r:
        print(f"  FAILED: {r}")
        sys.exit(1)
    pu = (r.get("data") or {}).get("pageUpdate", {})
    if pu.get("errors"):
        err = pu["errors"][0]
        if err.get("code") == "UNIQUE":
            print(f"  Slug already exists — updating instead ...")
            page_id = find_page_by_slug(PAGE["slug"])
            if not page_id:
                print(f"  Could not find existing page. Aborting.")
                sys.exit(1)
            return update_page(page_id, content_json)
        print(f"  SALEOR ERROR: {err.get('field')} — {err.get('message')} ({err.get('code')})")
        sys.exit(1)
    page = pu.get("page")
    print(f"  UPDATED  id={page['id']}")
    print(f"  URL: https://www.auricjewels.com/page/{PAGE['slug']}")
    return page["id"]

def create_page():
    content_json = json.dumps({
        "blocks": [{"type": "rawHtml", "data": {"html": PAGE["content"]}}]
    })

    mutation = """
    mutation PageCreate($input: PageCreateInput!) {
        pageCreate(input: $input) {
            page { id slug title }
            errors { field message code }
        }
    }"""

    variables = {"input": {
        "slug":        PAGE["slug"],
        "title":       PAGE["title"],
        "pageType":    PAGE_TYPE_ID,
        "isPublished": True,
        "content":     content_json,
        "seo": {
            "title":       PAGE["seoTitle"],
            "description": PAGE["seoDescription"],
        },
    }}

    print(f"Creating page: {PAGE['slug']} ...")
    r = gql(mutation, variables)

    if "httpError" in r or "error" in r:
        print(f"  FAILED: {r}")
        sys.exit(1)

    pc = (r.get("data") or {}).get("pageCreate", {})
    if pc.get("errors"):
        err = pc["errors"][0]
        print(f"  SALEOR ERROR: {err.get('field')} — {err.get('message')} ({err.get('code')})")
        sys.exit(1)

    page = pc.get("page")
    if not page:
        print(f"  Unexpected response: {json.dumps(r)[:300]}")
        sys.exit(1)

    print(f"  SUCCESS  id={page['id']}")
    print(f"  URL: https://www.auricjewels.com/page/{PAGE['slug']}")
    return page["id"]


def add_metadata(page_id):
    mutation = """
    mutation($id: ID!, $input: [MetadataInput!]!) {
        updateMetadata(id: $id, input: $input) {
            item { metadata { key value } }
            errors { field message }
        }
    }"""
    r = gql(mutation, {"id": page_id, "input": [{"key": "type", "value": "collection"}]})
    if (r.get("data") or {}).get("updateMetadata", {}).get("errors"):
        print(f"  Metadata warning: {r['data']['updateMetadata']['errors']}")
    else:
        print("  Metadata: type=collection added")


if __name__ == "__main__":
    page_id = create_page()
    add_metadata(page_id)
    print("Done.")
