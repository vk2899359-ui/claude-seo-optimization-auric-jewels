import fs from 'fs';
import path from 'path';
import Head from 'next/head';
import { useState, useEffect } from 'react';

const SITE_URL = 'https://www.auricjewels.com';
const WA_URL = 'https://wa.me/919012495941';

const blogMeta = {
  '01-best-diamond-jewellery-showroom-gurgaon': { title: 'Best Diamond Jewellery Showroom in Gurgaon', description: 'Why families across Delhi NCR trust Auric Jewels for certified diamond jewellery, BIS hallmarked gold, and solitaire collections.', category: 'Diamond Jewellery', readTime: '6 min read' },
  'gold-jewellery-investment-2026-gurgaon': { title: 'Gold Jewellery Investment Guide 2026', description: 'Is gold jewellery a good investment in 2026? Expert guide on gold purity, resale value, and smart buying strategies.', category: 'Gold Investment', readTime: '7 min read' },
  'jewellery-trends-india-2026': { title: 'Jewellery Trends India 2026', description: 'Top jewellery trends in India for 2026 — from layered necklaces to solitaire rings.', category: 'Jewellery Trends', readTime: '5 min read' },
  'lab-grown-vs-natural-diamonds-comparison-india': { title: 'Lab Grown vs Natural Diamonds', description: 'Complete comparison for Indian buyers — price, quality, resale value, and which to choose.', category: 'Diamond Guide', readTime: '8 min read' },
  'layered-necklace-styling-guide-indian-women': { title: 'Layered Necklace Styling Guide', description: 'How to style layered necklaces for Indian women — gold, diamond, and platinum ideas for every occasion.', category: 'Styling Guide', readTime: '5 min read' },
  'lightweight-gold-jewellery-working-women': { title: 'Lightweight Gold Jewellery for Working Women', description: 'Best lightweight gold jewellery for working women in 2026 — comfortable, elegant everyday pieces.', category: 'Everyday Jewellery', readTime: '5 min read' },
  'platinum-jewellery-men-gurgaon': { title: 'Platinum Jewellery for Men in Gurgaon', description: 'Premium platinum jewellery for men at Auric Jewels Gurgaon — rings, bracelets, chains in certified platinum.', category: "Men's Jewellery", readTime: '6 min read' },
};

// ─── SERVER-SIDE HTML PARSER ──────────────────────────────────────────────────

function decodeEntities(s) {
  return s
    .replace(/&amp;/g, '&')
    .replace(/&#8377;/g, '₹')
    .replace(/&gt;/g, '>')
    .replace(/&lt;/g, '<')
    .replace(/&nbsp;/g, '\u00a0')
    .replace(/&middot;/g, '·')
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n));
}

function stripTags(html) {
  return decodeEntities(html.replace(/<[^>]+>/g, '').trim());
}

function parseInlines(rawHtml) {
  const html = decodeEntities(rawHtml);
  const result = [];
  const re = /<a\s+href="([^"]*)"[^>]*>([\s\S]*?)<\/a>|<strong>([\s\S]*?)<\/strong>|<em>([\s\S]*?)<\/em>|<br\s*\/?>/gi;
  let last = 0;
  let m;
  while ((m = re.exec(html)) !== null) {
    if (m.index > last) {
      const txt = html.slice(last, m.index);
      if (txt) result.push({ t: 'text', v: txt });
    }
    const tag2 = m[0].slice(1, 3).toLowerCase();
    if (tag2 === 'a ') {
      result.push({ t: 'a', href: m[1], v: stripTags(m[2]) });
    } else if (tag2 === 'st') {
      result.push({ t: 'strong', v: decodeEntities(m[3] || '') });
    } else if (tag2 === 'em') {
      result.push({ t: 'em', v: decodeEntities(m[4] || '') });
    } else {
      result.push({ t: 'br' });
    }
    last = m.index + m[0].length;
  }
  if (last < html.length) {
    const txt = html.slice(last);
    if (txt) result.push({ t: 'text', v: txt });
  }
  return result;
}

function findCloseTag(html, start, closeTag) {
  const idx = html.indexOf(closeTag, start);
  return idx !== -1 ? idx : html.length;
}

function toId(text) {
  return text.toLowerCase().replace(/[^a-z0-9\s]/g, '').trim().replace(/\s+/g, '-').slice(0, 60);
}

function parseBlocks(rawHtml) {
  const html = rawHtml
    .replace(/^\s*<article[^>]*>\s*/i, '')
    .replace(/\s*<\/article>\s*$/i, '')
    .trim();

  const raw = [];
  let i = 0;

  while (i < html.length) {
    while (i < html.length && /\s/.test(html[i])) i++;
    if (i >= html.length) break;
    if (html[i] !== '<') { i++; continue; }

    const tagMatch = html.slice(i).match(/^<(\w+)(\s[^>]*)?>/i);
    if (!tagMatch) { i++; continue; }

    const tag = tagMatch[1].toLowerCase();
    const openLen = tagMatch[0].length;
    const closeTag = `</${tag}>`;

    if (['h1', 'h2', 'h3', 'h4', 'p', 'blockquote'].includes(tag)) {
      const ci = findCloseTag(html, i + openLen, closeTag);
      const inner = html.slice(i + openLen, ci).trim();
      const text = stripTags(inner);
      raw.push({
        tag,
        id: (tag === 'h2' || tag === 'h3') ? toId(text) : null,
        inner,
        text,
        inlines: parseInlines(inner),
        isFaq: tag === 'h3' && text.trimEnd().endsWith('?'),
        isCallout: tag === 'p' && text.trimStart().startsWith('At Auric Jewels'),
      });
      i = ci + closeTag.length;
    } else if (tag === 'ul' || tag === 'ol') {
      const ci = findCloseTag(html, i + openLen, closeTag);
      const inner = html.slice(i + openLen, ci);
      const items = [...inner.matchAll(/<li[^>]*>([\s\S]*?)<\/li>/gi)].map(m2 => ({
        inlines: parseInlines(m2[1].trim()),
        text: stripTags(m2[1]),
      }));
      raw.push({ tag, items });
      i = ci + closeTag.length;
    } else if (tag === 'table') {
      const ci = findCloseTag(html, i + openLen, '</table>');
      const tableHtml = html.slice(i + openLen, ci);
      const heads = [...tableHtml.matchAll(/<th[^>]*>([\s\S]*?)<\/th>/gi)].map(m2 => stripTags(m2[1]));
      const rows = [...tableHtml.matchAll(/<tr[^>]*>([\s\S]*?)<\/tr>/gi)]
        .map(m2 => [...m2[1].matchAll(/<td[^>]*>([\s\S]*?)<\/td>/gi)].map(c => stripTags(c[1])))
        .filter(r => r.length > 0);
      raw.push({ tag: 'table', heads, rows });
      i = ci + '</table>'.length;
    } else {
      const ci = html.indexOf(closeTag, i + openLen);
      i = ci !== -1 ? ci + closeTag.length : i + openLen;
    }
  }

  // Group FAQ h3+p pairs
  const nodes = [];
  let j = 0;
  while (j < raw.length) {
    if (raw[j].isFaq) {
      const q = raw[j];
      const a = raw[j + 1]?.tag === 'p' ? raw[j + 1] : null;
      nodes.push({ tag: 'faq', id: q.id, question: q, answer: a });
      j += a ? 2 : 1;
    } else {
      nodes.push(raw[j]);
      j++;
    }
  }
  return nodes;
}

// ─── INLINE RENDERER ─────────────────────────────────────────────────────────

function InlineContent({ inlines }) {
  return (
    <>
      {inlines.map((n, i) => {
        if (n.t === 'text') return <span key={i}>{n.v}</span>;
        if (n.t === 'a') return <a key={i} href={n.href} className="prose-a">{n.v}</a>;
        if (n.t === 'strong') return <strong key={i}>{n.v}</strong>;
        if (n.t === 'em') return <em key={i}>{n.v}</em>;
        if (n.t === 'br') return <br key={i} />;
        return null;
      })}
    </>
  );
}

// ─── COMPONENTS ──────────────────────────────────────────────────────────────

function ReadingProgressBar() {
  const [pct, setPct] = useState(0);
  useEffect(() => {
    const onScroll = () => {
      const el = document.documentElement;
      const total = el.scrollHeight - el.clientHeight;
      setPct(total > 0 ? Math.min(100, (el.scrollTop / total) * 100) : 0);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);
  return (
    <div style={{ position: 'fixed', top: 0, left: 0, right: 0, height: 3, zIndex: 9999, background: 'rgba(0,0,0,0.15)' }}>
      <div style={{ height: '100%', width: `${pct}%`, background: 'linear-gradient(90deg,#b8934a,#e8c97e,#b8934a)', transition: 'width 0.08s linear' }} />
    </div>
  );
}

function TableOfContents({ headings }) {
  const [active, setActive] = useState('');
  useEffect(() => {
    const els = headings.map(h => document.getElementById(h.id)).filter(Boolean);
    if (!els.length) return;
    const obs = new IntersectionObserver(
      entries => entries.forEach(e => { if (e.isIntersecting) setActive(e.target.id); }),
      { rootMargin: '-20% 0px -70% 0px' }
    );
    els.forEach(el => obs.observe(el));
    return () => obs.disconnect();
  }, [headings]);

  return (
    <div className="toc-box">
      <p className="toc-label">In this article</p>
      <nav>
        {headings.map(h => (
          <button
            key={h.id}
            className={`toc-item${active === h.id ? ' toc-active' : ''}`}
            onClick={() => { const el = document.getElementById(h.id); el && el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }}
          >
            {h.text}
          </button>
        ))}
      </nav>
    </div>
  );
}

function FaqItem({ node, isOpen, onToggle }) {
  return (
    <div className="faq-item">
      <button className="faq-q" onClick={onToggle} aria-expanded={isOpen}>
        <span><InlineContent inlines={node.question.inlines} /></span>
        <span className="faq-chevron" style={{ display: 'inline-block', transform: isOpen ? 'rotate(180deg)' : 'none', transition: 'transform 0.25s' }}>▾</span>
      </button>
      {isOpen && node.answer && (
        <div className="faq-a">
          <InlineContent inlines={node.answer.inlines} />
        </div>
      )}
    </div>
  );
}

function ArticleNode({ node, faqOpen, onFaqToggle }) {
  switch (node.tag) {
    case 'h1': return null;
    case 'h2':
      return <h2 id={node.id} className="article-h2"><InlineContent inlines={node.inlines} /></h2>;
    case 'h3':
      return <h3 id={node.id} className="article-h3"><InlineContent inlines={node.inlines} /></h3>;
    case 'p':
      if (node.isCallout) {
        return (
          <div className="callout-box">
            <span className="callout-icon">✦</span>
            <p><InlineContent inlines={node.inlines} /></p>
          </div>
        );
      }
      return <p className="article-p"><InlineContent inlines={node.inlines} /></p>;
    case 'ul':
      return (
        <ul className="article-list">
          {node.items.map((item, i) => <li key={i}><InlineContent inlines={item.inlines} /></li>)}
        </ul>
      );
    case 'ol':
      return (
        <ol className="article-list article-ol">
          {node.items.map((item, i) => <li key={i}><InlineContent inlines={item.inlines} /></li>)}
        </ol>
      );
    case 'table':
      return (
        <div className="table-wrap">
          <table className="article-table">
            {node.heads.length > 0 && (
              <thead><tr>{node.heads.map((h, i) => <th key={i}>{h}</th>)}</tr></thead>
            )}
            <tbody>
              {node.rows.map((row, ri) => (
                <tr key={ri}>{row.map((cell, ci) => <td key={ci}>{cell}</td>)}</tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    case 'blockquote':
      return <blockquote className="article-quote"><InlineContent inlines={node.inlines} /></blockquote>;
    case 'faq':
      return <FaqItem node={node} isOpen={faqOpen.has(node.id)} onToggle={() => onFaqToggle(node.id)} />;
    default:
      return null;
  }
}

function StatCards() {
  const stats = [
    { value: '18K', label: 'BIS Hallmarked Gold' },
    { value: '22K', label: 'BIS Hallmarked Gold' },
    { value: 'IGI', label: 'Certified Diamonds' },
  ];
  return (
    <div className="stat-cards">
      {stats.map(s => (
        <div key={s.value} className="stat-card">
          <span className="stat-value">{s.value}</span>
          <span className="stat-label">{s.label}</span>
        </div>
      ))}
    </div>
  );
}

function BottomCTA() {
  return (
    <div className="bottom-cta">
      <p className="cta-eyebrow">Ready to explore?</p>
      <h2 className="cta-title">Visit Auric Jewels in Gurgaon</h2>
      <p className="cta-sub">Book a private consultation or browse our certified diamond &amp; gold collection online.</p>
      <a href={WA_URL} target="_blank" rel="noopener noreferrer" className="wa-button">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.890-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
        </svg>
        Chat on WhatsApp
      </a>
    </div>
  );
}

function ReadNext({ blogs }) {
  return (
    <div className="read-next">
      <p className="rn-eyebrow">Continue Reading</p>
      <h2 className="rn-title">You May Also Like</h2>
      <div className="rn-grid">
        {blogs.map(b => (
          <a key={b.slug} href={`/blog/${b.slug}`} className="rn-card">
            <span className="rn-category">{b.category}</span>
            <span className="rn-card-title">{b.title}</span>
            <span className="rn-read">{b.readTime} →</span>
          </a>
        ))}
      </div>
    </div>
  );
}

// ─── PAGE ─────────────────────────────────────────────────────────────────────

export default function BlogPost({ slug, nodes, meta, relatedBlogs }) {
  const [faqOpen, setFaqOpen] = useState(new Set());

  const toggleFaq = (id) => {
    setFaqOpen(prev => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  const h2Headings = nodes.filter(n => n.tag === 'h2').map(n => ({ id: n.id, text: n.text }));
  const faqNodes = nodes.filter(n => n.tag === 'faq');

  const articleSchema = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: meta.title,
    description: meta.description,
    url: `${SITE_URL}/blog/${slug}`,
    author: { '@type': 'Organization', name: 'Auric Jewels', url: SITE_URL },
    publisher: {
      '@type': 'Organization',
      name: 'Auric Jewels',
      url: SITE_URL,
      logo: { '@type': 'ImageObject', url: `${SITE_URL}/logo.png` },
    },
    mainEntityOfPage: { '@type': 'WebPage', '@id': `${SITE_URL}/blog/${slug}` },
  };

  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: SITE_URL },
      { '@type': 'ListItem', position: 2, name: 'Blog', item: `${SITE_URL}/blog` },
      { '@type': 'ListItem', position: 3, name: meta.title, item: `${SITE_URL}/blog/${slug}` },
    ],
  };

  const faqSchema = faqNodes.length > 0 ? {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqNodes.map(n => ({
      '@type': 'Question',
      name: n.question.text,
      acceptedAnswer: { '@type': 'Answer', text: n.answer?.text || '' },
    })),
  } : null;

  return (
    <>
      <Head>
        <title>{meta.title} | Auric Jewels</title>
        <meta name="description" content={meta.description} />
        <link rel="canonical" href={`${SITE_URL}/blog/${slug}`} />
        <meta property="og:title" content={`${meta.title} | Auric Jewels`} />
        <meta property="og:description" content={meta.description} />
        <meta property="og:url" content={`${SITE_URL}/blog/${slug}`} />
        <meta property="og:type" content="article" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet" />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(articleSchema) }} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }} />
        {faqSchema && <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }} />}
        <style>{STYLES}</style>
      </Head>

      <ReadingProgressBar />

      {/* ── HERO ── */}
      <header className="hero">
        <div className="hero-inner">
          <nav className="hero-crumbs" aria-label="Breadcrumb">
            <a href="/">Home</a>
            <span className="hero-sep">›</span>
            <a href="/blog">Journal</a>
            <span className="hero-sep">›</span>
            <span>{meta.category}</span>
          </nav>
          <p className="hero-category">{meta.category}</p>
          <h1 className="hero-title">{meta.title}</h1>
          <p className="hero-meta">{meta.readTime}&nbsp;·&nbsp;Auric Jewels&nbsp;·&nbsp;Gurgaon</p>
          <div className="hero-rule" />
        </div>
      </header>

      <StatCards />

      {/* ── TWO-COLUMN BODY ── */}
      <div className="page-wrap">
        <div className="two-col">
          <article className="article-body">
            {nodes.map((node, i) => (
              <ArticleNode key={i} node={node} faqOpen={faqOpen} onFaqToggle={toggleFaq} />
            ))}
          </article>

          <aside className="sidebar">
            {h2Headings.length > 0 && <TableOfContents headings={h2Headings} />}
            <div className="sidebar-wa">
              <p className="sidebar-wa-eyebrow">Have a question?</p>
              <p className="sidebar-wa-text">Our jewellery experts are on WhatsApp — get answers in minutes.</p>
              <a href={WA_URL} target="_blank" rel="noopener noreferrer" className="sidebar-wa-btn">
                Chat with us
              </a>
            </div>
          </aside>
        </div>
      </div>

      <BottomCTA />
      <ReadNext blogs={relatedBlogs} />
    </>
  );
}

// ─── STYLES ───────────────────────────────────────────────────────────────────

const STYLES = `
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'DM Sans', sans-serif; color: #1a1a1a; background: #fff; }

  /* Hero */
  .hero {
    background: linear-gradient(135deg, #0d0d0d 0%, #1a1208 55%, #0d0d0d 100%);
    padding: 5rem 1.5rem 3.5rem;
    position: relative;
    overflow: hidden;
  }
  .hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 60% at 50% 110%, rgba(184,147,74,0.14) 0%, transparent 70%);
    pointer-events: none;
  }
  .hero-inner { max-width: 760px; margin: 0 auto; position: relative; }
  .hero-crumbs {
    font-size: 12px;
    color: rgba(255,255,255,0.35);
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
  }
  .hero-crumbs a { color: rgba(255,255,255,0.45); text-decoration: none; transition: color 0.2s; }
  .hero-crumbs a:hover { color: #b8934a; }
  .hero-sep { opacity: 0.3; }
  .hero-category {
    font-size: 11px;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #b8934a;
    margin-bottom: 1rem;
    font-weight: 500;
  }
  .hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(28px, 5vw, 54px);
    font-weight: 600;
    color: #fff;
    line-height: 1.15;
    margin-bottom: 1.25rem;
    letter-spacing: -0.01em;
  }
  .hero-meta { font-size: 13px; color: rgba(255,255,255,0.4); letter-spacing: 0.04em; }
  .hero-rule {
    width: 48px;
    height: 1px;
    background: linear-gradient(90deg, #b8934a, transparent);
    margin-top: 2rem;
  }

  /* Stat cards */
  .stat-cards {
    display: flex;
    background: #0d0d0d;
    border-bottom: 1px solid rgba(184,147,74,0.15);
  }
  .stat-card {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1.25rem 1rem;
    border-right: 1px solid rgba(184,147,74,0.12);
    gap: 4px;
  }
  .stat-card:last-child { border-right: none; }
  .stat-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 24px;
    font-weight: 600;
    background: linear-gradient(135deg, #b8934a 0%, #e8c97e 50%, #b8934a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  .stat-label {
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.38);
    text-align: center;
  }

  /* Layout */
  .page-wrap { max-width: 1180px; margin: 0 auto; padding: 3.5rem 1.5rem 4rem; }
  .two-col { display: grid; grid-template-columns: 1fr 280px; gap: 56px; align-items: start; }

  /* Article */
  .article-body { min-width: 0; }
  .article-h2 {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(22px, 3.5vw, 32px);
    font-weight: 600;
    color: #111;
    margin: 3rem 0 1.25rem;
    padding-left: 1rem;
    border-left: 3px solid #b8934a;
    line-height: 1.25;
    scroll-margin-top: 24px;
  }
  .article-h2:first-child { margin-top: 0; }
  .article-h3 {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(18px, 2.5vw, 24px);
    font-weight: 600;
    color: #222;
    margin: 2.25rem 0 0.9rem;
    line-height: 1.3;
    scroll-margin-top: 24px;
  }
  .article-p {
    font-size: 16px;
    line-height: 1.9;
    color: #2a2a2a;
    margin-bottom: 1.4rem;
  }
  .prose-a {
    color: #b8934a;
    text-decoration: underline;
    text-underline-offset: 3px;
    text-decoration-thickness: 1px;
    transition: color 0.2s;
  }
  .prose-a:hover { color: #96742d; }
  .article-list { padding-left: 1.5rem; margin-bottom: 1.4rem; }
  .article-list li { font-size: 15px; line-height: 1.85; color: #2a2a2a; margin-bottom: 0.5rem; }
  .article-ol { list-style-type: decimal; }
  .article-quote {
    border-left: 3px solid #b8934a;
    margin: 2rem 0;
    padding: 0.75rem 1.5rem;
    background: #fdf9f3;
    color: #555;
    font-style: italic;
    font-size: 16px;
    line-height: 1.8;
    border-radius: 0 6px 6px 0;
  }

  /* Callout box */
  .callout-box {
    display: flex;
    gap: 12px;
    background: linear-gradient(135deg, #fdf9f3 0%, #faf5ec 100%);
    border: 1px solid rgba(184,147,74,0.28);
    border-left: 4px solid #b8934a;
    border-radius: 0 8px 8px 0;
    padding: 1.25rem 1.5rem;
    margin: 1.75rem 0;
  }
  .callout-icon { color: #b8934a; font-size: 13px; flex-shrink: 0; margin-top: 3px; }
  .callout-box p { font-size: 15px; line-height: 1.85; color: #2a2a2a; }

  /* Table */
  .table-wrap {
    overflow-x: auto;
    margin: 2rem 0;
    border-radius: 8px;
    border: 1px solid #f0ece4;
    -webkit-overflow-scrolling: touch;
  }
  .article-table { width: 100%; border-collapse: collapse; font-size: 14px; }
  .article-table th {
    background: #0d0d0d;
    color: #b8934a;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 11px;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    padding: 12px 16px;
    text-align: left;
    white-space: nowrap;
  }
  .article-table td {
    padding: 11px 16px;
    border-bottom: 1px solid #f5f0e8;
    color: #333;
    line-height: 1.5;
    white-space: nowrap;
  }
  .article-table tr:last-child td { border-bottom: none; }
  .article-table tr:nth-child(even) td { background: #fdf9f4; }

  /* FAQ accordion */
  .faq-item { border-bottom: 1px solid #f0ece4; }
  .faq-q {
    width: 100%;
    background: none;
    border: none;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
    padding: 1.1rem 0;
    text-align: left;
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(17px, 2.5vw, 20px);
    font-weight: 600;
    color: #111;
    line-height: 1.4;
    transition: color 0.2s;
  }
  .faq-q:hover { color: #b8934a; }
  .faq-chevron { font-size: 18px; color: #b8934a; flex-shrink: 0; margin-top: 2px; }
  .faq-a {
    font-size: 15px;
    line-height: 1.85;
    color: #444;
    padding-bottom: 1.1rem;
    padding-right: 2rem;
  }

  /* Sidebar */
  .sidebar { position: sticky; top: 24px; display: flex; flex-direction: column; gap: 20px; }
  .toc-box {
    border: 1px solid #f0ece4;
    border-radius: 10px;
    padding: 1.5rem;
    background: #fdf9f3;
  }
  .toc-label {
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #b8934a;
    margin-bottom: 1rem;
    font-weight: 500;
  }
  .toc-item {
    display: block;
    width: 100%;
    background: none;
    border: none;
    border-left: 2px solid transparent;
    cursor: pointer;
    text-align: left;
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    color: #555;
    line-height: 1.5;
    padding: 5px 0 5px 10px;
    transition: color 0.2s, border-color 0.2s;
  }
  .toc-item:hover { color: #b8934a; }
  .toc-item.toc-active { color: #b8934a; border-left-color: #b8934a; font-weight: 500; }
  .sidebar-wa {
    background: linear-gradient(135deg, #0d0d0d 0%, #1a1208 100%);
    border-radius: 10px;
    padding: 1.5rem;
    border: 1px solid rgba(184,147,74,0.18);
  }
  .sidebar-wa-eyebrow {
    font-size: 10px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #b8934a;
    margin-bottom: 0.6rem;
  }
  .sidebar-wa-text {
    font-size: 13px;
    color: rgba(255,255,255,0.55);
    line-height: 1.6;
    margin-bottom: 1.1rem;
  }
  .sidebar-wa-btn {
    display: block;
    text-align: center;
    background: #25D366;
    color: #fff;
    font-size: 13px;
    font-weight: 500;
    padding: 10px 16px;
    border-radius: 6px;
    text-decoration: none;
    transition: opacity 0.2s;
  }
  .sidebar-wa-btn:hover { opacity: 0.88; }

  /* Bottom CTA */
  .bottom-cta {
    background: linear-gradient(135deg, #0d0d0d 0%, #1a1208 50%, #0d0d0d 100%);
    text-align: center;
    padding: 5rem 1.5rem;
    position: relative;
    overflow: hidden;
  }
  .bottom-cta::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 70% 50% at 50% 110%, rgba(184,147,74,0.16) 0%, transparent 70%);
    pointer-events: none;
  }
  .cta-eyebrow {
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #b8934a;
    margin-bottom: 0.8rem;
    position: relative;
  }
  .cta-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(28px, 4vw, 46px);
    font-weight: 600;
    color: #fff;
    margin-bottom: 1rem;
    position: relative;
  }
  .cta-sub {
    font-size: 15px;
    color: rgba(255,255,255,0.45);
    max-width: 440px;
    margin: 0 auto 2.25rem;
    line-height: 1.7;
    position: relative;
  }
  .wa-button {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: #25D366;
    color: #fff;
    font-size: 15px;
    font-weight: 500;
    padding: 14px 30px;
    border-radius: 50px;
    text-decoration: none;
    transition: transform 0.2s, opacity 0.2s;
    position: relative;
    letter-spacing: 0.02em;
  }
  .wa-button:hover { transform: translateY(-2px); opacity: 0.92; }

  /* Read Next */
  .read-next { max-width: 1180px; margin: 0 auto; padding: 4rem 1.5rem 5rem; }
  .rn-eyebrow {
    font-size: 11px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #b8934a;
    margin-bottom: 0.5rem;
  }
  .rn-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(24px, 3.5vw, 36px);
    font-weight: 600;
    color: #111;
    margin-bottom: 2rem;
  }
  .rn-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
  .rn-card {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 1.75rem;
    border: 1px solid #f0ece4;
    border-radius: 10px;
    text-decoration: none;
    transition: border-color 0.2s, transform 0.2s;
  }
  .rn-card:hover { border-color: #b8934a; transform: translateY(-2px); }
  .rn-category {
    font-size: 10px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #b8934a;
    font-weight: 500;
  }
  .rn-card-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 20px;
    font-weight: 600;
    color: #111;
    line-height: 1.3;
  }
  .rn-read { font-size: 12px; color: #aaa; margin-top: 4px; }

  /* Responsive */
  @media (max-width: 900px) {
    .two-col { grid-template-columns: 1fr; }
    .sidebar { display: none; }
  }
  @media (max-width: 600px) {
    .page-wrap { padding: 2.5rem 1rem 3rem; }
    .hero { padding: 4rem 1rem 3rem; }
    .stat-card { flex: 1 1 33.33%; }
    .rn-grid { grid-template-columns: 1fr; }
    .bottom-cta { padding: 3.5rem 1rem; }
    .table-wrap { margin: 1.5rem -1rem; border-radius: 0; border-left: none; border-right: none; }
  }
`;

// ─── DATA FETCHING ────────────────────────────────────────────────────────────

export async function getStaticPaths() {
  const contentDir = path.join(process.cwd(), 'content');
  const files = fs.readdirSync(contentDir).filter(f => f.startsWith('blog-') && f.endsWith('.html'));
  return {
    paths: files.map(f => ({ params: { slug: f.replace(/^blog-/, '').replace('.html', '') } })),
    fallback: false,
  };
}

export async function getStaticProps({ params }) {
  const { slug } = params;
  const contentDir = path.join(process.cwd(), 'content');
  const primary = path.join(contentDir, `${slug}.html`);
  const fallback = path.join(contentDir, `blog-${slug}.html`);
  const filePath = fs.existsSync(primary) ? primary : fallback;
  const rawHtml = fs.readFileSync(filePath, 'utf-8');
  const nodes = parseBlocks(rawHtml);

  const meta = blogMeta[slug] || {
    title: slug.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
    description: `Expert guide from Auric Jewels on ${slug.replace(/-/g, ' ')}.`,
    category: 'Jewellery Guide',
    readTime: '5 min read',
  };

  const relatedBlogs = Object.entries(blogMeta)
    .filter(([s]) => s !== slug)
    .slice(0, 2)
    .map(([s, m]) => ({ slug: s, ...m }));

  return { props: { slug, nodes, meta, relatedBlogs } };
}
