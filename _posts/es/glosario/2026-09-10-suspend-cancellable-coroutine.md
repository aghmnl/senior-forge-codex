---
layout: post
title: "suspendCancellableCoroutine"
date: 2026-09-10 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/suspend-cancellable-coroutine/
---

## The Theory (El Qué)

**`suspendCancellableCoroutine { cont -> }`** es la primitiva que convierte una API basada en [callbacks]({{ "/es/glosario/callbacks/" | relative_url }}) en una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}). Suspende la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}), te entrega su [Continuation]({{ "/es/glosario/continuation/" | relative_url }}), y se reanuda cuando llamás `cont.resume(value)` o `cont.resumeWithException(e)`. La variante *cancellable* además te deja registrar `invokeOnCancellation { }` para desmontar el callback si el llamador se cancela.

```kotlin
// Not found in FAS — standalone example
suspend fun LocationClient.awaitLastLocation(): Location? =
    suspendCancellableCoroutine { cont ->
        val listener = object : LocationListener {
            override fun onSuccess(loc: Location?) = cont.resume(loc)
            override fun onFailure(e: Exception) = cont.resumeWithException(e)
        }
        requestLastLocation(listener)
        cont.invokeOnCancellation { removeListener(listener) }
    }
```

Así es como Jetpack convirtió `CredentialManager`, `Task<T>` (`await()`), `ListenableFuture` y similares en APIs suspendibles — una vez, en el borde.

## The Senior Nuance (El Matiz Senior)

- **Tres obligaciones.** Reanudar exactamente una vez; propagar fallos con `resumeWithException`; desregistrar en la cancelación. Olvidar la tercera filtra el listener; olvidar la primera cuelga al llamador para siempre.
- **Preferila sobre `suspendCoroutine`.** La variante no cancelable ignora la [cooperative cancellation]({{ "/es/glosario/cooperative-cancellation/" | relative_url }}): un llamador cancelado queda suspendido hasta que el callback dispara, si es que alguna vez lo hace.
- **`callbackFlow` es el equivalente multi-shot.** Un callback → `suspendCancellableCoroutine`; un stream de callbacks → `callbackFlow` con `awaitClose`.
- **Rara vez la necesitás en código de app.** Room, Retrofit, DataStore, Credential Manager y Play Services ya traen APIs suspendibles. Usala solo al envolver un SDK legacy.
- Ver [Suspend Functions]({{ "/es/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
