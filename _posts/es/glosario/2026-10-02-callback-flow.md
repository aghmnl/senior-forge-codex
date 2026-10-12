---
layout: post
title: "callbackFlow"
date: 2026-10-02 12:00:00 +0000
categories: [es, glosario]
tags: [flow, callbacks, coroutines]
lang: es
permalink: /es/glosario/callback-flow/
---

## The Theory (El Qué)

**`callbackFlow { }`** construye un [Flow]({{ "/es/glosario/flow/" | relative_url }}) a partir de una API basada en [callbacks]({{ "/es/glosario/callbacks/" | relative_url }}), como las actualizaciones de ubicación, un sensor o un listener. Adentro del bloque registrás el callback, y cada vez que se dispara enviás el valor al flow con [trySend]({{ "/es/glosario/try-send/" | relative_url }}). El bloque termina con `awaitClose { }`, que mantiene vivo el flow mientras se colecta y **desregistra el callback** cuando el collector se detiene. Por dentro está respaldado por un [Channel]({{ "/es/glosario/channel/" | relative_url }}), y por eso los callbacks pueden enviar valores aunque no puedan suspender.

```kotlin
// Not found in FAS — standalone example
fun locationUpdates(client: LocationClient): Flow<Location> = callbackFlow {
    val listener = LocationListener { location -> trySend(location) }
    client.register(listener)
    awaitClose { client.unregister(listener) }   // corre cuando se deja de colectar
}
```

## The Senior Nuance (El Matiz Senior)

- **`awaitClose` es obligatorio.** Si el bloque termina sin él, `callbackFlow` falla con una `IllegalStateException`; y sin el lambda de limpieza, el callback nunca se desregistra y se fuga.
- **Convierte una API de "empuje" en un flow cold.** Cada collector registra su propio callback, y dejar de colectar lo desregistra, así que el listener vive exactamente mientras alguien escucha.
- Ver [callbackFlow]({{ "/es/02-coroutines-flow/callback-flow/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
