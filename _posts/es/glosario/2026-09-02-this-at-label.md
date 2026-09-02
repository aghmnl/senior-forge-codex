---
layout: post
title: "this@label"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/this-at-label/
---

## The Theory (El Qué)

**`this@label`** es la sintaxis de `this` cualificado de Kotlin para desambiguar a qué [receiver]({{ "/es/glosario/receiver-type/" | relative_url }}) te referís cuando hay múltiples receivers en [scope]({{ "/es/glosario/scope/" | relative_url }}). Cuando las [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) con receivers están anidadas — algo común en [DSLs]({{ "/es/glosario/dsl/" | relative_url }}) como [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) — el receiver más interno oculta a los exteriores. Escribir `this@outerLabel` selecciona explícitamente el receiver externo.

El label es el nombre de la función o clase que introdujo el receiver. Para una [extension function]({{ "/es/glosario/extension-functions/" | relative_url }}) como `drawWithContent {}`, el label es `drawWithContent`. Para un método de clase, el label es el nombre de la clase.

```kotlin
// From FollowApp Suite — AnimatedSearchBar.kt
.drawWithContent {
    val reveal = size.width * searchFraction
    clipRect(
        left = size.width - reveal,
        top = 0f,
        right = size.width,
        bottom = size.height
    ) {
        // Dentro de clipRect {}, 'this' es ClipScope.
        // Necesitamos llamar a drawContent() del DrawScope exterior.
        this@drawWithContent.drawContent()
    }
}
```

Sin `this@drawWithContent`, el compilador buscaría `drawContent()` en el receiver `ClipScope` (la lambda más interna) y fallaría — `drawContent()` pertenece al `ContentDrawScope` exterior.

## The Senior Nuance (El Matiz Senior)

- **Cuándo usarlo**: Siempre que anides [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) con diferentes [receiver types]({{ "/es/glosario/receiver-type/" | relative_url }}) y necesites un método de una capa exterior. Es común en las APIs de dibujo de Compose (`drawWithContent`, `drawBehind` + `clipRect`), scoping de Canvas, y [DSLs]({{ "/es/glosario/dsl/" | relative_url }}) personalizados.
- **Relación con `@DslMarker`**: [`@DslMarker`]({{ "/es/glosario/dsl-marker/" | relative_url }}) previene el acceso *implícito* a receivers exteriores — el compilador te fuerza a escribir `this@label` explícitamente si realmente lo necesitás. Sin `@DslMarker`, el receiver exterior es accesible silenciosamente, lo que provoca bugs sutiles en [DSLs]({{ "/es/glosario/dsl/" | relative_url }}) anidados.
- **Non-local returns**: En un contexto de lambdas anidadas, `return@label` usa el mismo mecanismo de labels pero para control de flujo en lugar de desambiguación de receivers. Ambas features comparten la convención de labeling, pero `this@label` selecciona un receiver mientras que `return@label` sale de una lambda específica.
- **Regla de legibilidad**: Si te encontrás escribiendo `this@label` frecuentemente, el anidamiento es demasiado profundo. Extraé el bloque interno a una función con nombre para aplanar la pila de receivers.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
