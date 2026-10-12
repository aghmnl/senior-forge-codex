---
layout: post
title: "ProducerScope"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, concurrency]
lang: es
permalink: /es/glosario/producer-scope/
---

## The Theory (El Qué)

**`ProducerScope<T>`** es el receptor de los bloques de `produce { }`, `channelFlow { }` y `callbackFlow { }`. Es a la vez un [`CoroutineScope`]({{ "/es/glosario/coroutine-scope/" | relative_url }}) (se puede hacer [`launch`]({{ "/es/glosario/launch/" | relative_url }}) adentro) y un `SendChannel<T>` (se puede hacer [`send`]({{ "/es/glosario/send/" | relative_url }}), [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) y [`close`]({{ "/es/glosario/close/" | relative_url }})), y expone el [channel]({{ "/es/glosario/channel/" | relative_url }}) mismo como [`channel`]({{ "/es/glosario/channel/" | relative_url }}).

## The Senior Nuance (El Matiz Senior)

- **Que sea un scope importa.** Las [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) lanzadas adentro son hijas del productor, así que se cancelan cuando la colección se detiene; así es como [`channelFlow`]({{ "/es/glosario/channel-flow/" | relative_url }}) combina varias fuentes de forma segura.
- **Que sea un [`SendChannel`]({{ "/es/glosario/send-channel/" | relative_url }}) también importa**: [`close()`]({{ "/es/glosario/close/" | relative_url }}) y `close(cause)` terminan el stream desde adentro, que es como un [callback]({{ "/es/glosario/callbacks/" | relative_url }}) informa el final o un error.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
