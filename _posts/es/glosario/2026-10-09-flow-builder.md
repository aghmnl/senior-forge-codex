---
layout: post
title: "flow { }"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [flow, coroutines]
lang: es
permalink: /es/glosario/flow-builder/
---

## The Theory (El Qué)

**`flow { }`** es el builder básico de un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) cold. Su bloque corre cada vez que alguien colecta, y [produce]({{ "/es/glosario/produce/" | relative_url }}) valores llamando a `emit(value)`, una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) que le entrega cada valor al [collector]({{ "/es/glosario/collector/" | relative_url }}) y espera a que se haya procesado.

```kotlin
// Not found in FAS — standalone example
fun countdown(from: Int): Flow<Int> = flow {
    for (i in from downTo 0) {
        emit(i)
        delay(1_000)
    }
}
```

## The Senior Nuance (El Matiz Senior)

- **Secuencial y de una sola [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) por contrato.** Cada [`emit`]({{ "/es/glosario/emit/" | relative_url }}) tiene que ocurrir en la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) que colecta: emitir desde [`launch`]({{ "/es/glosario/launch/" | relative_url }}), [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}) o un [callback]({{ "/es/glosario/callbacks/" | relative_url }}) en otro [thread]({{ "/es/glosario/thread/" | relative_url }}) falla en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) ("[Flow]({{ "/es/glosario/flow/" | relative_url }}) invariant is violated"). Para cambiar de [thread]({{ "/es/glosario/thread/" | relative_url }}) se usa [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}); para emitir desde varias [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) o un [callback]({{ "/es/glosario/callbacks/" | relative_url }}), [`channelFlow`]({{ "/es/glosario/channel-flow/" | relative_url }}) o [`callbackFlow`]({{ "/es/glosario/callback-flow/" | relative_url }}).
- **Es el builder más barato**: sin [channel]({{ "/es/glosario/channel/" | relative_url }}) ni buffer, los valores van directo del productor al [collector]({{ "/es/glosario/collector/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
