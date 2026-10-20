---
layout: default
title: Blogs
description: Immigration law articles and legal insights from Lawfinity Solicitors.
permalink: /blogs/
---
<section class="page-hero compact"><div class="container"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{{ '/' | relative_url }}">Home</a><span>/</span><span>Blogs</span></nav><p class="eyebrow">Resources &amp; Insight</p><h1>Blogs</h1><p class="lede">Commentary on UK immigration law, procedure, case law and issues affecting clients and practitioners.</p></div></section>
<section class="page-section"><div class="container">
  <div class="archive-note"><strong>Archive migration:</strong> the article URLs and titles have been preserved. Full original article bodies still need to be migrated from the existing site before production launch.</div>
  <div class="blog-grid">{% for post in site.posts %}<article class="blog-card"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%-d %B %Y" }}</time><h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2><p>{{ post.excerpt | strip_html | truncate: 155 }}</p><a class="text-link" href="{{ post.url | relative_url }}">Read more →</a></article>{% endfor %}</div>
</div></section>