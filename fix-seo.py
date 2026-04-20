# -*- coding: utf-8 -*-
# Auric Jewels -- Fix SEO Meta Titles & Descriptions
# Fixes Cloudflare error 1010 with browser-like headers
# Run: python fix-seo.py

import json, time, urllib.request, urllib.error, ssl, sys, io

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

API   = 'https://auric.thecodemesh.online/graphql/'
TOKEN = 'rlcLjvXb3wMMHMf1PBsePS8UdTmOBb'

# Browser-like headers to bypass Cloudflare 1010
HEADERS = {
    'Content-Type':  'application/json',
    'Authorization': 'Bearer ' + TOKEN,
    'User-Agent':    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept':        'application/json, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Origin':        'https://auric.thecodemesh.online',
    'Referer':       'https://auric.thecodemesh.online/graphql/',
    'Cache-Control': 'no-cache',
    'Pragma':        'no-cache',
}

FIXES = {
    'best-diamond-jewellery-showroom-gurgaon': {
        'seoTitle':       'Best Diamond Jewellery Showroom Gurgaon | Auric Jewels',
        'seoDescription': 'Best diamond jewellery showroom in Gurgaon. Auric Jewels - IGI/GIA certified diamonds, BIS hallmarked gold & solitaire rings. Visit Sector 45 or shop online.',
    },
    'solitaire-ring-buying-guide-gurgaon': {
        'seoTitle':       'Solitaire Ring Guide Gurgaon | Cuts & Price | Auric',
        'seoDescription': 'Complete solitaire ring buying guide for Gurgaon shoppers. Diamond cuts, clarity grades, IGI/GIA certification & price ranges. Expert advice at Auric Jewels.',
    },
    'luxury-bridal-gold-jewellery-gurgaon': {
        'seoTitle':       'Bridal Gold Jewellery Gurgaon | Wedding Sets | Auric',
        'seoDescription': 'Complete bridal gold jewellery guide for Gurgaon brides. Wedding set checklist, 22K vs 18K gold, budget planning & timeline. Visit Auric Jewels showroom.',
    },
    'diamond-mangalsutra-modern-designs': {
        'seoTitle':       'Diamond Mangalsutra Modern Designs 2026 | Auric Gurgaon',
        'seoDescription': 'Guide to choosing a modern diamond mangalsutra. Single-line, dual-chain & bracelet styles. Certified diamonds & sizing tips. Shop at Auric Jewels Gurgaon.',
    },
    'gold-rate-today-gurgaon-buying-tips': {
        'seoTitle':       'Gold Rate Gurgaon | Smart Jewellery Buying Tips | Auric',
        'seoDescription': 'Understand gold rates in Gurgaon before buying jewellery. Learn what drives prices, 22K vs 18K costs, making charges & how to buy smart at Auric Jewels.',
    },
    'custom-diamond-jewellery-gurgaon': {
        'seoTitle':       'Custom Diamond Jewellery Gurgaon | Auric Jewels',
        'seoDescription': 'Create bespoke diamond jewellery at Auric Jewels Gurgaon. Custom engagement rings, bridal sets & heirloom redesigns. Sketch to IGI certified piece. Book now.',
    },
    'polki-vs-kundan-vs-diamond-bridal-set': {
        'seoTitle':       'Polki vs Kundan vs Diamond | Bridal Set Gurgaon | Auric',
        'seoDescription': 'Compare polki, kundan & diamond bridal jewellery. Brilliance, durability, price & which suits each wedding ceremony. Expert guide from Auric Jewels Gurgaon.',
    },
    'anniversary-gift-jewellery-gurgaon': {
        'seoTitle':       'Anniversary Jewellery Gifts Gurgaon | Auric Jewels',
        'seoDescription': 'Find the perfect anniversary jewellery gift at Auric Jewels Gurgaon. Ideas by milestone year, top-gifted pieces & personalisation options. Free gift wrapping.',
    },
    'hallmark-gold-jewellery-purity-guide-gurgaon': {
        'seoTitle':       'BIS Hallmark Gold Purity Guide Gurgaon | Auric Jewels',
        'seoDescription': 'Learn how to verify BIS hallmark & HUID on gold jewellery. Step-by-step guide to checking gold purity before buying in Gurgaon at Auric Jewels showroom.',
    },
    'karva-chauth-gold-jewellery-gurgaon-2026': {
        'seoTitle':       'Karva Chauth Gold Jewellery Gurgaon 2026 | Auric Jewels',
        'seoDescription': 'Shop Karva Chauth jewellery gifts at Auric Jewels Gurgaon. Diamond pendants, gold bangles, mangalsutra upgrades & trending styles 2026. Free gift wrapping.',
    },
    'solitaire-vs-diamond-ring-difference': {
        'seoTitle':       'Solitaire vs Diamond Ring Difference | Auric Gurgaon',
        'seoDescription': 'Understand the difference between solitaire and diamond rings. Compare styles, sparkle, price & occasions. Expert buying guide from Auric Jewels Gurgaon.',
    },
    'mens-diamond-jewellery-gurgaon-2026': {
        'seoTitle':       "Men's Diamond Jewellery Gurgaon 2026 | Auric Jewels",
        'seoDescription': "Discover men's gold & diamond jewellery trending in Gurgaon 2026. Diamond studs, platinum chains, bracelets & rings. Shop certified pieces at Auric Jewels.",
    },
    'engagement-ring-shopping-gurgaon': {
        'seoTitle':       'Engagement Ring Shopping Gurgaon | Auric Jewels',
        'seoDescription': 'Complete engagement ring shopping guide for Gurgaon couples. Budget tips, diamond quality, ring styles & what to ask your jeweller. Visit Auric Jewels.',
    },
    'diamond-earrings-daily-wear-under-50000': {
        'seoTitle':       'Diamond Earrings Under Rs.50K Gurgaon | Auric Jewels',
        'seoDescription': 'Shop daily wear diamond earrings under Rs.50,000 at Auric Jewels Gurgaon. Studs, hoops & drops in 18K gold. IGI certified diamonds. Free shipping India.',
    },
    'bis-hallmark-gold-jewellery-buying-guide': {
        'seoTitle':       'Why BIS Hallmark Matters | Gold Buying Guide Gurgaon',
        'seoDescription': 'Why BIS hallmark is essential when buying gold jewellery in Gurgaon. What HUID means, how to verify purity & red flags to avoid. Full guide at Auric Jewels.',
    },
    'lightweight-gold-jewellery-working-women-daily-wear': {
        'seoTitle':       'Lightweight Gold Jewellery Working Women | Auric Gurgaon',
        'seoDescription': 'Discover the best lightweight gold jewellery for working women. Daily wear studs, chains, pendants & bangles in 18K/22K gold. Visit Auric Jewels Gurgaon.',
    },
    'lab-grown-vs-natural-diamonds-comparison-india': {
        'seoTitle':       'Lab-Grown vs Natural Diamonds India 2026 | Auric Jewels',
        'seoDescription': 'Lab-grown vs natural diamonds - price, resale value, certification & which to buy. Full 2026 comparison guide. Certified diamonds at Auric Jewels Gurgaon.',
    },
    'jewellery-trends-india-2026': {
        'seoTitle':       'Top 10 Jewellery Trends India 2026 | Auric Jewels',
        'seoDescription': 'Top 10 jewellery trends in India for 2026 - layered necklaces, sculptural earrings, Polki revival & more. Explore trending designs at Auric Jewels Gurgaon.',
    },
    'gold-jewellery-investment-2026-gurgaon': {
        'seoTitle':       'Gold Jewellery Investment 2026 Gurgaon | Auric Jewels',
        'seoDescription': 'Gold jewellery as investment in 2026 - price trends, BIS hallmark, making charges, resale value & smart buying guide. Trusted jeweller Auric Jewels Gurgaon.',
    },
    'platinum-jewellery-men-gurgaon': {
        'seoTitle':       'Platinum Jewellery for Men Gurgaon | Auric Jewels',
        'seoDescription': "Explore platinum jewellery for men - chains, bracelets, rings & cufflinks. Durable, hypoallergenic & sophisticated. Shop men's platinum at Auric Jewels Gurgaon.",
    },
    'layered-necklace-styling-guide-indian-women': {
        'seoTitle':       'Layered Necklace Styling Guide India | Auric Jewels',
        'seoDescription': 'Master layered necklace styling - rules, combinations, Indian & Western looks. Gold & diamond layering tips for 2026. Shop necklaces at Auric Jewels Gurgaon.',
    },
}

def gql(query, variables=None):
    payload = {'query': query}
    if variables:
        payload['variables'] = variables
    req = urllib.request.Request(
        API,
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers=HEADERS,
        method='POST',
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            return json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace') if e.fp else ''
        return {'networkError': 'HTTP ' + str(e.code) + ' | ' + body[:400]}
    except Exception as e:
        return {'networkError': str(e)}

print('=' * 60)
print('AURIC JEWELS -- SEO Meta Fix  |  20 Apr 2026')
print('=' * 60)

print('\n[1] Fetching pages from Saleor...')
r = gql('{pages(first:100){pageInfo{hasNextPage}edges{node{id slug seoTitle seoDescription}}}}')
if 'networkError' in r:
    print('ERROR:', r['networkError'])
    sys.exit(1)
edges = r.get('data', {}).get('pages', {}).get('edges', [])
pages = [(e['node']['slug'], e['node']['id'], e['node'].get('seoTitle',''), e['node'].get('seoDescription','')) for e in edges]
print('  Found', len(pages), 'pages')

# Print current state
print('\n[2] Current SEO audit:')
for slug, pid, t, d in pages:
    issues = []
    if not t: issues.append('NO_TITLE')
    elif len(t) > 60: issues.append('TITLE_TOO_LONG(%d)' % len(t))
    if not d: issues.append('NO_DESC')
    elif len(d) < 150: issues.append('DESC_TOO_SHORT(%d)' % len(d))
    elif len(d) > 160: issues.append('DESC_TOO_LONG(%d)' % len(d))
    status = ', '.join(issues) if issues else 'OK'
    print('  [%s] %s' % (status, slug))

slug_map = {slug: pid for slug, pid, t, d in pages}
fixed = skipped = failed = 0

print('\n[3] Applying fixes:')
for slug, fix in FIXES.items():
    if slug not in slug_map:
        print('  SKIP  ' + slug + ' (not found in Saleor)')
        skipped += 1
        continue

    res = gql(
        'mutation pageUpdate($id:ID!,$input:PageInput!){pageUpdate(id:$id,input:$input){page{id slug seoTitle seoDescription}errors{field message}}}',
        {'id': slug_map[slug], 'input': {'seoTitle': fix['seoTitle'], 'seoDescription': fix['seoDescription']}}
    )

    if 'networkError' in res:
        print('  FAIL  ' + slug + ' -- ' + res['networkError'][:120])
        failed += 1
        continue

    errs = (((res.get('data') or {}).get('pageUpdate') or {}).get('errors') or [])
    if errs:
        msgs = '; '.join(e.get('message', '?') for e in errs)
        print('  FAIL  ' + slug + ' -- ' + msgs)
        failed += 1
    else:
        updated = ((res.get('data') or {}).get('pageUpdate') or {}).get('page') or {}
        print('  OK    ' + slug)
        print('         title: ' + (updated.get('seoTitle') or ''))
    time.sleep(0.4)

print('\n' + '=' * 60)
print('SUMMARY')
print('  Fixed   : %d' % fixed)
print('  Skipped : %d' % skipped)
print('  Failed  : %d' % failed)
print('=' * 60)
