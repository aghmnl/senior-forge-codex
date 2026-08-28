---
layout: post
title: "Inferencia de Tipos"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/type-inference/
---

## The Theory (El Qué)

La **inferencia de tipos** es la capacidad del compilador de deducir el tipo de una expresión sin una anotación de tipo explícita. En [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}), el compilador de Kotlin analiza inicializadores, expresiones de retorno, parámetros de lambdas y argumentos genéricos para determinar tipos automáticamente. El resultado es código conciso y completamente type-safe — cada tipo inferido se verifica con el mismo rigor que uno explícito.

## The Senior Nuance (El Matiz Senior)

- La inferencia de tipos ocurre enteramente en tiempo de compilación. El [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) contiene tipos concretos — no hay costo ni ambigüedad en [tiempo de ejecución]({{ "/es/glosario/runtime/" | relative_url }}). `val x = 42` compila al mismo bytecode que `val x: Int = 42`.
- Kotlin infiere variables locales, tipos de retorno de funciones (para funciones de expresión única), tipos de parámetros de lambdas y argumentos de tipo genérico. Sin embargo, **los tipos de retorno de APIs públicas deben ser explícitos** — depender de la inferencia para funciones públicas acopla la firma de la API a la implementación.
- Los smart casts son una forma de narrowing de tipos que el compilador infiere después de verificaciones `is` o null checks. El compilador rastrea el tipo narrowed a través del flujo de control, eliminando la necesidad de casts manuales.
- Cuando la inferencia falla o produce un tipo inesperado (ej., `val items = emptyList()` infiere `List<Nothing>`), la solución es un argumento de tipo explícito — `emptyList<String>()` — no una anotación de tipo en la variable.
- La [resolución de sobrecarga]({{ "/es/glosario/overload-resolution/" | relative_url }}) y la inferencia de tipos interactúan: el compilador usa tipos esperados del contexto de llamada para resolver qué sobrecarga invocar, y el tipo de retorno de la sobrecarga elegida alimenta de vuelta la inferencia.

```kotlin
// From FollowApp Suite — TaskMapper.kt
fun TaskEntity.toDomain(): Task {
    return Task(
        id = this.id,                          // inferido como Long
        title = this.title,                    // inferido como String
        isCompleted = this.isCompleted,        // inferido como Boolean
        status = TaskStatus.valueOf(this.status) // inferido como TaskStatus
    )
}
```

El tipo de cada argumento se infiere del acceso a la propiedad, pero el compilador verifica que cada uno coincida con los tipos de parámetros del constructor de `Task` en tiempo de compilación.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
