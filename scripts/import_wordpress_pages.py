#!/usr/bin/env python3
"""Import the original Lawfinity WordPress service/policy/about page copy.

Use public WordPress REST content; preserve full text, headings, URLs and lists.
Skip non-Lawfinity WordPress template demo content.
Commit only validated pages and a source-content audit.
"""
from __future__ import annotations
import html
import json
import re
import pathlib
import sys
import requests
import yaml
from bs4 import BeautifulSoup, NavigableString, Tag
from urllib.parse import urlparse, urljoin

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = "https://lawfinitysolicitors.com"
API = BASE + "/wp-json/wp/v2/pages"
OUTPUT = ROOT / "live-content-import-report.json"

# These are the actual Lawfinity service, legal compliance, and information routes.
# Do not migrate Bravis template demos, test products, fictional staff or example pages.
HUBS = """family-immigration study-visa business-work-visas settlement-citizenship
humanitarian-asylum appeals-reviews eu-settlement-status other-immigration-services""".split()
SERVICES = """spouse-visa child-dependent-visa fiance-visa marriage-visitor-visa
dependent-and-elderly-relative-visas unmarried-partner-visa uk-ancestry-visa
student-visa graduate-visa skilled-worker-visa citizenship-by-descent ilr
indefinite-leave-to-remain-based-on-long-residence naturalisation
registration-of-a-stateless-child-as-a-british-citizen
registration-of-a-child-under-18-as-a-british-citizen asylum-application
discretionary-leave-to-remain immigration-appeals administrative-review judicial-review
pre-settled-status settled-status eu-family-member uk-visitor-visas
immigration-detention-bail-and-removals sponsor-licence-application-and-compliance
sponsorship-management-system sponsor-licence-suspension-and-revocation
additional-business-support affidavits-and-statutory-declarations-at-lawfinity-solicitors
deed-poll document-legalisation-and-certification power-of-attorney travel-authorisation""".split()
POLICIES = """complaint-handling-policy data-protection-policy
equality-and-diversity-and-vulnerable-clients-policy fee-scale gdpr-policy
online-review-policy website-terms-of-use""".split()
TARGETS = ["about"] + HUBS + SERVICES + POLICIES

STOP_TITLES = (
    "news feeds", "latest articles", "blog", "archives", "categories",
    "contact info", "follow us", "our brochures",
)
SKIP_WIDGET_TYPES = {
    "spacer", "divider", "google_maps", "image", "social-icons",
    "nav-menu", "sidebar", "wp-widget-archives", "wp-widget-categories",
    "pxl_blog_grid", "pxl_post_grid", "pxl_blog_carousel",
    "woocommerce-cart", "shortcode", "form", "contact-form-7",
}
TEXT_WIDGETS = {
    "text-editor", "heading", "icon-list", "icon-box", "image-box",
    "button", "toggle", "accordion", "tabs", "nested-tabs", "blockquote",
    "html", "alert", "testimonial",
}

session = requests.Session()
session.headers.update({
    "User-Agent":"Mozilla/5.0 (compatible; LawfinityContentMigration/2.0; +https://lawfinitysolicitors.com)",
    "Accept":"application/json,text/html;q=0.9,*/*;q=0.8"
})

def get_pages():
    allpages = {}
    for page in range(1, 8):
        r = session.get(API,params={
            "per_page":100, "page":page,
            "_fields":"slug,title,content,link,status,modified"},timeout=50)
        if not r.ok:
            if page == 1: raise RuntimeError(f"WordPress pages API: {r.status_code}")
            break
        data = r.json()
        if not isinstance(data,list): raise RuntimeError("Unexpected WordPress response")
        for item in data:
            if item.get("slug"): allpages[item["slug"]] = item
        if len(data) < 100: break
    return allpages

def safe_yaml(data):
    return "---\n" + yaml.safe_dump(data,sort_keys=False,allow_unicode=True,width=1000) + "---\n\n"

def old_frontmatter(filepath):
    if not filepath.is_file(): return {}
    content=filepath.read_text(encoding="utf-8")
    m=re.match(r"\A---\s*\n(.*?)\n---\s*\n",content,re.DOTALL)
    if not m:return {}
    obj=yaml.safe_load(m.group(1))
    return obj if isinstance(obj,dict) else {}

def clean_fragment(fragment, slugs):
    if isinstance(fragment, Tag):
        fragment=BeautifulSoup(str(fragment),"html.parser")
    elif isinstance(fragment,str):
        fragment=BeautifulSoup(fragment,"html.parser")
    # Strip Elementor display markup; retain actual prose, headings, lists and links.
    for child in fragment.select("script,style,svg,noscript,iframe,form,video,audio,canvas,button,.elementor-icon"):
        child.decompose()
    for child in list(fragment.find_all(True)):
        if child.name in {"a","img"}:
            key="href" if child.name=="a" else "src"
            value=child.get(key)
            if value:
                absolute=urljoin(BASE,value)
                u=urlparse(absolute)
                if child.name=="a" and u.netloc in ("lawfinitysolicitors.com","www.lawfinitysolicitors.com"):
                    local=u.path.strip("/")
                    if local in slugs:
                        child[key]="{{ '/"+local+"/' | relative_url }}"
                    elif local in ("","home"):
                        child[key]="{{ '/' | relative_url }}"
                    else:
                        child[key]=absolute
                else:
                    child[key]=absolute
        for a in list(child.attrs):
            if a not in {"href","src","alt","title","colspan","rowspan","scope","target","rel"}:
                del child.attrs[a]
        if child.name=="a" and child.get("href","").startswith("https://"):
            child["rel"]="noopener noreferrer"
    return fragment

def widget_fragment(widget, slugs):
    typ=(widget.get("data-widget_type") or "").split(".")[0].lower()
    if typ in SKIP_WIDGET_TYPES:return ""
    container=widget.select_one(".elementor-widget-container")
    if not container:return ""
    if typ not in TEXT_WIDGETS:
        # Many Elementor / third-party widgets are navigational or decorative.
        # Keep unknown widgets with substantial prose but no nested widgets.
        if len(container.get_text(" ",strip=True).split()) < 18:return ""
    text=container.get_text(" ",strip=True).lower()
    if text in STOP_TITLES or any(text.startswith(s) and len(text)<60 for s in STOP_TITLES):
        return "<!-- STOP_CONTENT -->"
    cleaned=clean_fragment(container,slugs)
    root=cleaned.select_one(".elementor-widget-container")
    if root is None:return ""
    # Drop decorative Elementor wrappers but preserve inner text and heading semantics.
    for wrapper in list(root.select(".elementor-icon-box-wrapper,.elementor-image-box-wrapper,.elementor-icon-box-content,.elementor-image-box-content,.elementor-toggle,.elementor-accordion,.elementor-tabs,.elementor-tab-content")):
        wrapper.unwrap()
    for icon in list(root.select(".elementor-icon-box-icon,.elementor-image-box-img,.elementor-toggle-icon,.elementor-accordion-icon")):
        icon.decompose()
    for entry in list(root.select(".elementor-heading-title")):
        if entry.name=="div":entry.name="h3"
    # Convert WordPress/Elementor interactive section labels to semantic headings.
    for elem in list(root.select(".elementor-tab-title,.elementor-toggle-title")):
        elem.name="h3"
    for node in list(root.find_all(True)):
        if node.name=="div" and not node.get_text(" ",strip=True):node.decompose()
        if node.name=="span" and not node.find(["a","img","br"]):node.unwrap()
    output="".join(str(c) for c in root.contents).strip()
    return output

def extract(body, slugs, title):
    soup=BeautifulSoup(body,"html.parser")
    main=soup.select_one(".elementor") or soup
    widgets=[]  # Preserve full source HTML; flatten Elementor wrappers afterwards
    chunks=[]
    stopped=False
    for w in widgets:
        if w.find_parent(class_="elementor-widget"):continue
        frag=widget_fragment(w,slugs)
        if "<!-- STOP_CONTENT -->" in frag:
            stopped=True
            break
        if frag:chunks.append(frag)
    rendered="\n".join(chunks).strip()
    # The site uses Elementor for its main content: use a safe fallback if a
    # route has no Elementor widgets or a plugin's widget types are unknown.
    if not rendered:
        fallback=soup.select_one(".entry-content") or soup
        cleaned=clean_fragment(fallback,slugs)
        rendered=str(cleaned)
    result=BeautifulSoup(rendered,"html.parser")
    # Elementor layout divs are meaningless without WordPress' theme. Unwrap
    # them while retaining every paragraph, list, link, table and heading.
    for decorative in list(result.find_all(["div","section","span"])):
        decorative.unwrap()
    for image in list(result.find_all("img")):
        if "Transparent-Logo" in image.get("src","") or not image.get("alt","").strip():
            image.decompose()
    # Remove the WordPress template's automated article feed, where present;
    # the new layout supplies its own linked Insights section.
    marker=next((h for h in result.find_all(["h2","h3","h4","h5","h6"])
        if h.get_text(" ",strip=True).casefold().rstrip(".") in ("news feeds","news feed")),None)
    if marker:
        for node in list(marker.next_siblings):node.extract()
        marker.decompose()
    # Drop empty decorative blocks and repeated top-level page title.
    for node in list(result.find_all(["p","div","span","h2","h3"])):
        if not node.get_text(" ",strip=True) and not node.find("img"):node.decompose()
    for h in result.find_all(["h1","h2","h3"],limit=2):
        if h.get_text(" ",strip=True).casefold()==title.casefold():h.decompose()
        break
    words=len(result.get_text(" ",strip=True).split())
    source_words=len(soup.get_text(" ",strip=True).split())
    return str(result).strip(), words, source_words, stopped

def main():
    pages=get_pages()
    known_slugs=set(TARGETS+["contact","blogs","coming-soon"])
    report=[]
    generated=[]
    failures=[]
    for slug in TARGETS:
        obj=pages.get(slug)
        if not obj or not obj.get("content",{}).get("rendered"):
            failures.append(slug)
            report.append({"slug":slug,"status":"MISSING_SOURCE"})
            continue
        title=BeautifulSoup(obj.get("title",{}).get("rendered",""),"html.parser").get_text(" ",strip=True)
        body,words,source_words,stopped=extract(obj["content"]["rendered"],known_slugs,title)
        min_words=15 if slug in HUBS else (130 if slug in POLICIES else 90)
        if words < min_words:
            report.append({"slug":slug,"status":"INSUFFICIENT_CONTENT","words":words,"source_words":source_words})
            failures.append(slug)
            continue
        file=ROOT/slug/"index.md"
        front=old_frontmatter(file)
        front.update({"layout":"hub" if slug in HUBS else ("page" if slug in POLICIES else ("replica" if slug=="about" else "service")),
                      "title":title or front.get("title",slug.replace("-"," ").title()),
                      "permalink":"/"+slug+"/",
                      "source_url":obj.get("link",BASE+"/"+slug+"/"),
                      "description":front.get("description") or title})
        front.pop("noindex",None)
        if slug not in HUBS:front.pop("cards",None)
        if slug not in HUBS:front.pop("intro",None)
        if slug not in HUBS:front.pop("overview",None)
        text=safe_yaml(front) + '<div class="live-source-content">\n'+body+'\n</div>\n'
        generated.append((file,text))
        report.append({"slug":slug,"status":"IMPORTED","words":words,"source_words":source_words,"coverage":round(words/max(source_words,1),2),"source_url":front["source_url"]})
        print("IMPORTED",slug,words,"/",source_words,"words")
    OUTPUT.write_text(json.dumps({
        "expected":len(TARGETS),
        "imported":len(generated),
        "missing":failures,
        "report":report,
        "source":BASE,
        "note":"Content imported from public WordPress pages; review legal accuracy, external links and imagery before replacing production."
    },indent=2,ensure_ascii=False),encoding="utf-8")
    if failures:
        print("ERROR: Not overwriting any pages because some originals could not be validated",failures)
        sys.exit(2)
    for file,content in generated:
        file.parent.mkdir(parents=True,exist_ok=True)
        file.write_text(content,encoding="utf-8")
    print("SUCCESS: Imported",len(generated),"complete Lawfinity pages")

if __name__=="__main__":main()
