# Auric Jewels SEO Progress

## Session: April 2026 — Claude Code (claude/setup-auric-jewels-dn44y)

---

## TASK 1 — Homepage SEO Meta Update

**Status: COMPLETE (code change applied)**

Updated `src/lib/seo-config.js` `homepageSEO` object:

| Field | Old Value | New Value |
|-------|-----------|-----------|
| `title` | Luxury Gold & Diamond Jewellery in Gurgaon \| Auric Jewels | **Auric Jewels Gurgaon \| BIS Hallmarked Gold & IGI Certified Diamond Jewellery** |
| `description` | Shop luxury gold & diamond jewellery in Gurgaon… | **Shop BIS hallmarked gold and IGI/GIA certified diamond jewellery at Auric Jewels, Sector 45 Gurgaon. Bridal, daily wear & gifting collections. Visit showroom or WhatsApp for expert guidance.** |

**Saleor CMS homepage update script** also created at:
`scripts/task1-homepage-seo-saleor.py`
→ Run from Windows machine: `python scripts/task1-homepage-seo-saleor.py`

---

## TASK 2 — 10 SEO Collection Pages

**Status: Scripts ready — run one-by-one from Windows machine**

> **Note:** Saleor GraphQL API (`auric.thecodemesh.online`) enforces an IP/host allowlist.
> Scripts must be executed from your local Windows machine, not this CI server.
> All scripts use: `python scripts/page-XX-name.py`

### Pages Created (run each script to publish to Saleor):

| # | Slug | Script | Status |
|---|------|--------|--------|
| 1 | bestsellers-jewellery-gurgaon | `page-01-bestsellers.py` | ⏳ Run locally |
| 2 | daily-wear-jewellery-gurgaon | `page-02-daily-wear.py` | ⏳ Run locally |
| 3 | gifts-under-25000-jewellery | `page-03-gifts-under-25000.py` | ⏳ Run locally |
| 4 | gifts-under-50000-jewellery | `page-04-gifts-under-50000.py` | ⏳ Run locally |
| 5 | bridal-jewellery-gurgaon | `page-05-bridal.py` | ⏳ Run locally |
| 6 | diamond-jewellery-gurgaon-collection | `page-06-diamond-collection.py` | ⏳ Run locally |
| 7 | office-wear-jewellery | `page-07-office-wear.py` | ⏳ Run locally |
| 8 | lightweight-gold-jewellery | `page-08-lightweight-gold.py` | ⏳ Run locally |
| 9 | anniversary-gift-jewellery-gurgaon | `page-09-anniversary.py` | ⏳ Run locally |
| 10 | new-arrivals-jewellery-gurgaon | `page-10-new-arrivals.py` | ⏳ Run locally |

### SEO Specifications (all pages):

| # | H1 | SEO Title | SEO Desc (~160 chars) |
|---|----|-----------|----------------------|
| 1 | Bestselling Jewellery in Gurgaon \| Auric Jewels | Bestselling Jewellery Gurgaon \| Gold & Diamond Top Picks \| Auric Jewels | Explore bestselling gold & diamond jewellery at Auric Jewels… |
| 2 | Daily Wear Gold & Diamond Jewellery \| Lightweight Designs | Daily Wear Gold & Diamond Jewellery Gurgaon \| Lightweight \| Auric Jewels | Shop daily wear gold & diamond jewellery at Auric Jewels… |
| 3 | Jewellery Gifts Under ₹25,000 \| Perfect for Every Occasion | Jewellery Gifts Under ₹25,000 \| Gold & Diamond Gifting \| Auric Jewels Gurgaon | Find the perfect jewellery gift under ₹25,000 at Auric Jewels… |
| 4 | Premium Jewellery Gifts Under ₹50,000 \| Auric Jewels | Premium Jewellery Gifts Under ₹50,000 \| Diamonds & Gold \| Auric Jewels Gurgaon | Shop premium jewellery gifts under ₹50,000 at Auric Jewels… |
| 5 | Bridal Jewellery in Gurgaon \| Wedding Gold & Diamond Sets | Bridal Jewellery Gurgaon \| Wedding Gold & Diamond Sets \| Auric Jewels | Shop bridal jewellery at Auric Jewels, Sector 45 Gurgaon… |
| 6 | Diamond Jewellery Collection Gurgaon \| IGI/GIA Certified | Diamond Jewellery Collection Gurgaon \| IGI/GIA Certified \| Auric Jewels | Explore Auric Jewels' certified diamond jewellery collection… |
| 7 | Office Wear Jewellery \| Subtle Gold & Diamond Pieces | Office Wear Jewellery Gurgaon \| Subtle Gold & Diamond Pieces \| Auric Jewels | Shop office wear jewellery at Auric Jewels, Sector 45 Gurgaon… |
| 8 | Lightweight Gold Jewellery for Daily Use \| Auric Jewels | Lightweight Gold Jewellery Daily Use Gurgaon \| 18K 22K \| Auric Jewels | Shop lightweight gold jewellery for daily use at Auric Jewels… |
| 9 | Anniversary Jewellery Gifts in Gurgaon \| Diamonds & Gold | Anniversary Jewellery Gifts Gurgaon \| Diamonds & Gold \| Auric Jewels | Find the perfect anniversary jewellery gift at Auric Jewels… |
| 10 | New Arrivals in Gold & Diamond Jewellery \| Auric Jewels | New Arrivals Gold & Diamond Jewellery Gurgaon 2026 \| Auric Jewels | Explore new arrivals in gold & diamond jewellery at Auric Jewels… |

### Content Quality Checklist (all 10 pages):
- [x] 400+ words per page
- [x] Keyword-rich, luxury tone (no "cheap/affordable/budget" language)
- [x] H1 matching task specification
- [x] Multiple H2 sections per page
- [x] Internal links to relevant existing blog articles
- [x] Metadata type=collection added via `updateMetadata` mutation
- [x] SEO title + meta description on every page
- [x] `isPublished: True` set on all pages

### Running Instructions (Windows):
```
cd C:\Users\pc\Desktop\auric-indexing
python scripts/page-01-bestsellers.py
# confirm SUCCESS, then:
python scripts/page-02-daily-wear.py
# confirm SUCCESS, then:
python scripts/page-03-gifts-under-25000.py
# ... continue through page-10
python scripts/task1-homepage-seo-saleor.py
```

---

## Previous Sessions

### Blog Articles Published (20 total across prior sessions)
- best-diamond-jewellery-showroom-gurgaon
- solitaire-ring-buying-guide-gurgaon
- luxury-bridal-gold-jewellery-gurgaon
- diamond-mangalsutra-modern-designs
- gold-rate-today-gurgaon-buying-tips
- custom-diamond-jewellery-gurgaon
- polki-vs-kundan-vs-diamond-bridal-set
- anniversary-gift-jewellery-gurgaon
- hallmark-gold-jewellery-purity-guide-gurgaon
- karva-chauth-gold-jewellery-gurgaon-2026
- solitaire-vs-diamond-ring-difference
- mens-diamond-jewellery-gurgaon-2026
- engagement-ring-shopping-gurgaon
- diamond-earrings-daily-wear-under-50000
- bis-hallmark-gold-jewellery-buying-guide
- lightweight-gold-jewellery-working-women-daily-wear
- lab-grown-vs-natural-diamonds-comparison-india
- jewellery-trends-india-2026
- gold-jewellery-investment-2026-gurgaon
- platinum-jewellery-men-gurgaon
- layered-necklace-styling-guide-indian-women
