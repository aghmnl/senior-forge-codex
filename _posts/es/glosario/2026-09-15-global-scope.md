---
layout: post
title: "GlobalScope"
date: 2026-09-15 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, lifecycle, memory]
lang: es
permalink: /es/glosario/global-scope/
---

## The Theory (El Qué)

**`GlobalScope`** es un [`CoroutineScope`]({{ "/es/glosario/coroutine-scope/" | relative_url }}) sin [`Job`]({{ "/es/glosario/job/" | relative_url }}) en su contexto: las coroutines lanzadas sobre él no tienen padre, nadie las espera, y solo se pueden cancelar una por una a través del `Job` que devuelve [`launch`]({{ "/es/glosario/launch/" | relative_url }}). Es la salida explícita de Structured Concurrency, y `kotlinx.coroutines` lo marca `@DelicateCoroutinesApi` por esa razón.

```kotlin
// Not found in FAS — standalone example
GlobalScope.launch {          // no parent: outlives the screen, the ViewModel, the test
    repository.sync()
}
```

## The Senior Nuance (El Matiz Senior)

- **Es un scope de vida de proceso sin dueño.** Un `@Singleton` también necesita un scope, pero `CoroutineScope(SupervisorJob() + Dispatchers.IO)` en un campo al menos *tiene* un `cancel()` que alguien puede llamar y un lugar donde agregar un [`CoroutineExceptionHandler`]({{ "/es/glosario/coroutine-exception-handler/" | relative_url }}).
- **Sus coroutines son invisibles para los tests.** [`runTest`]({{ "/es/glosario/run-test/" | relative_url }}) no puede esperarlas, así que las aserciones corren una carrera contra trabajo real.
- **Retiene referencias mientras corre.** Un `GlobalScope.launch` que sostiene una Activity o una View es un [memory leak]({{ "/es/glosario/memory-leaks/" | relative_url }}) hasta que la coroutine termina.
- Ver [Structured Concurrency]({{ "/es/02-coroutines-flow/structured-concurrency/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
