# Auric Jewels Bot — Progress Log

## 20 April 2026
**Task:** WhatsApp bot — live gold rate + image sending fixed

### Changes made (`src/pages/api/webhook.js`):

**FIX 1 — Live Gold Rate**
- Added `fetchLiveGoldRates()` — scrapes 24K/22K/18K per 10g from GoodReturns Gurgaon page
- Added `formatGoldRateMessage()` — formats response with date, rates, store footer
- Triggers: "gold rate", "gold ka rate", "sone ka bhav", "aaj ka gold", "gold price"

**FIX 2 — Image Sending**
- Added `sendWhatsAppImage()` — sends image messages via Meta Graph API v18.0
- Supports: rings, necklace, earrings, catalogue queries

**FIX 3 — Keyword Triggers**
- `isGoldRateQuery` → live gold rate response
- `isRingsQuery` → rings image + text
- `isNecklaceQuery` → necklace/haar image + text
- `isEarringsQuery` → earrings image + text
- `isCatalogueQuery` → catalogue image + browse link
- `isAddressQuery` → store address card (address, showroom kahan hai)
- `isTimingQuery` → "10 AM – 8 PM, 7 days a week" (timing, open, kab khulta)

All keyword matches bypass AI and return instant responses.
