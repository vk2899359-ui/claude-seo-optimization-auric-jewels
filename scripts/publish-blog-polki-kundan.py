#!/usr/bin/env python3
"""
Auric Jewels — Publish Blog: Polki, Kundan & Diamond Bridal Sets in Gurugram
=============================================================================

Target keyword : polki kundan bridal set gurugram
Blog slug      : polki-kundan-bridal-set-gurugram
Published URL  : https://www.auricjewels.com/blog/polki-kundan-bridal-set-gurugram

API Endpoint   : https://auric.thecodemesh.online/graphql/
Channel        : franchise1
Page Type ID   : UGFnZVR5cGU6Ng==

USAGE (run from an IP in the Saleor ALLOWED_HOSTS allowlist):
    python3 scripts/publish-blog-polki-kundan.py
"""

import json
import urllib.request
import urllib.error

API_ENDPOINT = "https://auric.thecodemesh.online/graphql/"
AUTH_TOKEN = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

CONTENT = {
    "time": 1746057600000,
    "blocks": [
        {
            "id": "intro1",
            "type": "paragraph",
            "data": {
                "text": (
                    "Every bride deserves a trousseau that speaks before she enters the room. "
                    "In the world of Indian luxury bridal jewellery, three names define that entrance: "
                    "<b>Polki</b>, <b>Kundan</b>, and <b>Diamond</b>. Each is magnificent. Each is distinct. "
                    "And the difference between them — in craft, value, and visual language — is precisely "
                    "what a discerning bride in Gurugram needs to understand before she chooses."
                )
            },
        },
        {
            "id": "intro2",
            "type": "paragraph",
            "data": {
                "text": (
                    "At Auric Jewels, we have guided hundreds of families through this decision. "
                    "This guide is our atelier's definitive answer to the question we are asked most often: "
                    "<i>Which bridal set — Polki, Kundan, or Diamond — is right for me?</i>"
                )
            },
        },
        {
            "id": "h2-craft",
            "type": "header",
            "data": {"text": "Understanding the Three: A Brief on Craft and Heritage", "level": 2},
        },
        {
            "id": "h3-polki",
            "type": "header",
            "data": {"text": "Polki — The Glow of Uncut Natural Diamonds", "level": 3},
        },
        {
            "id": "p-polki1",
            "type": "paragraph",
            "data": {
                "text": (
                    "Polki jewellery traces its lineage to the Mughal imperial court. The technique involves "
                    "setting <b>natural, uncut diamonds</b> in their raw form — exactly as they emerge from the earth "
                    "— into hand-crafted gold settings. There is no faceting, no machine-cutting. The diamonds are "
                    "used in their most elemental state, held in gold through a process called <i>jadau</i> — one of "
                    "India's most labour-intensive jewellery arts."
                )
            },
        },
        {
            "id": "p-polki2",
            "type": "paragraph",
            "data": {
                "text": (
                    "The result is a jewellery form unlike any other. Polki does not sparkle in the modern sense. "
                    "It <i>glows</i>. The light settles into the uncut surfaces and radiates outward with a warmth "
                    "that faceted stones cannot replicate. It is the difference between a chandelier and candlelight "
                    "— both luminous, but one far more intimate and enduring."
                )
            },
        },
        {
            "id": "h3-kundan",
            "type": "header",
            "data": {"text": "Kundan — The Art of Refined Gold and Gemstone Inlay", "level": 3},
        },
        {
            "id": "p-kundan1",
            "type": "paragraph",
            "data": {
                "text": (
                    "Often confused with Polki, Kundan is a distinct tradition originating in Rajasthan. "
                    "Here, highly refined gold foil (the <i>kundan</i> itself) is used as a setting medium, "
                    "embedding gemstones — traditionally glass, lac, or semi-precious stones — into elaborate "
                    "compositions. The technique demands extraordinary precision: layers of gold foil are worked "
                    "around each stone by hand, creating settings that are themselves works of art."
                )
            },
        },
        {
            "id": "p-kundan2",
            "type": "paragraph",
            "data": {
                "text": (
                    "Kundan jewellery is characterised by its vivid colour palette. Emerald green, ruby red, "
                    "and sapphire blue stones set against 24-karat gold produce a regal, jewel-box quality that "
                    "is deeply rooted in Indian royal aesthetics. It is the jewellery of the maharanis — and it "
                    "remains the definitive statement of ceremonial grandeur."
                )
            },
        },
        {
            "id": "h3-diamond",
            "type": "header",
            "data": {"text": "Diamond Bridal Sets — Timeless Brilliance, Modern Elegance", "level": 3},
        },
        {
            "id": "p-diamond1",
            "type": "paragraph",
            "data": {
                "text": (
                    "Natural diamond bridal jewellery, set in 18-karat or 22-karat gold, represents the "
                    "contemporary luxury bride's choice. IGI or GIA-certified diamonds, precisely cut to maximise "
                    "brilliance, are mounted in designs that range from classic solitaire-led bridal necklaces to "
                    "intricate pavé-set floral clusters. The result is jewellery that works as powerfully under the "
                    "lights of a wedding hall as it does at an anniversary dinner twenty years later."
                )
            },
        },
        {
            "id": "p-diamond2",
            "type": "paragraph",
            "data": {
                "text": "Diamond sets are the most versatile of the three — wearable across occasions, resizable, and appreciating in value over time."
            },
        },
        {
            "id": "h2-choose",
            "type": "header",
            "data": {"text": "Which Bridal Set Should You Choose? Auric Jewels' Atelier Perspective", "level": 2},
        },
        {
            "id": "h3-choose-polki",
            "type": "header",
            "data": {"text": "Choose Polki if you are a bride who values heritage over trend", "level": 3},
        },
        {
            "id": "p-choose-polki",
            "type": "paragraph",
            "data": {
                "text": (
                    "If your wedding is rooted in tradition — a lehenga in rich silk, a mandap adorned with marigolds, "
                    "a ceremony where the weight of heritage is palpable — Polki is your answer. The uncut diamond set "
                    "against jadau gold speaks of a lineage that machine-made jewellery simply cannot replicate. Polki "
                    "is not a fashion statement. It is a declaration of provenance. In Gurugram's luxury wedding circuit, "
                    "Polki is having its most significant resurgence in years. Brides who understand the difference between "
                    "craft and commerce are choosing Polki sets as their primary bridal trousseau — and then building a "
                    "separate diamond set for the reception."
                )
            },
        },
        {
            "id": "h3-choose-kundan",
            "type": "header",
            "data": {"text": "Choose Kundan if you want a canvas of colour alongside gold's warmth", "level": 3},
        },
        {
            "id": "p-choose-kundan",
            "type": "paragraph",
            "data": {
                "text": (
                    "For brides whose wedding aesthetic embraces rich, jewel-toned colour — deep maroon bridal wear, "
                    "emerald-edged dupattas, or a colour-story that celebrates Indian chromatic opulence — Kundan is "
                    "the supreme choice. A well-crafted Kundan necklace with emerald and ruby inlays against 24-karat "
                    "gold turns a bride into an artwork. Kundan is also the ideal choice for brides whose mehendi or "
                    "sangeet function calls for a distinct look — the ability to swap colour palettes while maintaining "
                    "the gold base adds remarkable versatility."
                )
            },
        },
        {
            "id": "h3-choose-diamond",
            "type": "header",
            "data": {"text": "Choose Diamonds if you are building a collection that lives beyond the wedding day", "level": 3},
        },
        {
            "id": "p-choose-diamond",
            "type": "paragraph",
            "data": {
                "text": (
                    "Diamond bridal jewellery — IGI or GIA certified, set in BIS hallmarked gold — is the investment "
                    "a luxury bride makes in her future wardrobe. A well-designed diamond necklace worn at the wedding "
                    "becomes the dinner jewellery for the years ahead. The solitaire earrings from the engagement become "
                    "the everyday fine jewellery that travels with her career. Diamond is not just a bridal choice; it "
                    "is a lifetime one. At Auric Jewels, our diamond bridal sets are designed with this dual life in mind: "
                    "magnificent enough for the wedding mandap, refined enough for the executive boardroom fifteen years later."
                )
            },
        },
        {
            "id": "h2-layering",
            "type": "header",
            "data": {"text": "Can You Wear All Three? The Art of Bridal Layering in Gurugram", "level": 2},
        },
        {
            "id": "p-layering",
            "type": "paragraph",
            "data": {
                "text": (
                    "The most sophisticated approach — and the one our Gurugram clientele is increasingly embracing — "
                    "is a curated <b>trousseau across all three traditions</b>. A Polki haara for the wedding ceremony. "
                    "Kundan jhumkas for the mehendi. A diamond solitaire pendant and earring set for the reception. "
                    "Each occasion receives jewellery appropriate to its spirit, and the bride herself is never visually "
                    "monotonous across a multi-day celebration. This is not excess. This is curation — the mark of a "
                    "bride who understands jewellery as a language, not a transaction."
                )
            },
        },
        {
            "id": "h2-consultation",
            "type": "header",
            "data": {
                "text": "The Auric Jewels Bridal Consultation: Gurugram's Most Personalised Jewellery Experience",
                "level": 2,
            },
        },
        {
            "id": "p-consultation",
            "type": "paragraph",
            "data": {
                "text": (
                    "Choosing a bridal set is among the most significant decisions a family makes. At Auric Jewels, "
                    "we honour that significance with a private bridal consultation at our Sector 45, Gurugram atelier. "
                    "Our consultants work with one bridal party at a time, over an unhurried appointment, to understand "
                    "the wedding aesthetic, the family's heritage, the bride's personal style, and the occasions the "
                    "jewellery will serve."
                )
            },
        },
        {
            "id": "list-promise",
            "type": "list",
            "data": {
                "style": "unordered",
                "items": [
                    "BIS hallmark with a traceable HUID number on every gold component",
                    "IGI or GIA certification for all diamonds above 0.30 carats",
                    "Lifetime exchange at full prevailing gold value — no deductions, no conditions",
                    "Complimentary jewellery care consultation with every bridal purchase",
                ],
            },
        },
        {
            "id": "h2-standard",
            "type": "header",
            "data": {"text": "The Auric Standard: Why Gurugram's Families Return", "level": 2},
        },
        {
            "id": "p-standard",
            "type": "paragraph",
            "data": {
                "text": (
                    "In a city where international luxury brands share a postcode with local jewellers, Auric Jewels "
                    "occupies a singular position: the precision and transparency of a fine jeweller, and the intimacy "
                    "and craft sensibility of a family atelier. Our Polki sets are sourced from master jadau artisans. "
                    "Our Kundan pieces carry the lineage of Rajasthani craftsmen. And our diamond bridal collections "
                    "are designed in-house, with every stone chosen by our gemologists."
                )
            },
        },
        {
            "id": "p-cta",
            "type": "paragraph",
            "data": {
                "text": (
                    "<b>Book your private bridal consultation at Auric Jewels — Greenwood Plaza, Shop No. 201, "
                    "Sector 45, Gurugram, Haryana 122003.</b> Visit auricjewels.com or call 0124-437-2846 to "
                    "schedule your appointment. Open Monday–Saturday 10:30 AM – 8:00 PM | Sunday 11:00 AM – 6:00 PM"
                )
            },
        },
    ],
    "version": "2.26.5",
}

MUTATION = """
mutation PageCreate($input: PageCreateInput!) {
  pageCreate(input: $input) {
    page {
      id
      title
      slug
      isPublished
      publishedAt
    }
    errors {
      field
      code
      message
    }
  }
}
"""

VARIABLES = {
    "input": {
        "title": "Polki, Kundan & Diamond Bridal Sets in Gurugram — The Luxury Bride's Complete Guide",
        "slug": "polki-kundan-bridal-set-gurugram",
        "pageType": PAGE_TYPE_ID,
        "isPublished": True,
        "seo": {
            "title": "Polki, Kundan & Diamond Bridal Sets Gurugram | Auric Jewels",
            "description": (
                "Choosing between Polki, Kundan, and Diamond for your bridal set? "
                "Auric Jewels, Gurugram's finest atelier, breaks down the craft, value, "
                "and eternal beauty of each — so your trousseau tells the right story."
            ),
        },
        "content": json.dumps(CONTENT),
    }
}


def run():
    payload = json.dumps({"query": MUTATION, "variables": VARIABLES}).encode("utf-8")
    req = urllib.request.Request(
        API_ENDPOINT,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AUTH_TOKEN}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"HTTP {e.code}: {body[:500]}")
        return

    errors = result.get("data", {}).get("pageCreate", {}).get("errors", [])
    page = result.get("data", {}).get("pageCreate", {}).get("page")

    if errors:
        print("GraphQL errors:")
        for err in errors:
            print(f"  [{err.get('field')}] {err.get('code')}: {err.get('message')}")
    elif page:
        print(f"Published successfully!")
        print(f"  ID   : {page['id']}")
        print(f"  Title: {page['title']}")
        print(f"  Slug : {page['slug']}")
        print(f"  URL  : https://www.auricjewels.com/blog/{page['slug']}")
    else:
        print("Unexpected response:", json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
