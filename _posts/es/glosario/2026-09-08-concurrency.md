---
layout: post
title: "Concurrency"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
tags: [concurrency, immutability, coroutines]
lang: es
permalink: /es/glosario/concurrency/
---

## The Theory (El Qué)

La **Concurrencia** es que múltiples flujos de ejecución progresen durante el mismo período, intercalándose en un thread o corriendo en paralelo en varios. En Android eso significa el main thread más las [Coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) que corran en `Dispatchers.IO`/`Default` — y todo el estado alcanzable desde más de uno de ellos.

```kotlin
// De FollowApp Suite — TasksViewModel.kt
// El estado se reemplaza, nunca se muta in-place: seguro ante updates concurrentes
_uiState.update { it.copy(selectedTaskIds = setOf(taskId)) }
```

## The Senior Nuance (El Matiz Senior)

- La Concurrencia es lo que hace que la [mutabilidad]({{ "/es/glosario/mutation/" | relative_url }}) sea peligrosa y no meramente desprolija. Un [`MutableList`]({{ "/es/glosario/mutable-list/" | relative_url }}) leído por una coroutine mientras otra lo escribe lanza `ConcurrentModificationException` en el mejor caso, y renderiza datos obsoletos en silencio en el peor.
- La [Inmutabilidad]({{ "/es/glosario/immutability/" | relative_url }}) es la respuesta más barata: un valor que nadie puede cambiar no necesita [Synchronized Block]({{ "/es/glosario/synchronized-block/" | relative_url }}) ni orden de locks. `MutableStateFlow.update { }` compone un read-modify-write atómico a partir de valores inmutables, y por eso reemplaza el objeto de estado en vez de editarlo.
- La segunda respuesta es el confinamiento: mantené el objeto mutable dentro de un solo [Stack Frame]({{ "/es/glosario/stack-frame/" | relative_url }}), o en un solo thread. La mayoría de las conclusiones del tipo "acá necesitamos un lock" son en realidad un objeto mutable que escapó de una función de la que nunca debió salir.
- Concurrencia no es paralelismo. Las coroutines intercalan trabajo suspendible en un solo thread sin problema — los riesgos sobre el estado son idénticos, porque un punto de suspensión es exactamente donde otra coroutine puede observar tu [mutación]({{ "/es/glosario/mutation/" | relative_url }}) a medio hacer.

**Documentación oficial:** [Coroutines guide](https://kotlinlang.org/docs/coroutines-guide.html) · [Shared mutable state and concurrency](https://kotlinlang.org/docs/shared-mutable-state-and-concurrency.html)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
