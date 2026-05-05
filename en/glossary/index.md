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
      <!-- Search results will be mirrored here -->
    </div>
  </div>
</div>

<script>
  document.addEventListener('DOMContentLoaded', function() {
    const glossaryInput = document.getElementById('glossary-search');
    const topSearchInput = document.getElementById('search-input');
    const topSearchResults = document.getElementById('search-results');
    const glossaryResults = document.getElementById('glossary-search-results');

    if (glossaryInput && topSearchInput) {
      glossaryInput.addEventListener('input', function(e) {
        const query = e.target.value;
        
        // Sync with top search
        topSearchInput.value = query;
        topSearchInput.dispatchEvent(new Event('input', { bubbles: true }));

        // Use a small timeout to let Chirpy's search engine render the results
        setTimeout(() => {
          if (query.length > 0) {
            // Mirror the results found in the top-bar search panel
            const resultsContent = topSearchResults.querySelector('.content');
            if (resultsContent) {
              glossaryResults.innerHTML = resultsContent.innerHTML;
              
              // Remove unwanted headers or empty messages if necessary
              const emptyMsg = glossaryResults.querySelector('.text-muted');
              if (emptyMsg && emptyMsg.innerText.includes('No results')) {
                 // Keep it or style it
              }
            }
          } else {
            glossaryResults.innerHTML = '';
          }
        }, 100);
      });

      // Also handle the 'Enter' key to follow the first result if needed
      glossaryInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
          const firstResult = glossaryResults.querySelector('a');
          if (firstResult) firstResult.click();
        }
      });
    }
  });
</script>
