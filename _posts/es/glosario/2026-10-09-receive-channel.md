---
layout: post
title: "ReceiveChannel"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [concurrency, coroutines]
lang: es
permalink: /es/glosario/receive-channel/
---

## The Theory (El Qué)

**`ReceiveChannel<T>`** es el **lado [receptor]({{ "/es/glosario/receive/" | relative_url }})** de un [Channel]({{ "/es/glosario/channel/" | relative_url }}): la interfaz con [`receive`]({{ "/es/glosario/receive/" | relative_url }}), `tryReceive`, la iteración (`for (x in channel)`) y [`cancel`]({{ "/es/glosario/cancel/" | relative_url }}). Un [`Channel`]({{ "/es/glosario/channel/" | relative_url }}) implementa tanto `SendChannel` como `ReceiveChannel`; exponer solo el tipo `ReceiveChannel` le permite a una clase entregar un [channel]({{ "/es/glosario/channel/" | relative_url }}) que otros pueden leer pero no escribir. `produce { }` devuelve uno.

```kotlin
// Not found in FAS — standalone example
fun CoroutineScope.ticks(): ReceiveChannel<Int> = produce {
    var n = 0
    while (true) { send(n++); delay(1_000) }
}
```

## The Senior Nuance (El Matiz Senior)

- **Es la vista de solo lectura de un [channel]({{ "/es/glosario/channel/" | relative_url }})**, la misma idea que exponer [`StateFlow`]({{ "/es/glosario/stateflow/" | relative_url }}) en lugar de [`MutableStateFlow`]({{ "/es/glosario/mutable-state-flow/" | relative_url }}).
- **[`cancel()`]({{ "/es/glosario/cancel/" | relative_url }}) le pertenece al [receptor]({{ "/es/glosario/receive/" | relative_url }}).** El [consumidor]({{ "/es/glosario/producer-consumer/" | relative_url }}) avisa "terminé de leer" con [`cancel()`]({{ "/es/glosario/cancel/" | relative_url }}); el [productor]({{ "/es/glosario/producer-consumer/" | relative_url }}) cierra con [`close()`]({{ "/es/glosario/close/" | relative_url }}) del lado del `SendChannel`.
- **La mayor parte del código de UI nunca lo ve**: `receiveAsFlow()` lo convierte en un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}), así que el [consumidor]({{ "/es/glosario/producer-consumer/" | relative_url }}) trabaja con operadores y colección consciente del ciclo de vida.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
