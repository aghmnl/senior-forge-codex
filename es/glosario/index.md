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

<script>
  document.addEventListener('DOMContentLoaded', function() {
    const glossaryInput = document.getElementById('glossary-search');
    const topSearchInput = document.getElementById('search-input');
    const topSearchResults = document.getElementById('search-results');
    const glossaryResults = document.getElementById('glossary-search-results');

    if (glossaryInput && topSearchInput) {
      glossaryInput.addEventListener('input', function(e) {
        const query = e.target.value;
        
        // Sincronizar con la búsqueda superior
        topSearchInput.value = query;
        topSearchInput.dispatchEvent(new Event('input', { bubbles: true }));

        // Usar un pequeño retraso para permitir que el motor de Chirpy renderice los resultados
        setTimeout(() => {
          if (query.length > 0) {
            // Reflejar los resultados encontrados en el panel de búsqueda superior
            const resultsContent = topSearchResults.querySelector('.content');
            if (resultsContent) {
              glossaryResults.innerHTML = resultsContent.innerHTML;
            }
          } else {
            glossaryResults.innerHTML = '';
          }
        }, 100);
      });

      // Manejar la tecla 'Enter' para seguir el primer resultado
      glossaryInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
          const firstResult = glossaryResults.querySelector('a');
          if (firstResult) firstResult.click();
        }
      });
    }
  });
</script>
