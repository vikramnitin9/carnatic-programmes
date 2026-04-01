---
layout: default
title: Home
---

# Programme Archive

Historical concert programmes from the Music Academy Madras and other South Indian music conferences, spanning 1935–1960.

<p style="margin: 1rem 0; font-size: 0.9rem; color: #666; font-style: italic;">These records have been extracted using OCR on the original souvenir booklets, and as a result there may be minor errors. Cross-check any important information with the original PDFs.</p>

<p style="margin: 1rem 0;"><a href="{{ '/search' | relative_url }}" style="font-size: 1.05rem;">🔍 Search by artist, song, raga, tala, or composer →</a></p>

{% assign programmes = site.pages | where: "type", "programme" | sort: "year" %}
{% assign decades = programmes | group_by_exp: "p", "p.year | divided_by: 10 | times: 10" %}

{% for decade in decades %}
<div class="decade-section">
<h2 class="decade-title">{{ decade.name }}s</h2>
<ul class="programme-list">
{% for p in decade.items %}
<li><a href="{{ p.url | relative_url }}"><span class="programme-year">{{ p.year }}</span> <span class="programme-label">{{ p.conference }}</span></a></li>
{% endfor %}
</ul>
</div>
{% endfor %}
