"""
Auric Jewels — Publish Diamond Mangalsutra Blog (April 2026 Session)
=====================================================================
Targets keyword: "diamond mangalsutra Gurgaon"
Publishes via Saleor pageCreate mutation.

USAGE:
    python3 scripts/publish-mangalsutra-blog.py
"""

import json
import sys
import time
import urllib.request
import urllib.error

API = "https://auric.thecodemesh.online/graphql/"
TOKEN = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
CHANNEL = "franchise1"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

BLOG = {
    "title": "Diamond Mangalsutra in Gurgaon: The Modern Bride’s Definitive Guide (2026)",
    "slug": "diamond-mangalsutra-gurgaon-wedding-2026",
    "seoTitle": "Diamond Mangalsutra Gurgaon — Modern Bride’s Complete Guide 2026 | Auric Jewels",
    "seoDescription": (
        "Choosing a diamond mangalsutra in Gurgaon? Discover certified designs, setting styles, "
        "IGI/GIA diamond grades & bespoke options. Expert guide by Auric Jewels Gurugram."
    ),
}

# EditorJS-format content (Saleor's rich-text storage format)
CONTENT_EDITORJS = {
    "time": int(time.time() * 1000),
    "version": "2.26.4",
    "blocks": [
        {
            "id": "blk001",
            "type": "paragraph",
            "data": {
                "text": (
                    "There is no piece in a bride’s trousseau that carries as much meaning as the mangalsutra. "
                    "Worn daily, cherished for decades, and passed on as legacy, it is the jewel that quietly "
                    "anchors everything. Yet in 2026, the diamond mangalsutra has shed the constraints of "
                    "convention — it is no longer simply ceremonial. For Gurgaon brides who move between "
                    "boardrooms, ballrooms, and family dinners with equal grace, the right diamond mangalsutra "
                    "is one that belongs in every chapter of her life."
                )
            },
        },
        {
            "id": "blk002",
            "type": "paragraph",
            "data": {
                "text": (
                    "This guide — written for the discerning buyer — walks you through every choice: "
                    "setting style, diamond quality, chain design, and how to ensure what you invest in is "
                    "certified, enduring, and uniquely yours."
                )
            },
        },
        {
            "id": "blk003",
            "type": "header",
            "data": {
                "text": "Why the Diamond Mangalsutra Has Become Gurgaon’s Most Requested Bridal Piece",
                "level": 2,
            },
        },
        {
            "id": "blk004",
            "type": "paragraph",
            "data": {
                "text": (
                    "Gurgaon’s bridal jewellery market has shifted decisively toward the diamond mangalsutra "
                    "over the past two wedding seasons. Three factors converge:"
                )
            },
        },
        {
            "id": "blk005",
            "type": "paragraph",
            "data": {
                "text": (
                    "<b>Gold at record highs.</b> With 22K gold touching ₹14,200 per gram in April 2026, "
                    "brides and families are making each gram count. A beautifully crafted diamond mangalsutra "
                    "delivers far greater visual presence — and emotional resonance — per gram of gold "
                    "than a heavy traditional chain."
                )
            },
        },
        {
            "id": "blk006",
            "type": "paragraph",
            "data": {
                "text": (
                    "<b>The shift from ceremony to continuity.</b> Today’s Gurgaon bride is not buying a "
                    "one-day showpiece. She wants jewellery that travels with her — that looks exquisite at "
                    "a reception, commanding in a meeting, and intimate at a family dinner. The diamond mangalsutra, "
                    "when chosen thoughtfully, achieves all three."
                )
            },
        },
        {
            "id": "blk007",
            "type": "paragraph",
            "data": {
                "text": (
                    "<b>Certification culture.</b> Buyers in Gurugram are far more informed. They ask for IGI or "
                    "GIA certification, query clarity grades, and expect transparency in pricing. A diamond "
                    "mangalsutra purchased without documentation is no longer acceptable to the modern buyer "
                    "— nor should it be."
                )
            },
        },
        {
            "id": "blk008",
            "type": "header",
            "data": {"text": "Understanding the Key Design Families", "level": 2},
        },
        {
            "id": "blk009",
            "type": "header",
            "data": {"text": "1. Single-Line Solitaire Mangalsutra", "level": 3},
        },
        {
            "id": "blk010",
            "type": "paragraph",
            "data": {
                "text": (
                    "A single brilliant-cut or emerald-cut diamond suspended on a slender 18K gold or platinum chain. "
                    "Minimal. Supremely elegant. The choice of brides who believe that perfection requires no "
                    "reinforcement. A 0.50 ct – 1.00 ct IGI-certified diamond in VS clarity and G–H colour "
                    "at this format reads as both understated and unmistakable."
                )
            },
        },
        {
            "id": "blk011",
            "type": "header",
            "data": {"text": "2. Diamond Cluster Pendant on Black Bead Chain", "level": 3},
        },
        {
            "id": "blk012",
            "type": "paragraph",
            "data": {
                "text": (
                    "The traditional form reimagined — black beads retained as cultural anchoring, but the "
                    "centrepiece is a pavé or halo-set diamond cluster that catches light from every angle. "
                    "This style bridges heritage and modernity without compromise, making it the most versatile "
                    "option for brides navigating large joint families alongside a contemporary lifestyle."
                )
            },
        },
        {
            "id": "blk013",
            "type": "header",
            "data": {"text": "3. Dual-Chain Convertible Mangalsutra", "level": 3},
        },
        {
            "id": "blk014",
            "type": "paragraph",
            "data": {
                "text": (
                    "A design innovation that has gained significant traction in 2026. The mangalsutra comes with "
                    "two interchangeable chains — a traditional black-bead chain for ceremonial days, and a "
                    "delicate gold or diamond-cut chain for everyday wear. One pendant, two personalities. For "
                    "Gurgaon’s cosmopolitan brides, this convertibility is not a luxury — it is a necessity."
                )
            },
        },
        {
            "id": "blk015",
            "type": "header",
            "data": {"text": "4. Bracelet-Style Diamond Mangalsutra", "level": 3},
        },
        {
            "id": "blk016",
            "type": "paragraph",
            "data": {
                "text": (
                    "A newer category where the traditional mangalsutra concept is distilled into a diamond-set "
                    "bracelet, worn on the wrist. Favoured by brides in high-profile corporate roles, this format "
                    "maintains the sanctity of the tradition while accommodating wardrobes where necklaces may be "
                    "impractical. Each piece is custom-fitted and typically set in 18K gold with VVS-clarity diamonds."
                )
            },
        },
        {
            "id": "blk017",
            "type": "header",
            "data": {"text": "The Diamond Quality Framework: What to Ask For", "level": 2},
        },
        {
            "id": "blk018",
            "type": "paragraph",
            "data": {
                "text": "When shopping for a diamond mangalsutra in Gurgaon, these four parameters determine everything:"
            },
        },
        {
            "id": "blk019",
            "type": "paragraph",
            "data": {
                "text": (
                    "<b>Cut:</b> For a mangalsutra meant to be worn daily, an Excellent or Very Good cut grade is "
                    "non-negotiable. Cut determines how brilliantly the stone captures and returns light — it is "
                    "the one parameter that no consideration should override."
                )
            },
        },
        {
            "id": "blk020",
            "type": "paragraph",
            "data": {
                "text": (
                    "<b>Colour:</b> D–F is exceptional. G–H is the sweet spot for a piece that looks "
                    "spectacular without carrying the premium of the rarest grades. Avoid anything below I for a "
                    "diamond this prominent."
                )
            },
        },
        {
            "id": "blk021",
            "type": "paragraph",
            "data": {
                "text": (
                    "<b>Clarity:</b> VS1–VS2 clarity means inclusions are invisible to the naked eye. VVS is "
                    "superb but the premium is steep. SI1 can be acceptable only if a gemologist confirms the "
                    "inclusions are eye-clean — ask to see the stone, not just the certificate."
                )
            },
        },
        {
            "id": "blk022",
            "type": "paragraph",
            "data": {
                "text": (
                    "<b>Carat Weight:</b> A mangalsutra pendant between 0.50 ct and 1.50 ct commands attention "
                    "without overwhelming the design. For cluster or pavé settings, total carat weight above "
                    "0.75 ct delivers the density of sparkle that reads beautifully in daylight and under evening "
                    "lighting alike."
                )
            },
        },
        {
            "id": "blk023",
            "type": "paragraph",
            "data": {
                "text": (
                    "Always insist on an IGI or GIA certificate for every diamond above 0.30 ct. These two "
                    "laboratories are the global benchmark for independent diamond grading — no other "
                    "certification should be accepted for a piece of this significance."
                )
            },
        },
        {
            "id": "blk024",
            "type": "header",
            "data": {"text": "Chain Choices: The Underrated Decision", "level": 2},
        },
        {
            "id": "blk025",
            "type": "paragraph",
            "data": {
                "text": (
                    "The pendant earns attention. The chain earns longevity. Many brides spend considerable time "
                    "selecting their diamond, then treat the chain as an afterthought — a choice they later "
                    "regret. For a piece worn daily, the chain is structural as much as it is aesthetic."
                )
            },
        },
        {
            "id": "blk026",
            "type": "list",
            "data": {
                "style": "unordered",
                "items": [
                    "<b>18K gold cable or box chain</b> — elegant, durable, resists kinking with daily wear",
                    "<b>Black bead with 22K gold accents</b> — traditional, structurally sound, the classic choice that ages with grace",
                    "<b>Diamond-cut gold chain</b> — catches light independently, adds visual depth without adding weight",
                ],
            },
        },
        {
            "id": "blk027",
            "type": "paragraph",
            "data": {
                "text": (
                    "Ask your jeweller about clasp security — a lobster-claw clasp with a safety extender is "
                    "the standard for a daily-wear piece at this price point."
                )
            },
        },
        {
            "id": "blk028",
            "type": "header",
            "data": {
                "text": "Bespoke Diamond Mangalsutra in Gurgaon: What the Process Looks Like",
                "level": 2,
            },
        },
        {
            "id": "blk029",
            "type": "paragraph",
            "data": {
                "text": (
                    "At Auric Jewels, the bespoke mangalsutra process begins with a design consultation. The couple "
                    "— and yes, many grooms actively participate in this choice, which speaks to how central "
                    "this piece has become — walks through a curated selection of loose IGI/GIA-certified "
                    "diamonds. The stone is chosen first. The setting and chain follow."
                )
            },
        },
        {
            "id": "blk030",
            "type": "paragraph",
            "data": {
                "text": (
                    "The design cycle typically spans 3–4 weeks from stone selection to delivery. Every piece "
                    "leaves with a full certification dossier: diamond grading report, gold purity certificate, and "
                    "a personalised card documenting the stone’s specifications. Because a mangalsutra will "
                    "likely outlast the decade — and possibly the generation — its provenance should be "
                    "equally documented."
                )
            },
        },
        {
            "id": "blk031",
            "type": "header",
            "data": {"text": "Caring for Your Diamond Mangalsutra", "level": 2},
        },
        {
            "id": "blk032",
            "type": "list",
            "data": {
                "style": "unordered",
                "items": [
                    "Remove before swimming, bathing, or any activity involving chlorinated water or harsh chemicals",
                    "Store separately in a soft pouch to prevent surface abrasion on the gold chain",
                    "Professional cleaning once annually — ultrasonic cleaning and prong inspection — ensures the setting remains secure over time",
                ],
            },
        },
        {
            "id": "blk033",
            "type": "header",
            "data": {"text": "Selecting the Right Piece in Gurgaon: A Final Word", "level": 2},
        },
        {
            "id": "blk034",
            "type": "paragraph",
            "data": {
                "text": (
                    "The diamond mangalsutra is not a transaction. It is a commitment to something lasting — "
                    "a piece that will be adjusted, cleaned, re-worn, and eventually passed forward. Gurgaon offers "
                    "a range of options, from mass-market chain jewellers to premium independent showrooms. The "
                    "distinction lies in certification rigour, design craft, and the willingness to take time with "
                    "the buyer."
                )
            },
        },
        {
            "id": "blk035",
            "type": "paragraph",
            "data": {
                "text": (
                    "At Auric Jewels, we do not offer the fastest or the lowest-priced mangalsutra in Gurgaon. "
                    "We offer the one that will still make her reach for it every morning, twenty years from now."
                )
            },
        },
        {
            "id": "blk036",
            "type": "paragraph",
            "data": {
                "text": (
                    "Visit our Gurugram showroom to explore the 2026 bridal collection — or write to us to "
                    "schedule a private consultation before your wedding date."
                )
            },
        },
    ],
}


def gql(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"  HTTP {e.code}: {e.reason} — {body[:300]}")
        return None
    except urllib.error.URLError as e:
        print(f"  Connection error: {e.reason}")
        return None


CREATE_PAGE = """
mutation PageCreate($input: PageCreateInput!) {
  pageCreate(input: $input) {
    page {
      id
      title
      slug
      isPublished
    }
    errors {
      field
      code
      message
    }
  }
}
"""


def publish():
    print("Auric Jewels — Diamond Mangalsutra Blog Publisher")
    print("=" * 52)
    print(f"  Title : {BLOG['title']}")
    print(f"  Slug  : {BLOG['slug']}")
    print()

    variables = {
        "input": {
            "title": BLOG["title"],
            "slug": BLOG["slug"],
            "pageType": PAGE_TYPE_ID,
            "isPublished": True,
            "content": json.dumps(CONTENT_EDITORJS),
            "seo": {
                "title": BLOG["seoTitle"],
                "description": BLOG["seoDescription"],
            },
        }
    }

    print("  Calling pageCreate mutation...")
    result = gql(CREATE_PAGE, variables)

    if result is None:
        print("\nFailed to reach API. Check network / token.")
        return False

    if "errors" in result and result["errors"]:
        print("\nGraphQL top-level errors:")
        for e in result["errors"]:
            print(f"  - {e.get('message', e)}")
        return False

    page_result = result.get("data", {}).get("pageCreate", {})
    page_errors = page_result.get("errors", [])

    if page_errors:
        print("\nPageCreate errors:")
        for e in page_errors:
            print(f"  [{e.get('field','?')}] {e.get('code','?')}: {e.get('message','?')}")
        return False

    page = page_result.get("page")
    if page:
        print("\nSUCCESS — Blog published to Saleor CMS")
        print(f"  Saleor ID  : {page['id']}")
        print(f"  Slug       : {page['slug']}")
        print(f"  Published  : {page['isPublished']}")
        print(f"  Live URL   : https://www.auricjewels.com/blog/{page['slug']}")
        return True

    print("\nUnexpected response structure:")
    print(json.dumps(result, indent=2))
    return False


if __name__ == "__main__":
    ok = publish()
    sys.exit(0 if ok else 1)
