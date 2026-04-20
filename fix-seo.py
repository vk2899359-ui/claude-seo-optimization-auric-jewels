# -*- coding: utf-8 -*-
# Auric Jewels -- Fix SEO Meta Titles & Descriptions (Standalone)
# Run: python fix-seo.py
# API: https://auric.thecodemesh.online/graphql/

import json, time, urllib.request, urllib.error, ssl, sys, io

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

API   = 'https://auric.thecodemesh.online/graphql/'
TOKEN = 'rlcLjvXb3wMMHMf1PBsePS8UdTmOBb'

FIXES = {
    'best-diamond-jewellery-showroom-gurgaon': {
        'seoTitle':       'Best Diamond Jewellery Showroom Gurgaon | Auric Jewels',
        'seoDescription': 'Best diamond jewellery showroom in Gurgaon. Auric Jewels — IGI/GIA certified diamonds, BIS hallmarked gold & solitaire rings. Visit Sector 45 or shop online.',
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
        'seoDescription': 'Lab-grown vs natural diamonds — price, resale value, certification & which to buy. Full 2026 comparison guide. Certified diamonds at Auric Jewels Gurgaon.',
    },
    'jewellery-trends-india-2026': {
        'seoTitle':       'Top 10 Jewellery Trends India 2026 | Auric Jewels',
        'seoDescription': 'Discover the top 10 jewellery trends in India for 2026 — layered necklaces, sculptural earrings, Polki revival & more. Explore trending designs at Auric Jewels.',
    },
    'gold-jewellery-investment-2026-gurgaon': {
        'seoTitle':       'Gold Jewellery Investment 2026 Gurgaon | Auric Jewels',
        'seoDescription': 'Gold jewellery as investment in 2026 — price trends, BIS hallmark, making charges, resale value & smart buying guide. Trusted jeweller Auric Jewels Gurgaon.',
    },
    'platinum-jewellery-men-gurgaon': {
        'seoTitle':       'Platinum Jewellery for Men Gurgaon | Auric Jewels',
        'seoDescription': "Explore platinum jewellery for men — chains, bracelets, rings & cufflinks. Durable, hypoallergenic & sophisticated. Shop men's platinum at Auric Jewels Gurgaon.",
    },
    'layered-necklace-styling-guide-indian-women': {
        'seoTitle':       'Layered Necklace Styling Guide India | Auric Jewels',
        'seoDescription': 'Master layered necklace styling — rules, combinations, Indian & Western looks. Gold & diamond layering tips for 2026. Shop necklaces at Auric Jewels Gurgaon.',
    },
}

def gql(query, variables=None):
    payload = {'query': query}
    if variables:
        payload['variables'] = variables
    req = urllib.request.Request(
        API,
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer ' + TOKEN},
        method='POST',
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            return json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace') if e.fp else ''
        return {'networkError': 'HTTP ' + str(e.code) + ': ' + body[:300]}
    except Exception as e:
        return {'networkError': str(e)}

def fetch_pages():
    print('Fetching pages from Saleor...')
    pages, cursor = [], None
    while True:
        after = ', after: "' + cursor + '"' if cursor else ''
        q = '{pages(first:100' + after + '){pageInfo{hasNextPage endCursor}edges{node{id slug title seoTitle seoDescription}}}}'
        r = gql(q)
        if 'networkError' in r:
            print('  ERROR:', r['networkError'])
            return None
        data = (r.get('data') or {}).get('pages', {})
        for edge in data.get('edges', []):
            pages.append(edge['node'])
        pi = data.get('pageInfo', {})
        if pi.get('hasNextPage'):
            cursor = pi['endCursor']
        else:
            break
    print('  Fetched', len(pages), 'pages')
    return pages

def update_page(page_id, seo_title, seo_description):
    q = 'mutation pageUpdate($id:ID!,$input:PageInput!){pageUpdate(id:$id,input:$input){page{id slug seoTitle seoDescription}errors{field message}}}'
    return gql(q, {'id': page_id, 'input': {'seoTitle': seo_title, 'seoDescription': seo_description}})

print('=' * 65)
print('AURIC JEWELS -- SEO Meta Fix  |  20 Apr 2026')
print('=' * 65)

pages = fetch_pages()
if not pages:
    print('Cannot connect to Saleor. Run this from your local machine (not a sandbox).')
    sys.exit(1)

slug_map = {p['slug']: p['id'] for p in pages}
fixed, skipped, failed = [], [], []

print('\nApplying fixes:')
for slug, fix in FIXES.items():
    if slug not in slug_map:
        skipped.append(slug)
        print('  SKIP ', slug, '(not in Saleor)')
        continue
    r = update_page(slug_map[slug], fix['seoTitle'], fix['seoDescription'])
    if 'networkError' in r:
        failed.append(slug)
        print('  FAIL ', slug, r['networkError'])
        continue
    errs = (((r.get('data') or {}).get('pageUpdate') or {}).get('errors') or [])
    if errs:
        failed.append(slug)
        print('  FAIL ', slug, ';'.join(e.get('message','?') for e in errs))
    else:
        fixed.append(slug)
        print('  OK   ', slug)
    time.sleep(0.3)

print('\n' + '=' * 65)
print('DONE  fixed=%d  skipped=%d  failed=%d' % (len(fixed), len(skipped), len(failed)))
if failed:
    print('FAILED:', ', '.join(failed))
print('=' * 65)
