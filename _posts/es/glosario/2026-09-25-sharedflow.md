---
layout: post
title: "SharedFlow"
date: 2026-09-25 12:00:00 +0000
categories: [es, glosario]
tags: [flow, coroutines, concurrency]
lang: es
permalink: /es/glosario/sharedflow/
---

## The Theory (El Qué)

**`SharedFlow<T>`** es el [stream hot]({{ "/es/glosario/hot-stream/" | relative_url }}) general de kotlinx.coroutines: una sola fuente que **transmite cada emisión a todos los [collectors]({{ "/es/glosario/collector/" | relative_url }}) actuales**. `MutableSharedFlow(replay, extraBufferCapacity, onBufferOverflow)` configura cuántos valores pasados recibe un suscriptor nuevo (`replay`), cuánto lugar hay antes de que [emit]({{ "/es/glosario/emit/" | relative_url }}) suspenda, y qué pasa cuando el buffer se llena. No tiene valor inicial, ni valor actual, ni filtrado por igualdad, y su `collect` nunca termina. [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) es un `SharedFlow` con una configuración fija: replay de 1, overflow que descarta el más viejo, un valor inicial y [distinctUntilChanged]({{ "/es/glosario/distinct-until-changed/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
private val _events = MutableSharedFlow<UiEvent>()          // replay = 0
val events: SharedFlow<UiEvent> = _events.asSharedFlow()

fun onSaveClicked() {
    viewModelScope.launch {
        _events.emit(UiEvent.ShowSaved)   // suspende hasta que cada suscriptor lo toma
    }
}
```

## The Senior Nuance (El Matiz Senior)

- **Con `replay = 0` y sin suscriptores, las emisiones se pierden.** Eso es justamente lo buscado para señales de "disparar y olvidar" y la trampa para todo lo que la UI no puede perderse (un evento emitido mientras la pantalla rota simplemente desaparece).
- **Difusión, no cola.** Cada colector recibe cada valor. Cuando un valor tiene que manejarlo exactamente una vez un único consumidor, la primitiva es un [Channel]({{ "/es/glosario/channel/" | relative_url }}).
- **`tryEmit` sin buffer falla.** Con la configuración por defecto, `tryEmit` devuelve `false` siempre que hay un suscriptor, porque no hay lugar para dejar el valor sin suspender. Necesita `extraBufferCapacity` o una política de overflow que no suspenda.
- También es lo que produce `shareIn`, el hermano de [stateIn]({{ "/es/glosario/state-in/" | relative_url }}): una sola colección del upstream compartida por muchos suscriptores.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
