# -*- coding: utf-8 -*-
# Auric Jewels -- Fix Product SEO Titles (short/empty)
# 9007 products, no channel filter needed
# Requires: pip install cloudscraper
# Run:      python fix-products-seo.py

import sys, io, json, time

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    import cloudscraper
except ImportError:
    print('ERROR: Run: pip install cloudscraper'); sys.exit(1)

API   = 'https://auric.thecodemesh.online/graphql/'
TOKEN = 'rlcLjvXb3wMMHMf1PBsePS8UdTmOBb'

scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
)

def gql(query, variables=None):
    payload = {'query': query}
    if variables:
        payload['variables'] = variables
    try:
        r = scraper.post(API, json=payload,
                         headers={'Authorization': 'Bearer ' + TOKEN}, timeout=30)
        if r.status_code != 200:
            return {'networkError': 'HTTP ' + str(r.status_code) + ': ' + r.text[:200]}
        return r.json()
    except Exception as e:
        return {'networkError': str(e)}

def make_title(name, cat):
    """[Product Name] | [Category] | Auric Jewels Gurgaon  (max 60)"""
    suffix = ' | Auric Jewels Gurgaon'
    cat    = (cat or 'Jewellery').strip()
    full   = name.strip() + ' | ' + cat + suffix
    if len(full) <= 60:
        return full
    short = name.strip() + suffix
    if len(short) <= 60:
        return short
    return name.strip()[:60 - len(suffix) - 3].rstrip() + '...' + suffix

def fetch_all_products():
    print('Fetching all products (no channel filter)...')
    products, cursor, page = [], None, 0
    while True:
        after = ', after: "' + cursor + '"' if cursor else ''
        q = ('{ products(first: 100' + after + ') {'
             'pageInfo { hasNextPage endCursor }'
             'totalCount'
             'edges { node { id name seoTitle seoDescription category { name } } } } }')
        r = gql(q)
        if 'networkError' in r:
            print('  ERROR:', r['networkError'][:150])
            return None
        if r.get('errors'):
            print('  GQL error:', r['errors'][0].get('message', '')[:120])
            return None
        data  = (r.get('data') or {}).get('products', {})
        edges = data.get('edges', [])
        for edge in edges:
            products.append(edge['node'])
        page += 1
        total = data.get('totalCount', '?')
        print('  Page %d | fetched %d / %s' % (page, len(products), total), end='\r')
        pi = data.get('pageInfo', {})
        if pi.get('hasNextPage'):
            cursor = pi['endCursor']
        else:
            break
    print('\n  Done. Total fetched:', len(products))
    return products

def main():
    print('=' * 62)
    print('AURIC JEWELS -- Fix Product SEO Titles  |  20 Apr 2026')
    print('=' * 62)

    products = fetch_all_products()
    if not products:
        print('No products returned. Check connection / token.')
        sys.exit(1)

    # Audit
    needs_fix = []
    for p in products:
        t = (p.get('seoTitle') or '').strip()
        if not t or len(t) < 30:
            needs_fix.append(p)

    ok_count = len(products) - len(needs_fix)
    print('\n[AUDIT]')
    print('  Total products : %d' % len(products))
    print('  Already OK     : %d (seoTitle >= 30 chars)' % ok_count)
    print('  Need fix       : %d (empty or < 30 chars)' % len(needs_fix))

    if not needs_fix:
        print('\nAll product SEO titles are already OK!')
        return

    # Preview first 10
    print('\n[PREVIEW - first 10 fixes]')
    for p in needs_fix[:10]:
        cat = (p.get('category') or {}).get('name', 'Jewellery')
        old = (p.get('seoTitle') or '(empty)').strip()
        new = make_title(p['name'], cat)
        print('  %-40s  =>  %s' % ((old[:38] + '..') if len(old) > 40 else old, new))

    print('\nStarting fixes (%d products)...' % len(needs_fix))
    fixed = failed = 0
    start = time.time()

    for i, p in enumerate(needs_fix, 1):
        cat       = (p.get('category') or {}).get('name', 'Jewellery')
        new_title = make_title(p['name'], cat)
        desc      = (p.get('seoDescription') or '').strip() or None

        res = gql(
            'mutation productUpdate($id:ID!,$input:ProductInput!)'
            '{productUpdate(id:$id,input:$input)'
            '{product{seoTitle}errors{field message}}}',
            {'id': p['id'], 'input': {'seoTitle': new_title, 'seoDescription': desc}}
        )

        if 'networkError' in res:
            print('  [%d/%d] FAIL %s | %s' % (i, len(needs_fix), p['name'][:35], res['networkError'][:60]))
            failed += 1
        else:
            errs = (((res.get('data') or {}).get('productUpdate') or {}).get('errors') or [])
            if errs:
                print('  [%d/%d] FAIL %s | %s' % (i, len(needs_fix), p['name'][:35],
                      errs[0].get('message','?')[:60]))
                failed += 1
            else:
                fixed += 1
                elapsed = time.time() - start
                eta     = elapsed / i * (len(needs_fix) - i)
                print('  [%d/%d] OK  %s  =>  %s  (ETA %ds)' % (
                    i, len(needs_fix), p['name'][:30], new_title[:40], int(eta)))
        time.sleep(0.35)

    print('\n' + '=' * 62)
    print('DONE')
    print('  Fixed   : %d' % fixed)
    print('  Failed  : %d' % failed)
    print('  Time    : %.0fs' % (time.time() - start))
    print('=' * 62)

if __name__ == '__main__':
    main()
