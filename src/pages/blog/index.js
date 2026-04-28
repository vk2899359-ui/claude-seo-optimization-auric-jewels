import fs from 'fs';
import path from 'path';
import Head from 'next/head';

const SITE_URL = 'https://www.auricjewels.com';

const blogMeta = {
  'blog-01-best-diamond-jewellery-showroom-gurgaon': { title: 'Best Diamond Jewellery Showroom in Gurgaon', description: 'Why families across Delhi NCR trust Auric Jewels for certified diamond jewellery, BIS hallmarked gold, and solitaire collections.', category: 'Diamond Jewellery', readTime: '6 min read' },
  'blog-gold-jewellery-investment-2026-gurgaon': { title: 'Gold Jewellery Investment Guide 2026', description: 'Is gold jewellery a good investment in 2026? Expert guide on gold purity, resale value, and smart buying strategies.', category: 'Gold Investment', readTime: '7 min read' },
  'blog-jewellery-trends-india-2026': { title: 'Jewellery Trends India 2026', description: 'Top jewellery trends in India for 2026 — from layered necklaces to solitaire rings.', category: 'Jewellery Trends', readTime: '5 min read' },
  'blog-lab-grown-vs-natural-diamonds-comparison-india': { title: 'Lab Grown vs Natural Diamonds', description: 'Complete comparison for Indian buyers — price, quality, resale value, and which to choose.', category: 'Diamond Guide', readTime: '8 min read' },
  'blog-layered-necklace-styling-guide-indian-women': { title: 'Layered Necklace Styling Guide', description: 'How to style layered necklaces for Indian women — gold, diamond, and platinum ideas for every occasion.', category: 'Styling Guide', readTime: '5 min read' },
  'blog-lightweight-gold-jewellery-working-women': { title: 'Lightweight Gold Jewellery for Working Women', description: 'Best lightweight gold jewellery for working women in 2026 — comfortable, elegant everyday pieces.', category: 'Everyday Jewellery', readTime: '5 min read' },
  'blog-platinum-jewellery-men-gurgaon': { title: 'Platinum Jewellery for Men in Gurgaon', description: 'Premium platinum jewellery for men at Auric Jewels Gurgaon — rings, bracelets, chains in certified platinum.', category: "Men's Jewellery", readTime: '6 min read' },
};

export default function BlogIndex({ blogs }) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'Blog',
    name: 'Auric Jewels Journal',
    description: 'Expert jewellery guides, styling tips, and buying advice from Auric Jewels Gurgaon.',
    url: `${SITE_URL}/blog`,
    publisher: { '@type': 'Organization', name: 'Auric Jewels', url: SITE_URL },
  };

  return (
    <>
      <Head>
        <title>Jewellery Guides & Expert Advice | Auric Jewels Blog</title>
        <meta name="description" content="Expert jewellery guides, diamond buying tips, gold investment advice, and styling inspiration from Auric Jewels — Gurgaon's premium jewellery showroom." />
        <link rel="canonical" href={`${SITE_URL}/blog`} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
        <style>{`
          @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=DM+Sans:wght@300;400;500&display=swap');
          .blog-index { max-width: 1100px; margin: 0 auto; padding: 3rem 1.5rem 5rem; font-family: 'DM Sans', sans-serif; }
          .blog-index-header { text-align: center; margin-bottom: 3rem; border-bottom: 1px solid #f0ece4; padding-bottom: 2rem; }
          .blog-index-label { font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; color: #b8934a; margin-bottom: 0.75rem; }
          .blog-index-title { font-family: 'Cormorant Garamond', serif; font-size: clamp(32px, 5vw, 52px); font-weight: 600; color: #111; margin: 0 0 1rem; line-height: 1.1; }
          .blog-index-subtitle { font-size: 15px; color: #666; max-width: 520px; margin: 0 auto; line-height: 1.7; }
          .blog-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 24px; }
          .blog-card { border: 1px solid #f0ece4; border-radius: 12px; padding: 1.75rem; text-decoration: none; display: block; transition: border-color 0.2s, transform 0.2s; background: white; }
          .blog-card:hover { border-color: #b8934a; transform: translateY(-2px); }
          .card-category { font-size: 10px; letter-spacing: 0.14em; text-transform: uppercase; color: #b8934a; margin-bottom: 0.6rem; font-weight: 500; }
          .card-title { font-family: 'Cormorant Garamond', serif; font-size: 21px; font-weight: 600; color: #111; line-height: 1.3; margin: 0 0 0.75rem; }
          .card-desc { font-size: 13px; line-height: 1.7; color: #666; margin: 0 0 1.25rem; }
          .card-meta { font-size: 11px; color: #aaa; display: flex; gap: 10px; align-items: center; }
          .card-meta span { color: #b8934a; }
          .breadcrumbs { font-size: 12px; color: #888; margin-bottom: 2rem; }
          .breadcrumbs a { color: #b8934a; text-decoration: none; }
          @media (max-width: 600px) { .blog-index { padding: 2rem 1rem 4rem; } .blog-grid { grid-template-columns: 1fr; } }
        `}</style>
      </Head>

      <main className="blog-index">
        <nav className="breadcrumbs">
          <a href="/">Home</a> &gt; <span style={{ color: '#333' }}>Blog</span>
        </nav>
        <div className="blog-index-header">
          <p className="blog-index-label">Auric Jewels Journal</p>
          <h1 className="blog-index-title">Jewellery Guides &amp; Expert Advice</h1>
          <p className="blog-index-subtitle">Diamond buying tips, gold investment insights, and styling inspiration from Gurgaon's most trusted jewellery showroom.</p>
        </div>
        <div className="blog-grid">
          {blogs.map((blog) => (
            <a key={blog.slug} href={`/blog/${blog.slug}`} className="blog-card">
              <p className="card-category">{blog.category}</p>
              <h2 className="card-title">{blog.title}</h2>
              <p className="card-desc">{blog.description}</p>
              <div className="card-meta">
                <span>{blog.readTime}</span>
                · Auric Jewels
              </div>
            </a>
          ))}
        </div>
      </main>
    </>
  );
}

export async function getStaticProps() {
  const contentDir = path.join(process.cwd(), 'content');
  const files = fs.readdirSync(contentDir).filter(f => f.startsWith('blog-') && f.endsWith('.html'));
  const blogs = files.map(f => {
    const slug = f.replace('.html', '');
    const meta = blogMeta[slug] || { title: slug.replace(/-/g, ' '), description: '', category: 'Jewellery Guide', readTime: '5 min read' };
    return { slug, ...meta };
  });
  return { props: { blogs }, revalidate: 3600 };
}
