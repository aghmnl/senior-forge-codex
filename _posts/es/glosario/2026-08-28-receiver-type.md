---
layout: post
title: "Receiver Type"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/receiver-type/
---

## The Theory (El Qué)

Un **receiver type** (tipo receptor) es el tipo sobre el que opera una [extension function]({{ "/es/glosario/extension-functions/" | relative_url }}) o una [lambda con receptor]({{ "/es/glosario/lambda-with-receiver/" | relative_url }}). En `fun String.isPalindrome()`, `String` es el receiver type — dentro del cuerpo de la función, `this` se refiere a la instancia de `String`. Kotlin también soporta [lambda with receiver]({{ "/es/glosario/lambda-with-receiver/" | relative_url }}) (`T.() -> R`), donde el cuerpo de la lambda se ejecuta en el [scope]({{ "/es/glosario/scope/" | relative_url }}) del receptor, habilitando APIs estilo [DSL]({{ "/es/glosario/dsl/" | relative_url }}).

```kotlin
// De FollowApp Suite — BackupSerializer.kt
private fun JSONObject.optStringOrNull(key: String): String? =
    if (isNull(key)) null else getString(key)

private fun JSONObject.optLongOrNull(key: String): Long? =
    if (isNull(key)) null else getLong(key)
```

```kotlin
// De FollowApp Suite — FollowAppLoadingGear.kt
private fun DrawScope.drawLoadingGear(colors: List<Color>, rotationDeg: Float) {
    // 'this' es el DrawScope — acceso directo a drawArc, drawCircle, etc.
}
```

## The Senior Nuance (El Matiz Senior)

- El receiver type determina qué `this` está disponible dentro del cuerpo de la función. Cuando se anidan múltiples [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) con receptor (ej. `Column { Row { ... } }` en Compose), el receptor más interno oculta los exteriores. Usá [`this@label`]({{ "/es/glosario/this-at-label/" | relative_url }}) para desambiguar, o aplicá [`@DslMarker`]({{ "/es/glosario/dsl-marker/" | relative_url }}) para prevenir acceso accidental a [scopes]({{ "/es/glosario/scope/" | relative_url }}) exteriores.
- Las [extension functions]({{ "/es/glosario/extension-functions/" | relative_url }}) se resuelven [estáticamente]({{ "/es/glosario/static-dispatch/" | relative_url }}) basándose en el tipo de receptor *declarado*, no en el tipo en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}). Si declarás `fun Animal.sound()` y `fun Dog.sound()`, llamar a `sound()` en una variable tipada como `Animal` siempre llama a la versión de `Animal` — aunque el objeto real sea un `Dog`. Esto es lo opuesto al [polimorfismo]({{ "/es/glosario/polymorphism/" | relative_url }}) vía dispatch virtual.
- El patrón `ColumnScope.() -> Unit` en Compose es una [lambda con receptor]({{ "/es/glosario/lambda-with-receiver/" | relative_url }}) que restringe qué composables están disponibles dentro de un `Column`: podés llamar a `Modifier.weight()` solo porque `ColumnScope` es el receptor. Es una restricción de [compile time]({{ "/es/glosario/compile-time/" | relative_url }}) impuesta por [`@LayoutScopeMarker`]({{ "/es/glosario/layout-scope-marker/" | relative_url }}), no un chequeo en runtime.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
