/** @type {import('next-sitemap').IConfig} */
module.exports = {
  siteUrl: 'https://www.auricjewels.com',
  generateRobotsTxt: false, // Using static public/robots.txt instead
  sitemapSize: 5000,
  changefreq: 'weekly',
  priority: 0.7,
  transform: async (config, path) => {
    // Higher priority for homepage and category pages
    let priority = config.priority;
    let changefreq = config.changefreq;

    if (path === '/') {
      priority = 1.0;
    } else if (path.startsWith('/categories/')) {
      priority = 0.9;
    } else if (path.startsWith('/products/')) {
      priority = 0.8;
    } else if (path.startsWith('/blog/')) {
      priority = 0.8;
      changefreq = 'daily';
    }

    return {
      loc: path,
      changefreq,
      priority,
      lastmod: new Date().toISOString(),
    };
  },
};
