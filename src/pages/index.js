import SEOHead from '../components/SEOHead';
import { homepageSEO, SITE_URL } from '../lib/seo-config';

// ─── STRUCTURED DATA: JewelryStore + LocalBusiness ───────────
const jewelryStoreSchema = {
  '@context': 'https://schema.org',
  '@type': 'JewelryStore',
  '@id': `${SITE_URL}/#jewelry-store`,
  name: 'Auric Jewels',
  alternateName: 'Auric Jewels Gurgaon',
  url: SITE_URL,
  logo: `${SITE_URL}/logo.png`,
  image: [
    `${SITE_URL}/images/auric-jewels-og.jpg`,
    `${SITE_URL}/images/auric-jewels-showroom.jpg`,
  ],
  description:
    'Premium gold & diamond jewellery store in Gurgaon, Haryana. BIS hallmarked gold jewellery, IGI/GIA certified diamonds, solitaire collection, bridal sets, and custom designs. Visit our showroom in Gurgaon.',
  address: {
    '@type': 'PostalAddress',
    streetAddress: 'Gurgaon',
    addressLocality: 'Gurgaon',
    addressRegion: 'Haryana',
    postalCode: '122001',
    addressCountry: 'IN',
  },
  geo: {
    '@type': 'GeoCoordinates',
    latitude: 28.4595,
    longitude: 77.0266,
  },
  areaServed: [
    { '@type': 'City', name: 'Gurgaon' },
    { '@type': 'City', name: 'Delhi' },
    { '@type': 'City', name: 'Noida' },
    { '@type': 'City', name: 'Faridabad' },
    { '@type': 'State', name: 'Haryana' },
    { '@type': 'Country', name: 'India' },
  ],
  priceRange: '₹₹₹',
  telephone: '+91-9012495941',
  email: 'info@auricjewels.com',
  openingHoursSpecification: [
    {
      '@type': 'OpeningHoursSpecification',
      dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      opens: '10:00',
      closes: '20:00',
    },
  ],
  sameAs: [
    'https://www.instagram.com/auricjewels/',
    'https://www.facebook.com/auricjewels/',
    'https://www.youtube.com/@auricjewels',
    'https://www.pinterest.com/auricjewels/',
  ],
  hasOfferCatalog: {
    '@type': 'OfferCatalog',
    name: 'Gold & Diamond Jewellery',
    itemListElement: [
      { '@type': 'OfferCatalog', name: 'Diamond Rings', url: `${SITE_URL}/categories/rings` },
      { '@type': 'OfferCatalog', name: 'Diamond Earrings', url: `${SITE_URL}/categories/earrings` },
      { '@type': 'OfferCatalog', name: 'Gold Necklaces', url: `${SITE_URL}/categories/necklaces` },
      { '@type': 'OfferCatalog', name: 'Diamond Bracelets', url: `${SITE_URL}/categories/bracelets` },
      { '@type': 'OfferCatalog', name: 'Gold Bangles', url: `${SITE_URL}/categories/bangles` },
      { '@type': 'OfferCatalog', name: 'Solitaire Collection', url: `${SITE_URL}/collections/solitaire-collection` },
    ],
  },
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: '4.9',
    bestRating: '5',
    worstRating: '1',
    ratingCount: '187',
    reviewCount: '142',
  },
  review: [
    {
      '@type': 'Review',
      reviewRating: { '@type': 'Rating', ratingValue: '5', bestRating: '5' },
      author: { '@type': 'Person', name: 'Priya M.' },
      reviewBody: 'Auric Jewels made my engagement ring shopping experience unforgettable. The team helped us choose the perfect solitaire with complete transparency on certification and pricing.',
    },
    {
      '@type': 'Review',
      reviewRating: { '@type': 'Rating', ratingValue: '5', bestRating: '5' },
      author: { '@type': 'Person', name: 'Rahul & Sneha K.' },
      reviewBody: 'We bought our complete bridal set from Auric Jewels. The quality of craftsmanship, the BIS hallmarking on every piece, and the personalised service made all the difference.',
    },
    {
      '@type': 'Review',
      reviewRating: { '@type': 'Rating', ratingValue: '5', bestRating: '5' },
      author: { '@type': 'Person', name: 'Anita S.' },
      reviewBody: 'I have been buying daily wear diamond jewellery from Auric Jewels for two years now. Every piece comes with proper certification and the lifetime exchange policy gives me complete peace of mind.',
    },
  ],
};

// ─── STRUCTURED DATA: FAQPage (for rich snippets in Google) ──
const faqSchema = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'Where is the best jewellery showroom in Gurgaon?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Auric Jewels is a premium jewellery showroom in Gurgaon offering BIS hallmarked gold and IGI/GIA certified diamond jewellery. Visit our showroom for a personalised experience with expert consultations, transparent pricing, and lifetime exchange policy.',
      },
    },
    {
      '@type': 'Question',
      name: 'Does Auric Jewels sell BIS hallmarked gold jewellery?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes, every piece of gold jewellery at Auric Jewels carries a BIS hallmark with a verifiable HUID number, guaranteeing the exact purity of 18K or 22K gold. We are committed to 100% transparency in gold purity.',
      },
    },
    {
      '@type': 'Question',
      name: 'Are the diamonds at Auric Jewels certified?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes, every diamond used in our jewellery is IGI or GIA certified, ensuring exceptional cut, clarity, colour, and carat weight. Certification documents are provided with every diamond purchase.',
      },
    },
    {
      '@type': 'Question',
      name: 'Does Auric Jewels offer free shipping in India?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes, Auric Jewels offers free insured shipping across India on all orders. Every shipment is fully insured and tracked for your peace of mind. We also offer a 15-day easy return policy and lifetime exchange at full gold value.',
      },
    },
    {
      '@type': 'Question',
      name: 'Can I buy diamond engagement rings in Gurgaon from Auric Jewels?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Absolutely! Auric Jewels offers a stunning collection of diamond engagement rings in Gurgaon, including solitaire rings, halo rings, and custom designs. All diamonds are IGI/GIA certified. Visit our Gurgaon showroom or shop online with free shipping.',
      },
    },
    {
      '@type': 'Question',
      name: 'What is the return policy at Auric Jewels?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Auric Jewels offers a 15-day easy return policy on all purchases. We also offer lifetime exchange at full gold value, giving you complete peace of mind with every purchase.',
      },
    },
  ],
};

// ─── STRUCTURED DATA: WebSite (for sitelinks search box) ─────
const websiteSchema = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  '@id': `${SITE_URL}/#website`,
  name: 'Auric Jewels',
  url: SITE_URL,
  potentialAction: {
    '@type': 'SearchAction',
    target: `${SITE_URL}/search?q={search_term_string}`,
    'query-input': 'required name=search_term_string',
  },
};

// Combine all structured data
const structuredData = [jewelryStoreSchema, faqSchema, websiteSchema];

const categories = [
  { name: 'Rings', slug: 'rings', icon: '💍' },
  { name: 'Earrings', slug: 'earrings', icon: '✦' },
  { name: 'Necklaces', slug: 'necklaces', icon: '◇' },
  { name: 'Pendants', slug: 'pendants', icon: '◆' },
  { name: 'Bracelets', slug: 'bracelets', icon: '○' },
  { name: 'Bangles', slug: 'bangles', icon: '◎' },
  { name: 'Chains', slug: 'chains', icon: '∞' },
];

const bestSellers = [
  { name: 'Aria Solitaire Ring', category: 'Rings', price: '₹62,500', slug: 'aria-solitaire-ring' },
  { name: 'Luna Diamond Studs', category: 'Earrings', price: '₹28,900', slug: 'luna-diamond-studs' },
  { name: 'Priya Gold Necklace', category: 'Necklaces', price: '₹1,15,000', slug: 'priya-gold-necklace' },
  { name: 'Zara Tennis Bracelet', category: 'Bracelets', price: '₹78,000', slug: 'zara-tennis-bracelet' },
  { name: 'Maya Diamond Pendant', category: 'Pendants', price: '₹35,500', slug: 'maya-diamond-pendant' },
  { name: 'Kiara Gold Bangles', category: 'Bangles', price: '₹52,000', slug: 'kiara-gold-bangles' },
];

const testimonials = [
  {
    name: 'Priya M.',
    location: 'Gurgaon',
    text: 'Auric Jewels made my engagement ring shopping experience unforgettable. The team helped us choose the perfect solitaire with complete transparency on certification and pricing. Truly a premium experience.',
    rating: 5,
  },
  {
    name: 'Rahul & Sneha K.',
    location: 'Delhi NCR',
    text: 'We bought our complete bridal set from Auric Jewels. The quality of craftsmanship, the BIS hallmarking on every piece, and the personalised service made all the difference. Highly recommended for wedding jewellery.',
    rating: 5,
  },
  {
    name: 'Anita S.',
    location: 'Gurgaon',
    text: 'I have been buying daily wear diamond jewellery from Auric Jewels for two years now. Every piece comes with proper certification and the lifetime exchange policy gives me complete peace of mind.',
    rating: 5,
  },
  {
    name: 'Vikram T.',
    location: 'Noida',
    text: 'Finally found a jeweller who takes men\'s jewellery seriously. My platinum chain and diamond studs from Auric Jewels are exceptional quality. The showroom experience in Gurgaon was world-class.',
    rating: 5,
  },
];

const blogPosts = [
  {
    title: 'Best Diamond Jewellery Showroom in Gurgaon — Why Families Trust Auric Jewels',
    slug: 'best-diamond-jewellery-showroom-gurgaon',
    excerpt: 'Discover what makes a diamond showroom truly premium — from IGI/GIA certification to BIS hallmarked gold and transparent pricing.',
  },
  {
    title: 'Solitaire Ring Buying Guide Gurgaon — Cuts, Clarity & Price 2026',
    slug: 'solitaire-ring-buying-guide-gurgaon',
    excerpt: 'Everything you need to know before buying a solitaire ring — the 4Cs, popular cuts, realistic price ranges, and what to ask your jeweller.',
  },
  {
    title: 'How to Choose a Diamond Mangalsutra — Modern Designs 2026',
    slug: 'diamond-mangalsutra-modern-designs',
    excerpt: 'The modern mangalsutra blends tradition with contemporary style. Explore single-line pendants, sleek chains, and styling tips.',
  },
];

export default function HomePage() {
  return (
    <>
      <SEOHead
        title={homepageSEO.title}
        description={homepageSEO.description}
        canonical="/"
        structuredData={structuredData}
      />

      {/* ═══════════════════════════════════════════════════
          1. HERO SECTION
          ═══════════════════════════════════════════════════ */}
      <section className="hero">
        <div className="hero-overlay">
          <div className="hero-content">
            <h1 className="hero-h1">Luxury Gold &amp; Diamond Jewellery in Gurgaon</h1>
            <p className="hero-subtitle">
              Certified Diamonds&ensp;|&ensp;BIS Hallmarked Gold&ensp;|&ensp;Gurgaon Showroom
            </p>
            <div className="hero-ctas">
              <a href="/collections/best-sellers" className="btn btn-primary">Explore Collections</a>
              <a href="#showroom" className="btn btn-outline">Visit Our Showroom</a>
            </div>
          </div>
        </div>
      </section>

      {/* ═══════════════════════════════════════════════════
          2. TRUST BAR
          ═══════════════════════════════════════════════════ */}
      <section className="trust-bar">
        <div className="container">
          <div className="trust-grid">
            <div className="trust-item">
              <span className="trust-icon">◆</span>
              <span className="trust-text">IGI/GIA Certified Diamonds</span>
            </div>
            <div className="trust-item">
              <span className="trust-icon">✓</span>
              <span className="trust-text">BIS Hallmarked Gold</span>
            </div>
            <div className="trust-item">
              <span className="trust-icon">⬡</span>
              <span className="trust-text">Free Insured Shipping</span>
            </div>
            <div className="trust-item">
              <span className="trust-icon">↩</span>
              <span className="trust-text">15-Day Returns</span>
            </div>
            <div className="trust-item">
              <span className="trust-icon">◉</span>
              <span className="trust-text">Gurgaon Showroom</span>
            </div>
          </div>
        </div>
      </section>

      <main className="container">

        {/* ═══════════════════════════════════════════════════
            3. FEATURED CATEGORIES
            ═══════════════════════════════════════════════════ */}
        <section className="section categories-section">
          <h2 className="section-title">Shop by Category</h2>
          <p className="section-subtitle">Explore our handcrafted collections in certified diamonds and hallmarked gold</p>
          <div className="category-grid">
            {categories.map((cat) => (
              <a key={cat.slug} href={`/categories/${cat.slug}`} className="category-card">
                <div className="category-image-placeholder">
                  <span className="category-icon">{cat.icon}</span>
                </div>
                <span className="category-name">{cat.name}</span>
              </a>
            ))}
          </div>
        </section>

        {/* ═══════════════════════════════════════════════════
            4. BEST SELLERS
            ═══════════════════════════════════════════════════ */}
        <section className="section bestsellers-section">
          <h2 className="section-title">Best Sellers</h2>
          <p className="section-subtitle">Our most loved pieces — chosen by families across Gurgaon and Delhi NCR</p>
          <div className="product-grid">
            {bestSellers.map((product) => (
              <a key={product.slug} href={`/products/${product.slug}`} className="product-card">
                <div className="product-image-placeholder">
                  <span className="product-image-text">{product.category}</span>
                </div>
                <div className="product-info">
                  <h3 className="product-name">{product.name}</h3>
                  <p className="product-category">{product.category}</p>
                  <p className="product-price">{product.price}</p>
                </div>
              </a>
            ))}
          </div>
          <div className="section-cta">
            <a href="/collections/best-sellers" className="btn btn-primary">View All Best Sellers</a>
          </div>
        </section>

        {/* ═══════════════════════════════════════════════════
            5. WHY AURIC JEWELS — SEO text content
            ═══════════════════════════════════════════════════ */}
        <section className="section why-section">
          <h2 className="section-title">Why Families in Gurgaon Trust Auric Jewels</h2>
          <div className="why-content">
            <div className="why-text">
              <p>
                Auric Jewels is a premium gold and diamond jewellery destination in Gurgaon, Haryana,
                trusted by families across Delhi NCR for certified quality, transparent pricing, and
                exceptional craftsmanship. Every diamond in our collection is IGI or GIA certified,
                ensuring you receive complete documentation of cut, clarity, colour, and carat weight.
                Every piece of gold jewellery carries a BIS hallmark with a verifiable HUID number,
                guaranteeing the exact purity of 18K or 22K gold.
              </p>
              <p>
                Our Gurgaon showroom offers a private, personalised shopping experience — whether you
                are choosing an engagement ring, assembling a bridal set, selecting a Karva Chauth gift,
                or simply investing in everyday luxury. Unlike high-footfall chain showrooms, we offer
                one-on-one consultations with jewellery experts who understand your style, your occasion,
                and your budget.
              </p>
              <p>
                From solitaire rings and diamond earrings to gold necklaces, mangalsutras, and men&apos;s
                platinum jewellery, our curated collections blend traditional Indian heritage with
                contemporary design. Every purchase includes free insured shipping across India, a 15-day
                return policy, and lifetime exchange at full gold value — because your trust is the
                foundation of everything we do.
              </p>
            </div>
            <div className="why-stats">
              <div className="stat">
                <span className="stat-number">IGI/GIA</span>
                <span className="stat-label">Certified Diamonds</span>
              </div>
              <div className="stat">
                <span className="stat-number">BIS</span>
                <span className="stat-label">Hallmarked Gold</span>
              </div>
              <div className="stat">
                <span className="stat-number">7 Days</span>
                <span className="stat-label">Showroom Open</span>
              </div>
              <div className="stat">
                <span className="stat-number">Lifetime</span>
                <span className="stat-label">Exchange Policy</span>
              </div>
            </div>
          </div>
        </section>

        {/* ═══════════════════════════════════════════════════
            6. TESTIMONIALS
            ═══════════════════════════════════════════════════ */}
        <section className="section testimonials-section">
          <h2 className="section-title">What Our Customers Say</h2>
          <div className="testimonials-grid">
            {testimonials.map((t, i) => (
              <div key={i} className="testimonial-card">
                <div className="testimonial-stars">{'★'.repeat(t.rating)}</div>
                <p className="testimonial-text">&ldquo;{t.text}&rdquo;</p>
                <p className="testimonial-author">
                  <strong>{t.name}</strong> — {t.location}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* ═══════════════════════════════════════════════════
            7. FAQ SECTION — matches FAQPage schema for rich snippets
            ═══════════════════════════════════════════════════ */}
        <section className="section faq-section">
          <h2 className="section-title">Frequently Asked Questions</h2>
          <div className="faq-grid">
            <div className="faq-item">
              <h3>Where is the best jewellery showroom in Gurgaon?</h3>
              <p>Auric Jewels is a premium jewellery showroom in Gurgaon offering BIS hallmarked gold and IGI/GIA certified diamond jewellery. Visit our showroom for a personalised experience with expert consultations, transparent pricing, and lifetime exchange policy.</p>
            </div>
            <div className="faq-item">
              <h3>Does Auric Jewels sell BIS hallmarked gold jewellery?</h3>
              <p>Yes, every piece of gold jewellery at Auric Jewels carries a BIS hallmark with a verifiable HUID number, guaranteeing the exact purity of 18K or 22K gold. We are committed to 100% transparency in gold purity.</p>
            </div>
            <div className="faq-item">
              <h3>Are the diamonds at Auric Jewels certified?</h3>
              <p>Yes, every diamond used in our jewellery is IGI or GIA certified, ensuring exceptional cut, clarity, colour, and carat weight. Certification documents are provided with every diamond purchase.</p>
            </div>
            <div className="faq-item">
              <h3>Does Auric Jewels offer free shipping in India?</h3>
              <p>Yes, Auric Jewels offers free insured shipping across India on all orders. Every shipment is fully insured and tracked for your peace of mind. We also offer a 15-day easy return policy and lifetime exchange at full gold value.</p>
            </div>
            <div className="faq-item">
              <h3>Can I buy diamond engagement rings in Gurgaon from Auric Jewels?</h3>
              <p>Absolutely! Auric Jewels offers a stunning collection of diamond engagement rings in Gurgaon, including solitaire rings, halo rings, and custom designs. All diamonds are IGI/GIA certified. Visit our Gurgaon showroom or shop online with free shipping.</p>
            </div>
            <div className="faq-item">
              <h3>What is the return policy at Auric Jewels?</h3>
              <p>Auric Jewels offers a 15-day easy return policy on all purchases. We also offer lifetime exchange at full gold value, giving you complete peace of mind with every purchase.</p>
            </div>
          </div>
        </section>

        {/* ═══════════════════════════════════════════════════
            8. BLOG PREVIEW
            ═══════════════════════════════════════════════════ */}
        <section className="section blog-section">
          <h2 className="section-title">From Our Journal</h2>
          <p className="section-subtitle">Expert guides on diamonds, gold, and jewellery buying</p>
          <div className="blog-grid">
            {blogPosts.map((post) => (
              <a key={post.slug} href={`/blog/${post.slug}`} className="blog-card">
                <div className="blog-image-placeholder" />
                <div className="blog-info">
                  <h3 className="blog-title">{post.title}</h3>
                  <p className="blog-excerpt">{post.excerpt}</p>
                  <span className="blog-link">Read More →</span>
                </div>
              </a>
            ))}
          </div>
        </section>
      </main>

      {/* ═══════════════════════════════════════════════════
          8. FOOTER
          ═══════════════════════════════════════════════════ */}
      <footer className="footer" id="showroom">
        <div className="container">
          <div className="footer-grid">
            <div className="footer-col">
              <h3 className="footer-heading">Auric Jewels</h3>
              <p className="footer-text">
                Premium gold &amp; diamond jewellery in Gurgaon. Certified diamonds, BIS hallmarked
                gold, and a showroom experience designed for families who value trust and craftsmanship.
              </p>
            </div>
            <div className="footer-col">
              <h3 className="footer-heading">Visit Our Showroom</h3>
              <address className="footer-address">
                Auric Jewels<br />
                Gurgaon, Haryana, India<br /><br />
                <a href="tel:+919012495941">+91-9012495941</a><br />
                <a href="mailto:info@auricjewels.com">info@auricjewels.com</a><br /><br />
                Open 7 days a week<br />
                10:00 AM — 8:00 PM
              </address>
            </div>
            <div className="footer-col">
              <h3 className="footer-heading">Quick Links</h3>
              <nav aria-label="Footer navigation">
                <ul className="footer-links">
                  <li><a href="/categories/rings">Rings</a></li>
                  <li><a href="/categories/earrings">Earrings</a></li>
                  <li><a href="/categories/necklaces">Necklaces</a></li>
                  <li><a href="/categories/bracelets">Bracelets</a></li>
                  <li><a href="/categories/bangles">Bangles</a></li>
                  <li><a href="/collections/solitaire-collection">Solitaire Collection</a></li>
                  <li><a href="/collections/best-sellers">Best Sellers</a></li>
                </ul>
              </nav>
            </div>
            <div className="footer-col">
              <h3 className="footer-heading">Follow Us</h3>
              <div className="social-links">
                <a href="#" aria-label="Instagram" className="social-link">Instagram</a>
                <a href="#" aria-label="Facebook" className="social-link">Facebook</a>
                <a href="#" aria-label="YouTube" className="social-link">YouTube</a>
                <a href="#" aria-label="Pinterest" className="social-link">Pinterest</a>
              </div>
            </div>
          </div>
          {/* Areas We Serve — Local SEO for Gurgaon & Delhi NCR */}
          <div className="footer-col footer-areas">
            <h3 className="footer-heading">Areas We Serve</h3>
            <p className="footer-text">
              Gurgaon (Gurugram) | DLF Phase 1-5 | Golf Course Road | MG Road | Sohna Road |
              Cyber City | Sector 29 | Sector 14 | South City | Manesar |
              Delhi | Noida | Faridabad | Greater Noida | Ghaziabad | Delhi NCR
            </p>
          </div>

          <div className="footer-bottom">
            <p>&copy; 2026 Auric Jewels. All rights reserved. | BIS Hallmarked Gold | IGI/GIA Certified Diamonds | Jewellery Shop in Gurgaon</p>
          </div>
        </div>
      </footer>
    </>
  );
}

export async function getServerSideProps() {
  return { props: {} };
}
