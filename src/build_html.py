"""Build a PROPER BOOK READER (single page at a time) from markdown. No deps.
Run: python src/build_html.py [in.md [out.html]]"""
import os, re, html, sys
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_MD = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "book_en.md")
OUT_HTML = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, "docs", "index.html")

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
    out, in_ul = [], False
    for ln in lines:
        s = ln.rstrip()
        if s.startswith("### "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<h3>{inline(s[4:].strip())}</h3>")
        elif s.startswith("## "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"@@PAGE@@<h2>{inline(s[3:].strip())}</h2>")
        elif s.startswith("# "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"@@PAGE@@<h1>{inline(s[2:].strip())}</h1>")
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
        else:
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<p>{inline(s)}</p>")
    return "\n".join(out)

def main():
    with open(IN_MD, encoding="utf-8") as f:
        md = f.read()
    body = md_to_html(md)
    pages = [p for p in body.split("@@PAGE@@") if p.strip()]
    cover = ("<div class='rule'>★ The Complete Edition · September 2026 ★</div>"
             "<h1>From Telangana Inter<br>to <em>Aerospace in Germany</em></h1>"
             "<p style='font-style:italic'>A book for one student: Telangana Board, MPC, Class 12 — "
             "without JEE. Every college · every fee · every form, verified point by point.</p>"
             "<button class='go' onclick='go(1)'>Open the Book</button>"
             "<p style='font-size:13px;opacity:.75'>2000 pages · English · remembers your page · ← → keys turn pages</p>")
    slides = f"<section class='sheet' data-i='0'>{cover}</section>\n" + "\n".join(f"<section class='sheet' data-i='{i+1}'>{p}</section>" for i, p in enumerate(pages))
    n = len(pages)
    doc = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Telangana to Germany Aerospace Book</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Georgia,'Times New Roman',serif;background:#2e2620;color:#2b2118;min-height:100vh;display:flex;flex-direction:column}
/* top bar */
.topbar{background:#1d150b;color:#e8dcc0;display:flex;align-items:center;gap:10px;padding:10px 18px;font-family:Arial,sans-serif;position:sticky;top:0;z-index:20;border-bottom:2px solid #b8860b}
.topbar b{font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.topbar .sp{flex:1}
.topbar button{background:transparent;color:#e8c15a;border:1px solid #b8860b;border-radius:6px;padding:6px 12px;font-size:13px;cursor:pointer}
.topbar button:hover{background:#b8860b;color:#1d150b}
#count{font-size:13px;color:#b7a37e;white-space:nowrap}
/* stage */
.stage{flex:1;display:flex;justify-content:center;padding:26px 14px 90px}
.sheet{display:none;background:#faf6ee;width:100%;max-width:720px;min-height:70vh;padding:52px 56px;border-radius:3px;box-shadow:0 0 0 1px #d8cba6,0 18px 60px #000;line-height:1.8;font-size:17px}
.sheet.on{display:block}
.sheet h1{font-size:1.9em;margin-bottom:12px;color:#1d150b}
.sheet h2{font-size:1.35em;margin-bottom:10px;color:#1d150b}
.sheet h3{font-size:1.1em;margin:12px 0 6px}
.sheet p{margin:10px 0}
.sheet ul{margin:10px 0 10px 4px;list-style:none}
.sheet li{padding:6px 0 6px 26px;position:relative;border-bottom:1px dotted #ddd0b2}
.sheet li::before{content:"\\2726";position:absolute;left:2px;color:#b8860b}
.sheet blockquote{border-left:4px solid #b8860b;background:#f6efdb;padding:10px 14px;margin:12px 0;font-style:italic}
.sheet a{color:#7c5a10}
.sheet.cover{background:radial-gradient(700px 400px at 50% 110%,#5a3d12 0%,#241a0e 65%),#1d150b;color:#f5e9cf;text-align:center;display:none;flex-direction:column;justify-content:center;align-items:center;min-height:70vh}
.sheet.cover.on{display:flex}
.sheet.cover h1{color:#f5e9cf;font-size:2em}
.sheet.cover em{color:#e8c15a}
.sheet.cover .rule{color:#e8c15a;letter-spacing:5px;font-size:12px;text-transform:uppercase;font-family:Arial}
.sheet.cover .go{background:#b8860b;color:#1d150b;border:0;padding:14px 44px;font-size:17px;border-radius:4px;cursor:pointer;font-family:Arial;font-weight:700;margin-top:22px}
/* bottom nav */
.pagenav{position:fixed;bottom:0;left:0;right:0;background:#1d150bf2;border-top:2px solid #b8860b;display:flex;align-items:center;justify-content:center;gap:14px;padding:12px;font-family:Arial}
.pagenav button{background:#b8860b;color:#1d150b;border:0;padding:10px 26px;font-size:15px;border-radius:6px;cursor:pointer;font-weight:700}
.pagenav button:disabled{opacity:.35;cursor:default}
.pagenav input{width:90px;padding:9px;text-align:center;border-radius:6px;border:1px solid #b8860b;background:#fff;font-size:15px}
/* TOC drawer */
#drawer{position:fixed;top:0;left:-320px;width:300px;height:100vh;background:#faf6ee;z-index:30;transition:left .25s;overflow:auto;padding:18px 14px;border-right:2px solid #b8860b;font-size:14px;font-family:Arial}
#drawer.open{left:0}
#drawer a{display:block;padding:6px 8px;color:#2b2118;text-decoration:none;border-bottom:1px dotted #ddd0b2;font-size:13px}
#drawer a:hover{background:#f6efdb}
#shade{position:fixed;inset:0;background:#0008;display:none;z-index:25}
#shade.open{display:block}
@media(max-width:640px){.sheet{padding:30px 22px;font-size:16px}.topbar b{display:none}}
@media print{.topbar,.pagenav,#drawer,#shade{display:none!important}.sheet{display:block!important;box-shadow:none;max-width:100%}}
</style></head><body>
<div class="topbar"><button onclick="drawer(true)">&#9776; Contents</button><b>Telangana &#8594; Germany Aerospace</b><span class="sp"></span><span id="count"></span><button onclick="bigger(1)">A+</button><button onclick="bigger(-1)">A-</button></div>
<div id="shade" onclick="drawer(false)"></div>
<nav id="drawer"><b>Contents</b><div id="toc"></div></nav>
<div class="stage" id="stage">
__SHEETS__
</div>
<div class="pagenav"><button id="prev" onclick="go(cur-1)">&#8592; Prev</button><input id="jump" inputmode="numeric" onkeydown="if(event.key==='Enter')go(parseInt(this.value,10)-1)"><button id="next" onclick="go(cur+1)">Next &#8594;</button></div>
<script>
var sheets=[...document.querySelectorAll('.sheet')],cur=0,N=sheets.length;
sheets[0].classList.add('cover');
var toc=document.getElementById('toc');
sheets.forEach((s,i)=>{var h=s.querySelector('h1,h2');var t=h?h.textContent.slice(0,70):('Page '+(i+1));var a=document.createElement('a');a.href='#';a.textContent=(i+1)+'. '+t;a.onclick=e=>{e.preventDefault();go(i);drawer(false)};toc.appendChild(a)});
function go(i){if(i<0)i=0;if(i>=N)i=N-1;sheets[cur].classList.remove('on');cur=i;sheets[cur].classList.add('on');
document.getElementById('count').textContent='Page '+(cur+1)+' of '+N;
document.getElementById('prev').disabled=cur===0;document.getElementById('next').disabled=cur===N-1;
document.getElementById('jump').value=cur+1;scrollTo(0,0);try{localStorage.setItem('aero-book-page',cur)}catch(e){}}
function drawer(o){document.getElementById('drawer').classList.toggle('open',o);document.getElementById('shade').classList.toggle('open',o)}
function bigger(d){var st=document.getElementById('stage');var s=parseFloat(getComputedStyle(sheets[cur]).fontSize)+d*2;document.querySelectorAll('.sheet').forEach(x=>x.style.fontSize=s+'px')}
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();go(cur+1)}if(e.key==='ArrowLeft')go(cur-1)});
(function(){var s=0;try{s=parseInt(localStorage.getItem('aero-book-page')||'0',10)||0}catch(e){}go(Math.min(s,N-1))})();
</script>
</body></html>"""
    doc = doc.replace("__SHEETS__", slides)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"WROTE {OUT_HTML} pages={n} bytes={len(doc.encode('utf-8'))}")

if __name__ == "__main__":
    main()
