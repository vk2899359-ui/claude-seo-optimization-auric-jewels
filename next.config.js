/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable React strict mode for better development experience
  reactStrictMode: true,

  // Image optimization for product images
  images: {
    domains: ['www.auricjewels.com', 'cdn.auricjewels.com'],
    formats: ['image/avif', 'image/webp'],
  },

  // Ensure all pages are server-side rendered or statically generated
  // No client-only rendering — this is critical for SEO
  output: 'standalone',

  // Custom headers for SEO
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
        ],
      },
    ];
  },

  // Redirects for SEO — normalize trailing slashes
  trailingSlash: false,

  async redirects() {
    return [
      // 301: non-www → www (canonical domain consolidation)
      {
        source: '/:path*',
        has: [{ type: 'host', value: 'auricjewels.com' }],
        destination: 'https://www.auricjewels.com/:path*',
        permanent: true,
      },
      {
        source: '/categories/DESIGNEREARING',
        destination: '/categories/earrings',
        permanent: true,
      },
      {
        source: '/category/DESIGNEREARING',
        destination: '/categories/earrings',
        permanent: true,
      },
      {
        source: '/category/necklaces',
        destination: '/categories/necklaces',
        permanent: true,
      },
      {
        source: '/category/pendants',
        destination: '/categories/pendants',
        permanent: true,
      },
      {
        source: '/undefined',
        destination: '/',
        permanent: true,
      },
      {
        source: '/default.asp',
        destination: '/',
        permanent: true,
      },
      {
        source: '/contact',
        destination: '/jewellery-store-gurgaon',
        permanent: true,
      },
    ];
  },
};

module.exports = nextConfig;
