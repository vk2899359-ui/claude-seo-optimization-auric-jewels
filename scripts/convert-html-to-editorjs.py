#!/usr/bin/env python3
"""
Convert HTML articles to Saleor EditorJS format and generate update publisher.
Converts <h1>,<h2>,<h3> -> header blocks, <p> -> paragraph blocks, <table> -> table blocks.
"""
import json, os, re, html as htmlmod

CONTENT_DIR = "content"
FILES = [
    ("blog-lightweight-gold-jewellery-working-women.html", "lightweight-gold-jewellery-working-women-daily-wear"),
    ("blog-lab-grown-vs-natural-diamonds-comparison-india.html", "lab-grown-vs-natural-diamonds-comparison-india"),
    ("blog-jewellery-trends-india-2026.html", "jewellery-trends-india-2026"),
    ("blog-gold-jewellery-investment-2026-gurgaon.html", "gold-jewellery-investment-2026-gurgaon"),
    ("blog-platinum-jewellery-men-gurgaon.html", "platinum-jewellery-men-gurgaon"),
    ("blog-layered-necklace-styling-guide-indian-women.html", "layered-necklace-styling-guide-indian-women"),
]

def html_to_editorjs(html_content):
    """Convert HTML to EditorJS blocks."""
    blocks = []
    bid = 1

    # Remove <article> wrapper
    html_content = re.sub(r'</?article>', '', html_content).strip()

    # Split into block-level elements
    # Match headers, paragraphs, tables
    pattern = r'(<h[1-3][^>]*>.*?</h[1-3]>|<p[^>]*>.*?</p>|<table[^>]*>.*?</table>)'
    parts = re.split(pattern, html_content, flags=re.DOTALL)

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Headers
        hm = re.match(r'<h([1-3])[^>]*>(.*?)</h[1-3]>', part, re.DOTALL)
        if hm:
            level = int(hm.group(1))
            text = hm.group(2).strip()
            # Strip tags from headers (keep plain text)
            text_clean = re.sub(r'<[^>]+>', '', text)
            blocks.append({
                "id": f"b{bid}",
                "type": "header",
                "data": {"text": text_clean, "level": level}
            })
            bid += 1
            continue

        # Paragraphs - keep inline HTML (a, strong, em, br)
        pm = re.match(r'<p[^>]*>(.*?)</p>', part, re.DOTALL)
        if pm:
            text = pm.group(1).strip()
            if text:
                blocks.append({
                    "id": f"b{bid}",
                    "type": "paragraph",
                    "data": {"text": text}
                })
                bid += 1
            continue

        # Tables
        tm = re.match(r'<table[^>]*>(.*?)</table>', part, re.DOTALL)
        if tm:
            table_html = tm.group(1)
            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table_html, re.DOTALL)
            content_rows = []
            has_header = '<thead' in part.lower()

            for row in rows:
                cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', row, re.DOTALL)
                cells_clean = [c.strip() for c in cells]
                content_rows.append(cells_clean)

            if content_rows:
                blocks.append({
                    "id": f"b{bid}",
                    "type": "table",
                    "data": {
                        "withHeadings": has_header,
                        "content": content_rows
                    }
                })
                bid += 1
            continue

    return {
        "time": 1712745600000,
        "blocks": blocks,
        "version": "2.24.3"
    }

# Process all articles
articles_js = []

for filename, slug in FILES:
    filepath = os.path.join(CONTENT_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()

    editorjs = html_to_editorjs(html_content)

    # Count blocks
    block_types = {}
    for b in editorjs["blocks"]:
        block_types[b["type"]] = block_types.get(b["type"], 0) + 1

    print(f"{slug}: {len(editorjs['blocks'])} blocks ({block_types})")

    # Escape for JS
    content_json = json.dumps(json.dumps(editorjs))
    articles_js.append(f'  {{slug: "{slug}", content: {content_json}}}')

# Generate the HTML publisher
js_array = ",\n".join(articles_js)

html_output = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Auric Jewels — Update Blog Content (EditorJS Format)</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',sans-serif;background:#0B1F3A;color:#F5F1E8;padding:2rem;min-height:100vh}
h1{font-size:1.4rem;margin-bottom:.5rem;color:#C9A14A}
.sub{color:rgba(245,241,232,.5);margin-bottom:1.5rem;font-size:.9rem}
button{background:linear-gradient(135deg,#C9A14A,#D4B56A);color:#0B1F3A;border:none;padding:14px 40px;border-radius:50px;font-weight:700;font-size:1rem;cursor:pointer;margin-bottom:2rem}
button:hover{box-shadow:0 8px 24px rgba(201,161,74,.4)}
button:disabled{opacity:.5;cursor:not-allowed}
.counter{margin-bottom:1rem;font-size:1.1rem;color:#C9A14A;font-weight:600}
.log{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:1.5rem;max-height:70vh;overflow-y:auto;font-family:'Consolas','Courier New',monospace;font-size:.82rem;line-height:1.9}
.ok{color:#4ADE80}.fail{color:#F87171}.info{color:#C9A14A}.dim{color:rgba(245,241,232,.4)}.warn{color:#FBBF24}
</style>
</head>
<body>
<h1>Auric Jewels — Update Blog Content (Proper EditorJS Format)</h1>
<p class="sub">Fixes content format: converts rawHtml to proper EditorJS header/paragraph/table blocks that Saleor dashboard can display.</p>
<div class="counter" id="counter">Ready — click to update all 6 blog articles</div>
<button id="start" onclick="run()">Update All 6 Blog Content</button>
<div class="log" id="log"></div>

<script>
const API = "https://auric.thecodemesh.online/graphql/";
const TOKEN = "DpDjidKqKWNnsr9zQarZKsVqnDT97D";

const log = document.getElementById("log");
const counter = document.getElementById("counter");
const btn = document.getElementById("start");

function out(msg, cls) { log.innerHTML += '<div class="'+(cls||'')+'">' + msg + '</div>'; log.scrollTop = log.scrollHeight; }

async function gql(query, variables) {
  const body = { query };
  if (variables) body.variables = variables;
  const r = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json", "Authorization": "Bearer " + TOKEN },
    body: JSON.stringify(body)
  });
  return r.json();
}

const ARTICLES = [
''' + js_array + '''
];

async function run() {
  btn.disabled = true;
  log.innerHTML = "";
  out("Updating 6 blog articles with proper EditorJS content format...", "info");
  out("", "");

  // Step 1: Get all pages to find IDs
  out("Fetching page list...", "dim");
  const r = await gql(`{ pages(first: 100) { edges { node { id slug } } } }`);
  if (r.errors) { out("Error: " + r.errors[0].message, "fail"); btn.disabled = false; return; }
  const pages = r.data?.pages?.edges || [];
  out("Found " + pages.length + " pages", "dim");
  out("", "");

  let ok = 0, fail = 0;

  for (let i = 0; i < ARTICLES.length; i++) {
    const a = ARTICLES[i];
    counter.textContent = "Updating " + (i+1) + "/" + ARTICLES.length + "...";

    const page = pages.find(p => p.node.slug === a.slug);
    if (!page) {
      out("[" + (i+1) + "] " + a.slug + " — NOT FOUND", "fail");
      fail++;
      continue;
    }

    const pageId = page.node.id;
    const contentObj = JSON.parse(a.content);
    out("[" + (i+1) + "] " + a.slug, "");
    out("&nbsp;&nbsp;&nbsp;&nbsp;ID: " + pageId + " | Blocks: " + contentObj.blocks.length, "dim");

    // Update content via pageUpdate
    const ur = await gql(`mutation($id: ID!, $input: PageInput!) {
      pageUpdate(id: $id, input: $input) {
        page { id slug title }
        errors { field message code }
      }
    }`, { id: pageId, input: { content: a.content } });

    if (ur.data?.pageUpdate?.page && !ur.data?.pageUpdate?.errors?.length) {
      out("&nbsp;&nbsp;&nbsp;&nbsp;\\u2714 Content updated with " + contentObj.blocks.length + " EditorJS blocks", "ok");
      ok++;
    } else {
      const err = ur.data?.pageUpdate?.errors?.[0] || ur.errors?.[0] || {};
      out("&nbsp;&nbsp;&nbsp;&nbsp;\\u2718 Failed: " + (err.message || JSON.stringify(err)), "fail");
      fail++;
    }
    out("", "");
    await new Promise(r => setTimeout(r, 500));
  }

  out("\\u2550".repeat(50), "dim");
  const msg = "Done: " + ok + " updated, " + fail + " failed";
  out(msg, ok === 6 ? "ok" : "warn");
  counter.textContent = msg;
  btn.disabled = false;
}
</script>
</body>
</html>'''

with open("scripts/fix-blog-content.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"\nCreated: scripts/fix-blog-content.html ({len(html_output):,} bytes)")
