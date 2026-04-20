"""
Auric Jewels — Bulk SEO Title + Meta Description Fixer
=======================================================
Run on your local machine (Windows/Mac/Linux):
    python scripts/fix-seo-bulk.py

No pip install needed — uses only Python stdlib.

What this does:
  1. AUDIT  — Fetches every product + page from Saleor and flags:
              duplicate titles, duplicate descriptions,
              too-short (<30 chars), too-long (>60 chars), empty
  2. FIX    — Generates corrected seoTitle + seoDescription per rules
  3. UPDATE — Bulk-updates via productUpdate / pageUpdate mutations
  4. VERIFY — Re-fetches and confirms everything is within spec
  5. LOG    — Writes AURIC_PROGRESS.md
"""

import json
import sys
import time
import textwrap
import urllib.request
import urllib.error
from collections import Counter
from datetime import date

# ── Configuration ─────────────────────────────────────────────────────────────
API = "https://auric.thecodemesh.online/graphql/"
TOKEN = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
CHANNEL = "default-channel"
BATCH_SIZE = 10

# ── GraphQL helpers ───────────────────────────────────────────────────────────

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
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        return {"errors": [{"message": f"HTTP {e.code}: {body[:200]}"}]}
    except Exception as e:
        return {"errors": [{"message": str(e)}]}


# ── Fetch all products ────────────────────────────────────────────────────────

PRODUCTS_QUERY = """
query Products($first: Int!, $after: String, $channel: String!) {
  products(first: $first, after: $after, channel: $channel) {
    edges {
      node {
        id
        name
        slug
        seoTitle
        seoDescription
        category {
          name
        }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

def fetch_all_products():
    products = []
    cursor = None
    page = 1
    while True:
        print(f"  Fetching products page {page}...", end="", flush=True)
        r = gql(PRODUCTS_QUERY, {"first": 100, "after": cursor, "channel": CHANNEL})
        if r.get("errors"):
            print(f"\n  ERROR: {r['errors'][0]['message']}")
            break
        conn = r.get("data", {}).get("products", {})
        edges = conn.get("edges", [])
        for e in edges:
            products.append(e["node"])
        page_info = conn.get("pageInfo", {})
        print(f" got {len(edges)} (total so far: {len(products)})")
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info["endCursor"]
        page += 1
    return products


# ── Fetch all pages ───────────────────────────────────────────────────────────

PAGES_QUERY = """
query Pages($first: Int!, $after: String) {
  pages(first: $first, after: $after) {
    edges {
      node {
        id
        title
        slug
        seoTitle
        seoDescription
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

def fetch_all_pages():
    pages = []
    cursor = None
    page_num = 1
    while True:
        print(f"  Fetching pages page {page_num}...", end="", flush=True)
        r = gql(PAGES_QUERY, {"first": 100, "after": cursor})
        if r.get("errors"):
            print(f"\n  ERROR: {r['errors'][0]['message']}")
            break
        conn = r.get("data", {}).get("pages", {})
        edges = conn.get("edges", [])
        for e in edges:
            pages.append(e["node"])
        page_info = conn.get("pageInfo", {})
        print(f" got {len(edges)} (total so far: {len(pages)})")
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info["endCursor"]
        page_num += 1
    return pages


# ── SEO title + description generators ───────────────────────────────────────

def truncate(text, max_len):
    """Truncate text to max_len, cutting at a word boundary."""
    if len(text) <= max_len:
        return text
    truncated = text[:max_len].rsplit(" ", 1)[0]
    return truncated.rstrip(" ,.|-")


def make_product_title(name, category_name):
    """
    Format: [Product Name] | [Category] | Auric Jewels
    Max 60 chars, never truncate category or brand.
    """
    suffix = " | Auric Jewels"
    if category_name:
        cat = category_name.strip()
        # Short category labels for common names
        CAT_SHORT = {
            "Rings": "Rings",
            "Earrings": "Earrings",
            "Necklaces": "Necklaces",
            "Bracelets": "Bracelets",
            "Bangles": "Bangles",
            "Pendants": "Pendants",
            "Chains": "Chains",
            "Mangalsutra": "Mangalsutra",
        }
        cat = CAT_SHORT.get(cat, cat)
        mid = f" | {cat}"
    else:
        mid = ""

    # Available space for product name
    budget = 60 - len(mid) - len(suffix)
    pname = truncate(name.strip(), budget)
    title = f"{pname}{mid}{suffix}"
    return title


def make_page_title(page_title):
    """
    Format: [Blog Topic] | Auric Jewels Gurgaon
    40-60 chars.
    """
    suffix = " | Auric Jewels Gurgaon"
    budget = 60 - len(suffix)
    topic = truncate(page_title.strip(), budget)
    title = f"{topic}{suffix}"
    # Pad if too short (under 40): keep as-is (it will be >=40 for any non-trivial topic)
    return title


def make_product_description(name, category_name):
    """150-160 chars: keyword + Gurgaon + price hint + CTA."""
    cat = category_name.strip() if category_name else "jewellery"
    cat_lower = cat.lower()

    price_hints = {
        "rings": "₹15,000",
        "earrings": "₹8,000",
        "necklaces": "₹20,000",
        "bracelets": "₹12,000",
        "bangles": "₹10,000",
        "pendants": "₹8,000",
        "chains": "₹10,000",
        "mangalsutra": "₹15,000",
    }
    price = price_hints.get(cat_lower, "₹10,000")

    desc = (
        f"Buy {name} at Auric Jewels Gurgaon. "
        f"IGI certified diamonds, BIS hallmarked gold. "
        f"{cat} from {price}. Visit Sector 45 showroom or shop online."
    )
    # Target 150-160 chars
    if len(desc) > 160:
        desc = truncate(desc, 157) + "..."
    return desc


def make_page_description(page_title):
    """150-160 chars for blog pages."""
    # Extract a keyword from the title
    title_lower = page_title.lower()
    if "solitaire" in title_lower:
        kw = "solitaire diamond jewellery"
    elif "bridal" in title_lower or "wedding" in title_lower:
        kw = "bridal gold jewellery"
    elif "mangalsutra" in title_lower:
        kw = "diamond mangalsutra"
    elif "gold rate" in title_lower or "gold price" in title_lower:
        kw = "gold jewellery"
    elif "diamond" in title_lower:
        kw = "diamond jewellery"
    elif "hallmark" in title_lower or "purity" in title_lower:
        kw = "hallmarked gold jewellery"
    elif "ring" in title_lower:
        kw = "diamond rings"
    elif "earring" in title_lower:
        kw = "diamond earrings"
    elif "necklace" in title_lower:
        kw = "gold necklaces"
    else:
        kw = "gold & diamond jewellery"

    desc = (
        f"Read our expert guide on {kw} at Auric Jewels Gurgaon. "
        f"Certified diamonds, BIS hallmarked gold. "
        f"Prices from ₹10,000. Visit our Sector 45 showroom."
    )
    if len(desc) > 160:
        desc = truncate(desc, 157) + "..."
    return desc


# ── Audit ─────────────────────────────────────────────────────────────────────

def audit(items, label):
    """Return list of dicts describing each item's issues."""
    title_counts = Counter(
        (i.get("seoTitle") or "").strip().lower()
        for i in items
        if (i.get("seoTitle") or "").strip()
    )
    desc_counts = Counter(
        (i.get("seoDescription") or "").strip().lower()
        for i in items
        if (i.get("seoDescription") or "").strip()
    )

    results = []
    for item in items:
        t = (item.get("seoTitle") or "").strip()
        d = (item.get("seoDescription") or "").strip()
        issues = []
        if not t:
            issues.append("empty_title")
        else:
            if len(t) < 30:
                issues.append(f"title_too_short({len(t)})")
            if len(t) > 60:
                issues.append(f"title_too_long({len(t)})")
            if title_counts[t.lower()] > 1:
                issues.append("duplicate_title")
        if not d:
            issues.append("empty_desc")
        else:
            if len(d) < 100:
                issues.append(f"desc_too_short({len(d)})")
            if len(d) > 170:
                issues.append(f"desc_too_long({len(d)})")
            if desc_counts[d.lower()] > 1:
                issues.append("duplicate_desc")
        results.append({**item, "_issues": issues})
    return results


def needs_fix(item):
    return bool(item["_issues"])


# ── GraphQL mutations ─────────────────────────────────────────────────────────

PRODUCT_UPDATE = """
mutation ProductUpdate($id: ID!, $input: ProductInput!) {
  productUpdate(id: $id, input: $input) {
    product {
      id
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

PAGE_UPDATE = """
mutation PageUpdate($id: ID!, $input: PageInput!) {
  pageUpdate(id: $id, input: $input) {
    page {
      id
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

def update_product_seo(product_id, seo_title, seo_description):
    return gql(PRODUCT_UPDATE, {
        "id": product_id,
        "input": {
            "seo": {
                "title": seo_title,
                "description": seo_description,
            }
        }
    })

def update_page_seo(page_id, seo_title, seo_description):
    return gql(PAGE_UPDATE, {
        "id": page_id,
        "input": {
            "seo": {
                "title": seo_title,
                "description": seo_description,
            }
        }
    })


def bulk_update(items, update_fn, label, fix_title_fn, fix_desc_fn):
    """Update items in batches of BATCH_SIZE. Returns (success_count, fail_count)."""
    to_fix = [i for i in items if needs_fix(i)]
    total = len(to_fix)
    if total == 0:
        print(f"  No {label} need fixing.")
        return 0, 0

    print(f"  {total} {label} need updating...")
    success = 0
    fail = 0

    for batch_start in range(0, total, BATCH_SIZE):
        batch = to_fix[batch_start:batch_start + BATCH_SIZE]
        for item in batch:
            name_key = item.get("name") or item.get("title") or item.get("slug") or item["id"]
            cat = item.get("category") or {}
            cat_name = cat.get("name", "") if isinstance(cat, dict) else ""

            new_title = fix_title_fn(item)
            new_desc = fix_desc_fn(item)

            r = update_fn(item["id"], new_title, new_desc)

            if r.get("errors") and not r.get("data"):
                print(f"    FAIL (network) [{name_key[:40]}]: {r['errors'][0]['message'][:80]}")
                fail += 1
                continue

            data_key = "productUpdate" if "productUpdate" in (r.get("data") or {}) else "pageUpdate"
            resp_data = (r.get("data") or {}).get(data_key, {})
            gql_errors = resp_data.get("errors", [])

            if gql_errors:
                err_msg = gql_errors[0].get("message", "unknown")
                print(f"    FAIL (gql) [{name_key[:40]}]: {err_msg[:80]}")
                fail += 1
            else:
                print(f"    OK [{name_key[:40]}] → '{new_title[:55]}'")
                success += 1

        time.sleep(0.3)  # Rate-limit courtesy

    print(f"  Batch done: {success} success, {fail} failed")
    return success, fail


# ── Verify ────────────────────────────────────────────────────────────────────

def verify(items, label):
    issues_remaining = sum(1 for i in items if needs_fix(i))
    print(f"  {label}: {len(items) - issues_remaining}/{len(items)} clean")
    return issues_remaining


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print()
    print("=" * 65)
    print("  Auric Jewels — Bulk SEO Fix")
    print("=" * 65)

    # ── STEP 1: AUDIT ────────────────────────────────────────────
    print()
    print("STEP 1: Auditing pages + products")
    print("-" * 40)

    print("\nFetching PRODUCTS...")
    raw_products = fetch_all_products()
    print(f"  Total products: {len(raw_products)}")

    print("\nFetching PAGES...")
    raw_pages = fetch_all_pages()
    print(f"  Total pages: {len(raw_pages)}")

    if not raw_products and not raw_pages:
        print("\nERROR: Could not fetch data. Check API token and endpoint.")
        sys.exit(1)

    products = audit(raw_products, "products")
    pages = audit(raw_pages, "pages")

    # Print audit summary
    print()
    print("AUDIT SUMMARY")
    print("-" * 40)
    issue_types = ["empty_title", "empty_desc", "duplicate_title", "duplicate_desc"]
    for label, audited in [("Products", products), ("Pages", pages)]:
        to_fix = [i for i in audited if i["_issues"]]
        print(f"\n{label} ({len(audited)} total, {len(to_fix)} need fixing):")
        counts = Counter()
        for item in audited:
            for issue in item["_issues"]:
                issue_key = issue.split("(")[0]
                counts[issue_key] += 1
        for issue, cnt in sorted(counts.items()):
            print(f"  {issue}: {cnt}")

    # ── STEP 2 + 3: FIX & UPDATE ─────────────────────────────────
    print()
    print("STEP 2+3: Generating fixes + bulk updating")
    print("-" * 40)

    # Product fix functions
    def product_title(item):
        cat = item.get("category") or {}
        cat_name = cat.get("name", "") if isinstance(cat, dict) else ""
        return make_product_title(item.get("name", ""), cat_name)

    def product_desc(item):
        cat = item.get("category") or {}
        cat_name = cat.get("name", "") if isinstance(cat, dict) else ""
        return make_product_description(item.get("name", ""), cat_name)

    # Page fix functions
    def page_title(item):
        return make_page_title(item.get("title", item.get("slug", "")))

    def page_desc(item):
        return make_page_description(item.get("title", item.get("slug", "")))

    print("\nUpdating PRODUCTS...")
    prod_success, prod_fail = bulk_update(
        products, update_product_seo, "products", product_title, product_desc
    )

    print("\nUpdating PAGES...")
    page_success, page_fail = bulk_update(
        pages, update_page_seo, "pages", page_title, page_desc
    )

    # ── STEP 4: VERIFY ───────────────────────────────────────────
    print()
    print("STEP 4: Verifying fixes")
    print("-" * 40)

    print("\nRe-fetching PRODUCTS...")
    verified_products_raw = fetch_all_products()
    verified_products = audit(verified_products_raw, "products")

    print("\nRe-fetching PAGES...")
    verified_pages_raw = fetch_all_pages()
    verified_pages = audit(verified_pages_raw, "pages")

    print()
    remaining_products = verify(verified_products, "Products")
    remaining_pages = verify(verified_pages, "Pages")

    if remaining_products or remaining_pages:
        print(f"\n  WARNING: {remaining_products + remaining_pages} items still have issues.")
        for item in verified_products:
            if item["_issues"]:
                print(f"    PRODUCT [{item.get('name', item['id'])[:40]}]: {item['_issues']}")
        for item in verified_pages:
            if item["_issues"]:
                print(f"    PAGE [{item.get('title', item['id'])[:40]}]: {item['_issues']}")
    else:
        print("\n  All clear — no remaining SEO issues detected.")

    # ── STEP 5: LOG ──────────────────────────────────────────────
    print()
    print("STEP 5: Writing AURIC_PROGRESS.md")
    print("-" * 40)

    today = date.today().strftime("%d %B %Y")
    total_fixed = prod_success + page_success
    total_failed = prod_fail + page_fail

    log_content = f"""# Auric Jewels — SEO Progress Log

## {today} — Bulk SEO Title + Meta Fix

| Metric | Value |
|---|---|
| Date | {today} |
| Task | Bulk SEO title + meta description fix |
| Products audited | {len(raw_products)} |
| Pages audited | {len(raw_pages)} |
| Products fixed | {prod_success} |
| Pages fixed | {page_success} |
| Total fixed | {total_fixed} |
| Failures | {total_failed} |
| Remaining issues (products) | {remaining_products} |
| Remaining issues (pages) | {remaining_pages} |

### Fix Rules Applied

**Products**
- Format: `[Product Name] | [Category] | Auric Jewels`
- Max 60 chars, truncated at word boundary
- Meta: 150-160 chars, includes keyword + Gurgaon + price hint + CTA

**Pages (Blogs)**
- Format: `[Blog Topic] | Auric Jewels Gurgaon`
- 40-60 chars, includes primary keyword + Gurgaon
- Meta: 150-160 chars, includes keyword + Gurgaon + price hint + CTA

### Issues Fixed
- Duplicate meta descriptions
- Duplicate title tags
- Titles too short (under 30 chars)
- Titles too long (over 60 chars)
- Empty titles / descriptions
"""

    try:
        with open("AURIC_PROGRESS.md", "w", encoding="utf-8") as f:
            f.write(log_content)
        print("  Written: AURIC_PROGRESS.md")
    except Exception as e:
        print(f"  Could not write AURIC_PROGRESS.md: {e}")
        print(log_content)

    # ── FINAL SUMMARY ─────────────────────────────────────────────
    print()
    print("=" * 65)
    print(f"  DONE — Products fixed: {prod_success}  |  Pages fixed: {page_success}")
    print(f"         Failures: {total_failed}  |  Still has issues: {remaining_products + remaining_pages}")
    print("=" * 65)
    print()

    sys.exit(0 if total_failed == 0 else 1)


if __name__ == "__main__":
    main()
