---
layout: page
title: Glosario
lang: es
permalink: /es/glosario/
---

<div class="d-flex flex-column align-items-center justify-content-center py-5">
  <h2 class="mb-3 text-center">{{ site.data.translations.es.glossary_title }}</h2>
  <p class="text-muted text-center mb-5" style="max-width: 600px;">
    {{ site.data.translations.es.glossary_description }}
  </p>

  <div class="w-100" style="max-width: 600px;">
    <div class="input-group input-group-lg shadow-sm">
      <span class="input-group-text bg-transparent border-end-0">
        <i class="fas fa-search text-muted"></i>
      </span>
      <input type="text" id="glossary-search" class="form-control border-start-0" placeholder="Buscar términos (ej. Corrutinas, Mutex...)" aria-label="Buscar términos del glosario" autofocus>
    </div>
    <div id="glossary-search-results" class="mt-4 w-100">
      <!-- Los resultados de búsqueda se reflejarán aquí -->
    </div>
  </div>
</div>

{% capture result_elem %}
  <article class="px-1 px-sm-2 px-lg-4 px-xl-0 mb-5">
    <header>
      <h2 class="h4 mb-1"><a href="{url}">{title}</a></h2>
      <div class="post-meta d-flex flex-column flex-sm-row text-muted mt-1 mb-1 small">
        {categories}
        {tags}
      </div>
    </header>
    <p class="text-muted small">{snippet}</p>
  </article>
{% endcapture %}

{% capture not_found %}<p class="mt-5 text-center text-muted">{{ site.data.locales.es.search.no_results }}</p>{% endcapture %}

<script>
  // Esperar a que el tema cargue SimpleJekyllSearch
  function initGlossarySearch() {
    if (typeof SimpleJekyllSearch === 'function') {
      SimpleJekyllSearch({
        searchInput: document.getElementById('glossary-search'),
        resultsContainer: document.getElementById('glossary-search-results'),
        json: '{{ "/assets/js/data/search.json" | relative_url }}',
        searchResultTemplate: '{{ result_elem | strip_newlines }}',
        noResultsText: '{{ not_found }}',
        templateMiddleware: function(prop, value, template) {
          if (prop === 'categories') {
            return value === '' ? '' : `<div class="me-sm-4"><i class="far fa-folder fa-fw"></i>${value}</div>`;
          }
          if (prop === 'tags') {
            return value === '' ? '' : `<div><i class="fa fa-tag fa-fw"></i>${value}</div>`;
          }
        }
      });
    } else {
      // Reintentar si aún no se ha cargado
      setTimeout(initGlossarySearch, 100);
    }
  }
  
  document.addEventListener('DOMContentLoaded', initGlossarySearch);
</script>
