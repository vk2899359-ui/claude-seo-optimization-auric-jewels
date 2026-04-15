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

// ─── Category-specific FAQs for rich snippets ──────────────
const categoryFAQs = {
  rings: [
    { q: 'What is the price range of diamond rings at Auric Jewels Gurgaon?', a: 'Diamond rings at Auric Jewels Gurgaon start from ₹15,000 for daily wear designs and go up to ₹5,00,000+ for premium solitaire engagement rings. All rings are crafted in 18K or 22K BIS hallmarked gold with IGI/GIA certified diamonds.' },
    { q: 'Can I customise an engagement ring at Auric Jewels?', a: 'Yes, Auric Jewels offers bespoke ring customisation. Choose your diamond, metal, and design. Our master craftsmen will create your dream engagement ring. Visit our Gurgaon showroom for a personalised consultation.' },
    { q: 'Do you offer solitaire rings in Gurgaon?', a: 'Yes, we have an extensive solitaire ring collection featuring IGI/GIA certified diamonds in various cuts — round brilliant, princess, cushion, oval, and emerald cut. All set in 18K or 22K hallmarked gold or platinum.' },
  ],
  earrings: [
    { q: 'What types of diamond earrings are available at Auric Jewels?', a: 'We offer diamond studs, hoops, drops, jhumkas, chandbalis, and ear cuffs. All crafted in BIS hallmarked gold with IGI/GIA certified diamonds. Perfect for everyday wear and special occasions.' },
    { q: 'Are diamond studs a good investment?', a: 'Diamond studs are one of the most versatile jewellery investments. They can be worn daily, for work, and for special occasions. At Auric Jewels, all diamond studs come with certification, ensuring value retention.' },
    { q: 'Can I buy lightweight gold earrings for daily wear?', a: 'Yes, Auric Jewels has a dedicated lightweight collection starting from 2 grams. Designed for working women who want elegance without heaviness. Available in 18K and 22K hallmarked gold.' },
  ],
  necklaces: [
    { q: 'What gold necklace designs are trending in 2026?', a: 'Layered necklaces, minimalist chain pendants, choker sets, and statement pieces are trending in 2026. Auric Jewels Gurgaon has the latest designs in 18K and 22K BIS hallmarked gold with certified diamonds.' },
    { q: 'Do you have bridal necklace sets in Gurgaon?', a: 'Yes, we have an exclusive bridal collection featuring complete necklace sets with matching earrings, maang tikka, and bangles. All in BIS hallmarked gold with IGI/GIA certified diamonds.' },
    { q: 'What is the starting price for gold necklaces?', a: 'Gold necklaces at Auric Jewels start from ₹25,000 for delicate chain designs. Bridal and statement necklaces range from ₹1,00,000 to ₹10,00,000+. All prices are transparent with no hidden charges.' },
  ],
  bracelets: [
    { q: 'What is a tennis bracelet and is it available at Auric Jewels?', a: 'A tennis bracelet is a thin, elegant bracelet featuring a continuous line of individually set diamonds. Auric Jewels offers stunning diamond tennis bracelets in 18K gold, starting from ₹50,000. All diamonds are IGI/GIA certified.' },
    { q: 'Are gold bracelets a good gift option?', a: 'Gold bracelets are one of the most appreciated gifts for women. They are versatile, timeless, and hold their value. Auric Jewels offers complimentary gift wrapping on all bracelet purchases.' },
  ],
  bangles: [
    { q: 'What is the gold purity of bangles at Auric Jewels?', a: 'Our gold bangles are available in both 18K (75% purity) and 22K (91.6% purity), all BIS hallmarked with HUID numbers for guaranteed authenticity.' },
    { q: 'Do you have diamond bangles for daily wear?', a: 'Yes, we have a lightweight diamond bangle collection designed for daily wear. These feature subtle diamond accents in 18K gold, combining elegance with comfort for everyday use.' },
  ],
  pendants: [
    { q: 'Can I buy a diamond pendant with chain at Auric Jewels?', a: 'Yes, all our diamond pendants can be purchased with a matching gold chain. We offer various chain lengths and styles to complement each pendant design. BIS hallmarked gold with certified diamonds.' },
    { q: 'What are popular pendant designs in 2026?', a: 'Initial pendants, evil eye designs, solitaire drops, heart-shaped pendants, and geometric patterns are popular in 2026. Explore our latest collection at the Gurgaon showroom or online.' },
  ],
  chains: [
    { q: 'What types of gold chains do you offer?', a: 'We offer rope chains, box chains, cable chains, curb chains, figaro chains, and designer link chains in 18K and 22K BIS hallmarked gold. Available for both women and men in multiple lengths.' },
    { q: 'Are gold chains available for men at Auric Jewels?', a: 'Yes, we have an extensive men\'s gold chain collection featuring bold, masculine designs in 22K hallmarked gold. Styles include rope, curb, and box chains in various weights and lengths.' },
  ],
  mangalsutra: [
    { q: 'What are the latest mangalsutra designs at Auric Jewels?', a: 'Our latest mangalsutra collection includes single-line diamond pendants, sleek modern chain designs, and contemporary dual-chain styles. All in 18K/22K BIS hallmarked gold with IGI certified diamonds.' },
    { q: 'Can I get a modern mangalsutra that looks like a regular necklace?', a: 'Yes, Auric Jewels specialises in modern mangalsutra designs that double as stylish necklaces. Sleek diamond pendants on delicate gold chains that blend tradition with contemporary fashion.' },
  ],
  'nose-pins': [
    { q: 'What nose pin designs are available at Auric Jewels?', a: 'We offer diamond studs, gold hoops, screw-back designs, and L-shaped nose pins in 18K and 22K BIS hallmarked gold. Diamond nose pins feature IGI/GIA certified stones.' },
    { q: 'Are diamond nose pins comfortable for daily wear?', a: 'Yes, our nose pins are designed for maximum comfort. We offer lightweight designs with secure screw-back and push-back fittings. The diamond studs start from just 0.5 grams for worry-free daily wear.' },
  ],
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

  // FAQPage schema for rich snippets
  const faqs = categoryFAQs[slug] || [];
  const faqSchema = faqs.length > 0 ? {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map((faq) => ({
      '@type': 'Question',
      name: faq.q,
      acceptedAnswer: { '@type': 'Answer', text: faq.a },
    })),
  } : null;

  const structuredData = faqSchema ? [breadcrumbData, faqSchema] : breadcrumbData;

  return (
    <>
      <SEOHead
        title={seo.title}
        description={seo.description}
        canonical={`/categories/${slug}`}
        structuredData={structuredData}
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

        {/* FAQ section — matches FAQPage schema for rich snippets */}
        <section className="faq-section">
          <h2>Frequently Asked Questions about {seo.h1.split('|')[0].trim()}</h2>
          {faqs.length > 0 && faqs.map((faq, i) => (
            <div key={i} className="faq-item">
              <h3>{faq.q}</h3>
              <p>{faq.a}</p>
            </div>
          ))}
          <div className="faq-item">
            <h3>What is the purity of gold used at Auric Jewels?</h3>
            <p>
              All our gold jewellery is available in 18K and 22K purity, BIS hallmarked
              for guaranteed quality and authenticity with verifiable HUID numbers.
            </p>
          </div>
          <div className="faq-item">
            <h3>Are the diamonds certified?</h3>
            <p>
              Yes, every diamond used in our jewellery is IGI or GIA certified, ensuring
              exceptional cut, clarity, colour, and carat weight. Certificates are provided with every purchase.
            </p>
          </div>
          <div className="faq-item">
            <h3>Do you offer free shipping?</h3>
            <p>
              Yes, we offer free insured shipping across India on all orders. We also offer
              a 15-day easy return policy and lifetime exchange at full gold value.
            </p>
          </div>
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
