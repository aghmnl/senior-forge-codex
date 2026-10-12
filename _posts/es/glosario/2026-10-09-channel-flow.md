---
layout: post
title: "channelFlow"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [flow, coroutines, concurrency]
lang: es
permalink: /es/glosario/channel-flow/
---

## The Theory (El Qué)

**`channelFlow { }`** construye un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) cold cuyo bloque corre en un [`ProducerScope`]({{ "/es/glosario/producer-scope/" | relative_url }}): los valores se envían a un [channel]({{ "/es/glosario/channel/" | relative_url }}) interno con [`send`]({{ "/es/glosario/send/" | relative_url }}) o [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}), así que pueden venir de **varias [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) a la vez** o de otro [thread]({{ "/es/glosario/thread/" | relative_url }}), algo que [`flow { }`]({{ "/es/glosario/flow-builder/" | relative_url }}) prohíbe.

```kotlin
// Not found in FAS — standalone example
fun search(query: String): Flow<Result> = channelFlow {
    launch { send(localSource.find(query)) }    // los dos corren en paralelo
    launch { send(remoteSource.find(query)) }
}
```

## The Senior Nuance (El Matiz Senior)

- **[`callbackFlow`]({{ "/es/glosario/callback-flow/" | relative_url }}) es un `channelFlow` que exige [`awaitClose`]({{ "/es/glosario/await-close/" | relative_url }}).** `channelFlow` va cuando el propio bloque hace el trabajo y termina; [`callbackFlow`]({{ "/es/glosario/callback-flow/" | relative_url }}) cuando los valores vienen de un [callback]({{ "/es/glosario/callbacks/" | relative_url }}) registrado que hay que desregistrar.
- **Cuesta un [channel]({{ "/es/glosario/channel/" | relative_url }}).** Para un único productor secuencial, [`flow { }`]({{ "/es/glosario/flow-builder/" | relative_url }}) es más simple y barato.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
