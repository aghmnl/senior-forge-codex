---
layout: post
title: "coroutineScope (builder)"
date: 2026-09-10 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/coroutine-scope-builder/
---

## The Theory (El Qué)

**`coroutineScope { }`** es una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) que crea un scope hijo, corre su bloque, y *suspende hasta que cada coroutine lanzada adentro haya completado*. Si algún hijo falla, los demás se cancelan y la excepción se relanza al llamador. Es la forma de introducir paralelismo dentro de código suspendible secuencial sin filtrar trabajo.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
try {
    coroutineScope {
        ids.forEach { launch { quickCompleteTaskUseCase(taskId = it, isCompleted = isCompleted) } }
    }
} finally {
    isBulkWriteInFlight = false
}
```

El `finally` corre exactamente una vez, después de que los veinte `launch` terminaron — `coroutineScope` convierte un fan-out en un único suspension point.

## The Senior Nuance (El Matiz Senior)

- **Es una suspend function, no un scope que guardás.** A diferencia de `CoroutineScope(...)`, que crea un scope de larga vida que tenés que cancelar vos, `coroutineScope` vive solo durante la llamada. Nada se filtra.
- **El fallo es todo o nada.** Un hijo que falla cancela a sus hermanos y propaga. Usá `supervisorScope` cuando hijos independientes no deben tirarse abajo entre sí.
- **Es la forma correcta de hacer "descomposición paralela" en un use case.** `coroutineScope { val a = async { .. }; val b = async { .. }; a.await() + b.await() }` — la función sigue siendo una `suspend fun` común para su llamador.
- **La cancelación fluye a través.** Si el job externo se cancela ([viewModelScope]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) limpiado), cada hijo lanzado acá recibe [CancellationException]({{ "/es/glosario/cancellation-exception/" | relative_url }}).
- Ver [Suspend Functions]({{ "/es/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
