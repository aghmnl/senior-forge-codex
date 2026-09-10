---
layout: post
title: "Continuation"
date: 2026-09-10 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/continuation/
---

## The Theory (El Qué)

Una **Continuation** es el objeto que una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) recibe como último parámetro oculto después de que el compilador aplica [Continuation-Passing Style]({{ "/es/glosario/continuation-passing-style/" | relative_url }}). Representa "el resto del cómputo": guarda las locales del llamador, la etiqueta actual de la [state machine]({{ "/es/glosario/state-machine/" | relative_url }}), y el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) en el que reanudar. Llamar `resume(value)` o `resumeWithException(e)` reentra a la función suspendida en el [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}) donde se detuvo.

```kotlin
// Not found in FAS — standalone example
// What you write:
suspend fun load(id: String): Task

// What the compiler emits (JVM signature):
fun load(id: String, cont: Continuation<Task>): Any?
```

Cada llamada `suspend` en FAS — una query de [DAO]({{ "/es/glosario/dao/" | relative_url }}), un use case, `withContext` — pasa su continuation hacia abajo en la cadena, y así el [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) sabe cómo volver al llamador cuando el trabajo termina.

## The Senior Nuance (El Matiz Senior)

- **Vive en el [heap]({{ "/es/glosario/heap/" | relative_url }}), no en el [stack]({{ "/es/glosario/stack-frame/" | relative_url }}).** Las locales que deben sobrevivir a una suspensión se guardan como campos de la continuation. Por eso una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) suspendida cuesta unos cientos de bytes, no el stack de un thread.
- **Es un [callback]({{ "/es/glosario/callbacks/" | relative_url }}) que nunca escribís.** `suspendCancellableCoroutine` es el único lugar donde el código de usuario toca una continuation directamente — ver [suspendCancellableCoroutine]({{ "/es/glosario/suspend-cancellable-coroutine/" | relative_url }}).
- **Reanudar exactamente una vez.** Reanudar dos veces lanza `IllegalStateException`; no reanudar nunca filtra la coroutine para siempre. Ambos bugs vienen de puentes escritos a mano, nunca del código generado.
- Mecánica completa en [Suspend Functions]({{ "/es/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
