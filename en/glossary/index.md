---
layout: page
title: Glossary
lang: en
permalink: /en/glossary/
---

<p class="text-muted mb-4">
  {{ site.data.translations.en.glossary_description }}
</p>

<div class="mb-4" style="max-width: 600px;">
  <div class="input-group input-group-lg shadow-sm">
    <span class="input-group-text bg-transparent border-end-0">
      <i class="fas fa-search text-muted"></i>
    </span>
    <input type="text" id="glossary-search" class="form-control border-start-0" placeholder="Search terms (e.g. Coroutines, Mutex...)" aria-label="Search glossary terms" autofocus>
  </div>
</div>

<div id="glossary-search-results" class="mt-4">
</div>

<script>
  (function() {
    const searchInput = document.getElementById('glossary-search');
    const resultsContainer = document.getElementById('glossary-search-results');
    let searchData = null;

    async function loadSearchData() {
      if (searchData) return searchData;
      try {
        const response = await fetch('{{ "/assets/js/data/search.json" | relative_url }}');
        if (!response.ok) throw new Error("HTTP " + response.status);
        searchData = await response.json();
        return searchData;
      } catch (e) {
        console.error("Glossary: Failed to load search index", e);
        return null;
      }
    }

    function renderResult(item) {
      return `
        <article class="px-1 px-sm-2 px-lg-4 px-xl-0 mb-5">
          <header>
            <h2 class="h4 mb-1"><a href="${item.url}">${item.title}</a></h2>
            <div class="post-meta d-flex flex-column flex-sm-row text-muted mt-1 mb-1 small">
              ${item.categories ? `<div class="me-sm-4"><i class="far fa-folder fa-fw"></i>${item.categories}</div>` : ''}
              ${item.tags ? `<div><i class="fa fa-tag fa-fw"></i>${item.tags}</div>` : ''}
            </div>
          </header>
          <p class="text-muted small">${item.snippet || ''}</p>
        </article>
      `;
    }

    if (searchInput) {
      searchInput.addEventListener('input', async (e) => {
        const query = e.target.value.toLowerCase().trim();
        const data = await loadSearchData();
        
        if (!data) return;
        if (query.length === 0) {
          resultsContainer.innerHTML = '';
          return;
        }

        const filtered = data.filter(item => 
          item.title.toLowerCase().includes(query) || 
          (item.snippet && item.snippet.toLowerCase().includes(query)) ||
          (item.tags && item.tags.toLowerCase().includes(query))
        );

        if (filtered.length > 0) {
          resultsContainer.innerHTML = filtered.map(renderResult).join('');
        } else {
          resultsContainer.innerHTML = `<p class="mt-5 text-center text-muted">{{ site.data.locales.en.search.no_results }}</p>`;
        }
      });

      searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          const firstLink = resultsContainer.querySelector('a');
          if (firstLink) firstLink.click();
        }
      });
    }
  })();
</script>

{% assign glossary_posts = '' | split: '' %}
{% for p in site.categories['glossary'] %}
  {% if p.lang == 'en' %}
    {% assign glossary_posts = glossary_posts | push: p %}
  {% endif %}
{% endfor %}

{% if glossary_posts.size > 0 %}
<style>
  #glossary-browse .card-body .text-muted p {
    margin: 0 !important;
    display: -webkit-box !important;
    -webkit-box-orient: vertical !important;
    overflow: hidden !important;
    -webkit-line-clamp: 4;
  }
</style>
<aside id="glossary-browse" aria-labelledby="glossary-browse-label" class="mt-5">
  <h3 class="mb-4" id="glossary-browse-label">
    {{ site.data.locales.en.post.relate_posts | default: "Further Reading" }}
  </h3>
  <nav class="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-4 mb-4">
    {% for post in glossary_posts limit: 6 %}
      <article class="col">
        <a href="{{ post.url | relative_url }}" class="post-preview card h-100">
          <div class="card-body">
            {% include datetime.html date=post.date lang='en' %}
            <h4 class="pt-0 my-2">{{ post.title }}</h4>
            <div class="text-muted">
              <p>{% include post-summary.html %}</p>
            </div>
          </div>
        </a>
      </article>
    {% endfor %}
  </nav>
</aside>
{% endif %}
