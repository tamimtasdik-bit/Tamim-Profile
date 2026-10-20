---
layout: default
title: Contact
description: Contact Lawfinity Solicitors in Covent Garden, London for UK immigration advice.
permalink: /contact/
---
<section class="page-hero compact"><div class="container"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{{ '/' | relative_url }}">Home</a><span>/</span><span>Contact</span></nav><p class="eyebrow">Contact us</p><h1>Speak to Lawfinity Solicitors</h1><p class="lede">Tell us about your immigration matter and the outcome you are seeking. We will help you identify the next practical step.</p></div></section>

<section class="page-section"><div class="container contact-grid">
  <div>
    <div class="contact-card">
      <p class="eyebrow">Our office</p><h2>Covent Garden, London</h2>
      <div class="contact-list">
        <div><strong>Address</strong><br>{{ site.firm.address }}</div>
        <div><strong>Phone</strong><br><a href="tel:{{ site.firm.phone_link }}">{{ site.firm.phone_display }}</a></div>
        <div><strong>Email</strong><br><a href="mailto:{{ site.firm.email }}">{{ site.firm.email }}</a></div>
      </div>
    </div>
    <iframe class="map-frame" title="Map showing Lawfinity Solicitors at Shelton Street, Covent Garden" loading="lazy" src="https://www.google.com/maps?q=71-75%20Shelton%20Street%2C%20Covent%20Garden%2C%20London%20WC2H%209JQ&output=embed"></iframe>
  </div>

  <div class="form-card">
    <p class="eyebrow light">Enquiry form</p><h2>How can we help?</h2>
    <p>Complete the form below. The form endpoint must be connected to the firm's Formspree account before production launch.</p>
    <form action="https://formspree.io/f/REPLACE_WITH_FORM_ID" method="POST">
      <div class="form-grid">
        <div class="field"><label for="name">Name</label><input id="name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
        <div class="field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
        <div class="field"><label for="area">Area of law</label><select id="area" name="area" required><option value="">Choose one</option><option>Family Immigration</option><option>Study Visas</option><option>Business & Work Visas</option><option>Settlement & Citizenship</option><option>Humanitarian & Asylum</option><option>Appeals & Reviews</option><option>EU Settlement Scheme</option><option>Corporate Immigration / Sponsor Licences</option><option>Commissioner for Oaths</option><option>Other</option></select></div>
        <div class="field full"><label for="message">Message</label><textarea id="message" name="message" required></textarea></div>
      </div>
      <label class="consent"><input type="checkbox" name="consent" required><span>I consent to Lawfinity Solicitors using the information I provide to respond to this enquiry. See our <a href="{{ '/gdpr-policy/' | relative_url }}">GDPR Policy</a>.</span></label>
      <button class="btn btn-light" type="submit">Send enquiry</button>
      <p class="form-note">Do not send confidential documents through this form until the firm has confirmed it can act for you.</p>
    </form>
  </div>
</div></section>

<section class="related-section"><div class="container"><div class="section-intro"><div><p class="eyebrow">News Feeds</p><h2>Latest articles</h2></div><a class="text-link" href="{{ '/blogs/' | relative_url }}">View all articles →</a></div><div class="post-grid">{% for post in site.posts limit:6 %}<article class="post-card"><span>Articles</span><h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3><p>{{ post.excerpt | strip_html | truncate: 130 }}</p><a class="text-link" href="{{ post.url | relative_url }}">Read more →</a></article>{% endfor %}</div></div></section>