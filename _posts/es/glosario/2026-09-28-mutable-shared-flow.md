---
layout: post
title: "MutableSharedFlow"
date: 2026-09-28 12:00:00 +0000
categories: [es, glosario]
tags: [flow, concurrency, coroutines]
lang: es
permalink: /es/glosario/mutable-shared-flow/
---

## The Theory (El Qué)

**`MutableSharedFlow<T>`** es la versión escribible de [SharedFlow]({{ "/es/glosario/sharedflow/" | relative_url }}). La función constructora `MutableSharedFlow(replay, extraBufferCapacity, onBufferOverflow)` fija todo su comportamiento: cuántos valores pasados recibe un suscriptor nuevo, cuánto lugar hay antes de que [emit]({{ "/es/glosario/emit/" | relative_url }}) suspenda, y qué pasa cuando el buffer se llena. Suma [emit]({{ "/es/glosario/emit/" | relative_url }}) y [tryEmit]({{ "/es/glosario/try-emit/" | relative_url }}) para meter valores, `subscriptionCount` (un [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) con la cantidad de [collectors]({{ "/es/glosario/collector/" | relative_url }}) activos) y [resetReplayCache()]({{ "/es/glosario/reset-replay-cache/" | relative_url }}). Queda privado y se expone de solo lectura con [asSharedFlow()]({{ "/es/glosario/as-shared-flow/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
private val _refreshRequests = MutableSharedFlow<Unit>(
    extraBufferCapacity = 1,
    onBufferOverflow = BufferOverflow.DROP_OLDEST
)
val refreshRequests: SharedFlow<Unit> = _refreshRequests.asSharedFlow()

// subscriptionCount: hacer el trabajo caro solo mientras alguien escucha
_refreshRequests.subscriptionCount
    .map { it > 0 }
    .distinctUntilChanged()
    .onEach { active -> if (active) startPolling() else stopPolling() }
    .launchIn(scope)
```

## The Senior Nuance (El Matiz Senior)

- **Los valores por defecto son un rendezvous.** `MutableSharedFlow<T>()` no tiene replay ni buffer: `emit` espera a cada suscriptor y [`tryEmit`]({{ "/es/glosario/try-emit/" | relative_url }}) falla siempre que haya uno. La mayoría de las sorpresas con shared flows vienen de no elegir estos parámetros a propósito.
- **Las políticas de descarte necesitan un buffer.** `DROP_OLDEST` y `DROP_LATEST` solo se aceptan cuando `replay` o `extraBufferCapacity` son mayores que cero; sin buffer no hay nada de dónde descartar.
- **`MutableStateFlow` también es uno.** Un [MutableStateFlow]({{ "/es/glosario/mutable-state-flow/" | relative_url }}) es un `MutableSharedFlow` con una configuración fija, por eso también tiene `subscriptionCount`, y por eso su [`resetReplayCache()`]({{ "/es/glosario/reset-replay-cache/" | relative_url }}) lanza una excepción: un state flow siempre tiene que tener un valor.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
