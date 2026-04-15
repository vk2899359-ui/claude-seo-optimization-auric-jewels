import { Html, Head, Main, NextScript } from 'next/document';

/**
 * Custom Document — renders on the server only.
 * Sets lang attribute, preloads critical resources, and includes analytics.
 */
export default function Document() {
  return (
    <Html lang="en" dir="ltr">
      <Head>
        <meta charSet="utf-8" />
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
        <link rel="manifest" href="/manifest.json" />
        <meta name="theme-color" content="#8B6914" />
        <meta name="msapplication-TileColor" content="#8B6914" />

        {/* DNS Prefetch & Preconnect for performance */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link rel="dns-prefetch" href="https://www.googletagmanager.com" />
        <link rel="dns-prefetch" href="https://www.google-analytics.com" />
        <link rel="dns-prefetch" href="https://cdn.auricjewels.com" />

        {/* Google Analytics 4 — G-5C09XPPJ66 */}
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-5C09XPPJ66" />
        <script
          dangerouslySetInnerHTML={{
            __html: `
              window.dataLayer = window.dataLayer || [];
              function gtag(){dataLayer.push(arguments);}
              gtag('js', new Date());
              gtag('config', 'G-5C09XPPJ66');
            `,
          }}
        />
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
