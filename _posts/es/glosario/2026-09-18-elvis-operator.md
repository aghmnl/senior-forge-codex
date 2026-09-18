---
layout: post
title: "?: (Elvis Operator)"
date: 2026-09-18 12:00:00 +0000
categories: [es, glosario]
tags: [null-safety, syntax]
lang: es
permalink: /es/glosario/elvis-operator/
---

## The Theory (El Qué)

**`?:`** — el operador Elvis — evalúa a su operando izquierdo cuando este no es [`null`]({{ "/es/glosario/null/" | relative_url }}), y al derecho en caso contrario: `a ?: b`. El lado derecho puede ser cualquier expresión, incluyendo [`throw`]({{ "/es/glosario/throw/" | relative_url }}), `return`, `continue` o `break`, porque esas tienen tipo `Nothing` y colapsan el resultado al tipo no-nulo. Es el segundo operador central de [Null Safety: Elvis & Safe Calls]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}), normalmente encadenado después de un [safe call]({{ "/es/glosario/safe-call/" | relative_url }}): `user?.name ?: "Anónimo"`. El nombre viene de que el emoticón `?:` parece el peinado de Elvis Presley.

```kotlin
// De FollowApp Suite — PresetRepositoryImpl
// Elvis como default: fallback seguro en producción
fun resolvePosition(existing: Preset?): Int {
    return existing?.position ?: dao.nextPosition()
}

// De FollowApp Suite — BillingConnector
// Elvis como guard clause: sale de la función cuando es null
val details = productDetails ?: return false
```

## The Senior Nuance (El Matiz Senior)

- **Tres idiomas, un operador.** Valor por defecto (`?: 0`), salida temprana ([`?: return`]({{ "/es/glosario/elvis-return/" | relative_url }})) y falla con nombre (`?: throw `[`IllegalStateException`]({{ "/es/glosario/illegal-state-exception/" | relative_url }})`(...)`). Cada uno reemplaza un `!!` por una decisión explícita sobre qué significa null acá.
- **El lado derecho se evalúa de forma lazy.** `cache ?: load()` solo llama a `load()` cuando falta, así que Elvis sirve también como patrón barato de memoización.
- **Ojo con `?.let { } ?: else`.** Si el bloque de `let` devuelve null, la rama del Elvis también corre. Usá `if/else` cuando el resultado del bloque puede ser null.
- Ver [Null Safety: Elvis & Safe Calls]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
