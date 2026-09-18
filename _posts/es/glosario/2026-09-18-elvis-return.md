---
layout: post
title: "?: return (Elvis Early Return)"
date: 2026-09-18 12:00:00 +0000
categories: [es, glosario]
tags: [null-safety, design-principles, syntax]
lang: es
permalink: /es/glosario/elvis-return/
---

## The Theory (El Qué)

**`?: return`** es el [operador Elvis]({{ "/es/glosario/elvis-operator/" | relative_url }}) con `return` como lado derecho: `val x = nullable ?: return`. Como `return` tiene tipo `Nothing`, el tipo de la expresión colapsa al `T` no-nulo, y la función sale inmediatamente cuando el valor es [`null`]({{ "/es/glosario/null/" | relative_url }}). Es la [guard clause]({{ "/es/glosario/guard-clause/" | relative_url }}) idiomática de Kotlin — elimina la nullabilidad del resto del [scope]({{ "/es/glosario/scope/" | relative_url }}) de la función en una línea, mantiene el camino feliz plano, y es la primera alternativa que [Null Safety: Elvis & Safe Calls]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}) da al `!!`. La misma forma funciona con `?: continue`, `?: break` y `?: throw`.

```kotlin
// De FollowApp Suite — BillingConnector
// Guard clause con Elvis: elimina null del resto del scope
fun launchPurchase(activity: Activity): Boolean {
    val details = productDetails ?: return false
    // details: ProductDetails (no-nulo) de acá en adelante
    ...
}

// De FollowApp Suite — TasksViewModel
fun onCascadeConfirmed() {
    val action = _uiState.value.pendingCascadeAction ?: return
    ...
}
```

## The Senior Nuance (El Matiz Senior)

- **Cambia el tipo, no solo el flujo.** Después de `val details = productDetails ?: return false`, `details` es `ProductDetails`, no `ProductDetails?`; cada línea posterior queda libre de `?.`. Esa es la diferencia entre una guard clause y un `if (x == null) return` que deja a `x` nullable.
- **Ponelo arriba.** Las guard clauses van en las primeras líneas de la función para que quien lee conozca las precondiciones antes que la lógica. Un `?: return` enterrado a mitad de función es una salida escondida.
- **Devolvé un valor con significado.** `?: return false`, `?: return emptyList()`, `?: return@launch`: el valor (o el label) documenta qué significa "nada que hacer" para esta función.
- Ver [Null Safety: Elvis & Safe Calls]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
