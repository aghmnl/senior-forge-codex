---
layout: post
title: "Dispatcher"
date: 2026-09-10 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/dispatcher/
---

## The Theory (El Qué)

Un **Dispatcher** (`CoroutineDispatcher`) es la parte del contexto de una coroutine que decide *qué [thread]({{ "/es/glosario/thread/" | relative_url }}) o [thread pool]({{ "/es/glosario/thread-pool/" | relative_url }})* la corre. Cuando una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) se reanuda después de un [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}), su [Continuation]({{ "/es/glosario/continuation/" | relative_url }}) se entrega al dispatcher, que la agenda. Android trae cuatro: `Dispatchers.Main` (el [main thread]({{ "/es/glosario/main-thread/" | relative_url }})), `Main.immediate`, `Dispatchers.IO` (pool para I/O bloqueante) y `Dispatchers.Default` (pool para CPU, dimensionado según los cores).

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Date math off the main thread: pattern scans over months/years
// must never stall input dispatching (popup ANR)
val suggested = withContext(Dispatchers.Default) {
    val settings = getRecurrenceSettingsUseCase().first()
    // ... RecurrenceCalculator.suggestPatternDueDate(...)
}
```

`withContext` cambia el dispatcher durante su bloque y vuelve al original después — sin nueva coroutine, sin `launch`.

## The Senior Nuance (El Matiz Senior)

- **El dispatcher se hereda, no se elige por llamada.** Una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) corre en el dispatcher en que estaba su llamador. Por eso la main-safety debe imponerse *dentro* de la función con `withContext`, no asumirse en el call site.
- **`IO` y `Default` comparten threads.** `Dispatchers.IO` es una vista sobre el mismo pool que `Default` con un límite de paralelismo mayor, así que `withContext(IO)` desde `Default` muchas veces no cambia de thread — el runtime elide el salto.
- **`Main.immediate` se saltea el post si ya está en Main.** [viewModelScope]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) lo usa para que un `launch` desde un click handler corra de forma síncrona hasta la primera suspensión, evitando un frame de latencia.
- **Nunca hardcodees `Dispatchers.IO` en una clase que querés testear.** Inyectá el dispatcher para que los tests puedan sustituir `StandardTestDispatcher`.
- Ver [Suspend Functions]({{ "/es/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
