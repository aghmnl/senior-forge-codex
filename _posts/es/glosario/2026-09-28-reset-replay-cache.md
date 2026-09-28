---
layout: post
title: "resetReplayCache"
date: 2026-09-28 12:00:00 +0000
categories: [es, glosario]
tags: [flow, state-management]
lang: es
permalink: /es/glosario/reset-replay-cache/
---

## The Theory (El Qué)

**`resetReplayCache()`** vacía el replay cache de un [MutableSharedFlow]({{ "/es/glosario/mutable-shared-flow/" | relative_url }}). Después de la llamada, los suscriptores **nuevos** solo reciben los valores emitidos a partir de ese momento; los que ya estaban colectando igual reciben los valores que tenían en buffer. Solo importa para shared flows creados con `replay` mayor que cero.

```kotlin
// Not found in FAS — standalone example
private val _banner = MutableSharedFlow<String>(replay = 1)

fun showBanner(text: String) { _banner.tryEmit(text) }

fun onBannerHandled() {
    // Sin esto, cada suscriptor nuevo (una pantalla rotada) lo vuelve a ver
    _banner.resetReplayCache()
}
```

## The Senior Nuance (El Matiz Senior)

- **Suele ser una señal de que el valor en realidad es estado.** Limpiar un valor reproducido "una vez que se manejó" es exactamente el patrón de confirmación, hecho con una primitiva que no fue diseñada para eso. Modelar el valor como estado de UI que la UI confirma es más simple y sobrevive a la muerte del proceso.
- **El momento es frágil.** Entre la emisión y el reset, cualquier suscriptor nuevo sigue recibiendo el valor viejo. Llamarlo demasiado pronto le quita el valor a una pantalla que todavía no lo vio.
- **Lanza una excepción sobre un [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}).** Llamarlo sobre un [MutableStateFlow]({{ "/es/glosario/mutable-state-flow/" | relative_url }}) lanza `UnsupportedOperationException`, porque un state flow siempre tiene que tener un valor actual.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
