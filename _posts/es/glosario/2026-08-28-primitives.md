---
layout: post
title: "Primitivos"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/primitives/
---

## The Theory (El Qué)

Los **primitivos** son los tipos de datos básicos que la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) maneja directamente a nivel de hardware: `int`, `long`, `float`, `double`, `boolean`, `char`, `byte` y `short`. Se almacenan en el stack (o inline en objetos), no en el heap, y no tienen overhead de objeto — sin headers, sin [recolección de basura]({{ "/es/glosario/garbage-collector/" | relative_url }}). En Kotlin, escribís `Int`, `Long`, `Boolean`, etc., y el compilador decide en [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}) si usar un primitivo JVM o su wrapper boxed en el [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) generado.

## The Senior Nuance (El Matiz Senior)

- El `Int` de Kotlin compila al primitivo JVM `int` siempre que sea posible. Se boxea a `java.lang.Integer` solo cuando se usa como tipo nullable (`Int?`), como argumento de tipo genérico (`List<Int>` almacena objetos `Integer`), o cuando se pasa a una función que espera `Any`. Entender este límite de boxing es crítico para código sensible al rendimiento.
- **`const val`** solo funciona con primitivos y `String`. Estas constantes de compile-time se insertan directamente en el bytecode — el valor mismo se copia en cada sitio de uso, eliminando cualquier acceso a campo en [tiempo de ejecución]({{ "/es/glosario/runtime/" | relative_url }}).
- Los `UInt`, `ULong`, etc. de Kotlin son **inline classes** que wrappean primitivos. A nivel de bytecode, siguen siendo `int`/`long` — la semántica unsigned se aplica en tiempo de compilación mediante [resolución de sobrecarga]({{ "/es/glosario/overload-resolution/" | relative_url }}) y funciones intrínsecas.
- En arrays, `IntArray` mapea a `int[]` (array primitivo, sin boxing), mientras que `Array<Int>` mapea a `Integer[]` (boxed, heap-allocated). Para arrays grandes, esta diferencia es medible tanto en memoria como en rendimiento.

```kotlin
// From FollowApp Suite — DragToReorder.kt
companion object {
    const val LONG_PRESS_TAP_SLOP_PX = 24f  // Primitivo Float, inlined en cada sitio de uso
}
```

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
