---
layout: post
title: "viewModelScope"
date: 2026-09-10 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/viewmodel-scope/
---

## The Theory (El Qué)

**`viewModelScope`** es una propiedad de extensión `CoroutineScope` sobre `ViewModel` (de `lifecycle-viewmodel-ktx`) ligada a `SupervisorJob() + Dispatchers.Main.immediate`. Cada [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) lanzada en él se cancela automáticamente en `onCleared()`, lo que lo convierte en el lugar por defecto para que un [ViewModel]({{ "/es/glosario/viewmodel-store/" | relative_url }}) llame [suspend functions]({{ "/es/glosario/suspend-functions/" | relative_url }}).

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Dispatchers.IO because viewModelScope defaults to Main.immediate,
// and Main is saturated by Compose's first composition on cold start.
viewModelScope.launch(Dispatchers.IO) {
    val snapshot = runCatching { tasksViewPreferences.read() }
        .onFailure { Log.e(TAG, "Error restoring TasksView prefs — falling back to defaults", it) }
        .getOrNull()
    // ...
}
```

El [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) por defecto es Main, así que todo lo lanzado acá corre en el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) hasta el primer [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}) — por eso las suspend functions que llama tienen que ser main-safe.

## The Senior Nuance (El Matiz Senior)

- **`Main.immediate` corre de forma síncrona hasta la primera suspensión.** Un `launch` desde un click handler ejecuta sus primeras líneas antes de que el handler devuelva — sin frame extra de latencia, pero tampoco sin chance de "escapar" de un main thread ocupado. El `restoreViewPreferences` de FAS sobreescribe a `Dispatchers.IO` precisamente porque Main estaba saturado durante el cold start.
- **`SupervisorJob` aísla los fallos.** Una coroutine que crashea no cancela a sus hermanas en el scope — pero una excepción no atrapada igual crashea la app. Manejá errores dentro de cada `launch`.
- **La cancelación es cooperativa.** `onCleared()` cancela el job; cada coroutine se detiene en su próximo suspension point. El trabajo sin suspension points sigue corriendo — ver [cooperative cancellation]({{ "/es/glosario/cooperative-cancellation/" | relative_url }}).
- **No lo pases hacia abajo.** Un repositorio o use case que recibe `viewModelScope` se acopla al lifecycle de la UI. Exponé suspend functions y dejá que el llamador sea dueño del scope.
- Ver [Suspend Functions]({{ "/es/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
