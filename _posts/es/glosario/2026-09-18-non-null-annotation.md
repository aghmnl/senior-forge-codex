---
layout: post
title: "@NonNull"
date: 2026-09-18 12:00:00 +0000
categories: [es, glosario]
tags: [interop, null-safety]
lang: es
permalink: /es/glosario/non-null-annotation/
---

## The Theory (El Qué)

**`@NonNull`** (también `@NotNull` en el set de JetBrains) es la anotación Java que le dice al compilador de Kotlin que un valor que viene de Java nunca es [`null`]({{ "/es/glosario/null/" | relative_url }}). Kotlin entonces trata al `String` Java como un `String` común en vez de un [platform type]({{ "/es/glosario/platform-types/" | relative_url }}) `String!`, así que no hace falta manejar null — y, para parámetros, Kotlin se niega a pasarle un nullable. Junto con [`@Nullable`]({{ "/es/glosario/nullable-annotation/" | relative_url }}), hace que el límite Java/Kotlin sea tan estricto como código Kotlin puro, que es el punto de la guía de interop en [Null Safety: Elvis & Safe Calls]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

```kotlin
// Lado Java
public @NonNull List<Task> loadTasks(@NonNull String userId) { ... }

// Lado Kotlin
val tasks: List<Task> = api.loadTasks(userId)   // no hace falta ?.
// api.loadTasks(null)                            // no compila
```

## The Senior Nuance (El Matiz Senior)

- **Kotlin genera un chequeo en runtime para parámetros `@NonNull` de funciones Kotlin llamadas desde Java, no al revés.** Un retorno Java `@NonNull` que miente igual produce una NPE en Kotlin; la anotación es documentación en la que el compilador confía, así que aplicala solo donde el código Java lo garantiza de verdad.
- **Anotá toda la superficie pública de un módulo Java, no unos pocos métodos.** Una API anotada a medias es peor que ninguna: quien lee asume que los métodos sin anotar también fueron revisados.
- **Opción moderna: JSpecify `@NullMarked`.** Una anotación a nivel de package hace todo no-nulo por defecto y te deja marcar solo las excepciones nullable.
- Ver [Null Safety: Elvis & Safe Calls]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
