---
layout: post
title: "ChannelResult"
date: 2026-10-02 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, concurrency, error-handling]
lang: es
permalink: /es/glosario/channel-result/
---

## The Theory (El Qué)

**`ChannelResult`** es lo que devuelve [trySend]({{ "/es/glosario/try-send/" | relative_url }}): un valor chico que dice cómo salió el intento. Tiene tres propiedades: **`isSuccess`** (el valor se agregó), **`isFailure`** (no se agregó, por ejemplo porque el buffer estaba lleno) e **`isClosed`** (no se agregó porque el channel está [cerrado]({{ "/es/glosario/close/" | relative_url }})). Un resultado de cerrado también es una falla, así que en ese caso `isFailure` también es `true`. Nunca lanza: el resultado está en el valor devuelto, y es quien llama el que lo tiene que mirar.

```kotlin
// Not found in FAS — standalone example
val result = channel.trySend(event)
when {
    result.isSuccess -> Unit
    result.isClosed -> Log.w(TAG, "Channel cerrado, evento descartado")
    result.isFailure -> Log.w(TAG, "Buffer lleno, evento descartado")
}
```

## The Senior Nuance (El Matiz Senior)

- **Ignorarlo es la forma en que los valores se pierden en silencio.** Un `trySend` que falla no produce ningún error ni log salvo que el código revise el resultado.
- **Revisá `isClosed` antes que `isFailure`.** Como un resultado de cerrado también es una falla, el orden importa cuando cada caso necesita un manejo distinto. Los helpers `onSuccess`, `onFailure` y `onClosed` siguen la misma regla: `onFailure` también corre con el channel cerrado.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
