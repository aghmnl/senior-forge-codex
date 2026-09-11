---
layout: post
title: "Race Condition"
date: 2026-09-09 12:00:00 +0000
categories: [es, glosario]
tags: [concurrency, state-management, coroutines]
lang: es
permalink: /es/glosario/race-condition/
---

## The Theory (El Qué)

Una **Race Condition** (condición de carrera) es un defecto donde la corrección del programa depende del timing relativo de dos operaciones concurrentes. La forma más común es la secuencia *check-then-act* o *read-modify-write*: un thread lee estado compartido, calcula algo a partir de él y lo escribe de vuelta — mientras otro thread ya cambió ese estado en el medio.

```kotlin
// Dos coroutines activando filtros distintos al mismo tiempo
// Thread A: lee el state (filters = {}), calcula {dueToday}
// Thread B: lee el state (filters = {}), calcula {starred}
// A escribe {dueToday}. B escribe {starred}. El filtro de A desapareció en silencio.
_uiState.value = _uiState.value.copy(filters = _uiState.value.filters + newFilter)
```

## The Senior Nuance (El Matiz Senior)

- Las races en estado de UI rara vez crashean — **pierden updates**, que es peor. La pantalla renderiza un estado plausible que simplemente omite una de las acciones del usuario, así que el bug se reporta como "a veces el filtro no me queda" y no se reproduce en un dispositivo rápido.
- En Android el consuelo falso es "todo corre en el main thread". No es así: `viewModelScope.launch(Dispatchers.IO)`, `flowOn`, un `collect` en un dispatcher de background y un callback de repositorio escriben estado fuera de Main. Y aun en `Main.immediate`, una llamada `suspend` dentro de un read-modify-write introduce un punto de suspensión donde otra coroutine puede intercalarse.
- La solución no es un lock; es hacer [atómico]({{ "/es/glosario/atomicity/" | relative_url }}) todo el read-modify-write con [`update`]({{ "/es/glosario/update/" | relative_url }}), sobre estado [inmutable]({{ "/es/glosario/immutability/" | relative_url }}). La detección también importa: las races son invisibles a los tests normales, así que ejercitá updates concurrentes de forma explícita en vez de confiar en un test dispatcher de un solo thread.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
