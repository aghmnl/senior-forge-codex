---
layout: post
title: "CoroutineExceptionHandler"
date: 2026-09-14 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, error-handling]
lang: es
permalink: /es/glosario/coroutine-exception-handler/
---

## The Theory (El Qué)

Un **`CoroutineExceptionHandler`** es un elemento del [`CoroutineContext`]({{ "/es/glosario/coroutine-context/" | relative_url }}) que recibe las excepciones que ninguna coroutine atrapó. Se invoca solo para coroutines *raíz* — un `launch` directo en un scope, o un hijo de un [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) — porque en cualquier otro lugar la excepción se propaga primero al [`Job`]({{ "/es/glosario/job/" | relative_url }}) padre. Sin handler, una excepción no capturada llega al handler por defecto del thread y, en Android, crashea el proceso.

```kotlin
// Not found in FAS — standalone example
private val scope = CoroutineScope(
    SupervisorJob() + Dispatchers.IO +
        CoroutineExceptionHandler { _, e -> Log.e(TAG, "billing collector failed", e) }
)
```

Los tres elementos responden cada uno a una pregunta distinta: qué falla de forma independiente (`SupervisorJob`), dónde corre (`Dispatchers.IO`), y qué pasa cuando igual falla (el handler).

## The Senior Nuance (El Matiz Senior)

- **Nunca aplica a `async`.** Una excepción dentro de `async` se guarda en el `Deferred` y la relanza `await()`; el handler queda de lado. Manejala en la llamada a `await`.
- **No es un `try/catch`.** Para cuando el handler corre la coroutine ya está muerta y los hijos de su scope (salvo que estén supervisados) ya cancelados. Es para loguear y reportar — `recordException` de [Crashlytics]({{ "/es/glosario/crashlytics/" | relative_url }}) es el cuerpo típico — no para recuperarse.
- **`viewModelScope` no tiene ninguno por defecto.** Una excepción no capturada en un `launch` ahí crashea la app como en cualquier otro lado. Manejá los errores dentro de cada `launch`, o agregá un handler con `viewModelScope.launch(handler) { }` cuando el trabajo es fire-and-forget.
- **[`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}) nunca se le entrega.** La cancelación es completación normal desde el punto de vista del framework.
- Ver [Context & Dispatchers]({{ "/es/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
