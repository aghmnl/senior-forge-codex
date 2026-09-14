---
layout: post
title: "Dispatchers.Main.immediate"
date: 2026-09-14 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, threading, state-management]
lang: es
permalink: /es/glosario/dispatchers-main-immediate/
---

## The Theory (El Qué)

**`Dispatchers.Main.immediate`** es [`Dispatchers.Main`]({{ "/es/glosario/dispatchers-main/" | relative_url }}) con una optimización: si la coroutine *ya* está en el main thread cuando se despacha, corre de forma síncrona en vez de hacer post a la cola del [`Looper`]({{ "/es/glosario/looper/" | relative_url }}). Fuera de Main se comporta exactamente como `Main`. [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) y `lifecycleScope` lo usan, así que un [`launch`]({{ "/es/glosario/launch/" | relative_url }}) desde un click handler se ejecuta hasta su primer [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}) antes de que el handler devuelva.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Reset the form FIRST, then trigger the suggestion recompute.
// viewModelScope uses Main.immediate, so the combine collector may run
// synchronously when a source flow is set — if the form reset came after,
// it would wipe the freshly computed labelSearchResults.
_uiState.update { it.copy(isFormVisible = true, form = TaskFormState()) }
_formOpenTrigger.value = System.currentTimeMillis()
```

## The Senior Nuance (El Matiz Senior)

- **Es una garantía de orden.** Como la coroutine corre de forma síncrona hasta su primera suspensión, las sentencias posteriores al `launch` observan sus primeros efectos — y un collector de Flow en `Main.immediate` puede correr *adentro* del `value =` que lo disparó. El orden de las sentencias pasa a sostener la corrección; comentalo.
- **Ahorra un frame de latencia**, y esa es la razón por la que los scopes de lifecycle lo eligieron: el estado seteado en un click handler es visible en el próximo frame, no en el siguiente.
- **No puede escapar de un Main ocupado.** Si Main está saturado (cold start, primera composición) el resume igual se encola. Sobrescribir con `launch(Dispatchers.IO)` es el fix cuando el trabajo es thread-safe.
- Ver [Context & Dispatchers]({{ "/es/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
