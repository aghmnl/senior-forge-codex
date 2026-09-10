---
layout: post
title: "Blocking Call"
date: 2026-09-10 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/blocking-call/
---

## The Theory (El Qué)

Una **blocking call** (llamada bloqueante) es cualquier operación que detiene al [thread]({{ "/es/glosario/thread/" | relative_url }}) llamador hasta que completa: `Thread.sleep`, I/O síncrono de archivo o socket, `Object.wait`, un lock `synchronized` bajo contención, [runBlocking]({{ "/es/glosario/run-blocking/" | relative_url }}). Mientras está bloqueado, el thread no hace nada más — no puede correr otras [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}), y si es el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) la UI deja de renderizar.

```kotlin
// Not found in FAS — standalone example
suspend fun readConfig(): String = File("config.json").readText()   // still blocks the caller's thread

suspend fun readConfig(): String = withContext(Dispatchers.IO) {   // main-safe
    File("config.json").readText()
}
```

Marcar una función como `suspend` **no** hace que sus llamadas bloqueantes dejen de bloquear. Solo los [suspension points]({{ "/es/glosario/suspension-point/" | relative_url }}) genuinos liberan el thread; una llamada bloqueante dentro de una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) sigue bloqueando a quien la llamó.

## The Senior Nuance (El Matiz Senior)

- **Bloquear en `Dispatchers.Main` es el ANR.** Cinco segundos de main thread bloqueado y el sistema mata la app. Incluso 16 ms tira un frame.
- **`Dispatchers.IO` existe para absorber llamadas bloqueantes.** Es un [thread pool]({{ "/es/glosario/thread-pool/" | relative_url }}) dimensionado (64+ threads) precisamente para que las llamadas bloqueantes de archivo y red puedan detener threads sin dejar sin recursos al trabajo de CPU. Envolvé el código bloqueante con `withContext(Dispatchers.IO)` *dentro* de la suspend function, así cada llamador obtiene una API main-safe.
- **Bloquear dentro de una coroutine también bloquea la cancelación.** Un thread detenido no puede llegar a un suspension point, así que `cancel()` no tiene efecto hasta que la llamada bloqueante devuelve. Preferí equivalentes suspendibles (`delay` sobre `sleep`, I/O suspendible de Okio/Ktor sobre streams) donde existan.
- Contraste con la suspensión en [Suspend Functions]({{ "/es/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
