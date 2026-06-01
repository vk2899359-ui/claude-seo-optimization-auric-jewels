import Head from 'next/head';
import { SITE_NAME, SITE_URL, DEFAULT_OG_IMAGE } from '../lib/seo-config';

/**
 * Reusable SEO Head component for every page.
 * Ensures proper title, meta description, Open Graph, Twitter Card,
 * canonical URL, and structured data on every page.
 */
export default function SEOHead({
  title,
  description,
  canonical,
  ogImage,
  ogType = 'website',
  structuredData,
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

      {/* Open Graph / Facebook */}
      <meta property="og:type" content={ogType} />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:url" content={fullCanonical} />
      <meta property="og:image" content={fullOgImage} />
      <meta property="og:site_name" content={SITE_NAME} />
      <meta property="og:locale" content="en_IN" />

      {/* Twitter Card */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={fullOgImage} />

      {/* Additional SEO */}
      <meta name="robots" content="index, follow" />
      <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large" />

      {/* Structured Data (JSON-LD) */}
      {structuredData && (Array.isArray(structuredData) ? structuredData : [structuredData]).map((schema, i) => (
        <script
          key={i}
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
        />
      ))}
    </Head>
  );
}
