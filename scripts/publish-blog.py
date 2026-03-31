"""
Auric Jewels — Blog Publisher via JewelsCraft GraphQL API
==========================================================

USAGE (Windows PowerShell):
    python scripts/publish-blog.py

USAGE (Mac/Linux):
    python3 scripts/publish-blog.py

This script:
  1. Introspects the GraphQL schema to discover available mutations
  2. Publishes the first SEO blog article to the JewelsCraft CMS
  3. Reports the result with the published URL
"""

import json
import os
import sys
import urllib.request
import urllib.error

# ── Configuration ────────────────────────────────────────────
API_ENDPOINT = "https://auric.thecodemesh.online/graphql/"
AUTH_TOKEN = "fAPR16BVrzI4thcLtj8c4tUUG1wGU6"

BLOG = {
    "title": "Best Diamond Jewellery Showroom in Gurgaon \u2014 Why Families Trust Auric Jewels",
    "slug": "best-diamond-jewellery-showroom-gurgaon",
    "metaDescription": (
        "Looking for the best diamond jewellery showroom in Gurgaon? "
        "Auric Jewels offers certified diamonds, BIS hallmarked gold "
        "& solitaire collections. Visit our showroom."
    ),
    "contentFile": os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "content",
        "blog-01-best-diamond-jewellery-showroom-gurgaon.html",
    ),
}


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
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        print(f"  HTTP {e.code}: {e.reason}")
        if body:
            print(f"  Response: {body[:500]}")
        return None
    except urllib.error.URLError as e:
        print(f"  Connection error: {e.reason}")
        return None


def step1_introspect():
    """Discover all available mutations in the GraphQL schema."""
    print("=" * 60)
    print("STEP 1: Discovering GraphQL schema")
    print("=" * 60)
    print()

    query = """{
        __schema {
            mutationType {
                fields {
                    name
                    args {
                        name
                        type {
                            name
                            kind
                            ofType { name kind ofType { name kind } }
                        }
                    }
                    type { name kind ofType { name } }
                }
            }
            queryType {
                fields {
                    name
                    args {
                        name
                        type {
                            name
                            kind
                            ofType { name kind ofType { name kind } }
                        }
                    }
                }
            }
        }
    }"""

    result = graphql_request(query)
    if not result:
        print("  Failed to connect to API.")
        return None, None

    if "errors" in result:
        print("  GraphQL errors:")
        for err in result["errors"]:
            print(f"    - {err.get('message', err)}")
        return None, None

    schema = result.get("data", {}).get("__schema", {})

    # Print mutations
    mutations = []
    mutation_type = schema.get("mutationType")
    if mutation_type and mutation_type.get("fields"):
        print("Available MUTATIONS:")
        for field in mutation_type["fields"]:
            args = ", ".join(a["name"] for a in field.get("args", []))
            ret = field.get("type", {}).get("name") or field.get("type", {}).get("ofType", {}).get("name", "?")
            print(f"  {field['name']}({args}) -> {ret}")
            mutations.append(field)
    else:
        print("  No mutations found.")

    # Print queries (look for blog-related)
    print()
    queries = []
    query_type = schema.get("queryType")
    if query_type and query_type.get("fields"):
        print("Available QUERIES (blog/post/article related):")
        for field in query_type["fields"]:
            name_lower = field["name"].lower()
            if any(kw in name_lower for kw in ["blog", "post", "article", "page", "content"]):
                args = ", ".join(a["name"] for a in field.get("args", []))
                print(f"  {field['name']}({args})")
                queries.append(field)
        if not queries:
            print("  (none found -- showing all queries)")
            for field in query_type["fields"]:
                args = ", ".join(a["name"] for a in field.get("args", []))
                print(f"  {field['name']}({args})")

    return mutations, queries


def step2_find_input_type(type_name):
    """Get detailed fields for a GraphQL input type."""
    print()
    print(f"Inspecting input type: {type_name}")

    query = """query InspectType($name: String!) {
        __type(name: $name) {
            name
            kind
            inputFields {
                name
                type {
                    name
                    kind
                    ofType { name kind ofType { name kind } }
                }
            }
            fields {
                name
                type {
                    name
                    kind
                    ofType { name kind ofType { name kind } }
                }
            }
        }
    }"""

    result = graphql_request(query, {"name": type_name})
    if not result or "errors" in result:
        print(f"  Could not inspect type: {type_name}")
        return None

    type_info = result.get("data", {}).get("__type")
    if not type_info:
        print(f"  Type {type_name} not found")
        return None

    fields = type_info.get("inputFields") or type_info.get("fields") or []
    print(f"  Fields for {type_name}:")
    for f in fields:
        ftype = f["type"]
        type_str = ftype.get("name") or ""
        if not type_str and ftype.get("ofType"):
            inner = ftype["ofType"]
            type_str = inner.get("name") or ""
            if ftype.get("kind") == "NON_NULL":
                type_str += " (required)"
            if inner.get("kind") == "LIST":
                type_str = f"[{inner.get('ofType', {}).get('name', '?')}]"
        print(f"    {f['name']}: {type_str}")

    return fields


def step3_publish(mutations):
    """Attempt to publish the blog using discovered mutations."""
    print()
    print("=" * 60)
    print("STEP 3: Publishing blog article")
    print("=" * 60)
    print()

    # Read blog content
    content_path = BLOG["contentFile"]
    if not os.path.exists(content_path):
        print(f"  Blog content file not found: {content_path}")
        print(f"  Run this script from the project root directory.")
        return False

    with open(content_path, "r", encoding="utf-8") as f:
        blog_content = f.read()

    print(f"  Title: {BLOG['title']}")
    print(f"  Slug: {BLOG['slug']}")
    print(f"  Content: {len(blog_content)} characters")
    print()

    # Find the right mutation
    mutation_name = None
    blog_keywords = ["createblog", "createpost", "createarticle", "blogcreate",
                     "postcreate", "articlecreate", "createblogpost",
                     "publishblog", "publishpost", "addblog", "addpost"]

    if mutations:
        for m in mutations:
            if m["name"].lower() in blog_keywords:
                mutation_name = m["name"]
                break

        # If no exact match, try partial match
        if not mutation_name:
            for m in mutations:
                name_lower = m["name"].lower()
                if any(kw in name_lower for kw in ["blog", "post", "article"]):
                    mutation_name = m["name"]
                    break

    if not mutation_name:
        print("  Could not auto-detect the blog mutation.")
        print("  Trying common mutation names...")
        mutation_name = "createBlog"

    # Try multiple mutation patterns
    mutation_patterns = [
        # Pattern 1: Input object
        {
            "name": "input object",
            "query": f"""mutation CreateBlog($input: CreateBlogInput!) {{
                {mutation_name}(input: $input) {{
                    id
                    slug
                    title
                }}
            }}""",
            "variables": {
                "input": {
                    "title": BLOG["title"],
                    "slug": BLOG["slug"],
                    "content": blog_content,
                    "metaDescription": BLOG["metaDescription"],
                    "status": "published",
                }
            },
        },
        # Pattern 2: Direct args
        {
            "name": "direct args",
            "query": f"""mutation {{
                {mutation_name}(
                    title: {json.dumps(BLOG["title"])},
                    slug: {json.dumps(BLOG["slug"])},
                    content: {json.dumps(blog_content)},
                    metaDescription: {json.dumps(BLOG["metaDescription"])},
                    status: "published"
                ) {{
                    id
                    slug
                    title
                }}
            }}""",
            "variables": None,
        },
        # Pattern 3: Data input
        {
            "name": "data input",
            "query": f"""mutation CreateBlog($data: BlogInput!) {{
                {mutation_name}(data: $data) {{
                    id
                    slug
                    title
                }}
            }}""",
            "variables": {
                "data": {
                    "title": BLOG["title"],
                    "slug": BLOG["slug"],
                    "content": blog_content,
                    "metaDescription": BLOG["metaDescription"],
                    "status": "published",
                }
            },
        },
        # Pattern 4: Minimal fields
        {
            "name": "minimal fields",
            "query": f"""mutation {{
                {mutation_name}(
                    title: {json.dumps(BLOG["title"])},
                    slug: {json.dumps(BLOG["slug"])},
                    body: {json.dumps(blog_content)},
                    description: {json.dumps(BLOG["metaDescription"])}
                ) {{
                    id
                    slug
                    title
                }}
            }}""",
            "variables": None,
        },
    ]

    for pattern in mutation_patterns:
        print(f"  Trying pattern: {pattern['name']}...")
        result = graphql_request(pattern["query"], pattern.get("variables"))

        if not result:
            print("    No response.")
            continue

        if "errors" in result:
            error_msg = result["errors"][0].get("message", "")
            print(f"    Error: {error_msg[:120]}")
            continue

        # Success
        data = result.get("data", {})
        print()
        print("  SUCCESS! Blog published.")
        print(f"  Response: {json.dumps(data, indent=2)}")
        print()
        print(f"  URL: https://www.auricjewels.com/blog/{BLOG['slug']}")
        return True

    print()
    print("  All patterns failed. Manual steps:")
    print()
    print("  1. Check the mutations listed in Step 1 above")
    print("  2. Find the blog/post/article creation mutation")
    print("  3. Edit the mutation_name variable in this script")
    print("  4. Or paste the HTML content directly into your CMS admin panel")
    print(f"     File: {content_path}")
    return False


def main():
    print()
    print("  Auric Jewels — SEO Blog Publisher")
    print("  JewelsCraft GraphQL API")
    print()

    # Step 1: Discover schema
    mutations, queries = step1_introspect()

    if mutations is None:
        print()
        print("Could not connect to the API. Check:")
        print(f"  1. Endpoint: {API_ENDPOINT}")
        print(f"  2. Token starts with: {AUTH_TOKEN[:10]}...")
        print("  3. Your internet connection")
        sys.exit(1)

    # Step 2: Inspect input types for blog mutations
    if mutations:
        for m in mutations:
            for arg in m.get("args", []):
                arg_type = arg.get("type", {})
                type_name = arg_type.get("name")
                if not type_name and arg_type.get("ofType"):
                    type_name = arg_type["ofType"].get("name")
                if type_name and type_name not in ("String", "Int", "Boolean", "ID", "Float"):
                    step2_find_input_type(type_name)

    # Step 3: Publish
    success = step3_publish(mutations)

    print()
    if success:
        print("Done! Blog article is live.")
    else:
        print("Publishing requires manual adjustment. See instructions above.")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
