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
    'Shop luxury gold & diamond jewellery in Gurgaon. Explore rings, earrings, necklaces, bracelets & bridal sets at Auric Jewels. BIS hallmarked. Visit our showroom.',
  canonical: SITE_URL,
};

// ─── CATEGORY / COLLECTION PAGES ────────────────────────────
export const categorySEO = {
  rings: {
    title: 'Gold & Diamond Rings | Engagement & Daily Wear | Auric Jewels Gurgaon',
    h1: 'Gold & Diamond Rings | Auric Jewels Gurgaon',
    description:
      'Explore stunning gold & diamond rings at Auric Jewels Gurgaon. Engagement, solitaire & daily wear rings. BIS hallmarked. Shop online or visit showroom.',
  },
  earrings: {
    title: 'Diamond & Gold Earrings for Women | Designer Collection | Auric Jewels Gurgaon',
    h1: 'Designer Gold & Diamond Earrings | Auric Jewels Gurgaon',
    description:
      'Shop designer diamond & gold earrings at Auric Jewels Gurgaon. Studs, hoops, drops & jhumkas. Hallmarked gold. Free shipping. Visit our Gurgaon showroom.',
  },
  necklaces: {
    title: 'Gold & Diamond Necklaces | Bridal & Daily Wear | Auric Jewels Gurgaon',
    h1: 'Gold & Diamond Necklaces | Auric Jewels Gurgaon',
    description:
      'Discover gold & diamond necklaces at Auric Jewels Gurgaon. Bridal sets, chokers & pendants. Certified diamonds. Shop online or visit our showroom.',
  },
  bracelets: {
    title: 'Diamond & Gold Bracelets for Women | Shop Online | Auric Jewels Gurgaon',
    h1: 'Diamond & Gold Bracelets for Women | Auric Jewels Gurgaon',
    description:
      'Buy diamond & gold bracelets for women at Auric Jewels Gurgaon. Tennis, chain & mangalsutra bracelets. Hallmarked. Shop online or visit showroom.',
  },
  bangles: {
    title: 'Gold & Diamond Bangles for Women | Buy Online | Auric Jewels Gurgaon',
    h1: 'Gold & Diamond Bangles | Auric Jewels Gurgaon',
    description:
      'Shop gold & diamond bangles at Auric Jewels Gurgaon. Daily wear & bridal designs. BIS hallmarked. Free shipping. Visit our Gurgaon showroom.',
  },
  pendants: {
    title: 'Diamond & Gold Pendants for Women | Auric Jewels Gurgaon',
    h1: 'Diamond & Gold Pendants | Auric Jewels Gurgaon',
    description:
      'Explore diamond & gold pendants at Auric Jewels Gurgaon. Solitaire, heart & floral designs. Certified. Shop online or visit our showroom.',
  },
  chains: {
    title: 'Gold Chains for Women & Men | Latest Designs | Auric Jewels Gurgaon',
    h1: 'Gold Chains for Women & Men | Auric Jewels Gurgaon',
    description:
      'Buy gold chains for women & men at Auric Jewels Gurgaon. 18KT & 22KT designs. BIS hallmarked. Shop latest collection online.',
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
      'Shop solitaire diamond rings, pendants & earrings at Auric Jewels Gurgaon. IGI certified. Premium cuts. Visit showroom or buy online.',
  },
  'best-sellers': {
    title: 'Best Selling Gold & Diamond Jewellery | Auric Jewels Gurgaon',
    h1: 'Best Selling Gold & Diamond Jewellery | Auric Jewels Gurgaon',
    description:
      'Discover Auric Jewels best selling gold & diamond jewellery in Gurgaon. Customer favourites in rings, earrings & bracelets. Shop now.',
  },
  'new-arrivals': {
    title: 'New Arrivals in Gold & Diamond Jewellery | Auric Jewels Gurgaon',
    h1: 'New Arrivals in Gold & Diamond Jewellery | Auric Jewels Gurgaon',
    description:
      'Explore latest gold & diamond jewellery designs at Auric Jewels Gurgaon. New arrivals in rings, earrings, necklaces & more. Shop now.',
  },
  'for-her': {
    title: 'Gold & Diamond Jewellery for Her | Auric Jewels Gurgaon',
    h1: 'Gold & Diamond Jewellery for Her | Auric Jewels Gurgaon',
    description:
      'Shop gold & diamond jewellery gifts for her at Auric Jewels Gurgaon. Curated collection for birthdays, anniversaries & special occasions.',
  },
  'for-him': {
    title: "Men's Gold & Diamond Jewellery | Auric Jewels Gurgaon",
    h1: "Men's Gold & Diamond Jewellery | Auric Jewels Gurgaon",
    description:
      "Discover men's gold & diamond jewellery at Auric Jewels Gurgaon. Chains, bracelets, rings & studs for men. Hallmarked. Shop now.",
  },
  'anniversary-collection': {
    title: 'Anniversary Gift Jewellery | Gold & Diamond | Auric Jewels Gurgaon',
    h1: 'Anniversary Gift Jewellery | Gold & Diamond | Auric Jewels Gurgaon',
    description:
      'Find the perfect anniversary jewellery gift at Auric Jewels Gurgaon. Gold & diamond rings, pendants & bracelets. Shop online or visit showroom.',
  },
  'valentine-collection': {
    title: "Valentine's Day Jewellery Gifts | Auric Jewels Gurgaon",
    h1: "Valentine's Day Jewellery Gifts | Auric Jewels Gurgaon",
    description:
      "Shop Valentine's Day jewellery gifts at Auric Jewels Gurgaon. Diamond rings, heart pendants & love bracelets. Free gift packaging.",
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
        : `Buy ${name} online at Auric Jewels Gurgaon. ${categoryLabel} in hallmarked gold with certified diamonds. Free shipping & easy returns.`,
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
