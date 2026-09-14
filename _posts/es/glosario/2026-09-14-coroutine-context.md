---
layout: post
title: "CoroutineContext"
date: 2026-09-14 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, threading, cancellation]
lang: es
permalink: /es/glosario/coroutine-context/
---

## The Theory (El Qué)

Un **`CoroutineContext`** es el conjunto inmutable e indexado de elementos que lleva toda [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}): su [`Job`]({{ "/es/glosario/job/" | relative_url }}), su [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}), un [`CoroutineExceptionHandler`]({{ "/es/glosario/coroutine-exception-handler/" | relative_url }}) opcional y un `CoroutineName`. Cada tipo de elemento ocupa un único slot, así que los contextos se componen con `+` y un elemento posterior del mismo tipo reemplaza al anterior. Una coroutine hija hereda el contexto de su padre; lo que se pase a `launch`, `async` o [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}) se mergea encima.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Dispatchers.IO because viewModelScope defaults to Main.immediate,
// and Main is saturated by Compose's first composition on cold start.
viewModelScope.launch(Dispatchers.IO) {
    val snapshot = runCatching { tasksViewPreferences.read() }.getOrNull()
    // ...
}
```

`launch(Dispatchers.IO)` conserva el `SupervisorJob` de `viewModelScope` y `Main.immediate` se reemplaza por `IO` — solo cambió el slot del dispatcher.

## The Senior Nuance (El Matiz Senior)

- **La herencia es todo el punto.** La cancelación funciona porque el `Job` de un hijo se crea como hijo del `Job` del padre a partir del contexto heredado. Pasarle un `Job()` *nuevo* a `launch` rompe ese vínculo — la coroutine ya no se cancela con su scope, lo cual es casi siempre un bug.
- **`coroutineContext` se puede leer desde cualquier suspend function.** `coroutineContext[Job]`, `coroutineContext[CoroutineDispatcher]` y `ensureActive()` lo leen; así es como la [cancelación cooperativa]({{ "/es/glosario/cooperative-cancellation/" | relative_url }}) verifica el job actual sin un parámetro.
- **No es lo mismo que `CoroutineScope`.** Un [scope]({{ "/es/glosario/coroutine-scope/" | relative_url }}) es solo un objeto que sostiene un contexto y le da un receiver a `launch`; el contexto es el dato. `CoroutineScope(ctx).coroutineContext === ctx`.
- **Tampoco es el `Context` de Android** — una confusión clásica de entrevista. Ver [Context]({{ "/es/glosario/context-programming/" | relative_url }}) para los tres significados de la palabra.
- Tratamiento completo en [Context & Dispatchers]({{ "/es/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
