---
layout: post
title: "Suspension Point"
date: 2026-09-10 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/suspension-point/
---

## The Theory (El Qué)

Un **suspension point** (punto de suspensión) es una llamada dentro de una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) donde la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) *puede* pausarse y devolver su [thread]({{ "/es/glosario/thread/" | relative_url }}) al [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}). Cada llamada a otra suspend function es candidata; el IDE las marca con un ícono en el margen. Que la coroutine realmente suspenda depende del callee — una query de [DAO]({{ "/es/glosario/dao/" | relative_url }}) de Room lo hace, un `if` no.

```kotlin
// From FollowApp Suite — QuickCompleteTaskUseCase.kt
suspend operator fun invoke(taskId: String, isCompleted: Boolean, cascade: Boolean = false) {
    taskRepository.updateTaskCompletion(taskId = taskId, isCompleted = isCompleted)
    if (cascade) {
        taskRepository.updateDescendantsCompletion(taskId = taskId, isCompleted = isCompleted)
    }
    if (isCompleted) {
        spawnNextOccurrence(taskId)
    }
}
```

Tres suspension points, uno por línea. Entre ellos el código corre de forma síncrona en el thread que lo reanudó.

## The Senior Nuance (El Matiz Senior)

- **Los suspension points son donde se verifica la cancelación.** Cada llamada suspendible de `kotlinx.coroutines` chequea el job antes y después de suspender y lanza [CancellationException]({{ "/es/glosario/cancellation-exception/" | relative_url }}) si fue cancelado. El código sin suspension points es incancelable — ver [cooperative cancellation]({{ "/es/glosario/cooperative-cancellation/" | relative_url }}).
- **Los suspension points son donde el thread puede cambiar.** Después de que `withContext(Dispatchers.IO)` devuelve, estás de vuelta en el dispatcher del llamador pero no necesariamente en el mismo thread físico. Nunca confíes en la identidad del thread a través de un suspension point (`ThreadLocal`, locks no reentrantes).
- **No toda llamada `suspend` suspende.** Una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) cuyo fast path devuelve un valor cacheado completa de forma síncrona y nunca devuelve `COROUTINE_SUSPENDED`. El punto es *potencial*, no garantizado.
- Detallado en [Suspend Functions]({{ "/es/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
