---
layout: post
title: "Error (UI State)"
date: 2026-09-23 12:00:00 +0000
categories: [es, glosario]
tags: [state-management, sealed-types, architecture]
lang: es
permalink: /es/glosario/error-state/
---

## The Theory (El Qué)

**`Error`** es el miembro de una jerarquía sellada de estado de UI que representa una falla que la pantalla tiene que mostrar: `data class Error(val messageRes: Int)`, junto a `Loading`, [`Idle`]({{ "/es/glosario/idle-state/" | relative_url }}) y [`Success`]({{ "/es/glosario/success-state/" | relative_url }}). Modelar la falla como *estado* y no como línea de log es lo que convierte a un bloque [`catch`]({{ "/es/glosario/catch/" | relative_url }}) en algo que el usuario puede ver — sin eso, una carga fallida deja la pantalla girando para siempre.

```kotlin
// De FollowApp Suite — LabelsListViewModel.kt
// El bloque catch mueve el state holder a un estado de error
.catch { e ->
    Log.e(TAG, "Error loading labels", e)
    _uiState.update { it.copy(isLoading = false, errorMessageRes = e.toUserMessage()) }
}
```

## The Senior Nuance (El Matiz Senior)

- **Llevá un recurso de mensaje, no un `Throwable`.** El estado es para la UI, así que guarda lo que la UI necesita: un id de string resource que respeta el idioma. La excepción va al log y a Crashlytics.
- **Un estado de error necesita una salida.** Reintentar, descartar, o caer a datos cacheados — un `Error` sin camino de recuperación es un callejón sin salida del que el usuario solo escapa matando la app.
- **Distinguí "falló" de "vacío".** Una carga fallida y una lista legítimamente vacía se ven idénticas si ambas renderizan una pantalla vacía, y el usuario no puede saber si conviene reintentar.
- Ver [Error Handling: try-catch & .catch]({{ "/es/02-coroutines-flow/error-handling/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
