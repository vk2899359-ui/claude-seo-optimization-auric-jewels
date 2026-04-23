#!/usr/bin/env python3
"""
Assign products to collections on auricjewels.com via Saleor GraphQL API.

Mapping rules:
- Bridal Jewellery     → Necklaces, Rings, Bangles, Earrings categories
- Diamond Rings        → Rings category + "diamond" in name/description
- Gold Necklaces       → Necklaces category + "gold" in name
- Mangalsutra          → "mangalsutra" in name
- Gold Bangles         → all Bangles category products
- Diamond Earrings     → Earrings category + "diamond" in name/description
- Solitaire Rings      → "solitaire" in name
"""

import sys
import json
import time
import requests

GRAPHQL_URL = "https://auric.thecodemesh.online/graphql/"
AUTH_TOKEN = "rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"
CHANNEL = "franchise1"

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
    edges {
      node {
        id
        name
      }
    }
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
# Step 2: Fetch all products with category and descriptions
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
        category {
          id
          name
        }
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
# Step 3: Apply mapping rules
# ---------------------------------------------------------------------------

BRIDAL_CATEGORIES = {"necklaces", "rings", "bangles", "earrings"}


def product_text(p: dict) -> str:
    """Return a lower-cased combined text of name + description for keyword matching."""
    desc = ""
    if p.get("description"):
        try:
            # Saleor stores description as Editorjs JSON
            desc_data = json.loads(p["description"])
            for block in desc_data.get("blocks", []):
                desc += " " + block.get("data", {}).get("text", "")
        except (json.JSONDecodeError, TypeError):
            desc = str(p["description"])
    return (p["name"] + " " + desc).lower()


def category_name(p: dict) -> str:
    return (p.get("category") or {}).get("name", "").lower()


def build_collection_product_map(
    collections: list[dict], products: list[dict]
) -> dict[str, list[str]]:
    """
    Returns {collection_id: [product_id, ...]} based on mapping rules.
    """
    # Build collection name → id lookup (lower-cased for matching)
    coll_by_name: dict[str, str] = {c["name"].lower(): c["id"] for c in collections}

    result: dict[str, list[str]] = {c["id"]: [] for c in collections}

    def add(collection_name_lower: str, product_id: str):
        cid = coll_by_name.get(collection_name_lower)
        if cid:
            result[cid].append(product_id)

    for p in products:
        pid = p["id"]
        cat = category_name(p)
        text = product_text(p)

        # Bridal Jewellery — products from Necklaces, Rings, Bangles, Earrings
        if cat in BRIDAL_CATEGORIES:
            add("bridal jewellery", pid)

        # Diamond Rings — Rings category + "diamond" keyword
        if cat == "rings" and "diamond" in text:
            add("diamond rings", pid)

        # Gold Necklaces — Necklaces category + "gold" keyword
        if cat == "necklaces" and "gold" in text:
            add("gold necklaces", pid)

        # Mangalsutra — "mangalsutra" in name/description
        if "mangalsutra" in text:
            add("mangalsutra", pid)

        # Gold Bangles — all Bangles category
        if cat == "bangles":
            add("gold bangles", pid)

        # Diamond Earrings — Earrings category + "diamond" keyword
        if cat == "earrings" and "diamond" in text:
            add("diamond earrings", pid)

        # Solitaire Rings — "solitaire" in name/description
        if "solitaire" in text:
            add("solitaire rings", pid)

    return result


# ---------------------------------------------------------------------------
# Step 4: Assign products via collectionAddProducts mutation
# ---------------------------------------------------------------------------

ADD_PRODUCTS_MUTATION = """
mutation CollectionAddProducts($collectionId: ID!, $productIds: [ID!]!) {
  collectionAddProducts(collectionId: $collectionId, products: $productIds) {
    collection {
      id
      name
    }
    errors {
      field
      message
      code
    }
  }
}
"""

BATCH_SIZE = 100  # Saleor handles up to 100 IDs per mutation call


def assign_products_to_collection(collection_id: str, product_ids: list[str]) -> int:
    """Assign products in batches; returns total assigned count."""
    assigned = 0
    for i in range(0, len(product_ids), BATCH_SIZE):
        batch = product_ids[i : i + BATCH_SIZE]
        data = gql(ADD_PRODUCTS_MUTATION, {"collectionId": collection_id, "productIds": batch})
        errors = data["collectionAddProducts"]["errors"]
        if errors:
            print(f"  [WARN] Errors assigning batch: {errors}", file=sys.stderr)
        else:
            assigned += len(batch)
        time.sleep(0.1)  # gentle rate limiting
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

    # Build id → name for reporting
    coll_name_map = {c["id"]: c["name"] for c in collections}

    print("\nStep 4: Assigning products to collections...\n")
    summary = []
    for cid, pids in coll_product_map.items():
        cname = coll_name_map[cid]
        if not pids:
            print(f"  {cname}: 0 products matched — skipping")
            summary.append((cname, 0))
            continue
        print(f"  {cname}: assigning {len(pids)} product(s)...")
        assigned = assign_products_to_collection(cid, pids)
        summary.append((cname, assigned))

    print("\n" + "=" * 50)
    print("Step 5: Summary")
    print("=" * 50)
    total = 0
    for cname, count in sorted(summary, key=lambda x: -x[1]):
        print(f"  {cname:<25} {count:>4} product(s) assigned")
        total += count
    print("-" * 50)
    print(f"  {'TOTAL':<25} {total:>4} assignment(s)")
    print("=" * 50)


if __name__ == "__main__":
    main()
