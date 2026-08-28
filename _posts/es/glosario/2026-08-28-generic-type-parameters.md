---
layout: post
title: "Parámetros de Tipo Genérico"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/generic-type-parameters/
---

## The Theory (El Qué)

Los **parámetros de tipo genérico** (la `T` en `List<T>`, `Flow<T>`, `Class<T>`) son placeholders que permiten a clases, interfaces y funciones operar sobre cualquier tipo manteniendo la seguridad de tipos en [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}). El compilador verifica la corrección de tipos — no podés poner un `String` en un `MutableList<Int>` — pero en la [JVM]({{ "/es/glosario/jvm/" | relative_url }}), los parámetros de tipo genérico se **borran** en [tiempo de ejecución]({{ "/es/glosario/runtime/" | relative_url }}): el bytecode solo ve el tipo raw (`List`, `Flow`, `Class`). Esto se llama *type erasure*.

## The Senior Nuance (El Matiz Senior)

- Type erasure significa que **no podés** verificar tipos genéricos en runtime: `value is List<String>` no compila porque la JVM no puede distinguir `List<String>` de `List<Int>`. El workaround son los parámetros de tipo [`reified`]({{ "/es/glosario/reified/" | relative_url }}) en [funciones inline]({{ "/es/glosario/inline-functions/" | relative_url }}), donde el compilador sustituye el tipo concreto en cada sitio de llamada.
- Kotlin agrega **varianza en el sitio de declaración** (`out T`, `in T`) que el compilador verifica en [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}). `List<out T>` es covariante — un `List<String>` puede asignarse a un `List<Any>`. Java requiere wildcards en el sitio de uso (`? extends T`) para lo mismo.
- La **star projection** (`List<*>`) es el equivalente Kotlin del raw type de Java, pero más segura — el compilador la trata como `List<out Any?>` (legible) pero previene escribir valores inseguros en ella.
- En Android, los parámetros de tipo genérico están en todas partes: `Flow<UiState>`, `LiveData<List<Task>>`, `Result<T>`, `Adapter<VH>`. Entender varianza y type erasure es crítico para escribir componentes reusables y type-safe.
- `Class<T>` y `KClass<T>` llevan el class token a través del type erasure, por eso patrones como `intent.getParcelableExtra<T>(key)` o `Room.inMemoryDatabaseBuilder(context, MyTasksDatabase::class.java)` requieren pasar la clase explícitamente — la `T` genérica sola se borraría.

```kotlin
// From FollowApp Suite — TaskDaoSortTest.kt
db = Room.inMemoryDatabaseBuilder(context, MyTasksDatabase::class.java)
    .allowMainThreadQueries()
    .build()
```

`MyTasksDatabase::class.java` es el class token que sobrevive al type erasure — Room necesita la clase concreta en runtime para instanciar la implementación de base de datos generada por [procesamiento de anotaciones]({{ "/es/glosario/annotation-processing/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
