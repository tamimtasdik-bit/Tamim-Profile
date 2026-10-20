---
layout: default
title: Blogs
description: UK immigration law articles and legal analysis from Lawfinity Solicitors.
permalink: /blogs/
---
<section class="page-hero compact">
  <div class="container">
    <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{{ '/' | relative_url }}">Home</a><span>/</span><span>Blogs</span></nav>
    <p class="eyebrow">Resources &amp; Insight</p><h1>Blogs</h1>
    <p class="lede">Immigration law developments, legal insights and practical case commentary.</p>
  </div>
</section>
<section class="page-section">
  <div class="container">
    <p style="margin-bottom:28px;color:var(--muted)">The complete articles remain available on the firm's current website while the archive is being transferred. Select an article below to read its original text.</p>
    <div class="blog-grid">
    {% for post in site.posts %}
      <article class="blog-card">
        <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%-d %B %Y" }}</time>
        <h2><a href="https://lawfinitysolicitors.com{{ post.url }}">{{ post.title }}</a></h2>
        <a class="text-link" href="https://lawfinitysolicitors.com{{ post.url }}">Read original article →</a>
      </article>
    {% endfor %}
    </div>
  </div>
</section>