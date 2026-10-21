---
layout: default
title: Blogs
description: Legal articles and immigration law commentary from Lawfinity Solicitors.
permalink: /blogs/
---
<section class="page-hero"><div class="container">
  <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{{ '/' | relative_url }}">Home</a><span>/</span><span>Blogs</span></nav>
  <p class="kicker">Resources &amp; Insight</p><h1>Legal insights</h1><p class="lede">Case law, immigration procedure and commentary from Lawfinity Solicitors.</p>
</div></section>
<section class="page-section"><div class="container"><div class="blog-grid">{% for post in site.posts %}
  <article class="blog-card"><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%-d %B %Y" }}</time><h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2><p>{{ post.excerpt | strip_html | truncate: 155 }}</p><a class="understated-link" href="{{ post.url | relative_url }}">Read full article →</a></article>
{% endfor %}</div></div></section>