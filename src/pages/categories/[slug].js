import SEOHead from '../../components/SEOHead';
import { categorySEO, SITE_URL } from '../../lib/seo-config';

/**
 * CATEGORY PAGE — Statically generated at build time (SSG).
 *
 * Key SEO fixes:
 * 1. SSG via getStaticProps/getStaticPaths — pre-rendered HTML for every category
 * 2. Unique H1 per category with target keywords
 * 3. Optimized title tags (was: "Earrings | Auric Jewels" → now includes location + CTA)
 * 4. 150-char meta descriptions per category
 * 5. Breadcrumbs for navigation and structured data
 * 6. Crawlable category description text (fixes 0 word count)
 */

const categoryDescriptions = {
  rings: `Explore our curated collection of gold and diamond rings at Auric Jewels Gurgaon. From classic solitaire engagement rings and diamond-studded wedding bands to contemporary cocktail rings and everyday statement pieces, every ring is handcrafted in 18K or 22K BIS hallmarked gold. Our diamonds are IGI/GIA certified for exceptional brilliance. Whether you're looking for the perfect engagement ring, an anniversary gift, or a ring to celebrate your style, Auric Jewels offers designs that blend Indian heritage with modern elegance. Browse by metal type, stone, price range, or occasion. Free shipping across India.`,

  earrings: `Discover designer gold and diamond earrings at Auric Jewels Gurgaon. Our collection features everything from classic diamond studs and elegant hoops to traditional jhumkas, glamorous chandbalis, and modern drop earrings. Each pair is crafted in 18K or 22K BIS hallmarked gold with IGI/GIA certified diamonds. Whether you need everyday studs for the office, statement earrings for a wedding, or a gift for someone special, our range has you covered. Our earrings are designed for comfort and durability, with secure closures and lightweight construction. Shop online with free shipping and 15-day returns.`,

  necklaces: `Shop exquisite gold and diamond necklaces at Auric Jewels Gurgaon. From delicate chain pendants and layered necklaces to traditional chokers and grand bridal sets, our necklace collection celebrates every style and occasion. Handcrafted in 18K and 22K BIS hallmarked gold with certified diamonds, each necklace is a work of art. Our designs range from minimalist everyday pieces to elaborate statement necklaces perfect for weddings and festivals. Every purchase includes a certificate of authenticity. Browse by style, metal, occasion, or price range. Free shipping and lifetime exchange on all orders.`,

  bracelets: `Browse gold and diamond bracelets at Auric Jewels Gurgaon. Our collection includes sleek tennis bracelets, traditional gold bangles reimagined, charm bracelets, and contemporary cuff designs. Every bracelet is handcrafted in 18K or 22K BIS hallmarked gold and adorned with IGI/GIA certified diamonds. Whether you prefer a delicate chain bracelet for everyday wear or a bold diamond tennis bracelet for special occasions, Auric Jewels has the perfect piece. Our bracelets feature secure clasps and comfortable fits. Shop online with free insured shipping across India and hassle-free 15-day returns.`,

  bangles: `Discover our stunning collection of gold and diamond bangles at Auric Jewels Gurgaon. From traditional kadas and classic gold bangles to modern diamond-studded designs, our bangle collection offers timeless elegance for every woman. Handcrafted in 18K and 22K BIS hallmarked gold with certified diamonds, each bangle reflects the finest Indian craftsmanship. Perfect for weddings, festivals, daily wear, or gifting. Our bangles are available in a variety of sizes and styles. Every purchase comes with a certificate of authenticity and lifetime exchange guarantee. Free shipping across India.`,

  pendants: `Shop gold and diamond pendants at Auric Jewels Gurgaon. From classic solitaire pendants and initial charms to religious motifs and contemporary geometric designs, our pendant collection offers versatile pieces for every style. Crafted in 18K and 22K BIS hallmarked gold with IGI/GIA certified diamonds, each pendant is designed to be both beautiful and meaningful. Layer them with chains or wear as a standalone statement. Perfect for gifting on birthdays, anniversaries, or festivals. Every pendant comes with a certificate of authenticity. Free shipping and easy returns.`,

  mangalsutra: `Explore modern diamond mangalsutra designs at Auric Jewels Gurgaon. We offer a beautiful range of mangalsutras that blend traditional significance with contemporary style. Choose from sleek single-line designs, classic dual-chain styles, or modern pendant-style mangalsutras — all crafted in 18K and 22K BIS hallmarked gold with certified diamonds. Our mangalsutras are designed for the modern woman who values tradition but loves contemporary aesthetics. Available in various lengths and styles. Every piece comes with a certificate of authenticity. Free shipping and lifetime exchange.`,

  chains: `Shop gold chains for women and men at Auric Jewels Gurgaon. Our chain collection features classic rope chains, sleek cable chains, sturdy box chains, and designer link chains in 18K and 22K BIS hallmarked gold. Whether you're looking for a delicate everyday chain, a bold statement piece, or the perfect chain to pair with a pendant, our range offers exceptional variety and craftsmanship. Each chain is crafted for durability and comfort, with secure clasps and a luxurious finish. Available in multiple lengths and weights. Every purchase comes with a certificate of authenticity. Free shipping across India and 15-day easy returns.`,

  'nose-pins': `Shop delicate gold and diamond nose pins at Auric Jewels Gurgaon. Our collection features classic studs, elegant hoops, and trendy screw-back designs crafted in 18K and 22K BIS hallmarked gold. Adorned with IGI/GIA certified diamonds, each nose pin is designed for comfort and sparkle. Whether you prefer a subtle diamond stud for everyday wear or a statement piece for special occasions, our range has something for everyone. All nose pins come with secure fittings for worry-free wear. Free shipping across India and 15-day easy returns.`,
};

export default function CategoryPage({ slug, seo }) {
  const breadcrumbData = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: SITE_URL },
      {
        '@type': 'ListItem',
        position: 2,
        name: seo.h1.split('|')[0].trim(),
        item: `${SITE_URL}/categories/${slug}`,
      },
    ],
  };

  return (
    <>
      <SEOHead
        title={seo.title}
        description={seo.description}
        canonical={`/categories/${slug}`}
        structuredData={breadcrumbData}
      />

      <main className="container">
        {/* Breadcrumbs — helps Google understand site hierarchy */}
        <nav className="breadcrumbs" aria-label="Breadcrumb">
          <a href="/">Home</a> &gt; <span>{seo.h1.split('|')[0].trim()}</span>
        </nav>

        {/* H1 — unique, keyword-rich heading for each category */}
        <h1>{seo.h1}</h1>

        {/* Category description — fixes 0 word count issue */}
        <section className="product-description">
          <p>{categoryDescriptions[slug]}</p>
        </section>

        {/* Product grid placeholder — replace with actual product data */}
        <section>
          <h2>Browse {seo.h1.split('|')[0].trim()}</h2>
          <div className="product-grid">
            {/* Products will be rendered here from your data source */}
            <p>
              Loading products... (Connect your product API or CMS to populate
              this grid with actual product cards.)
            </p>
          </div>
        </section>

        {/* FAQ section for additional crawlable content */}
        <section>
          <h2>Frequently Asked Questions</h2>
          <h3>What is the purity of gold used at Auric Jewels?</h3>
          <p>
            All our gold jewellery is available in 18K and 22K purity, BIS hallmarked
            for guaranteed quality and authenticity.
          </p>
          <h3>Are the diamonds certified?</h3>
          <p>
            Yes, every diamond used in our jewellery is IGI or GIA certified, ensuring
            exceptional cut, clarity, colour, and carat weight.
          </p>
          <h3>Do you offer free shipping?</h3>
          <p>
            Yes, we offer free insured shipping across India on all orders. International
            shipping is available at additional cost.
          </p>
        </section>
      </main>
    </>
  );
}

/**
 * SSG — generates a static HTML page for each category at build time.
 * Google sees fully-rendered HTML immediately. No JavaScript needed to view content.
 *
 * Add revalidate for ISR (Incremental Static Regeneration) to update
 * without full rebuilds.
 */
export async function getStaticProps({ params }) {
  const { slug } = params;
  const seo = categorySEO[slug] || {
    title: `${slug.charAt(0).toUpperCase() + slug.slice(1).replace(/-/g, ' ')} | Auric Jewels Gurgaon`,
    h1: `${slug.charAt(0).toUpperCase() + slug.slice(1).replace(/-/g, ' ')} | Auric Jewels Gurgaon`,
    description: `Shop ${slug.replace(/-/g, ' ')} at Auric Jewels Gurgaon. Handcrafted gold and diamond jewellery. BIS hallmarked. Certified diamonds. Free shipping.`,
  };

  return {
    props: { slug, seo },
    revalidate: 3600, // ISR: regenerate every hour
  };
}

export async function getStaticPaths() {
  const categories = Object.keys(categorySEO);
  return {
    paths: categories.map((slug) => ({ params: { slug } })),
    fallback: 'blocking', // SSR on-demand for new categories, then cache
  };
}
