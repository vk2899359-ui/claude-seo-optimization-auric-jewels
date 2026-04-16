import SEOHead from '../components/SEOHead';
import { SITE_URL } from '../lib/seo-config';

const showroomSchema = {
  '@context': 'https://schema.org',
  '@type': 'JewelryStore',
  'name': 'Auric Jewels',
  'image': `${SITE_URL}/images/showroom-hero.jpg`,
  '@id': `${SITE_URL}/luxury-jewellery-showroom-sector-45-gurgaon`,
  'url': `${SITE_URL}/luxury-jewellery-showroom-sector-45-gurgaon`,
  'telephone': '+919012495941',
  'priceRange': '\u20B9\u20B9\u20B9',
  'address': {
    '@type': 'PostalAddress',
    'streetAddress': 'Sector 45',
    'addressLocality': 'Gurgaon',
    'addressRegion': 'Haryana',
    'postalCode': '122003',
    'addressCountry': 'IN',
  },
  'geo': {
    '@type': 'GeoCoordinates',
    'latitude': 28.4485,
    'longitude': 77.0755,
  },
  'openingHoursSpecification': [
    {
      '@type': 'OpeningHoursSpecification',
      'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
      'opens': '11:00',
      'closes': '20:30',
    },
  ],
};

const breadcrumbData = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [
    { '@type': 'ListItem', position: 1, name: 'Home', item: SITE_URL },
    {
      '@type': 'ListItem',
      position: 2,
      name: 'Luxury Jewellery Showroom Sector 45 Gurgaon',
      item: `${SITE_URL}/luxury-jewellery-showroom-sector-45-gurgaon`,
    },
  ],
};

const faqData = [
  {
    question: 'Where is the Auric Jewels showroom located in Gurgaon?',
    answer: 'Auric Jewels is located in Sector 45, Gurgaon, Haryana 122003. The showroom is easily accessible from Golf Course Road, Sohna Road, and MG Road areas.',
  },
  {
    question: 'What are the showroom timings?',
    answer: 'The Auric Jewels showroom is open 7 days a week from 11:00 AM to 8:30 PM. Walk-ins are welcome, or you can book a private appointment by calling +91-9012495941.',
  },
  {
    question: 'Does Auric Jewels sell BIS hallmarked gold jewellery?',
    answer: 'Yes. Every piece of gold jewellery at Auric Jewels is BIS hallmarked with a verifiable HUID number, guaranteeing 18K or 22K gold purity as certified by the Bureau of Indian Standards.',
  },
  {
    question: 'Are the diamonds at Auric Jewels certified?',
    answer: 'Yes. All diamonds at Auric Jewels are IGI (International Gemological Institute) or GIA (Gemological Institute of America) certified, with detailed grading reports on cut, clarity, colour, and carat.',
  },
  {
    question: 'Does Auric Jewels offer custom jewellery design?',
    answer: 'Yes. We offer a full bespoke jewellery design service — from initial concept and CAD rendering to handcrafted production. Custom engagement rings, bridal sets, and heirloom redesigns are our specialities.',
  },
  {
    question: 'What is the return and exchange policy at Auric Jewels?',
    answer: 'We offer a 15-day return policy and lifetime exchange at full gold value. Every purchase comes with a certificate of authenticity and free insured shipping across India.',
  },
];

const faqSchema = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: faqData.map((faq) => ({
    '@type': 'Question',
    name: faq.question,
    acceptedAnswer: {
      '@type': 'Answer',
      text: faq.answer,
    },
  })),
};

export default function ShowroomPage() {
  const structuredData = [showroomSchema, breadcrumbData, faqSchema];

  return (
    <>
      <SEOHead
        title="Luxury Jewellery Showroom in Sector 45 Gurgaon | Auric Jewels"
        description="Visit Auric Jewels luxury jewellery showroom in Sector 45, Gurgaon. Certified diamonds, BIS hallmarked gold, solitaire collections & bridal sets. Open 7 days."
        canonical="/luxury-jewellery-showroom-sector-45-gurgaon"
        structuredData={structuredData}
      />

      <main>
        {/* Hero Section */}
        <section className="showroom-hero">
          <div className="showroom-hero-overlay">
            <div className="container">
              <nav className="breadcrumbs breadcrumbs-light" aria-label="Breadcrumb">
                <a href="/">Home</a> &gt; <span>Showroom — Sector 45, Gurgaon</span>
              </nav>
              <h1>Luxury Jewellery Showroom in Sector 45, Gurgaon</h1>
              <p className="showroom-hero-sub">
                Certified Diamonds&ensp;|&ensp;BIS Hallmarked Gold&ensp;|&ensp;Private Appointments
              </p>
              <div className="hero-ctas">
                <a href="tel:+919012495941" className="btn btn-primary">
                  Call +91-9012495941
                </a>
                <a href="#visit" className="btn btn-outline">
                  Plan Your Visit
                </a>
              </div>
            </div>
          </div>
        </section>

        <div className="container">
          {/* About Section */}
          <section className="section">
            <h2 className="section-title">About Auric Jewels — Gurgaon&apos;s Premier Jewellery Showroom</h2>
            <div className="showroom-about">
              <p>
                Auric Jewels is a premium gold and diamond jewellery showroom in Sector 45,
                Gurgaon, trusted by families across Delhi NCR for certified quality, transparent
                pricing, and exceptional craftsmanship. Our showroom offers an intimate,
                appointment-friendly shopping experience — a refreshing alternative to
                high-footfall chain stores.
              </p>
              <p>
                Every diamond in our collection is IGI or GIA certified, and every gold piece
                carries BIS hallmarking with a verifiable HUID number. From solitaire engagement
                rings and bridal necklace sets to daily wear earrings and men&apos;s platinum
                jewellery, our curated collections blend Indian heritage with contemporary design.
              </p>
              <p>
                Located in one of Gurgaon&apos;s most accessible sectors — just minutes from Golf
                Course Road, Sohna Road, and the Rapid Metro — our Sector 45 showroom is designed
                for families who value trust, privacy, and personalised attention.
              </p>
            </div>
          </section>

          {/* Collections Section */}
          <section className="section showroom-collections-section">
            <h2 className="section-title">Collections Available at Our Gurgaon Showroom</h2>
            <div className="showroom-collections">
              <div className="showroom-collection-card">
                <h3>Solitaire Collection</h3>
                <p>IGI/GIA certified solitaire rings, pendants &amp; studs from 0.30ct to 2.00ct+. Set in 18K/22K gold or platinum.</p>
                <a href="/collections/solitaire-collection" className="blog-link">Explore Solitaires →</a>
              </div>
              <div className="showroom-collection-card">
                <h3>Bridal Jewellery</h3>
                <p>Complete wedding sets — necklaces, earrings, bangles &amp; maang tikka in gold and diamond. Traditional &amp; contemporary styles.</p>
                <a href="/categories/necklaces" className="blog-link">Explore Bridal →</a>
              </div>
              <div className="showroom-collection-card">
                <h3>Daily Wear Diamonds</h3>
                <p>Lightweight diamond earrings, pendants &amp; bracelets designed for everyday elegance. Starting from &#8377;20,000.</p>
                <a href="/categories/earrings" className="blog-link">Explore Daily Wear →</a>
              </div>
              <div className="showroom-collection-card">
                <h3>Men&apos;s Jewellery</h3>
                <p>Diamond studs, platinum chains, gold bracelets &amp; rings crafted for the modern man. BIS hallmarked, certified stones.</p>
                <a href="/collections/for-him" className="blog-link">Explore For Him →</a>
              </div>
              <div className="showroom-collection-card">
                <h3>Gold Bangles &amp; Chains</h3>
                <p>22K &amp; 18K gold bangles, kadas &amp; chains for festive, bridal, and daily wear. Verified purity with HUID.</p>
                <a href="/categories/bangles" className="blog-link">Explore Gold →</a>
              </div>
              <div className="showroom-collection-card">
                <h3>Custom Bespoke Design</h3>
                <p>Create one-of-a-kind pieces — engagement rings, heirloom redesigns &amp; personalised jewellery from sketch to finished piece.</p>
                <a href="tel:+919012495941" className="blog-link">Enquire Now →</a>
              </div>
            </div>
          </section>

          {/* Why Visit Section */}
          <section className="section">
            <h2 className="section-title">Why Visit Our Sector 45 Gurgaon Showroom?</h2>
            <div className="showroom-why-grid">
              <div className="showroom-why-card">
                <h3>Certified Quality</h3>
                <p>Every diamond is IGI/GIA certified. Every gold piece is BIS hallmarked with HUID. No compromises on purity or authenticity.</p>
              </div>
              <div className="showroom-why-card">
                <h3>Private Experience</h3>
                <p>Book a one-on-one consultation with our jewellery experts. No crowds, no pressure — just personalised guidance at your pace.</p>
              </div>
              <div className="showroom-why-card">
                <h3>Transparent Pricing</h3>
                <p>Full cost breakdown — gold weight, diamond value, making charges, and GST. See exactly what you&apos;re paying for, with no hidden extras.</p>
              </div>
              <div className="showroom-why-card">
                <h3>Lifetime Exchange</h3>
                <p>Exchange your gold jewellery at full gold value, anytime. Upgrade your diamond solitaire whenever you&apos;re ready — pay only the difference.</p>
              </div>
              <div className="showroom-why-card">
                <h3>Convenient Location</h3>
                <p>Sector 45, Gurgaon — minutes from Golf Course Road, Sohna Road, MG Road &amp; Rapid Metro. Open 7 days, 11 AM to 8:30 PM.</p>
              </div>
              <div className="showroom-why-card">
                <h3>Free Shipping &amp; Returns</h3>
                <p>Free insured shipping across India. 15-day hassle-free returns. Certificate of authenticity with every purchase.</p>
              </div>
            </div>
          </section>

          {/* Visit Info Section */}
          <section className="section showroom-visit-section" id="visit">
            <h2 className="section-title">Plan Your Visit to Auric Jewels Gurgaon</h2>
            <div className="showroom-visit-grid">
              <div className="showroom-visit-info">
                <h3>Address</h3>
                <address>
                  Auric Jewels<br />
                  Sector 45, Gurgaon<br />
                  Haryana 122003, India
                </address>

                <h3>Showroom Hours</h3>
                <p>Open 7 days a week<br />11:00 AM — 8:30 PM</p>

                <h3>Contact</h3>
                <p>
                  Phone: <a href="tel:+919012495941">+91-9012495941</a><br />
                  Email: <a href="mailto:info@auricjewels.com">info@auricjewels.com</a><br />
                  Website: <a href="https://www.auricjewels.com">www.auricjewels.com</a>
                </p>

                <h3>Appointments</h3>
                <p>
                  Walk-ins are always welcome. For a private consultation, call or WhatsApp
                  us at <a href="tel:+919012495941">+91-9012495941</a> to book your preferred
                  time slot.
                </p>
              </div>
              <div className="showroom-visit-map">
                <h3>Directions</h3>
                <p>
                  <strong>From Golf Course Road:</strong> Take the Sector 45 exit, 3 minutes by car.<br />
                  <strong>From MG Road:</strong> Via Sikanderpur, approximately 10 minutes.<br />
                  <strong>From Sohna Road:</strong> Via Sector 49 Chowk, approximately 8 minutes.<br />
                  <strong>By Metro:</strong> HUDA City Centre station (Yellow Line), then 10 min auto/cab to Sector 45.
                </p>
                <p>Ample parking available near the showroom.</p>
              </div>
            </div>
          </section>

          {/* FAQ Section */}
          <section className="section">
            <h2 className="section-title">Frequently Asked Questions</h2>
            <div className="showroom-faq">
              {faqData.map((faq, i) => (
                <div key={i} className="showroom-faq-item">
                  <h3>{faq.question}</h3>
                  <p>{faq.answer}</p>
                </div>
              ))}
            </div>
          </section>
        </div>
      </main>
    </>
  );
}

export async function getStaticProps() {
  return { props: {} };
}
