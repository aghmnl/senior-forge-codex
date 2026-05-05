---
layout: page
title: Glossary
lang: en
permalink: /en/glossary/
---

<div class="d-flex flex-column align-items-center justify-content-center py-5">
  <h2 class="mb-3 text-center">{{ site.data.translations.en.glossary_title }}</h2>
  <p class="text-muted text-center mb-5" style="max-width: 600px;">
    {{ site.data.translations.en.glossary_description }}
  </p>

  <div class="w-100" style="max-width: 600px;">
    <div class="input-group input-group-lg shadow-sm">
      <span class="input-group-text bg-transparent border-end-0">
        <i class="fas fa-search text-muted"></i>
      </span>
      <input type="text" id="glossary-search" class="form-control border-start-0" placeholder="Search terms (e.g. Coroutines, Mutex...)" aria-label="Search glossary terms" autofocus>
    </div>
    <div id="glossary-search-results" class="mt-4 w-100">
      <!-- Search results will appear here -->
    </div>
  </div>
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
