import SEOHead from '../components/SEOHead';
import { homepageSEO, SITE_URL } from '../lib/seo-config';

const structuredData = {
  '@context': 'https://schema.org',
  '@type': 'JewelryStore',
  name: 'Auric Jewels',
  url: SITE_URL,
  image: `${SITE_URL}/logo.png`,
  description:
    'Premium gold & diamond jewellery store in Gurgaon. BIS hallmarked jewellery, certified diamonds, solitaire collection.',
  address: {
    '@type': 'PostalAddress',
    addressLocality: 'Gurgaon',
    addressRegion: 'Haryana',
    addressCountry: 'IN',
  },
  priceRange: '₹₹₹',
  telephone: '+91-9012495941',
  openingHours: 'Mo-Su 10:00-20:00',
};

const faqStructuredData = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'Where is the best jewellery showroom in Gurgaon?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Auric Jewels at 201 Greenwood Plaza, Sector 45, Gurugram is one of the finest jewellery showrooms in Gurgaon offering IGI certified diamonds and BIS hallmarked gold.',
      },
    },
    {
      '@type': 'Question',
      name: 'Does Auric Jewels sell BIS hallmarked gold jewellery?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes, all gold jewellery at Auric Jewels is BIS hallmarked in 18K and 22K purity with HUID verification.',
      },
    },
    {
      '@type': 'Question',
      name: 'Are the diamonds at Auric Jewels certified?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes, all diamonds are IGI or GIA certified with full grading reports.',
      },
    },
    {
      '@type': 'Question',
      name: 'Does Auric Jewels offer free shipping in India?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes, free insured shipping across India on all orders.',
      },
    },
    {
      '@type': 'Question',
      name: 'Can I buy diamond engagement rings from Auric Jewels in Gurgaon?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Yes, we have an extensive collection of solitaire and diamond engagement rings at our Sector 45 showroom.',
      },
    },
    {
      '@type': 'Question',
      name: "What is Auric Jewels' return and exchange policy?",
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'We offer a 15-day return policy and lifetime exchange at full gold value.',
      },
    },
  ],
};

const categories = [
  { name: 'Rings',     slug: 'rings',     icon: '💍' },
  { name: 'Earrings',  slug: 'earrings',  icon: '✦' },
  { name: 'Necklaces', slug: 'necklaces', icon: '◇' },
  { name: 'Pendants',  slug: 'pendants',  icon: '◆' },
  { name: 'Bracelets', slug: 'bracelets', icon: '○' },
  { name: 'Bangles',   slug: 'bangles',   icon: '◎' },
  { name: 'Chains',    slug: 'chains',    icon: '∞' },
];

const bestSellers = [
  { name: 'Aria Solitaire Ring',    category: 'Rings',     price: '₹62,500', slug: 'aria-solitaire-ring',    badge: 'Best Seller' },
  { name: 'Luna Diamond Studs',     category: 'Earrings',  price: '₹28,900', slug: 'luna-diamond-studs',     badge: 'New In' },
  { name: 'Priya Gold Necklace',    category: 'Necklaces', price: '₹1,15,000', slug: 'priya-gold-necklace', badge: 'Signature' },
  { name: 'Zara Tennis Bracelet',   category: 'Bracelets', price: '₹78,000', slug: 'zara-tennis-bracelet',   badge: 'Limited' },
  { name: 'Maya Diamond Pendant',   category: 'Pendants',  price: '₹35,500', slug: 'maya-diamond-pendant',   badge: 'Best Seller' },
  { name: 'Kiara Gold Bangles',     category: 'Bangles',   price: '₹52,000', slug: 'kiara-gold-bangles',     badge: 'Bridal' },
];

const testimonials = [
  {
    name: 'Priya M.', location: 'Gurgaon', rating: 5,
    text: 'Auric Jewels made my engagement ring shopping experience unforgettable. Complete transparency on certification and pricing. Truly a premium showroom experience.',
  },
  {
    name: 'Rahul & Sneha K.', location: 'Delhi NCR', rating: 5,
    text: 'We bought our complete bridal set here. The BIS hallmarking on every piece and the personalised service made all the difference. Highly recommended.',
  },
  {
    name: 'Anita S.', location: 'Gurgaon', rating: 5,
    text: 'Two years of buying daily-wear diamond jewellery from Auric Jewels. Every piece comes with proper certification and the lifetime exchange gives me complete peace of mind.',
  },
  {
    name: 'Vikram T.', location: 'Noida', rating: 5,
    text: "Finally a jeweller who takes men's jewellery seriously. My platinum chain and diamond studs are exceptional quality. World-class showroom experience.",
  },
];

const blogPosts = [
  {
    title: 'Best Diamond Jewellery Showroom in Gurgaon — Why Families Trust Auric Jewels',
    slug: 'best-diamond-jewellery-showroom-gurgaon',
    excerpt: 'Discover what makes a diamond showroom truly premium — IGI/GIA certification, BIS hallmarked gold and transparent pricing.',
    tag: 'Guide',
  },
  {
    title: 'Solitaire Ring Buying Guide Gurgaon — Cuts, Clarity & Price 2026',
    slug: 'solitaire-ring-buying-guide-gurgaon',
    excerpt: 'Everything you need to know before buying a solitaire ring — the 4Cs, popular cuts, realistic price ranges.',
    tag: 'Education',
  },
  {
    title: 'How to Choose a Diamond Mangalsutra — Modern Designs 2026',
    slug: 'diamond-mangalsutra-modern-designs',
    excerpt: 'The modern mangalsutra blends tradition with contemporary style. Explore single-line pendants and sleek chains.',
    tag: 'Trend',
  },
];

const TICKER_ITEMS = [
  { label: '24K Gold Rate — Gurgaon', value: '₹94,000 / 10g' },
  { label: '22K Gold Rate', value: '₹86,100 / 10g' },
  { label: '18K Gold Rate', value: '₹70,500 / 10g' },
  { label: 'Free Insured Shipping', value: 'Pan India' },
  { label: 'BIS Hallmarked', value: '18K & 22K' },
  { label: 'IGI / GIA Certified', value: 'Diamonds' },
  { label: 'Gurgaon Showroom', value: 'Sector 45 · Open 7 Days' },
];

export default function HomePage() {
  const tickerContent = [...TICKER_ITEMS, ...TICKER_ITEMS];

  return (
    <>
      <SEOHead
        title={homepageSEO.title}
        description={homepageSEO.description}
        canonical="/"
        structuredData={[structuredData, faqStructuredData]}
      />

      {/* ── 1. HERO ─────────────────────────────────────── */}
      <section className="hero">
        <div className="hero-bg-pattern" />
        <div className="hero-border-tl" />
        <div className="hero-border-br" />

        <div className="hero-content">
          <p className="hero-eyebrow">Gurgaon · Est. 2015 · BIS Hallmarked · IGI Certified</p>

          <div className="diamond-sep" style={{ marginBottom: '1.5rem' }}>
            <span>✦</span>
          </div>

          <h1 className="hero-h1">
            <em>Luxury</em> Gold &amp;<br />Diamond Jewellery
          </h1>

          <p className="hero-subtitle">
            Certified Diamonds&nbsp;&nbsp;·&nbsp;&nbsp;BIS Hallmarked Gold&nbsp;&nbsp;·&nbsp;&nbsp;Gurgaon Showroom
          </p>

          <div className="hero-ctas">
            <a href="/collections/best-sellers" className="btn btn-gold">Explore Collections</a>
            <a href="#showroom" className="btn btn-outline-white">Visit Showroom</a>
          </div>
        </div>

        <div className="hero-scroll-hint">
          <div className="hero-scroll-line" />
          <span>Scroll</span>
        </div>
      </section>

      {/* ── 2. GOLD RATE TICKER ──────────────────────────── */}
      <div className="ticker-bar">
        <div className="ticker-track">
          {tickerContent.map((item, i) => (
            <span key={i} className="ticker-item">
              <span className="ticker-label">{item.label}</span>
              <span className="ticker-sep">◆</span>
              {item.value}
              <span className="ticker-sep" style={{ marginLeft: '1.5rem' }}>|</span>
            </span>
          ))}
        </div>
      </div>

      {/* ── 3. TRUST BAR ─────────────────────────────────── */}
      <div className="trust-bar">
        <div className="container">
          <div className="trust-grid">
            {[
              { icon: '◆', label: 'IGI / GIA Certified Diamonds' },
              { icon: '✓', label: 'BIS Hallmarked Gold' },
              { icon: '↩', label: '15-Day Easy Returns' },
              { icon: '⬡', label: 'Free Insured Shipping' },
              { icon: '◉', label: 'Lifetime Exchange Policy' },
            ].map((t) => (
              <div key={t.label} className="trust-item">
                <span className="trust-icon">{t.icon}</span>
                <span className="trust-label">{t.label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── 4. COLLECTION SPOTLIGHT ─────────────────────── */}
      <div className="spotlight-grid">
        <div className="spotlight-panel spotlight-panel-dark">
          <div className="spotlight-bg" />
          <div className="spotlight-overlay" />
          <div className="spotlight-decorative" />
          <div className="spotlight-content">
            <p className="spotlight-tag">New Collection 2026</p>
            <h2 className="spotlight-title">Solitaire &amp;<br /><em>Bridal Jewellery</em></h2>
            <a href="/collections/solitaire-collection" className="spotlight-link">
              Explore Collection →
            </a>
          </div>
        </div>
        <div className="spotlight-panel spotlight-panel-gold">
          <div className="spotlight-bg" />
          <div className="spotlight-overlay" />
          <div className="spotlight-decorative" />
          <div className="spotlight-content">
            <p className="spotlight-tag">Timeless Heritage</p>
            <h2 className="spotlight-title">22K Gold<br /><em>Signature Pieces</em></h2>
            <a href="/collections/best-sellers" className="spotlight-link">
              Shop Best Sellers →
            </a>
          </div>
        </div>
      </div>

      {/* ── 5. CATEGORIES ────────────────────────────────── */}
      <section className="categories-section">
        <div className="container">
          <p className="section-label">Browse by Category</p>
          <div className="diamond-sep">
            <span>✦</span>
          </div>
          <h2 className="section-title" style={{ marginBottom: '3rem' }}>Our Collections</h2>
          <div className="category-grid">
            {categories.map((cat) => (
              <a key={cat.slug} href={`/categories/${cat.slug}`} className="category-card">
                <div className="category-circle">
                  <span className="category-icon">{cat.icon}</span>
                </div>
                <span className="category-name">{cat.name}</span>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* ── 6. BEST SELLERS ──────────────────────────────── */}
      <section className="bestsellers-section">
        <div className="container">
          <p className="section-label">Curated Picks</p>
          <div className="diamond-sep">
            <span>✦</span>
          </div>
          <h2 className="section-title" style={{ color: 'var(--charcoal)' }}>Best Sellers</h2>
          <p className="section-subtitle">
            Our most loved pieces — chosen by families across Gurgaon and Delhi NCR
          </p>
          <div className="product-grid">
            {bestSellers.map((product) => (
              <a key={product.slug} href={`/products/${product.slug}`} className="product-card">
                <div className="product-image-wrap">
                  <div className="product-image-placeholder">
                    <span className="product-image-text">{product.category}</span>
                  </div>
                  {product.badge && (
                    <span className="product-badge">{product.badge}</span>
                  )}
                </div>
                <div className="product-info">
                  <p className="product-category">{product.category}</p>
                  <h3 className="product-name">{product.name}</h3>
                  <div className="product-footer">
                    <p className="product-price">{product.price}</p>
                    <span className="product-arrow">→</span>
                  </div>
                </div>
              </a>
            ))}
          </div>
          <div className="section-cta">
            <a href="/collections/best-sellers" className="btn btn-dark">View All Collections</a>
          </div>
        </div>
      </section>

      {/* ── 7. WHY AURIC JEWELS ──────────────────────────── */}
      <section className="why-section" id="about">
        <div className="container">
          <div className="why-inner">
            <div>
              <p className="section-label-left">Our Promise</p>
              <div className="gold-rule-left" />
              <h2 className="section-title-left" style={{ color: 'var(--white)', marginBottom: '1.75rem' }}>
                Why Families in Gurgaon<br />Trust Auric Jewels
              </h2>
              <div className="why-text">
                <p>
                  Auric Jewels is a premium gold and diamond jewellery destination in Gurgaon, Haryana,
                  trusted by families across Delhi NCR for certified quality, transparent pricing, and
                  exceptional craftsmanship. Every diamond in our collection is IGI or GIA certified.
                  Every piece of gold jewellery carries a BIS hallmark with a verifiable HUID number.
                </p>
                <p>
                  Our Gurgaon showroom at Greenwood Plaza, Sector 45 offers a private, personalised
                  shopping experience — whether you are choosing an engagement ring, assembling a bridal
                  set, or selecting an anniversary gift. From solitaire rings and diamond earrings to
                  gold necklaces, mangalsutras, and men&apos;s platinum jewellery, our collections blend
                  traditional Indian heritage with contemporary design.
                </p>
              </div>
              <a href="/collections/best-sellers" className="btn btn-outline-gold" style={{ marginTop: '2rem' }}>Explore the Collection</a>
            </div>
            <div className="why-stats">
              {[
                { number: 'IGI/GIA', label: 'Certified Diamonds' },
                { number: 'BIS', label: 'Hallmarked Gold' },
                { number: '15-Day', label: 'Easy Returns' },
                { number: 'Lifetime', label: 'Exchange Policy' },
              ].map((s) => (
                <div key={s.label} className="stat-card">
                  <span className="stat-number">{s.number}</span>
                  <span className="stat-label">{s.label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── 8. CERTIFICATE BADGES ────────────────────────── */}
      <section className="cert-section">
        <div className="container">
          <div className="cert-grid">
            {[
              { icon: '◆', title: 'IGI / GIA', sub: 'Certified Diamonds' },
              { icon: '✓', title: 'BIS', sub: 'Hallmarked Gold · HUID' },
              { icon: '↩', title: '15-Day', sub: 'Easy Returns' },
              { icon: '◉', title: 'Lifetime', sub: 'Exchange at Gold Value' },
            ].map((b) => (
              <div key={b.title} className="cert-badge">
                <span className="cert-badge-icon">{b.icon}</span>
                <h3 className="cert-badge-title">{b.title}</h3>
                <span className="cert-badge-sub">{b.sub}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── 9. TESTIMONIALS ──────────────────────────────── */}
      <section className="testimonials-section">
        <div className="container">
          <p className="section-label">Customer Stories</p>
          <div className="diamond-sep">
            <span>✦</span>
          </div>
          <h2 className="section-title">What Our Customers Say</h2>
          <p className="section-subtitle">
            Trusted by thousands of families across Gurgaon and Delhi NCR
          </p>
          <div className="testimonials-grid">
            {testimonials.map((t, i) => (
              <div key={i} className="testimonial-card">
                <span className="testimonial-quote-mark">&ldquo;</span>
                <div className="testimonial-stars">{'★'.repeat(t.rating)}</div>
                <p className="testimonial-text">{t.text}</p>
                <div className="testimonial-author">
                  <strong>{t.name}</strong>
                  <span>{t.location}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── 10. BLOG ─────────────────────────────────────── */}
      <section className="blog-section">
        <div className="container">
          <p className="section-label">From Our Journal</p>
          <div className="diamond-sep">
            <span>✦</span>
          </div>
          <h2 className="section-title">Expert Jewellery Guides</h2>
          <p className="section-subtitle">
            Insights on diamonds, gold, and making the right purchase decision
          </p>
          <div className="blog-grid">
            {blogPosts.map((post) => (
              <a key={post.slug} href={`/blog/${post.slug}`} className="blog-card">
                <div className="blog-image-placeholder">
                  <span className="blog-image-label">{post.tag}</span>
                </div>
                <div className="blog-info">
                  <h3 className="blog-title">{post.title}</h3>
                  <p className="blog-excerpt">{post.excerpt}</p>
                  <span className="blog-link">Read Article →</span>
                </div>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* ── 11. FOOTER ───────────────────────────────────── */}
      <footer className="footer" id="showroom">
        <div className="container">
          <div className="footer-top">
            <div>
              <p className="footer-brand-name">Auric Jewels</p>
              <div className="footer-brand-line" />
              <p className="footer-text">
                Premium gold &amp; diamond jewellery in Gurgaon. Certified diamonds, BIS hallmarked
                gold, and a showroom experience designed for families who value trust and craftsmanship.
              </p>
            </div>

            <div>
              <h3 className="footer-heading">Showroom</h3>
              <address className="footer-address">
                Auric Jewels<br />
                Greenwood Plaza, Sector 45<br />
                Gurugram, Haryana<br /><br />
                <a href="tel:+919012495941">+91-9012495941</a><br />
                <a href="mailto:info@auricjewels.com">info@auricjewels.com</a><br /><br />
                Mon – Sun · 10 AM – 8 PM
              </address>
            </div>

            <div>
              <h3 className="footer-heading">Collections</h3>
              <ul className="footer-links">
                <li><a href="/categories/rings">Rings</a></li>
                <li><a href="/categories/earrings">Earrings</a></li>
                <li><a href="/categories/necklaces">Necklaces</a></li>
                <li><a href="/categories/bracelets">Bracelets</a></li>
                <li><a href="/categories/bangles">Bangles</a></li>
                <li><a href="/collections/solitaire-collection">Solitaire Collection</a></li>
                <li><a href="/collections/best-sellers">Best Sellers</a></li>
              </ul>
            </div>

            <div>
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
            <p className="footer-copy">&copy; 2026 Auric Jewels. All rights reserved.</p>
            <span className="footer-cert-line">BIS Hallmarked Gold · IGI / GIA Certified Diamonds · HUID Verified</span>
          </div>
        </div>
      </footer>
    </>
  );
}

export async function getServerSideProps() {
  return { props: {} };
}
