import SEOHead from '../components/SEOHead';
import { homepageSEO, SITE_URL } from '../lib/seo-config';

const jewelryStoreSchema = {
  '@context': 'https://schema.org',
  '@type': 'JewelryStore',
  name: 'Auric Jewels',
  url: SITE_URL,
  image: `${SITE_URL}/logo.png`,
  description:
    'Premium gold & diamond jewellery store in Gurgaon. BIS hallmarked jewellery, certified diamonds, solitaire collection.',
  address: {
    '@type': 'PostalAddress',
    streetAddress: 'Greenwood Plaza, Sector 45',
    addressLocality: 'Gurugram',
    addressRegion: 'Haryana',
    postalCode: '122003',
    addressCountry: 'IN',
  },
  priceRange: '\u20B9\u20B9\u20B9',
  telephone: '+91-79060-81795',
  openingHours: 'Mo-Su 10:00-21:00',
};

const homepageFaqItems = [
  {
    q: 'Where is Auric Jewels located?',
    a: 'Auric Jewels is located at Greenwood Plaza, Sector 45, Gurugram, Haryana 122003. We are open 7 days a week from 10 AM to 9 PM.',
  },
  {
    q: 'What gold karats does Auric Jewels offer?',
    a: 'Auric Jewels offers 18K and 22K BIS hallmarked gold jewellery. Each piece carries a verifiable HUID number guaranteeing gold purity.',
  },
  {
    q: 'Does Auric Jewels offer diamond jewellery?',
    a: 'Yes. Auric Jewels offers a wide range of IGI and GIA certified diamond jewellery \u2014 including solitaire rings, diamond earrings, necklaces, bracelets, and bridal sets.',
  },
  {
    q: 'What is the price range at Auric Jewels?',
    a: 'Our collection ranges from \u20B920,000 for everyday diamond jewellery to \u20B92,00,000 and above for bridal sets and solitaire pieces. We offer transparent pricing with no hidden charges.',
  },
  {
    q: 'Is Auric Jewels a certified jeweller?',
    a: 'Yes. Auric Jewels is a BIS hallmarked jeweller. All gold jewellery carries BIS certification and all diamonds come with IGI or GIA grading reports, ensuring complete quality assurance.',
  },
];

const faqSchema = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: homepageFaqItems.map(({ q, a }) => ({
    '@type': 'Question',
    name: q,
    acceptedAnswer: { '@type': 'Answer', text: a },
  })),
};

const structuredData = [jewelryStoreSchema, faqSchema];

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
            7. BLOG PREVIEW
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
        {/* ═══════════════════════════════════════════════════
            8. FAQ SECTION
            ═══════════════════════════════════════════════════ */}
        <section className="section faq-section">
          <h2 className="section-title">Frequently Asked Questions</h2>
          <div className="faq-list">
            {homepageFaqItems.map(({ q, a }, i) => (
              <details key={i} className="faq-item">
                <summary className="faq-question">{q}</summary>
                <p className="faq-answer">{a}</p>
              </details>
            ))}
          </div>
        </section>

      </main>

      {/* ═══════════════════════════════════════════════════
          9. FOOTER
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
          <div className="footer-bottom">
            <p>&copy; 2026 Auric Jewels. All rights reserved. | BIS Hallmarked Gold | IGI/GIA Certified Diamonds</p>
          </div>
        </div>
      </footer>
    </>
  );
}

export async function getServerSideProps() {
  return { props: {} };
}
