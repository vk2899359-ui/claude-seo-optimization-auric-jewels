"""
Auric Jewels — Polki Bridal Jewellery Blog Publisher
=====================================================
Date: 2026-05-09
Target keyword: polki bridal jewellery Gurgaon

USAGE:
    python3 scripts/publish-polki-blog-2026-05-09.py

Publishes via Saleor pageCreate mutation to:
  Endpoint : https://auric.thecodemesh.online/graphql/
  Channel  : franchise1
  PageType : UGFnZVR5cGU6Ng==
"""

import json
import sys
import urllib.request
import urllib.error

API_ENDPOINT = "https://auric.thecodemesh.online/graphql/"
AUTH_TOKEN   = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
CHANNEL      = "franchise1"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

BLOG_TITLE = (
    "Royal Polki Bridal Jewellery in Gurgaon: "
    "The Connoisseur’s Guide to Uncut Diamond Magnificence"
)
BLOG_SLUG  = "polki-bridal-jewellery-gurgaon"
BLOG_SEO_DESCRIPTION = (
    "Discover Auric Jewels’ exquisite Polki bridal jewellery collection in Gurgaon. "
    "Hand-crafted Kundan-set uncut diamond pieces for the discerning bride — "
    "heritage craftsmanship, modern sensibility. Book a private consultation."
)

# Rich-text content (Saleor / Editor.js JSON format)
BLOG_CONTENT = {
    "time": 1746748800000,
    "blocks": [
        {
            "id": "p1",
            "type": "paragraph",
            "data": {
                "text": (
                    "There is a particular moment — the one just before a bride walks into the light "
                    "of her wedding mandap — when jewellery stops being ornament and becomes identity. "
                    "In that moment, nothing commands the air quite like Polki. Ancient, luminous, "
                    "irreducibly royal: uncut diamonds set in 22-karat gold have adorned the courts of "
                    "Mughal empresses and Rajputana queens for centuries. Today, discerning brides in "
                    "Gurgaon are rediscovering what those queens always knew."
                )
            },
        },
        {
            "id": "p2",
            "type": "paragraph",
            "data": {
                "text": (
                    "At Auric Jewels, Gurgaon’s sanctuary for heritage luxury, the Polki bridal "
                    "collection is crafted for women who understand that true magnificence requires no "
                    "embellishment beyond nature itself."
                )
            },
        },
        {
            "id": "h1",
            "type": "header",
            "data": {
                "text": "What Makes Polki Jewellery the Pinnacle of Bridal Luxury?",
                "level": 2,
            },
        },
        {
            "id": "p3",
            "type": "paragraph",
            "data": {
                "text": (
                    "Polki diamonds are uncut, unpolished natural diamonds — preserved in their most "
                    "elemental form, set flat to capture light in a diffuse, almost otherworldly glow. "
                    "Unlike their faceted counterparts, Polki stones do not refract light in sharp "
                    "flashes; instead, they absorb it, releasing a soft inner luminescence that "
                    "photographs as warmth rather than glitter."
                )
            },
        },
        {
            "id": "p4",
            "type": "paragraph",
            "data": {
                "text": (
                    "This quality makes Polki uniquely magnificent under the rich, layered lighting of "
                    "Indian weddings — mehendi candlelight, phera firelight, reception chandeliers. "
                    "A Polki set does not compete with the occasion. It completes it."
                )
            },
        },
        {
            "id": "p5",
            "type": "paragraph",
            "data": {
                "text": (
                    "Polki craftsmanship — known as Kundan setting — is one of India’s most "
                    "labour-intensive jewellery traditions. Master karigars in Rajasthan spend weeks "
                    "embedding each stone in a bed of 24-karat gold foil, layer by layer, before "
                    "finishing the reverse with intricate meenakari enamelwork. At Auric Jewels, every "
                    "Polki piece bears the signature of this unbroken tradition."
                )
            },
        },
        {
            "id": "h2",
            "type": "header",
            "data": {
                "text": "2026 Polki Bridal Jewellery Trends in Gurgaon",
                "level": 2,
            },
        },
        {
            "id": "p6",
            "type": "paragraph",
            "data": {
                "text": (
                    "This year’s bridal season in Gurgaon and the wider NCR is witnessing a decisive "
                    "return to heritage grandeur — but interpreted through a contemporary lens. "
                    "Here is what the most deliberate brides are choosing:"
                )
            },
        },
        {
            "id": "h3",
            "type": "header",
            "data": {"text": "Layered Polki Rani Haars", "level": 3},
        },
        {
            "id": "p7",
            "type": "paragraph",
            "data": {
                "text": (
                    "The multi-strand Rani Haar — falling dramatically from collarbone to sternum — "
                    "is the statement of 2026. Auric’s signature interpretation uses graduated Polki "
                    "stones, with the finest specimens at the centre, framed by rubies or emeralds for a "
                    "palette that reads as both regal and deeply personal."
                )
            },
        },
        {
            "id": "h4",
            "type": "header",
            "data": {
                "text": "Polki Mathapatti with Architectural Precision",
                "level": 3,
            },
        },
        {
            "id": "p8",
            "type": "paragraph",
            "data": {
                "text": (
                    "Headpieces have evolved from simple maang tikkas into architectural crown structures. "
                    "The modern Polki mathapatti at Auric Jewels is engineered to drape without weight — "
                    "a critical consideration for brides wearing the piece through a six-hour ceremony."
                )
            },
        },
        {
            "id": "h5",
            "type": "header",
            "data": {
                "text": "Chandbali Earrings: The Essential Counterpoint",
                "level": 3,
            },
        },
        {
            "id": "p9",
            "type": "paragraph",
            "data": {
                "text": (
                    "The crescent-form Chandbali, set with Polki and finished with natural pearl drops, "
                    "provides the perfect counterpoint to heavily layered neckwear. Brides pairing a "
                    "Polki rani haar with oversized Chandbalis achieve maximum visual impact without "
                    "redundancy."
                )
            },
        },
        {
            "id": "h6",
            "type": "header",
            "data": {
                "text": "Polki Bangles and Kadas for the Modern Trousseau",
                "level": 3,
            },
        },
        {
            "id": "p10",
            "type": "paragraph",
            "data": {
                "text": (
                    "Where previous generations invested in complete matching sets, today’s Gurgaon "
                    "bride builds a trousseau — individual Polki pieces of exceptional quality that "
                    "can be worn and reworn across events, styled differently each time. An Auric Polki "
                    "kada, for instance, moves elegantly from the wedding to the reception to a formal "
                    "dinner, years hence."
                )
            },
        },
        {
            "id": "h7",
            "type": "header",
            "data": {
                "text": "Why Gurgaon’s Most Discerning Brides Choose Auric Jewels",
                "level": 2,
            },
        },
        {
            "id": "p11",
            "type": "paragraph",
            "data": {
                "text": (
                    "Gurgaon’s luxury jewellery market has grown considerably, but not all Polki is "
                    "equal. The quality of Polki work is determined entirely by the calibre of the "
                    "karigar and the purity of the gold used. At Auric Jewels, we work exclusively with "
                    "master craftsmen whose families have practised Kundan setting for three generations, "
                    "using only hallmarked 22-karat gold."
                )
            },
        },
        {
            "id": "p12",
            "type": "paragraph",
            "data": {
                "text": (
                    "Every Polki piece at Auric comes with full karigar certification tracing the piece "
                    "to its maker, IGI-assessed diamond weight documentation for the uncut stones, "
                    "meenakari inspection under magnification before any piece leaves the atelier, and "
                    "lifetime restoration service — because heirloom pieces deserve heirloom care."
                )
            },
        },
        {
            "id": "h8",
            "type": "header",
            "data": {
                "text": "Planning Your Polki Bridal Consultation in Gurgaon",
                "level": 2,
            },
        },
        {
            "id": "p13",
            "type": "paragraph",
            "data": {
                "text": (
                    "A Polki bridal set is not a purchase made in an afternoon. It is a conversation — "
                    "about your wedding aesthetic, the weight you prefer to wear, the events across which "
                    "you’ll be seen, and the legacy you wish to begin. Auric Jewels offers private "
                    "bridal consultations at our Gurgaon showroom, where our jewellery specialists will "
                    "guide you through the full Polki collection, assist with customisation, and advise "
                    "on the ideal combination of pieces for each wedding function."
                )
            },
        },
        {
            "id": "p14",
            "type": "paragraph",
            "data": {
                "text": (
                    "Bespoke Polki commissions are accepted with a minimum of 12 weeks’ lead time, "
                    "allowing karigar teams to create a set designed exclusively around your requirements "
                    "— stone size, gold weight, colour accent, length and form."
                )
            },
        },
        {
            "id": "h9",
            "type": "header",
            "data": {"text": "The Investment Dimension", "level": 2},
        },
        {
            "id": "p15",
            "type": "paragraph",
            "data": {
                "text": (
                    "Beyond their aesthetic authority, Polki jewellery sets hold intrinsic value that "
                    "modern jewellery rarely matches. As gold prices in India continue their ascent in "
                    "2026, Polki pieces — with their high gold content and natural diamond weight — "
                    "represent a compelling store of wealth dressed in extraordinary beauty."
                )
            },
        },
        {
            "id": "p16",
            "type": "paragraph",
            "data": {
                "text": (
                    "Brides who invest in Polki bridal jewellery from Auric Jewels are not merely "
                    "equipping themselves for a wedding. They are beginning a family jewellery tradition "
                    "that will be passed down, admired, and worn again — perhaps at their daughter’s "
                    "wedding, perhaps at their granddaughter’s. That is the nature of the finest "
                    "things. They endure."
                )
            },
        },
    ],
    "version": "2.24.3",
}


def graphql_request(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_ENDPOINT,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AUTH_TOKEN}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        print(f"  HTTP {e.code}: {e.reason}")
        if body:
            print(f"  Body: {body[:400]}")
        return None
    except urllib.error.URLError as e:
        print(f"  Connection error: {e.reason}")
        return None


def main():
    print()
    print("  Auric Jewels — SEO Blog Publisher")
    print("  2026-05-09 | Polki Bridal Jewellery Gurgaon")
    print()

    mutation = """
    mutation PageCreate($input: PageCreateInput!) {
      pageCreate(input: $input) {
        page {
          id
          title
          slug
          isPublished
          seoTitle
          seoDescription
        }
        errors {
          field
          message
          code
        }
      }
    }
    """

    variables = {
        "input": {
            "title":          BLOG_TITLE,
            "slug":           BLOG_SLUG,
            "pageType":       PAGE_TYPE_ID,
            "content":        json.dumps(BLOG_CONTENT),
            "isPublished":    True,
            "seoTitle":       (
                "Polki Bridal Jewellery in Gurgaon | Royal Uncut Diamond Sets — Auric Jewels"
            ),
            "seoDescription": BLOG_SEO_DESCRIPTION,
        }
    }

    print(f"  Title : {BLOG_TITLE}")
    print(f"  Slug  : {BLOG_SLUG}")
    print(f"  PageType: {PAGE_TYPE_ID}")
    print()
    print("  Sending pageCreate mutation...")
    print()

    result = graphql_request(mutation, variables)

    if result is None:
        print("  No response from API. Check network / token.")
        sys.exit(1)

    if "errors" in result:
        print("  GraphQL top-level errors:")
        for err in result["errors"]:
            print(f"    - {err.get('message', err)}")
        sys.exit(1)

    page_data = result.get("data", {}).get("pageCreate", {})
    page_errors = page_data.get("errors", [])

    if page_errors:
        print("  pageCreate errors:")
        for err in page_errors:
            print(f"    [{err.get('field', '?')}] {err.get('message', '')} (code: {err.get('code', '')})")
        sys.exit(1)

    page = page_data.get("page")
    if page:
        print("  SUCCESS — blog page published!")
        print(f"  ID          : {page.get('id')}")
        print(f"  Slug        : {page.get('slug')}")
        print(f"  isPublished : {page.get('isPublished')}")
        print(f"  Live URL    : https://auricjewels.com/{page.get('slug', BLOG_SLUG)}")
    else:
        print("  Published but no page object returned.")
        print(f"  Raw: {json.dumps(result, indent=2)[:500]}")

    sys.exit(0)


if __name__ == "__main__":
    main()
