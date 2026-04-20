#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auric Jewels -- Fix Duplicate & Oversized SEO Meta Titles/Descriptions
=======================================================================
Audit: 20 Apr 2026

Issues found (21 pages):
  - 18/21 seoTitles exceed 60 chars (Google truncates at ~60)
  - 8/21 seoDescriptions out of 150-160 char target range
  - Page 1 had "Auric Jewels" duplicated in title
  - Page 19 had "Gurgaon" duplicated in title
  - 0 duplicate titles or descriptions detected

USAGE (Windows):
    python scripts/fix-seo-meta.py

API: https://auric.thecodemesh.online/graphql/
"""

import json
import time
import urllib.request
import urllib.error
import ssl
import sys
import io

# Fix Windows console UTF-8 output (handles Rs, em-dash etc.)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── Config ───────────────────────────────────────────────────
API = "https://auric.thecodemesh.online/graphql/"
TOKEN = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"

# ── Pre-computed SEO fixes (audited 20 Apr 2026) ─────────────
# Rules: title ≤60 chars, desc 150-160 chars, unique, Gurgaon included
FIXES = {
    # ── title was 91 chars, desc was 164 chars ──────────────
    "best-diamond-jewellery-showroom-gurgaon": {
        "seoTitle": "Best Diamond Jewellery Showroom Gurgaon | Auric Jewels",
        "seoDescription": (
            "Best diamond jewellery showroom in Gurgaon. Auric Jewels — "
            "IGI/GIA certified diamonds, BIS hallmarked gold & solitaire "
            "rings. Visit Sector 45 or shop online."
        ),
    },
    # ── title was 79 chars, desc was 168 chars ──────────────
    "solitaire-ring-buying-guide-gurgaon": {
        "seoTitle": "Solitaire Ring Guide Gurgaon | Cuts & Price | Auric",
        "seoDescription": (
            "Complete solitaire ring buying guide for Gurgaon shoppers. "
            "Diamond cuts, clarity grades, IGI/GIA certification & price "
            "ranges. Expert advice at Auric Jewels."
        ),
    },
    # ── title was 83 chars ──────────────────────────────────
    "luxury-bridal-gold-jewellery-gurgaon": {
        "seoTitle": "Bridal Gold Jewellery Gurgaon | Wedding Sets | Auric",
        "seoDescription": (
            "Complete bridal gold jewellery guide for Gurgaon brides. "
            "Wedding set checklist, 22K vs 18K gold, budget planning & "
            "timeline. Visit Auric Jewels showroom."
        ),
    },
    # ── title was 72 chars ──────────────────────────────────
    "diamond-mangalsutra-modern-designs": {
        "seoTitle": "Diamond Mangalsutra Modern Designs 2026 | Auric Gurgaon",
        "seoDescription": (
            "Guide to choosing a modern diamond mangalsutra. Single-line, "
            "dual-chain & bracelet styles. Certified diamonds & sizing "
            "tips. Shop at Auric Jewels Gurgaon."
        ),
    },
    # ── title was 82 chars ──────────────────────────────────
    "gold-rate-today-gurgaon-buying-tips": {
        "seoTitle": "Gold Rate Gurgaon | Smart Jewellery Buying Tips | Auric",
        "seoDescription": (
            "Understand gold rates in Gurgaon before buying jewellery. "
            "Learn what drives prices, 22K vs 18K costs, making charges "
            "& how to buy smart at Auric Jewels."
        ),
    },
    # ── title was 76 chars, desc was 148 chars ──────────────
    "custom-diamond-jewellery-gurgaon": {
        "seoTitle": "Custom Diamond Jewellery Gurgaon | Auric Jewels",
        "seoDescription": (
            "Create bespoke diamond jewellery at Auric Jewels Gurgaon. "
            "Custom engagement rings, bridal sets & heirloom redesigns. "
            "Sketch to IGI certified piece. Book now."
        ),
    },
    # ── title was 78 chars ──────────────────────────────────
    "polki-vs-kundan-vs-diamond-bridal-set": {
        "seoTitle": "Polki vs Kundan vs Diamond | Bridal Set Gurgaon | Auric",
        "seoDescription": (
            "Compare polki, kundan & diamond bridal jewellery. Brilliance, "
            "durability, price & which suits each wedding ceremony. "
            "Expert guide from Auric Jewels Gurgaon."
        ),
    },
    # ── title was 82 chars ──────────────────────────────────
    "anniversary-gift-jewellery-gurgaon": {
        "seoTitle": "Anniversary Jewellery Gifts Gurgaon | Auric Jewels",
        "seoDescription": (
            "Find the perfect anniversary jewellery gift at Auric Jewels "
            "Gurgaon. Ideas by milestone year, top-gifted pieces & "
            "personalisation options. Free gift wrapping."
        ),
    },
    # ── title was 85 chars, desc was 147 chars ──────────────
    "hallmark-gold-jewellery-purity-guide-gurgaon": {
        "seoTitle": "BIS Hallmark Gold Purity Guide Gurgaon | Auric Jewels",
        "seoDescription": (
            "Learn how to verify BIS hallmark & HUID on gold jewellery. "
            "Step-by-step guide to checking gold purity before buying in "
            "Gurgaon at Auric Jewels showroom."
        ),
    },
    # ── title was 73 chars ──────────────────────────────────
    "karva-chauth-gold-jewellery-gurgaon-2026": {
        "seoTitle": "Karva Chauth Gold Jewellery Gurgaon 2026 | Auric Jewels",
        "seoDescription": (
            "Shop Karva Chauth jewellery gifts at Auric Jewels Gurgaon. "
            "Diamond pendants, gold bangles, mangalsutra upgrades & "
            "trending styles 2026. Free gift wrapping."
        ),
    },
    # ── title was 80 chars, desc was 146 chars ──────────────
    "solitaire-vs-diamond-ring-difference": {
        "seoTitle": "Solitaire vs Diamond Ring Difference | Auric Gurgaon",
        "seoDescription": (
            "Understand the difference between solitaire and diamond rings. "
            "Compare styles, sparkle, price & occasions. Expert buying "
            "guide from Auric Jewels Gurgaon."
        ),
    },
    # ── title was 79 chars, desc was 141 chars ──────────────
    "mens-diamond-jewellery-gurgaon-2026": {
        "seoTitle": "Men's Diamond Jewellery Gurgaon 2026 | Auric Jewels",
        "seoDescription": (
            "Discover men's gold & diamond jewellery trending in Gurgaon "
            "2026. Diamond studs, platinum chains, bracelets & rings. "
            "Shop certified pieces at Auric Jewels."
        ),
    },
    # ── title was 79 chars ──────────────────────────────────
    "engagement-ring-shopping-gurgaon": {
        "seoTitle": "Engagement Ring Shopping Gurgaon | Auric Jewels",
        "seoDescription": (
            "Complete engagement ring shopping guide for Gurgaon couples. "
            "Budget tips, diamond quality, ring styles & what to ask your "
            "jeweller. Visit Auric Jewels."
        ),
    },
    # ── title was 75 chars, desc was 142 chars ──────────────
    "diamond-earrings-daily-wear-under-50000": {
        "seoTitle": "Diamond Earrings Under ₹50K Gurgaon | Auric Jewels",
        "seoDescription": (
            "Shop daily wear diamond earrings under ₹50,000 at Auric Jewels "
            "Gurgaon. Studs, hoops & drops in 18K gold. IGI certified "
            "diamonds. Free shipping across India."
        ),
    },
    # ── title was 77 chars, desc was 148 chars ──────────────
    "bis-hallmark-gold-jewellery-buying-guide": {
        "seoTitle": "Why BIS Hallmark Matters | Gold Buying Guide Gurgaon",
        "seoDescription": (
            "Why BIS hallmark is essential when buying gold jewellery in "
            "Gurgaon. What HUID means, how to verify purity & red flags "
            "to avoid. Full guide at Auric Jewels."
        ),
    },
    # ── title was 63 chars (trim 3) ─────────────────────────
    "lightweight-gold-jewellery-working-women-daily-wear": {
        "seoTitle": "Lightweight Gold Jewellery Working Women | Auric Gurgaon",
        "seoDescription": (
            "Discover the best lightweight gold jewellery for working women "
            "— daily wear studs, chains, pendants & bangles in 18K/22K "
            "gold. Visit Auric Jewels Gurgaon."
        ),
    },
    # ── title was 63 chars (trim 3) ─────────────────────────
    "lab-grown-vs-natural-diamonds-comparison-india": {
        "seoTitle": "Lab-Grown vs Natural Diamonds India 2026 | Auric Jewels",
        "seoDescription": (
            "Lab-grown vs natural diamonds — price, resale value, "
            "certification & which to buy. Full 2026 comparison guide. "
            "Certified diamonds at Auric Jewels Gurgaon."
        ),
    },
    # ── title OK (57 chars), desc OK (160 chars) ────────────
    "jewellery-trends-india-2026": {
        "seoTitle": "Top 10 Jewellery Trends India 2026 | Auric Jewels",
        "seoDescription": (
            "Discover the top 10 jewellery trends in India for 2026 — "
            "layered necklaces, sculptural earrings, Polki revival & more. "
            "Explore trending designs at Auric Jewels."
        ),
    },
    # ── title was 61 chars (had Gurgaon twice) ──────────────
    "gold-jewellery-investment-2026-gurgaon": {
        "seoTitle": "Gold Jewellery Investment 2026 Gurgaon | Auric Jewels",
        "seoDescription": (
            "Gold jewellery as investment in 2026 — price trends, BIS "
            "hallmark, making charges, resale value & smart buying guide. "
            "Trusted jeweller Auric Jewels Gurgaon."
        ),
    },
    # ── title OK (58 chars), desc OK (160 chars) ────────────
    "platinum-jewellery-men-gurgaon": {
        "seoTitle": "Platinum Jewellery for Men Gurgaon | Auric Jewels",
        "seoDescription": (
            "Explore platinum jewellery for men — chains, bracelets, rings "
            "& cufflinks. Durable, hypoallergenic & sophisticated. Shop "
            "men's platinum at Auric Jewels Gurgaon."
        ),
    },
    # ── title OK (59 chars), desc OK (157 chars) ────────────
    "layered-necklace-styling-guide-indian-women": {
        "seoTitle": "Layered Necklace Styling Guide India | Auric Jewels",
        "seoDescription": (
            "Master layered necklace styling — rules, combinations, Indian "
            "& Western looks. Gold & diamond layering tips for 2026. "
            "Shop necklaces at Auric Jewels Gurgaon."
        ),
    },
}


# ── GraphQL helpers ──────────────────────────────────────────
def gql(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    req = urllib.request.Request(
        API,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Bearer " + TOKEN,
        },
        method="POST",
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return {"networkError": "HTTP " + str(e.code) + ": " + body[:300]}
    except Exception as e:
        return {"networkError": str(e)}


def fetch_all_pages():
    print("Fetching all pages from Saleor...")
    pages = []
    cursor = None
    while True:
        after = f', after: "{cursor}"' if cursor else ""
        q = f"""
        {{
          pages(first: 100{after}) {{
            pageInfo {{ hasNextPage endCursor }}
            edges {{
              node {{
                id
                slug
                title
                seoTitle
                seoDescription
              }}
            }}
          }}
        }}
        """
        r = gql(q)
        if "networkError" in r:
            print(f"  ERROR: {r['networkError']}")
            return None
        data = (r.get("data") or {}).get("pages", {})
        edges = data.get("edges", [])
        for edge in edges:
            pages.append(edge["node"])
        pi = data.get("pageInfo", {})
        if pi.get("hasNextPage"):
            cursor = pi["endCursor"]
        else:
            break
    print(f"  Fetched {len(pages)} pages.")
    return pages


def update_page(page_id, seo_title, seo_description):
    q = """
    mutation pageUpdate($id: ID!, $input: PageInput!) {
      pageUpdate(id: $id, input: $input) {
        page {
          id
          slug
          seoTitle
          seoDescription
        }
        errors {
          field
          message
        }
      }
    }
    """
    v = {
        "id": page_id,
        "input": {
            "seoTitle": seo_title,
            "seoDescription": seo_description,
        },
    }
    return gql(q, v)


def audit_pages(pages):
    """Return list of pages that need fixes."""
    issues = []
    seen_titles = {}
    seen_descs = {}

    for p in pages:
        page_issues = []
        t = (p.get("seoTitle") or "").strip()
        d = (p.get("seoDescription") or "").strip()

        if not t:
            page_issues.append("EMPTY_TITLE")
        elif t.lower() in ("auric jewels", "auricjewels"):
            page_issues.append("GENERIC_TITLE")
        elif len(t) > 60:
            page_issues.append(f"TITLE_TOO_LONG({len(t)})")

        if not d:
            page_issues.append("EMPTY_DESC")
        elif len(d) < 150:
            page_issues.append(f"DESC_TOO_SHORT({len(d)})")
        elif len(d) > 160:
            page_issues.append(f"DESC_TOO_LONG({len(d)})")

        if t:
            if t in seen_titles:
                page_issues.append(f"DUP_TITLE(also:{seen_titles[t]})")
            else:
                seen_titles[t] = p["slug"]

        if d:
            if d in seen_descs:
                page_issues.append(f"DUP_DESC(also:{seen_descs[d]})")
            else:
                seen_descs[d] = p["slug"]

        if page_issues:
            issues.append({**p, "issues": page_issues})

    return issues


def main():
    print("=" * 65)
    print("AURIC JEWELS — SEO Meta Fix Script  |  20 Apr 2026")
    print("=" * 65)

    # Pre-flight: validate fixes data
    print("\n[0] Pre-flight validation of fix data:")
    validation_errors = 0
    for slug, fix in FIXES.items():
        t = fix["seoTitle"]
        d = fix["seoDescription"]
        errs = []
        if len(t) > 60:
            errs.append(f"title too long ({len(t)} chars)")
        if len(d) < 150 or len(d) > 160:
            errs.append(f"desc out of range ({len(d)} chars)")
        if errs:
            print(f"  ❌ {slug}: {', '.join(errs)}")
            validation_errors += 1
        else:
            print(f"  ✓ {slug}: title={len(t)}, desc={len(d)}")
    if validation_errors:
        print(f"\n  {validation_errors} validation errors. Fix the data above before running.")
        sys.exit(1)
    print("  All fix data validated OK.")

    # Fetch pages
    print("\n[1] Fetching pages from Saleor:")
    pages = fetch_all_pages()
    if pages is None:
        print("  Cannot reach Saleor API. Ensure this script runs from a whitelisted IP.")
        sys.exit(1)

    # Audit
    print("\n[2] Auditing SEO fields:")
    issues = audit_pages(pages)
    if not issues:
        print("  No issues found. All pages have valid, unique SEO fields.")
    else:
        print(f"  Found {len(issues)} page(s) with issues:")
        for p in issues:
            print(f"    {p['slug']}: {', '.join(p['issues'])}")

    # Apply fixes
    print("\n[3] Applying fixes:")
    slug_to_id = {p["slug"]: p["id"] for p in pages}
    fixed = []
    skipped = []
    failed = []

    for slug, fix in FIXES.items():
        if slug not in slug_to_id:
            skipped.append(slug)
            print(f"  SKIP  {slug} (not found in Saleor)")
            continue

        page_id = slug_to_id[slug]
        r = update_page(page_id, fix["seoTitle"], fix["seoDescription"])

        if "networkError" in r:
            failed.append(slug)
            print(f"  FAIL  {slug}: {r['networkError']}")
            continue

        errors = (((r.get("data") or {}).get("pageUpdate") or {}).get("errors") or [])
        if errors:
            failed.append(slug)
            msgs = "; ".join(e.get("message", "?") for e in errors)
            print(f"  FAIL  {slug}: {msgs}")
        else:
            fixed.append(slug)
            print(f"  OK    {slug}")

        time.sleep(0.3)

    # Summary
    print("\n" + "=" * 65)
    print("SUMMARY")
    print("=" * 65)
    print(f"  Pages fetched   : {len(pages)}")
    print(f"  Issues detected : {len(issues)}")
    print(f"  Fixed           : {len(fixed)}")
    print(f"  Skipped         : {len(skipped)}")
    print(f"  Failed          : {len(failed)}")
    if failed:
        print(f"  Failed slugs    : {', '.join(failed)}")
    print("=" * 65)


if __name__ == "__main__":
    main()
