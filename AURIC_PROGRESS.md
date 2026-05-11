# Auric Jewels — SEO Session Progress Log

---

## Session: 2026-05-11

### Trending Keywords Identified (India, May 2026)
| Rank | Keyword | Signal |
|------|---------|--------|
| 1 | **polki bridal jewellery set** | Peak bridal season search surge; #1 wedding jewellery trend 2026 |
| 2 | **lab grown diamond jewellery India** | 75-80% cheaper than natural; major trend shift among millennials |
| 3 | **gold price today India 2026** | 24K at ₹15,235/gram — high purchase intent, daily search volume |
| 4 | **solitaire ring Gurgaon** | Local intent + oval/pear cut emerging; lifestyle not occasion jewellery |
| 5 | **wedding jewellery Gurgaon** | Bridal season + local search; competitors thin on local pages |
| 6 | **lightweight gold jewellery bride** | Comfort + luxury signal; multi-ceremony brides driving this query |
| 7 | **polki kundan bridal set** | High intent, low competition nationally and locally |

---

### Keyword Gap Analysis — 3-5 High-Opportunity Keywords
Auric Jewels is NOT currently ranking for these while competitors are:

| Keyword | Who Ranks | Auric Gap | Action |
|---------|-----------|-----------|--------|
| `polki kundan bridal set gurgaon` | **Zero** major competitors rank | Wide open — no Tanishq/Kalyan/CaratLane local page | Blog + Landing page |
| `lab grown diamond jewellery luxury` | CaratLane (budget angle), Ivana Jewels | Luxury positioning gap; no competitor owns this intersection | Future blog |
| `oval cut solitaire ring Gurgaon` | Small local players only | New cut trend, Gurgaon local intent, competitors absent | Product page SEO |
| `custom diamond jewellery Gurgaon` | No named competitor | 100% gap; high-intent bespoke searches | Landing page |
| `polki jewellery Gurugram` | BlueStone generic product page only | City-name variant, thin competitor presence | Blog internal link |

---

### Content Action Taken

**Target Keyword:** `polki bridal jewellery set` *(+ local variant: polki bridal jewellery set gurgaon)*

**Blog Title:** The Polki Bridal Jewellery Set: Why India's Most Discerning Brides Are Choosing Uncut Diamonds in 2026

**File Created:** `content/blog-polki-bridal-jewellery-set-gurgaon.html`

**Word Count:** ~1,050 words

**SEO Meta:**
- Title tag: `Polki Bridal Jewellery Set in Gurgaon | Auric Jewels`
- Meta description: Discover why India's most discerning 2026 brides are choosing Polki bridal jewellery sets. Explore uncut diamond craftsmanship, styling inspiration, and exclusive Polki collections at Auric Jewels, Gurgaon.
- Canonical: `https://auricjewels.com/blog/polki-bridal-jewellery-set-gurgaon`

**H2 Structure:**
1. What Is Polki, and Why Does It Command Such Reverence?
2. The 2026 Polki Bridal Jewellery Set: Tradition Elevated
3. Polki vs. Kundan vs. Diamond: Understanding the Distinction
4. Why Auric Jewels Is Gurgaon's Destination for Polki Bridal Jewellery
5. Caring for Your Polki Bridal Jewellery Set
6. Begin Your Polki Bridal Consultation at Auric Jewels, Gurgaon

**Tone:** Luxury editorial — no budget language, targets ₹2L+ trousseau buyers

---

### Saleor Publish Status

**Endpoint:** `https://auric.thecodemesh.online/graphql/`
**Channel:** `franchise1`
**Page Type ID:** `UGFnZVR5cGU6Ng==`
**Auth Token:** provided

**Status:** BLOCKED — HTTP 403 "Host not in allowlist"
- Root cause: Django `ALLOWED_HOSTS` on the Saleor server does not include the IP of the Claude Code execution environment
- The publish script is prepared and ready at: `scripts/publish-polki-blog-saleor.sh`
- **Action required by server admin:** Whitelist the calling host in Saleor's Django settings (`ALLOWED_HOSTS`) or Cloudflare firewall, then run the script

---

### Next Session Recommendations

1. **Publish pending blog** once ALLOWED_HOSTS resolved — run `scripts/publish-polki-blog-saleor.sh`
2. **Create landing page** for `custom diamond jewellery Gurgaon` — zero competitor, high-intent
3. **Write blog:** "Lab Grown vs Natural Diamond: What India's Luxury Bride Needs to Know" — target growing lab-grown demand with luxury positioning that CaratLane misses
4. **Internal linking:** Add polki blog to homepage "Bridal" section and from existing `blog-jewellery-trends-india-2026.html`
5. **Schema markup:** Add `Article` + `LocalBusiness` JSON-LD to blog template for Gurgaon local SEO boost

---
