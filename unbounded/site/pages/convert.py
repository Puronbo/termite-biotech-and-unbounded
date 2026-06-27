#!/usr/bin/env python3
"""Convert markdown files to styled HTML pages for the UNBOUNDED site."""
import os, sys, re, markdown

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
SITE_ROOT = os.path.join(REPO_ROOT, 'unbounded', 'site')
OUTPUT_DIR = os.path.join(SITE_ROOT, 'pages')

TEMPLATE = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{meta_desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://Puronbo.github.io/termite-biotech-and-unbounded/unbounded/site/pages/{rel_path}">
<meta property="og:image" content="https://raw.githubusercontent.com/Puronbo/termite-biotech-and-unbounded/main/unbounded/site/favicon.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0e0e16">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap" rel="stylesheet">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<title>{title}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{
  --bg: #08080c; --surface: #0e0e16; --surface2: #14142e;
  --border: rgba(255,255,255,0.05); --accent: #7c3aed; --accent2: #ff6b35;
  --accent3: #60a5fa; --fg: #e0e0ec; --muted: #7878a0;
  --radius: 12px;
}}
body {{
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--bg); color: var(--fg); line-height: 1.7;
  min-height: 100vh;
}}
body::before {{
  content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: radial-gradient(ellipse at 50% 0%, rgba(124,58,237,0.06) 0%, transparent 70%);
  pointer-events: none; z-index: 0;
}}
.wrapper {{
  max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem 4rem;
  position: relative; z-index: 1;
}}
.top-nav {{
  display: flex; align-items: center; gap: 1rem; padding: 0.75rem 0;
  margin-bottom: 2rem; border-bottom: 1px solid var(--border);
  font-size: 0.85rem; flex-wrap: wrap;
}}
.top-nav a {{
  color: var(--muted); text-decoration: none; transition: color 0.2s;
  display: inline-flex; align-items: center; gap: 0.3rem;
}}
.top-nav a:hover {{ color: var(--accent); }}
.top-nav .sep {{ color: var(--border); }}
h1 {{
  font-size: 2rem; font-weight: 700; margin-bottom: 1.5rem;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  line-height: 1.3;
}}
h2 {{ font-size: 1.4rem; font-weight: 600; margin: 2rem 0 0.75rem; color: var(--fg); }}
h3 {{ font-size: 1.15rem; font-weight: 600; margin: 1.5rem 0 0.5rem; color: var(--accent3); }}
p {{ margin-bottom: 1rem; color: var(--fg); }}
a {{ color: var(--accent2); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
strong {{ color: #fff; }}
em {{ color: var(--muted); }}
ul, ol {{ margin: 0 0 1rem 1.5rem; }}
li {{ margin-bottom: 0.3rem; }}
code {{
  background: rgba(124,58,237,0.1); padding: 0.15rem 0.4rem;
  border-radius: 4px; font-size: 0.85rem; color: var(--accent3);
}}
pre {{
  background: var(--surface2); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 1rem; overflow-x: auto;
  margin-bottom: 1rem;
}}
pre code {{ background: none; padding: 0; }}
blockquote {{
  border-left: 3px solid var(--accent); padding-left: 1rem;
  margin: 1rem 0; color: var(--muted); font-style: italic;
}}
table {{
  width: 100%; border-collapse: collapse; margin-bottom: 1rem;
  font-size: 0.9rem; display: block; overflow-x: auto;
  -webkit-overflow-scrolling: touch; max-width: 100%;
}}
th, td {{
  padding: 0.5rem 0.75rem; text-align: left;
  border-bottom: 1px solid var(--border);
}}
th {{ background: var(--surface2); color: var(--muted); font-weight: 600; }}
tr:hover td {{ background: rgba(124,58,237,0.05); }}
hr {{ border: none; border-top: 1px solid var(--border); margin: 2rem 0; }}
img {{ max-width: 100%; border-radius: var(--radius); }}
.foot-nav {{
  margin-top: 3rem; padding-top: 1.5rem;
  border-top: 1px solid var(--border);
  display: flex; justify-content: space-between; flex-wrap: wrap; gap: 1rem;
}}
.foot-nav a {{
  color: var(--accent); font-size: 0.9rem; text-decoration: none;
}}
.foot-nav a:hover {{ color: var(--accent2); }}
@media (max-width: 600px) {{
  .wrapper {{ padding: 1.5rem 1rem; }}
  h1 {{ font-size: 1.5rem; }}
  pre {{ font-size: 0.8rem; }}
}}
a:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
@media print {{
  body {{ background: #fff; color: #000; }}
  body::before {{ display: none; }}
  .top-nav, .foot-nav {{ display: none; }}
  h1 {{ -webkit-text-fill-color: initial; background: none; color: #000; }}
}}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{ animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }}
}}
</style>
</head>
<body>
<div class="wrapper">
<div class="top-nav">
  <a href="../../portal.html">&#9670; Portal</a>
  <span class="sep">/</span>
  <a href="{section_index}">{section_name}</a>
  <span class="sep">/</span>
  <span style="color:var(--fg)">{title_short}</span>
</div>
{content}
<div class="foot-nav">
  <a href="../../portal.html">&#9670; Back to Portal</a>
  <a href="https://github.com/Puronbo/termite-biotech-and-unbounded/blob/main/unbounded/{md_rel_path}" target="_blank">&#9998; Edit on GitHub</a>
  <a href="#">&#8593; Top</a>
</div>
</div>
<script>
(function(){{var p=location.pathname;var h=p.substring(p.lastIndexOf('/')+1);var r;try{{r=JSON.parse(localStorage.getItem('unbounded-history')||'[]')}}catch(e){{r=[]}};if(!r.includes(h)){{r.unshift(h);if(r.length>20)r.length=20;try{{localStorage.setItem('unbounded-history',JSON.stringify(r))}}catch(e){{}}}}}})();
(function(){{var u='https://aurxoemycvcywtdwahuc.supabase.co';var k='sb_publishable__bSnqp9ioikLs515Uxtudg_8HtvJPuE';var hd={{apikey:k,'Authorization':'Bearer '+k,'Content-Type':'application/json'}};var s;try{{s=localStorage.getItem('unbounded-session')}}catch(e){{s=''}};if(!s){{s='s_'+Date.now()+'_'+Math.random().toString(36).substr(2,9);try{{localStorage.setItem('unbounded-session',s)}}catch(e){{}}}};var pn=location.pathname.split('/').pop()||'index';fetch(u+'/rest/v1/page_views',{{method:'POST',headers:Object.assign({{Prefer:'return=minimal'}},hd),body:JSON.stringify({{page:pn,session_id:s}})}}).catch(function(){{}});fetch(u+'/rest/v1/sessions?on_conflict=id',{{method:'POST',headers:Object.assign({{Prefer:'resolution=merge-duplicates'}},hd),body:JSON.stringify({{id:s,last_active:new Date().toISOString()}})}}).catch(function(){{}});var lb;try{{lb=localStorage.getItem('unbounded-heartbeat')}}catch(e){{lb=''}};if(!lb||Date.now()-parseInt(lb)>86400000){{fetch(u+'/rest/v1/heartbeats',{{method:'POST',headers:Object.assign({{Prefer:'return=minimal'}},hd),body:'{{}}'}}).catch(function(){{}});try{{localStorage.setItem('unbounded-heartbeat',''+Date.now())}}catch(e){{}}}}}})();
</script>
</body>
</html>'''

def convert_file(md_path, output_rel):
    """Convert a markdown file to HTML."""
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Extract first h1 as title
    title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else os.path.splitext(os.path.basename(md_path))[0]
    title_short = title if len(title) < 50 else title[:47] + '...'
    meta_desc = title_short

    # Determine section
    rel_path = os.path.normpath(output_rel).replace('\\', '/')
    path_parts = rel_path.split('/')
    if len(path_parts) > 1:
        section = path_parts[0]
    else:
        section = ''

    section_names = {
        'docs': 'Documentation',
        'calls': 'Calls to Action',
        'termite': 'Termite Research',
        'unbounded': 'UNBOUNDED',
        '': '',
    }
    section_name = section_names.get(section, section.capitalize())
    section_index = f'{section}/index.html' if section else '../portal.html'
    if section:
        section_index_path = os.path.join(os.path.dirname(rel_path), 'index.html')
        # Compute relative path for section index
        depth = rel_path.count('/')
        if depth > 1:
            section_index = '../' * (depth - 1) + section + '/index.html'

    # Convert markdown
    html_body = markdown.markdown(
        md_content,
        extensions=['fenced_code', 'tables', 'codehilite', 'nl2br', 'sane_lists']
    )

    # Fix relative image/links in markdown
    md_dir = os.path.dirname(md_path)
    html_body = re.sub(
        r'<a href="(?!https?://|#|/)([^"]+)">',
        lambda m: f'<a href="{m.group(1)}">',
        html_body
    )

    # Compute relative path from repo root for Edit on GitHub link
    try:
        md_rel_path = os.path.relpath(md_path, REPO_ROOT)
    except ValueError:
        md_rel_path = rel_path.replace('.html', '.md')
    md_rel_path = md_rel_path.replace('\\', '/')

    # Render template
    page = TEMPLATE.format(
        title=title, title_short=title_short, meta_desc=meta_desc,
        content=html_body, section_name=section_name,
        section_index=section_index, rel_path=rel_path.replace('\\', '/'),
        md_rel_path=md_rel_path
    )
    return page


def generate_index(files, section_name, output_path):
    """Generate an index page for a section."""
    links = []
    for f in files:
        name = os.path.splitext(os.path.basename(f))[0]
        label = name.replace('-', ' ').replace('_', ' ').title()
        links.append((f, label))

    rows = '\n'.join(
        f'<tr><td><a href="{f}">{label}</a></td></tr>'
        for f, label in links
    )

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{section_name} &mdash; UNBOUNDED</title>
<meta name="description" content="{section_name} — documents and resources from the UNBOUNDED project.">
<meta property="og:title" content="{section_name} &mdash; UNBOUNDED">
<meta property="og:description" content="{section_name} — documents and resources from the UNBOUNDED project.">
<meta property="og:type" content="website">
<meta property="og:image" content="https://raw.githubusercontent.com/Puronbo/termite-biotech-and-unbounded/main/unbounded/site/favicon.svg">
<meta name="theme-color" content="#0e0e16">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{ --bg: #08080c; --surface: #0e0e16; --surface2: #14142e; --border: rgba(255,255,255,0.05); --accent: #7c3aed; --accent2: #ff6b35; --fg: #e0e0ec; --muted: #7878a0; --radius: 12px; }}
body {{ font-family: 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--fg); min-height: 100vh; }}
body::before {{ content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(ellipse at 50% 0%, rgba(124,58,237,0.06) 0%, transparent 70%); pointer-events: none; z-index: 0; }}
.wrapper {{ max-width: 700px; margin: 0 auto; padding: 3rem 1.5rem; position: relative; z-index: 1; }}
h1 {{ font-size: 1.8rem; font-weight: 700; margin-bottom: 0.5rem; background: linear-gradient(135deg, var(--accent), var(--accent2)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
.sub {{ color: var(--muted); margin-bottom: 2rem; font-size: 0.95rem; }}
.back {{ display: inline-block; margin-bottom: 1.5rem; color: var(--accent); text-decoration: none; font-size: 0.85rem; }}
.back:hover {{ color: var(--accent2); }}
table {{ width: 100%; border-collapse: collapse; }}
td {{ padding: 0.75rem 0; border-bottom: 1px solid var(--border); }}
td a {{ color: var(--fg); text-decoration: none; font-size: 0.95rem; display: block; transition: color 0.15s; }}
td a:hover {{ color: var(--accent); }}
td .desc {{ color: var(--muted); font-size: 0.8rem; margin-top: 0.15rem; }}
</style>
</head>
<body>
<div class="wrapper">
<a class="back" href="../../portal.html">&#9664; Back to Portal</a>
<h1>{section_name}</h1>
<p class="sub">Browse documents in this section.</p>
<table>{rows}</table>
</div>
</body>
</html>'''
    return html


def main():
    # Define all markdown files to convert
    conversions = [
        # (source_md, output_relative_path)
    ]

    # unbounded/docs/
    docs_dir = os.path.join(REPO_ROOT, 'unbounded', 'docs')
    conversions += [
        (os.path.join(docs_dir, 'MANIFESTO.md'), 'docs/manifesto.html'),
        (os.path.join(docs_dir, 'PLATFORM-BLUEPRINT.md'), 'docs/platform-blueprint.html'),
        (os.path.join(docs_dir, 'ROADMAP.md'), 'docs/roadmap.html'),
    ]

    # unbounded/calls/
    calls_dir = os.path.join(REPO_ROOT, 'unbounded', 'calls')
    conversions += [
        (os.path.join(calls_dir, 'OPEN-LETTER.md'), 'calls/open-letter.html'),
        (os.path.join(calls_dir, 'FOR-DEVELOPERS.md'), 'calls/for-developers.html'),
        (os.path.join(calls_dir, 'FOR-CREATIVES.md'), 'calls/for-creatives.html'),
    ]

    # unbounded/ root
    ub_root = os.path.join(REPO_ROOT, 'unbounded')
    conversions += [
        (os.path.join(ub_root, 'WELCOME.md'), 'unbounded/welcome.html'),
        (os.path.join(ub_root, 'GOVERNANCE.md'), 'unbounded/governance.html'),
        (os.path.join(ub_root, 'CONTRIBUTING.md'), 'unbounded/contributing.html'),
    ]

    # termite-projects/ root
    tp_root = os.path.join(REPO_ROOT, 'termite-projects')
    conversions += [
        (os.path.join(tp_root, 'MASTER-PROJECT-SUMMARY.md'), 'termite/master-summary.html'),
        (os.path.join(tp_root, 'CROSS-VERIFICATION.md'), 'termite/cross-verification.html'),
        (os.path.join(tp_root, 'README.md'), 'termite/readme.html'),
    ]

    # Create output directories
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for _, rel in conversions:
        dirname = os.path.join(OUTPUT_DIR, os.path.dirname(rel))
        os.makedirs(dirname, exist_ok=True)

    # Convert each file
    print(f"Converting {len(conversions)} files...")
    for md_path, rel_path in conversions:
        if not os.path.exists(md_path):
            print(f"  SKIP (not found): {md_path}")
            continue
        try:
            page = convert_file(md_path, rel_path)
            out_path = os.path.join(OUTPUT_DIR, rel_path)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(page)
            size = len(page)
            print(f"  OK: {rel_path} ({size} bytes)")
        except Exception as e:
            print(f"  ERROR: {rel_path}: {e}")

    # Generate index pages
    index_configs = [
        ('docs', 'Documentation', ['manifesto.html', 'platform-blueprint.html', 'roadmap.html']),
        ('calls', 'Calls to Action', ['open-letter.html', 'for-developers.html', 'for-creatives.html']),
        ('unbounded', 'UNBOUNDED Project', ['welcome.html', 'governance.html', 'contributing.html']),
        ('termite', 'Termite Research', ['master-summary.html', 'cross-verification.html', 'readme.html']),
    ]
    for section, name, files in index_configs:
        html = generate_index(files, name, section)
        out_path = os.path.join(OUTPUT_DIR, section, 'index.html')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  INDEX: {section}/index.html")

    # Generate root pages index
    all_sections = []
    for section, name, files in index_configs:
        all_sections.append(f'<tr><td><a href="{section}/index.html">{name}</a></td><td style="color:var(--muted);font-size:0.85rem">{len(files)} documents</td></tr>')
    rows = '\n'.join(all_sections)
    root_index = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Documentation &mdash; UNBOUNDED + Termite Research</title>
<meta name="description" content="All project documents across UNBOUNDED, Termite Research, and Calls sections.">
<meta property="og:title" content="Documentation &mdash; UNBOUNDED + Termite Research">
<meta property="og:description" content="All project documents across UNBOUNDED, Termite Research, and Calls sections.">
<meta property="og:type" content="website">
<meta property="og:image" content="https://raw.githubusercontent.com/Puronbo/termite-biotech-and-unbounded/main/unbounded/site/favicon.svg">
<meta name="theme-color" content="#0e0e16">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
:root {{ --bg: #08080c; --surface: #0e0e16; --border: rgba(255,255,255,0.05); --accent: #7c3aed; --accent2: #ff6b35; --fg: #e0e0ec; --muted: #7878a0; --radius: 12px; }}
body {{ font-family: 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--fg); min-height: 100vh; }}
body::before {{ content: ''; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(ellipse at 50% 0%, rgba(124,58,237,0.06) 0%, transparent 70%); pointer-events: none; z-index: 0; }}
.wrapper {{ max-width: 700px; margin: 0 auto; padding: 3rem 1.5rem; position: relative; z-index: 1; }}
h1 {{ font-size: 1.8rem; font-weight: 700; margin-bottom: 0.5rem; background: linear-gradient(135deg, var(--accent), var(--accent2)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
.sub {{ color: var(--muted); margin-bottom: 2rem; font-size: 0.95rem; }}
.back {{ display: inline-block; margin-bottom: 1.5rem; color: var(--accent); text-decoration: none; font-size: 0.85rem; }}
.back:hover {{ color: var(--accent2); }}
table {{ width: 100%; border-collapse: collapse; }}
td {{ padding: 0.75rem 0; border-bottom: 1px solid var(--border); }}
td a {{ color: var(--accent); text-decoration: none; font-size: 1rem; display: block; }}
td a:hover {{ color: var(--accent2); }}
</style>
</head>
<body>
<div class="wrapper">
<a class="back" href="../portal.html">&#9664; Back to Portal</a>
<h1>Documentation</h1>
<p class="sub">All project documents, organized by section.</p>
<table>{rows}</table>
</div>
</body>
</html>'''
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(root_index)
    print(f"  INDEX: index.html (root pages index)")

    print(f"\nAll done. Files written to: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
