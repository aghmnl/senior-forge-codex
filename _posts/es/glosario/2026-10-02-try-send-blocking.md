---
layout: post
title: "trySendBlocking"
date: 2026-10-02 12:00:00 +0000
categories: [es, glosario]
tags: [concurrency, threading, coroutines]
lang: es
permalink: /es/glosario/try-send-blocking/
---

## The Theory (El Qué)

**`trySendBlocking(value)`** envía un valor a un [Channel]({{ "/es/glosario/channel/" | relative_url }}) desde código que **no es una coroutine**, esperando lugar mediante el **bloqueo del [thread]({{ "/es/glosario/thread/" | relative_url }}) actual**. Es el puente para un thread de background que produce valores (el lector de un socket, una librería vieja) y tiene que respetar el [backpressure]({{ "/es/glosario/backpressure/" | relative_url }}) en vez de descartar valores. Igual que [trySend]({{ "/es/glosario/try-send/" | relative_url }}), devuelve un [ChannelResult]({{ "/es/glosario/channel-result/" | relative_url }}) en vez de lanzar.

```kotlin
// Not found in FAS — standalone example
// Una librería vieja entrega frames en su propio thread de background
legacyDecoder.setFrameCallback { frame ->
    frames.trySendBlocking(frame)   // bloquea ESTE thread hasta que haya lugar
}
```

## The Senior Nuance (El Matiz Senior)

- **Nunca en el main thread.** Bloquear el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) congela la UI, y después de unos segundos el sistema muestra un [ANR]({{ "/es/glosario/anr/" | relative_url }}).
- **Adentro de una coroutine, usá [send]({{ "/es/glosario/send/" | relative_url }}).** `send` espera suspendiendo, lo que libera el thread; `trySendBlocking` espera bloqueándolo.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
