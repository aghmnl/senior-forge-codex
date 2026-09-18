---
layout: post
title: "as? (Safe Cast)"
date: 2026-09-18 12:00:00 +0000
categories: [es, glosario]
tags: [type-system, null-safety]
lang: es
permalink: /es/glosario/as-safe-cast/
---

## The Theory (El Qué)

**`as?`** es el operador de [cast]({{ "/es/glosario/cast/" | relative_url }}) *seguro*: `x as? Foo` devuelve `x` tipado como `Foo?` cuando el cast funciona y `null` cuando no — nunca lanza [`ClassCastException`]({{ "/es/glosario/class-cast-exception/" | relative_url }}). El resultado es nullable por diseño, así que se compone con el [safe call]({{ "/es/glosario/safe-call/" | relative_url }}) `?.` y el operador Elvis `?:` en expresiones de una línea: `(value as? Long)?.toInt() ?: 0`. Es el fallback que prescribe el artículo de [Smart Casts]({{ "/es/01-kotlin-core/smart-casts/" | relative_url }}) cuando el smart cast no está disponible y el tipo es legítimamente incierto.

```kotlin
// De FollowApp Suite — TasksViewModel.kt
// as? devuelve null si el LabelValue es Scale (no Tag); ?. y ?: manejan el null
val taskLabels = (task.customLabels["labels"] as? LabelValue.Tag)
    ?.values?.toSet() ?: emptySet()

// De FollowApp Suite — RecurrenceCalculator.kt
val until = (rule.end as? RecurrenceEnd.UntilDate)?.date
```

## The Senior Nuance (El Matiz Senior)

- **`as?` convierte una pregunta de tipo en una pregunta de null.** Esa es su fuerza — Kotlin tiene excelentes herramientas para nulls — y su trampa: ahora el null necesita una decisión (`?:` default, early return, `let`). Un `as?` pelado cuyo resultado después recibe un `!!` es peor que el [`as`]({{ "/es/glosario/as-cast/" | relative_url }}) que reemplazó.
- **Expresión vs. control de flujo.** `as?` brilla dentro de expresiones (`?.let`, `?:`, mapeos); cuando ya estás ramificando, `if (x is Foo)` da un `Foo` no-nulo y se lee mejor que `(x as? Foo)?.let { }`.
- **Un null de `as?` puede esconder un bug.** Si un valor *siempre* debería ser de ese tipo, `as?` devuelve null en silencio y la falla aparece lejos. Usá `as` (o `check(x is Foo)`) cuando un tipo incorrecto es un error de programación.
- Ver [Smart Casts]({{ "/es/01-kotlin-core/smart-casts/" | relative_url }}) y [Null Safety]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
