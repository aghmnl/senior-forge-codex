---
layout: post
title: "asSharedFlow"
date: 2026-09-28 12:00:00 +0000
categories: [es, glosario]
tags: [flow, state-management, architecture]
lang: es
permalink: /es/glosario/as-shared-flow/
---

## The Theory (El Qué)

**`asSharedFlow()`** devuelve una **vista de solo lectura** de un [MutableSharedFlow]({{ "/es/glosario/mutable-shared-flow/" | relative_url }}): un `SharedFlow` que entrega las mismas emisiones pero no ofrece forma de emitir. Es el equivalente para [SharedFlow]({{ "/es/glosario/sharedflow/" | relative_url }}) de [asStateFlow()]({{ "/es/glosario/as-state-flow/" | relative_url }}), y es la forma en que una clase expone un stream propio sin dejar que quien lo recibe escriba en él.

```kotlin
// Not found in FAS — standalone example
class SessionManager {
    private val _sessionExpired = MutableSharedFlow<Unit>(extraBufferCapacity = 1)
    val sessionExpired: SharedFlow<Unit> = _sessionExpired.asSharedFlow()
}
```

## The Senior Nuance (El Matiz Senior)

- **Hacer upcast no alcanza.** Declarar `val events: SharedFlow<T> = _events` esconde el tipo mutable de la firma, pero cualquiera que lo reciba puede castearlo de vuelta a [`MutableSharedFlow`]({{ "/es/glosario/mutable-shared-flow/" | relative_url }}) y emitir. `asSharedFlow()` devuelve otro objeto que no se puede castear de vuelta.
- **Impone el [flujo unidireccional de datos]({{ "/es/glosario/unidirectional-data-flow/" | relative_url }}).** Solo el dueño puede producir valores; todos los demás solo pueden [colectar]({{ "/es/glosario/collect/" | relative_url }}). Así cada emisión se puede rastrear hasta un único lugar.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
