import Head from 'next/head';
import { SITE_NAME, SITE_URL, DEFAULT_OG_IMAGE } from '../lib/seo-config';

/**
 * Reusable SEO Head component for every page.
 * Ensures proper title, meta description, Open Graph, Twitter Card,
 * canonical URL, geo targeting, hreflang, and structured data on every page.
 */
export default function SEOHead({
  title,
  description,
  canonical,
  ogImage,
  ogType = 'website',
  structuredData,
  noindex = false,
}) {
  const fullCanonical = canonical
    ? canonical.startsWith('http')
      ? canonical
      : `${SITE_URL}${canonical}`
    : SITE_URL;

  const fullOgImage = ogImage || `${SITE_URL}${DEFAULT_OG_IMAGE}`;

  return (
    <Head>
      {/* Primary Title & Description */}
      <title>{title}</title>
      <meta name="description" content={description} />
      <link rel="canonical" href={fullCanonical} />

      {/* Hreflang — Regional targeting for India */}
      <link rel="alternate" hrefLang="en-in" href={fullCanonical} />
      <link rel="alternate" hrefLang="x-default" href={fullCanonical} />

      {/* Geo Targeting — Gurgaon, Haryana, India */}
      <meta name="geo.region" content="IN-HR" />
      <meta name="geo.placename" content="Gurgaon" />
      <meta name="geo.position" content="28.4595;77.0266" />
      <meta name="ICBM" content="28.4595, 77.0266" />

      {/* Open Graph / Facebook */}
      <meta property="og:type" content={ogType} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:url" content={fullCanonical} />
      <meta property="og:image" content={fullOgImage} />
      <meta property="og:image:width" content="1200" />
      <meta property="og:image:height" content="630" />
      <meta property="og:image:alt" content={`${title} - Auric Jewels Gurgaon`} />
      <meta property="og:site_name" content={SITE_NAME} />
      <meta property="og:locale" content="en_IN" />

      {/* Twitter Card */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={fullOgImage} />
      <meta name="twitter:image:alt" content={`${title} - Auric Jewels Gurgaon`} />

      {/* Additional SEO */}
      <meta name="robots" content={noindex ? 'noindex, nofollow' : 'index, follow'} />
      <meta name="googlebot" content={noindex ? 'noindex, nofollow' : 'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1'} />
      <meta name="bingbot" content={noindex ? 'noindex, nofollow' : 'index, follow, max-snippet:-1, max-image-preview:large'} />

      {/* Content Language */}
      <meta httpEquiv="content-language" content="en-IN" />

      {/* Structured Data (JSON-LD) */}
      {structuredData && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
        />
      )}
    </Head>
  );
}
