"""Build docs/index.html from book.md. No deps. Run: python src/build_html.py"""
import os, re, html
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_MD = os.path.join(BASE, "book.md")
OUT_HTML = os.path.join(BASE, "docs", "index.html")

def esc(s):
    return html.escape(s, quote=False)

def inline(s):
    s = esc(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'\[([^\]]+)\]\((https?[^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s

def md_to_html(md):
    lines = md.split("\n")
    out, in_ul, lid = [], False, 0
    toc = []
    for ln in lines:
        s = ln.rstrip()
        if s.startswith("### "):
            if in_ul: out.append("</ul>"); in_ul = False
            lid += 1; t = s[4:].strip()
            toc.append((3, lid, t)); out.append(f"<h3 id='p{lid}'>{inline(t)}</h3>")
        elif s.startswith("## "):
            if in_ul: out.append("</ul>"); in_ul = False
            lid += 1; t = s[3:].strip()
            toc.append((2, lid, t)); out.append(f"<h2 id='p{lid}' class='page'>{inline(t)}</h2>")
        elif s.startswith("# "):
            if in_ul: out.append("</ul>"); in_ul = False
            lid += 1; t = s[2:].strip()
            toc.append((1, lid, t)); out.append(f"<h1 id='p{lid}'>{inline(t)}</h1>")
        elif s.startswith("- "):
            if not in_ul: out.append("<ul>"); in_ul = True
            out.append(f"<li>{inline(s[2:])}</li>")
        elif s.strip() == "---":
            if in_ul: out.append("</ul>"); in_ul = False
            out.append("<hr>")
        elif s.strip().startswith("> "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<blockquote>{inline(s.strip()[2:])}</blockquote>")
        elif s.strip() == "":
            if in_ul: out.append("</ul>"); in_ul = False
            out.append("")
        elif s.strip().startswith("<div"):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(s)
        else:
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<p>{inline(s)}</p>")
    return "\n".join(out), toc

def main():
    with open(IN_MD, encoding="utf-8") as f:
        md = f.read()
    body, toc = md_to_html(md)
    toc_html = "\n".join(
        f"<a class='toc-l{t[0]}' href='#p{t[1]}'>{esc(t[2][:90])}</a>" for t in toc[:2200]
    )
    html_doc = f"""<!DOCTYPE html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Deutschland Aerospace für Telangana — 2000-Seiten-Buch</title>
<style>
:root {{ --bg:#0f172a; --fg:#e2e8f0; --acc:#38bdf8; }}
* {{ box-sizing:border-box; }} body {{ margin:0; font-family:Georgia,serif; color:#1e293b; background:#f8fafc; }}
header {{ position:sticky; top:0; background:var(--bg); color:var(--fg); padding:12px 20px; display:flex; gap:12px; align-items:center; z-index:10; }}
header input {{ flex:1; max-width:420px; padding:8px 12px; border-radius:8px; border:0; }}
.layout {{ display:grid; grid-template-columns:300px 1fr; }} nav {{ height:calc(100vh - 53px); overflow:auto; position:sticky; top:53px; background:#fff; border-right:1px solid #e2e8f0; padding:12px; font-size:13px; }}
nav a {{ display:block; padding:3px 6px; color:#334155; text-decoration:none; border-radius:6px; }} nav a:hover {{ background:#e0f2fe; }} .toc-l1 {{ font-weight:bold; }} .toc-l2 {{ padding-left:12px!important; }}
main {{ padding:32px; max-width:900px; }} h1 {{ font-size:2em; }} h2.page {{ border-top:4px solid var(--bg); padding-top:24px; }} blockquote {{ border-left:4px solid var(--acc); background:#f0f9ff; padding:12px 16px; }} code {{ background:#f1f5f9; padding:2px 6px; border-radius:4px; }} a {{ color:#0284c7; }}
.badge {{ background:var(--acc); color:#001; padding:2px 10px; border-radius:20px; font-size:12px; }}
@media print {{ header,nav,.noprint {{ display:none!important; }} .layout {{ display:block; }} main {{ max-width:100%; }} h2.page {{ page-break-before:always; }} @page {{ size:A4; margin:18mm; @bottom-center {{ content:"Seite " counter(page) " / 2000"; }} }} body {{ counter-reset:page; }} }}
</style></head><body>
<header><strong>✈ Deutschland Aerospace · Telangana</strong><span class="badge">2000 Seiten</span>
<input id="q" placeholder="Suchen (z. B. TUM, Blocked, FSP, VFS) …" oninput="f(this.value)"><button class="noprint" onclick="window.print()">Drucken / PDF</button></header>
<div class="layout"><nav id="toc">{toc_html}</nav><main id="content">{body}<hr><p><small>Kompiliert aus CYCLE 1–4. Keine Vorhersage. [UNVERIFIED] vor Zahlung prüfen. Offiziell: aps-india.de · daad.in · stk.kit.edu · anabin.kmk.org · uni-assist.de · india.diplo.de · digital.diplo.de</small></p></main></div>
<script>function f(v){{v=v.toLowerCase();document.querySelectorAll('#content h2,#content p,#content li').forEach(e=>{{e.style.background=e.textContent.toLowerCase().includes(v)&&v?'#fef08a':''}})}};</script>
</body></html>"""
    os.makedirs(os.path.dirname(OUT_HTML), exist_ok=True)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_doc)
    print(f"WROTE {OUT_HTML} bytes={len(html_doc.encode('utf-8'))} toc={len(toc)}")

if __name__ == "__main__":
    main()
