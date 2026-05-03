# Auric Jewels — SEO Progress Log

---

## Session: 2026-05-03

### Trending Keywords Identified
- **#1 Trending:** `polki bridal jewellery Gurgaon` — confirmed dominant 2026 bridal search with zero named-competitor local page coverage
- `polki kundan bridal set` — surging in India bridal searches
- `lightweight bridal jewellery 2026` — brides prioritising comfort + elegance
- `solitaire engagement ring Gurgaon` — high intent, weak competitor coverage
- `uncut diamond bridal necklace India` — no competitor blog content exists
- Gold price today India: ₹15,093/gram (24K) | ₹13,835/gram (22K) as of May 3, 2026 — drives jewellery purchase intent

### Keyword Gap Analysis (vs Tanishq, CaratLane, BlueStone, Kalyan)
| Keyword | Opportunity | Gap |
|---|---|---|
| `polki kundan bridal jewellery Gurgaon` | High | Zero named-competitor coverage locally |
| `solitaire engagement ring Gurgaon` | High | Only small local directories rank |
| `lab grown diamond jewellery Gurgaon` | Medium-High | Only niche labs (Emori); no luxury jeweller blogs |
| `uncut diamond bridal necklace India` | High | No competitor blog content |
| `diamond choker necklace wedding India 2026` | Medium | No dedicated content from any jeweller |

### Content Action
- **Action:** New blog post drafted
- **Title:** Polki Bridal Jewellery in Gurgaon: The 2026 Guide for the Discerning Bride
- **File:** `content/blog-polki-bridal-jewellery-gurgaon-2026.html`
- **Target Keyword:** `polki bridal jewellery Gurgaon`
- **Secondary Keywords:** polki kundan bridal set, uncut diamond jewellery Gurgaon, luxury bridal jewellery Gurgaon 2026
- **Word Count:** ~1,050 words
- **Tone:** Luxury, heritage-forward; no budget language; ₹20K–₹2L+ audience
- **Slug:** `polki-bridal-jewellery-gurgaon-2026`

### Saleor Publication
- **Status:** Blocked — outbound network call to `auric.thecodemesh.online` disallowed in CI environment
- **GraphQL Endpoint:** `https://auric.thecodemesh.online/graphql/`
- **Page Type ID:** `UGFnZVR5cGU6Ng==`
- **Channel:** `franchise1`
- **Publish Command (run manually):**
```bash
curl -X POST https://auric.thecodemesh.online/graphql/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer rlcLjvXb3wMMHMf1PBsePS8UdTmOBb" \
  -d '{
    "query": "mutation { pageCreate(input: { title: \"Polki Bridal Jewellery in Gurgaon: The 2026 Guide for the Discerning Bride\", slug: \"polki-bridal-jewellery-gurgaon-2026\", pageType: \"UGFnZVR5cGU6Ng==\", isPublished: true, seo: { title: \"Polki Bridal Jewellery Gurgaon | 2026 Guide | Auric Jewels\", description: \"Discover Polki bridal jewellery in Gurgaon for 2026 weddings. Auric Jewels curates uncut diamond bridal sets in 22K gold — handcrafted, certified, and made for the discerning Indian bride.\" } }) { page { id title slug } errors { field message } } }"
  }'
```

---

## Sessions Archive

*(Prior sessions will be appended below as the log grows)*
