import { saleorFetch, ALL_PAGES_QUERY } from '../lib/saleor';

const SITE_URL = 'https://www.auricjewels.com';

function generateSiteMap(staticPages, blogPosts) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- Static Pages -->
  <url>
    <loc>${SITE_URL}</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
    <lastmod>${new Date().toISOString()}</lastmod>
  </url>
${staticPages.map((page) => `  <url>
    <loc>${SITE_URL}${page.path}</loc>
    <changefreq>${page.changefreq || 'weekly'}</changefreq>
    <priority>${page.priority || 0.7}</priority>
    <lastmod>${new Date().toISOString()}</lastmod>
  </url>`).join('\n')}
  <!-- Blog Index -->
  <url>
    <loc>${SITE_URL}/blog</loc>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
    <lastmod>${new Date().toISOString()}</lastmod>
  </url>
  <!-- Blog Posts -->
${blogPosts.map((post) => `  <url>
    <loc>${SITE_URL}/blog/${post.slug}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
    <lastmod>${post.updatedAt || new Date().toISOString()}</lastmod>
  </url>`).join('\n')}
</urlset>`;
}

export async function getServerSideProps({ res }) {
  // Static pages
  const staticPages = [
    { path: '/luxury-jewellery-showroom-sector-45-gurgaon', changefreq: 'monthly', priority: 0.9 },
    // Category pages
    { path: '/categories/rings', changefreq: 'weekly', priority: 0.9 },
    { path: '/categories/earrings', changefreq: 'weekly', priority: 0.9 },
    { path: '/categories/necklaces', changefreq: 'weekly', priority: 0.9 },
    { path: '/categories/bracelets', changefreq: 'weekly', priority: 0.9 },
    { path: '/categories/bangles', changefreq: 'weekly', priority: 0.9 },
    { path: '/categories/pendants', changefreq: 'weekly', priority: 0.9 },
    { path: '/categories/chains', changefreq: 'weekly', priority: 0.9 },
    { path: '/categories/mangalsutra', changefreq: 'weekly', priority: 0.9 },
    { path: '/categories/nose-pins', changefreq: 'weekly', priority: 0.9 },
    // Collection pages
    { path: '/collections/solitaire-collection', changefreq: 'weekly', priority: 0.8 },
    { path: '/collections/best-sellers', changefreq: 'weekly', priority: 0.8 },
    { path: '/collections/new-arrivals', changefreq: 'weekly', priority: 0.8 },
    { path: '/collections/for-her', changefreq: 'weekly', priority: 0.8 },
    { path: '/collections/for-him', changefreq: 'weekly', priority: 0.8 },
    { path: '/collections/anniversary-collection', changefreq: 'weekly', priority: 0.8 },
    { path: '/collections/valentine-collection', changefreq: 'weekly', priority: 0.8 },
  ];

  // Fetch blog posts from Saleor
  let blogPosts = [];
  try {
    const data = await saleorFetch(ALL_PAGES_QUERY);
    if (data?.pages?.edges) {
      blogPosts = data.pages.edges
        .map((edge) => edge.node)
        .filter((page) => page.isPublished)
        .map((page) => ({
          slug: page.slug,
          updatedAt: page.publishedDate || page.created,
        }));
    }
  } catch (err) {
    console.error('Failed to fetch blog posts for sitemap:', err);
  }

  const sitemap = generateSiteMap(staticPages, blogPosts);

  res.setHeader('Content-Type', 'text/xml');
  res.setHeader('Cache-Control', 'public, s-maxage=3600, stale-while-revalidate=86400');
  res.write(sitemap);
  res.end();

  return { props: {} };
}

export default function SiteMap() {
  // This component will not render because getServerSideProps writes the XML response directly
  return null;
}
