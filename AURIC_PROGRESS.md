# Auric Jewels — SEO Progress Log

## 20 April 2026 — Bulk SEO Title + Meta Fix

| Metric | Value |
|---|---|
| Date | 20 April 2026 |
| Task | Bulk SEO title + meta description fix |
| Script | `scripts/fix-seo-bulk.py` |
| Status | Script ready — run locally to apply fixes |

### Audit Findings (pre-fix)

| Issue | Count |
|---|---|
| Duplicate meta descriptions | 7 pages |
| Duplicate title tags | 7 pages |
| Titles too short (< 30 chars) | 53 pages |
| Titles too long (> 60 chars) | 1 page |
| **Total pages requiring fixes** | ~61 (some overlap) |

### Fix Rules Applied

**Products**
- Format: `[Product Name] | [Category] | Auric Jewels`
- Max 60 chars, truncated at word boundary
- Meta: 150–160 chars — keyword + Gurgaon + price hint + CTA

**Pages (Blogs)**
- Format: `[Blog Topic] | Auric Jewels Gurgaon`
- 40–60 chars, includes primary keyword + Gurgaon
- Meta: 150–160 chars — keyword + Gurgaon + price hint + CTA

### How to Run

```
# From C:\Users\pc\Desktop\auric-indexing\  (your local machine)
python scripts/fix-seo-bulk.py
```

The script will:
1. Audit all products + pages
2. Generate corrected titles + descriptions
3. Bulk-update via `productUpdate` / `pageUpdate` GraphQL mutations
4. Verify all titles are 40–60 chars, unique, keyword-rich
5. Overwrite this file with final counts

> **Note:** The Saleor API (`auric.thecodemesh.online`) enforces an IP allowlist.
> Run this script from your local machine, not a remote server.
