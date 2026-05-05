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

  <div class="w-100" style="max-width: 500px;">
    <div class="input-group input-group-lg shadow-sm">
      <span class="input-group-text bg-transparent border-end-0">
        <i class="fas fa-search text-muted"></i>
      </span>
      <input type="text" id="glossary-search" class="form-control border-start-0" placeholder="Buscar términos (ej. Corrutinas, Mutex...)" aria-label="Buscar términos del glosario">
    </div>
  </div>
</div>

<div id="glossary-list" class="mt-5">
  <!-- Esta sección puede usarse para listar categorías o términos comunes si es necesario -->
</div>

<script>
  // Conectar la búsqueda del glosario con la búsqueda principal para una experiencia unificada
  document.getElementById('glossary-search').addEventListener('input', function(e) {
    const topSearch = document.getElementById('search-input');
    if (topSearch) {
      topSearch.value = e.target.value;
      // Disparar el evento de entrada para invocar el motor de búsqueda de Chirpy
      topSearch.dispatchEvent(new Event('input', { bubbles: true }));
      
      // Enfocar la búsqueda superior para mostrar el dropdown de resultados
      if (e.target.value.length > 0) {
        document.getElementById('search-trigger').click();
        topSearch.focus();
      }
    }
  });
</script>
