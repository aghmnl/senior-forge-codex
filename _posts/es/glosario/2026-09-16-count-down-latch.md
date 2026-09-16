---
layout: post
title: "CountDownLatch"
date: 2026-09-16 12:00:00 +0000
categories: [es, glosario]
tags: [threading, concurrency, testing]
lang: es
permalink: /es/glosario/count-down-latch/
---

## The Theory (El Qué)

**`java.util.concurrent.CountDownLatch`** es un sincronizador de la JVM: un contador inicializado en N, decrementado con `countDown()`, y un `await()` bloqueante que estaciona el [thread]({{ "/es/glosario/thread/" | relative_url }}) que llama hasta que el contador llega a cero. Es la herramienta clásica para "esperá hasta que pasaron N cosas" entre threads — y la herramienta clásica en tests de Android pre-coroutines para esperar un [callback]({{ "/es/glosario/callbacks/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
val latch = CountDownLatch(1)
legacyApi.load { result -> captured = result; latch.countDown() }
latch.await(5, TimeUnit.SECONDS)      // blocks the test thread
```

## The Senior Nuance (El Matiz Senior)

- **Su `await()` bloquea un thread; el `await()` de coroutines suspende.** Llamar a `CountDownLatch.await()` desde una coroutine estaciona un thread del dispatcher — en [Main]({{ "/es/glosario/dispatchers-main/" | relative_url }}) es un ANR, en [Default]({{ "/es/glosario/dispatchers-default/" | relative_url }}) deja sin un core a los demás.
- **El reemplazo nativo de coroutines es [`CompletableDeferred`]({{ "/es/glosario/completable-deferred/" | relative_url }}).** `CountDownLatch(1)` con un resultado que leés después es exactamente `CompletableDeferred<T>`: `complete(value)` en vez de `countDown()`, un `await()` suspendible que devuelve el valor.
- **Bajo [`runTest`]({{ "/es/glosario/run-test/" | relative_url }}) es un deadlock.** El tiempo virtual nunca avanza mientras un thread real está bloqueado en un latch.
- Ver [Launch vs Async/Await]({{ "/es/02-coroutines-flow/launch-vs-async-await/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
