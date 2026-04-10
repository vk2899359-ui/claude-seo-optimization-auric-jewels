# Google Search Console Setup & Blog Indexing Guide for Auric Jewels

**Website:** www.auricjewels.com
**Last Updated:** April 2026

This guide walks you through setting up Google Search Console (GSC), submitting your sitemap, and getting all Auric Jewels blog pages indexed on Google as fast as possible.

---

## Table of Contents

1. [Setting Up Google Search Console](#1-setting-up-google-search-console)
2. [Verifying Domain Ownership](#2-verifying-domain-ownership)
3. [Submitting Your Sitemap](#3-submitting-your-sitemap)
4. [Requesting Indexing for Blog URLs](#4-requesting-indexing-for-blog-urls)
5. [Tips for Faster Indexing](#5-tips-for-faster-indexing)
6. [Monitoring Indexing Status](#6-monitoring-indexing-status)
7. [Checking Search Performance for Blog Keywords](#7-checking-search-performance-for-blog-keywords)
8. [Blog URLs to Index](#8-blog-urls-to-index)

---

## 1. Setting Up Google Search Console

Google Search Console is a free tool from Google that lets you monitor how your website appears in Google Search results. It tells you which pages are indexed, what keywords bring visitors, and alerts you to any problems.

### Steps to Get Started

1. Open your browser and go to **https://search.google.com/search-console**
2. Sign in with the Google account you want to manage the website with (use a company Google account if you have one)
3. Click **"Add property"** (top-left dropdown)
4. You will see two options:
   - **Domain** (recommended) -- covers all subdomains and protocols (http, https, www, non-www)
   - **URL prefix** -- covers only the exact URL pattern you enter
5. For Auric Jewels, choose **Domain** and enter: `auricjewels.com`
   - If you prefer URL prefix, enter: `https://www.auricjewels.com`
6. Click **Continue** to proceed to verification

---

## 2. Verifying Domain Ownership

Google needs to confirm that you own the website. There are several methods -- pick whichever is easiest for you.

### Method A: DNS Record Verification (Recommended for Domain property)

This is the most reliable method and works for the "Domain" property type.

1. Google will show you a TXT record that looks like: `google-site-verification=XXXXXXXXXXXX`
2. Log in to your domain registrar (GoDaddy, Namecheap, Cloudflare, etc.)
3. Go to **DNS Settings** for `auricjewels.com`
4. Add a new **TXT record**:
   - **Host/Name:** `@` (or leave blank)
   - **Type:** TXT
   - **Value:** paste the verification string Google gave you
   - **TTL:** 3600 (or default)
5. Save the record
6. Go back to Google Search Console and click **Verify**
7. It may take a few minutes to a few hours for DNS to propagate. If verification fails, wait 30 minutes and try again.

### Method B: HTML Meta Tag (URL Prefix only)

1. Google will give you a meta tag like: `<meta name="google-site-verification" content="XXXXXXXXXXXX" />`
2. Add this tag inside the `<head>` section of your homepage
3. In a Next.js project, add it to your `_app.js` or `layout.tsx` file inside a `<Head>` component
4. Deploy the change to your live website
5. Go back to Google Search Console and click **Verify**

### Method C: HTML File Upload (URL Prefix only)

1. Google will give you a file to download (e.g., `googleXXXXXXXXXXXX.html`)
2. Place this file in your `/public` folder in your Next.js project
3. Deploy the change so the file is accessible at `https://www.auricjewels.com/googleXXXXXXXXXXXX.html`
4. Go back to Google Search Console and click **Verify**

### Verification Tips

- DNS verification is the best option because it covers everything automatically
- Once verified, do NOT remove the verification record/tag -- Google re-checks periodically
- You can add multiple users to Search Console under **Settings > Users and permissions**

---

## 3. Submitting Your Sitemap

A sitemap tells Google about all the pages on your website and helps Google find and index them.

### Your Sitemap URL

```
https://www.auricjewels.com/sitemap.xml
```

### How to Submit

1. In Google Search Console, click **Sitemaps** in the left menu
2. In the "Add a new sitemap" box, enter: `sitemap.xml`
3. Click **Submit**
4. You should see a green "Success" status after a few moments
5. Google will now regularly check your sitemap for new pages

### What to Expect

- Google will show the number of URLs discovered in your sitemap
- It may take a few days for Google to fully process the sitemap
- You can re-submit the sitemap anytime you add new blog posts

---

## 4. Requesting Indexing for Blog URLs

After submitting the sitemap, you should also manually request indexing for each blog URL. This speeds things up significantly.

### Using the URL Inspection Tool

1. In Google Search Console, click the **search bar at the top** of the page (it says "Inspect any URL...")
2. Paste the full blog URL, for example:
   ```
   https://www.auricjewels.com/blog/lightweight-gold-jewellery-working-women-daily-wear
   ```
3. Press **Enter**
4. Google will check whether this URL is already indexed
5. If the URL is **not indexed**, you will see a message saying "URL is not on Google"
6. Click the **"Request Indexing"** button
7. Google will add the URL to its priority crawl queue
8. Repeat this process for each blog URL (see the full list below)

### Important Notes

- There is a **daily limit** on indexing requests (roughly 10-12 per day per property). Do not exceed this.
- After requesting indexing, it typically takes **a few hours to a few days** for the page to appear in search results.
- If the URL is already indexed, you will see "URL is on Google" -- no action needed.

### Step-by-Step for Each Blog URL

Repeat the URL Inspection process for each of these URLs:

| # | Blog URL | Status |
|---|----------|--------|
| 1 | `https://www.auricjewels.com/blog/lightweight-gold-jewellery-working-women-daily-wear` | Live |
| 2 | `https://www.auricjewels.com/blog/lab-grown-vs-natural-diamonds-comparison-india` | Live |
| 3 | `https://www.auricjewels.com/blog/jewellery-trends-india-2026` | Live |
| 4 | `https://www.auricjewels.com/blog/gold-jewellery-investment-2026-gurgaon` | Live |
| 5 | `https://www.auricjewels.com/blog/platinum-jewellery-men-gurgaon` | Live |
| 6 | `https://www.auricjewels.com/blog/layered-necklace-styling-guide-indian-women` | Live |
| 7 | `https://www.auricjewels.com/blog/akshaya-tritiya-gold-buying-guide-2026-gurgaon` | Coming Soon |
| 8 | `https://www.auricjewels.com/blog/bridal-jewellery-set-guide-indian-bride-2026` | Coming Soon |
| 9 | `https://www.auricjewels.com/blog/solitaire-diamond-ring-buying-guide-gurgaon` | Coming Soon |
| 10 | `https://www.auricjewels.com/blog/gold-rate-today-gurgaon-2026-price-trends` | Coming Soon |

---

## 5. Tips for Faster Indexing

Google can take days or weeks to index new pages. Here are proven ways to speed it up:

### a) Ping the Sitemap

Notify Google that your sitemap has been updated by visiting this URL in your browser:

```
https://www.google.com/ping?sitemap=https://www.auricjewels.com/sitemap.xml
```

Do this every time you publish a new blog post.

### b) Share on Social Media

Google's crawlers follow links from social media platforms. Share each blog post on:
- Instagram (link in bio or stories)
- Facebook business page
- LinkedIn
- Twitter/X
- WhatsApp Business status
- Google Business Profile posts (very effective for local SEO)

### c) Google Business Profile

If Auric Jewels has a Google Business Profile (Google Maps listing):
1. Go to **https://business.google.com**
2. Create a new **Post** with a link to each blog article
3. Google indexes these links very quickly since they come from Google's own platform

### d) Internal Linking

Make sure your blog pages link to each other and that your main website pages link to the blog:
- Add a "Blog" or "Articles" link in your website's navigation menu
- Each blog post should link to 2-3 other blog posts
- Your homepage should have a "Latest from Our Blog" section linking to recent posts

### e) Submit to Bing Webmaster Tools

Don't forget Bing! About 5-10% of search traffic in India comes from Bing.

1. Go to **https://www.bing.com/webmasters**
2. Sign in with a Microsoft account
3. Add your site and verify ownership
4. Submit your sitemap: `https://www.auricjewels.com/sitemap.xml`

### f) Fetch as Google (URL Inspection)

After requesting indexing through the URL Inspection tool, click **"Test Live URL"** to make sure Google can access the page without errors. Fix any issues it reports.

---

## 6. Monitoring Indexing Status

### Check Which Pages Are Indexed

1. In Google Search Console, go to **Pages** (left menu, under "Indexing")
2. You will see a chart showing:
   - **Indexed** pages (green) -- pages that appear in Google
   - **Not indexed** pages (gray) -- pages Google knows about but hasn't indexed
3. Click on "Not indexed" to see the reasons and fix any issues

### Quick Check in Google Search

You can also check if a specific page is indexed by searching on Google:

```
site:www.auricjewels.com/blog/lightweight-gold-jewellery-working-women-daily-wear
```

If the page appears in results, it is indexed. If it shows "No results found," it is not yet indexed.

### Check All Blog Pages at Once

Search on Google:
```
site:www.auricjewels.com/blog/
```

This will show all indexed blog pages.

---

## 7. Checking Search Performance for Blog Keywords

Once your blog pages are indexed and receiving traffic, monitor their performance:

### Using the Performance Report

1. In Google Search Console, click **Performance** (left menu)
2. You will see charts for:
   - **Total clicks** -- how many times people clicked on your pages from Google
   - **Total impressions** -- how many times your pages appeared in search results
   - **Average CTR** -- click-through rate (clicks divided by impressions)
   - **Average position** -- your average ranking position in search results

### Filter by Blog Pages

1. Click **+ New** at the top of the Performance page
2. Select **Page**
3. Choose "URLs containing" and enter: `/blog/`
4. Click **Apply**
5. Now you see performance data only for your blog pages

### Check Which Keywords Drive Traffic

1. With the blog filter applied, click the **Queries** tab below the chart
2. This shows the exact keywords people used to find your blog posts
3. Look for keywords where you have high impressions but low CTR -- these are opportunities to improve your title tags and meta descriptions

### Key Metrics to Watch

| Metric | What it means | Good target |
|--------|--------------|-------------|
| Impressions | How often your pages appear in search | Growing month over month |
| Clicks | How many visitors came from search | Growing month over month |
| CTR | % of people who click when they see your result | Above 3% |
| Position | Average ranking in search results | Below 20 (first 2 pages) |

### Set Up Email Alerts

Google Search Console automatically sends email alerts for:
- Indexing issues
- Security problems
- Manual actions
- Make sure the email on your Google account is one you check regularly

---

## 8. Blog URLs to Index

Here is the complete list of blog URLs for quick copy-paste into the URL Inspection tool:

### Currently Live (Index These Now)

```
https://www.auricjewels.com/blog/lightweight-gold-jewellery-working-women-daily-wear
https://www.auricjewels.com/blog/lab-grown-vs-natural-diamonds-comparison-india
https://www.auricjewels.com/blog/jewellery-trends-india-2026
https://www.auricjewels.com/blog/gold-jewellery-investment-2026-gurgaon
https://www.auricjewels.com/blog/platinum-jewellery-men-gurgaon
https://www.auricjewels.com/blog/layered-necklace-styling-guide-indian-women
```

### Coming Soon (Index After Publishing)

```
https://www.auricjewels.com/blog/akshaya-tritiya-gold-buying-guide-2026-gurgaon
https://www.auricjewels.com/blog/bridal-jewellery-set-guide-indian-bride-2026
https://www.auricjewels.com/blog/solitaire-diamond-ring-buying-guide-gurgaon
https://www.auricjewels.com/blog/gold-rate-today-gurgaon-2026-price-trends
```

### Sitemap URL

```
https://www.auricjewels.com/sitemap.xml
```

---

## Quick-Reference Checklist

Use this checklist every time you publish a new blog post:

- [ ] Blog post is live on the website
- [ ] Open Google Search Console
- [ ] Use URL Inspection tool to request indexing for the new URL
- [ ] Ping the sitemap: `https://www.google.com/ping?sitemap=https://www.auricjewels.com/sitemap.xml`
- [ ] Share the blog post on social media (Instagram, Facebook, LinkedIn, Twitter)
- [ ] Create a Google Business Profile post with the blog link
- [ ] Add internal links from other blog posts and website pages to the new post
- [ ] Check indexing status in 2-3 days using `site:www.auricjewels.com/blog/your-url`
- [ ] Submit the URL to Bing Webmaster Tools as well

---

*Need help? Contact your web developer or refer to Google's official documentation at https://support.google.com/webmasters*
