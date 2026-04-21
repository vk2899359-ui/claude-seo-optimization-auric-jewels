#!/usr/bin/env python3
"""
Auric Jewels — Create SEO Collection Page #10
Slug: new-arrivals-jewellery-gurgaon
Run: python scripts/page-10-new-arrivals.py
"""
import json, urllib.request, urllib.error, sys

API          = "https://auric.thecodemesh.online/graphql/"
TOKEN        = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
PAGE_TYPE_ID = "UGFnZVR5cGU6Ng=="

PAGE = {
    "slug": "new-arrivals-jewellery-gurgaon",
    "title": "New Arrivals in Gold & Diamond Jewellery | Auric Jewels",
    "seoTitle": "New Arrivals Gold & Diamond Jewellery Gurgaon 2026 | Auric Jewels",
    "seoDescription": (
        "Explore new arrivals in gold & diamond jewellery at Auric Jewels, Sector 45 Gurgaon. "
        "Latest 2026 designs in rings, earrings, necklaces & bracelets. "
        "BIS hallmarked & IGI certified. Visit showroom or WhatsApp."
    ),
    "content": """
<h1>New Arrivals in Gold & Diamond Jewellery | Auric Jewels</h1>

<p>Fine jewellery evolves — slowly, deliberately, and always in the direction of enduring beauty. At <strong>Auric Jewels, Sector 45 Gurugram</strong>, our new arrivals are not impulsive trend responses but considered additions to our permanent collection: designs that have been refined over months of consultation with our clients, drawing on both what is emerging in global jewellery design and what Indian women actually reach for again and again.</p>

<h2>What's New in 2026</h2>

<p>The 2026 jewellery season is characterised by a tension between maximum and minimum — and both are thriving simultaneously. On one hand, <strong>bold sculptural gold pieces</strong> with architectural, three-dimensional forms are earning significant attention among Gurgaon's design-forward clientele. On the other, <strong>ultra-fine diamond jewellery</strong> — stacking rings that are barely there, diamond dust pendants, and negative-space earrings — is winning converts among women who have always preferred restraint.</p>

<p>For a deeper look at what is driving Indian jewellery trends this year, read our comprehensive piece on <a href="/blog/jewellery-trends-india-2026">the top 10 jewellery trends in India for 2026</a>.</p>

<h2>New Gold Arrivals</h2>

<p>Our newest gold additions include:</p>

<ul>
  <li><strong>Sculptural 22K gold cuffs</strong> — wide-format bangles with hammered, organic surfaces that catch light differently at every angle. Each piece is unique in its texture.</li>
  <li><strong>Layered chain necklaces in 22K gold</strong> — two or three different link styles combined on a single clasp mechanism, designed to be worn as a single coordinated piece. Our <a href="/blog/layered-necklace-styling-guide-indian-women">layered necklace styling guide</a> shows exactly how to wear these.</li>
  <li><strong>18K gold charm bracelets with diamond accents</strong> — a contemporary take on the traditional gold bracelet, with detachable charm loops that allow personalisation over time.</li>
  <li><strong>Temple-work earrings in 22K gold (updated silhouettes)</strong> — our perennial temple jewellery range, refreshed with slimmer proportions and lighter weights for modern wear.</li>
</ul>

<h2>New Diamond Arrivals</h2>

<p>Our diamond collection has expanded significantly in 2026, with particular focus on:</p>

<ul>
  <li><strong>Fancy-cut diamond pendants</strong> — pear, marquise, and oval diamonds in 18K yellow gold settings, offering the romance of colourful geometry at prices comparable to round-brilliant equivalents of the same carat weight.</li>
  <li><strong>Open-work diamond rings</strong> — negative-space designs in 18K white gold where the diamond appears to float within the architecture of the setting rather than being held by it.</li>
  <li><strong>Diamond mangalsutra pendants (redesigned)</strong> — modern, lighter, and more wearable versions of a traditional piece, featuring certified diamonds in 18K gold. Our comprehensive guide to <a href="/blog/diamond-mangalsutra-modern-designs">choosing a modern diamond mangalsutra</a> covers all current design directions.</li>
  <li><strong>Men's diamond studs in 18K white gold</strong> — demand from Gurgaon's male clientele has grown steadily; our new men's range reflects this with designs calibrated for masculine aesthetics. See our guide on <a href="/blog/mens-diamond-jewellery-gurgaon-2026">trending men's diamond jewellery in Gurgaon 2026</a>.</li>
</ul>

<h2>Limited Quantities, Permanent Quality</h2>

<p>New arrival pieces at Auric Jewels are introduced in limited initial quantities to maintain the exclusivity our clients value. Once a design sells out, it may be reordered — but certain one-of-a-kind or very limited-run pieces will not be replicated. If you see something that speaks to you, visit or WhatsApp us promptly.</p>

<p>Every new arrival, like every piece in our permanent collection, is fully certified: BIS HUID hallmarked for gold, and individually IGI or GIA certified for diamonds. The documentation is included with your purchase, ensuring your investment is protected from day one.</p>

<h2>Stay Updated</h2>

<p>New pieces arrive at our showroom throughout the year. The most reliable way to see new arrivals before they sell is to follow us or WhatsApp our jewellery consultants directly — we send periodic updates to clients who have expressed interest in specific categories. Visit our <strong>Sector 45, Gurugram showroom</strong> any day of the week, or reach us on WhatsApp for photos and real-time availability before you make the trip.</p>
""",
}


def gql(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    req = urllib.request.Request(
        API,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"},
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
