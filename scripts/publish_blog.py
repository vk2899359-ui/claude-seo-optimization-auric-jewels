#!/usr/bin/env python3
"""Publish SEO blog post to Auric Jewels Saleor CMS."""

import json
import urllib.request
import urllib.error
import sys

ENDPOINT = "https://auric.thecodemesh.online/graphql/"
TOKEN = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="
CHANNEL = "franchise1"

BLOG_TITLE = "Solitaire Diamond Rings for Brides in Gurgaon: The 2026 Guide to Timeless Elegance"
BLOG_SLUG = "solitaire-diamond-rings-brides-gurgaon-2026-guide"

CONTENT = {
    "time": 1747094400000,
    "blocks": [
        {
            "id": "intro1",
            "type": "paragraph",
            "data": {
                "text": "There is a moment in every bride's journey — quiet, crystalline, and certain — when she knows exactly what she wants. Not something ornate or overwrought. Not something that speaks in the language of excess. She wants one perfect stone. Set with precision. Worn with intention. A solitaire diamond ring."
            }
        },
        {
            "id": "intro2",
            "type": "paragraph",
            "data": {
                "text": "In 2026, Gurgaon's most discerning brides are making this choice with greater conviction than ever before. As gold reaches historic highs this May, the solitaire diamond ring has emerged not merely as a symbol of love — but as the definitive statement of modern bridal sophistication. At Auric Jewels, Gurugram's destination for heirloom-quality diamond jewellery, we have witnessed this shift firsthand. This is our guide for the bride who knows that true luxury speaks in whispers, not roars."
            }
        },
        {
            "id": "h2-reign",
            "type": "header",
            "data": {
                "text": "Why the Solitaire Reigns Supreme for the Modern Bride",
                "level": 2
            }
        },
        {
            "id": "reign1",
            "type": "paragraph",
            "data": {
                "text": "The single-stone diamond ring is, at its core, a study in confidence. There is nowhere to hide — and no reason to. The solitaire places the diamond at the absolute centre of attention, demanding nothing but the finest stone, the most precise setting, and the most considered craftsmanship."
            }
        },
        {
            "id": "reign2",
            "type": "paragraph",
            "data": {
                "text": "In the pantheon of bridal jewellery, the solitaire diamond ring has transcended trend. It was worn by the women who defined elegance in every decade before ours, and it will be worn by the women who define it in every decade after. For the 2026 bride in Gurgaon — a woman who navigates boardrooms as gracefully as she navigates weddings — it is the logical, luminous choice."
            }
        },
        {
            "id": "reign3",
            "type": "paragraph",
            "data": {
                "text": "Wedding season 2026 arrives with a distinct aesthetic sensibility: refined minimalism paired with maximum intention. The bride is not sacrificing grandeur; she is redefining it. A 1.5-carat round brilliant solitaire in a six-prong platinum setting makes a statement no elaborate necklace can match."
            }
        },
        {
            "id": "h2-fourccs",
            "type": "header",
            "data": {
                "text": "Understanding the Four Cs — The Language of Diamond Excellence",
                "level": 2
            }
        },
        {
            "id": "4cs-intro",
            "type": "paragraph",
            "data": {
                "text": "Choosing a solitaire diamond ring is, above all, an education in diamond quality. At Auric Jewels, we guide every bride through the four pillars of diamond excellence:"
            }
        },
        {
            "id": "cut-h",
            "type": "header",
            "data": {
                "text": "Cut: The Soul of the Stone",
                "level": 3
            }
        },
        {
            "id": "cut-p",
            "type": "paragraph",
            "data": {
                "text": "The cut of a diamond is the single most important factor in its brilliance. A perfectly cut round brilliant diamond reflects light from facet to facet with an almost supernatural luminosity. At Auric Jewels, we recommend nothing below Very Good cut — and for our most discerning clients, Excellent cut is the only acceptable standard. The way a perfectly cut stone catches the morning light as you lift your chai cup — that is worth every consideration."
            }
        },
        {
            "id": "colour-h",
            "type": "header",
            "data": {
                "text": "Colour: The Subtle Gradient of Purity",
                "level": 3
            }
        },
        {
            "id": "colour-p",
            "type": "paragraph",
            "data": {
                "text": "Diamond colour is graded on a scale from D (completely colourless) to Z (warm yellow tones). For a white metal setting — platinum or white gold — we recommend D to H range, where the stone reads as pure white to the naked eye. For a yellow gold setting, H to J can be extraordinary, as the warm metal complements any subtle warmth in the stone."
            }
        },
        {
            "id": "clarity-h",
            "type": "header",
            "data": {
                "text": "Clarity: The Inner Universe",
                "level": 3
            }
        },
        {
            "id": "clarity-p",
            "type": "paragraph",
            "data": {
                "text": "Most diamonds carry inclusions — nature's fingerprints, formed under unimaginable pressure. The question for the bride is not whether they exist, but whether they are visible. Stones graded VS1 and above are considered eye-clean: no inclusion visible to the naked eye, only under 10x magnification. This is the benchmark Auric Jewels sets for our bridal collections."
            }
        },
        {
            "id": "carat-h",
            "type": "header",
            "data": {
                "text": "Carat: The Weight of Beauty",
                "level": 3
            }
        },
        {
            "id": "carat-p",
            "type": "paragraph",
            "data": {
                "text": "Carat is a measure of weight, not size — though the two are related. A well-cut 1-carat round brilliant diamond measures approximately 6.5mm in diameter. At Auric Jewels, our bridal solitaire collection begins at 0.50 carats and extends to 3.00+ carats for bespoke commissions. Our guidance: choose the carat weight that looks extraordinary on your specific hand, not the number that sounds impressive in conversation."
            }
        },
        {
            "id": "h2-settings",
            "type": "header",
            "data": {
                "text": "Solitaire Settings That Define Modern Bridal Luxury",
                "level": 2
            }
        },
        {
            "id": "settings-intro",
            "type": "paragraph",
            "data": {
                "text": "The setting is the architecture of the solitaire — and the choices are more nuanced than most brides realise."
            }
        },
        {
            "id": "prong-h",
            "type": "header",
            "data": {
                "text": "The Classic Prong Setting",
                "level": 3
            }
        },
        {
            "id": "prong-p",
            "type": "paragraph",
            "data": {
                "text": "Six prongs cradle the diamond, lifting it high above the band and allowing maximum light entry from all angles. This is the most iconic solitaire setting, and for good reason: nothing showcases a diamond's brilliance more generously. At Auric Jewels, our six-prong settings are crafted in platinum 950 for brides who want a metal that holds its colour and hardness through decades of wear."
            }
        },
        {
            "id": "bezel-h",
            "type": "header",
            "data": {
                "text": "The Bezel Setting",
                "level": 3
            }
        },
        {
            "id": "bezel-p",
            "type": "paragraph",
            "data": {
                "text": "A full bezel encircles the diamond with a rim of metal, creating a sleek, contemporary silhouette. This setting offers superior protection for the stone and a modern aesthetic that reads beautifully against both traditional bridal wear and contemporary fashion. A bezel-set solitaire in yellow gold is among the most sought-after combinations in our 2026 collection."
            }
        },
        {
            "id": "cathedral-h",
            "type": "header",
            "data": {
                "text": "The Cathedral Setting",
                "level": 3
            }
        },
        {
            "id": "cathedral-p",
            "type": "paragraph",
            "data": {
                "text": "The band arches gracefully upward on each side to meet the stone, creating a profile that is architectural and unmistakably grand. The cathedral setting adds height and drama to the solitaire without competing with the stone itself — a favourite among brides who wear traditional bridal lehenga and saree ensembles."
            }
        },
        {
            "id": "tension-h",
            "type": "header",
            "data": {
                "text": "The Tension Setting",
                "level": 3
            }
        },
        {
            "id": "tension-p",
            "type": "paragraph",
            "data": {
                "text": "For the bride who lives at the intersection of art and engineering, the tension setting holds the diamond suspended between two ends of the band, secured by the precise pressure of the metal. It is daring, modern, and exquisitely beautiful — a conversation piece worn on the most important finger."
            }
        },
        {
            "id": "h2-auric",
            "type": "header",
            "data": {
                "text": "Gurgaon's Discerning Brides Choose Auric Jewels",
                "level": 2
            }
        },
        {
            "id": "auric-intro",
            "type": "paragraph",
            "data": {
                "text": "Auric Jewels is Gurugram's destination for certified diamond jewellery crafted to heirloom standards. Each solitaire ring in our collection is accompanied by a GIA or IGI certification, providing complete transparency on the stone's cut, colour, clarity, and carat weight."
            }
        },
        {
            "id": "auric-list",
            "type": "list",
            "data": {
                "style": "unordered",
                "items": [
                    "Bespoke design consultations for brides seeking a ring as individual as their love story",
                    "Certified diamonds across the full range of shapes — round brilliant, oval, cushion, emerald, pear, marquise, and princess",
                    "Custom band metalwork in platinum 950, 18K white gold, 18K yellow gold, and 18K rose gold",
                    "Complete bridal suites — matching earrings, pendants, and mangalsutra to complement the solitaire",
                    "Private appointments at our Gurugram showroom, serving brides across Delhi NCR"
                ]
            }
        },
        {
            "id": "h2-beyond",
            "type": "header",
            "data": {
                "text": "Beyond the Ring: Completing Your Bridal Diamond Story",
                "level": 2
            }
        },
        {
            "id": "beyond-intro",
            "type": "paragraph",
            "data": {
                "text": "A solitaire ring is the centrepiece, but the finest bridal jewellery tells a coherent story across every piece. The 2026 bride in Gurgaon understands this instinctively."
            }
        },
        {
            "id": "studs-h",
            "type": "header",
            "data": {
                "text": "Diamond Studs",
                "level": 3
            }
        },
        {
            "id": "studs-p",
            "type": "paragraph",
            "data": {
                "text": "A pair of brilliant-cut diamond studs in a matching setting metal complements the solitaire without competing with it. Half-carat to one-carat studs are the most elegant choice for the ceremony — present in every photograph, absent in every distraction."
            }
        },
        {
            "id": "mangalsutra-h",
            "type": "header",
            "data": {
                "text": "The Diamond Mangalsutra",
                "level": 3
            }
        },
        {
            "id": "mangalsutra-p",
            "type": "paragraph",
            "data": {
                "text": "Reimagined for the modern bride, the diamond mangalsutra at Auric Jewels pairs a traditional symbol with contemporary craftsmanship — a piece that transitions seamlessly from wedding morning to work meeting to anniversary dinner, worn as naturally as the solitaire it mirrors."
            }
        },
        {
            "id": "bangle-h",
            "type": "header",
            "data": {
                "text": "The Diamond Bangle",
                "level": 3
            }
        },
        {
            "id": "bangle-p",
            "type": "paragraph",
            "data": {
                "text": "A single, slender diamond bangle worn alongside the solitaire creates a composed, intentional look that has become the signature of Gurgaon's most style-conscious brides in 2026. Restraint, here, is the highest form of opulence."
            }
        },
        {
            "id": "h2-investment",
            "type": "header",
            "data": {
                "text": "A Solitaire Diamond Ring: An Investment in Timeless Beauty",
                "level": 2
            }
        },
        {
            "id": "invest1",
            "type": "paragraph",
            "data": {
                "text": "At a time when gold trades above ₹1.5 lakh per 10 grams, the solitaire diamond ring stands as a particularly compelling choice for the 2026 bride. Diamonds retain their intrinsic beauty indefinitely — a well-crafted solitaire will look identical in forty years as it does today. It is a piece your daughter will wear, and her daughter after her."
            }
        },
        {
            "id": "invest2",
            "type": "paragraph",
            "data": {
                "text": "This is the promise that Auric Jewels makes to every bride who walks through our doors in Gurugram: that the solitaire diamond ring you choose today will remain extraordinary for a lifetime — and well beyond it."
            }
        },
        {
            "id": "cta",
            "type": "paragraph",
            "data": {
                "text": "Discover Auric Jewels' bridal solitaire diamond ring collection. Schedule a private consultation at our Gurugram showroom and begin the most luminous chapter of your story."
            }
        }
    ],
    "version": "2.26.5"
}


def graphql_request(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return {"error": str(e), "body": body}
    except Exception as e:
        return {"error": str(e)}


CREATE_PAGE_MUTATION = """
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

PAGE_CHANNEL_UPDATE_MUTATION = """
mutation PageChannelListingUpdate($id: ID!, $input: PageChannelListingUpdateInput!) {
  pageChannelListingUpdate(id: $id, input: $input) {
    page {
      id
      title
    }
    errors {
      field
      code
      message
    }
  }
}
"""


def main():
    print("=== Auric Jewels SEO Blog Publisher ===")
    print(f"Title: {BLOG_TITLE}")
    print(f"Slug:  {BLOG_SLUG}")
    print()

    # Step 1: Create the page
    print("Step 1: Creating page...")
    create_vars = {
        "input": {
            "title": BLOG_TITLE,
            "slug": BLOG_SLUG,
            "pageType": PAGE_TYPE_ID,
            "content": json.dumps(CONTENT),
            "isPublished": True,
            "seo": {
                "title": "Solitaire Diamond Ring Gurgaon | Bridal Diamond Rings | Auric Jewels",
                "description": (
                    "Discover why Gurgaon's most discerning brides choose solitaire diamond rings in 2026. "
                    "Certified diamonds, bespoke settings, heirloom craftsmanship at Auric Jewels, Gurugram."
                ),
            },
        }
    }

    result = graphql_request(CREATE_PAGE_MUTATION, create_vars)
    print("API Response:", json.dumps(result, indent=2))

    if "error" in result:
        print(f"\nERROR: {result['error']}")
        sys.exit(1)

    page_data = result.get("data", {}).get("pageCreate", {})
    errors = page_data.get("errors", [])
    if errors:
        print(f"\nGraphQL Errors: {errors}")
        sys.exit(1)

    page = page_data.get("page")
    if not page:
        print("\nERROR: No page returned")
        sys.exit(1)

    page_id = page["id"]
    print(f"\nPage created successfully!")
    print(f"  ID:    {page_id}")
    print(f"  Title: {page['title']}")
    print(f"  Slug:  {page['slug']}")

    # Step 2: Publish to channel
    print(f"\nStep 2: Publishing to channel '{CHANNEL}'...")
    channel_vars = {
        "id": page_id,
        "input": {
            "addChannels": [
                {
                    "channelId": CHANNEL,
                    "isPublished": True,
                }
            ]
        },
    }

    channel_result = graphql_request(PAGE_CHANNEL_UPDATE_MUTATION, channel_vars)
    print("Channel API Response:", json.dumps(channel_result, indent=2))

    channel_errors = (
        channel_result.get("data", {})
        .get("pageChannelListingUpdate", {})
        .get("errors", [])
    )
    if channel_errors:
        print(f"\nChannel listing errors: {channel_errors}")

    print("\n=== Blog post published successfully! ===")
    print(f"Page ID: {page_id}")
    return page_id


if __name__ == "__main__":
    main()
