#!/usr/bin/env python3
"""
Auric Jewels — Create SEO Collection Page #5
Slug: bridal-jewellery-gurgaon
Run: python scripts/page-05-bridal.py
"""
import json, urllib.request, urllib.error, sys

API          = "https://auric.thecodemesh.online/graphql/"
TOKEN        = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

PAGE = {
    "slug": "bridal-jewellery-gurgaon",
    "title": "Bridal Jewellery in Gurgaon | Wedding Gold & Diamond Sets",
    "seoTitle": "Bridal Jewellery Gurgaon | Wedding Gold & Diamond Sets | Auric Jewels",
    "seoDescription": (
        "Shop bridal jewellery at Auric Jewels, Sector 45 Gurgaon. Complete wedding gold & "
        "diamond sets — necklaces, maang tikka, jhumkas & bangles. BIS hallmarked, "
        "IGI certified. Book a bridal consultation today."
    ),
    "content": """
<h1>Bridal Jewellery in Gurgaon | Wedding Gold & Diamond Sets</h1>

<p>Your wedding jewellery will be photographed more than almost anything else in your life — and it will be treasured across generations. At <strong>Auric Jewels, Sector 45 Gurugram</strong>, we take bridal jewellery with the seriousness it deserves. Every set in our bridal collection is crafted to hold up under studio lighting and the scrutiny of time, combining traditional craftsmanship with contemporary sensibilities that suit the modern bride.</p>

<h2>The Complete Bridal Set: What You Need</h2>

<p>A traditional North Indian bridal look typically requires seven to nine pieces of jewellery worn across different moments of the wedding: the <strong>necklace (or two-necklace combination)</strong>, <strong>maang tikka</strong>, <strong>jhumkas or chandbaalis</strong>, <strong>nath (nose ring)</strong>, <strong>bangles or kadas</strong>, <strong>haath phool or bracelet</strong>, <strong>waist chain (kamarband)</strong>, and <strong>payal (anklets)</strong>. Not every bride chooses all nine, but understanding the complete set helps you plan your jewellery budget across pieces with very different price points.</p>

<p>Our bridal consultants will guide you through every element, including which pieces to invest more heavily in (necklace, earrings) and which can be more design-focused than investment-focused (maang tikka, nath). Read our detailed guide on <a href="/blog/luxury-bridal-gold-jewellery-gurgaon">planning a luxury bridal gold jewellery set in Gurgaon</a> before your consultation for a head start.</p>

<h2>Gold Bridal Collections</h2>

<p>Our <strong>22K Kundan-polki bridal sets</strong> are designed for the bride who wants to honour tradition without sacrificing visual impact. Kundan work — setting uncut gemstones in purified gold foil — creates a rich, regal look that photographs beautifully in natural and artificial light alike. Our sets come in complete versions (necklace, earrings, maang tikka, and nath as a set) and individual pieces for brides who already own some elements.</p>

<p>For brides who prefer a more contemporary profile, our <strong>18K gold bridal sets with diamond accents</strong> combine yellow and white gold with certified pavé diamonds to create pieces that feel bridal yet modern. These sets suit outdoor wedding receptions and destination weddings particularly well.</p>

<h2>Diamond Bridal Jewellery</h2>

<p>Diamond-forward bridal jewellery is growing in popularity among Gurgaon brides, particularly for the reception and honeymoon. Our <strong>statement diamond necklaces in 18K white gold</strong> — rivière styles, cluster designs, and bib necklaces — create the visual drama of a traditional bridal necklace with a contemporary lightness and sparkle that gold alone cannot achieve.</p>

<p>Our <strong>diamond jhumka earrings</strong> bridge tradition and modernity beautifully. A pavé-set gold top with cascading diamond drops suits the sari, lehenga, and anarkali alike. If you are considering the difference between traditional polki, Kundan, and certified diamond sets for your wedding, our blog post on <a href="/blog/polki-vs-kundan-vs-diamond-bridal-set">Polki vs Kundan vs Diamond bridal sets</a> lays out the comparison in detail.</p>

<h2>The Bridal Consultation at Auric Jewels</h2>

<p>We strongly recommend booking a dedicated bridal consultation at least three months before your wedding date. This allows time for custom work if required, alterations, and sizing. During your consultation, you will:</p>
<ul>
  <li>Try on sets against your lehenga or saree fabric and colour</li>
  <li>Receive an honest assessment of what suits your face shape and neckline</li>
  <li>Discuss your total jewellery budget and how to allocate it across pieces</li>
  <li>Receive a written quotation with timelines and certification details</li>
</ul>

<h2>After the Wedding: Your Jewellery as an Asset</h2>

<p>Bridal jewellery from Auric Jewels does not retire after the wedding. Our pieces are designed for post-wedding wearability — statement earrings that transition to formal events, necklaces that work as statement pieces for festivals, and gold sets that can be melted or exchanged for contemporary designs as your taste evolves. Every piece includes our <strong>lifetime exchange policy</strong>, ensuring your investment grows with you.</p>

<p>Visit our <strong>Sector 45, Gurugram showroom</strong> or WhatsApp us to schedule your bridal consultation. We serve brides from across the Delhi NCR region, and our team has helped hundreds of Gurgaon families create their perfect wedding jewellery story.</p>
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
