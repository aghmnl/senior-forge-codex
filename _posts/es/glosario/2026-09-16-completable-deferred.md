---
layout: post
title: "CompletableDeferred"
date: 2026-09-16 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, testing, callbacks]
lang: es
permalink: /es/glosario/completable-deferred/
---

## The Theory (El Qué)

**`CompletableDeferred<T>`** es un [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) sin ningún bloque [`async`]({{ "/es/glosario/async/" | relative_url }}) detrás: lo creás vacío y lo completás a mano con `complete(value)` o `completeExceptionally(e)`. Quien llame a [`await()`]({{ "/es/glosario/await/" | relative_url }}) sobre él suspende hasta que pase una de esas dos cosas. Es la promesa de un solo disparo nativa de coroutines — el [`CountDownLatch(1)`]({{ "/es/glosario/count-down-latch/" | relative_url }}) que suspende en vez de bloquear y lleva un valor.

```kotlin
// From FollowApp Suite — FakeLabelRepository.kt
/** When set, getLabelsWithOptions suspends until completed — lets tests observe in-flight reloads. */
var loadGate: CompletableDeferred<Unit>? = null

override fun getLabelsWithOptions(): Flow<Map<Label, List<LabelOption>>> =
    flow.map {
        loadGate?.await()
        // ...
    }
```

```kotlin
// From FollowApp Suite — LabelsListViewModelTest.kt
labelRepo.loadGate = CompletableDeferred()      // hold the next read in flight
vm.onConfirmScaleOptionRename(option.id)
advanceUntilIdle()
assertFalse(vm.uiState.value.isLoading)          // assert the intermediate state
labelRepo.loadGate!!.complete(Unit)              // release it
```

## The Senior Nuance (El Matiz Senior)

- **Sus dos trabajos: compuertas en tests y puentes de callbacks.** En tests congela una coroutine en un punto elegido para poder afirmar un estado intermedio de forma determinista. En producción convierte un [callback]({{ "/es/glosario/callbacks/" | relative_url }}) de un solo disparo en una llamada suspend — aunque [`suspendCancellableCoroutine`]({{ "/es/glosario/suspend-cancellable-coroutine/" | relative_url }}) suele ser mejor herramienta para eso, porque conecta la cancelación de vuelta al callback.
- **Sigue siendo un [`Job`]({{ "/es/glosario/job/" | relative_url }}).** Pasale un padre (`CompletableDeferred(parent = job)`) si debe cancelarse con un scope; si no, no tiene dueño.
- **`complete()` devuelve `Boolean`.** `false` significa que ya estaba completado — un "el primero gana" barato sin lock.
- Ver [Launch vs Async/Await]({{ "/es/02-coroutines-flow/launch-vs-async-await/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
