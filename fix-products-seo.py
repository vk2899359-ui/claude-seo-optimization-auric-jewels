# -*- coding: utf-8 -*-
# Auric Jewels -- Fix Product SEO Titles (short / empty)
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
    print('ERROR: cloudscraper not installed.')
    print('Run:   pip install cloudscraper')
    sys.exit(1)

API   = 'https://auric.thecodemesh.online/graphql/'
TOKEN = 'rlcLjvXb3wMMHMf1PBsePS8UdTmOBb'

scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
)

# ── GraphQL helper ───────────────────────────────────────────
def gql(query, variables=None):
    payload = {'query': query}
    if variables:
        payload['variables'] = variables
    try:
        r = scraper.post(
            API,
            json=payload,
            headers={'Authorization': 'Bearer ' + TOKEN},
            timeout=30,
        )
        if r.status_code != 200:
            return {'networkError': 'HTTP ' + str(r.status_code) + ': ' + r.text[:300]}
        return r.json()
    except Exception as e:
        return {'networkError': str(e)}

# ── Fetch ALL products (paginated) ───────────────────────────
def fetch_all_products():
    print('Fetching products from Saleor...')
    products = []
    cursor   = None

    while True:
        after = ', after: "' + cursor + '"' if cursor else ''
        q = '''
        {
          products(first: 100, channel: "default-channel"''' + after + ''') {
            pageInfo { hasNextPage endCursor }
            edges {
              node {
                id
                name
                seoTitle
                seoDescription
                category { name }
              }
            }
          }
        }
        '''
        r = gql(q)
        if 'networkError' in r:
            print('  ERROR:', r['networkError'][:200])
            return None

        errs = r.get('errors', [])
        if errs:
            # Retry without channel if default-channel not found
            if cursor is None and any('channel' in str(e).lower() for e in errs):
                print('  default-channel not found, retrying without channel...')
                return fetch_all_products_no_channel()
            print('  GQL errors:', errs[:2])
            return None

        data  = (r.get('data') or {}).get('products', {})
        edges = data.get('edges', [])
        for edge in edges:
            products.append(edge['node'])

        pi = data.get('pageInfo', {})
        if pi.get('hasNextPage'):
            cursor = pi['endCursor']
        else:
            break

    print('  Fetched', len(products), 'products')
    return products


def fetch_all_products_no_channel():
    products = []
    cursor   = None
    while True:
        after = ', after: "' + cursor + '"' if cursor else ''
        q = '''
        {
          products(first: 100''' + after + ''') {
            pageInfo { hasNextPage endCursor }
            edges {
              node {
                id
                name
                seoTitle
                seoDescription
                category { name }
              }
            }
          }
        }
        '''
        r = gql(q)
        if 'networkError' in r:
            print('  ERROR:', r['networkError'][:200])
            return None
        data  = (r.get('data') or {}).get('products', {})
        edges = data.get('edges', [])
        for edge in edges:
            products.append(edge['node'])
        pi = data.get('pageInfo', {})
        if pi.get('hasNextPage'):
            cursor = pi['endCursor']
        else:
            break
    print('  Fetched', len(products), 'products (no-channel mode)')
    return products


# ── Build fixed seoTitle ─────────────────────────────────────
def make_seo_title(name, category_name):
    """
    Format: "[Product Name] | [Category] | Auric Jewels Gurgaon"
    Hard max: 60 chars. Truncate product name if needed.
    """
    suffix = ' | Auric Jewels Gurgaon'
    cat    = (category_name or 'Jewellery').strip()

    # Full attempt
    full = name.strip() + ' | ' + cat + suffix
    if len(full) <= 60:
        return full

    # Try without category
    no_cat = name.strip() + suffix
    if len(no_cat) <= 60:
        return no_cat

    # Truncate product name to fit
    max_name = 60 - len(suffix) - 3  # 3 for '...'
    truncated = name.strip()[:max_name].rstrip() + '...'
    return truncated + suffix


# ── productUpdate mutation ───────────────────────────────────
def update_product_seo(product_id, seo_title, seo_description):
    q = '''
    mutation productUpdate($id: ID!, $input: ProductInput!) {
      productUpdate(id: $id, input: $input) {
        product {
          id
          name
          seoTitle
          seoDescription
        }
        errors {
          field
          message
          code
        }
      }
    }
    '''
    v = {
        'id': product_id,
        'input': {
            'seoTitle':       seo_title,
            'seoDescription': seo_description,
        },
    }
    return gql(q, v)


# ── Main ─────────────────────────────────────────────────────
def main():
    print('=' * 60)
    print('AURIC JEWELS -- Fix Product SEO Titles  |  20 Apr 2026')
    print('=' * 60)

    products = fetch_all_products()
    if products is None:
        print('\nCannot reach Saleor. Try mobile hotspot if Cloudflare blocks.')
        sys.exit(1)

    # ── Audit ────────────────────────────────────────────────
    needs_fix = []
    ok_count  = 0

    print('\n[AUDIT]')
    for p in products:
        t = (p.get('seoTitle') or '').strip()
        needs = not t or len(t) < 30
        flag  = 'FIX' if needs else 'OK '
        print('  [%s] len=%-3s  %s' % (flag, len(t) if t else '0', p['name'][:55]))
        if needs:
            needs_fix.append(p)
        else:
            ok_count += 1

    print('\n  Total products : %d' % len(products))
    print('  Already OK     : %d' % ok_count)
    print('  Need fix       : %d' % len(needs_fix))

    if not needs_fix:
        print('\nAll product SEO titles are already >= 30 chars. Nothing to do.')
        return

    # ── Fix ──────────────────────────────────────────────────
    print('\n[FIXING]')
    fixed  = []
    failed = []

    for p in needs_fix:
        cat_name = (p.get('category') or {}).get('name', 'Jewellery')
        new_title = make_seo_title(p['name'], cat_name)

        # Keep existing description if present; else leave empty
        existing_desc = (p.get('seoDescription') or '').strip()

        r = update_product_seo(p['id'], new_title, existing_desc or None)

        if 'networkError' in r:
            print('  FAIL  %s -- %s' % (p['name'][:45], r['networkError'][:80]))
            failed.append(p['name'])
            continue

        errs = (((r.get('data') or {}).get('productUpdate') or {}).get('errors') or [])
        if errs:
            msgs = '; '.join(e.get('message', '?') for e in errs)
            print('  FAIL  %s -- %s' % (p['name'][:45], msgs[:80]))
            failed.append(p['name'])
        else:
            updated = ((r.get('data') or {}).get('productUpdate') or {}).get('product') or {}
            actual  = updated.get('seoTitle', new_title)
            print('  OK    %s' % p['name'][:45])
            print('        -> "%s" (%d chars)' % (actual, len(actual)))
            fixed.append(p['name'])

        time.sleep(0.4)

    # ── Summary ──────────────────────────────────────────────
    print('\n' + '=' * 60)
    print('SUMMARY')
    print('  Total fetched : %d' % len(products))
    print('  Already OK    : %d' % ok_count)
    print('  Fixed         : %d' % len(fixed))
    print('  Failed        : %d' % len(failed))
    if failed:
        print('  FAILED:')
        for n in failed:
            print('    - ' + n)
    print('=' * 60)


if __name__ == '__main__':
    main()
