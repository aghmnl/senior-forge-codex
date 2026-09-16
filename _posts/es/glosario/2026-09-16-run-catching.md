---
layout: post
title: "runCatching"
date: 2026-09-16 12:00:00 +0000
categories: [es, glosario]
tags: [error-handling, functional, syntax]
lang: es
permalink: /es/glosario/run-catching/
---

## The Theory (El Qué)

**`runCatching { }`** corre un bloque y envuelve el resultado en un [`Result<T>`]({{ "/es/glosario/result/" | relative_url }}): `Result.success(value)` si retorna, `Result.failure(e)` si lanza. Es la alternativa funcional a [`try/catch`]({{ "/es/glosario/try-catch/" | relative_url }}) cuando querés el error como *valor* que podés mapear, recuperar o pasar — `getOrNull()`, `getOrDefault()`, `onFailure { }`, `getOrThrow()`.

```kotlin
// From FollowApp Suite — BackupManager.kt
suspend fun exportTo(uri: Uri): Result<Unit> = withContext(Dispatchers.IO) {
    runCatching {
        val json = BackupSerializer.serialize(bundle)
        context.contentResolver.openOutputStream(uri, "wt").use { /* ... */ }
    }.onSuccess {
        Log.d(TAG, "Backup exported")
    }.onFailure { Log.e(TAG, "Backup export failed", it) }
}
```

## The Senior Nuance (El Matiz Senior)

- **Atrapa `Throwable` — incluida [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}).** Dentro de una coroutine, `runCatching { suspendCall() }` se traga la cancelación y la convierte en un `failure`. Si el bloque suspende, relanzala: `.onFailure { if (it is CancellationException) throw it }`, o usá un `try/catch` más específico. Es el bug de `runCatching` más común en código Android.
- **Alrededor de [`await()`]({{ "/es/glosario/await/" | relative_url }}) dentro de [`supervisorScope`]({{ "/es/glosario/supervisor-scope/" | relative_url }}) es el idiom de recuperación por hijo.** `runCatching { header.await() }.getOrNull()` deja que una parte opcional falle sin las otras.
- **No devuelvas `Result` desde APIs públicas por defecto.** El `Result` de Kotlin está pensado para manejo local; una jerarquía sealed comunica mejor los errores de dominio entre capas.
- Ver [Launch vs Async/Await]({{ "/es/02-coroutines-flow/launch-vs-async-await/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
