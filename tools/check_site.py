"""Static site checks: internal links, anchors, assets, basic accessibility."""
from lxml import html, etree
import os, glob, re, urllib.parse

ROOT = r"C:\Users\erhan\Documents\ai\biyopet"
pages = sorted(glob.glob(os.path.join(ROOT, "*.html")))
problems = []

ids_by_page = {}
docs = {}
for page in pages:
    name = os.path.basename(page)
    parser = html.HTMLParser(recover=True, encoding="utf-8")
    with open(page, "rb") as f:
        raw = f.read()
    doc = html.fromstring(raw, parser=parser)
    docs[name] = doc
    ids = set(doc.xpath("//*[@id]/@id"))
    all_ids = doc.xpath("//*[@id]/@id")
    dups = {i for i in all_ids if all_ids.count(i) > 1}
    for d in sorted(dups):
        problems.append(f"[HTML] {name}: duplicate id '{d}'")
    ids_by_page[name] = ids
    if parser.error_log:
        for err in parser.error_log:
            # lxml's HTML4 parser treats HTML5/SVG elements as invalid; ignore those
            if err.message.startswith("Tag ") and err.message.endswith(" invalid"):
                continue
            problems.append(f"[HTML] {name}:{err.line}: {err.message}")

    # title / lang / meta description
    if not doc.xpath("//title/text()"):
        problems.append(f"[SEO] {name}: missing <title>")
    if not doc.xpath("//html/@lang"):
        problems.append(f"[SEO] {name}: missing lang attribute")
    if not doc.xpath('//meta[@name="description"]'):
        problems.append(f"[SEO] {name}: missing meta description")

    # images: src exists + alt
    for img in doc.xpath("//img"):
        src = img.get("src") or ""
        if not src:
            problems.append(f"[IMG] {name}: img without src")
            continue
        path = os.path.normpath(os.path.join(ROOT, src))
        if not os.path.exists(path):
            problems.append(f"[IMG] {name}: missing file {src}")
        if img.get("alt") is None:
            problems.append(f"[IMG] {name}: missing alt for {src}")
        for source in doc.xpath(f"//picture[img[@src='{src}']]/source"):
            s = source.get("srcset")
            if s and not os.path.exists(os.path.normpath(os.path.join(ROOT, s))):
                problems.append(f"[IMG] {name}: missing srcset file {s}")

    # links
    for a in doc.xpath("//a[@href]"):
        href = a.get("href").strip()
        if href.startswith(("mailto:", "tel:", "http:", "https:")):
            continue
        if href == "#":
            problems.append(f"[LINK] {name}: placeholder href='#' ({' '.join(a.text_content().split())[:40] or a.get('aria-label')})")
            continue
        parts = urllib.parse.urlsplit(href)
        target = parts.path or name
        if not os.path.exists(os.path.normpath(os.path.join(ROOT, target))):
            problems.append(f"[LINK] {name}: missing target {href}")
        elif parts.fragment and target in ids_by_page and parts.fragment not in ids_by_page[target]:
            problems.append(f"[LINK] {name}: broken anchor {href}")

    # heading order
    headings = [int(h.tag[1]) for h in doc.xpath("//h1|//h2|//h3|//h4|//h5|//h6")]
    h1s = doc.xpath("//h1")
    if len(h1s) != 1:
        problems.append(f"[A11Y] {name}: expected exactly one h1, found {len(h1s)}")
    prev = 0
    for level in headings:
        if prev and level > prev + 1:
            problems.append(f"[A11Y] {name}: heading jump h{prev} -> h{level}")
        prev = level

    # form labels
    for field in doc.xpath("//input[@type='text' or @type='email' or @type='tel' or @type='checkbox']|//textarea|//select"):
        fid = field.get("id")
        if fid:
            if not doc.xpath(f"//label[@for='{fid}']") and not field.xpath("ancestor::label"):
                problems.append(f"[A11Y] {name}: field #{fid} has no label")
        elif field.get("aria-label") is None:
            problems.append(f"[A11Y] {name}: field without id/label")

    # javascript hooks present?
    # buttons without text
    for btn in doc.xpath("//button"):
        if not (btn.text_content().strip() or btn.get("aria-label")):
            problems.append(f"[A11Y] {name}: button without accessible name")

print(f"Pages checked: {len(pages)}")
if problems:
    print(f"Problems: {len(problems)}")
    for p in problems:
        print(" -", p)
else:
    print("No problems found.")
