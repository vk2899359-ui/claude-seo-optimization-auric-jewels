/**
 * Central SEO configuration for all pages on auricjewels.com
 * This ensures every page has proper title tags, meta descriptions, and H1 headings.
 */

const SITE_NAME = 'Auric Jewels';
const SITE_URL = 'https://www.auricjewels.com';
const DEFAULT_OG_IMAGE = '/images/auric-jewels-og.jpg';

// ─── HOMEPAGE ───────────────────────────────────────────────
export const homepageSEO = {
  title: 'Luxury Gold & Diamond Jewellery in Gurgaon | Auric Jewels',
  h1: 'Luxury Gold & Diamond Jewellery in Gurgaon | Auric Jewels',
  description:
    'Shop exquisite gold and diamond jewellery at Auric Jewels Gurgaon. Explore handcrafted rings, earrings, necklaces, bracelets & more. Certified diamonds, BIS hallmarked gold.',
  canonical: SITE_URL,
};

// ─── CATEGORY / COLLECTION PAGES ────────────────────────────
export const categorySEO = {
  rings: {
    title: 'Gold & Diamond Rings | Engagement & Daily Wear | Auric Jewels Gurgaon',
    h1: 'Gold & Diamond Rings | Auric Jewels Gurgaon',
    description:
      'Discover stunning gold and diamond rings at Auric Jewels Gurgaon. Engagement rings, wedding bands, cocktail rings & everyday designs. BIS hallmarked. Free shipping.',
  },
  earrings: {
    title: 'Diamond & Gold Earrings for Women | Designer Collection | Auric Jewels Gurgaon',
    h1: 'Designer Gold & Diamond Earrings | Auric Jewels Gurgaon',
    description:
      'Shop designer gold and diamond earrings at Auric Jewels Gurgaon. Studs, hoops, jhumkas, drops & chandbalis. Certified diamonds, BIS hallmarked gold. Free shipping.',
  },
  necklaces: {
    title: 'Gold & Diamond Necklaces | Bridal & Daily Wear | Auric Jewels Gurgaon',
    h1: 'Gold & Diamond Necklaces | Auric Jewels Gurgaon',
    description:
      'Explore elegant gold and diamond necklaces at Auric Jewels Gurgaon. Chokers, pendants, layered necklaces & statement pieces. BIS hallmarked gold. Free shipping.',
  },
  bracelets: {
    title: 'Diamond & Gold Bracelets for Women | Shop Online | Auric Jewels Gurgaon',
    h1: 'Diamond & Gold Bracelets for Women | Auric Jewels Gurgaon',
    description:
      'Shop gold and diamond bracelets at Auric Jewels Gurgaon. Tennis bracelets, bangles, charm bracelets & cuffs. Certified diamonds. BIS hallmarked. Free shipping.',
  },
  bangles: {
    title: 'Gold & Diamond Bangles for Women | Buy Online | Auric Jewels Gurgaon',
    h1: 'Gold & Diamond Bangles | Auric Jewels Gurgaon',
    description:
      'Discover exquisite gold and diamond bangles at Auric Jewels Gurgaon. Traditional kadas, modern bangles & diamond-studded designs. BIS hallmarked. Free shipping.',
  },
  pendants: {
    title: 'Diamond & Gold Pendants for Women | Auric Jewels Gurgaon',
    h1: 'Diamond & Gold Pendants | Auric Jewels Gurgaon',
    description:
      'Shop beautiful gold and diamond pendants at Auric Jewels Gurgaon. Solitaire, cluster, initial & religious pendants. Certified diamonds. BIS hallmarked. Free shipping.',
  },
  chains: {
    title: 'Gold Chains for Women & Men | Latest Designs | Auric Jewels Gurgaon',
    h1: 'Gold Chains for Women & Men | Auric Jewels Gurgaon',
    description:
      'Shop gold chains for women and men at Auric Jewels Gurgaon. Rope chains, cable chains, box chains & designer styles in 18K & 22K BIS hallmarked gold. Free shipping.',
  },
  'mangalsutra': {
    title: 'Diamond Mangalsutra Designs | Buy Online | Auric Jewels Gurgaon',
    h1: 'Diamond Mangalsutra Designs | Auric Jewels Gurgaon',
    description:
      'Shop modern diamond mangalsutra designs at Auric Jewels Gurgaon. Traditional and contemporary styles in 18K & 22K gold. Certified diamonds. Free shipping.',
  },
  'nose-pins': {
    title: 'Gold & Diamond Nose Pins | Buy Online | Auric Jewels Gurgaon',
    h1: 'Gold & Diamond Nose Pins | Auric Jewels Gurgaon',
    description:
      'Discover delicate gold and diamond nose pins at Auric Jewels Gurgaon. Studs, rings & screw-back designs. Certified diamonds, BIS hallmarked gold. Free shipping.',
  },
};

// ─── COLLECTION PAGES (Best Sellers, New Arrivals, etc.) ────
export const collectionSEO = {
  'solitaire-collection': {
    title: 'Solitaire Diamond Jewellery Collection | Auric Jewels Gurgaon',
    h1: 'Solitaire Diamond Jewellery Collection | Auric Jewels Gurgaon',
    description:
      'Shop stunning solitaire diamond rings, earrings & pendants at Auric Jewels Gurgaon. IGI/GIA certified solitaires in 18K & 22K gold. Free shipping.',
  },
  'best-sellers': {
    title: 'Best Selling Gold & Diamond Jewellery | Auric Jewels Gurgaon',
    h1: 'Best Selling Gold & Diamond Jewellery | Auric Jewels Gurgaon',
    description:
      'Shop our best selling gold and diamond jewellery at Auric Jewels Gurgaon. Customer favourites in rings, earrings, necklaces & more. BIS hallmarked. Free shipping.',
  },
  'new-arrivals': {
    title: 'New Arrivals in Gold & Diamond Jewellery | Auric Jewels Gurgaon',
    h1: 'New Arrivals in Gold & Diamond Jewellery | Auric Jewels Gurgaon',
    description:
      'Explore the latest gold and diamond jewellery at Auric Jewels Gurgaon. Fresh designs in rings, earrings, necklaces, bracelets & more. Shop new arrivals today.',
  },
  'for-her': {
    title: 'Gold & Diamond Jewellery for Her | Auric Jewels Gurgaon',
    h1: 'Gold & Diamond Jewellery for Her | Auric Jewels Gurgaon',
    description:
      'Shop gold and diamond jewellery for women at Auric Jewels Gurgaon. Curated rings, earrings, necklaces & bracelets for every occasion. BIS hallmarked. Free shipping.',
  },
  'for-him': {
    title: "Men's Gold & Diamond Jewellery | Auric Jewels Gurgaon",
    h1: "Men's Gold & Diamond Jewellery | Auric Jewels Gurgaon",
    description:
      "Shop men's gold and diamond jewellery at Auric Jewels Gurgaon. Rings, bracelets, chains & cufflinks for men. BIS hallmarked gold. Certified diamonds. Free shipping.",
  },
  'anniversary-collection': {
    title: 'Anniversary Gift Jewellery | Gold & Diamond | Auric Jewels Gurgaon',
    h1: 'Anniversary Gift Jewellery | Gold & Diamond | Auric Jewels Gurgaon',
    description:
      'Find the perfect anniversary jewellery gift at Auric Jewels Gurgaon. Gold and diamond rings, pendants & bracelets for every milestone. Gift wrapping available.',
  },
  'valentine-collection': {
    title: "Valentine's Day Jewellery Gifts | Auric Jewels Gurgaon",
    h1: "Valentine's Day Jewellery Gifts | Auric Jewels Gurgaon",
    description:
      "Shop Valentine's Day jewellery gifts at Auric Jewels Gurgaon. Heart pendants, diamond rings & love-themed designs in certified gold. Free gift wrapping & shipping.",
  },
};

// ─── PRODUCT PAGE SEO GENERATOR ─────────────────────────────
export function generateProductSEO(product) {
  const { name, category, price, material, description } = product;
  const categoryLabel = category ? category.charAt(0).toUpperCase() + category.slice(1) : 'Jewellery';

  return {
    title: `${name} | ${categoryLabel} | Auric Jewels Gurgaon`,
    h1: `${name} — ${categoryLabel} | Auric Jewels`,
    description:
      description && description.length > 50
        ? description.substring(0, 150).trim() + '...'
        : `Buy ${name} from Auric Jewels Gurgaon. ${material || 'Gold & diamond'} ${categoryLabel.toLowerCase()} with certified quality. BIS hallmarked. Free shipping & easy returns.`,
  };
}

// ─── PRODUCT DESCRIPTION GENERATOR ──────────────────────────
// Generates 100-200 word product descriptions for SEO
export function generateProductDescription(product) {
  const { name, category, material, weight, purity, stone, stoneWeight, price } = product;

  const materialDesc = material || '18K gold';
  const categoryLabel = category || 'jewellery';
  const stoneDesc = stone || 'diamond';

  return `Discover the ${name}, a stunning piece of ${categoryLabel} from the Auric Jewels collection. Meticulously handcrafted in ${materialDesc}${purity ? ` (${purity})` : ''}, this exquisite ${categoryLabel} piece showcases the perfect blend of traditional Indian craftsmanship and contemporary design.

${stone || stoneWeight ? `Adorned with ${stoneDesc}${stoneWeight ? ` totalling ${stoneWeight}` : ''}, each stone is carefully selected and certified for exceptional clarity, cut, and brilliance. ` : ''}${weight ? `The piece weighs approximately ${weight}, ensuring a comfortable yet substantial feel. ` : ''}

Every piece from Auric Jewels comes with a BIS hallmark certification, guaranteeing the purity of gold used. ${stoneDesc === 'diamond' ? 'All diamonds are IGI/GIA certified for your peace of mind. ' : ''}

This ${name} is perfect for ${category === 'rings' ? 'engagements, anniversaries, or everyday elegance' : category === 'earrings' ? 'weddings, parties, or adding a touch of luxury to your daily look' : category === 'necklaces' ? 'special occasions, festivals, or as a statement piece' : 'gifting, celebrations, or treating yourself to timeless luxury'}.

Shop with confidence at Auric Jewels Gurgaon — enjoy free shipping across India, easy 15-day returns, and lifetime exchange. Visit our Gurgaon showroom for an in-person experience.`;
}

export { SITE_NAME, SITE_URL, DEFAULT_OG_IMAGE };
