"""
Auric Jewels — Daily SEO Automation Routine
============================================
Scheduled via Windows Task Scheduler to run daily at 9 AM.

Flow:
  1. Pick today's keyword (rotating bank, seasonal-aware, no repeats for 60 days)
  2. Draft 1000+ word blog via Claude API (haiku-4-5 for cost efficiency)
  3. Save HTML to content/blog-{slug}.html as local backup
  4. Publish to Saleor via Playwright browser automation (Cloudflare-safe)
  5. Append result row to AURIC_PROGRESS.md

Requirements (run install-deps.ps1 once):
  pip install anthropic playwright
  playwright install chromium

Environment variables:
  ANTHROPIC_API_KEY   — required for blog drafting
"""

import json
import os
import re
import sys
import time
from datetime import date, datetime

# ── Config ────────────────────────────────────────────────────────────────────

API        = "https://auric.thecodemesh.online/graphql/"
ORIGIN     = "https://auric.thecodemesh.online"
TOKEN      = "EXjfazrP5PWBz5LE0TyckHNvQ5M7Q1"
PAGE_TYPE  = "UGFnZVR5cGU6Ng=="
CHANNEL    = "franchise1"

ROOT        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(ROOT, "content")
PROGRESS_MD = os.path.join(ROOT, "AURIC_PROGRESS.md")
STATE_FILE  = os.path.join(ROOT, "scripts", ".seo-state.json")

# ── Keyword bank (60 topics, seasonal-aware) ─────────────────────────────────
#
# Each entry: (keyword, meta_category, peak_months)
# peak_months = None means always relevant.
# Seasonal entries are preferred when their month matches today.

KEYWORD_BANK = [
    # Core — always relevant
    ("diamond jewellery showroom gurgaon",          "Diamond Jewellery",  None),
    ("gold jewellery gurgaon 2026",                 "Gold Jewellery",     None),
    ("engagement ring gurgaon",                     "Engagement Rings",   None),
    ("bridal jewellery set gurgaon",                "Bridal Jewellery",   None),
    ("solitaire diamond ring gurgaon",              "Solitaire Rings",    None),
    ("diamond earrings gurgaon",                    "Diamond Earrings",   None),
    ("gold bangles gurgaon",                        "Gold Bangles",       None),
    ("platinum jewellery gurgaon",                  "Platinum Jewellery", None),
    ("diamond necklace gurgaon",                    "Diamond Necklaces",  None),
    ("jewellery showroom sector 45 gurgaon",        "Showroom Guide",     None),
    # Product-specific
    ("diamond mangalsutra modern designs 2026",     "Mangalsutra",        None),
    ("lab grown diamonds india 2026",               "Lab Grown Diamonds", None),
    ("polki jewellery bridal gurgaon",              "Polki Jewellery",    None),
    ("kundan jewellery wedding gurgaon",            "Kundan Jewellery",   None),
    ("antique gold jewellery gurgaon",              "Heritage Jewellery", None),
    ("rose gold jewellery gurgaon",                 "Rose Gold",          None),
    ("white gold ring gurgaon",                     "White Gold",         None),
    ("diamond bracelet women gurgaon",              "Diamond Bracelets",  None),
    ("gold chain for men gurgaon",                  "Men's Jewellery",    None),
    ("diamond pendant necklace gurgaon",            "Diamond Pendants",   None),
    ("gold earrings traditional gurgaon",           "Gold Earrings",      None),
    ("diamond studs gurgaon",                       "Diamond Studs",      None),
    ("bridal necklace set gurgaon 2026",            "Bridal Sets",        None),
    ("wedding bands platinum gurgaon",              "Wedding Bands",      None),
    ("custom diamond jewellery gurgaon",            "Bespoke Jewellery",  None),
    ("IGI certified diamond ring gurgaon",          "Diamond Rings",      None),
    ("GIA diamond buying guide india",              "Diamond Guide",      None),
    ("diamond ring under 2 lakh gurgaon",           "Diamond Rings",      None),
    ("stackable gold rings gurgaon",                "Gold Rings",         None),
    ("heirloom jewellery redesign gurgaon",         "Custom Jewellery",   None),
    # Occasion / seasonal
    ("diwali jewellery gift gurgaon 2026",          "Festival Jewellery", [10, 11]),
    ("dhanteras gold jewellery gurgaon 2026",       "Festival Jewellery", [10, 11]),
    ("akshaya tritiya gold jewellery 2026",         "Gold Investment",    [4,  5]),
    ("karva chauth jewellery gurgaon 2026",         "Festival Jewellery", [10]),
    ("navratri jewellery gurgaon 2026",             "Festival Jewellery", [10]),
    ("valentine jewellery gift gurgaon",            "Gift Jewellery",     [1,  2]),
    ("mother's day jewellery gift gurgaon",         "Gift Jewellery",     [5]),
    ("anniversary jewellery gift gurgaon",          "Anniversary",        None),
    ("birthday jewellery gift gurgaon",             "Gift Jewellery",     None),
    ("wedding season jewellery delhi ncr",          "Bridal Jewellery",   [11, 12, 1, 2]),
    # Buying guides / informational
    ("how to buy diamond jewellery india 2026",     "Buying Guide",       None),
    ("gold jewellery investment india 2026",        "Gold Investment",    None),
    ("22k vs 18k gold jewellery india",             "Gold Guide",         None),
    ("bis hallmark gold jewellery guide",           "Gold Purity",        None),
    ("diamond 4cs buying guide india",              "Diamond Guide",      None),
    ("best jewellery showroom gurgaon",             "Showroom Guide",     None),
    ("jewellery care tips india",                   "Jewellery Care",     None),
    ("how to choose bridal jewellery india",        "Bridal Guide",       None),
    ("diamond vs gold jewellery investment india",  "Buying Guide",       None),
    ("solitaire vs halo ring comparison india",     "Diamond Guide",      None),
    # Long-tail
    ("lightweight gold jewellery working women gurgaon", "Daily Wear",   None),
    ("diamond earrings under 50000 gurgaon",        "Diamond Earrings",   None),
    ("gold necklace under 1 lakh gurgaon",          "Gold Necklaces",     None),
    ("platinum jewellery groom gurgaon",            "Men's Jewellery",    None),
    ("solitaire 0.5 carat diamond gurgaon",         "Solitaire Rings",    None),
    ("jewellery exchange policy gurgaon",           "Buying Guide",       None),
    ("mangalsutra modern designs 2026",             "Mangalsutra",        None),
    ("diamond jewellery men gurgaon",               "Men's Jewellery",    None),
    ("daily wear diamond ring gurgaon",             "Daily Wear",         None),
    ("gold jewellery gifting guide india",          "Gift Jewellery",     None),
]

# ── State (tracks recently used keywords) ────────────────────────────────────

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"used_slugs": [], "total_published": 0, "last_run": None}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# ── Keyword selection ─────────────────────────────────────────────────────────

def pick_keyword(state):
    """
    Prefer seasonal keywords whose peak_months include today's month.
    Avoid keywords used in the last 60 days (tracked by slug in state).
    Falls back to day-of-year rotation if everything is used.
    """
    today_month = date.today().month
    recent = set(state.get("used_slugs", [])[-60:])

    # Score: seasonal match = 2, unused = 1, else 0
    candidates = []
    for kw, category, months in KEYWORD_BANK:
        slug = re.sub(r"[^a-z0-9]+", "-", kw.lower()).strip("-")
        if slug in recent:
            continue
        score = 2 if (months and today_month in months) else 1
        candidates.append((score, kw, category, slug))

    if not candidates:
        # All used — reset and pick by day-of-year
        state["used_slugs"] = []
        idx = date.today().timetuple().tm_yday % len(KEYWORD_BANK)
        kw, category, _ = KEYWORD_BANK[idx]
        slug = re.sub(r"[^a-z0-9]+", "-", kw.lower()).strip("-")
        return kw, category, slug

    candidates.sort(key=lambda x: (-x[0], x[1]))
    _, kw, category, slug = candidates[0]
    return kw, category, slug


# ── Blog drafting (Claude API) ────────────────────────────────────────────────

BLOG_SYSTEM_PROMPT = """\
You are a luxury jewellery editorial writer for Auric Jewels, a premium showroom in \
Sector 45, Gurgaon. Your writing style is authoritative and editorial — think Vogue \
Living or Architectural Digest applied to fine jewellery.

STRICT RULES:
- Never use: budget, affordable, cheap, bargain, deal, inexpensive, low-cost
- Use instead: investment, curated, crafted, certified, discerning, heritage, connoisseur
- Always mention: IGI or GIA certified diamonds, BIS hallmarked gold, Sector 45 Gurgaon
- Phone number for CTAs: +91-9012495941
- Website: https://www.auricjewels.com

OUTPUT FORMAT — return only the raw HTML, no markdown fences, no commentary:

<article>

<h1>[keyword-rich title — 60-70 chars]</h1>

<p>[150-word intro. Must mention "Auric Jewels" and "Sector 45, Gurgaon". \
Natural keyword placement in first sentence.]</p>

[4-5 × <h2> sections, each with 2-3 × <h3> subsections and 100-150 word paragraphs]

[exactly one <table> with <thead>/<tbody> comparing 2+ options across 5+ rows]

[2-3 paragraphs that START with: "At Auric Jewels, "]

<h2>Frequently Asked Questions</h2>

[4-5 × <h3> questions ending with "?" each immediately followed by a <p> answer]

<h2>[closing CTA h2]</h2>

<p>[closing paragraph with phone link <a href="tel:+919012495941"> and \
<a href="https://www.auricjewels.com"> website link]</p>

</article>

TARGET LENGTH: 1,100–1,400 words.
"""

def draft_blog(keyword, category):
    """Call Claude haiku to generate the blog. Returns raw HTML string."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("  !! ANTHROPIC_API_KEY not set — using template fallback")
        return _template_fallback(keyword, category)

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4096,
            system=BLOG_SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": (
                    f"Write a complete SEO blog article targeting the keyword: "
                    f'"{keyword}"\n'
                    f"Category context: {category}\n"
                    f"Today's date: {date.today().strftime('%d %B %Y')}\n"
                    f"Return only the HTML. Start with <article> and end with </article>."
                ),
            }],
        )
        html = message.content[0].text.strip()
        # Strip any accidental markdown fences
        html = re.sub(r"^```html\s*", "", html, flags=re.IGNORECASE)
        html = re.sub(r"\s*```$", "", html)
        return html
    except Exception as e:
        print(f"  !! Claude API error: {e} — using template fallback")
        return _template_fallback(keyword, category)


def _template_fallback(keyword, category):
    """Minimal but valid HTML article for when Claude API is unavailable."""
    title = keyword.title()
    return f"""\
<article>

<h1>{title} — Expert Guide from Auric Jewels Gurgaon</h1>

<p>For discerning buyers seeking {keyword}, Auric Jewels in Sector 45, Gurgaon offers \
an unrivalled selection of certified pieces crafted to the highest standard. Every diamond \
is IGI or GIA certified; every gold piece carries a BIS hallmark with HUID verification. \
This guide covers what to look for, what to ask, and why Auric Jewels is the address \
families across Delhi NCR trust for {category.lower()}.</p>

<h2>What to Look for When Buying {title}</h2>

<h3>Certification First</h3>
<p>No fine jewellery purchase should be made without independent certification. \
At Auric Jewels, every diamond above 0.10 carats carries an IGI or GIA report \
detailing cut, colour, clarity, and carat weight — the four criteria that determine \
a diamond's true value.</p>

<h3>Metal Purity</h3>
<p>BIS hallmarking with a Hallmark Unique Identification number is the only guarantee \
of gold purity in India. Auric Jewels provides the HUID on your purchase certificate, \
allowing independent verification on the BIS Care app.</p>

<h2>Collections Available at Auric Jewels, Sector 45</h2>

<h3>18K Gold Collection</h3>
<p>Our 18K collection — 75 per cent pure gold — is crafted for daily wear and \
contemporary styling. Available in white, yellow, and rose gold across all categories.</p>

<h3>22K Gold Heritage Collection</h3>
<p>Traditional jewellery in 91.6 per cent pure 22K gold, suited to occasions that call \
for the warm lustre of heritage craftsmanship.</p>

<h2>Price Comparison</h2>

<table>
<thead><tr><th>Category</th><th>Metal</th><th>Starting Price</th><th>Certification</th></tr></thead>
<tbody>
<tr><td>Diamond Rings</td><td>18K White Gold</td><td>₹35,000</td><td>IGI/GIA</td></tr>
<tr><td>Gold Necklaces</td><td>22K BIS Hallmarked</td><td>₹45,000</td><td>BIS HUID</td></tr>
<tr><td>Diamond Earrings</td><td>18K Gold</td><td>₹25,000</td><td>IGI/GIA</td></tr>
<tr><td>Platinum Rings</td><td>95% Platinum</td><td>₹60,000</td><td>Certified</td></tr>
<tr><td>Bridal Sets</td><td>22K / 18K Fusion</td><td>₹1,50,000</td><td>IGI + BIS HUID</td></tr>
</tbody>
</table>

<p>At Auric Jewels, pricing is fully transparent — gold value, making charges, stone \
value, and GST are itemised separately on every purchase bill. This standard is \
non-negotiable because our buyers deserve to understand exactly where their investment goes.</p>

<h2>Why Families Across Delhi NCR Choose Auric Jewels</h2>

<p>At Auric Jewels in Sector 45, Gurgaon, every visit is a private consultation — \
not a transaction. Our consultants take time to understand the occasion, the wearer, \
and the aesthetic before presenting options. There is no commission incentive and no \
pressure. The result is a jewellery purchase made with full information and genuine confidence.</p>

<h2>Frequently Asked Questions</h2>

<h3>Where is Auric Jewels located in Gurgaon?</h3>
<p>Auric Jewels is located in Sector 45, Gurgaon, open seven days a week from \
10:00 AM to 8:00 PM. Private appointments are available by calling \
<a href="tel:+919012495941">+91-9012495941</a>.</p>

<h3>Are all diamonds at Auric Jewels certified?</h3>
<p>Yes. Every diamond at Auric Jewels carries an IGI or GIA certification report. \
This applies to all pieces across all price points without exception.</p>

<h3>Does Auric Jewels offer an exchange policy?</h3>
<p>Yes. Auric Jewels offers a lifetime exchange at full current gold value for all \
gold and gold-diamond pieces, plus a 15-day return policy from purchase date.</p>

<h3>Can I order Auric Jewels jewellery online?</h3>
<p>Yes. The full collection is available at \
<a href="https://www.auricjewels.com">auricjewels.com</a> with free insured shipping \
across India and a certificate of authenticity included with every order.</p>

<h2>Visit Auric Jewels — Gurgaon's Most Trusted Jewellery Showroom</h2>

<p>Experience the finest {keyword} at Auric Jewels, Sector 45, Gurgaon. Our showroom \
is open 10:00 AM to 8:00 PM, seven days a week. Book a private consultation at \
<a href="tel:+919012495941">+91-9012495941</a> or explore the collection online at \
<a href="https://www.auricjewels.com">auricjewels.com</a>.</p>

</article>"""


# ── Content helpers ───────────────────────────────────────────────────────────

def slug_from_keyword(keyword):
    return re.sub(r"[^a-z0-9]+", "-", keyword.lower()).strip("-")


def editorjs_content(html):
    doc = {
        "time": 0,
        "version": "2.26.5",
        "blocks": [{"type": "rawHtml", "data": {"html": html}}],
    }
    return json.dumps(doc, ensure_ascii=False)


def extract_title(html):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.IGNORECASE | re.DOTALL)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    return ""


def save_html(slug, html):
    os.makedirs(CONTENT_DIR, exist_ok=True)
    path = os.path.join(CONTENT_DIR, f"blog-{slug}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


# ── Playwright publisher (Cloudflare-safe) ────────────────────────────────────

PAGE_CREATE_MUTATION = """
mutation PageCreate($input: PageCreateInput!) {
  pageCreate(input: $input) {
    page { id slug title }
    errors { field message code }
  }
}
"""

CHANNEL_LISTING_MUTATION = """
mutation PageChannelListing($id: ID!, $input: PageChannelListingUpdateInput!) {
  pageChannelListingUpdate(id: $id, input: $input) {
    page { id slug }
    errors { field message code }
  }
}
"""

CHANNEL_QUERY = """
query { channel(slug: "%s") { id } }
"""


def publish_via_playwright(title, slug, html, meta_title, meta_desc):
    """
    Launch headless Chromium, navigate to the site to pick up Cloudflare
    session cookies, then run the GraphQL mutation via the browser's own
    fetch() — indistinguishable from a real user's browser request.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {"error": "playwright not installed — run: pip install playwright && playwright install chromium"}

    variables = {
        "input": {
            "title":       title,
            "slug":        slug,
            "pageType":    PAGE_TYPE,
            "isPublished": True,
            "content":     editorjs_content(html),
            "seo": {
                "title":       meta_title[:70],
                "description": meta_desc[:160],
            },
        }
    }

    js_fetch = """
    async ({ api, token, mutation, variables }) => {
        try {
            const resp = await fetch(api, {
                method: 'POST',
                headers: {
                    'Content-Type':  'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({ query: mutation, variables }),
            });
            const text = await resp.text();
            try { return { ok: true, data: JSON.parse(text) }; }
            catch { return { ok: false, error: 'non-json', body: text.slice(0, 500) }; }
        } catch(e) {
            return { ok: false, error: e.message };
        }
    }
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            locale="en-US",
            timezone_id="Asia/Kolkata",
        )
        page = context.new_page()

        # Step 1 — navigate to site to establish Cloudflare session cookies
        print("    Browser: navigating to site for Cloudflare session…")
        try:
            page.goto(ORIGIN, wait_until="domcontentloaded", timeout=30_000)
            page.wait_for_timeout(2_000)
        except Exception as e:
            print(f"    Browser: warm-up nav failed ({e}) — proceeding anyway")

        # Step 2 — run pageCreate via fetch inside the browser context
        print("    Browser: executing pageCreate mutation…")
        raw = page.evaluate(js_fetch, {
            "api":       API,
            "token":     TOKEN,
            "mutation":  PAGE_CREATE_MUTATION,
            "variables": variables,
        })

        if not raw.get("ok"):
            browser.close()
            return {"error": raw.get("error", "unknown"), "body": raw.get("body", "")}

        result = raw["data"]
        page_create = (result.get("data") or {}).get("pageCreate") or {}
        gql_errors = page_create.get("errors") or result.get("errors") or []

        if gql_errors:
            browser.close()
            return {"errors": gql_errors}

        created_page = page_create.get("page") or {}
        page_id = created_page.get("id")

        # Step 3 — add channel listing (best-effort, non-fatal)
        if page_id:
            print(f"    Browser: adding channel listing ({CHANNEL})…")
            try:
                ch_raw = page.evaluate(js_fetch, {
                    "api":      API,
                    "token":    TOKEN,
                    "mutation": CHANNEL_QUERY % CHANNEL,
                    "variables": {},
                })
                channel_id = (
                    ((ch_raw.get("data") or {}).get("data") or {})
                    .get("channel", {}).get("id")
                )
                if channel_id:
                    page.evaluate(js_fetch, {
                        "api":      API,
                        "token":    TOKEN,
                        "mutation": CHANNEL_LISTING_MUTATION,
                        "variables": {
                            "id": page_id,
                            "input": {
                                "addChannels": [{"channelId": channel_id, "isPublished": True}]
                            },
                        },
                    })
            except Exception as e:
                print(f"    Browser: channel listing step failed ({e}) — page still published")

        browser.close()
        return {"page": created_page}


# ── Progress log ──────────────────────────────────────────────────────────────

DAILY_LOG_HEADER = "\n## Daily Automation Log\n\n| Date | Keyword | Slug | Status |\n|------|---------|------|--------|\n"


def log_progress(keyword, slug, status):
    today = date.today().isoformat()
    row = f"| {today} | {keyword} | `{slug}` | {status} |\n"

    with open(PROGRESS_MD, "a", encoding="utf-8") as f:
        # Write the table header once if the section doesn't exist yet
        if "Daily Automation Log" not in open(PROGRESS_MD, encoding="utf-8").read():
            f.write(DAILY_LOG_HEADER)
        f.write(row)

    print(f"  Logged to AURIC_PROGRESS.md: {row.strip()}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print()
    print("=" * 60)
    print(f"  Auric Jewels — Daily SEO Routine  [{datetime.now().strftime('%Y-%m-%d %H:%M')}]")
    print("=" * 60)

    state = load_state()

    # 1. Pick keyword
    print("\nSTEP 1: Selecting keyword")
    keyword, category, slug = pick_keyword(state)
    print(f"  Keyword  : {keyword}")
    print(f"  Category : {category}")
    print(f"  Slug     : {slug}")

    # 2. Draft blog
    print("\nSTEP 2: Drafting blog post (Claude API)")
    html = draft_blog(keyword, category)
    title = extract_title(html) or keyword.title()
    word_count = len(re.sub(r"<[^>]+>", " ", html).split())
    print(f"  Title    : {title}")
    print(f"  Words    : {word_count:,}")

    # 3. Save HTML locally
    print("\nSTEP 3: Saving HTML to content/")
    saved_path = save_html(slug, html)
    print(f"  Saved    : {os.path.relpath(saved_path, ROOT)}")

    # 4. Publish via Playwright
    print("\nSTEP 4: Publishing via Playwright (Cloudflare-safe browser automation)")
    meta_title = f"{title} | Auric Jewels"
    meta_desc  = (
        re.sub(r"<[^>]+>", " ", html)
        .split(".")[0].strip()[:157] + "…"
    )
    result = publish_via_playwright(title, slug, html, meta_title, meta_desc)

    if "error" in result:
        status = f"❌ FAILED — {result['error'][:80]}"
        if result.get("body"):
            print(f"    Body: {result['body'][:300]}")
    elif "errors" in result:
        msgs = "; ".join(f"[{e.get('field','?')}] {e.get('message','?')}" for e in result["errors"])
        status = f"❌ FAILED — {msgs[:100]}"
    else:
        page = result.get("page", {})
        page_id   = page.get("id", "?")
        page_slug = page.get("slug", slug)
        status = f"✅ PUBLISHED — id={page_id}"
        print(f"  Published: https://www.auricjewels.com/blog/{page_slug}")

    print(f"\n  Status: {status}")

    # 5. Update state
    used = state.get("used_slugs", [])
    used.append(slug)
    state["used_slugs"]       = used[-120:]   # keep last 120 entries (~4 months)
    state["last_run"]         = date.today().isoformat()
    state["total_published"]  = state.get("total_published", 0) + (1 if "✅" in status else 0)
    save_state(state)

    # 6. Log to AURIC_PROGRESS.md
    print("\nSTEP 5: Logging to AURIC_PROGRESS.md")
    log_progress(keyword, slug, status)

    print()
    print("=" * 60)
    print(f"  Done. Total published via automation: {state['total_published']}")
    print("=" * 60)
    print()

    sys.exit(0 if "✅" in status else 1)


if __name__ == "__main__":
    main()
