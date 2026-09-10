---
layout: post
title: "Main Thread"
date: 2026-09-10 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/main-thread/
---

## The Theory (El Qué)

El **main thread** (UI thread) es el único [thread]({{ "/es/glosario/thread/" | relative_url }}) en el que Android despacha eventos de input, corre callbacks de lifecycle, mide/posiciona/dibuja views y compone frames de [Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}). Todo lo que el usuario ve pasa por él, a ~16 ms por frame a 60 Hz. Una [llamada bloqueante]({{ "/es/glosario/blocking-call/" | relative_url }}) ahí tira frames; cinco segundos de bloqueo disparan un diálogo de ANR y el sistema mata la app.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Date math off the main thread: pattern scans over months/years
// must never stall input dispatching (popup ANR)
val suggested = withContext(Dispatchers.Default) {
    val settings = getRecurrenceSettingsUseCase().first()
    // ... RecurrenceCalculator.suggestPatternDueDate(...)
}
```

`Dispatchers.Main` es el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) que lo apunta. [viewModelScope]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) usa `Main.immediate` por defecto, así que las suspend functions llamadas desde un ViewModel arrancan en el main thread y tienen que mover su propio trabajo pesado con `withContext`.

## The Senior Nuance (El Matiz Senior)

- **Suspender en Main es gratis; bloquear en Main es el bug.** Una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) que llega a un [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}) real libera el main thread para renderizar. Una que llama `File.readText()` no.
- **El trabajo de CPU también cuenta.** FAS mueve la aritmética de fechas de recurrencia a `Dispatchers.Default` aunque no sea I/O — cualquier cosa que tome más de unos milisegundos va fuera de Main.
- **Algunas APIs *requieren* Main.** Mutaciones de views, `LiveData.setValue`, la mayoría de las escrituras de estado de Compose desde fuera de un composable. `withContext(Dispatchers.Main)` es como una coroutine en background vuelve a él.
- **El Main del cold start es el thread más disputado de la app.** El comentario de `restoreViewPreferences` en FAS documenta el síntoma: una lectura rápida de DataStore reanudada en Main quedó encolada detrás de la primera composición por cientos de milisegundos.
- Ver [Suspend Functions]({{ "/es/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
