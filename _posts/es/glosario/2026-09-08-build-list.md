---
layout: post
title: "buildList"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/build-list/
---

## The Theory (El Qué)

**`buildList { }`** es una [Builder Function]({{ "/es/glosario/builder-functions/" | relative_url }}) [inline]({{ "/es/glosario/inline-functions/" | relative_url }}) que te da un [`MutableList`]({{ "/es/glosario/mutable-list/" | relative_url }}) como receiver de la [lambda]({{ "/es/glosario/lambda-with-receiver/" | relative_url }}) y devuelve un [`List`]({{ "/es/glosario/list/" | relative_url }}) de solo lectura. Codifica "mutá localmente, publicá inmutable" en una sola expresión.

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

- La construcción condicional es donde gana. La alternativa — `listOfNotNull` más `takeIf`, o una cadena de `+` que reasigna en cada paso — se lee peor y asigna más.
- Después de que la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) retorna, la lista queda congelada: escribir a través de una referencia capturada adentro lanza `UnsupportedOperationException`. Eso es lo que la hace más fuerte que un `mutableListOf` artesanal devuelto como `List`, que es apenas una [Read-Only View]({{ "/es/glosario/read-only-view/" | relative_url }}).
- `buildList(capacity) { }` predimensiona el [`ArrayList`]({{ "/es/glosario/arraylist/" | relative_url }}) de respaldo. Al ser [`inline`]({{ "/es/glosario/inline-functions/" | relative_url }}), el builder en sí no agrega [Overhead]({{ "/es/glosario/overhead/" | relative_url }}) — no se asigna ningún objeto lambda.

**Documentación oficial:** [`kotlin.collections.buildList`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/build-list.html)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
