---
layout: default
title: Blogs
description: UK immigration law articles and legal analysis from Lawfinity Solicitors.
permalink: /blogs/
---
<section class="page-hero compact">
  <div class="container">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{{ '/' | relative_url }}">Home</a><span>/</span><span>Blogs</span></nav>
    <p class="eyebrow">Resources &amp; Insight</p><h1>Legal Articles &amp; Commentary</h1>
    <p class="lede">UK immigration law, tribunal decisions, judicial review and practical legal analysis.</p>
  </div>
</section>
<section class="page-section">
  <div class="container">
    <div class="blog-grid">
      {% for post in site.posts %}
      <article class="blog-card">
        <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%-d %B %Y" }}</time>
        <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
        <p>{{ post.excerpt | strip_html | truncate: 155 }}</p>
        <a class="text-link" href="{{ post.url | relative_url }}">Read full article →</a>
      </article>
      {% endfor %}
    </div>
  </div>
</section>