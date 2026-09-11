---
layout: post
title: "Builder Functions"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
tags: [collections, immutability, lambdas]
lang: es
permalink: /es/glosario/builder-functions/
---

## The Theory (El Qué)

Las **Builder Functions** — `buildList {}`, `buildSet {}`, `buildMap {}`, `buildString {}` — son [Inline Functions]({{ "/es/glosario/inline-functions/" | relative_url }}) de la [Standard Library]({{ "/es/glosario/standard-library/" | relative_url }}) que te dan un receiver mutable dentro de una [Lambda with Receiver]({{ "/es/glosario/lambda-with-receiver/" | relative_url }}) y devuelven el supertipo de solo lectura.

```kotlin
// De FollowApp Suite — LabelsListScreen.kt
val actions = buildList {
    add(ToolbarAction(icon = UiIcons.Delete, /* ... */))
    if (allTags) {
        add(ToolbarAction(icon = UiIcons.ConvertToScale, /* ... */))
    }
}
```

## The Senior Nuance (El Matiz Senior)

- Codifican la regla "mutá localmente, publicá [inmutable]({{ "/es/glosario/immutability/" | relative_url }})" en el sistema de tipos: el receiver `MutableList` existe solo dentro de la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}), así que no puede escapar como una [Read-Only View]({{ "/es/glosario/read-only-view/" | relative_url }}) sobre estado vivo. Después de que el builder retorna, la colección queda congelada — escribir en una referencia capturada lanza `UnsupportedOperationException`.
- Son la respuesta correcta cuando la construcción es condicional. Una cadena de `listOfNotNull` más `takeIf` se lee peor que tres `add` guardados por `if`, y asigna más.
- `buildList(capacity)` predimensiona el array de respaldo, lo que importa en [Hot Loops]({{ "/es/glosario/hot-loops/" | relative_url }}) donde el crecimiento repetido copiaría. Al ser [`inline`]({{ "/es/glosario/inline-functions/" | relative_url }}), no hay [Overhead]({{ "/es/glosario/overhead/" | relative_url }}) por la lambda en sí.

**Documentación oficial:** [`buildList`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/build-list.html) · [`buildMap`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/build-map.html)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
