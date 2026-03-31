import SEOHead from '../../components/SEOHead';
import { collectionSEO, SITE_URL } from '../../lib/seo-config';

/**
 * COLLECTION PAGE — SSG with ISR for pages like Best Sellers, New Arrivals, etc.
 *
 * Key SEO fixes:
 * 1. SSG — fully rendered HTML at build time
 * 2. Unique H1 per collection (was: "Best Seller | Auric Jewels" → keyword-rich)
 * 3. Proper title tags with location and CTA keywords
 * 4. 150-char meta descriptions
 * 5. Crawlable text content
 */

const collectionDescriptions = {
  'best-seller': `Discover the most loved jewellery at Auric Jewels Gurgaon. Our best sellers feature customer-favourite gold and diamond pieces — from timeless diamond studs and classic solitaire rings to elegant necklaces and statement bangles. These are the designs our customers return to again and again, crafted in 18K and 22K BIS hallmarked gold with IGI/GIA certified diamonds. Each best-selling piece has earned its place through exceptional design, quality craftsmanship, and outstanding value. Shop our most popular jewellery and see why thousands of customers across India trust Auric Jewels for their fine jewellery needs.`,

  'new-arrivals': `Be the first to explore our latest gold and diamond jewellery designs at Auric Jewels Gurgaon. Our new arrivals collection features fresh designs that reflect the latest trends while honouring timeless elegance. From modern minimalist pieces to bold statement jewellery, our designers continuously create collections that inspire. Every new piece is handcrafted in BIS hallmarked gold with certified diamonds. Our new arrivals are updated weekly, so there's always something new to discover. Shop the latest in rings, earrings, necklaces, bracelets, and more. Free shipping across India on all new arrivals.`,

  'under-50k': `Find stunning gold and diamond jewellery under Rs 50,000 at Auric Jewels Gurgaon. Luxury doesn't have to come with a hefty price tag. Our affordable collection features beautifully designed rings, earrings, pendants, and bracelets that deliver exceptional style and quality at accessible prices. Every piece is crafted in BIS hallmarked gold with certified diamonds — the same quality as our premium collection, at prices that fit your budget. Perfect for everyday wear, gifting, or starting your fine jewellery collection. Browse by category or price range. Free shipping and 15-day returns.`,

  'gifting': `Find the perfect jewellery gift at Auric Jewels Gurgaon. Whether you're celebrating a birthday, anniversary, wedding, festival, or just want to show someone you care, our curated gifting collection makes it easy to choose the right piece. From elegant diamond studs and delicate pendants to personalised initial necklaces and charm bracelets, every gift from Auric Jewels comes beautifully packaged and ready to delight. All pieces are crafted in BIS hallmarked gold with certified diamonds. Gift wrapping included with every order. Free shipping across India and lifetime exchange guarantee.`,
};

export default function CollectionPage({ slug, seo }) {
  const breadcrumbData = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: SITE_URL },
      {
        '@type': 'ListItem',
        position: 2,
        name: seo.h1.split('|')[0].trim(),
        item: `${SITE_URL}/collections/${slug}`,
      },
    ],
  };

  return (
    <>
      <SEOHead
        title={seo.title}
        description={seo.description}
        canonical={`/collections/${slug}`}
        structuredData={breadcrumbData}
      />

      <main className="container">
        <nav className="breadcrumbs" aria-label="Breadcrumb">
          <a href="/">Home</a> &gt; <span>{seo.h1.split('|')[0].trim()}</span>
        </nav>

        <h1>{seo.h1}</h1>

        <section className="product-description">
          <p>{collectionDescriptions[slug]}</p>
        </section>

        <section>
          <h2>Shop {seo.h1.split('|')[0].trim()}</h2>
          <div className="product-grid">
            <p>
              Loading products... (Connect your product API or CMS to populate
              this grid with actual product cards.)
            </p>
          </div>
        </section>
      </main>
    </>
  );
}

export async function getStaticProps({ params }) {
  const { slug } = params;
  const seo = collectionSEO[slug] || {
    title: `${slug.charAt(0).toUpperCase() + slug.slice(1).replace(/-/g, ' ')} | Auric Jewels Gurgaon`,
    h1: `${slug.charAt(0).toUpperCase() + slug.slice(1).replace(/-/g, ' ')} | Auric Jewels Gurgaon`,
    description: `Shop ${slug.replace(/-/g, ' ')} at Auric Jewels Gurgaon. Premium gold and diamond jewellery. BIS hallmarked. Certified diamonds. Free shipping.`,
  };

  return {
    props: { slug, seo },
    revalidate: 3600,
  };
}

export async function getStaticPaths() {
  const collections = Object.keys(collectionSEO);
  return {
    paths: collections.map((slug) => ({ params: { slug } })),
    fallback: 'blocking',
  };
}
