---
layout: post
title: "is Operator"
date: 2026-09-18 12:00:00 +0000
categories: [es, glosario]
tags: [type-system, syntax, sealed-types]
lang: es
permalink: /es/glosario/is-operator/
---

## The Theory (El Qué)

**`is`** es el operador de verificación de tipo de Kotlin: `x is Foo` devuelve `true` cuando `x` es una instancia de `Foo` (o de un subtipo), y `!is` lo niega. Reemplaza al `instanceof` de Java con una diferencia decisiva: después de una verificación positiva, el compilador aplica un smart cast ([Smart Casts]({{ "/es/01-kotlin-core/smart-casts/" | relative_url }})), así que `x` puede usarse como `Foo` dentro de la rama sin [cast]({{ "/es/glosario/cast/" | relative_url }}) explícito. En una [expresión `when`]({{ "/es/glosario/when-expression/" | relative_url }}) sobre una [jerarquía sellada]({{ "/es/glosario/sealed-hierarchy/" | relative_url }}), las ramas `is` funcionan además como verificación de [exhaustividad]({{ "/es/glosario/exhaustiveness/" | relative_url }}).

```kotlin
// De FollowApp Suite — CleanUpPresetsUseCase.kt
// Después del chequeo, `filter` es un ScaleFilterState.Include: `filter.values` no necesita cast
if (filter is ScaleFilterState.Include && oldValue in filter.values) {
    val updatedValues = filter.values - oldValue + newValue
}
```

## The Senior Nuance (El Matiz Senior)

- **El chequeo es solo la mitad de la feature.** `is` sin el smart cast que lo sigue es apenas `instanceof`; el valor está en lo que el compilador te deja hacer después. Eso solo funciona cuando el valor chequeado es estable — una variable local o un [`val`]({{ "/es/glosario/val/" | relative_url }}) sin [getter]({{ "/es/glosario/getter/" | relative_url }}) custom. Sobre una propiedad [`var`]({{ "/es/glosario/var/" | relative_url }}) el chequeo compila pero el smart cast no.
- **`is` dentro de `when` es exhaustivo sobre tipos sellados.** Agregar un subtipo rompe cada `when` que no lo cubra; por eso las ramas `is` son la columna vertebral del manejo type-safe del estado de UI.
- **Preferí `is` a `as?` cuando ya estás ramificando.** `if (x is Foo)` te da un `Foo` no-nulo dentro de la rama; `(x as? Foo)?.bar` te da un nullable. `is` para control de flujo, [`as?`]({{ "/es/glosario/as-safe-cast/" | relative_url }}) para expresiones.
- Ver [Smart Casts]({{ "/es/01-kotlin-core/smart-casts/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
