---
layout: post
title: "Channel Capacity"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [concurrency, coroutines]
lang: es
permalink: /es/glosario/channel-capacity/
---

## The Theory (El Qué)

La **capacidad** de un [Channel]({{ "/es/glosario/channel/" | relative_url }}) es cuántos valores puede guardar mientras nadie los tomó todavía. Se elige al crear el channel, y decide dos cosas: cuándo [`send`]({{ "/es/glosario/send/" | relative_url }}) tiene que **esperar**, y cuándo [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) **falla**. Hay cuatro tipos:

- **`RENDEZVOUS`** (el de por defecto, `Channel<T>()`): sin lugar. Un valor solo pasa cuando un emisor y un receptor se encuentran, así que `send` espera hasta que alguien [recibe]({{ "/es/glosario/receive/" | relative_url }}), y `trySend` falla salvo que ya haya un receptor esperando.
- **`BUFFERED`**: una cantidad fija de lugar (64 por defecto, o el número que pases, como `Channel(capacity = 10)`). `send` espera solo cuando está lleno, y `trySend` falla solo cuando está lleno.
- **`UNLIMITED`**: lugar sin límite. `send` nunca espera y `trySend` nunca falla (salvo con el channel [cerrado]({{ "/es/glosario/close/" | relative_url }})).
- **`CONFLATED`**: lugar para exactamente un valor, el último. Un valor nuevo **reemplaza** al que estaba esperando, así que `send` nunca espera, `trySend` nunca falla, y los valores intermedios se descartan a propósito.

```kotlin
// Not found in FAS — standalone example
val handoff = Channel<Task>()                          // RENDEZVOUS
val queue = Channel<Task>(capacity = 10)               // BUFFERED, lugar para 10
val unbounded = Channel<Task>(Channel.UNLIMITED)       // UNLIMITED
val latest = Channel<Location>(Channel.CONFLATED)      // CONFLATED, se queda con el más nuevo
```

## The Senior Nuance (El Matiz Senior)

- **Elegí preguntándote "¿qué pasa cuando el consumidor se atrasa?".** Con `RENDEZVOUS` o `BUFFERED`, el productor espera ([backpressure]({{ "/es/glosario/backpressure/" | relative_url }})). Con `UNLIMITED`, crece la memoria. Con `CONFLATED`, se pierden los valores viejos. Uno de esos tres tiene que ser aceptable para esos datos.
- **`UNLIMITED` no es "seguro", mueve el problema.** Un productor que es siempre más rápido llena un buffer sin límite hasta que la app se queda sin memoria.
- **`CONFLATED` es la versión para channels de la [conflation]({{ "/es/glosario/conflation/" | relative_url }})**, la misma idea que aplica un `StateFlow`: solo importa el último valor. Sirve para actualizaciones de ubicación o lecturas de un sensor, nunca para algo como la confirmación de un pago.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
