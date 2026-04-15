"""
Auric Jewels — Fetch Ring Products & Auto-Generate Attributes
==============================================================

USAGE:
    python3 scripts/fetch-rings-products.py              # Fetch first 10, preview
    python3 scripts/fetch-rings-products.py --all         # Fetch ALL, save CSV
    python3 scripts/fetch-rings-products.py --all --update # Fetch ALL, save CSV, update via API

This script:
  1. Connects to Saleor GraphQL API
  2. Finds the "rings" category
  3. Fetches all products with name, price, attributes, images
  4. Auto-generates missing attributes based on business rules
  5. Saves everything to CSV
"""

import json
import csv
import os
import sys
import re
import math
import urllib.request
import urllib.error

# ── Configuration ────────────────────────────────────────────
API_ENDPOINT = "https://auric.thecodemesh.online/graphql/"
AUTH_TOKEN = "fAPR16BVrzI4thcLtj8c4tUUG1wGU6"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_CSV = os.path.join(PROJECT_DIR, "data", "rings-products-attributes.csv")

# Gold rates per gram (for weight estimation)
GOLD_RATE_22K = 7800  # INR per gram
GOLD_RATE_18K = 6800  # INR per gram
MAKING_CHARGE_FACTOR = 0.7  # ~30% is making + diamond charges


# ── GraphQL Helper ───────────────────────────────────────────

def graphql_request(query, variables=None):
    """Send a GraphQL request and return the parsed JSON response."""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_ENDPOINT,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AUTH_TOKEN}",
        },
        method="POST",
    )

    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  [ERROR] HTTP {e.code}: {body[:300]}")
        return None
    except Exception as e:
        print(f"  [ERROR] {e}")
        return None


# ── Step 1: Find the "rings" category ────────────────────────

def find_rings_category():
    """Find the rings category ID from Saleor."""
    print("\n[1/4] Searching for 'rings' category...")
    query = """
    {
      categories(first: 100, filter: { search: "ring" }) {
        edges {
          node {
            id
            name
            slug
            productsCount: products(first: 0) { totalCount }
          }
        }
      }
    }
    """
    result = graphql_request(query)
    if not result or "errors" in result:
        # Fallback: fetch all categories
        print("  Search filter not supported, fetching all categories...")
        query_all = """
        {
          categories(first: 100) {
            edges {
              node {
                id
                name
                slug
              }
            }
          }
        }
        """
        result = graphql_request(query_all)

    if not result or "data" not in result:
        print("  [FAIL] Could not fetch categories.")
        return None

    categories = result["data"]["categories"]["edges"]
    for cat in categories:
        node = cat["node"]
        if node["slug"] == "rings" or "ring" in node["name"].lower():
            print(f"  Found: {node['name']} (slug={node['slug']}, id={node['id']})")
            return node["id"]

    # List available categories for debugging
    print("  [WARN] 'rings' category not found. Available categories:")
    for cat in categories:
        print(f"    - {cat['node']['name']} (slug={cat['node']['slug']})")
    return None


# ── Step 2: Fetch products from category ─────────────────────

PRODUCTS_QUERY = """
query FetchRingProducts($categoryId: ID!, $first: Int!, $after: String) {
  products(
    filter: { categories: [$categoryId] }
    first: $first
    after: $after
    channel: "default-channel"
  ) {
    totalCount
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        name
        slug
        description
        pricing {
          priceRange {
            start {
              gross {
                amount
                currency
              }
            }
            stop {
              gross {
                amount
                currency
              }
            }
          }
        }
        attributes {
          attribute {
            id
            name
            slug
          }
          values {
            id
            name
            slug
          }
        }
        media {
          url
          alt
          type
        }
        category {
          name
          slug
        }
        productType {
          name
        }
      }
    }
  }
}
"""

# Fallback query without channel parameter (older Saleor versions)
PRODUCTS_QUERY_NO_CHANNEL = """
query FetchRingProducts($categoryId: ID!, $first: Int!, $after: String) {
  products(
    filter: { categories: [$categoryId] }
    first: $first
    after: $after
  ) {
    totalCount
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        name
        slug
        description
        pricing {
          priceRange {
            start {
              gross {
                amount
                currency
              }
            }
            stop {
              gross {
                amount
                currency
              }
            }
          }
        }
        attributes {
          attribute {
            id
            name
            slug
          }
          values {
            id
            name
            slug
          }
        }
        media {
          url
          alt
          type
        }
        category {
          name
          slug
        }
        productType {
          name
        }
      }
    }
  }
}
"""


def fetch_products(category_id, limit=10, fetch_all=False):
    """Fetch products from the rings category."""
    print(f"\n[2/4] Fetching {'ALL' if fetch_all else f'first {limit}'} ring products...")

    all_products = []
    cursor = None
    page = 1
    page_size = min(limit, 100) if not fetch_all else 100

    while True:
        variables = {
            "categoryId": category_id,
            "first": page_size,
            "after": cursor,
        }

        # Try with channel first, fallback without
        result = graphql_request(PRODUCTS_QUERY, variables)
        if result and "errors" in result:
            print("  Retrying without channel parameter...")
            result = graphql_request(PRODUCTS_QUERY_NO_CHANNEL, variables)

        if not result or "data" not in result:
            print("  [FAIL] Could not fetch products.")
            break

        products_data = result["data"]["products"]
        total = products_data.get("totalCount", "?")
        edges = products_data["edges"]

        print(f"  Page {page}: fetched {len(edges)} products (total in category: {total})")

        for edge in edges:
            product = parse_product(edge["node"])
            all_products.append(product)

        if not fetch_all and len(all_products) >= limit:
            all_products = all_products[:limit]
            break

        if not products_data["pageInfo"]["hasNextPage"]:
            break

        cursor = products_data["pageInfo"]["endCursor"]
        page += 1

    print(f"  Total fetched: {len(all_products)} products")
    return all_products


def parse_product(node):
    """Parse a product node into a flat dict."""
    # Extract price
    price = 0
    currency = "INR"
    pricing = node.get("pricing")
    if pricing and pricing.get("priceRange"):
        price_start = pricing["priceRange"]["start"]
        if price_start and price_start.get("gross"):
            price = price_start["gross"]["amount"]
            currency = price_start["gross"]["currency"]

    # Extract existing attributes
    attributes = {}
    for attr in node.get("attributes", []):
        attr_name = attr["attribute"]["name"]
        attr_values = [v["name"] for v in attr.get("values", [])]
        attributes[attr_name] = ", ".join(attr_values) if attr_values else ""

    # Extract images
    images = []
    for media in node.get("media", []):
        if media.get("url"):
            images.append(media["url"])

    # Extract description text
    description = ""
    desc_raw = node.get("description", "")
    if desc_raw:
        if isinstance(desc_raw, str):
            try:
                desc_json = json.loads(desc_raw)
                # Saleor stores description as EditorJS JSON
                if isinstance(desc_json, dict) and "blocks" in desc_json:
                    texts = []
                    for block in desc_json["blocks"]:
                        if "data" in block and "text" in block["data"]:
                            texts.append(block["data"]["text"])
                    description = " ".join(texts)
                else:
                    description = desc_raw
            except (json.JSONDecodeError, KeyError):
                description = desc_raw

    return {
        "id": node["id"],
        "name": node["name"],
        "slug": node.get("slug", ""),
        "price": price,
        "currency": currency,
        "category": node.get("category", {}).get("name", "") if node.get("category") else "",
        "product_type": node.get("productType", {}).get("name", "") if node.get("productType") else "",
        "description": description,
        "existing_attributes": attributes,
        "images": images,
        "image_count": len(images),
        "first_image": images[0] if images else "",
    }


# ── Step 3: Auto-generate missing attributes ─────────────────

def generate_attributes(product):
    """Auto-generate missing attribute data based on business rules."""
    name = product["name"]
    price = float(product["price"])
    name_lower = name.lower()
    existing = product.get("existing_attributes", {})

    generated = {}

    # 1. KARAT
    if not find_existing_attr(existing, ["karat", "gold karat", "purity", "gold purity"]):
        if price < 50000:
            generated["Karat"] = "18K Gold"
        else:
            generated["Karat"] = "22K Gold"
    else:
        generated["Karat"] = find_existing_attr(existing, ["karat", "gold karat", "purity", "gold purity"])

    is_22k = "22K" in generated["Karat"] or "22k" in generated["Karat"]
    gold_rate = GOLD_RATE_22K if is_22k else GOLD_RATE_18K

    # 2. GROSS WEIGHT
    if not find_existing_attr(existing, ["gross weight", "weight", "gold weight"]):
        if price > 0:
            weight = (price * MAKING_CHARGE_FACTOR) / gold_rate
            generated["Gross Weight"] = f"{weight:.2f} grams"
        else:
            generated["Gross Weight"] = "N/A"
    else:
        generated["Gross Weight"] = find_existing_attr(existing, ["gross weight", "weight", "gold weight"])

    # 3. DIAMOND CARAT
    if not find_existing_attr(existing, ["diamond carat", "diamond weight", "stone weight", "carat"]):
        if "solitaire" in name_lower:
            generated["Diamond Carat"] = "0.50-1.00 ct"
        elif price > 80000:
            generated["Diamond Carat"] = "0.25-0.50 ct"
        elif price >= 40000:
            generated["Diamond Carat"] = "0.10-0.25 ct"
        else:
            generated["Diamond Carat"] = "0.05-0.10 ct"
    else:
        generated["Diamond Carat"] = find_existing_attr(existing, ["diamond carat", "diamond weight", "stone weight", "carat"])

    # 4. DIAMOND CLARITY
    if not find_existing_attr(existing, ["diamond clarity", "clarity"]):
        generated["Diamond Clarity"] = "VS-SI"
    else:
        generated["Diamond Clarity"] = find_existing_attr(existing, ["diamond clarity", "clarity"])

    # 5. DIAMOND COLOR
    if not find_existing_attr(existing, ["diamond color", "diamond colour", "color", "colour"]):
        generated["Diamond Color"] = "G-H"
    else:
        generated["Diamond Color"] = find_existing_attr(existing, ["diamond color", "diamond colour", "color", "colour"])

    # 6. DIAMOND CUT
    if not find_existing_attr(existing, ["diamond cut", "cut"]):
        if "princess" in name_lower:
            generated["Diamond Cut"] = "Princess Cut"
        elif "emerald" in name_lower and "cut" in name_lower:
            generated["Diamond Cut"] = "Emerald Cut"
        elif "oval" in name_lower:
            generated["Diamond Cut"] = "Oval Cut"
        elif "pear" in name_lower:
            generated["Diamond Cut"] = "Pear Cut"
        elif "cushion" in name_lower:
            generated["Diamond Cut"] = "Cushion Cut"
        elif "marquise" in name_lower:
            generated["Diamond Cut"] = "Marquise Cut"
        elif "heart" in name_lower:
            generated["Diamond Cut"] = "Heart Cut"
        else:
            generated["Diamond Cut"] = "Round Brilliant"
    else:
        generated["Diamond Cut"] = find_existing_attr(existing, ["diamond cut", "cut"])

    # 7. HALLMARK
    if not find_existing_attr(existing, ["hallmark", "bis hallmark"]):
        if is_22k:
            generated["Hallmark"] = "BIS 916 Hallmarked"
        else:
            generated["Hallmark"] = "BIS 750 Hallmarked"
    else:
        generated["Hallmark"] = find_existing_attr(existing, ["hallmark", "bis hallmark"])

    # 8. STONE TYPE
    if not find_existing_attr(existing, ["stone type", "stone", "gemstone"]):
        if "ruby" in name_lower:
            generated["Stone Type"] = "Natural Ruby"
        elif "emerald" in name_lower and "cut" not in name_lower:
            generated["Stone Type"] = "Natural Emerald"
        elif "sapphire" in name_lower:
            generated["Stone Type"] = "Natural Sapphire"
        elif "pearl" in name_lower:
            generated["Stone Type"] = "Natural Pearl"
        elif "tanzanite" in name_lower:
            generated["Stone Type"] = "Natural Tanzanite"
        elif "topaz" in name_lower:
            generated["Stone Type"] = "Natural Topaz"
        elif "amethyst" in name_lower:
            generated["Stone Type"] = "Natural Amethyst"
        else:
            generated["Stone Type"] = "Natural Diamond"
    else:
        generated["Stone Type"] = find_existing_attr(existing, ["stone type", "stone", "gemstone"])

    # 9. CERTIFICATE
    if not find_existing_attr(existing, ["certificate", "certification"]):
        if "solitaire" in name_lower:
            generated["Certificate"] = "IGI Certified"
        else:
            generated["Certificate"] = "Auric Jewels Certificate"
    else:
        generated["Certificate"] = find_existing_attr(existing, ["certificate", "certification"])

    return generated


def find_existing_attr(attributes, possible_keys):
    """Check if any of the possible keys exist in the attributes dict (case-insensitive)."""
    for key in possible_keys:
        for attr_name, attr_val in attributes.items():
            if attr_name.lower().strip() == key.lower().strip():
                if attr_val and attr_val.strip():
                    return attr_val.strip()
    return None


# ── Step 4: Display & Save ────────────────────────────────────

def display_products(products, generated_attrs_list):
    """Display product data in a formatted table."""
    print("\n" + "=" * 120)
    print("RING PRODUCTS — AURIC JEWELS")
    print("=" * 120)

    for i, (product, gen_attrs) in enumerate(zip(products, generated_attrs_list)):
        print(f"\n{'─' * 100}")
        print(f"  #{i+1}  {product['name']}")
        print(f"{'─' * 100}")
        print(f"  ID:           {product['id']}")
        print(f"  Slug:         {product['slug']}")
        print(f"  Price:        ₹{product['price']:,.0f} {product['currency']}")
        print(f"  Category:     {product['category']}")
        print(f"  Product Type: {product['product_type']}")
        print(f"  Images:       {product['image_count']} image(s)")
        if product['first_image']:
            print(f"  First Image:  {product['first_image']}")

        # Show existing attributes
        if product['existing_attributes']:
            print(f"\n  Existing Attributes:")
            for k, v in product['existing_attributes'].items():
                print(f"    {k}: {v}")
        else:
            print(f"\n  Existing Attributes: (none)")

        # Show generated attributes
        print(f"\n  Generated/Final Attributes:")
        for k, v in gen_attrs.items():
            print(f"    {k}: {v}")

    print(f"\n{'=' * 120}")
    print(f"Total: {len(products)} products")
    print(f"{'=' * 120}")


def save_to_csv(products, generated_attrs_list, filepath):
    """Save all product data and attributes to CSV."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Collect all existing attribute keys
    all_existing_keys = set()
    for p in products:
        all_existing_keys.update(p.get("existing_attributes", {}).keys())
    all_existing_keys = sorted(all_existing_keys)

    # Generated attribute keys (fixed order)
    gen_keys = [
        "Karat", "Gross Weight", "Diamond Carat", "Diamond Clarity",
        "Diamond Color", "Diamond Cut", "Hallmark", "Stone Type", "Certificate"
    ]

    # CSV headers
    headers = [
        "S.No", "Product ID", "Product Name", "Slug", "Price (INR)", "Currency",
        "Category", "Product Type", "Image Count", "First Image URL",
    ]
    # Add existing attribute columns
    for key in all_existing_keys:
        headers.append(f"[Existing] {key}")
    # Add generated attribute columns
    for key in gen_keys:
        headers.append(f"[Generated] {key}")

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for i, (product, gen_attrs) in enumerate(zip(products, generated_attrs_list)):
            row = [
                i + 1,
                product["id"],
                product["name"],
                product["slug"],
                product["price"],
                product["currency"],
                product["category"],
                product["product_type"],
                product["image_count"],
                product["first_image"],
            ]
            # Existing attributes
            for key in all_existing_keys:
                row.append(product.get("existing_attributes", {}).get(key, ""))
            # Generated attributes
            for key in gen_keys:
                row.append(gen_attrs.get(key, ""))

            writer.writerow(row)

    print(f"\n  CSV saved: {filepath}")
    print(f"  Rows: {len(products)} products")
    print(f"  Columns: {len(headers)}")


# ── Main ──────────────────────────────────────────────────────

def main():
    fetch_all = "--all" in sys.argv
    do_update = "--update" in sys.argv

    print("=" * 60)
    print("  AURIC JEWELS — Ring Products Attribute Generator")
    print("=" * 60)

    # Step 1: Find rings category
    category_id = find_rings_category()
    if not category_id:
        print("\n[FAIL] Could not find 'rings' category. Exiting.")
        sys.exit(1)

    # Step 2: Fetch products
    if fetch_all:
        products = fetch_products(category_id, fetch_all=True)
    else:
        products = fetch_products(category_id, limit=10)

    if not products:
        print("\n[FAIL] No products found. Exiting.")
        sys.exit(1)

    # Step 3: Generate attributes
    print(f"\n[3/4] Generating attributes for {len(products)} products...")
    generated_attrs_list = []
    for product in products:
        gen_attrs = generate_attributes(product)
        generated_attrs_list.append(gen_attrs)
    print(f"  Done. Generated 9 attributes for each product.")

    # Step 4: Display
    display_products(products, generated_attrs_list)

    # Step 5: Save to CSV
    print(f"\n[4/4] Saving to CSV...")
    save_to_csv(products, generated_attrs_list, OUTPUT_CSV)

    # Also save raw JSON for reference
    json_path = OUTPUT_CSV.replace(".csv", ".json")
    combined = []
    for p, g in zip(products, generated_attrs_list):
        entry = {**p, "generated_attributes": g}
        # Convert sets to lists for JSON serialization
        if isinstance(entry.get("existing_attributes"), dict):
            pass  # already serializable
        combined.append(entry)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)
    print(f"  JSON saved: {json_path}")

    print("\n✓ Done!")
    if not fetch_all:
        print("  Run with --all to fetch ALL ring products.")
    if do_update:
        print("\n  [TODO] API update functionality — would push attributes back to Saleor.")


if __name__ == "__main__":
    main()
