import SEOHead from '../../components/SEOHead';
import { SITE_URL } from '../../lib/seo-config';

const blogPosts = [
  {
    slug: 'best-diamond-jewellery-showroom-gurgaon',
    title: 'Best Diamond Jewellery Showroom in Gurgaon — Why Families Trust Auric Jewels',
    excerpt: 'Discover what makes a diamond showroom truly premium — from IGI/GIA certification to BIS hallmarked gold and transparent pricing.',
    date: '2026-03-15',
  },
  {
    slug: 'gold-jewellery-investment-2026-gurgaon',
    title: 'Gold Jewellery as Investment in 2026 — Gurgaon Buyer\'s Guide',
    excerpt: 'Is gold jewellery a good investment in 2026? Learn about gold purity, hallmarking, making charges, and how to buy smart in Gurgaon.',
    date: '2026-03-10',
  },
  {
    slug: 'jewellery-trends-india-2026',
    title: 'Top Jewellery Trends in India 2026 — What\'s Hot Right Now',
    excerpt: 'From layered necklaces to lab-grown diamonds, discover the biggest jewellery trends shaping India in 2026.',
    date: '2026-03-05',
  },
  {
    slug: 'lab-grown-vs-natural-diamonds-comparison-india',
    title: 'Lab-Grown vs Natural Diamonds — Complete Comparison for Indian Buyers',
    excerpt: 'Understand the key differences between lab-grown and natural diamonds — price, quality, resale value, and certification.',
    date: '2026-02-28',
  },
  {
    slug: 'layered-necklace-styling-guide-indian-women',
    title: 'Layered Necklace Styling Guide for Indian Women',
    excerpt: 'Master the art of layering necklaces with Indian outfits. Tips, tricks, and curated combinations for every occasion.',
    date: '2026-02-20',
  },
  {
    slug: 'lightweight-gold-jewellery-working-women',
    title: 'Lightweight Gold Jewellery for Working Women — Style Meets Comfort',
    excerpt: 'Discover elegant, lightweight gold jewellery designed for the modern working woman. Office-friendly pieces that don\'t compromise on style.',
    date: '2026-02-15',
  },
  {
    slug: 'platinum-jewellery-men-gurgaon',
    title: 'Platinum Jewellery for Men in Gurgaon — Complete Buying Guide',
    excerpt: 'Explore the world of men\'s platinum jewellery — chains, bracelets, rings, and more. Why platinum is the new gold for modern men.',
    date: '2026-02-10',
  },
];

export default function BlogIndex() {
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'Blog',
    name: 'Auric Jewels Journal — Expert Guides on Gold & Diamond Jewellery',
    description: 'Expert articles on buying gold and diamond jewellery in Gurgaon. Guides on diamonds, gold investment, jewellery trends, and styling tips from Auric Jewels.',
    url: `${SITE_URL}/blog`,
    publisher: {
      '@type': 'Organization',
      name: 'Auric Jewels',
      url: SITE_URL,
    },
    blogPost: blogPosts.map((post) => ({
      '@type': 'BlogPosting',
      headline: post.title,
      description: post.excerpt,
      url: `${SITE_URL}/blog/${post.slug}`,
      datePublished: post.date,
      author: { '@type': 'Organization', name: 'Auric Jewels' },
      publisher: { '@type': 'Organization', name: 'Auric Jewels' },
    })),
  };

  return (
    <>
      <SEOHead
        title="Jewellery Buying Guides & Tips | Auric Jewels Blog | Gurgaon"
        description="Expert guides on buying gold & diamond jewellery in Gurgaon. Learn about diamond certification, gold purity, jewellery trends 2026, styling tips & investment advice from Auric Jewels."
        canonical="/blog"
        structuredData={structuredData}
      />

      <main className="container">
        <nav className="breadcrumbs" aria-label="Breadcrumb">
          <a href="/">Home</a> &gt; <span>Blog</span>
        </nav>

        <h1>Auric Jewels Journal — Expert Guides on Gold &amp; Diamond Jewellery</h1>
        <p className="section-subtitle">
          Your trusted resource for jewellery buying guides, diamond education, gold investment tips,
          and styling inspiration from the experts at Auric Jewels Gurgaon.
        </p>

        <div className="blog-grid">
          {blogPosts.map((post) => (
            <a key={post.slug} href={`/blog/${post.slug}`} className="blog-card">
              <div className="blog-image-placeholder" />
              <div className="blog-info">
                <time dateTime={post.date} className="blog-date">
                  {new Date(post.date).toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric' })}
                </time>
                <h2 className="blog-title">{post.title}</h2>
                <p className="blog-excerpt">{post.excerpt}</p>
                <span className="blog-link">Read Full Article &rarr;</span>
              </div>
            </a>
          ))}
        </div>
      </main>
    </>
  );
}

export async function getStaticProps() {
  return { props: {} };
}
