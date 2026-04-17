# Auric Jewels — SEO Indexing Scripts

Three scripts for accelerating indexing of `https://www.auricjewels.com`:

| Script | Target | Recommended? |
| --- | --- | --- |
| `sitemap-submit.py` | Google Search Console + Bing Webmaster | **Yes** — the sanctioned path for e-commerce/blog pages. Run after every deploy. |
| `indexnow-submit.py` | Bing, Yandex, Seznam, Naver, Yep (via IndexNow) | **Yes** — works for any page type, no policy gotchas. Run after every deploy. |
| `bulk-index.py` | Google Indexing API (`URL_UPDATED`) | **Caution** — see policy warning below. |

All three scripts must be run **locally** on a machine that has the Google service account JSON key. They're intentionally *not* wired into CI, because running them requires a private credential that must never be committed.

---

## Policy warning on `bulk-index.py`

Google's Indexing API is officially restricted to pages containing `JobPosting` or `BroadcastEvent` structured data:

> The Indexing API can only be used to crawl pages with either `JobPosting` or `BroadcastEvent` embedded in a `VideoObject`.
> — [Google Search Central docs](https://developers.google.com/search/apis/indexing-api/v3/quickstart)

Jewelry category/product/blog pages don't qualify. Submitting them may return `200 OK` but:
- Google typically drops the notification silently for non-qualifying pages.
- The service account can be rate-limited or flagged for abuse.
- Repeated misuse has historically led to API access revocation for the project.

For Auric Jewels pages, the **correct** accelerator is `sitemap-submit.py` + `indexnow-submit.py`. `bulk-index.py` is kept here at explicit request and should be used with that understanding.

---

## One-time setup

### 1. Install Python deps

```bash
cd scripts/seo-indexing
pip install -r requirements.txt
```

### 2. Place the Google service account key

Copy the JSON key to `scripts/seo-indexing/service-account.json`:

```bash
cp ~/Downloads/auric-jewels-indexing-64015e673a7f.json \
   scripts/seo-indexing/service-account.json
```

Or point to it via env var (anywhere on disk):

```bash
export SERVICE_ACCOUNT_FILE=~/Downloads/auric-jewels-indexing-64015e673a7f.json
```

**Do not commit this file.** `.gitignore` is configured to exclude it, but double-check with `git status` before every commit.

### 3. Confirm the service account is added as an Owner in Google Search Console

Search Console → Settings → Users and permissions → Add user with the service account email (`…@…iam.gserviceaccount.com`) at **Owner** permission. Owner is required for both the Indexing API and the Search Console sitemap submission endpoint.

### 4. Generate an IndexNow key and deploy it

```bash
python indexnow-submit.py --create-key
```

This writes `public/<64-hex>.txt`. Commit it, deploy the site, then verify:

```bash
curl -I https://www.auricjewels.com/<64-hex>.txt   # expect 200 OK
```

### 5. (Optional) Get a Bing Webmaster API key

To enable Bing sitemap submission inside `sitemap-submit.py`:

1. Sign in at https://www.bing.com/webmasters/
2. Verify ownership of `auricjewels.com`
3. Settings → API access → generate key
4. Export it: `export BING_WEBMASTER_KEY=<your-key>`

Skip this and `sitemap-submit.py` will skip Bing cleanly. IndexNow still covers Bing anyway, so this is strictly optional.

---

## Running

From `scripts/seo-indexing/`:

```bash
# Recommended post-deploy flow:
python sitemap-submit.py            # Google + Bing (if configured)
python indexnow-submit.py           # Bing, Yandex, Seznam, Naver, Yep

# Optional (read the policy warning above first):
python bulk-index.py                # Google Indexing API

# Useful flags:
python bulk-index.py --dry-run      # print URL set, don't submit
python indexnow-submit.py --dry-run
```

### What each script does

**`sitemap-submit.py`** — Authenticates via the service account, calls `webmasters.sitemaps.submit` (Google) and/or Bing Webmaster `SubmitFeed`. One API call per engine; instant.

**`indexnow-submit.py`** — Fetches the live `sitemap.xml`, dedupes URLs, POSTs them in batches of up to 10,000 to three IndexNow endpoints (`api.indexnow.org`, `www.bing.com/indexnow`, `yandex.com/indexnow`). Requires the key file at `public/<key>.txt` to be live before submitting.

**`bulk-index.py`** — Fetches the live sitemap, merges with a hardcoded fallback list (in case the sitemap fetch fails), then submits each URL to Google's Indexing API with `type=URL_UPDATED`. Rate-limited to ~1.6 req/s. The fallback list is kept in the script for resilience; edit it there if you ever need to hand-curate the URL set.

---

## Verifying results

- **Google:** https://search.google.com/search-console/ → Sitemaps + URL Inspection
- **Bing:** https://www.bing.com/webmasters/ → URL submission + Sitemaps
- **IndexNow:** check server logs for visits from `BingBot`, `YandexBot`, etc., hitting the key file (proof the engines picked up your submission).

Indexing takes 24–72 hours typically, longer for new sites.

---

## Troubleshooting

**`403 PERMISSION_DENIED` from Indexing API** — Service account isn't Owner in Search Console, or the site property isn't verified. Add as Owner; re-verify via DNS or HTML file.

**`400 Failed to parse URL` from Indexing API** — URL must match the verified property exactly, including `https://` and trailing slash rules. Don't mix `www` / non-`www`.

**IndexNow `422 Unprocessable Entity`** — Key file is not reachable. Check: deployed? correct path? content exactly matches the filename stem?

**Sitemap fetch returns empty list** — Hit `https://www.auricjewels.com/sitemap.xml` in a browser. If it's a sitemap index, the scripts walk it recursively, but a 404 or empty file means `next-sitemap` didn't run at build — check the deploy pipeline.
