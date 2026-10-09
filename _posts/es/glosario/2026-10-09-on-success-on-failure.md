---
layout: post
title: "onSuccess / onFailure"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [callbacks, error-handling]
lang: es
permalink: /es/glosario/on-success-on-failure/
---

## The Theory (El Qué)

**`onSuccess`** y **`onFailure`** son el par habitual de [callbacks]({{ "/es/glosario/callbacks/" | relative_url }}) de una operación asíncrona que [produce]({{ "/es/glosario/produce/" | relative_url }}) **un solo resultado**: la [API]({{ "/es/glosario/api/" | relative_url }}) llama al primero con el valor cuando funciona, o al segundo con el error cuando no. Los `Task` de Play services (`addOnSuccessListener` / `addOnFailureListener`) y muchos SDKs siguen esta forma. El [`Result`]({{ "/es/glosario/result/" | relative_url }}) de [Kotlin]({{ "/es/glosario/kotlin/" | relative_url }}) tiene funciones con los mismos nombres.

```kotlin
// Not found in FAS — standalone example
appUpdateManager.appUpdateInfo
    .addOnSuccessListener { info -> handle(info) }
    .addOnFailureListener { e -> Log.w(TAG, "Check failed", e) }
```

## The Senior Nuance (El Matiz Senior)

- **Un resultado significa una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}), no un [flow]({{ "/es/glosario/flow/" | relative_url }}).** Se envuelve el par con [`suspendCancellableCoroutine`]({{ "/es/glosario/suspend-cancellable-coroutine/" | relative_url }}): reanudar con el valor en `onSuccess`, reanudar con la excepción en `onFailure`, y quien llama usa un `try`/`catch` común.
- **Se llama exactamente a uno de los dos, exactamente una vez.** El código que supone otra cosa (reanudar dos veces) rompe la [continuation]({{ "/es/glosario/continuation/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
