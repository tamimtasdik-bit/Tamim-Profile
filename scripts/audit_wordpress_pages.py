#!/usr/bin/env python3
"""Audit which sources reliably expose the live site's page content."""
import json, requests
from bs4 import BeautifulSoup

base="https://lawfinitysolicitors.com"
paths=["about","family-immigration","sponsor-licence-application-and-compliance",
       "affidavits-and-statutory-declarations-at-lawfinity-solicitors",
       "spouse-visa","skilled-worker-visa","gdpr-policy","fee-scale","contact",
       "blogs","settlement-citizenship"]
s=requests.Session()
s.headers.update({"User-Agent":"Mozilla/5.0 (compatible; LawfinitySiteMigration/1.0)","Accept":"text/html,application/json;q=0.9"})
try:
 r=s.get(base+"/wp-json/wp/v2/pages?per_page=100&_fields=id,slug,link,title,content,modified",timeout=35)
 print("REST_PAGES",r.status_code,len(r.content),r.text[:130])
 data=r.json() if r.ok else []
 if isinstance(data,list):
  for p in data[:100]:
   slug=p.get("slug"); txt=BeautifulSoup(p.get("content",{}).get("rendered",""),"html.parser").get_text(" ",strip=True)
   print("REST_PAGE",slug,len(txt.split()),txt[:80])
except Exception as e:print("REST_ERROR",str(e)[:190])
report=[]
for slug in paths:
 try:
  r=s.get(base+"/"+slug+"/",timeout=25)
  soup=BeautifulSoup(r.text,"html.parser")
  item={"slug":slug,"status":r.status_code,"bytes":len(r.content),"title":soup.title.get_text(strip=True) if soup.title else ""}
  for selector in ["main",".site-content",".pxl-page-content",".pxl-content",".elementor-location-single",".elementor",".elementor-widget-container",".entry-content",".pxl-post--content",".pxl-content-area",".pxl-row",".page-content"]:
   matches=soup.select(selector)
   if matches:
    wordcounts=[len(x.get_text(" ",strip=True).split()) for x in matches]
    item[selector]={"count":len(matches),"maxwords":max(wordcounts),"sumwords":sum(wordcounts),"sample":max(matches,key=lambda x:len(x.get_text(" ",strip=True))).get_text(" ",strip=True)[:120]}
  headings=soup.select("h1,h2,h3")
  item["headings"]=[x.get_text(" ",strip=True)[:80] for x in headings[:10]]
  item["mainhtml"]=str(soup.find("main"))[:170] if soup.find("main") else None
  report.append(item)
  print("AUDIT",json.dumps(item,ensure_ascii=False))
 except Exception as e:print("ERROR",slug,str(e)[:150])
with open("wp-audit-report.json","w") as f:json.dump(report,f,ensure_ascii=False,indent=2)
