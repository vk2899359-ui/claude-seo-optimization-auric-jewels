/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable React strict mode for better development experience
  reactStrictMode: true,

  // Image optimization for product images
  images: {
    domains: ['www.auricjewels.com', 'cdn.auricjewels.com'],
    formats: ['image/avif', 'image/webp'],
    minimumCacheTTL: 60 * 60 * 24, // Cache images for 24 hours
  },

  // Ensure all pages are server-side rendered or statically generated
  // No client-only rendering — this is critical for SEO
  output: 'standalone',

  // Compress responses for faster page loads (Core Web Vitals)
  compress: true,

  // Optimize fonts for performance
  optimizeFonts: true,

  // Custom headers for SEO and security
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'X-XSS-Protection', value: '1; mode=block' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
          { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=(self)' },
        ],
      },
      {
        // Cache static assets aggressively for better page speed
        source: '/images/(.*)',
        headers: [
          { key: 'Cache-Control', value: 'public, max-age=31536000, immutable' },
        ],
      },
      {
        source: '/icons/(.*)',
        headers: [
          { key: 'Cache-Control', value: 'public, max-age=31536000, immutable' },
        ],
      },
    ];
  },

  // Redirects for SEO — handle common URL variations
  async redirects() {
    return [
      // Redirect /jewellery to homepage (common search term)
      { source: '/jewellery', destination: '/', permanent: true },
      { source: '/jewelry', destination: '/', permanent: true },
      // Redirect category variations
      { source: '/category/:slug', destination: '/categories/:slug', permanent: true },
      { source: '/collection/:slug', destination: '/collections/:slug', permanent: true },
      { source: '/product/:slug', destination: '/products/:slug', permanent: true },
    ];
  },

  // Redirects for SEO — normalize trailing slashes
  trailingSlash: false,
};

module.exports = nextConfig;
