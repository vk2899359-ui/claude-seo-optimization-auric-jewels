import SEOHead from '../../components/SEOHead';
import { generateProductSEO, generateProductDescription, SITE_URL } from '../../lib/seo-config';

/**
 * PRODUCT PAGE — SSR with caching for dynamic product data.
 *
 * Key SEO fixes:
 * 1. SSR — Google sees full product HTML, not empty JS shell
 * 2. H1 = Product Name + Category + "Auric Jewels"
 * 3. 100-200 word product description (was: just product name)
 * 4. JSON-LD Product structured data for rich snippets in Google
 * 5. Breadcrumbs for site hierarchy
 * 6. Proper title tag and meta description
 */

export default function ProductPage({ product }) {
  const seo = generateProductSEO(product);
  const fullDescription = product.longDescription || generateProductDescription(product);

  const productStructuredData = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    brand: 'Auric Jewels',
    category: product.category,
    description: seo.description,
    image: product.images || [],
    offers: {
      '@type': 'Offer',
      priceCurrency: 'INR',
      price: product.price,
      availability: 'https://schema.org/InStock',
      seller: {
        '@type': 'Organization',
        name: 'Auric Jewels',
      },
    },
  };

  const breadcrumbData = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: SITE_URL },
      {
        '@type': 'ListItem',
        position: 2,
        name: product.category
          ? product.category.charAt(0).toUpperCase() + product.category.slice(1)
          : 'Jewellery',
        item: `${SITE_URL}/categories/${product.category || 'all'}`,
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: product.name,
        item: `${SITE_URL}/products/${product.slug}`,
      },
    ],
  };

  // Merge both structured data objects
  const structuredData = [productStructuredData, breadcrumbData];

  return (
    <>
      <SEOHead
        title={seo.title}
        description={seo.description}
        canonical={`/products/${product.slug}`}
        ogType="product"
        ogImage={product.images?.[0]}
        structuredData={structuredData}
      />

      <main className="container">
        {/* Breadcrumbs */}
        <nav className="breadcrumbs" aria-label="Breadcrumb">
          <a href="/">Home</a> &gt;{' '}
          <a href={`/categories/${product.category || 'all'}`}>
            {product.category
              ? product.category.charAt(0).toUpperCase() + product.category.slice(1)
              : 'Jewellery'}
          </a>{' '}
          &gt; <span>{product.name}</span>
        </nav>

        {/* H1 — Product Name + Category + Auric Jewels */}
        <h1>{seo.h1}</h1>

        {/* Product details */}
        <section>
          <div>
            {/* Product image gallery placeholder */}
            {product.images?.map((img, i) => (
              <img
                key={i}
                src={img}
                alt={`${product.name} - ${product.category} - Auric Jewels - View ${i + 1}`}
                width={600}
                height={600}
                loading={i === 0 ? 'eager' : 'lazy'}
              />
            ))}
          </div>

          <div>
            {/* Price and key details */}
            {product.price && (
              <p>
                <strong>Price:</strong> &#8377;{Number(product.price).toLocaleString('en-IN')}
              </p>
            )}
            {product.material && (
              <p><strong>Metal:</strong> {product.material}</p>
            )}
            {product.weight && (
              <p><strong>Weight:</strong> {product.weight}</p>
            )}
            {product.purity && (
              <p><strong>Purity:</strong> {product.purity}</p>
            )}
            {product.stone && (
              <p><strong>Stone:</strong> {product.stone}</p>
            )}
          </div>
        </section>

        {/* ── PRODUCT DESCRIPTION — 100-200 words for SEO ── */}
        <section>
          <h2>Product Description</h2>
          <div className="product-description">
            {fullDescription.split('\n\n').map((paragraph, i) => (
              <p key={i}>{paragraph}</p>
            ))}
          </div>
        </section>

        {/* Shipping & trust signals — additional crawlable content */}
        <section>
          <h2>Shipping &amp; Returns</h2>
          <ul>
            <li>Free insured shipping across India</li>
            <li>15-day easy return policy</li>
            <li>Lifetime exchange at full value</li>
            <li>BIS hallmarked gold guarantee</li>
            <li>IGI/GIA certified diamonds</li>
            <li>Certificate of authenticity included</li>
          </ul>
        </section>
      </main>
    </>
  );
}

/**
 * SSR for product pages — fetches product data on every request.
 *
 * IMPORTANT: Replace the sample product below with your actual data source:
 * - Shopify Storefront API
 * - Your own database/CMS
 * - Headless commerce platform
 *
 * The key point: getServerSideProps runs on the SERVER, so Google
 * receives fully-rendered HTML with all product content visible.
 */
export async function getServerSideProps({ params, res }) {
  const { slug } = params;

  // Cache the SSR response for 1 hour on Vercel's CDN
  res.setHeader(
    'Cache-Control',
    'public, s-maxage=3600, stale-while-revalidate=86400'
  );

  // TODO: Replace this sample product with your actual data fetch
  // Example: const product = await fetch(`https://your-api.com/products/${slug}`).then(r => r.json());
  const product = {
    slug,
    name: slug
      .split('-')
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' '),
    category: 'rings', // Will come from your API
    material: '18K Yellow Gold',
    weight: '4.5g',
    purity: '75% (18K)',
    stone: 'Diamond',
    stoneWeight: '0.25 ct',
    price: 45000,
    inStock: true,
    images: [],
    longDescription: '', // If empty, auto-generated description is used
  };

  return { props: { product } };
}
