import { useEffect, useState } from 'react';
import SEOHead from '../components/SEOHead';
import { SITE_URL } from '../lib/seo-config';

const AKSHAYA_TRITIYA_DATE = new Date('2026-04-30T06:00:00+05:30');

const offers = [
  { title: 'Making Charges Waiver', detail: 'Up to 50% off on making charges on all gold jewellery', icon: '✦' },
  { title: 'Diamond Jewellery Special', detail: 'Flat 20% off on making charges + free IGI certification on solitaires', icon: '◆' },
  { title: 'Gold Rate Lock-In', detail: 'Pay 10% advance today, lock current gold rate for April 30', icon: '◎' },
  { title: 'Gold Coins at Best Price', detail: '24K BIS certified gold coins — 1g, 5g, 10g, 20g at lowest premium', icon: '○' },
  { title: 'Lifetime Exchange', detail: 'Full gold value exchange on every Akshaya Tritiya purchase', icon: '∞' },
  { title: 'Free Gift Packaging', detail: 'Premium gift box + certificate of authenticity on all purchases', icon: '◇' },
];

const collections = [
  { name: 'Gold Bangles', desc: 'Starting ₹40,000', link: '/categories/bangles' },
  { name: 'Diamond Necklaces', desc: 'Starting ₹75,000', link: '/categories/necklaces' },
  { name: 'Solitaire Rings', desc: 'Starting ₹45,000', link: '/collections/solitaire-collection' },
  { name: 'Gold Chains', desc: 'Starting ₹25,000', link: '/categories/chains' },
  { name: 'Diamond Earrings', desc: 'Starting ₹18,000', link: '/categories/earrings' },
  { name: 'Gold Coins', desc: 'Starting ₹15,500', link: '/categories/bangles' },
];

const structuredData = {
  '@context': 'https://schema.org',
  '@type': 'Event',
  name: 'Akshaya Tritiya 2026 Jewellery Sale — Auric Jewels Gurgaon',
  description: 'Akshaya Tritiya 2026 special offers at Auric Jewels. Up to 50% off on making charges, gold rate lock-in, free IGI certification on solitaires. Visit our Sector 45, Gurgaon showroom.',
  startDate: '2026-04-23',
  endDate: '2026-04-30',
  eventStatus: 'https://schema.org/EventScheduled',
  eventAttendanceMode: 'https://schema.org/OfflineEventAttendanceMode',
  location: {
    '@type': 'Place',
    name: 'Auric Jewels',
    address: {
      '@type': 'PostalAddress',
      streetAddress: '201, Greenwood Plaza, Greenwood City',
      addressLocality: 'Gurugram',
      addressRegion: 'Haryana',
      postalCode: '122003',
      addressCountry: 'IN',
    },
  },
  organizer: {
    '@type': 'JewelryStore',
    name: 'Auric Jewels',
    url: SITE_URL,
    telephone: '+91-9012495941',
    address: {
      '@type': 'PostalAddress',
      streetAddress: '201, Greenwood Plaza, Greenwood City, Sector 45',
      addressLocality: 'Gurugram',
      addressRegion: 'Haryana',
      postalCode: '122003',
      addressCountry: 'IN',
    },
    geo: {
      '@type': 'GeoCoordinates',
      latitude: '28.4595',
      longitude: '77.0266',
    },
    openingHoursSpecification: {
      '@type': 'OpeningHoursSpecification',
      dayOfWeek: ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],
      opens: '10:00',
      closes: '20:00',
    },
    priceRange: '₹₹₹',
    image: `${SITE_URL}/logo.png`,
    sameAs: [
      'https://www.instagram.com/auricjewels/',
      'https://www.facebook.com/auricjewels/',
    ],
  },
  offers: {
    '@type': 'Offer',
    name: 'Akshaya Tritiya Making Charges Waiver',
    description: 'Up to 50% off on making charges on gold and diamond jewellery',
    validFrom: '2026-04-23',
    validThrough: '2026-04-30',
    availability: 'https://schema.org/InStock',
  },
};

const localBusinessSchema = {
  '@context': 'https://schema.org',
  '@type': 'JewelryStore',
  '@id': `${SITE_URL}/#jewelry-store`,
  name: 'Auric Jewels',
  alternateName: 'Auric Jewels Gurgaon',
  url: SITE_URL,
  telephone: '+91-9012495941',
  email: 'info@auricjewels.com',
  description: 'Premium gold & diamond jewellery store in Sector 45, Gurugram. BIS hallmarked gold, IGI/GIA certified diamonds, solitaire collection, bridal jewellery, and custom design service.',
  image: `${SITE_URL}/logo.png`,
  logo: `${SITE_URL}/logo.png`,
  address: {
    '@type': 'PostalAddress',
    streetAddress: '201, Greenwood Plaza, Greenwood City, Sector 45',
    addressLocality: 'Gurugram',
    addressRegion: 'Haryana',
    postalCode: '122003',
    addressCountry: 'IN',
  },
  geo: {
    '@type': 'GeoCoordinates',
    latitude: '28.4595',
    longitude: '77.0266',
  },
  openingHoursSpecification: [
    {
      '@type': 'OpeningHoursSpecification',
      dayOfWeek: ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],
      opens: '10:00',
      closes: '20:00',
    },
  ],
  priceRange: '₹₹₹',
  currenciesAccepted: 'INR',
  paymentAccepted: 'Cash, Credit Card, Debit Card, UPI, Net Banking',
  areaServed: [
    { '@type': 'City', name: 'Gurugram' },
    { '@type': 'City', name: 'Delhi' },
    { '@type': 'City', name: 'Noida' },
  ],
  hasOfferCatalog: {
    '@type': 'OfferCatalog',
    name: 'Auric Jewels Collections',
    itemListElement: [
      { '@type': 'OfferCatalog', name: 'Diamond Rings' },
      { '@type': 'OfferCatalog', name: 'Gold Necklaces' },
      { '@type': 'OfferCatalog', name: 'Bridal Jewellery' },
      { '@type': 'OfferCatalog', name: 'Solitaire Collection' },
      { '@type': 'OfferCatalog', name: 'Gold Bangles' },
      { '@type': 'OfferCatalog', name: 'Diamond Earrings' },
    ],
  },
  sameAs: [
    'https://www.instagram.com/auricjewels/',
    'https://www.facebook.com/auricjewels/',
  ],
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: '4.9',
    reviewCount: '127',
    bestRating: '5',
  },
};

function Countdown() {
  const [time, setTime] = useState({ days: 0, hours: 0, minutes: 0, seconds: 0 });
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const tick = () => {
      const now = new Date();
      const diff = AKSHAYA_TRITIYA_DATE - now;
      if (diff <= 0) {
        setTime({ days: 0, hours: 0, minutes: 0, seconds: 0 });
        return;
      }
      setTime({
        days: Math.floor(diff / 86400000),
        hours: Math.floor((diff % 86400000) / 3600000),
        minutes: Math.floor((diff % 3600000) / 60000),
        seconds: Math.floor((diff % 60000) / 1000),
      });
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, []);

  if (!mounted) return null;

  return (
    <div className="at-countdown">
      {[
        { label: 'Days', value: time.days },
        { label: 'Hours', value: time.hours },
        { label: 'Minutes', value: time.minutes },
        { label: 'Seconds', value: time.seconds },
      ].map((unit) => (
        <div key={unit.label} className="at-countdown-unit">
          <span className="at-countdown-num">{String(unit.value).padStart(2, '0')}</span>
          <span className="at-countdown-label">{unit.label}</span>
        </div>
      ))}
    </div>
  );
}

export default function AkshayaTritiya() {
  const combinedSchema = [structuredData, localBusinessSchema];

  return (
    <>
      <SEOHead
        title="Akshaya Tritiya 2026 Jewellery Offers | Up to 50% Off Making Charges | Auric Jewels Gurgaon"
        description="Akshaya Tritiya 2026 special offers at Auric Jewels, Sector 45 Gurgaon. Up to 50% off making charges, gold rate lock-in, free IGI certification. BIS hallmarked gold & certified diamonds. Visit 201, Greenwood Plaza."
        canonical="/akshaya-tritiya-2026"
        structuredData={combinedSchema}
      />

      {/* Hero Section */}
      <section className="at-hero">
        <div className="container">
          <div className="at-hero-badge">Limited Time Offer</div>
          <h1 className="at-hero-title">Akshaya Tritiya 2026</h1>
          <p className="at-hero-subtitle">The Most Auspicious Day to Buy Gold & Diamond Jewellery</p>
          <p className="at-hero-date">Wednesday, April 30, 2026</p>
          <Countdown />
          <div className="at-hero-ctas">
            <a href="tel:+919012495941" className="at-btn at-btn-gold">
              Call Now: +91 90124 95941
            </a>
            <a href="https://wa.me/919012495941?text=Hi%20Auric%20Jewels!%20I%20am%20interested%20in%20Akshaya%20Tritiya%20offers" className="at-btn at-btn-outline" target="_blank" rel="noopener noreferrer">
              WhatsApp Enquiry
            </a>
          </div>
        </div>
      </section>

      {/* Offers Section */}
      <section className="at-offers section">
        <div className="container">
          <h2 className="section-title">Akshaya Tritiya Exclusive Offers</h2>
          <p className="section-subtitle">Available April 23 — April 30, 2026 at our Sector 45, Gurgaon showroom</p>
          <div className="at-offers-grid">
            {offers.map((offer) => (
              <div key={offer.title} className="at-offer-card">
                <span className="at-offer-icon">{offer.icon}</span>
                <h3>{offer.title}</h3>
                <p>{offer.detail}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Gold Rate Section */}
      <section className="at-gold-rate section" style={{ background: 'var(--cream)' }}>
        <div className="container">
          <h2 className="section-title">Today's Gold Rate — Lock It Now</h2>
          <p className="section-subtitle">Gold prices are at historic highs. Lock today's rate with just 10% advance.</p>
          <div className="at-rate-cards">
            <div className="at-rate-card">
              <h3>24K Gold</h3>
              <p className="at-rate-price">~₹15,500/gram</p>
              <p className="at-rate-note">₹1,55,000 per 10 grams</p>
              <p>Best for: Coins & investment</p>
            </div>
            <div className="at-rate-card at-rate-featured">
              <div className="at-rate-badge">Most Popular</div>
              <h3>22K Gold</h3>
              <p className="at-rate-price">~₹14,200/gram</p>
              <p className="at-rate-note">₹1,42,000 per 10 grams</p>
              <p>Best for: Bangles, chains, traditional jewellery</p>
            </div>
            <div className="at-rate-card">
              <h3>18K Gold</h3>
              <p className="at-rate-price">~₹11,650/gram</p>
              <p className="at-rate-note">₹1,16,500 per 10 grams</p>
              <p>Best for: Diamond jewellery & daily wear</p>
            </div>
          </div>
          <div style={{ textAlign: 'center', marginTop: '2rem' }}>
            <a href="tel:+919012495941" className="at-btn at-btn-gold">Lock Gold Rate — Call Now</a>
          </div>
        </div>
      </section>

      {/* Collections Section */}
      <section className="at-collections section">
        <div className="container">
          <h2 className="section-title">Shop by Collection</h2>
          <p className="section-subtitle">Curated for Akshaya Tritiya — BIS hallmarked gold, IGI/GIA certified diamonds</p>
          <div className="at-collections-grid">
            {collections.map((c) => (
              <a key={c.name} href={c.link} className="at-collection-card">
                <h3>{c.name}</h3>
                <p>{c.desc}</p>
                <span className="at-collection-arrow">Browse Collection →</span>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* Why Auric Section */}
      <section className="at-why section" style={{ background: 'var(--navy)', color: 'var(--cream)' }}>
        <div className="container">
          <h2 className="section-title" style={{ color: 'var(--gold)' }}>Why Buy from Auric Jewels This Akshaya Tritiya?</h2>
          <div className="at-why-grid">
            <div className="at-why-item">
              <h3>BIS Hallmarked Gold</h3>
              <p>Every piece carries BIS hallmark with HUID. Verified purity on every purchase.</p>
            </div>
            <div className="at-why-item">
              <h3>IGI/GIA Certified Diamonds</h3>
              <p>Every diamond above 0.20 ct has independent certification. No exceptions.</p>
            </div>
            <div className="at-why-item">
              <h3>Lowest Making Charges</h3>
              <p>Starting 8% — significantly lower than chain retailers charging 14-20%.</p>
            </div>
            <div className="at-why-item">
              <h3>Lifetime Exchange</h3>
              <p>Full gold value exchange, any time, no conditions. Your investment is never stuck.</p>
            </div>
            <div className="at-why-item">
              <h3>Personal Consultation</h3>
              <p>Private, unhurried shopping. One-on-one attention from jewellery specialists.</p>
            </div>
            <div className="at-why-item">
              <h3>Transparent Pricing</h3>
              <p>Itemised billing: gold weight, diamond value, making charges, GST — all separate.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Visit Section */}
      <section className="at-visit section">
        <div className="container" style={{ textAlign: 'center' }}>
          <h2 className="section-title">Visit Our Showroom</h2>
          <div className="at-visit-address">
            <p><strong>Auric Jewels</strong></p>
            <p>201, Greenwood Plaza, Greenwood City</p>
            <p>Sector 45, Gurugram, Haryana — 122003</p>
            <p style={{ marginTop: '1rem' }}>Open 10 AM — 8 PM, Seven Days a Week</p>
            <p>Extended hours during Akshaya Tritiya week: 10 AM — 9 PM</p>
          </div>
          <div className="at-hero-ctas" style={{ marginTop: '2rem' }}>
            <a href="tel:+919012495941" className="at-btn at-btn-gold">
              Call: +91 90124 95941
            </a>
            <a href="https://wa.me/919012495941?text=Hi!%20I%20want%20to%20visit%20for%20Akshaya%20Tritiya%20shopping" className="at-btn at-btn-outline" target="_blank" rel="noopener noreferrer">
              Book Appointment on WhatsApp
            </a>
            <a href="https://maps.google.com/?q=Auric+Jewels+Greenwood+Plaza+Sector+45+Gurugram" className="at-btn at-btn-outline" target="_blank" rel="noopener noreferrer">
              Get Directions
            </a>
          </div>
        </div>
      </section>

      <style jsx>{`
        .at-hero {
          background: linear-gradient(135deg, var(--navy) 0%, var(--navy-deep) 100%);
          color: var(--cream);
          text-align: center;
          padding: 5rem 0 4rem;
          position: relative;
          overflow: hidden;
        }
        .at-hero::before {
          content: '';
          position: absolute;
          top: -50%;
          left: -50%;
          width: 200%;
          height: 200%;
          background: radial-gradient(circle at 30% 50%, rgba(201,161,74,0.08) 0%, transparent 50%);
          pointer-events: none;
        }
        .at-hero-badge {
          display: inline-block;
          background: rgba(201,161,74,0.15);
          color: var(--gold);
          padding: 0.4rem 1.2rem;
          border-radius: 50px;
          font-size: 0.85rem;
          font-weight: 600;
          letter-spacing: 0.05em;
          text-transform: uppercase;
          margin-bottom: 1.5rem;
          border: 1px solid rgba(201,161,74,0.3);
        }
        .at-hero-title {
          font-family: 'Playfair Display', Georgia, serif;
          font-size: clamp(2.5rem, 6vw, 4rem);
          font-weight: 700;
          color: var(--gold);
          margin-bottom: 0.5rem;
          line-height: 1.1;
        }
        .at-hero-subtitle {
          font-size: clamp(1rem, 2.5vw, 1.35rem);
          color: rgba(250,248,244,0.7);
          margin-bottom: 0.25rem;
          max-width: 600px;
          margin-left: auto;
          margin-right: auto;
        }
        .at-hero-date {
          font-size: 1.1rem;
          color: var(--gold-light);
          font-weight: 600;
          margin-bottom: 2rem;
        }
        .at-countdown {
          display: flex;
          justify-content: center;
          gap: 1rem;
          margin-bottom: 2.5rem;
        }
        .at-countdown-unit {
          background: rgba(255,255,255,0.06);
          border: 1px solid rgba(201,161,74,0.25);
          border-radius: 12px;
          padding: 1rem 1.25rem;
          min-width: 80px;
        }
        .at-countdown-num {
          display: block;
          font-size: 2rem;
          font-weight: 700;
          color: var(--gold);
          line-height: 1;
        }
        .at-countdown-label {
          display: block;
          font-size: 0.75rem;
          color: rgba(250,248,244,0.5);
          text-transform: uppercase;
          letter-spacing: 0.05em;
          margin-top: 0.3rem;
        }
        .at-hero-ctas {
          display: flex;
          gap: 1rem;
          justify-content: center;
          flex-wrap: wrap;
        }
        .at-btn {
          display: inline-block;
          padding: 0.9rem 2rem;
          border-radius: 50px;
          font-weight: 700;
          font-size: 1rem;
          cursor: pointer;
          transition: all 0.3s;
          text-align: center;
        }
        .at-btn-gold {
          background: linear-gradient(135deg, var(--gold), var(--gold-light));
          color: var(--navy);
          border: none;
        }
        .at-btn-gold:hover {
          box-shadow: 0 8px 24px rgba(201,161,74,0.4);
          transform: translateY(-2px);
        }
        .at-btn-outline {
          background: transparent;
          color: var(--gold);
          border: 2px solid var(--gold);
        }
        .at-btn-outline:hover {
          background: rgba(201,161,74,0.1);
        }
        .section-subtitle {
          text-align: center;
          color: var(--text-muted);
          font-size: 1.05rem;
          margin-bottom: 3rem;
          max-width: 600px;
          margin-left: auto;
          margin-right: auto;
        }
        .at-offers-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 1.5rem;
        }
        .at-offer-card {
          background: var(--white);
          border: 1px solid var(--cream-dark);
          border-radius: var(--radius);
          padding: 2rem;
          transition: all 0.3s;
        }
        .at-offer-card:hover {
          border-color: var(--gold);
          box-shadow: 0 8px 24px rgba(201,161,74,0.1);
          transform: translateY(-3px);
        }
        .at-offer-icon {
          font-size: 1.5rem;
          color: var(--gold);
          display: block;
          margin-bottom: 0.75rem;
        }
        .at-offer-card h3 {
          font-size: 1.15rem;
          color: var(--navy);
          margin-bottom: 0.5rem;
        }
        .at-offer-card p {
          color: var(--text-muted);
          font-size: 0.95rem;
          line-height: 1.5;
        }
        .at-rate-cards {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 1.5rem;
          max-width: 900px;
          margin: 0 auto;
        }
        .at-rate-card {
          background: var(--white);
          border: 1px solid var(--cream-dark);
          border-radius: var(--radius);
          padding: 2rem;
          text-align: center;
          position: relative;
        }
        .at-rate-featured {
          border-color: var(--gold);
          box-shadow: 0 4px 20px rgba(201,161,74,0.15);
        }
        .at-rate-badge {
          position: absolute;
          top: -12px;
          left: 50%;
          transform: translateX(-50%);
          background: var(--gold);
          color: var(--navy);
          padding: 0.25rem 1rem;
          border-radius: 50px;
          font-size: 0.75rem;
          font-weight: 700;
          text-transform: uppercase;
        }
        .at-rate-card h3 {
          color: var(--navy);
          font-size: 1.2rem;
          margin-bottom: 0.5rem;
        }
        .at-rate-price {
          font-size: 1.75rem;
          font-weight: 700;
          color: var(--gold);
          margin-bottom: 0.25rem;
        }
        .at-rate-note {
          color: var(--text-muted);
          font-size: 0.9rem;
          margin-bottom: 0.75rem;
        }
        .at-rate-card p:last-child {
          color: var(--text-muted);
          font-size: 0.85rem;
        }
        .at-collections-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 1.25rem;
        }
        .at-collection-card {
          background: var(--cream);
          border: 1px solid var(--cream-dark);
          border-radius: var(--radius);
          padding: 1.75rem;
          transition: all 0.3s;
          display: block;
        }
        .at-collection-card:hover {
          border-color: var(--gold);
          background: var(--white);
          transform: translateY(-2px);
        }
        .at-collection-card h3 {
          color: var(--navy);
          font-size: 1.15rem;
          margin-bottom: 0.3rem;
        }
        .at-collection-card p {
          color: var(--gold);
          font-weight: 600;
          margin-bottom: 0.75rem;
        }
        .at-collection-arrow {
          color: var(--text-muted);
          font-size: 0.85rem;
        }
        .at-why-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 2rem;
          margin-top: 2rem;
        }
        .at-why-item h3 {
          color: var(--gold);
          font-size: 1.1rem;
          margin-bottom: 0.5rem;
        }
        .at-why-item p {
          color: rgba(250,248,244,0.65);
          font-size: 0.95rem;
          line-height: 1.6;
        }
        .at-visit-address {
          font-size: 1.1rem;
          line-height: 1.8;
          color: var(--text-dark);
        }
        @media (max-width: 640px) {
          .at-countdown { gap: 0.5rem; }
          .at-countdown-unit { padding: 0.75rem; min-width: 65px; }
          .at-countdown-num { font-size: 1.5rem; }
          .at-hero { padding: 3rem 0 2.5rem; }
          .at-hero-ctas { flex-direction: column; align-items: center; }
          .at-btn { width: 100%; max-width: 300px; }
        }
      `}</style>
    </>
  );
}
