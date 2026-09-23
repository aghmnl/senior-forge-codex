---
layout: post
title: "Throwable"
date: 2026-09-23 12:00:00 +0000
categories: [es, glosario]
tags: [error-handling, jvm]
lang: es
permalink: /es/glosario/throwable/
---

## The Theory (El Qué)

**`Throwable`** es la raíz de la jerarquía de errores de la JVM: todo lo que se puede lanzar es un `Throwable`, dividido en `Exception` (condiciones recuperables, incluidas las [`RuntimeException`]({{ "/es/glosario/runtime-exception/" | relative_url }})) y `Error` (`OutOfMemoryError`, `StackOverflowError` — fallas que una aplicación no debería manejar). Atrapar `Throwable` atrapa entonces *todo*, y por eso [`runCatching`]({{ "/es/glosario/run-catching/" | relative_url }}) es peligroso en código de [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}): `Throwable` incluye a [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}).

```kotlin
// De FollowApp Suite — ErrorMapping.kt
// Throwable es el receiver correcto para un mapper: tiene que aceptar cualquier cosa
fun Throwable.toUserMessage(): Int = when {
    this is SQLiteConstraintException && message.orEmpty().contains("UNIQUE") ->
        R.string.error_duplicate_tag
    else -> R.string.error_generic
}
```

## The Senior Nuance (El Matiz Senior)

- **`Throwable` es el tipo correcto para *recibir*, el incorrecto para *atrapar*.** Un mapper, un logger o un reportador de crashes deberían aceptar `Throwable`; un bloque `catch` casi nunca.
- **`Error` no es tuyo para manejar.** Atrapar un `OutOfMemoryError` para "seguir andando" normalmente produce un proceso zombi que falla de forma más rara un segundo después.
- **El [stack trace]({{ "/es/glosario/stack-trace/" | relative_url }}) es la carga útil.** Hagas lo que hagas con un `Throwable`, conservá la cadena de causas: loguear solo `e.message` tira justo la parte que identifica el bug.
- Ver [Error Handling: try-catch & .catch]({{ "/es/02-coroutines-flow/error-handling/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
