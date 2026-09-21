---
layout: post
title: "=== (Referential Equality)"
date: 2026-09-21 12:00:00 +0000
categories: [es, glosario]
tags: [type-system, jvm, syntax]
lang: es
permalink: /es/glosario/referential-equality/
---

## The Theory (El Qué)

**`===`** es la igualdad referencial: es `true` solo cuando ambos operandos apuntan a la *misma instancia*, y no se puede sobreescribir nunca. Es la contraparte de [`==`]({{ "/es/glosario/structural-equality/" | relative_url }}), que pregunta por equivalencia. Para un [`data object`]({{ "/es/glosario/data-object/" | relative_url }}) las dos siempre coinciden, porque hay exactamente una instancia; para una [Data Classes: copy, equals, toString]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}) con contenidos idénticos no coinciden — `==` da `true`, `===` da `false`. `!==` es su negación.

```kotlin
// Not found in FAS — standalone example
data class Loading0()            // una clase: instancia nueva cada vez
Loading0() == Loading0()         // true  — equals sobre cero propiedades
Loading0() === Loading0()        // false — dos allocations

data object Loading1             // un singleton
val x: Any = Loading1
x === Loading1                   // true  — y == coincide
```

## The Senior Nuance (El Matiz Senior)

- **Usalo para probar identidad, no equivalencia.** Verificar que se reusó una instancia cacheada, que [`copy()`]({{ "/es/glosario/copy/" | relative_url }}) no copió, o que un singleton es realmente uno: esas son preguntas de `===`. Todo lo demás es `==`.
- **Es la razón por la que una `data class` sin estado es la herramienta equivocada.** `data class Loading()` te da `==` true pero `===` false más una [allocation]({{ "/es/glosario/allocations/" | relative_url }}) por uso; un `data object` te da las dos y cero allocations.
- **Compose también lee identidad.** Saltear recomposiciones se apoya en comparar instancias para los tipos inestables, así que crear instancias nuevas gratuitas del "mismo" estado lo anula.
- Ver [Data Objects: Singleton & Memory Savings]({{ "/es/01-kotlin-core/data-objects/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
