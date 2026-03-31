#!/bin/bash
# ============================================================
# Auric Jewels — Blog Publisher via JewelsCraft GraphQL API
# ============================================================
#
# USAGE:
#   chmod +x scripts/publish-blog.sh
#   ./scripts/publish-blog.sh
#
# This script publishes the first SEO blog article to the
# JewelsCraft CMS. Run this from your local machine (not
# the sandbox, as the API endpoint is blocked there).
#
# Before running:
# 1. Run the introspection query below to discover the exact
#    mutation name and fields for your CMS
# 2. Update the MUTATION variable below with the correct mutation
# ============================================================

API_ENDPOINT="https://auric.thecodemesh.online/graphql/"
AUTH_TOKEN="fAPR16BVrzI4thcLtj8c4tUUG1wGU6"

# ── Step 1: Discover the schema ──────────────────────────────
echo "Step 1: Discovering GraphQL schema..."
echo ""

SCHEMA=$(curl -s -X POST "$API_ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -d '{"query": "{ __schema { mutationType { fields { name args { name type { name kind ofType { name kind ofType { name kind } } } } type { name } } } } }"}')

echo "Available mutations:"
echo "$SCHEMA" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if 'data' in data and data['data']['__schema']['mutationType']:
    for field in data['data']['__schema']['mutationType']['fields']:
        args = ', '.join([a['name'] for a in field.get('args', [])])
        print(f\"  {field['name']}({args})\")
else:
    print('  No mutations found or error:', json.dumps(data, indent=2))
" 2>/dev/null || echo "$SCHEMA"

echo ""
echo "──────────────────────────────────────────────"
echo "Step 2: Review the mutations above and update"
echo "the MUTATION variable in this script, then"
echo "uncomment and run Step 3."
echo "──────────────────────────────────────────────"

# ── Step 3: Publish the blog (uncomment after discovering schema) ──
# Common mutation patterns for JewelsCraft CMS:
#
# Pattern A: createBlog / createPost / createArticle
# Pattern B: blogCreate / postCreate
# Pattern C: createBlogPost
#
# Update the mutation below based on Step 1 output:

# BLOG_TITLE="Best Diamond Jewellery Showroom in Gurgaon — Why Families Trust Auric Jewels"
# BLOG_SLUG="best-diamond-jewellery-showroom-gurgaon"
# META_DESC="Looking for the best diamond jewellery showroom in Gurgaon? Auric Jewels offers certified diamonds, BIS hallmarked gold & solitaire collections. Visit our showroom."
#
# # Read the HTML content
# BLOG_CONTENT=$(cat content/blog-01-best-diamond-jewellery-showroom-gurgaon.html | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
#
# curl -s -X POST "$API_ENDPOINT" \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer $AUTH_TOKEN" \
#   -d "{
#     \"query\": \"mutation { createBlog(input: { title: \\\"$BLOG_TITLE\\\", slug: \\\"$BLOG_SLUG\\\", content: $BLOG_CONTENT, metaDescription: \\\"$META_DESC\\\", status: \\\"published\\\" }) { id slug title } }\"
#   }" | python3 -m json.tool
#
# echo ""
# echo "Blog published! Check: https://www.auricjewels.com/blog/$BLOG_SLUG"
