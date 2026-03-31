import SEOHead from '../components/SEOHead';
import { homepageSEO, SITE_URL } from '../lib/seo-config';

/**
 * HOMEPAGE — Server-side rendered for full SEO visibility.
 *
 * Key SEO fixes:
 * 1. SSR via getServerSideProps — Google sees full HTML, not empty JS shell
 * 2. H1 tag with target keyword
 * 3. Title tag optimized for "luxury gold diamond jewellery Gurgaon"
 * 4. 150-char meta description
 * 5. JSON-LD structured data for LocalBusiness + JewelryStore
 * 6. Semantic HTML with crawlable text content
 */

const structuredData = {
  '@context': 'https://schema.org',
  '@type': ['JewelryStore', 'LocalBusiness'],
  name: 'Auric Jewels',
  url: SITE_URL,
  logo: `${SITE_URL}/images/auric-jewels-logo.png`,
  image: `${SITE_URL}/images/auric-jewels-storefront.jpg`,
  description:
    'Premium gold and diamond jewellery store in Gurgaon offering handcrafted rings, earrings, necklaces, bracelets and more.',
  address: {
    '@type': 'PostalAddress',
    addressLocality: 'Gurgaon',
    addressRegion: 'Haryana',
    addressCountry: 'IN',
  },
  geo: {
    '@type': 'GeoCoordinates',
    latitude: '28.4595',
    longitude: '77.0266',
  },
  priceRange: '$$$$',
  openingHoursSpecification: {
    '@type': 'OpeningHoursSpecification',
    dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    opens: '10:00',
    closes: '20:00',
  },
  sameAs: [],
};

export default function HomePage() {
  return (
    <>
      <SEOHead
        title={homepageSEO.title}
        description={homepageSEO.description}
        canonical="/"
        structuredData={structuredData}
      />

      <main className="container">
        {/* ── H1 — Critical for SEO. Must be visible, not hidden. ── */}
        <h1>{homepageSEO.h1}</h1>

        {/* ── Crawlable intro content — gives Google word count ── */}
        <section>
          <p>
            Welcome to Auric Jewels — Gurgaon&apos;s premier destination for luxury gold and
            diamond jewellery. Our handcrafted collections feature exquisite designs in 18K and
            22K BIS hallmarked gold, adorned with IGI and GIA certified diamonds.
          </p>
          <p>
            From timeless solitaire rings and elegant diamond earrings to statement necklaces
            and contemporary bracelets, every piece at Auric Jewels is crafted with precision
            and passion. Whether you&apos;re shopping for an engagement ring, a wedding gift,
            or everyday luxury, our curated collections offer something for every occasion.
          </p>
        </section>

        {/* ── Category links — crawlable internal linking ── */}
        <section>
          <h2>Shop by Category</h2>
          <nav aria-label="Product categories">
            <ul>
              <li><a href="/categories/rings">Gold &amp; Diamond Rings</a></li>
              <li><a href="/categories/earrings">Designer Earrings</a></li>
              <li><a href="/categories/necklaces">Necklaces &amp; Pendants</a></li>
              <li><a href="/categories/bracelets">Bracelets</a></li>
              <li><a href="/categories/bangles">Bangles</a></li>
              <li><a href="/categories/pendants">Pendants</a></li>
              <li><a href="/categories/mangalsutra">Mangalsutra</a></li>
              <li><a href="/categories/nose-pins">Nose Pins</a></li>
            </ul>
          </nav>
        </section>

        {/* ── Collections — crawlable links to top collection pages ── */}
        <section>
          <h2>Popular Collections</h2>
          <nav aria-label="Popular collections">
            <ul>
              <li><a href="/collections/best-seller">Best Sellers</a></li>
              <li><a href="/collections/new-arrivals">New Arrivals</a></li>
              <li><a href="/collections/under-50k">Under &#8377;50,000</a></li>
              <li><a href="/collections/gifting">Gifting Collection</a></li>
            </ul>
          </nav>
        </section>

        {/* ── Additional crawlable content for word count ── */}
        <section>
          <h2>Why Choose Auric Jewels?</h2>
          <p>
            At Auric Jewels, we believe that fine jewellery is more than an accessory — it&apos;s
            an expression of your personal style and a celebration of life&apos;s most precious
            moments. Here&apos;s what sets us apart:
          </p>
          <ul>
            <li>
              <strong>Certified Quality:</strong> Every diamond is IGI or GIA certified. All gold
              jewellery is BIS hallmarked, guaranteeing purity.
            </li>
            <li>
              <strong>Handcrafted Excellence:</strong> Our master artisans bring decades of experience
              to every piece, blending traditional Indian karigari with modern design aesthetics.
            </li>
            <li>
              <strong>Transparent Pricing:</strong> No hidden charges. Our prices reflect the true
              value of materials and craftsmanship.
            </li>
            <li>
              <strong>Free Shipping &amp; Returns:</strong> Enjoy free insured shipping across India
              and hassle-free 15-day returns.
            </li>
            <li>
              <strong>Lifetime Exchange:</strong> Exchange your Auric Jewels purchase at full value,
              any time.
            </li>
          </ul>
        </section>

        <section>
          <h2>Visit Our Gurgaon Showroom</h2>
          <p>
            Experience our collections in person at our Gurgaon showroom. Our jewellery
            consultants will help you find the perfect piece for any occasion — from everyday
            elegance to bridal jewellery. Book an appointment or walk in during our opening
            hours, 10 AM to 8 PM, seven days a week.
          </p>
        </section>
      </main>
    </>
  );
}

/**
 * SSR — ensures Google crawls full HTML on every request.
 * For a mostly-static site, consider switching to getStaticProps + ISR
 * once content is stable: revalidate: 3600 (1 hour)
 */
export async function getServerSideProps() {
  return { props: {} };
}
