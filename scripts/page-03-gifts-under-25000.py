#!/usr/bin/env python3
"""
Auric Jewels — Create SEO Collection Page #3
Slug: gifts-under-25000-jewellery
Run: python scripts/page-03-gifts-under-25000.py
"""
import json, urllib.request, urllib.error, sys

API          = "https://auric.thecodemesh.online/graphql/"
TOKEN        = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

PAGE = {
    "slug": "gifts-under-25000-jewellery",
    "title": "Jewellery Gifts Under ₹25,000 | Perfect for Every Occasion",
    "seoTitle": "Jewellery Gifts Under ₹25,000 | Gold & Diamond Gifting | Auric Jewels Gurgaon",
    "seoDescription": (
        "Find the perfect jewellery gift under ₹25,000 at Auric Jewels, Sector 45 Gurgaon. "
        "Diamond studs, gold pendants, bracelets & chains — hallmarked & certified, "
        "beautifully gift-wrapped for every occasion."
    ),
    "content": """
<h1>Jewellery Gifts Under ₹25,000 | Perfect for Every Occasion</h1>

<p>Fine jewellery has always been the gift that outlasts every other — more personal than flowers, more enduring than experiences, more meaningful than gadgets. At <strong>Auric Jewels, Sector 45 Gurugram</strong>, our curated selection of jewellery gifts under ₹25,000 proves that you do not need an unlimited budget to give something truly extraordinary. Every piece here is BIS hallmarked or IGI/GIA certified, gift-wrapped at no extra charge, and backed by a lifetime exchange policy.</p>

<h2>Diamond Pieces Under ₹25,000</h2>

<p>Certified diamond jewellery begins well within this range. Our <strong>diamond stud earrings in 18K white gold</strong> — featuring round-brilliant diamonds from 0.10 carats per pair up to 0.30 carats — are among our most gifted pieces. Each pair comes with an IGI certificate, which adds tangible value to the gift beyond its aesthetic beauty. The recipient holds documentation confirming exactly what they own.</p>

<p>Our <strong>solitaire diamond pendants in 18K yellow or white gold</strong> sit beautifully in the ₹12,000–₹22,000 range depending on carat weight. Paired with a slim gold chain, these make an especially thoughtful gift because they transition effortlessly from daily wear to formal occasions. A <strong>single-stone diamond nose pin</strong> in 18K gold is another popular choice — delicate, personal, and priced accessibly within this range.</p>

<h2>Gold Jewellery Gifts That Impress</h2>

<p>A <strong>22K gold chain in 5–7 grams</strong> makes a classic, practical gift that appreciates in value over time. Box or Singapore-link chains in this weight range fall comfortably under ₹25,000 at prevailing gold rates, and their versatility means they pair with almost anything. For a more decorative option, our <strong>gold pendants with enamel or stone accents</strong> — temple motifs, floral patterns, and geometric designs — are priced in the ₹8,000–₹18,000 range.</p>

<p><strong>Gold bangles in 22K</strong> (2mm to 3mm round cross-section, single bangle) are another thoughtful choice. Lightweight enough for daily wear, they carry the cultural significance of gold gifting that resonates deeply in Indian households. A pair of slim <strong>22K gold hoop earrings</strong> with a plain or twisted finish is a perennial gifting favourite for younger recipients.</p>

<h2>Occasions This Budget Covers Beautifully</h2>

<ul>
  <li><strong>Birthdays</strong> — diamond studs or a gold pendant with a personal touch</li>
  <li><strong>Diwali & Dhanteras</strong> — gold coins, small gold chains, or diamond earrings</li>
  <li><strong>Baby showers & naming ceremonies</strong> — gold anklets, small gold bangles, or a gold coin</li>
  <li><strong>Farewell & retirement gifts</strong> — a meaningful gold pendant or delicate diamond piece</li>
  <li><strong>Raksha Bandhan</strong> — a gold bracelet or diamond pendant for a sister</li>
  <li><strong>Karva Chauth</strong> — a gold chain or diamond mangalsutra pendant to complement the occasion</li>
</ul>

<p>For anniversary gifting across different milestone years, read our guide on <a href="/blog/anniversary-gift-jewellery-gurgaon">the best anniversary jewellery gifts in Gurgaon</a> — it covers ideal pieces by milestone year and budget tier.</p>

<h2>Gifting Made Easy at Auric Jewels</h2>

<p>Every gift purchase at our showroom comes with:</p>
<ul>
  <li>Complimentary premium gift packaging with ribbon</li>
  <li>BIS hallmark certificate or IGI/GIA lab report (included with the piece)</li>
  <li>A personalised gift message card on request</li>
  <li>Lifetime exchange policy — your recipient can upgrade or exchange the piece at any future date</li>
</ul>

<p>Not sure what to pick? Our gift consultants at the <strong>Sector 45, Gurugram showroom</strong> are trained to help. Tell us who the gift is for, the occasion, and your exact budget — and we will show you three to five options that fit perfectly. You can also WhatsApp us photos of your preferred pieces before visiting, so your in-store experience is efficient and enjoyable.</p>

<h2>Why Certified Jewellery Makes a Better Gift</h2>

<p>A gift of certified jewellery carries an implicit message: <em>I valued you enough to choose something real</em>. Understanding <a href="/blog/bis-hallmark-gold-jewellery-buying-guide">why BIS hallmarking matters</a> helps both the giver and the recipient appreciate the full value of what is being exchanged. At Auric Jewels, no piece leaves our showroom without proper certification — making every gift one that stands up to scrutiny and stands the test of time.</p>
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
