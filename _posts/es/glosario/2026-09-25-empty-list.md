---
layout: post
title: "emptyList"
date: 2026-09-25 12:00:00 +0000
categories: [es, glosario]
tags: [collections, immutability, memory]
lang: es
permalink: /es/glosario/empty-list/
---

## The Theory (El Qué)

**`emptyList<T>()`** es la función de la [standard library]({{ "/es/glosario/standard-library/" | relative_url }}) que devuelve una **[List]({{ "/es/glosario/list/" | relative_url }}) vacía de solo lectura**. No reserva memoria: cada llamada devuelve el mismo objeto singleton interno, sea cual sea el tipo. `listOf()` sin argumentos devuelve lo mismo. Cuando el tipo no se puede inferir hay que indicarlo: `emptyList<Task>()`.

```kotlin
// De FollowApp Suite — TasksViewModel.kt
// Una lista vacía tipada como valor inicial de un StateFlow
private val _selectedLabels = MutableStateFlow<List<String>>(emptyList())
```

## The Senior Nuance (El Matiz Senior)

- **Vacío es un valor, no una ausencia.** Como valor inicial de un [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}), `emptyList()` dice "no hay ítems", lo cual es mentira mientras los datos todavía se están cargando. "Todavía no cargó" necesita su propia representación: un flag `isLoading`, un estado `Loading` o `null`.
- **La igualdad es estructural.** `emptyList<Int>() == ArrayList<Int>()` es `true`, porque la [igualdad]({{ "/es/glosario/equals/" | relative_url }}) de listas compara contenido. Reemplazar una lista vacía por otra no hace emitir a un `StateFlow`.
- **De solo lectura, no mutable.** Castearla a `MutableList` y llamar a [add]({{ "/es/glosario/add/" | relative_url }}) lanza `UnsupportedOperationException`. Usá [mutableListOf()]({{ "/es/glosario/mutable-list/" | relative_url }}) cuando la lista tiene que crecer.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
