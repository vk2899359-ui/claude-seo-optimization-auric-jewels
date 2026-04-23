#!/usr/bin/env python3
"""
Assign products to collections on auricjewels.com via Saleor GraphQL API.

Actual store collections (discovered from live API):
  Anniversary Collection, Best Seller, Bracelets, Earrings, Featured Products,
  Flash Sale, For Her, For Him, Necklaces, New Arrivals, Solitaire Collection,
  Top Products, Trendy Styles, Valentine Collection

Mapping rules (category matching is partial/case-insensitive):
  Necklaces           → category contains necklace / mangalsutra / chain / pendant
  Earrings            → category contains earring
  Bracelets           → category contains bracelet / bangle
  Solitaire Collection→ "solitaire" in name/description
  For Her             → category contains necklace / earring / bangle / mangalsutra / bracelet
  For Him             → category contains ring / bracelet / chain; or "men"/"gents" in text
  Anniversary Collection → "diamond" in text + ring/necklace/pendant category
  Valentine Collection→ heart/love/valentine/couple/solitaire in text
  Featured Products   → "diamond" in name/description
  Best Seller         → "gold" in name/description
  Top Products        → category contains necklace / ring / earring / bangle / bracelet
  Trendy Styles       → trendy/modern/fashion/lightweight keywords OR earring/bracelet category
  Flash Sale          → skipped (needs price/sale logic)
  New Arrivals        → skipped (needs date-based filtering)
"""

import os
import sys
import json
import time
import requests

GRAPHQL_URL = os.getenv("SALEOR_URL", "https://auric.thecodemesh.online/graphql/")
AUTH_TOKEN = os.getenv("SALEOR_TOKEN", "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb")
CHANNEL = os.getenv("SALEOR_CHANNEL", "franchise1")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AUTH_TOKEN}",
}


def gql(query: str, variables: dict = None) -> dict:
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    resp = requests.post(GRAPHQL_URL, headers=HEADERS, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {json.dumps(data['errors'], indent=2)}")
    return data["data"]


# ---------------------------------------------------------------------------
# Step 1: Fetch all collections
# ---------------------------------------------------------------------------

COLLECTIONS_QUERY = """
query GetCollections($after: String) {
  collections(first: 100, after: $after, channel: "%s") {
    pageInfo { hasNextPage endCursor }
    edges { node { id name } }
  }
}
""" % CHANNEL


def fetch_all_collections() -> list[dict]:
    collections = []
    after = None
    while True:
        data = gql(COLLECTIONS_QUERY, {"after": after})
        page = data["collections"]
        for edge in page["edges"]:
            collections.append(edge["node"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]
    return collections


# ---------------------------------------------------------------------------
# Step 2: Fetch all products with category and description
# ---------------------------------------------------------------------------

PRODUCTS_QUERY = """
query GetProducts($after: String) {
  products(first: 100, after: $after, channel: "%s") {
    pageInfo { hasNextPage endCursor }
    edges {
      node {
        id
        name
        description
        category { id name }
      }
    }
  }
}
""" % CHANNEL


def fetch_all_products() -> list[dict]:
    products = []
    after = None
    while True:
        data = gql(PRODUCTS_QUERY, {"after": after})
        page = data["products"]
        for edge in page["edges"]:
            products.append(edge["node"])
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]
    return products


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def product_text(p: dict) -> str:
    """Lower-cased name + description text for keyword matching."""
    desc = ""
    if p.get("description"):
        try:
            desc_data = json.loads(p["description"])
            for block in desc_data.get("blocks", []):
                desc += " " + block.get("data", {}).get("text", "")
        except (json.JSONDecodeError, TypeError):
            desc = str(p["description"])
    return (p["name"] + " " + desc).lower()


def cat(p: dict) -> str:
    return (p.get("category") or {}).get("name", "").lower()


def cat_has(p: dict, *keywords: str) -> bool:
    c = cat(p)
    return any(k in c for k in keywords)


def text_has(text: str, *keywords: str) -> bool:
    return any(k in text for k in keywords)


# ---------------------------------------------------------------------------
# Step 3: Build mapping  {collection_id: [product_id, ...]}
# ---------------------------------------------------------------------------

def build_collection_product_map(
    collections: list[dict], products: list[dict]
) -> dict[str, list[str]]:
    # lowercase name → id
    coll_by_name: dict[str, str] = {c["name"].lower(): c["id"] for c in collections}
    result: dict[str, list[str]] = {c["id"]: [] for c in collections}

    # Print discovered categories for transparency
    unique_cats = sorted({cat(p) for p in products if cat(p)})
    print(f"  Discovered {len(unique_cats)} product categories:")
    for uc in unique_cats:
        print(f"    • {uc}")

    def add(collection_name_lower: str, product_id: str):
        cid = coll_by_name.get(collection_name_lower)
        if cid and product_id not in result[cid]:
            result[cid].append(product_id)

    for p in products:
        pid = p["id"]
        text = product_text(p)

        # Necklaces — necklace / mangalsutra / chain / pendant categories
        if cat_has(p, "necklace", "mangalsutra", "chain", "pendant"):
            add("necklaces", pid)

        # Earrings — earring category
        if cat_has(p, "earring"):
            add("earrings", pid)

        # Bracelets — bracelet / bangle category
        if cat_has(p, "bracelet", "bangle"):
            add("bracelets", pid)

        # Solitaire Collection — "solitaire" in name/description
        if text_has(text, "solitaire"):
            add("solitaire collection", pid)

        # For Her — feminine jewelry categories
        if cat_has(p, "necklace", "earring", "bangle", "mangalsutra", "bracelet", "pendant"):
            add("for her", pid)

        # For Him — rings, chains, bracelets, or explicitly for men
        if cat_has(p, "ring", "bracelet", "chain") or text_has(text, " men", "gents", "for him", "mens"):
            add("for him", pid)

        # Anniversary Collection — diamond jewelry in premium categories
        if text_has(text, "diamond") and cat_has(p, "ring", "necklace", "pendant", "earring"):
            add("anniversary collection", pid)

        # Valentine Collection — romantic / heart / love themes or solitaire
        if text_has(text, "heart", "love", "valentine", "couple", "solitaire", "romantic"):
            add("valentine collection", pid)

        # Featured Products — any diamond jewelry
        if text_has(text, "diamond"):
            add("featured products", pid)

        # Best Seller — gold jewelry (most popular material)
        if text_has(text, "gold"):
            add("best seller", pid)

        # Top Products — main jewelry categories
        if cat_has(p, "necklace", "ring", "earring", "bangle", "bracelet", "pendant", "mangalsutra"):
            add("top products", pid)

        # Trendy Styles — fashion/modern keywords OR earrings/bracelets (fast-fashion items)
        if text_has(text, "trendy", "modern", "contemporary", "fashion", "stylish",
                    "lightweight", "daily wear", "casual"):
            add("trendy styles", pid)
        elif cat_has(p, "earring", "bracelet", "bangle"):
            add("trendy styles", pid)

        # Flash Sale — skipped (needs price/sale logic)
        # New Arrivals — skipped (needs date-based filtering)

    return result


# ---------------------------------------------------------------------------
# Step 4: Assign products via collectionAddProducts mutation
# ---------------------------------------------------------------------------

ADD_PRODUCTS_MUTATION = """
mutation CollectionAddProducts($collectionId: ID!, $productIds: [ID!]!) {
  collectionAddProducts(collectionId: $collectionId, products: $productIds) {
    collection { id name }
    errors { field message code }
  }
}
"""

BATCH_SIZE = 100


def assign_products_to_collection(collection_id: str, product_ids: list[str]) -> int:
    assigned = 0
    for i in range(0, len(product_ids), BATCH_SIZE):
        batch = product_ids[i : i + BATCH_SIZE]
        data = gql(ADD_PRODUCTS_MUTATION, {"collectionId": collection_id, "productIds": batch})
        errors = data["collectionAddProducts"]["errors"]
        if errors:
            print(f"    [WARN] batch {i//BATCH_SIZE + 1} errors: {errors}", file=sys.stderr)
        else:
            assigned += len(batch)
        time.sleep(0.1)
    return assigned


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=== Auric Jewels — Assign Products to Collections ===\n")

    print("Step 1: Fetching collections...")
    collections = fetch_all_collections()
    print(f"  Found {len(collections)} collection(s):")
    for c in collections:
        print(f"    [{c['id']}] {c['name']}")

    print("\nStep 2: Fetching products...")
    products = fetch_all_products()
    print(f"  Found {len(products)} product(s)")

    print("\nStep 3: Applying mapping rules...")
    coll_product_map = build_collection_product_map(collections, products)

    coll_name_map = {c["id"]: c["name"] for c in collections}

    print("\nStep 4: Assigning products to collections...")
    summary = []
    skipped = ["flash sale", "new arrivals"]
    for cid, pids in coll_product_map.items():
        cname = coll_name_map[cid]
        if cname.lower() in skipped:
            print(f"  {cname}: skipped (needs price/date logic)")
            summary.append((cname, 0, "skipped"))
            continue
        if not pids:
            print(f"  {cname}: 0 products matched — skipping")
            summary.append((cname, 0, "no match"))
            continue
        print(f"  {cname}: assigning {len(pids)} product(s)...")
        assigned = assign_products_to_collection(cid, pids)
        summary.append((cname, assigned, "done"))

    print("\n" + "=" * 55)
    print("Step 5: Summary")
    print("=" * 55)
    total = 0
    for cname, count, status in sorted(summary, key=lambda x: -x[1]):
        flag = "" if status == "done" else f"  [{status}]"
        print(f"  {cname:<28} {count:>5} product(s){flag}")
        total += count
    print("-" * 55)
    print(f"  {'TOTAL':<28} {total:>5} assignment(s)")
    print("=" * 55)


if __name__ == "__main__":
    main()
