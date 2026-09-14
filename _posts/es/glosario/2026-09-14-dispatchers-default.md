---
layout: post
title: "Dispatchers.Default"
date: 2026-09-14 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, threading, performance]
lang: es
permalink: /es/glosario/dispatchers-default/
---

## The Theory (El Qué)

**`Dispatchers.Default`** es el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) para trabajo de CPU: ordenar, parsear, hacer diff, aritmética de fechas, decodificar imágenes. Su [thread pool]({{ "/es/glosario/thread-pool/" | relative_url }}) está dimensionado según la cantidad de cores (mínimo 2), porque más threads que cores no pueden hacer más rápido un cómputo. Es también el default de `launch`/`async` en un scope que no especifica dispatcher.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Date math off the main thread: pattern scans over months/years
// must never stall input dispatching (popup ANR)
val suggested = withContext(Dispatchers.Default) {
    RecurrenceCalculator.suggestPatternDueDate(/* ... */)
}
```

## The Senior Nuance (El Matiz Senior)

- **Bloquear en `Default` es el error caro.** Con tantos threads como cores, un thread detenido en I/O le quita un core entero a toda otra coroutine. El trabajo bloqueante va en [`IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}).
- **"Lento" no es el criterio.** La aritmética de fechas es lenta *y* de CPU → `Default`. Una llamada de red es lenta *y* bloqueante → `IO`. Elegí según qué hace el thread mientras espera.
- **Comparte threads con `IO`.** Saltar `Default → IO → Default` muchas veces reutiliza el mismo worker; el [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) elide el cambio cuando los límites de paralelismo lo permiten.
- **Los loops largos de CPU tienen que cooperar.** Agregá `ensureActive()` o `yield()` para que la [cancelación]({{ "/es/glosario/cooperative-cancellation/" | relative_url }}) pueda alcanzarlos.
- Ver [Context & Dispatchers]({{ "/es/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
