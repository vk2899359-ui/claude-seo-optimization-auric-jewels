#!/usr/bin/env python3
"""
Auric Jewels — Create SEO Collection Page #7
Slug: office-wear-jewellery
Run: python scripts/page-07-office-wear.py
"""
import json, urllib.request, urllib.error, sys

API          = "https://auric.thecodemesh.online/graphql/"
TOKEN        = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

PAGE = {
    "slug": "office-wear-jewellery",
    "title": "Office Wear Jewellery | Subtle Gold & Diamond Pieces",
    "seoTitle": "Office Wear Jewellery Gurgaon | Gold & Diamond | Auric Jewels",
    "seoDescription": (
        "Shop office wear jewellery at Auric Jewels, Sector 45 Gurgaon. Subtle gold & diamond "
        "studs, slim chains, stacking rings & bracelets perfect for the professional woman. "
        "BIS hallmarked & IGI certified."
    ),
    "content": """
<h1>Office Wear Jewellery | Subtle Gold & Diamond Pieces</h1>

<p>The professional woman in Gurgaon navigates multiple worlds in a single day — a morning board presentation, a client lunch, an evening networking event, and perhaps a casual dinner after. Her jewellery must work flawlessly across all of these contexts without drawing attention away from her competence. At <strong>Auric Jewels, Sector 45 Gurugram</strong>, our office wear collection is curated precisely for this woman: pieces that signal refinement and authority without spectacle.</p>

<h2>The Office Wear Jewellery Philosophy</h2>

<p>Office jewellery occupies the space between invisible and conspicuous. The goal is to be noticed for the overall effect — a woman who is well put-together — rather than to have the jewellery itself become the topic of conversation. This calls for:</p>
<ul>
  <li>Smaller stones and simpler silhouettes that photograph neutrally on video calls</li>
  <li>Metal finishes (white gold, yellow gold) that complement rather than clash with wardrobe palettes</li>
  <li>Secure fastenings that do not require adjustment through the day</li>
  <li>Lightweight construction that remains comfortable across 10–12 hour workdays</li>
</ul>

<h2>Diamond Studs: The Cornerstone of Office Jewellery</h2>

<p>A single pair of <strong>round-brilliant diamond studs in 18K white gold</strong> — in the 0.10 to 0.30 carat range per pair — is the single most versatile piece of office jewellery in existence. Studs sit flush against the ear, present no snag risk, and read as effortlessly polished in both Indian and international professional environments. Our studs are individually IGI or GIA certified, ensuring the quality is real and verifiable.</p>

<p>For those who prefer a slightly more decorative look without crossing into formal territory, our <strong>bezel-set stud earrings</strong> — where a thin gold rim encircles the stone instead of prongs — are increasingly popular with architects, lawyers, and corporate professionals. The bezel setting is also more durable than prong settings for active daily wear.</p>

<h2>Slim Chains for Professional Necklines</h2>

<p>A <strong>slim 18K gold chain (1–1.5mm width)</strong> worn at the collarbone is the ideal complement to both formal shirts and blouses. Our box chains and cable chains in this width sit almost invisibly at the neck in meetings but catch the light beautifully at evening events. Pair with a small diamond or gold pendant for added personality that stays within professional boundaries.</p>

<p>For a more structured neckline, our <strong>gold bar necklaces</strong> — a thin horizontal bar in 18K gold, plain or with a small pavé accent — are designed specifically for this purpose. They work beautifully with open-collar shirts and V-neck blouses.</p>

<h2>Stacking Rings for the Professional Hand</h2>

<p>A single <strong>slim 18K gold band (2mm)</strong> worn on the right hand speaks volumes with total restraint. Our stacking ring collection allows you to wear one, two, or three thin bands — in plain, milgrain, or single-diamond-set styles — in combinations that remain completely office-appropriate. Many of our professional clients maintain one set of stacking rings for work and rearrange or add to them for evening and weekend wear.</p>

<h2>Bracelets That Stay in Their Lane</h2>

<p>Bracelets for the office require cuff-friendly proportions and silent wear. Our <strong>thin oval-link gold bracelets</strong> in 18K gold (2mm width) sit neatly under shirt and kurta sleeves, clicking open and shut with a secure box clasp. Our <strong>slim diamond tennis bracelets</strong> (0.25–0.50 carats total) are appropriate for business environments where tasteful jewellery is acceptable — they catch the light subtly rather than flashily.</p>

<p>For a full guide to building a working-woman jewellery collection from daily wear to formal, read our article on <a href="/blog/lightweight-gold-jewellery-working-women-daily-wear">lightweight gold jewellery for working women</a>. And if you are building up your diamond collection gradually, our guide to <a href="/blog/diamond-earrings-daily-wear-under-50000">daily wear diamond earrings under ₹50,000</a> outlines exactly which designs last and which trends fade.</p>

<h2>Visit or WhatsApp Us</h2>

<p>Our <strong>Sector 45, Gurugram showroom</strong> is open seven days a week. Our consultants understand the professional context and will help you build a compact, high-quality office jewellery wardrobe that earns compliments without demanding attention. WhatsApp us photos of your typical office outfits and we'll suggest pieces before you even step in — saving you time and delivering curated recommendations you can try in person.</p>
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
