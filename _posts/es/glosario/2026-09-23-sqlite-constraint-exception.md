---
layout: post
title: "SQLiteConstraintException"
date: 2026-09-23 12:00:00 +0000
categories: [es, glosario]
tags: [error-handling, persistence]
lang: es
permalink: /es/glosario/sqlite-constraint-exception/
---

## The Theory (El Qué)

**`SQLiteConstraintException`** se lanza cuando una escritura viola una restricción del esquema: un índice `UNIQUE`, una columna `NOT NULL`, una foreign key. En [Room]({{ "/es/glosario/room/" | relative_url }}) aparece desde un `@Insert` o un `@Update` cuyos datos rompen una regla que la base de datos hace cumplir — un nombre de etiqueta duplicado, una fila huérfana. Es una [`RuntimeException`]({{ "/es/glosario/runtime-exception/" | relative_url }}), así que nada te obliga a manejarla, y es el caso de manual de una excepción técnica que lleva información que vale la pena preservar hasta el borde de la UI.

```kotlin
// De FollowApp Suite — ErrorMapping.kt
// Traducida una sola vez, en el borde de la UI: la restricción se vuelve un mensaje real
fun Throwable.toUserMessage(): Int = when {
    this is SQLiteConstraintException && message.orEmpty().contains("UNIQUE") ->
        R.string.error_duplicate_tag
    else -> R.string.error_generic
}
```

## The Senior Nuance (El Matiz Senior)

- **No te la tragues en el repositorio.** "Algo salió mal" es lo que queda después de que la capa de datos tiró el único detalle sobre el que el usuario podía actuar: *ese nombre ya existe*.
- **Es una señal de validación, no siempre un bug.** Una violación de `UNIQUE` sobre un nombre que escribió el usuario es entrada esperada, así que la UI debería presentarla como error de formulario y no como reporte de crash.
- **Matchear contra el mensaje es frágil pero pragmático.** No hay una API tipada de "qué restricción falló", así que chequear `UNIQUE` en el mensaje es el workaround habitual — merece un comentario y merece un test.
- Ver [Error Handling: try-catch & .catch]({{ "/es/02-coroutines-flow/error-handling/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
