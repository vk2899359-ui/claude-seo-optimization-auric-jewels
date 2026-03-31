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
};

module.exports = nextConfig;
