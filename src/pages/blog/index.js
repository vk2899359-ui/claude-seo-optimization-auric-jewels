import SEOHead from '../../components/SEOHead';
import { SITE_URL } from '../../lib/seo-config';
import { saleorFetch, ALL_PAGES_QUERY } from '../../lib/saleor';

function estimateReadingTime(content) {
  if (!content) return 5;
  const text = typeof content === 'string'
    ? content.replace(/<[^>]*>/g, '')
    : JSON.stringify(content);
  const words = text.split(/\s+/).length;
  return Math.max(1, Math.ceil(words / 200));
}

function formatDate(dateString) {
  if (!dateString) return '';
  return new Date(dateString).toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

export default function BlogIndex({ posts }) {
  const breadcrumbData = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: SITE_URL },
      { '@type': 'ListItem', position: 2, name: 'Blog', item: `${SITE_URL}/blog` },
    ],
  };

  const structuredData = [
    breadcrumbData,
    {
      '@context': 'https://schema.org',
      '@type': 'CollectionPage',
      name: 'Auric Jewels Blog — Gold & Diamond Jewellery Guides',
      description: 'Expert guides on buying gold jewellery, diamond rings, bridal sets, solitaire collections, and more from Auric Jewels Gurgaon.',
      url: `${SITE_URL}/blog`,
      isPartOf: { '@type': 'WebSite', name: 'Auric Jewels', url: SITE_URL },
    },
  ];

  return (
    <>
      <SEOHead
        title="Jewellery Buying Guides & Expert Tips | Auric Jewels Blog"
        description="Expert guides on buying gold jewellery, diamond rings, bridal sets, solitaire collections & more. Trusted advice from Auric Jewels Gurgaon."
        canonical="/blog"
        structuredData={structuredData}
      />

      <main className="container">
        <nav className="breadcrumbs" aria-label="Breadcrumb">
          <a href="/">Home</a> &gt; <span>Blog</span>
        </nav>

        <h1>Auric Jewels Blog — Gold &amp; Diamond Jewellery Guides</h1>
        <p className="blog-index-subtitle">
          Expert buying guides, styling tips, and insider knowledge from Gurgaon&apos;s
          trusted jewellery showroom.
        </p>

        <div className="blog-grid">
          {posts.map((post) => (
            <a key={post.slug} href={`/blog/${post.slug}`} className="blog-card">
              <div className="blog-image-placeholder" />
              <div className="blog-info">
                <h2 className="blog-title">{post.title}</h2>
                <p className="blog-meta">
                  {formatDate(post.publishedDate || post.created)}
                  {' '}·{' '}{estimateReadingTime(post.content)} min read
                </p>
                <p className="blog-excerpt">
                  {post.seoDescription || post.title}
                </p>
                <span className="blog-link">Read More →</span>
              </div>
            </a>
          ))}
        </div>

        {posts.length === 0 && (
          <p>No blog posts found. Check back soon for expert jewellery guides.</p>
        )}
      </main>
    </>
  );
}

export async function getServerSideProps({ res }) {
  res.setHeader(
    'Cache-Control',
    'public, s-maxage=3600, stale-while-revalidate=86400'
  );

  let posts = [];
  try {
    const data = await saleorFetch(ALL_PAGES_QUERY);
    if (data?.pages?.edges) {
      posts = data.pages.edges
        .map((edge) => edge.node)
        .filter((page) => page.isPublished)
        .sort((a, b) => new Date(b.publishedDate || b.created) - new Date(a.publishedDate || a.created));
    }
  } catch (err) {
    console.error('Failed to fetch blog posts from Saleor:', err);
  }

  return { props: { posts } };
}
