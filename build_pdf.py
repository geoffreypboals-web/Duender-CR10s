"""Combined PDF of the Lego (MGN9 X) manual for each printer (T-015, owner 2026-10-14).

One PDF per edition: cover, contents with page numbers, README-mgn9x, then every chapter in the order of the
README-mgn9x contents table (the clean -mgn9x chapters; build history and owner notes live in
manual/REVIEW-NOTES-mgn9x.md, which is not printed). Links between included chapters become links inside the PDF; links to files that are not in the PDF
point at the file on GitHub (default branch); pictures are embedded.

Needs WeasyPrint, Markdown and BeautifulSoup (BSD-licensed):
  python3 -m venv /tmp/pdfenv && /tmp/pdfenv/bin/pip install weasyprint markdown beautifulsoup4
Run from the repo root:
  /tmp/pdfenv/bin/python manual/build_pdf.py            # all editions
  /tmp/pdfenv/bin/python manual/build_pdf.py c300-v3    # one
Writes manual/pdf/<edition>-mgn9x.pdf.
"""
import os, re, sys, datetime, unicodedata
from pathlib import Path
from urllib.parse import unquote
import markdown
from bs4 import BeautifulSoup
from weasyprint import HTML

REPO = Path(__file__).resolve().parent.parent
MANUAL = REPO / "manual"
OUT = MANUAL / "pdf"
GITHUB = "https://github.com/geoffreypboals-web/Toolchanger-Research/blob/claude/toolhead-changer-designs-u2qeuq/"
# T-021: the seven frame manuals (make_frame_editions.py); the three full build manuals stay until the toolhead and
# electronics manuals take over their chapters 8-12
FRAMES = ["frame-c300-cut", "frame-c300-cr10", "frame-c300-cr10v2", "frame-c400-cut", "frame-c400-cr10s4",
          "frame-c500-cut", "frame-c500-cr10s5"]
EDITIONS = ["c300-v3", "c400-s4", "c500-s5", "upgrades"] + FRAMES + ["toolhead", "electronics"]


def gh_slug(text):
    """GitHub's heading anchor: lower case, punctuation (and emoji) dropped, spaces to hyphens."""
    text = text.strip().lower()
    text = "".join(c for c in text if c in " -_" or unicodedata.category(c)[0] in "LN")
    return text.replace(" ", "-")


def chapter_files(ed):
    """README-mgn9x first, then the files linked from its '## Chapters' table."""
    readme = MANUAL / "editions" / ed / "README-mgn9x.md"
    text = readme.read_text()
    table = text.split("## Chapters", 1)[1].split("\n## ", 1)[0]
    files = [readme]
    for line in table.splitlines():
        m = re.match(r"\|\s*[0-9A-Z]+\s*\|\s*\[[^\]]*\]\(([^)#]+\.md)\)", line)
        if m:
            files.append((readme.parent / m.group(1)).resolve())
    return files


def key_for(path):
    return "ch-" + re.sub(r"[^a-z0-9]+", "-", path.stem.lower())


# Only real emoji get the emoji font: with it in the body font list, digits come out as emoji glyphs.
EMOJI = re.compile("([\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\u2300-\u23FF]\uFE0F?)")


def emoji_spans(html):
    soup = BeautifulSoup(html, "html.parser")
    for node in list(soup.find_all(string=EMOJI)):
        if node.parent.name in ("style", "script", "title"):
            continue
        new = BeautifulSoup(EMOJI.sub(r'<span class="emoji">\1</span>', str(node).replace("&", "&amp;").replace("<", "&lt;")), "html.parser")
        node.replace_with(new)
    return str(soup)


LIST_START = re.compile(r"^(?P<prev>(?![ \t]*(?:\d+\.|[-*+])[ \t])[^\n|>][^\n]*)\n(?=(?:\d+\.|[-*+])[ \t])", re.M)


MARK_START = re.compile(r"^(?P<prev>[^\n|>][^\n]*)\n(?=(?:✅|⚠️))", re.M)     # a ✅ / ⚠️ line starts its own paragraph


def list_breaks(text):
    """GitHub starts a list right after a paragraph line ("**Do:**" then "1. …"); Python-Markdown needs a blank line
    first, or the steps run together into one paragraph. Add it outside code fences."""
    parts = re.split(r"(^```.*?^```[ \t]*$)", text, flags=re.M | re.S)
    return "".join(p if p.startswith("```") else MARK_START.sub(r"\g<prev>\n\n", LIST_START.sub(r"\g<prev>\n\n", p))
                   for p in parts)


def render(path, included):
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "md_in_html", "sane_lists"],
                           extension_configs={"toc": {"slugify": lambda t, sep: gh_slug(t)}})
    soup = BeautifulSoup(md.convert(list_breaks(path.read_text())), "html.parser")
    key = key_for(path)
    for tag in soup.find_all(id=True):
        tag["id"] = f"{key}--{tag['id']}"
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if re.match(r"^[a-z]+:", href):
            continue
        target, _, frag = href.partition("#")
        dest = (path.parent / unquote(target)).resolve() if target else path
        if dest in included:
            a["href"] = f"#{key_for(dest)}--{frag}" if frag else f"#{key_for(dest)}"
        elif dest.exists() and REPO in dest.parents:
            a["href"] = GITHUB + str(dest.relative_to(REPO)) + (f"#{frag}" if frag else "")
    for img in soup.find_all("img", src=True):
        src = img["src"]
        if not re.match(r"^[a-z]+:", src):
            img["src"] = (path.parent / unquote(src)).resolve().as_uri()
    h1 = soup.find("h1")
    title = h1.get_text() if h1 else path.stem
    return key, title, emoji_spans(str(soup))


CSS = """
@page { size: A4; margin: 16mm 14mm 18mm 14mm;
        @bottom-center { content: counter(page); font: 9pt 'DejaVu Sans'; color: #666; }
        @bottom-left { content: string(edition); font: 8pt 'DejaVu Sans'; color: #999; } }
@page cover { @bottom-center { content: none; } @bottom-left { content: none; } }
body { font: 10pt/1.42 'DejaVu Sans', sans-serif; color: #1b1b1b; }
.emoji { font-family: 'Noto Color Emoji'; font-weight: normal; }
.cover { page: cover; text-align: center; padding-top: 18mm; }
.cover h1 { font-size: 24pt; margin: 0 0 4mm; string-set: edition content(); }
.cover .sub { font-size: 12pt; color: #444; }
.cover img { width: 100%; margin: 8mm 0; }
.cover .meta { font-size: 9pt; color: #666; }
.toc { page-break-before: always; }
.toc h1 { font-size: 18pt; }
.toc ol { list-style: none; padding: 0; }
.toc li { margin: 2.2mm 0; font-size: 11pt; }
.toc a { color: #1b1b1b; text-decoration: none; }
.toc a::after { content: leader('.') target-counter(attr(href), page); }
section.chapter { page-break-before: always; }
h1 { font-size: 18pt; border-bottom: 2px solid #f08a24; padding-bottom: 2mm; }
h2 { font-size: 13.5pt; margin-top: 7mm; page-break-after: avoid; }
h3 { font-size: 11.5pt; page-break-after: avoid; }
img { max-width: 100%; max-height: 225mm; display: block; margin: 3mm auto; page-break-inside: avoid; }
td img, th img { max-width: 48%; display: inline-block; margin: 1mm; }
table { border-collapse: collapse; width: 100%; font-size: 8.8pt; margin: 3mm 0; }
th, td { border: 0.5pt solid #bbb; padding: 1.4mm 2mm; vertical-align: top; }
th { background: #fff7e6; }
tr { page-break-inside: avoid; }
blockquote { margin: 3mm 0; padding: 2mm 4mm; background: #f6f7f9; border-left: 3px solid #f08a24; }
code { font: inherit; }   /* part and file names in the paragraph's own font (owner, 2026-10-14) */
pre { background: #f2f2f2; padding: 3mm; white-space: pre-wrap; }
pre code { font: 8pt 'DejaVu Sans Mono', monospace; }
a { color: #b4410f; }
"""


HISTORY = re.compile(r"T-0\d\d|20\d\d-\d\d-\d\d|[Oo]wner|[Dd]raft|original chapter|[Oo]riginal (?:text|value|manual|README)|"
                     r"🔧|❓|Lego version|CHANGED|used to say|[Cc]orrected|[Pp]roposed|the human")


CREDIT = "Real parts from Andizzle's CR10 Duender (GPL-2.0) and Sergei's Duender / MedusaHC STEP files (GPL-2.0 / GPL-3.0); schematic lengths are estimates."
CREDIT_TH = "Real parts from Sergei's MedusaHC V0.2 STEP files (GPL-3.0), real size."
CREDIT_EL = "Board facts from BIGTREETECH's manuals and configs, Klipper's board configs and Sergei's MedusaHC V0.2 (GPL-3.0)."


def build(ed):
    files = chapter_files(ed)
    missing = [f for f in files if not f.exists()]
    assert not missing, missing
    included = set(files)
    parts = [render(f, included) for f in files]
    name = parts[0][1].split()[0].rstrip(":")   # "C400-S4 build manual (...)" -> "C400-S4"
    cover_img = MANUAL / "images" / f"c{ed[1:4]}" / "lego-mgn9x" / "step-all-v2.png"
    title, sub = f"{name} build manual", "Lego edition · X gantry on MGN9 · Duender triple Z"
    if ed.startswith("frame-"):                  # its own title; the cover picture carries the model's tag
        title = parts[0][1]; sub = "Frame and motion · MGN9 XY (MedusaHC V-Back) · Andizzle triple Z"
        m = re.search(r"c(\d{3})-duender-3z-mgn9x(-[a-z0-9]+)?\.step", files[0].read_text())
        cover_img = MANUAL / "images" / f"c{m.group(1)}" / "lego-mgn9x" / f"step-all{m.group(2) or ''}-v2.png"
    if ed == "toolhead":                         # shared by all seven frames
        title = parts[0][1]; sub = "Tools, docks, toolhead and feeder · all seven frames"
        cover_img = MANUAL / "images" / "toolhead" / "t6-complete.png"
    if ed == "upgrades":
        title = parts[0][1]; sub = "Stiffer frame and Z rails · all seven frames"
        cover_img = MANUAL / "images" / "c300" / "lego-mgn9x" / "before-after-purple.png"
    if ed == "electronics":
        title = parts[0][1]; sub = "Boards, power, wiring, Klipper and MedusaHC · all seven frames"
        cover_img = MANUAL / "images" / "toolhead" / "t6-complete.png"
    toc = emoji_spans("".join(f'<li><a href="#{k}">{t}</a></li>' for k, t, _ in parts))
    body = "".join(f'<section class="chapter" id="{k}">{h}</section>' for k, _, h in parts)
    html = f"""<!doctype html><html><head><meta charset="utf-8"><title>{title}</title>
<style>{CSS}</style></head><body>
<div class="cover"><h1>{title}</h1>
<div class="sub">{sub}</div>
<img src="{cover_img.as_uri()}">
<div class="meta">{datetime.date.today():%B %Y}<br>
{dict(toolhead=CREDIT_TH, electronics=CREDIT_EL).get(ed, CREDIT)}</div></div>
<div class="toc"><h1>Contents</h1><ol>{toc}</ol></div>
{body}</body></html>"""
    # build history must not reach the printed manual (owner, 2026-10-14)
    text = re.sub(r"<[^>]+>", " ", body)
    leaks = sorted({m.group(0) for m in HISTORY.finditer(text)})
    print(f"{ed}: history words in the text: {leaks if leaks else 'none'}")
    ids = set(re.findall(r'id="([^"]+)"', html))
    dead = sorted({h for h in re.findall(r'href="#([^"]+)"', html) if h not in ids})
    n_int = len(re.findall(r'href="#', html))
    print(f"{ed}: {n_int} internal links, {len(dead)} without a target", dead[:10])
    OUT.mkdir(exist_ok=True)
    out = OUT / f"{ed}-mgn9x.pdf"
    HTML(string=html, base_url=str(MANUAL)).write_pdf(out)
    print(f"{out}  {out.stat().st_size / 1e6:.1f} MB  ({len(files)} files)")
    return out


if __name__ == "__main__":
    for ed in sys.argv[1:] or EDITIONS:
        build(ed)
