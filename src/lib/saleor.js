const SALEOR_API_URL = process.env.SALEOR_API_URL || 'https://auric.thecodemesh.online/graphql/';
const SALEOR_TOKEN = process.env.SALEOR_TOKEN || 'fAPR16BVrzI4thcLtj8c4tUUG1wGU6';

export async function saleorFetch(query, variables = {}) {
  const res = await fetch(SALEOR_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${SALEOR_TOKEN}`,
    },
    body: JSON.stringify({ query, variables }),
  });
  const json = await res.json();
  if (json.errors) {
    console.error('Saleor GraphQL errors:', json.errors);
  }
  return json.data;
}

export const ALL_PAGES_QUERY = `
  query AllPages {
    pages(first: 100) {
      edges {
        node {
          id
          slug
          title
          seoTitle
          seoDescription
          created
          publishedDate
          content
          isPublished
        }
      }
    }
  }
`;

export const PAGE_BY_SLUG_QUERY = `
  query PageBySlug($slug: String!) {
    page(slug: $slug) {
      id
      slug
      title
      seoTitle
      seoDescription
      created
      publishedDate
      content
      isPublished
    }
  }
`;
