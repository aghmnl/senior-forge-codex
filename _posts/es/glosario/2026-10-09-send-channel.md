---
layout: post
title: "SendChannel"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [concurrency, coroutines]
lang: es
permalink: /es/glosario/send-channel/
---

## The Theory (El Qué)

**`SendChannel<T>`** es el **lado emisor** de un [Channel]({{ "/es/glosario/channel/" | relative_url }}): la interfaz con [`send`]({{ "/es/glosario/send/" | relative_url }}), [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) y [`close`]({{ "/es/glosario/close/" | relative_url }}). Un [`Channel`]({{ "/es/glosario/channel/" | relative_url }}) implementa tanto `SendChannel` como [`ReceiveChannel`]({{ "/es/glosario/receive-channel/" | relative_url }}); entregar solo el tipo `SendChannel` permite que otro código produzca valores sin poder consumirlos.

## The Senior Nuance (El Matiz Senior)

- **[`close()`]({{ "/es/glosario/close/" | relative_url }}) le pertenece al emisor.** Significa "no hay más valores": los receptores vacían lo que está en el buffer y después terminan. El lado receptor, en cambio, corta antes con [`cancel()`]({{ "/es/glosario/cancel/" | relative_url }}).
- **[`ProducerScope`]({{ "/es/glosario/producer-scope/" | relative_url }}) es un `SendChannel`**, por eso [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) y [`close`]({{ "/es/glosario/close/" | relative_url }}) están disponibles directamente adentro de [`callbackFlow`]({{ "/es/glosario/callback-flow/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
