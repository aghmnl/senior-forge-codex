---
layout: post
title: "Cooperative Cancellation"
date: 2026-09-10 12:00:00 +0000
categories: [es, glosario]
tags: [cancellation, coroutines]
lang: es
permalink: /es/glosario/cooperative-cancellation/
---

## The Theory (El Qué)

La **cooperative cancellation** (cancelación cooperativa) es la regla de que una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) nunca es matada desde afuera — tiene que *llegar a un punto donde verifica* si fue cancelada. Esos puntos son cada [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}) de `kotlinx.coroutines` (`delay`, `withContext`, `yield`, una llamada a un [DAO]({{ "/es/glosario/dao/" | relative_url }}) de Room, `Flow.collect`) más los chequeos explícitos: `isActive`, `ensureActive()`. En un punto así, una coroutine cancelada lanza [CancellationException]({{ "/es/glosario/cancellation-exception/" | relative_url }}).

```kotlin
// From FollowApp Suite — DragToReorder.kt
} catch (e: CancellationException) {
    // Gesture coroutine disposed mid-drag (e.g. composition change)
    state.endDrag(cancelled = true)
    throw e
}
```

Como la coroutine elige *dónde* puede ser interrumpida, nunca se detiene a mitad de una escritura de base de datos ni con un file handle abierto.

## The Senior Nuance (El Matiz Senior)

- **Los loops de CPU son incancelables salvo que los hagas cancelables.** Un `while` que nunca suspende va a correr hasta terminar después de que [viewModelScope]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) fue limpiado. Agregá `ensureActive()` o `yield()` dentro de loops largos.
- **Las [llamadas bloqueantes]({{ "/es/glosario/blocking-call/" | relative_url }}) derrotan la cancelación.** Un thread detenido en `InputStream.read` no puede verificar nada. Preferí I/O suspendible, o aceptá que la cancelación tiene efecto después de que la llamada devuelve.
- **`NonCancellable` es la vía de escape para cleanup.** `withContext(NonCancellable) { db.commit() }` dentro de un `finally` garantiza que el cleanup en sí no se cancele a medias.
- **El trade-off de diseño:** la cancelación cooperativa cuesta disciplina (relanzar, no tragar) y compra seguridad — sin escrituras rotas, sin recursos filtrados, `finally` determinista.
- Ver [Suspend Functions]({{ "/es/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
