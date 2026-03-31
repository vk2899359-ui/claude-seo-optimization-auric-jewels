/** @type {import('next-sitemap').IConfig} */
module.exports = {
  siteUrl: 'https://www.auricjewels.com',
  generateRobotsTxt: true,
  sitemapSize: 5000,
  changefreq: 'weekly',
  priority: 0.7,
  robotsTxtOptions: {
    additionalSitemaps: [],
    policies: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/api/', '/checkout/', '/account/'],
      },
    ],
  },
  transform: async (config, path) => {
    // Higher priority for homepage and category pages
    let priority = config.priority;
    if (path === '/') priority = 1.0;
    else if (path.startsWith('/categories/')) priority = 0.9;
    else if (path.startsWith('/products/')) priority = 0.8;

    return {
      loc: path,
      changefreq: config.changefreq,
      priority,
      lastmod: new Date().toISOString(),
    };
  },
};
