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
  'solitaire-collection': `Explore our exclusive solitaire diamond jewellery collection at Auric Jewels Gurgaon. From breathtaking solitaire engagement rings and elegant solitaire pendants to classic solitaire studs, every piece features a single, stunning IGI/GIA certified diamond set in 18K or 22K BIS hallmarked gold. A solitaire is the ultimate expression of timeless elegance — one brilliant diamond that speaks volumes. Our master craftsmen ensure every setting maximises the stone's brilliance and fire. Whether you're proposing, celebrating a milestone, or investing in a forever piece, our solitaire collection offers exceptional quality and value. Free shipping across India.`,

  'best-sellers': `Discover the most loved jewellery at Auric Jewels Gurgaon. Our best sellers feature customer-favourite gold and diamond pieces — from timeless diamond studs and classic solitaire rings to elegant necklaces and statement bangles. These are the designs our customers return to again and again, crafted in 18K and 22K BIS hallmarked gold with IGI/GIA certified diamonds. Each best-selling piece has earned its place through exceptional design, quality craftsmanship, and outstanding value. Shop our most popular jewellery and see why thousands of customers across India trust Auric Jewels for their fine jewellery needs.`,

  'new-arrivals': `Be the first to explore our latest gold and diamond jewellery designs at Auric Jewels Gurgaon. Our new arrivals collection features fresh designs that reflect the latest trends while honouring timeless elegance. From modern minimalist pieces to bold statement jewellery, our designers continuously create collections that inspire. Every new piece is handcrafted in BIS hallmarked gold with certified diamonds. Our new arrivals are updated weekly, so there's always something new to discover. Shop the latest in rings, earrings, necklaces, bracelets, and more. Free shipping across India on all new arrivals.`,

  'for-her': `Shop our curated collection of gold and diamond jewellery for women at Auric Jewels Gurgaon. From delicate everyday pieces to glamorous statement jewellery, this collection is designed for every woman and every occasion. Discover rings that sparkle, earrings that frame your face, necklaces that elevate any outfit, and bracelets that add effortless elegance. Every piece is handcrafted in 18K and 22K BIS hallmarked gold with IGI/GIA certified diamonds. Whether you're treating yourself or gifting someone special, our "For Her" collection makes it easy to find something she'll treasure. Free shipping and 15-day returns.`,

  'for-him': `Discover our collection of men's gold and diamond jewellery at Auric Jewels Gurgaon. From bold gold chains and sleek bracelets to classic rings and refined cufflinks, our men's collection combines masculine design with fine craftsmanship. Every piece is crafted in 18K and 22K BIS hallmarked gold with certified diamonds where featured. Whether he prefers understated elegance or a statement piece, our range offers designs for every taste and occasion — from everyday wear to weddings and formal events. All pieces come with a certificate of authenticity. Free shipping across India and lifetime exchange.`,

  'anniversary-collection': `Celebrate your love story with anniversary jewellery from Auric Jewels Gurgaon. Our anniversary collection features romantic gold and diamond pieces perfect for marking every milestone — from your first anniversary to your golden jubilee. Discover diamond eternity bands, heart pendants, matching couple rings, and elegant bracelets, all handcrafted in 18K and 22K BIS hallmarked gold with IGI/GIA certified diamonds. Each piece is beautifully gift-wrapped and ready to create a memorable moment. Make every anniversary unforgettable with a timeless piece from Auric Jewels. Free shipping and lifetime exchange.`,

  'valentine-collection': `Find the perfect Valentine's Day jewellery gift at Auric Jewels Gurgaon. Our Valentine's collection features heart-shaped pendants, love knot rings, infinity bracelets, and romantic diamond earrings — all designed to express your deepest feelings. Every piece is crafted in 18K and 22K BIS hallmarked gold with IGI/GIA certified diamonds. Whether you're surprising your partner, celebrating a new romance, or treating yourself, our Valentine's Day designs combine love and luxury beautifully. Complimentary gift wrapping with every order. Free shipping across India and 15-day easy returns.`,
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
