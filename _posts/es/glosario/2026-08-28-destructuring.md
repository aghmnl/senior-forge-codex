---
layout: post
title: "Destructuring"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/destructuring/
---

## The Theory (El Qué)

**Destructuring** en Kotlin permite desempaquetar las propiedades de un objeto en variables separadas en una sola declaración. Funciona a través de funciones operador `componentN()`: `component1()` se mapea a la primera variable, `component2()` a la segunda, y así sucesivamente. Las data classes generan estas funciones automáticamente para las propiedades de su [constructor primario]({{ "/es/glosario/primary-constructor/" | relative_url }}).

```kotlin
// De FollowApp Suite — TaskConfirmationDialogs.kt
val (titleRes, messageRes) = when (action) {
    is BulkAction.Complete -> R.string.bulk_complete_title to R.string.bulk_complete_message
    is BulkAction.Archive -> R.string.bulk_archive_title to R.string.bulk_archive_message
    is BulkAction.Delete -> R.string.bulk_delete_title to R.string.bulk_delete_message
}
```

## The Senior Nuance (El Matiz Senior)

- El destructuring enlaza por *posición*, no por nombre. Si el orden de las propiedades del [constructor primario]({{ "/es/glosario/primary-constructor/" | relative_url }}) cambia, todos los sitios de destructuring silenciosamente se enlazan a valores diferentes — sin error de compilación. Esto es un riesgo de refactoring en codebases grandes.
- Usá `_` para saltear componentes que no necesitás: `val (_, second) = pair`. Es más limpio que introducir una variable no utilizada y evita warnings de lint.
- El destructuring funciona en [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) también: `.map { (key, value) -> ... }` es más legible que `.map { entry -> entry.key ... }` cuando se iteran [maps]({{ "/es/glosario/maps/" | relative_url }}). Pero evitá destructuring profundamente anidado — se vuelve ilegible rápido.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
