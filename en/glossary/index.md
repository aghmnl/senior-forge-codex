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

  <div class="w-100" style="max-width: 500px;">
    <div class="input-group input-group-lg shadow-sm">
      <span class="input-group-text bg-transparent border-end-0">
        <i class="fas fa-search text-muted"></i>
      </span>
      <input type="text" id="glossary-search" class="form-control border-start-0" placeholder="Search terms (e.g. Coroutines, Mutex...)" aria-label="Search glossary terms">
    </div>
  </div>
</div>

<div id="glossary-list" class="mt-5">
  <!-- This section can be used to list categories or common terms if needed -->
</div>

<script>
  // Bridge the glossary search with the top-bar search for a unified experience
  document.getElementById('glossary-search').addEventListener('input', function(e) {
    const topSearch = document.getElementById('search-input');
    if (topSearch) {
      topSearch.value = e.target.value;
      // Trigger the same event as the top search to invoke the Chirpy search engine
      topSearch.dispatchEvent(new Event('input', { bubbles: true }));
      
      // Focus the top search to show the results dropdown
      if (e.target.value.length > 0) {
        document.getElementById('search-trigger').click();
        topSearch.focus();
      }
    }
  });
</script>
