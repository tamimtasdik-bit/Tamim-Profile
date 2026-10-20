#!/usr/bin/env python3
"""Transfer *original* public Lawfinity WordPress articles into the Jekyll archive.

Prefer WordPress REST rendered bodies; fallback to public single-article HTML.
Preserves original body HTML, original URL, title, date, and citation hyperlinks.
Never rewrites legal analysis. Fails closed rather than publishing fake summaries.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import os
import pathlib
import re
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parents[1]
POSTDIR = ROOT / "_posts"
BASE = "https://lawfinitysolicitors.com"
SLUGS = """
brexits-impact-on-modern-slavery-in-the-uks-hospitality-industry-an-alarming-trend
article-14-and-the-right-to-non-discrimination-analyzing-r-swp-v-secretary-of-state-for-the-home-department
detention-of-pregnant-women-and-children-concerns-raised-over-proposed-uk-asylum-legislation
navigating-the-immigration-tribunal-the-advisors-guide-to-seeking-adjournment
the-intersection-of-mental-health-and-immigration-bail-applying-for-immigration-bail-on-grounds-of-mental-health
judicial-conduct-and-fair-hearings-an-analysis-of-the-case-of-sshd-vs-ms-anonymity-order-made-bangladesh-2023-ukut-00114
navigating-the-compassionate-path-assisting-vulnerable-clients
unprecedented-surge-in-modern-slavery-alarming-statistics-from-england-and-wales
modern-slavery-and-the-implications-of-objective-evidence-on-victims-rights-and-recent-developments
navigating-paternity-tests-in-complex-cases-a-handy-guide
siac-ruling-in-d5-d6-d7-v-sshd-expanding-the-scope-of-deprivation-decisions
policy-paradox-a-deep-dive-into-uk-immigration-reforms
navigating-spouse-visa-refusals-based-on-illegal-working-a-comprehensive-legal-analysis
navigating-deprivation-unraveling-procedure-and-discretion-a-critical-analysis-of-kolicaj-deprivation-procedure-and-discretion-albania-2023
decoding-the-impact-of-dani-non-removal-human-rights-submissions-albania-2023-ukut-293-iac-on-article-8-in-euss-appeals
breach-of-rights-xys-legal-odyssey-against-sshds-unlawful-practices-secret-policy-breach-of-art-8-art-14-and-lack-of-candour-transparency
unveiling-the-dynamics-home-offices-recent-guidance-on-public-order-disqualification-and-re-trafficking-risk-assessment-under-the-nationality-and-bo
securing-due-process-lessons-learned-from-ullah-v-secretary-of-state-for-the-home-department
understanding-historical-injustice-a-close-look-at-recent-legal-precedents
md-and-others-v-secretary-of-state-for-the-home-department-interpretation-of-appendix-eu-family-permit-fp6-1d
navigating-waiver-requests-for-the-knowledge-of-language-and-life-in-the-uk-requirement-a-comprehensive-guide-for-legal-practitioners
immigration-appeal-success-a-case-of-illegal-work-and-re-documentation-challenges
lack-of-clear-tribunal-reasoning-and-limitations-of-the-eu-withdrawal-agreement-case-analysis-the-upper-tribunals-decision-on-eu-settlement-scheme
upper-tribunal-rejects-realistic-prospect-test-in-zambrano-rights-assessment-key-implications-of-the-maisiri-case
dealing-with-vulnerable-clients-facing-removal-and-detention-a-guide-for-immigration-lawyers
expert-evidence-in-judicial-review-insights-from-r-ms-v-kent-county-council-and-practical-steps-for-compliance-with-cpr-35-41
navigating-the-cancellation-and-curtailment-of-leave-under-appendix-eu-key-considerations-for-legal-practitioners-and-pre-settled-status-holders
handling-detention-and-removal-matters-during-the-holiday-period-a-guide-for-immigration-lawyers
""".strip().splitlines()

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (compatible; LawfinityMigration/1.0; +https://lawfinitysolicitors.com/)",
    "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
})
report: list[dict] = []


def get(url: str, *, timeout=30):
    resp = session.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp


def wordpress_posts():
    records = []
    for page in range(1, 5):
        url = f"{BASE}/wp-json/wp/v2/posts"
        try:
            response = get(url + f"?per_page=100&page={page}&_fields=id,slug,link,date,title,content,excerpt,modified")
            value = response.json()
            if not isinstance(value, list):
                print("WordPress API returned non-list", str(value)[:250])
                break
            records.extend(value)
            if len(value) < 100:
                break
        except Exception as e:
            print(f"WordPress API error page {page}: {type(e).__name__}: {e}")
            break
    return {item['slug']: item for item in records if isinstance(item,dict) and item.get('slug')}


def clean_html(raw: str) -> tuple[str, int]:
    soup = BeautifulSoup(raw, "html.parser")
    for bad in soup.select("script, style, iframe, form, nav, .sharedaddy, .wp-block-buttons .wp-block-button__link"):
        bad.decompose()
    for tag in soup.find_all(True):
        for attr in list(tag.attrs):
            if attr not in {"href", "src", "alt", "title", "width", "height", "colspan", "rowspan", "class"}:
                del tag[attr]
        if tag.name == "a" and tag.get("href"):
            tag["href"] = urljoin(BASE, tag["href"])
        if tag.name == "img" and tag.get("src"):
            tag["src"] = urljoin(BASE, tag["src"])
    body = str(soup).strip()
    words = len(soup.get_text(" ", strip=True).split())
    return body, words


def fallback_page(slug: str):
    url = f"{BASE}/articles/{slug}/"
    response = get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title_element = soup.find("h1") or soup.find("h2")
    title = title_element.get_text(" ", strip=True) if title_element else slug.replace("-", " ").title()
    timestamp = soup.find("time", attrs={"datetime": True})
    if timestamp:
        date = timestamp["datetime"][:10]
    else:
        date = "2025-01-06"
        for phrase in ["January 5, 2025", "January 6, 2025"]:
            if phrase in soup.get_text(" ", strip=True):
                date = "2025-01-05" if "January 5" in phrase else "2025-01-06"
                break
    selectors = [
        ".pxl-post--content", ".pxl-post-content", ".entry-content",
        ".post-content", ".single-post-content", ".blog-details-content",
        ".elementor-widget-theme-post-content .elementor-widget-container",
        "article .elementor-widget-text-editor .elementor-widget-container",
        "article .item--content", ".post-details .content", "article",
    ]
    options = []
    for sel in selectors:
        for node in soup.select(sel):
            fragment, words = clean_html(str(node))
            if words >= 120:
                options.append((words, fragment, sel))
    if not options:
        print(f"No suitable content node for {slug}")
        return None
    options.sort(key=lambda x: (x[2] == "article", -x[0]))
    # Pick most specific eligible selector before broad article fallback.
    for selector in selectors:
        matches = [item for item in options if item[2] == selector]
        if matches:
            words, content, chosen = max(matches, key=lambda x: x[0])
            print(f"HTML fallback {slug}: {words} words from {chosen}")
            return {"title": title, "date": date, "content": content, "words": words, "source": "html"}
    return None


def load(slug, api):
    data = api.get(slug)
    if data and data.get("content", {}).get("rendered"):
        body, words = clean_html(data["content"]["rendered"])
        title = BeautifulSoup(data.get("title", {}).get("rendered",""), "html.parser").get_text(" ",strip=True)
        date = data.get("date", "2025-01-06")[:10]
        if words >= 120:
            return {"title": title, "date": date, "content": body, "words": words, "source": "wordpress-rest"}
        print(f"WordPress API content too short for {slug}: {words}")
    try:
        return fallback_page(slug)
    except Exception as exc:
        print(f"HTML fallback error {slug}: {type(exc).__name__}: {exc}")
        return None


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def main():
    api = wordpress_posts()
    print(f"WordPress API returned {len(api)} posts; expected {len(SLUGS)} listed articles")
    POSTDIR.mkdir(parents=True, exist_ok=True)
    imported = 0
    for slug in SLUGS:
        data = load(slug, api)
        if not data:
            report.append({"slug":slug, "status":"MISSING"})
            continue
        if data["words"] < 120:
            report.append({"slug":slug,"status":"TOO_SHORT","words":data["words"]})
            continue
        old = list(POSTDIR.glob("*-" + slug + ".md"))
        for existing in old:
            existing.unlink()
        published = data["date"]
        try:
            dt.date.fromisoformat(published)
        except Exception:
            published = "2025-01-06"
        source_url = f"{BASE}/articles/{slug}/"
        source_metadata = (
            "---\n"
            "layout: post\n"
            f"title: {yaml_string(data['title'])}\n"
            f"date: {published} 12:00:00 +0000\n"
            f"permalink: /articles/{slug}/\n"
            f"source_url: {yaml_string(source_url)}\n"
            "category: Articles\n"
            "description: \"Legal insight originally published by Lawfinity Solicitors.\"\n"
            "---\n\n"
        )
        dest = POSTDIR / f"{published}-{slug}.md"
        dest.write_text(source_metadata + data["content"] + "\n", encoding="utf-8")
        imported += 1
        report.append({"slug":slug,"status":"IMPORTED","words":data["words"],"source":data["source"],"path":str(dest.relative_to(ROOT))})
        print(f"IMPORTED {slug} ({data['words']} words, {data['source']})")
    results = {"expected":len(SLUGS),"imported":imported,"missing":len(SLUGS)-imported,"posts":report}
    (ROOT/"article-import-report.json").write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps({"expected":len(SLUGS),"imported":imported,"missing":len(SLUGS)-imported},indent=2))
    # Fail closed: require complete migration to avoid publishing an incomplete archive
    if imported != len(SLUGS):
        sys.exit(2)


if __name__ == "__main__":
    main()
