import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import SEOHead from '../../components/SEOHead';
import { SITE_URL } from '../../lib/seo-config';

// Blog metadata for SEO
const blogMeta = {
  'best-diamond-jewellery-showroom-gurgaon': {
    title: 'Best Diamond Jewellery Showroom in Gurgaon — Why Families Trust Auric Jewels',
    description: 'Discover what makes a diamond showroom truly premium — from IGI/GIA certification to BIS hallmarked gold and transparent pricing. A guide for jewellery buyers in Gurgaon.',
    date: '2026-03-15',
    file: 'blog-01-best-diamond-jewellery-showroom-gurgaon.html',
  },
  'gold-jewellery-investment-2026-gurgaon': {
    title: 'Gold Jewellery as Investment in 2026 — Gurgaon Buyer\'s Guide',
    description: 'Is gold jewellery a good investment in 2026? Learn about gold purity, BIS hallmarking, making charges, resale value, and how to buy smart in Gurgaon.',
    date: '2026-03-10',
    file: 'blog-gold-jewellery-investment-2026-gurgaon.html',
  },
  'jewellery-trends-india-2026': {
    title: 'Top Jewellery Trends in India 2026 — What\'s Hot Right Now',
    description: 'From layered necklaces to lab-grown diamonds, discover the biggest jewellery trends shaping India in 2026. Expert insights from Auric Jewels Gurgaon.',
    date: '2026-03-05',
    file: 'blog-jewellery-trends-india-2026.html',
  },
  'lab-grown-vs-natural-diamonds-comparison-india': {
    title: 'Lab-Grown vs Natural Diamonds — Complete Comparison for Indian Buyers',
    description: 'Understand the key differences between lab-grown and natural diamonds — price, quality, resale value, and certification. Expert analysis from Auric Jewels.',
    date: '2026-02-28',
    file: 'blog-lab-grown-vs-natural-diamonds-comparison-india.html',
  },
  'layered-necklace-styling-guide-indian-women': {
    title: 'Layered Necklace Styling Guide for Indian Women',
    description: 'Master the art of layering necklaces with Indian outfits. Tips, tricks, and curated combinations for sarees, kurtas, and western wear.',
    date: '2026-02-20',
    file: 'blog-layered-necklace-styling-guide-indian-women.html',
  },
  'lightweight-gold-jewellery-working-women': {
    title: 'Lightweight Gold Jewellery for Working Women — Style Meets Comfort',
    description: 'Discover elegant, lightweight gold jewellery designed for the modern working woman. Office-friendly pieces in BIS hallmarked gold from Auric Jewels Gurgaon.',
    date: '2026-02-15',
    file: 'blog-lightweight-gold-jewellery-working-women.html',
  },
  'platinum-jewellery-men-gurgaon': {
    title: 'Platinum Jewellery for Men in Gurgaon — Complete Buying Guide',
    description: 'Explore men\'s platinum jewellery — chains, bracelets, rings. Why platinum is the premium choice for modern men. Available at Auric Jewels Gurgaon showroom.',
    date: '2026-02-10',
    file: 'blog-platinum-jewellery-men-gurgaon.html',
  },
};

export default function BlogPost({ slug, meta, htmlContent }) {
  const articleSchema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: meta.title,
    description: meta.description,
    url: `${SITE_URL}/blog/${slug}`,
    datePublished: meta.date,
    dateModified: meta.date,
    author: {
      '@type': 'Organization',
      name: 'Auric Jewels',
      url: SITE_URL,
    },
    publisher: {
      '@type': 'Organization',
      name: 'Auric Jewels',
      url: SITE_URL,
      logo: {
        '@type': 'ImageObject',
        url: `${SITE_URL}/logo.png`,
      },
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': `${SITE_URL}/blog/${slug}`,
    },
    image: `${SITE_URL}/images/auric-jewels-og.jpg`,
  };

  const breadcrumbData = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: SITE_URL },
      { '@type': 'ListItem', position: 2, name: 'Blog', item: `${SITE_URL}/blog` },
      { '@type': 'ListItem', position: 3, name: meta.title, item: `${SITE_URL}/blog/${slug}` },
    ],
  };

  return (
    <>
      <SEOHead
        title={`${meta.title} | Auric Jewels`}
        description={meta.description}
        canonical={`/blog/${slug}`}
        structuredData={[articleSchema, breadcrumbData]}
      />

      <main className="container">
        <nav className="breadcrumbs" aria-label="Breadcrumb">
          <a href="/">Home</a> &gt; <a href="/blog">Blog</a> &gt; <span>{meta.title}</span>
        </nav>

        <article className="blog-article">
          <header>
            <h1>{meta.title}</h1>
            <time dateTime={meta.date} className="blog-date">
              {new Date(meta.date).toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric' })}
            </time>
          </header>

          {htmlContent ? (
            <div
              className="blog-content"
              dangerouslySetInnerHTML={{ __html: htmlContent }}
            />
          ) : (
            <div className="blog-content">
              <p>{meta.description}</p>
            </div>
          )}
        </article>

        {/* Internal linking for SEO */}
        <section className="blog-cta">
          <h2>Explore Auric Jewels</h2>
          <div className="blog-cta-links">
            <a href="/categories/rings">Diamond Rings</a>
            <a href="/categories/earrings">Diamond Earrings</a>
            <a href="/categories/necklaces">Gold Necklaces</a>
            <a href="/collections/solitaire-collection">Solitaire Collection</a>
            <a href="/collections/best-sellers">Best Sellers</a>
            <a href="/blog">More Articles</a>
          </div>
        </section>
      </main>
    </>
  );
}

export async function getStaticProps({ params }) {
  const { slug } = params;
  const meta = blogMeta[slug];

  if (!meta) {
    return { notFound: true };
  }

  let htmlContent = '';
  if (meta.file) {
    const filePath = join(process.cwd(), 'content', meta.file);
    if (existsSync(filePath)) {
      htmlContent = readFileSync(filePath, 'utf-8');
    }
  }

  return {
    props: { slug, meta, htmlContent },
    revalidate: 86400, // Revalidate once per day
  };
}

export async function getStaticPaths() {
  const slugs = Object.keys(blogMeta);
  return {
    paths: slugs.map((slug) => ({ params: { slug } })),
    fallback: 'blocking',
  };
}
