---
layout: post
title: "WhileSubscribed"
date: 2026-09-25 12:00:00 +0000
categories: [es, glosario]
tags: [flow, lifecycle, performance]
lang: es
permalink: /es/glosario/while-subscribed/
---

## The Theory (El Qué)

**`SharingStarted.WhileSubscribed(stopTimeoutMillis, replayExpirationMillis)`** es la estrategia de compartición de [stateIn]({{ "/es/glosario/state-in/" | relative_url }}) y `shareIn` que mantiene corriendo la colección del [upstream]({{ "/es/glosario/upstream/" | relative_url }}) **solo mientras hay al menos un suscriptor**. Cuando el último [collector]({{ "/es/glosario/collector/" | relative_url }}) se va, espera `stopTimeoutMillis` y después cancela el upstream; cuando llega un suscriptor nuevo, lo vuelve a arrancar. `replayExpirationMillis` controla cuánto sobrevive el valor cacheado después de que se detiene el upstream (por defecto, para siempre).

```kotlin
// Not found in FAS — standalone example
.stateIn(
    scope = viewModelScope,
    // Sobrevive a una rotación (~1 s sin suscriptores)
    // y frena la query tras 5 s en background
    started = SharingStarted.WhileSubscribed(5_000),
    initialValue = UiState.Loading
)
```

## The Senior Nuance (El Matiz Senior)

- **Por qué 5 segundos.** Un cambio de configuración saca al suscriptor por un momento y lo vuelve a agregar. Con un timeout de `0` el upstream se reiniciaría en cada rotación; con `5_000` sobrevive a la rotación pero igual se detiene cuando el usuario realmente sale de la app.
- **Solo funciona si el colector realmente se va.** `collectAsState()` sigue colectando en background, así que `WhileSubscribed` nunca ve cero suscriptores. Necesita un colector [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}): [collectAsStateWithLifecycle]({{ "/es/glosario/collect-as-state-with-lifecycle/" | relative_url }}) o [repeatOnLifecycle]({{ "/es/glosario/repeat-on-lifecycle/" | relative_url }}).
- **Reiniciar significa volver a ejecutar.** Cuando el upstream se reinicia es un [Flow]({{ "/es/glosario/flow/" | relative_url }}) cold que se colecta otra vez desde cero: la query corre de nuevo y la UI ve primero, por un instante, el valor cacheado.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
