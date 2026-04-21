#!/usr/bin/env python3
"""
Auric Jewels — Create SEO Collection Page #8
Slug: lightweight-gold-jewellery
Run: python scripts/page-08-lightweight-gold.py
"""
import json, urllib.request, urllib.error, sys

API          = "https://auric.thecodemesh.online/graphql/"
TOKEN        = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

PAGE = {
    "slug": "lightweight-gold-jewellery",
    "title": "Lightweight Gold Jewellery for Daily Use | Auric Jewels",
    "seoTitle": "Lightweight Gold Jewellery Daily Use Gurgaon | 18K 22K | Auric Jewels",
    "seoDescription": (
        "Shop lightweight gold jewellery for daily use at Auric Jewels, Sector 45 Gurgaon. "
        "18K & 22K gold chains, studs, bangles & rings — BIS hallmarked, "
        "designed for all-day comfort and lasting elegance."
    ),
    "content": """
<h1>Lightweight Gold Jewellery for Daily Use | Auric Jewels</h1>

<p>Gold jewellery has been woven into Indian daily life for thousands of years — and yet the designs that serve daily wear best are not the grandest or the heaviest. They are the ones that feel like a natural extension of the body: light enough to forget, beautiful enough to remember. At <strong>Auric Jewels, Sector 45 Gurugram</strong>, our lightweight gold collection is built on this philosophy — every piece BIS hallmarked, every gram accounted for.</p>

<h2>Why Weight Matters in Daily Wear Gold</h2>

<p>The traditional heavy gold sets worn for weddings and major occasions serve their purpose magnificently — but wearing them daily causes neck fatigue, skin irritation from pressure, and unnecessary wear on both the piece and the wearer. <strong>Lightweight gold jewellery</strong> in the 2–8 gram range per piece is designed for all-day comfort without sacrificing the intrinsic value and beauty of gold.</p>

<p>At current gold rates, even a 4-gram 22K necklace carries meaningful gold value — typically ₹22,000–₹30,000 at prevailing rates, varying with the market. This means lightweight is not the same as inexpensive. It simply means smart design — hollow constructions, open-link patterns, and slim profiles that maximise visual presence per gram. Read our guide on <a href="/blog/gold-rate-today-gurgaon-buying-tips">understanding gold rates in Gurgaon</a> to appreciate how weight translates to value.</p>

<h2>Lightweight Gold Chains</h2>

<p>Our best-selling lightweight chains include the <strong>box chain in 22K gold (1mm–1.5mm width, 3–5 grams)</strong>, the <strong>rope chain in 22K (2mm, 4–6 grams)</strong>, and the <strong>Singapore chain in 22K (1.5mm, 3–4 grams)</strong>. These styles are strong enough for daily wear — the twisted constructions of rope and Singapore chains resist kinking — yet light enough to be forgotten at the neck.</p>

<p>For those who prefer 18K gold, our <strong>cable and curb link chains</strong> in 18K yellow gold offer slightly more durability due to the harder alloy composition, making them ideal for active daily wear. 18K chains are also the preferred choice for diamond pendants, which we stock in styles suited to all neckline lengths.</p>

<h2>Gold Bangles That Move With You</h2>

<p>A single <strong>22K gold bangle in a round cross-section (2–3mm diameter, 5–8 grams)</strong> is perhaps the definitive lightweight gold jewellery piece for Indian women. It glides with every gesture, catches the light without demanding it, and accumulates meaning with every year it is worn. We carry bangles in plain polished, hammered, rope-textured, and floral-carved finishes — all in 22K gold with BIS HUID hallmarking.</p>

<p>For those who prefer the look of multiple bangles without the weight of multiple heavy ones, our <strong>slim bangle sets (2mm each, five bangles per set)</strong> provide the visual effect of a stacked wrist at a combined weight of 10–12 grams — far more comfortable than a single heavy bangle of the same visual mass.</p>

<h2>Gold Earrings for All Day, Every Day</h2>

<p>Our lightweight gold earring range includes <strong>small gold studs</strong> (ball, flower, and star designs in 22K, under 1 gram each), <strong>plain gold hoops</strong> (18K or 22K, 15mm–25mm diameter, 1.5–3 grams per pair), and <strong>gold drop earrings</strong> with delicate chain or filigree elements. These are the earrings you put on in the morning and forget until you look in the mirror and notice how well they complete your look.</p>

<p>Women who work or commute especially benefit from our selection of <strong>screw-back and push-back gold studs</strong>, which do not come loose during movement. See how our lightweight gold earrings fit into a complete daily wear jewellery wardrobe in our guide on <a href="/blog/lightweight-gold-jewellery-working-women-daily-wear">lightweight gold jewellery for working women</a>.</p>

<h2>Investment Value of Lightweight Gold</h2>

<p>Lightweight gold jewellery is not just a comfort choice — it is a smart financial one. Gold's value is determined by weight and purity, not by the size of the piece. A 5-gram 22K chain holds precisely the same intrinsic gold value as 5 grams of gold in any other form. When you buy from Auric Jewels, every piece comes with accurate weight documentation and BIS hallmarking, ensuring you can exchange or liquidate at fair value whenever you choose. Read about <a href="/blog/gold-jewellery-investment-2026-gurgaon">gold jewellery as an investment in 2026</a> for the full picture.</p>

<p>Visit our <strong>Sector 45, Gurugram showroom</strong> to browse our lightweight collection in person — we also accept WhatsApp enquiries for photos and pricing. Every purchase comes with certification, gift packaging, and our lifetime exchange guarantee.</p>
""",
}


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
