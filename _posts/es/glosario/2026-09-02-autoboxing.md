---
layout: post
title: "Autoboxing"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/autoboxing/
---

## The Theory (El Qué)

**Autoboxing** es la conversión automática entre un tipo [primitivo]({{ "/es/glosario/primitives/" | relative_url }}) (`int`, `long`, `boolean`) y su correspondiente clase wrapper (`Integer`, `Long`, `Boolean`) realizada por la [JVM]({{ "/es/glosario/jvm/" | relative_url }}). En Kotlin, esto sucede transparentemente cuando un primitivo se usa en un contexto genérico — porque el [type erasure]({{ "/es/glosario/type-erasure/" | relative_url }}) fuerza a todos los parámetros genéricos a ser objetos en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
val primitive: Int = 42           // Kotlin Int → JVM int (sin objeto, sin heap)
val boxed: Int? = 42              // nullable fuerza boxing: JVM Integer en el heap
val list: List<Int> = listOf(1, 2, 3)  // cada elemento boxeado a Integer — 3 allocations en heap
```

Lo inverso — **unboxing** — extrae el valor primitivo de un objeto wrapper. Ambos ocurren implícitamente y tienen un costo: cada boxing [asigna]({{ "/es/glosario/allocations/" | relative_url }}) un objeto en el [heap]({{ "/es/glosario/heap/" | relative_url }}), y cada unboxing desreferencia un puntero.

## The Senior Nuance (El Matiz Senior)

- En Kotlin, `Int` compila a `int` de la JVM cuando se usa como local o parámetro no-nullable. En el momento que se vuelve nullable (`Int?`), genérico (`List<Int>`), o se pasa a una función que espera `Any`, el compilador lo boxea a `java.lang.Integer`. Entender estos triggers es esencial para código crítico en performance.
- [`IntArray`]({{ "/es/glosario/intarray/" | relative_url }}), `LongArray`, `FloatArray`, etc., son el escape hatch de Kotlin: compilan a arrays primitivos de la JVM (`int[]`, `long[]`, `float[]`) con cero boxing por elemento. Usalos sobre `Array<Int>` o `List<Int>` en loops intensivos o colecciones grandes.
- Las [inline classes]({{ "/es/01-kotlin-core/value-classes/" | relative_url }}) (`@JvmInline value class`) wrappean un primitivo sin boxing en la mayoría de los casos — el wrapper se borra en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}). Solo se boxean cuando se usan como tipo genérico o nullable.
- El autoboxing es la razón por la que las comparaciones de identidad (`===`) en valores boxeados son peligrosas: `val a: Int? = 128; val b: Int? = 128; a === b` es `false` porque el cache de `Integer` de la JVM solo cubre -128 a 127. Usá `==` para igualdad de valor.
- En código de UI Android, el autoboxing dentro de `onDraw()`, `onMeasure()`, o lambdas de recomposición de Compose crea churn del GC que causa drops de frames. El [Garbage Collector]({{ "/es/glosario/garbage-collector/" | relative_url }}) reclama estos boxes de corta vida, pero el costo de las pausas se acumula.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
