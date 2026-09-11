---
layout: post
title: "toMutableList"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
tags: [collections, immutability]
lang: es
permalink: /es/glosario/to-mutable-list/
---

## The Theory (El Qué)

**`toMutableList()`** devuelve un [`MutableList`]({{ "/es/glosario/mutable-list/" | relative_url }}) nuevo — un [`ArrayList`]({{ "/es/glosario/arraylist/" | relative_url }}) — con los elementos del receiver. Es la [Defensive Copy]({{ "/es/glosario/defensive-copy/" | relative_url }}) *de entrada*: copiás precisamente porque vas a [mutar]({{ "/es/glosario/mutation/" | relative_url }}) y no debés tocar el original.

```kotlin
// De FollowApp Suite — TasksScreen.kt
val source = localGroups[originIdx].tasks.toMutableList()
val target = localGroups[targetIdx].tasks.toMutableList()
```

## The Senior Nuance (El Matiz Senior)

- Usarlo es una señal para revisar la propiedad del dato. Acá el `tasks` del grupo es un [`List`]({{ "/es/glosario/list/" | relative_url }}) de solo lectura propiedad de un objeto de estado, así que un drag entre grupos copia, edita las copias y publica grupos nuevos — nunca se escribe sobre el objeto de estado.
- `LabelsListViewModel` usa la misma forma para reordenar opciones de escala: copiar, `add`/`removeAt`, y emitir un estado nuevo. La lista mutable vive dentro de un solo [Stack Frame]({{ "/es/glosario/stack-frame/" | relative_url }}) y nunca se guarda.
- Siempre copia, incluso si el receiver ya es mutable — ese es el punto, pero también significa que llamarlo dentro de un loop sobre `n` grupos son `n` copias de array. Copiá una vez, afuera.

**Documentación oficial:** [`kotlin.collections.toMutableList`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/to-mutable-list.html)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
