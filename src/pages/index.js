import SEOHead from '../components/SEOHead';
import { homepageSEO, SITE_URL } from '../lib/seo-config';

const structuredData = {
  '@context': 'https://schema.org',
  '@type': 'JewelryStore',
  '@id': `${SITE_URL}/#jewellerystore`,
  name: 'Auric Jewels',
  alternateName: 'Auric Jewels Gurgaon',
  url: SITE_URL,
  image: [
    `${SITE_URL}/logo.png`,
    `${SITE_URL}/images/auric-jewels-showroom.jpg`,
    `${SITE_URL}/images/auric-jewels-og.jpg`,
  ],
  logo: {
    '@type': 'ImageObject',
    url: `${SITE_URL}/logo.png`,
    width: 512,
    height: 512,
  },
  description:
    'Auric Jewels is a premium gold and diamond jewellery showroom in Sector 45, Gurgaon, Haryana. Shop from \u20B950Cr+ inventory of BIS hallmarked gold jewellery and IGI/GIA certified diamond jewellery including rings, earrings, necklaces, pendants, chains, bracelets, bangles, and mangalsutra.',
  address: {
    '@type': 'PostalAddress',
    streetAddress: 'Sector 45',
    addressLocality: 'Gurgaon',
    addressRegion: 'Haryana',
    postalCode: '122003',
    addressCountry: 'IN',
  },
  geo: {
    '@type': 'GeoCoordinates',
    latitude: 28.4595,
    longitude: 77.0266,
  },
  telephone: '+919012495941',
  email: 'info@auricjewels.com',
  priceRange: '\u20B9\u20B9\u20B9\u20B9',
  currenciesAccepted: 'INR',
  paymentAccepted: 'Cash, Credit Card, Debit Card, UPI',
  openingHours: 'Mo-Su 10:00-20:00',
  openingHoursSpecification: [
    {
      '@type': 'OpeningHoursSpecification',
      dayOfWeek: [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday',
      ],
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
    name: 'Auric Jewels Jewellery Collection',
    itemListElement: [
      {
        '@type': 'OfferCatalog',
        name: 'Rings',
        url: `${SITE_URL}/categories/rings`,
        itemListElement: [
          {
            '@type': 'Offer',
            itemOffered: {
              '@type': 'Product',
              name: 'Gold & Diamond Rings',
              description: 'Engagement rings, solitaire rings, and daily wear rings in BIS hallmarked gold with IGI/GIA certified diamonds.',
            },
          },
        ],
      },
      {
        '@type': 'OfferCatalog',
        name: 'Earrings',
        url: `${SITE_URL}/categories/earrings`,
        itemListElement: [
          {
            '@type': 'Offer',
            itemOffered: {
              '@type': 'Product',
              name: 'Diamond & Gold Earrings',
              description: 'Designer studs, hoops, drops, and jhumkas in hallmarked gold with certified diamonds.',
            },
          },
        ],
      },
      {
        '@type': 'OfferCatalog',
        name: 'Necklaces',
        url: `${SITE_URL}/categories/necklaces`,
        itemListElement: [
          {
            '@type': 'Offer',
            itemOffered: {
              '@type': 'Product',
              name: 'Gold & Diamond Necklaces',
              description: 'Bridal necklace sets, chokers, and statement necklaces in hallmarked gold.',
            },
          },
        ],
      },
      {
        '@type': 'OfferCatalog',
        name: 'Pendants',
        url: `${SITE_URL}/categories/pendants`,
        itemListElement: [
          {
            '@type': 'Offer',
            itemOffered: {
              '@type': 'Product',
              name: 'Diamond & Gold Pendants',
              description: 'Solitaire, heart, and floral diamond pendants in 18K and 22K hallmarked gold.',
            },
          },
        ],
      },
      {
        '@type': 'OfferCatalog',
        name: 'Chains',
        url: `${SITE_URL}/categories/chains`,
        itemListElement: [
          {
            '@type': 'Offer',
            itemOffered: {
              '@type': 'Product',
              name: 'Gold Chains',
              description: 'Gold chains for women and men in 18KT and 22KT BIS hallmarked gold.',
            },
          },
        ],
      },
      {
        '@type': 'OfferCatalog',
        name: 'Bracelets',
        url: `${SITE_URL}/categories/bracelets`,
        itemListElement: [
          {
            '@type': 'Offer',
            itemOffered: {
              '@type': 'Product',
              name: 'Diamond & Gold Bracelets',
              description: 'Tennis bracelets, chain bracelets, and diamond bracelets in hallmarked gold.',
            },
          },
        ],
      },
      {
        '@type': 'OfferCatalog',
        name: 'Bangles',
        url: `${SITE_URL}/categories/bangles`,
        itemListElement: [
          {
            '@type': 'Offer',
            itemOffered: {
              '@type': 'Product',
              name: 'Gold & Diamond Bangles',
              description: 'Daily wear and bridal bangles in BIS hallmarked gold with certified diamonds.',
            },
          },
        ],
      },
      {
        '@type': 'OfferCatalog',
        name: 'Mangalsutra',
        url: `${SITE_URL}/categories/mangalsutra`,
        itemListElement: [
          {
            '@type': 'Offer',
            itemOffered: {
              '@type': 'Product',
              name: 'Diamond Mangalsutra',
              description: 'Modern and traditional diamond mangalsutra designs in 18K and 22K hallmarked gold.',
            },
          },
        ],
      },
    ],
  },
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: '4.9',
    reviewCount: '320',
    bestRating: '5',
    worstRating: '1',
  },
  areaServed: [
    {
      '@type': 'City',
      name: 'Gurgaon',
      sameAs: 'https://en.wikipedia.org/wiki/Gurgaon',
    },
    {
      '@type': 'Place',
      name: 'Delhi NCR',
      description: 'National Capital Region including Delhi, Noida, Faridabad, and Ghaziabad',
    },
  ],
  knowsAbout: [
    'Gold Jewellery',
    'Diamond Jewellery',
    'BIS Hallmarked Gold',
    'IGI Certified Diamonds',
    'GIA Certified Diamonds',
    'Solitaire Rings',
    'Bridal Jewellery',
    'Wedding Jewellery',
  ],
  slogan: 'Certified Diamonds. Hallmarked Gold. Trusted by Families.',
  foundingDate: '2020',
  numberOfEmployees: {
    '@type': 'QuantitativeValue',
    minValue: 10,
    maxValue: 50,
  },
  isAccessibleForFree: true,
  publicAccess: true,
};

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
