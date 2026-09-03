---
layout: post
title: "Allocations"
date: 2026-08-30 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/allocations/
---

## The Theory (El Qué)

Una **allocation** (asignación de memoria) es el acto de reservar memoria en el [heap]({{ "/es/glosario/heap/" | relative_url }}) para una nueva instancia de objeto. Cada vez que llamás a un [constructor]({{ "/es/glosario/constructor/" | relative_url }}) (`MyClass()`), creás un [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) que captura variables, o hacés boxing de un [primitivo]({{ "/es/glosario/primitives/" | relative_url }}), la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) asigna memoria para ese objeto. El [Garbage Collector]({{ "/es/glosario/garbage-collector/" | relative_url }}) reclama esa memoria cuando el objeto deja de estar referenciado. Aunque las allocations individuales son rápidas (un pointer bump en la generación joven), las allocations de alta frecuencia incrementan la presión del GC, causando pausas que afectan la fluidez de la UI — especialmente en Android, donde el presupuesto por frame es de 16ms.

```kotlin
// De FollowApp Suite — RecurrenceRule.kt
// data object Never: CERO allocations — es un singleton
sealed class RecurrenceEnd {
    data object Never : RecurrenceEnd()
    data class AfterOccurrences(val remaining: Int) : RecurrenceEnd()  // una allocation por instancia
    data class UntilDate(val date: Long) : RecurrenceEnd()             // una allocation por instancia
}

// Emitir Never a través de StateFlow miles de veces no crea objetos.
// Emitir AfterOccurrences(5) crea un objeto nuevo cada vez.
```

## The Senior Nuance (El Matiz Senior)

- En [jerarquías selladas]({{ "/es/glosario/sealed-hierarchy/" | relative_url }}), usá `data object` para variantes sin estado para evitar allocations por emisión. Un `data object Loading` es un [singleton]({{ "/es/glosario/singleton/" | relative_url }}) — referenciarlo es gratis. Un `data class Loading()` asignaría un objeto nuevo en cada [emisión de estado]({{ "/es/glosario/state-emission-patterns/" | relative_url }}), agregando presión al GC sin beneficio alguno.
- Las [inline functions]({{ "/es/glosario/inline-functions/" | relative_url }}) eliminan la allocation del objeto wrapper del lambda. Cuando una [función de orden superior]({{ "/es/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) está marcada como `inline`, el cuerpo del lambda se copia al call site en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}), evitando la allocation en el [heap]({{ "/es/glosario/heap/" | relative_url }}) que un lambda normal requeriría.
- El [autoboxing]({{ "/es/glosario/autoboxing/" | relative_url }}) es una fuente oculta de allocations: una `List<Int>` almacena objetos `Integer` (boxeados), no [primitivos]({{ "/es/glosario/primitives/" | relative_url }}) `int`. En loops intensivos, preferí [`IntArray`]({{ "/es/glosario/intarray/" | relative_url }}) sobre `List<Int>` para mantener los valores en el stack o en un array plano.
- En Android, el código con muchas allocations en `onDraw()`, `onMeasure()`, o lambdas de recomposición es la principal fuente de jank. Perfilá con el Memory Profiler de Android Studio para identificar hotspots de allocations antes de optimizar — la optimización prematura sin profiling es adivinación.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
