/** @type {import('next-sitemap').IConfig} */
module.exports = {
  siteUrl: 'https://www.auricjewels.com',
  generateRobotsTxt: false, // Using static public/robots.txt instead
  sitemapSize: 5000,
  changefreq: 'weekly',
  priority: 0.7,
  exclude: ['/admin', '/checkout', '/api/*', '/404', '/500'],
  transform: async (config, path) => {
    // Dynamic priority and change frequency based on page type
    let priority = config.priority;
    let changefreq = config.changefreq;

    if (path === '/') {
      priority = 1.0;
      changefreq = 'daily';
    } else if (path.startsWith('/categories/')) {
      priority = 0.9;
      changefreq = 'weekly';
    } else if (path.startsWith('/collections/')) {
      priority = 0.85;
      changefreq = 'weekly';
    } else if (path.startsWith('/products/')) {
      priority = 0.8;
      changefreq = 'weekly';
    } else if (path === '/blog') {
      priority = 0.8;
      changefreq = 'daily';
    } else if (path.startsWith('/blog/')) {
      priority = 0.75;
      changefreq = 'monthly';
    }

    return {
      loc: path,
      changefreq,
      priority,
      lastmod: new Date().toISOString(),
    };
  },
  additionalPaths: async () => {
    // Ensure blog pages are included in sitemap
    const blogSlugs = [
      'best-diamond-jewellery-showroom-gurgaon',
      'gold-jewellery-investment-2026-gurgaon',
      'jewellery-trends-india-2026',
      'lab-grown-vs-natural-diamonds-comparison-india',
      'layered-necklace-styling-guide-indian-women',
      'lightweight-gold-jewellery-working-women',
      'platinum-jewellery-men-gurgaon',
    ];

    return [
      { loc: '/blog', changefreq: 'daily', priority: 0.8, lastmod: new Date().toISOString() },
      ...blogSlugs.map((slug) => ({
        loc: `/blog/${slug}`,
        changefreq: 'monthly',
        priority: 0.75,
        lastmod: new Date().toISOString(),
      })),
    ];
  },
};
