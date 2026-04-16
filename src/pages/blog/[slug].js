import SEOHead from '../../components/SEOHead';
import { SITE_URL } from '../../lib/seo-config';
import { saleorFetch, PAGE_BY_SLUG_QUERY, ALL_PAGES_QUERY } from '../../lib/saleor';

function estimateReadingTime(content) {
  if (!content) return 5;
  const text = typeof content === 'string'
    ? content.replace(/<[^>]*>/g, '')
    : JSON.stringify(content);
  const words = text.split(/\s+/).length;
  return Math.max(1, Math.ceil(words / 200));
}

function formatDate(dateString) {
  if (!dateString) return '';
  return new Date(dateString).toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

function extractFAQs(htmlContent) {
  if (!htmlContent || typeof htmlContent !== 'string') return [];

  const faqs = [];
  // Match h3 followed by the next p tag as Q&A pairs after the FAQ heading
  const faqSectionMatch = htmlContent.match(/Frequently Asked Questions[\s\S]*$/i);
  if (!faqSectionMatch) return [];

  const faqSection = faqSectionMatch[0];
  const h3Regex = /<h3>(.*?)<\/h3>\s*<p>([\s\S]*?)<\/p>/gi;
  let match;
  while ((match = h3Regex.exec(faqSection)) !== null) {
    faqs.push({
      question: match[1].replace(/<[^>]*>/g, ''),
      answer: match[2].replace(/<[^>]*>/g, ''),
    });
  }
  return faqs;
}

function renderContent(content) {
  if (!content) return '<p>Content not available.</p>';

  // Handle Saleor rich text JSON format
  if (typeof content === 'string') {
    // If it looks like JSON, try to parse it
    if (content.trim().startsWith('{') || content.trim().startsWith('[')) {
      try {
        const parsed = JSON.parse(content);
        return renderEditorJS(parsed);
      } catch {
        // It's HTML, return as-is
        return content;
      }
    }
    return content;
  }

  if (typeof content === 'object') {
    return renderEditorJS(content);
  }

  return '<p>Content not available.</p>';
}

function renderEditorJS(data) {
  if (!data || !data.blocks) {
    if (data?.text) return `<p>${data.text}</p>`;
    return JSON.stringify(data);
  }

  return data.blocks
    .map((block) => {
      switch (block.type) {
        case 'paragraph':
          return `<p>${block.data?.text || ''}</p>`;
        case 'header':
          const level = block.data?.level || 2;
          return `<h${level}>${block.data?.text || ''}</h${level}>`;
        case 'list':
          const tag = block.data?.style === 'ordered' ? 'ol' : 'ul';
          const items = (block.data?.items || []).map((item) => `<li>${item}</li>`).join('');
          return `<${tag}>${items}</${tag}>`;
        case 'quote':
          return `<blockquote><p>${block.data?.text || ''}</p></blockquote>`;
        case 'image':
          return `<figure><img src="${block.data?.file?.url || block.data?.url || ''}" alt="${block.data?.caption || ''}" loading="lazy" />${block.data?.caption ? `<figcaption>${block.data.caption}</figcaption>` : ''}</figure>`;
        case 'table':
          const rows = (block.data?.content || [])
            .map((row, i) => {
              const cells = row.map((cell) => i === 0 && block.data?.withHeadings ? `<th>${cell}</th>` : `<td>${cell}</td>`).join('');
              return `<tr>${cells}</tr>`;
            })
            .join('');
          return `<table>${rows}</table>`;
        default:
          return block.data?.text ? `<p>${block.data.text}</p>` : '';
      }
    })
    .join('\n');
}

export default function BlogPost({ page, relatedPosts }) {
  if (!page) {
    return (
      <>
        <SEOHead title="Post Not Found | Auric Jewels Blog" description="The blog post you're looking for could not be found." canonical="/blog" />
        <main className="container">
          <h1>Post Not Found</h1>
          <p>The blog post you&apos;re looking for could not be found.</p>
          <a href="/blog">← Back to Blog</a>
        </main>
      </>
    );
  }

  const title = page.seoTitle || page.title;
  const description = page.seoDescription || `Read ${page.title} — expert jewellery guide from Auric Jewels Gurgaon.`;
  const publishedDate = page.publishedDate || page.created;
  const readingTime = estimateReadingTime(page.content);
  const htmlContent = renderContent(page.content);
  const faqs = extractFAQs(htmlContent);

  const breadcrumbData = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: SITE_URL },
      { '@type': 'ListItem', position: 2, name: 'Blog', item: `${SITE_URL}/blog` },
      { '@type': 'ListItem', position: 3, name: page.title, item: `${SITE_URL}/blog/${page.slug}` },
    ],
  };

  const articleSchema = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: title,
    description: description,
    url: `${SITE_URL}/blog/${page.slug}`,
    datePublished: publishedDate,
    dateModified: publishedDate,
    author: {
      '@type': 'Organization',
      name: 'Auric Jewels',
      url: SITE_URL,
    },
    publisher: {
      '@type': 'Organization',
      name: 'Auric Jewels',
      url: SITE_URL,
      logo: {
        '@type': 'ImageObject',
        url: `${SITE_URL}/logo.png`,
      },
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': `${SITE_URL}/blog/${page.slug}`,
    },
    wordCount: htmlContent.replace(/<[^>]*>/g, '').split(/\s+/).length,
    timeRequired: `PT${readingTime}M`,
  };

  const structuredData = [breadcrumbData, articleSchema];

  // Add FAQPage schema if FAQs found
  if (faqs.length > 0) {
    structuredData.push({
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      mainEntity: faqs.map((faq) => ({
        '@type': 'Question',
        name: faq.question,
        acceptedAnswer: {
          '@type': 'Answer',
          text: faq.answer,
        },
      })),
    });
  }

  return (
    <>
      <SEOHead
        title={`${title} | Auric Jewels`}
        description={description}
        canonical={`/blog/${page.slug}`}
        ogType="article"
        structuredData={structuredData}
      />

      <main className="container">
        <nav className="breadcrumbs" aria-label="Breadcrumb">
          <a href="/">Home</a> &gt; <a href="/blog">Blog</a> &gt; <span>{page.title}</span>
        </nav>

        <article className="blog-article">
          <header className="blog-article-header">
            <h1>{page.title}</h1>
            <div className="blog-article-meta">
              <span>By <strong>Auric Jewels</strong></span>
              <span>·</span>
              <time dateTime={publishedDate}>
                {formatDate(publishedDate)}
              </time>
              <span>·</span>
              <span>{readingTime} min read</span>
            </div>
          </header>

          <div
            className="blog-article-content"
            dangerouslySetInnerHTML={{ __html: htmlContent }}
          />
        </article>

        {relatedPosts && relatedPosts.length > 0 && (
          <section className="section related-posts">
            <h2 className="section-title">Related Articles</h2>
            <div className="blog-grid">
              {relatedPosts.map((post) => (
                <a key={post.slug} href={`/blog/${post.slug}`} className="blog-card">
                  <div className="blog-image-placeholder" />
                  <div className="blog-info">
                    <h3 className="blog-title">{post.title}</h3>
                    <p className="blog-excerpt">{post.seoDescription || post.title}</p>
                    <span className="blog-link">Read More →</span>
                  </div>
                </a>
              ))}
            </div>
          </section>
        )}
      </main>
    </>
  );
}

export async function getServerSideProps({ params, res }) {
  const { slug } = params;

  res.setHeader(
    'Cache-Control',
    'public, s-maxage=3600, stale-while-revalidate=86400'
  );

  let page = null;
  let relatedPosts = [];

  try {
    // Fetch the current page
    const pageData = await saleorFetch(PAGE_BY_SLUG_QUERY, { slug });
    page = pageData?.page || null;

    if (!page || !page.isPublished) {
      return { notFound: true };
    }

    // Fetch related posts (other published pages)
    const allData = await saleorFetch(ALL_PAGES_QUERY);
    if (allData?.pages?.edges) {
      relatedPosts = allData.pages.edges
        .map((edge) => edge.node)
        .filter((p) => p.isPublished && p.slug !== slug)
        .sort(() => 0.5 - Math.random())
        .slice(0, 3);
    }
  } catch (err) {
    console.error('Failed to fetch blog post from Saleor:', err);
    return { notFound: true };
  }

  return { props: { page, relatedPosts } };
}
