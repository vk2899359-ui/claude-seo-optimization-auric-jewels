#!/usr/bin/env python3
"""
Auric Jewels — Create SEO Collection Page #4
Slug: gifts-under-50000-jewellery
Run: python scripts/page-04-gifts-under-50000.py
"""
import json, urllib.request, urllib.error, sys

API          = "https://auric.thecodemesh.online/graphql/"
TOKEN        = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

PAGE = {
    "slug": "gifts-under-50000-jewellery",
    "title": "Premium Jewellery Gifts Under ₹50,000 | Auric Jewels",
    "seoTitle": "Premium Jewellery Gifts Under ₹50,000 | Diamonds & Gold | Auric Jewels",
    "seoDescription": (
        "Shop premium jewellery gifts under ₹50,000 at Auric Jewels, Sector 45 Gurgaon. "
        "Diamond tennis bracelets, gold necklaces, solitaire pendants & more — "
        "IGI certified, BIS hallmarked, gifted with elegance."
    ),
    "content": """
<h1>Premium Jewellery Gifts Under ₹50,000 | Auric Jewels</h1>

<p>Between ₹25,000 and ₹50,000 lies one of the most rewarding gifting territories in fine jewellery. At this tier, diamond pieces grow meaningfully in carat weight and design complexity, and gold jewellery can carry significant visual and intrinsic presence. At <strong>Auric Jewels, Sector 45 Gurugram</strong>, we have curated our most sought-after pieces in this range — every one BIS hallmarked or IGI/GIA certified, and each telling a story worthy of the occasion.</p>

<h2>Diamond Jewellery That Makes a Statement</h2>

<p>The ₹25,000–₹50,000 band opens up exceptional diamond gifting possibilities. Our <strong>diamond tennis bracelets in slim 18K white or yellow gold</strong> — featuring 0.50 to 0.75 carats of total diamond weight — are among our most gifted pieces in this range. The effect is luxurious: a continuous line of round-brilliant diamonds that catches the light with every movement. Each bracelet comes with IGI certification for the diamonds used.</p>

<p>A <strong>three-stone diamond ring</strong> in 18K gold, symbolising past, present, and future, is a profoundly meaningful gift for significant milestones. We offer these from 0.30 carats total weight (three matched round brilliants) through to 0.75 carats. If the recipient prefers earrings, our <strong>diamond halo stud earrings</strong> — a central brilliant surrounded by a ring of pavé diamonds — deliver outstanding visual impact in the ₹30,000–₹48,000 range.</p>

<p>For those who love understated luxury, a <strong>bezel-set solitaire necklace in 18K gold</strong> featuring a 0.25–0.40 carat IGI-certified diamond is one of the most wearable gifting choices we offer. It works with office wear, evening wear, and traditional Indian attire alike.</p>

<h2>Gold Jewellery With Presence</h2>

<p>In gold, this budget commands real presence. A <strong>22K gold necklace in 12–18 grams</strong> — whether a plain cable chain, a textured snake design, or a traditional thushi (layered choker) — represents significant intrinsic and aesthetic value. Gold at this weight is not a trinket; it is an heirloom-in-progress.</p>

<p>Our <strong>gold bangles with diamond or gemstone accents</strong> in 18K gold sit beautifully in the ₹28,000–₹46,000 range. A pair of 18K bangles with pavé diamonds along the top arc is the kind of piece that earns compliments at every gathering. For a more traditional choice, our <strong>22K gold necklaces with temple-work pendants</strong> are perennially popular gifting choices for festivals, weddings, and milestone birthdays.</p>

<h2>For Every Milestone Gift</h2>

<p>This budget is ideal for:</p>
<ul>
  <li><strong>Milestone anniversaries</strong> (5th, 10th, 15th years) — our guide to <a href="/blog/anniversary-gift-jewellery-gurgaon">anniversary jewellery gifts by milestone year</a> can help you choose</li>
  <li><strong>Significant birthdays</strong> (30th, 40th, 50th) — a diamond piece she will wear for decades</li>
  <li><strong>Promotions and achievements</strong> — celebrate professional success with lasting elegance</li>
  <li><strong>Wedding gifts for the bride</strong> — a certified diamond piece to complement her bridal set</li>
  <li><strong>Mother's Day and Karva Chauth</strong> — meaningful gold or diamond gifting for the women who matter most</li>
</ul>

<h2>The Auric Jewels Gifting Experience</h2>

<p>Every gift purchase at our showroom includes complimentary premium packaging, the original certification document (IGI/GIA report or BIS hallmark), and a personalised gift card. Our gift consultants will spend time understanding the recipient — her style, her metal preference, and the occasions she dresses for — before recommending pieces. You will never feel rushed, and you will leave confident that your gift will be treasured.</p>

<p>WhatsApp us a photo of the recipient's existing jewellery for style matching, or visit our <strong>Sector 45, Gurugram showroom</strong> any day of the week to browse in person. For further guidance on what makes a gift truly special, read our <a href="/blog/solitaire-ring-buying-guide-gurgaon">solitaire ring buying guide</a> — the same principles of quality and value apply across all our certified diamond gifting pieces.</p>
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
