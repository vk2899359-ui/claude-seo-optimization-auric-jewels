import json
import urllib.request
import urllib.error

ENDPOINT = "https://auric.thecodemesh.online/graphql/"
TOKEN = "EXjfazrP5PWBz5LE0TyckHNvQ5M7Q1"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="
CHANNEL = "franchise1"

content_json = {
    "time": 1745539200000,
    "blocks": [
        {
            "id": "intro01",
            "type": "paragraph",
            "data": {
                "text": "Akshaya Tritiya 2026 has just passed — and for discerning families across Gurgaon and Delhi NCR, the season it inaugurates is far from over. The auspicious day, which fell on April 19 this year, marks the beginning of the most significant jewellery-buying period in the Indian calendar: the wedding season. Gold sales nationwide surged 56% in volume year-on-year to 25 tonnes, and natural diamond purchases rose 12% as families invested in pieces designed to endure not just a season but a lifetime. At Auric Jewels, Gurgaon’s trusted destination for certified gold and diamond jewellery, this season represents an invitation to acquire something truly timeless — guided by clarity, craftsmanship, and a heritage of trust."
            }
        },
        {
            "id": "h2_01",
            "type": "header",
            "data": {
                "text": "The Significance of Akshaya Tritiya for Jewellery Buyers in Gurgaon",
                "level": 2
            }
        },
        {
            "id": "p_02",
            "type": "paragraph",
            "data": {
                "text": "Akshaya Tritiya — the Sanskrit word meaning “never diminishing” — is regarded as one of the most auspicious occasions in the Hindu calendar for making lasting investments. Acquiring gold and fine jewellery on this day is believed to bring unending prosperity to the household. In 2026, with 24-karat gold trading at approximately ₹1.54 lakh per 10 grams, the decision to invest in certified, hallmarked jewellery is not only spiritually meaningful but financially significant."
            }
        },
        {
            "id": "p_03",
            "type": "paragraph",
            "data": {
                "text": "In Gurgaon, where wealth is concentrated and taste is cultivated, Akshaya Tritiya buying has evolved beyond a ritual into a considered act of legacy planning. Families visiting Auric Jewels during this season are not merely purchasing jewellery — they are selecting heirlooms: pieces that will travel forward through generations, worn at weddings, held in velvet boxes, and passed between mothers and daughters with equal reverence."
            }
        },
        {
            "id": "h2_02",
            "type": "header",
            "data": {
                "text": "What Auric Jewels Curated for Akshaya Tritiya 2026",
                "level": 2
            }
        },
        {
            "id": "p_04",
            "type": "paragraph",
            "data": {
                "text": "The Auric Jewels Akshaya Tritiya 2026 selection was built around four guiding principles: certified quality, design distinction, wearable permanence, and Gurgaon’s evolving taste for refined luxury. Here is what our clients discovered this season."
            }
        },
        {
            "id": "h3_01",
            "type": "header",
            "data": {
                "text": "22-Karat BIS Hallmarked Gold Jewellery",
                "level": 3
            }
        },
        {
            "id": "p_05",
            "type": "paragraph",
            "data": {
                "text": "With gold at its current valuation, BIS hallmarked 22-karat gold jewellery occupies the highest-demand position in the bridal and gifting category. Every gram carries not just monetary value but the assurance of verified purity — a non-negotiable for informed buyers. At Auric Jewels, our gold necklace sets, bangles, and earrings each carry a HUID-stamped BIS hallmark, verifiable on the national BIS portal. For the Akshaya Tritiya buyer seeking gold with absolute integrity, this assurance is foundational."
            }
        },
        {
            "id": "h3_02",
            "type": "header",
            "data": {
                "text": "IGI-Certified Solitaire Diamond Rings",
                "level": 3
            }
        },
        {
            "id": "p_06",
            "type": "paragraph",
            "data": {
                "text": "The solitaire diamond ring has emerged as the definitive Akshaya Tritiya purchase for 2026 — a piece that bridges the occasion with the wedding season that follows. India’s preference for solitaire cuts has matured significantly: oval east-west settings, elongated cushion cuts, and classic round brilliants are all in demand, each set into architectural 18-karat gold bands that complement rather than overpower the stone."
            }
        },
        {
            "id": "p_07",
            "type": "paragraph",
            "data": {
                "text": "Auric Jewels’ solitaire collection features IGI-certified natural diamonds from 0.50 carats to over 3.00 carats. Each stone is selected by our in-house gemologist for superior cut, colour, and clarity. A solitaire from Auric Jewels is not a commodity purchase — it is an acquisition informed by expertise, documented by certification, and designed to appreciate in personal meaning with every year that passes."
            }
        },
        {
            "id": "h3_03",
            "type": "header",
            "data": {
                "text": "Natural Diamond Mangalsutras — Tradition Reimagined",
                "level": 3
            }
        },
        {
            "id": "p_08",
            "type": "paragraph",
            "data": {
                "text": "The mangalsutra remains one of the most emotionally significant purchases of the Akshaya Tritiya season. In 2026, the modern mangalsutra has evolved: white gold chains set with VS-clarity diamond pendants, sleek dual-chain designs in yellow gold, and contemporary asymmetric forms that pair with both a silk saree and a linen blazer. At Auric Jewels, our diamond mangalsutra collection offers this essential piece in designs that honour its sacred purpose while embracing the contemporary Indian woman’s aesthetic."
            }
        },
        {
            "id": "h3_04",
            "type": "header",
            "data": {
                "text": "Heritage Bridal Necklace Sets for the Wedding Season",
                "level": 3
            }
        },
        {
            "id": "p_09",
            "type": "paragraph",
            "data": {
                "text": "Akshaya Tritiya opens the wedding calendar — and for families with forthcoming celebrations, the visit to Auric Jewels often doubles as a bridal jewellery consultation. Our bridal necklace suites for the 2026 wedding season draw from the season’s prevailing aesthetic: bold temple-inspired forms in 22-karat gold, heritage enamel work with diamond accents, and layered designs that transition between ceremonies without requiring a jewellery change. Our bridal consultations are private, unhurried, and led by experienced advisors who understand that a bridal set must complement skin tone, lehenga palette, and personal temperament."
            }
        },
        {
            "id": "h2_03",
            "type": "header",
            "data": {
                "text": "The Case for Natural Diamonds at Current Gold Valuations",
                "level": 2
            }
        },
        {
            "id": "p_10",
            "type": "paragraph",
            "data": {
                "text": "With gold at ₹1.54 lakh per 10 grams, the value proposition for certified natural diamond jewellery has never been sharper. Diamond jewellery offers an irreplaceable combination of aesthetic elegance and intrinsic value — without the weight of equivalent-cost gold pieces. A 1.00-carat IGI-certified round brilliant solitaire in an 18-karat gold setting from Auric Jewels delivers brilliance, portability, and documented provenance that no gold bangle can replicate. For the Akshaya Tritiya buyer who views jewellery as both ornament and investment, natural diamond jewellery from a certified showroom represents the most considered allocation of a meaningful budget."
            }
        },
        {
            "id": "h2_04",
            "type": "header",
            "data": {
                "text": "Bespoke Jewellery — When the Season Calls for Something Entirely Your Own",
                "level": 2
            }
        },
        {
            "id": "p_11",
            "type": "paragraph",
            "data": {
                "text": "Not every milestone deserves an off-the-shelf response. For clients marking a 25th anniversary, commissioning a daughter’s first set, or seeking an engagement ring as distinct as the relationship it celebrates, Auric Jewels offers a full bespoke design service. The process begins with a private conversation — about the wearer, the occasion, the aesthetic, the intention. From there, our design team works through sketches, CAD renders, and stone selection to produce a piece that exists nowhere else in the world. Akshaya Tritiya is an ideal moment to commission a bespoke piece: the season’s energy of new beginnings aligns perfectly with the creation of something made to last."
            }
        },
        {
            "id": "h2_05",
            "type": "header",
            "data": {
                "text": "Frequently Asked Questions — Akshaya Tritiya Jewellery Buying in Gurgaon",
                "level": 2
            }
        },
        {
            "id": "h3_05",
            "type": "header",
            "data": {
                "text": "Is Akshaya Tritiya still a good time to buy gold in 2026?",
                "level": 3
            }
        },
        {
            "id": "p_12",
            "type": "paragraph",
            "data": {
                "text": "Yes. Despite gold trading at ₹1.54 lakh per 10 grams, Akshaya Tritiya remains the most auspicious and psychologically meaningful time to invest in gold and diamond jewellery. For certified, hallmarked pieces from a trusted showroom like Auric Jewels, the purchase represents lasting value regardless of the day’s spot price."
            }
        },
        {
            "id": "h3_06",
            "type": "header",
            "data": {
                "text": "What is the best jewellery to buy on Akshaya Tritiya?",
                "level": 3
            }
        },
        {
            "id": "p_13",
            "type": "paragraph",
            "data": {
                "text": "The best choice depends on the buyer’s purpose. For investment, BIS hallmarked 22-karat gold jewellery offers the most transparent value. For milestone gifting, an IGI-certified solitaire ring or diamond pendant from Auric Jewels is unmatched in elegance and provenance. For bridal trousseau planning, Akshaya Tritiya is the ideal moment to begin a consultation for a complete wedding set."
            }
        },
        {
            "id": "h3_07",
            "type": "header",
            "data": {
                "text": "Does Auric Jewels offer private consultations?",
                "level": 3
            }
        },
        {
            "id": "p_14",
            "type": "paragraph",
            "data": {
                "text": "Yes. Auric Jewels offers private consultations by appointment for bridal jewellery, solitaire selection, and bespoke design. Visit our showroom in Gurgaon (open 10 AM to 8 PM, seven days a week) or book an appointment at auricjewels.com."
            }
        },
        {
            "id": "h3_08",
            "type": "header",
            "data": {
                "text": "What certifications does Auric Jewels provide?",
                "level": 3
            }
        },
        {
            "id": "p_15",
            "type": "paragraph",
            "data": {
                "text": "Every diamond at Auric Jewels comes with an IGI or GIA certificate. All gold jewellery carries a BIS hallmark with a unique HUID number, verifiable on the official BIS portal. These certifications ensure that every purchase is fully documented and traceable — an essential assurance at current gold valuations."
            }
        },
        {
            "id": "h2_06",
            "type": "header",
            "data": {
                "text": "The Season of Celebration Begins at Auric Jewels, Gurgaon",
                "level": 2
            }
        },
        {
            "id": "p_16",
            "type": "paragraph",
            "data": {
                "text": "Akshaya Tritiya 2026 is not a single day — it is a beginning. The weddings, the anniversaries, the first purchases and the milestone gifts that follow over the next six months are all part of the season this auspicious occasion inaugurates. Auric Jewels, Gurgaon’s foremost destination for certified gold and diamond jewellery, is honoured to be your partner through every one of those moments. Visit our showroom in Gurgaon or explore the complete collection at auricjewels.com. For private appointments and bespoke enquiries, call +91-9012495941."
            }
        }
    ],
    "version": "2.26.5"
}

mutation = """
mutation CreatePage($input: PageCreateInput!) {
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
      message
      code
    }
  }
}
"""

variables = {
    "input": {
        "title": "Akshaya Tritiya 2026 in Gurgaon — Celebrating Prosperity with Fine Gold & Diamond Jewellery from Auric Jewels",
        "slug": "akshaya-tritiya-2026-gold-jewellery-gurgaon-auric-jewels",
        "pageType": PAGE_TYPE_ID,
        "isPublished": True,
        "content": json.dumps(content_json),
        "seo": {
            "title": "Akshaya Tritiya 2026 Gold Jewellery Gurgaon | Auric Jewels",
            "description": "Celebrate Akshaya Tritiya 2026 with fine gold & diamond jewellery from Auric Jewels, Gurgaon. IGI-certified solitaires, BIS hallmarked gold, bridal sets & bespoke designs for the discerning collector."
        }
    }
}

payload = json.dumps({"query": mutation, "variables": variables}).encode("utf-8")

req = urllib.request.Request(
    ENDPOINT,
    data=payload,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
        result = json.loads(body)
        print(json.dumps(result, indent=2, ensure_ascii=False))
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
    print(e.read().decode("utf-8"))
except urllib.error.URLError as e:
    print(f"URL Error: {e.reason}")
except Exception as e:
    print(f"Error: {e}")
