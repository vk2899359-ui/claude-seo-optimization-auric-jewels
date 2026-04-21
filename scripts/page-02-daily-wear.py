#!/usr/bin/env python3
"""
Auric Jewels — Create SEO Collection Page #2
Slug: daily-wear-jewellery-gurgaon
Run: python scripts/page-02-daily-wear.py
"""
import json, urllib.request, urllib.error, sys

API          = "https://auric.thecodemesh.online/graphql/"
TOKEN        = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

PAGE = {
    "slug": "daily-wear-jewellery-gurgaon",
    "title": "Daily Wear Gold & Diamond Jewellery | Lightweight Designs",
    "seoTitle": "Daily Wear Gold & Diamond Jewellery Gurgaon | Lightweight | Auric Jewels",
    "seoDescription": (
        "Shop daily wear gold & diamond jewellery at Auric Jewels, Sector 45 Gurgaon. "
        "Lightweight 18K & 22K gold designs — studs, chains, bangles & pendants for "
        "everyday elegance. BIS hallmarked & IGI certified."
    ),
    "content": """
<h1>Daily Wear Gold & Diamond Jewellery | Lightweight Designs</h1>

<p>The most well-dressed women in Gurgaon share one trait: they wear fine jewellery not just for weddings and festivals but every single day. At <strong>Auric Jewels, Sector 45 Gurugram</strong>, our daily wear collection is built on this very insight — jewellery that is lightweight enough to forget you are wearing it, yet refined enough that people notice when you are not.</p>

<h2>What Makes a Piece Truly Wearable Every Day?</h2>

<p>Daily wear jewellery must clear three hurdles: <strong>comfort, durability, and versatility</strong>. A pair of studs that snags on your hair, bangles that clink distractingly through meetings, or a chain that requires daily polishing simply will not survive a busy schedule. Our daily wear range is designed with these realities in mind.</p>

<p>We work in <strong>18-karat gold</strong> for most daily wear diamond pieces — an alloy strong enough to resist scratching and deformation during regular activity. For plain gold pieces like chains and bangles, <strong>22-karat gold</strong> with reinforced closures and polished finishes ensures beauty that endures. Every piece in this collection carries a <strong>BIS HUID hallmark</strong>, so the purity you are promised is the purity you receive.</p>

<h2>Diamond Jewellery for the Working Woman</h2>

<p>A single round-brilliant <strong>diamond stud in 18K white gold</strong> is the most versatile piece in any jewellery collection. It pairs equally well with a crisp formal shirt on a Monday morning and a silk saree on a Friday evening. Our studs start from 0.10 carats per pair and scale up to 1 carat total weight, all carrying individual IGI or GIA certificates.</p>

<p>Our <strong>petite diamond pendants</strong> — round halos, bezel-set solitaires, and delicate floral designs — sit perfectly on both 18-inch and 20-inch chains for different necklines. These pendants are our most gifted daily wear pieces, and for good reason: they suit every age, every outfit, and every occasion that falls between "casual" and "grand".</p>

<p>For those who prefer something on the wrist, our <strong>diamond tennis bracelets in reduced-carat, slim-band versions</strong> are designed for daily wear. A 2mm-wide bracelet set with 0.50 carats of total diamond weight looks elegant without feeling precious or fragile.</p>

<p>Read our full guide on <a href="/blog/diamond-earrings-daily-wear-under-50000">the best diamond earring designs for daily wear under ₹50,000</a> to understand which styles deliver the best value and longevity.</p>

<h2>Lightweight Gold for Everyday Life</h2>

<p>Our <strong>hollow gold chains</strong> in 22K offer the visual richness of solid gold at a fraction of the weight — ideal for women who want a prominent chain presence without neck fatigue. Box chains, rope chains, and Singapore designs all come in widths from 1mm to 3mm.</p>

<p><strong>Plain gold bangles</strong> in round cross-sections are our top sellers for daily wear. A pair of 22K bangles in 2mm to 3mm thickness is light enough to wear from morning to night and durable enough to last decades. We also carry <strong>gold kadas with plain and textured finishes</strong> for those who prefer a single, heavier piece over multiple thinner ones.</p>

<p>Working women particularly love our <strong>stacking rings in 18K gold</strong> — thin bands in plain, milgrain, and channel-set diamond styles that can be worn alone or combined. Read our detailed guide on <a href="/blog/lightweight-gold-jewellery-working-women-daily-wear">lightweight gold jewellery for working women</a> to see how to build a complete daily wear collection from scratch.</p>

<h2>Care Tips for Daily Wear Jewellery</h2>

<p>Even the most hardwearing pieces benefit from simple care. Remove jewellery before swimming, heavy exercise, or applying perfume and lotion. Wipe pieces with a soft dry cloth after wearing. Store daily wear items separately in fabric pouches rather than loose in a drawer. Following these habits will keep your pieces looking showroom-fresh for years.</p>

<h2>Visit Our Showroom or Shop Online</h2>

<p>Our daily wear collection is displayed in dedicated cases at our <strong>Sector 45, Gurugram showroom</strong>. Our consultants are trained to help you select pieces that work across multiple roles — from boardroom to dinner table. Walk in any day of the week, or WhatsApp us for photos and pricing before you visit. Every purchase comes with complimentary gift packaging, a care guide, and a hallmark or certification document.</p>
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
        "seo": {"title": PAGE["seoTitle"], "description": PAGE["seoDescription"]},
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
    errs = ((r.get("data") or {}).get("updateMetadata") or {}).get("errors", [])
    if errs:
        print(f"  Metadata warning: {errs}")
    else:
        print("  Metadata: type=collection added")


if __name__ == "__main__":
    page_id = create_page()
    add_metadata(page_id)
    print("Done.")
