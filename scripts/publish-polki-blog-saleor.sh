#!/bin/bash
# Publishes the Polki Bridal Jewellery Set blog post to Saleor CMS
# Run this from a machine/IP that is whitelisted in Saleor's ALLOWED_HOSTS
#
# Pre-requisites:
#   - Server admin must add the calling host to ALLOWED_HOSTS in Saleor Django settings
#   - Auth token must remain valid: rlcLjvXb3wMMHMf1PBsePS8UdTmOBb

ENDPOINT="https://auric.thecodemesh.online/graphql/"
AUTH_TOKEN="rlcLjvXb3wMMHMf1PBsePS8UdTmOBb"

# Step 1: Create the page (blog post)
CREATE_RESPONSE=$(curl -s -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  --data-raw '{
    "query": "mutation CreatePage($input: PageCreateInput!) { pageCreate(input: $input) { page { id title slug isPublished } errors { field message code } } }",
    "variables": {
      "input": {
        "title": "The Polki Bridal Jewellery Set: Why India'\''s Most Discerning Brides Are Choosing Uncut Diamonds in 2026",
        "slug": "polki-bridal-jewellery-set-gurgaon",
        "pageType": "UGFnZVR5cGU6Ng==",
        "isPublished": true,
        "seo": {
          "title": "Polki Bridal Jewellery Set in Gurgaon | Auric Jewels",
          "description": "Discover why India'\''s most discerning 2026 brides are choosing Polki bridal jewellery sets. Explore uncut diamond craftsmanship and exclusive collections at Auric Jewels, Gurgaon."
        },
        "attributes": []
      }
    }
  }')

echo "Create Response:"
echo "$CREATE_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$CREATE_RESPONSE"

# Extract page ID from response
PAGE_ID=$(echo "$CREATE_RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
page = data.get('data', {}).get('pageCreate', {}).get('page', {})
print(page.get('id', ''))
" 2>/dev/null)

if [ -z "$PAGE_ID" ]; then
  echo "ERROR: Could not create page. Check the response above."
  exit 1
fi

echo "Created page ID: $PAGE_ID"

# Step 2: Publish to channel 'franchise1'
PUBLISH_RESPONSE=$(curl -s -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  --data-raw "{
    \"query\": \"mutation PublishPage(\$id: ID!, \$channels: [PageChannelListingAddInput!]!) { pageChannelListingUpdate(id: \$id, input: { addChannels: \$channels }) { page { id isPublished } errors { field message } } }\",
    \"variables\": {
      \"id\": \"$PAGE_ID\",
      \"channels\": [
        {
          \"channelId\": \"franchise1\",
          \"isPublished\": true,
          \"publishedAt\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"
        }
      ]
    }
  }")

echo "Publish Response:"
echo "$PUBLISH_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$PUBLISH_RESPONSE"
echo ""
echo "Done. Blog post should now be live at: https://auricjewels.com/blog/polki-bridal-jewellery-set-gurgaon"
