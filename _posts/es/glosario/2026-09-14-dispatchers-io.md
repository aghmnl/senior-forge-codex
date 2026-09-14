---
layout: post
title: "Dispatchers.IO"
date: 2026-09-14 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, threading, performance]
lang: es
permalink: /es/glosario/dispatchers-io/
---

## The Theory (El Qué)

**`Dispatchers.IO`** es el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) diseñado para [llamadas bloqueantes]({{ "/es/glosario/blocking-call/" | relative_url }}): I/O de archivos y sockets, SDKs síncronos, cualquier cosa que detenga un [thread]({{ "/es/glosario/thread/" | relative_url }}) mientras espera. Es una vista sobre el [thread pool]({{ "/es/glosario/thread-pool/" | relative_url }}) compartido que permite hasta 64 threads (o la cantidad de cores, lo que sea mayor) bloqueados a la vez, así los threads que esperan no dejan sin recursos al trabajo de CPU.

```kotlin
// From FollowApp Suite — BackupManager.kt
suspend fun exportTo(uri: Uri): Result<Unit> = withContext(Dispatchers.IO) {
    // escritura de archivo
}
```

El cambio vive *adentro* de la suspend function, y eso es lo que la hace main-safe para todo llamador.

## The Senior Nuance (El Matiz Senior)

- **IO es para detenerse, no para computar.** Los loops pesados de CPU acá son un desperdicio pero inofensivos; el error real es el inverso — bloquear en [`Default`]({{ "/es/glosario/dispatchers-default/" | relative_url }}).
- **Room, Retrofit y DataStore ya lo usan internamente.** Envolver sus llamadas suspend en `withContext(IO)` es redundante; envolvé tu propio código de archivos/JSON.
- **`limitedParallelism(1)`** talla un sub-dispatcher single-thread — la forma de confinar un SDK no thread-safe sin crear un thread.
- **Hardcodearlo es un smell de testing.** Inyectá un `CoroutineDispatcher` (`@IoDispatcher`) para que los tests puedan sustituir un [`TestDispatcher`]({{ "/es/glosario/test-dispatcher/" | relative_url }}).
- Ver [Context & Dispatchers]({{ "/es/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
