#!/usr/bin/env python3
"""
Auric Jewels — Create SEO Collection Page #9
Slug: anniversary-gift-jewellery-gurgaon
Run: python scripts/page-09-anniversary.py
"""
import json, urllib.request, urllib.error, sys

API          = "https://auric.thecodemesh.online/graphql/"
TOKEN        = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

PAGE = {
    "slug": "anniversary-gift-jewellery-gurgaon",
    "title": "Anniversary Jewellery Gifts in Gurgaon | Diamonds & Gold",
    "seoTitle": "Anniversary Jewellery Gifts Gurgaon | Diamonds & Gold | Auric Jewels",
    "seoDescription": (
        "Find the perfect anniversary jewellery gift at Auric Jewels, Sector 45 Gurgaon. "
        "Diamond rings, gold necklaces & certified solitaires for every milestone year. "
        "Free gift packaging. WhatsApp for expert advice."
    ),
    "content": """
<h1>Anniversary Jewellery Gifts in Gurgaon | Diamonds & Gold</h1>

<p>An anniversary is one of those rare occasions that calls for a gift that matches the weight of the moment. Flowers fade. Experiences end. Jewellery endures — worn on the wrist or at the neck every day, or stored carefully for the next celebration, it carries the memory of the occasion forward indefinitely. At <strong>Auric Jewels, Sector 45 Gurugram</strong>, we have helped hundreds of couples mark their anniversaries with pieces that will outlast the bouquets and dinners by decades.</p>

<h2>Matching the Gift to the Milestone</h2>

<p>Different anniversary years carry different traditions and emotional significance. Our gift consultants at Auric Jewels have recommendations calibrated to each:</p>

<ul>
  <li><strong>1st Anniversary (Paper):</strong> A delicate diamond pendant on a gold chain — something light and personal to begin the jewellery collection together.</li>
  <li><strong>5th Anniversary (Wood):</strong> Diamond stud earrings in 18K white gold — a piece she will wear for the next 50 years.</li>
  <li><strong>10th Anniversary (Tin/Aluminium):</strong> A diamond tennis bracelet — substantial, beautiful, and designed for lifelong wear.</li>
  <li><strong>15th Anniversary (Crystal):</strong> A solitaire ring upgrade or a three-stone diamond ring (past, present, future).</li>
  <li><strong>20th Anniversary (China):</strong> A diamond-and-gold necklace or significant gold set — a piece worthy of a milestone two decades in the making.</li>
  <li><strong>25th Anniversary (Silver):</strong> A statement diamond piece or a classic gold necklace — something that can eventually become a family heirloom.</li>
</ul>

<p>For a complete anniversary gifting strategy across milestone years, read our in-depth guide on <a href="/blog/anniversary-gift-jewellery-gurgaon">anniversary jewellery gift ideas for her in Gurgaon</a>.</p>

<h2>Diamond Anniversary Gifts</h2>

<p>Diamonds have become the quintessential anniversary gift because they embody permanence — and because their value is documented and verifiable. Every diamond piece at Auric Jewels carries an IGI or GIA certificate confirming cut, colour, clarity, and carat weight. When you give a certified diamond, you give something that can be independently verified, exchanged, upgraded, and passed down.</p>

<p>Our most popular anniversary diamond gifts include:</p>
<ul>
  <li><strong>Solitaire diamond ring</strong> — an upgrade to or addition alongside the original engagement ring</li>
  <li><strong>Diamond eternity band</strong> — a ring set all the way around with small matched diamonds, traditionally given to mark the birth of a child or a significant anniversary</li>
  <li><strong>Diamond pendant and chain set</strong> — elegant, versatile, worn daily</li>
  <li><strong>Diamond drop earrings</strong> — for the woman who prefers earrings above all other jewellery</li>
</ul>

<p>Read about <a href="/blog/solitaire-vs-diamond-ring-difference">the difference between solitaire and diamond rings</a> before choosing — it helps clarify which style suits her best.</p>

<h2>Gold Anniversary Gifts</h2>

<p>Gold is never the wrong anniversary gift. Its intrinsic value grows with time, its beauty is immediate, and its cultural significance in Indian households runs deep. For anniversary gifting, our most requested gold pieces include:</p>
<ul>
  <li><strong>22K gold necklace (10–18 grams)</strong> — a statement piece for festivals and family occasions</li>
  <li><strong>18K gold bracelet with diamond accents</strong> — bridges the worlds of gold and diamond gifting</li>
  <li><strong>22K gold bangle pair</strong> — traditional, enduring, and deeply personal</li>
  <li><strong>22K gold coin</strong> — for those who prefer the investment form factor</li>
</ul>

<h2>Personalisation Options</h2>

<p>Every anniversary gift at Auric Jewels can be personalised. We offer laser engraving on the inside of rings and bangles, customised pendant shapes (initials, dates, meaningful symbols), and made-to-order pieces built around a specific design the recipient loves. Personalised pieces require a lead time of 2–4 weeks, so plan accordingly.</p>

<h2>The Gifting Experience at Our Showroom</h2>

<p>Visit our <strong>Sector 45, Gurugram showroom</strong> with her ring size (if known), a note of her metal preference, and your budget — our consultants handle everything from there. Every gift comes with premium packaging, the original certification document, and a handwritten card on request. WhatsApp us in advance and we will prepare a curated selection before you arrive, making your showroom visit swift and enjoyable.</p>
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
