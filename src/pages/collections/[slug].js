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

// ─── Collection-specific FAQs for rich snippets ─────────────
const collectionFAQs = {
  'solitaire-collection': [
    { q: 'What is a solitaire diamond ring?', a: 'A solitaire diamond ring features a single diamond as the centrepiece, set in a simple band. It is the most classic and timeless engagement ring style. At Auric Jewels Gurgaon, our solitaire rings feature IGI/GIA certified diamonds in 18K and 22K hallmarked gold.' },
    { q: 'How do I choose the right solitaire diamond?', a: 'Focus on the 4Cs — Cut, Clarity, Colour, and Carat. Cut is the most important factor for brilliance. Visit Auric Jewels Gurgaon for an expert consultation where our diamond specialists will help you choose the perfect solitaire within your budget.' },
    { q: 'What is the starting price of a solitaire ring in Gurgaon?', a: 'Solitaire diamond rings at Auric Jewels Gurgaon start from ₹35,000 for 0.15 carat stones and go up based on the diamond size, quality, and metal choice. All stones are IGI/GIA certified.' },
  ],
  'best-sellers': [
    { q: 'What are the best selling jewellery items at Auric Jewels?', a: 'Our best sellers include diamond studs, solitaire engagement rings, gold chain necklaces, tennis bracelets, and lightweight daily-wear bangles. These are the most loved pieces by our customers across Gurgaon and Delhi NCR.' },
    { q: 'Why should I buy from Auric Jewels\' best sellers collection?', a: 'Our best sellers are customer-tested and loved. They represent the finest craftsmanship, design, and value. Every piece is in BIS hallmarked gold with certified diamonds, backed by our lifetime exchange guarantee.' },
  ],
  'new-arrivals': [
    { q: 'How often does Auric Jewels add new designs?', a: 'We update our New Arrivals collection weekly with fresh designs in gold and diamond jewellery. Follow us on Instagram or visit our Gurgaon showroom to see the latest additions first.' },
    { q: 'Can I pre-order upcoming designs?', a: 'Yes, you can pre-order upcoming designs or request custom modifications. Contact our team at +91-9012495941 or visit our Gurgaon showroom for personalised assistance.' },
  ],
  'for-her': [
    { q: 'What jewellery gifts are best for women?', a: 'Diamond studs, pendant necklaces, charm bracelets, and stackable rings are universally loved gifts. Auric Jewels offers complimentary gift wrapping and personalised engraving on select pieces.' },
    { q: 'Do you have jewellery for everyday wear?', a: 'Yes, our "For Her" collection features a dedicated everyday wear range — lightweight, durable, and elegant. Designed for working women who want to look stylish without the heaviness of traditional jewellery.' },
  ],
  'for-him': [
    { q: 'Does Auric Jewels sell men\'s jewellery?', a: 'Yes! Our men\'s collection features gold chains, bracelets, rings, diamond studs, and cufflinks. Crafted in 18K and 22K BIS hallmarked gold with masculine, contemporary designs.' },
    { q: 'What is the most popular men\'s jewellery?', a: 'Gold chains and diamond studs are our most popular men\'s pieces. We also see growing demand for men\'s bracelets and platinum rings. Visit our Gurgaon showroom for the full men\'s collection.' },
  ],
  'anniversary-collection': [
    { q: 'What is the best anniversary gift in jewellery?', a: 'Diamond eternity bands, heart pendants, and matching couple rings are the most popular anniversary gifts. Auric Jewels offers beautiful gift packaging with personalised engraving options.' },
    { q: 'Do you have jewellery for milestone anniversaries?', a: 'Yes, we have curated collections for every milestone — from your first anniversary to silver (25th) and golden (50th) jubilee. Each piece comes with complimentary gift wrapping.' },
  ],
  'valentine-collection': [
    { q: 'What jewellery should I gift on Valentine\'s Day?', a: 'Heart-shaped pendants, love knot rings, infinity bracelets, and diamond studs are perfect Valentine\'s Day gifts. Auric Jewels offers complimentary gift wrapping and express delivery for Valentine\'s week.' },
    { q: 'When should I order Valentine\'s Day jewellery?', a: 'We recommend ordering at least 5-7 days before Valentine\'s Day for standard delivery, or 3 days before with express shipping. Visit our Gurgaon showroom for same-day purchases.' },
  ],
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

  // FAQPage schema for rich snippets
  const faqs = collectionFAQs[slug] || [];
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
        canonical={`/collections/${slug}`}
        structuredData={structuredData}
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

        {/* FAQ section — matches FAQPage schema for rich snippets */}
        {faqs.length > 0 && (
          <section className="faq-section">
            <h2>Frequently Asked Questions</h2>
            {faqs.map((faq, i) => (
              <div key={i} className="faq-item">
                <h3>{faq.q}</h3>
                <p>{faq.a}</p>
              </div>
            ))}
          </section>
        )}
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
