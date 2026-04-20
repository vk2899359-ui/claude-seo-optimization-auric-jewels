# -*- coding: utf-8 -*-
# Auric Jewels -- Fix Product SEO Titles
# Channel: franchise1  |  Total: ~9007 products
# Fixes: seoTitle empty / under 30 chars / same as product name
# Format: "[Product Name] | [Category] | Auric Jewels"  (max 60)
# Requires: pip install cloudscraper
# Run:      python fix-products-seo.py

import sys, io, time

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    import cloudscraper
except ImportError:
    print('ERROR: Run:  pip install cloudscraper'); sys.exit(1)

API    = 'https://auric.thecodemesh.online/graphql/'
TOKEN  = 'rlcLjvXb3wMMHMf1PBsePS8UdTmOBb'
CHANNEL = 'franchise1'

scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
)


# ---------------------------------------------------------------------------
def gql(query, variables=None):
    payload = {'query': query}
    if variables:
        payload['variables'] = variables
    try:
        r = scraper.post(API, json=payload,
                         headers={'Authorization': 'Bearer ' + TOKEN}, timeout=30)
        if r.status_code != 200:
            return {'networkError': 'HTTP %d: %s' % (r.status_code, r.text[:200])}
        return r.json()
    except Exception as e:
        return {'networkError': str(e)}


# ---------------------------------------------------------------------------
def make_title(name, cat):
    """
    Format: "[Product Name] | [Category] | Auric Jewels"  max 60 chars
    Truncation order:
      1. Full form with category
      2. Without category
      3. Truncate product name with '...'
    """
    suffix = ' | Auric Jewels'
    cat    = (cat or 'Jewellery').strip()

    full = name.strip() + ' | ' + cat + suffix        # preferred
    if len(full) <= 60:
        return full

    short = name.strip() + suffix                     # drop category
    if len(short) <= 60:
        return short

    max_n = 60 - len(suffix) - 3                      # truncate name
    return name.strip()[:max_n].rstrip() + '...' + suffix


def needs_fix(product):
    """Return True if this product's seoTitle should be updated."""
    name  = (product.get('name') or '').strip()
    title = (product.get('seoTitle') or '').strip()
    if not title:                   return True   # empty
    if len(title) < 30:             return True   # too short
    if title.lower() == name.lower(): return True # same as product name
    return False


# ---------------------------------------------------------------------------
def fetch_all_products():
    print('Fetching all products from channel "%s"...' % CHANNEL)
    products, cursor, page = [], None, 0

    while True:
        after = ', after: "%s"' % cursor if cursor else ''
        q = ('{products(first:100, channel:"%s"%s)'
             '{totalCount pageInfo{hasNextPage endCursor}'
             'edges{node{id name seoTitle seoDescription category{name}}}}}') % (CHANNEL, after)

        r = gql(q)
        if 'networkError' in r:
            print('\n  ERROR:', r['networkError'][:150])
            return None
        if r.get('errors'):
            print('\n  GQL error:', r['errors'][0].get('message','')[:120])
            return None

        data  = (r.get('data') or {}).get('products', {})
        edges = data.get('edges', [])
        for edge in edges:
            products.append(edge['node'])

        page += 1
        total = data.get('totalCount', '?')
        sys.stdout.write('  Page %3d | %4d / %s fetched\r' % (page, len(products), total))
        sys.stdout.flush()

        pi = data.get('pageInfo', {})
        if pi.get('hasNextPage'):
            cursor = pi['endCursor']
        else:
            break

    print('\n  Fetch complete. Total products: %d' % len(products))
    return products


# ---------------------------------------------------------------------------
def main():
    print('=' * 64)
    print('AURIC JEWELS -- Fix Product SEO Titles  |  20 Apr 2026')
    print('Channel : ' + CHANNEL)
    print('=' * 64)

    products = fetch_all_products()
    if not products:
        print('0 products returned. Check token / channel / connection.')
        sys.exit(1)

    # ---- Audit --------------------------------------------------------
    to_fix = [p for p in products if needs_fix(p)]
    ok     = len(products) - len(to_fix)

    print('\n[AUDIT]')
    print('  Total products   : %d' % len(products))
    print('  Already OK       : %d' % ok)
    print('  Need fix         : %d' % len(to_fix))
    print('  Reason breakdown :')
    empty   = sum(1 for p in to_fix if not (p.get('seoTitle') or '').strip())
    short   = sum(1 for p in to_fix if (p.get('seoTitle') or '').strip() and
                  len((p.get('seoTitle') or '').strip()) < 30 and
                  (p.get('seoTitle') or '').strip().lower() != (p.get('name') or '').strip().lower())
    same    = sum(1 for p in to_fix if (p.get('seoTitle') or '').strip().lower() ==
                  (p.get('name') or '').strip().lower())
    print('    Empty title      : %d' % empty)
    print('    Under 30 chars   : %d' % short)
    print('    Same as name     : %d' % same)

    if not to_fix:
        print('\nNothing to fix!')
        return

    # ---- Preview first 8 ---------------------------------------------
    print('\n[PREVIEW - first 8]')
    print('  %-36s  ->  %s' % ('OLD TITLE', 'NEW TITLE'))
    print('  ' + '-' * 80)
    for p in to_fix[:8]:
        cat = (p.get('category') or {}).get('name', 'Jewellery')
        old = (p.get('seoTitle') or '(empty)').strip()
        new = make_title(p['name'], cat)
        print('  %-36s  ->  %s' % (old[:36], new))

    # ---- Fix ----------------------------------------------------------
    print('\n[FIXING %d products]' % len(to_fix))
    print('  Estimated time: ~%d minutes\n' % max(1, int(len(to_fix) * 0.25 / 60)))

    fixed = failed = 0
    start = time.time()

    for i, p in enumerate(to_fix, 1):
        cat       = (p.get('category') or {}).get('name', 'Jewellery')
        new_title = make_title(p['name'], cat)
        desc      = (p.get('seoDescription') or '').strip() or None

        res = gql(
            'mutation productUpdate($id:ID!,$input:ProductInput!)'
            '{productUpdate(id:$id,input:$input)'
            '{product{seoTitle}errors{field message code}}}',
            {'id': p['id'], 'input': {'seoTitle': new_title, 'seoDescription': desc}}
        )

        elapsed = time.time() - start
        eta     = int(elapsed / i * (len(to_fix) - i)) if i > 1 else 0
        prog    = '[%d/%d | ETA %ds]' % (i, len(to_fix), eta)

        if 'networkError' in res:
            print('  FAIL %s %s | %s' % (prog, p['name'][:30], res['networkError'][:60]))
            failed += 1
        else:
            errs = (((res.get('data') or {}).get('productUpdate') or {}).get('errors') or [])
            if errs:
                print('  FAIL %s %s | %s' % (prog, p['name'][:30],
                      errs[0].get('message','?')[:60]))
                failed += 1
            else:
                fixed += 1
                print('  OK   %s %-32s -> %s' % (prog, p['name'][:32], new_title[:42]))

        time.sleep(0.25)

    # ---- Summary ------------------------------------------------------
    total_time = int(time.time() - start)
    print('\n' + '=' * 64)
    print('SUMMARY')
    print('  Products fetched : %d' % len(products))
    print('  Fixed            : %d' % fixed)
    print('  Failed           : %d' % failed)
    print('  Time taken       : %dm %ds' % (total_time // 60, total_time % 60))
    print('=' * 64)


if __name__ == '__main__':
    main()
