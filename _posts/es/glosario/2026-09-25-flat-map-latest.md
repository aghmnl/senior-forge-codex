---
layout: post
title: "flatMapLatest"
date: 2026-09-25 12:00:00 +0000
categories: [es, glosario]
tags: [flow, cancellation, coroutines]
lang: es
permalink: /es/glosario/flat-map-latest/
---

## The Theory (El Qué)

**`flatMapLatest`** es un operador de [Flow]({{ "/es/glosario/flow/" | relative_url }}) que mapea cada valor del [upstream]({{ "/es/glosario/upstream/" | relative_url }}) a un flow interno nuevo y **colecta solo el más reciente**: cuando llega un valor nuevo, el flow interno del valor anterior se cancela y se reemplaza. Es la herramienta para "la query depende de parámetros que cambian": cada juego de parámetros nuevo cancela la query anterior y arranca una nueva. Está marcado como `@ExperimentalCoroutinesApi`.

```kotlin
// De FollowApp Suite — TasksViewModel.kt
// Cada QueryParams distinto cancela la query anterior a la base de datos
// y arranca una nueva con el orden y los filtros nuevos
@OptIn(ExperimentalCoroutinesApi::class)
private fun observeTasks() {
    viewModelScope.launch {
        _restored
            .filter { it }
            .flatMapLatest { _queryParams }
            .flatMapLatest { params ->
                if (params.query.isNotEmpty()) {
                    searchTasksUseCase(query = params.query, statuses = params.filters, sort = params.sort)
                } else {
                    getActiveTasksUseCase(params.sort)
                }
            }
            .collect { /* ... */ }
    }
}
```

## The Senior Nuance (El Matiz Senior)

- **Latest vs concat vs merge.** `flatMapLatest` cancela el flow interno viejo; `flatMapConcat` espera a que termine antes de arrancar el siguiente; `flatMapMerge` los corre en paralelo. Para un buscador, solo *latest* es correcto: los resultados de una query vieja nunca deben llegar después de los de la nueva.
- **La cancelación es la gracia.** El flow interno anterior se cancela mediante [cancelación cooperativa]({{ "/es/glosario/cooperative-cancellation/" | relative_url }}), así que el trabajo de adentro tiene que ser cancelable para que el ahorro sea real.
- **Encaja naturalmente con un [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) de parámetros.** Como un `StateFlow` descarta las escrituras iguales, asignar los mismos filtros dos veces no reinicia la query.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
