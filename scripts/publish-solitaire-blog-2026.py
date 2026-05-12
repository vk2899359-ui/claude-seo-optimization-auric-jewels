"""
Auric Jewels — Saleor pageCreate Publisher
==========================================
Publishes the solitaire diamond ring SEO blog post via Saleor GraphQL API.

USAGE (run from your local machine — API endpoint is IP-restricted):
    python3 scripts/publish-solitaire-blog-2026.py

Config:
    Endpoint  : https://auric.thecodemesh.online/graphql/
    Auth Token: rlcLjvXb3wMMHMf1PBsePS8UdTmOBb
    Channel   : franchise1
    PageType  : UGFnZVR5cGU6Ng==
"""

import json
import time
import urllib.request
import urllib.error

API_ENDPOINT = "https://auric.thecodemesh.online/graphql/"
AUTH_TOKEN   = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="
CHANNEL      = "franchise1"

TITLE = "The Art of the Solitaire: How Gurgaon's Most Discerning Brides Are Choosing Their Diamond Ring in 2026"
SLUG  = "solitaire-diamond-ring-gurgaon-2026"
SEO_TITLE       = "Solitaire Diamond Ring Gurgaon 2026 | Luxury Bridal Rings | Auric Jewels"
SEO_DESCRIPTION = (
    "Discover the finest solitaire diamond rings in Gurgaon at Auric Jewels. "
    "GIA-certified oval, cushion & round brilliant cuts in 18K gold & platinum. "
    "Private bridal consultations available."
)

# Editor.js JSON content — Saleor's rich-text format
EDITORJS_CONTENT = {
    "time": int(time.time() * 1000),
    "version": "2.26.5",
    "blocks": [
        {
            "id": "b01", "type": "paragraph",
            "data": {"text": "There is a moment every bride knows — when the stone catches the light for the first time and everything else in the room disappears. In 2026, that moment belongs to the solitaire diamond ring. Not the layered look, not the cluster setting, not the coloured gemstone accent. Just one diamond, perfectly chosen, set with absolute intention."}
        },
        {
            "id": "b02", "type": "paragraph",
            "data": {"text": "At Auric Jewels in Gurgaon, we have witnessed a profound shift over the past season. The brides walking through our doors arrive with extraordinary clarity of vision. They have done their research. They understand the four Cs. They know the difference between a GIA-certified stone and one that simply looks beautiful under showroom lighting. And overwhelmingly, they are choosing the solitaire."}
        },
        {
            "id": "b03", "type": "header",
            "data": {"text": "Why the Solitaire Has Reclaimed Its Crown in 2026", "level": 2}
        },
        {
            "id": "b04", "type": "paragraph",
            "data": {"text": "The solitaire diamond ring has always been the purest expression of commitment — one stone, one promise, no distraction. But 2026 has elevated it further. As Indian brides become more globally influenced and confidently discerning, the maximalist stacked look is yielding to the quiet authority of a single, exceptional diamond."}
        },
        {
            "id": "b05", "type": "paragraph",
            "data": {"text": "Design houses from Antwerp to Mumbai are reporting the same trend: brides are investing in one remarkable stone rather than several modest ones. A single two-carat oval-cut solitaire makes a declaration that a ring set with twelve quarter-carat diamonds simply cannot. And with 22K gold trading at ₹13,945 per gram and 24K at ₹15,213 per gram in May 2026, the discerning bride is concentrating her investment where it will appreciate most — in the diamond itself."}
        },
        {
            "id": "b06", "type": "header",
            "data": {"text": "The Cuts That Are Defining Gurgaon's Bridal Season", "level": 2}
        },
        {
            "id": "b07", "type": "header",
            "data": {"text": "The Oval Cut", "level": 3}
        },
        {
            "id": "b08", "type": "paragraph",
            "data": {"text": "If there is one shape dominating Gurgaon's luxury jewellery conversations in 2026, it is the oval. Oval-cut diamonds create the illusion of greater size — a 1.5-carat oval appears as expansive as a 2-carat round brilliant on the finger. They elongate with effortless elegance and are extraordinarily flattering across every hand type. Our brides, from DLF Phase 1 to Golf Course Road, are requesting this cut almost exclusively."}
        },
        {
            "id": "b09", "type": "header",
            "data": {"text": "The Elongated Cushion", "level": 3}
        },
        {
            "id": "b10", "type": "paragraph",
            "data": {"text": "For the bride who finds the round brilliant too conventional but remains drawn to a softer, romantic silhouette, the elongated cushion offers the ideal answer. Its gently rounded corners and deep pavilion hold fire brilliantly — that prismatic play of colour that commands attention across a wedding mandap."}
        },
        {
            "id": "b11", "type": "header",
            "data": {"text": "The Classic Round Brilliant", "level": 3}
        },
        {
            "id": "b12", "type": "paragraph",
            "data": {"text": "There is a reason this cut has never truly fallen from favour. Its 57 or 58 precisely calculated facets are engineered to return more light to the eye than any other shape. For brides who want the stone itself to do all the speaking, this remains the definitive choice."}
        },
        {
            "id": "b13", "type": "header",
            "data": {"text": "Understanding What You Are Buying: The Auric Difference", "level": 2}
        },
        {
            "id": "b14", "type": "paragraph",
            "data": {"text": "Gurgaon has no shortage of jewellery options. What it has in shorter supply is genuine expertise in exceptional stones. At Auric Jewels, every solitaire in our collection is independently certified — primarily by GIA (Gemological Institute of America), the global standard in diamond grading. Our team does not simply present certificates; we educate."}
        },
        {
            "id": "b15", "type": "paragraph",
            "data": {"text": "When you sit across from our gemologist, you will understand precisely why a G-colour, VS1-clarity stone in a superior cut outperforms a comparable F-colour stone with a lesser cut grade. We work with a curated network of diamond merchants who share our commitment to ethical sourcing and complete transparency of origin. Every stone that becomes an Auric solitaire can be traced through its supply chain with full documentation."}
        },
        {
            "id": "b16", "type": "header",
            "data": {"text": "The Setting Is Not Secondary", "level": 2}
        },
        {
            "id": "b17", "type": "paragraph",
            "data": {"text": "The solitaire setting is frequently underestimated because it appears simple. In practice, it demands greater craftsmanship than any ornate cluster design, because there is nothing to draw the eye away from imperfection."}
        },
        {
            "id": "b18", "type": "header",
            "data": {"text": "The Knife-Edge Six-Prong", "level": 3}
        },
        {
            "id": "b19", "type": "paragraph",
            "data": {"text": "Six delicate prongs rising to hold the diamond at the point of a blade-thin band. Maximum light enters from every angle; maximum brilliance returns to the eye. The band appears to vanish beneath the stone, placing all attention where it belongs."}
        },
        {
            "id": "b20", "type": "header",
            "data": {"text": "The Bezel-Set Solitaire", "level": 3}
        },
        {
            "id": "b21", "type": "paragraph",
            "data": {"text": "For the contemporary bride who lives an active life without wanting to compromise her ring, the bezel setting encircles the diamond in a fine rim of 18K gold or platinum. It reads as architectural and modern, protecting the stone from the side while keeping the table fully exposed to light."}
        },
        {
            "id": "b22", "type": "header",
            "data": {"text": "The Cathedral Setting", "level": 3}
        },
        {
            "id": "b23", "type": "paragraph",
            "data": {"text": "Two arches of gold rise from the band to embrace the stone, elevating it dramatically above the finger. This is the setting for a bride who wishes her ring to make a presence felt across a reception hall."}
        },
        {
            "id": "b24", "type": "header",
            "data": {"text": "Pairing Your Solitaire with the Bridal Look", "level": 2}
        },
        {
            "id": "b25", "type": "paragraph",
            "data": {"text": "One of the quiet skills our Auric styling consultants have developed is helping brides integrate a solitaire into the full landscape of their bridal jewellery. The solitaire ring does not compete — it anchors. A bride wearing a heavily worked Polki and Jadau set for her ceremony can transition to her diamond solitaire and a slender diamond bracelet for the reception. The effect is both coherent and breathtaking."}
        },
        {
            "id": "b26", "type": "header",
            "data": {"text": "Investing in a Solitaire Diamond Ring in Gurgaon", "level": 2}
        },
        {
            "id": "b27", "type": "paragraph",
            "data": {"text": "A solitaire diamond ring of genuine quality — a GIA-certified stone of 0.75 carats or above in an expertly crafted 18K gold or platinum setting — is a piece that transcends occasion. It is not jewellery for a wedding. It is jewellery for a lifetime."}
        },
        {
            "id": "b28", "type": "paragraph",
            "data": {"text": "At Auric Jewels, our solitaire collections begin where most end. We do not believe in compromise at this level of investment, and neither, we have found, do our clients. We invite you to visit our Gurgaon boutique for a private consultation with our gemologist. Bring your questions, bring your instincts, and allow us to help you find the one stone that will carry every promise you are about to make."}
        },
    ]
}

MUTATION = """
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
      code
      message
    }
  }
}
"""

VARIABLES = {
    "input": {
        "title":       TITLE,
        "slug":        SLUG,
        "pageType":    PAGE_TYPE_ID,
        "isPublished": True,
        "content":     json.dumps(EDITORJS_CONTENT),
        "seo": {
            "title":       SEO_TITLE,
            "description": SEO_DESCRIPTION,
        },
        "attributes": [],
    }
}


def graphql(query, variables=None):
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        API_ENDPOINT,
        data=payload,
        headers={
            "Content-Type":  "application/json",
            "Authorization": f"Bearer {AUTH_TOKEN}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"HTTP {e.code}: {e.reason}\n{body[:400]}")
        return None
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}")
        return None


def main():
    print("\nAuric Jewels — Saleor Blog Publisher")
    print("=" * 50)
    print(f"Title : {TITLE}")
    print(f"Slug  : {SLUG}")
    print(f"Type  : {PAGE_TYPE_ID}")
    print()

    result = graphql(MUTATION, VARIABLES)

    if not result:
        print("No response from API. Check network access and token.")
        return

    if "errors" in result:
        print("GraphQL errors:")
        for e in result["errors"]:
            print(f"  - {e.get('message')}")
        return

    data = result.get("data", {}).get("pageCreate", {})
    page_errors = data.get("errors", [])

    if page_errors:
        print("pageCreate errors:")
        for e in page_errors:
            print(f"  [{e.get('field')}] {e.get('code')}: {e.get('message')}")
        return

    page = data.get("page", {})
    print("SUCCESS — Page published!")
    print(f"  ID          : {page.get('id')}")
    print(f"  Slug        : {page.get('slug')}")
    print(f"  Published   : {page.get('isPublished')}")
    print(f"  URL         : https://www.auricjewels.com/blog/{page.get('slug')}")


if __name__ == "__main__":
    main()
