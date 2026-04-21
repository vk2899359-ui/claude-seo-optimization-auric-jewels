#!/usr/bin/env python3
"""
Auric Jewels — Create SEO Collection Page #6
Slug: diamond-jewellery-gurgaon-collection
Run: python scripts/page-06-diamond-collection.py
"""
import json, urllib.request, urllib.error, sys

API          = "https://auric.thecodemesh.online/graphql/"
TOKEN        = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

PAGE = {
    "slug": "diamond-jewellery-gurgaon-collection",
    "title": "Diamond Jewellery Collection Gurgaon | IGI/GIA Certified",
    "seoTitle": "Diamond Jewellery Collection | IGI/GIA Certified | Auric Jewels",
    "seoDescription": (
        "Explore Auric Jewels' certified diamond jewellery collection in Gurgaon. "
        "IGI & GIA certified solitaires, pendants, earrings & bracelets in 18K gold. "
        "Sector 45 showroom — visit or WhatsApp for expert guidance."
    ),
    "content": """
<h1>Diamond Jewellery Collection Gurgaon | IGI/GIA Certified</h1>

<p>A diamond is only as valuable as the trust behind it. At <strong>Auric Jewels, Sector 45 Gurugram</strong>, every diamond in our collection is individually certified by IGI (International Gemological Institute) or GIA (Gemological Institute of America) — the two most trusted names in diamond grading globally. When you purchase a diamond from Auric Jewels, you receive not just a beautiful stone but a permanent record of its cut grade, colour, clarity, and exact carat weight. That documentation protects your investment and your family's for generations.</p>

<h2>Understanding Diamond Certification</h2>

<p>IGI and GIA certifications are internationally recognised assessments of a diamond's four Cs: <strong>Cut, Colour, Clarity, and Carat</strong>. Cut determines how brilliantly the stone reflects light — an excellent or ideal cut maximises sparkle. Colour is graded from D (colourless) through to Z (light yellow); most premium jewellery uses stones in the D–J range. Clarity assesses internal and surface characteristics — VS1 and VS2 grades are considered eye-clean and represent outstanding value.</p>

<p>When you buy a certified diamond, you know exactly what you own. When you sell or exchange it in the future, you receive accurate value for it. Uncertified diamonds, by contrast, are valued on trust — and trust is not a metric. Read our thorough comparison of <a href="/blog/lab-grown-vs-natural-diamonds-comparison-india">lab-grown vs natural diamonds in India</a> to understand how certification works across both categories.</p>

<h2>Solitaire Rings & Pendants</h2>

<p>Our solitaire collection spans from 0.15 carats to 2.00 carats in round-brilliant, princess, cushion, pear, and oval cuts. Each stone is set in either 18K white gold, yellow gold, or platinum-plated settings, with prong, bezel, and channel setting options. A <strong>round-brilliant solitaire ring</strong> in a four-prong setting remains our best-selling diamond piece — and for many Gurgaon families, the first significant diamond purchase they make.</p>

<p>Our <strong>solitaire pendants</strong> pair beautifully with our slim gold chains for a complete look that works from boardroom to dinner. The pendant-chain combination is also a thoughtful first diamond gift because it is size-agnostic — unlike rings, no ring-sizing consultation is required.</p>

<p>Before purchasing a solitaire, read our <a href="/blog/solitaire-ring-buying-guide-gurgaon">complete solitaire ring buying guide for Gurgaon</a> — it covers diamond cuts, clarity grades, price-to-quality ratios, and what to ask your jeweller.</p>

<h2>Diamond Earrings: Our Widest Range</h2>

<p>Earrings represent our deepest diamond inventory. From 0.05-carat pavé studs to 2-carat statement drop earrings, we carry styles to suit every occasion and face shape. Our most popular styles include:</p>
<ul>
  <li><strong>Classic round-brilliant studs</strong> — the foundation of any jewellery collection</li>
  <li><strong>Halo stud earrings</strong> — a central stone surrounded by pavé diamonds for a larger visual impact at a controlled price</li>
  <li><strong>Diamond jhumkas</strong> — gold-top earrings with cascading diamond drops for traditional occasions</li>
  <li><strong>Diamond hoops</strong> — inside-set or outside-set with small rounds for everyday elegance</li>
  <li><strong>Drop and chandelier earrings</strong> — designed for weddings, receptions, and formal events</li>
</ul>

<h2>Diamond Bracelets & Necklaces</h2>

<p>Our <strong>diamond tennis bracelets</strong> in 18K gold are a signature piece for the Auric Jewels collection — a single continuous row of matched round brilliants, certified and set with precision. Available in total diamond weights from 0.50 carats to 3.00 carats, with matching necklace options for those who want a set.</p>

<p>Our <strong>diamond necklaces</strong> range from delicate single-diamond pendants to multi-row cluster designs for weddings and receptions. Cluster necklaces in 18K yellow or white gold, featuring between 1 and 5 carats of total diamond weight, are designed to make a statement at Indian weddings while remaining mountable as fine jewellery year-round.</p>

<h2>Custom Diamond Jewellery</h2>

<p>Every piece in our collection can also be made to order in a custom configuration. Bring your diamond budget, your design inspiration (a photo, a sketch, or simply a description), and let our design team create something original. Read about <a href="/blog/custom-diamond-jewellery-gurgaon">the custom diamond jewellery process at Auric Jewels</a> — from initial consultation through certification and delivery.</p>

<p>Visit our <strong>Sector 45, Gurugram showroom</strong> or contact us on WhatsApp to begin your diamond jewellery journey with complete confidence and transparent pricing.</p>
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
