---
layout: post
title: "ensureActive"
date: 2026-09-15 12:00:00 +0000
categories: [es, glosario]
tags: [cancellation, coroutines]
lang: es
permalink: /es/glosario/ensure-active/
---

## The Theory (El Qué)

**`ensureActive()`** es la comprobación explícita de cancelación: lanza [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}) si el [`Job`]({{ "/es/glosario/job/" | relative_url }}) actual fue cancelado, y no hace nada en caso contrario. Toda [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) de `kotlinx.coroutines` la llama (o un equivalente) por vos, y por eso la cancelación solo se observa en [suspension points]({{ "/es/glosario/suspension-point/" | relative_url }}). El código que corre un loop largo *sin* suspender no tiene ese punto, y tiene que llamar a `ensureActive()` por su cuenta para seguir siendo [cooperativo]({{ "/es/glosario/cooperative-cancellation/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
withContext(Dispatchers.Default) {
    for (chunk in bigList.chunked(500)) {
        ensureActive()          // otherwise cancellation waits for the whole loop
        index.addAll(chunk.map(::tokenize))
    }
}
```

## The Senior Nuance (El Matiz Senior)

- **Preferilo a `if (!isActive) return`.** Retornar temprano completa la coroutine *normalmente*, escondiéndole la cancelación al padre. Lanzar mantiene intacta la semántica del árbol.
- **`yield()` hace lo mismo y además cede el thread.** Usá `yield()` cuando importa la equidad, `ensureActive()` cuando solo necesitás la comprobación.
- **Está disponible en `Job`, `CoroutineScope` y `CoroutineContext`.** Dentro de la lambda de un coroutine builder el receiver es un scope, así que un `ensureActive()` pelado funciona.
- Ver [Structured Concurrency]({{ "/es/02-coroutines-flow/structured-concurrency/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
