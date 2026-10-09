---
layout: post
title: "consumeAsFlow"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [flow, coroutines, cancellation]
lang: es
permalink: /es/glosario/consume-as-flow/
---

## The Theory (El Qué)

**`consumeAsFlow()`** expone un [Channel]({{ "/es/glosario/channel/" | relative_url }}) como [`Flow`]({{ "/es/glosario/flow/" | relative_url }}), igual que [`receiveAsFlow`]({{ "/es/glosario/receive-as-flow/" | relative_url }}), pero **se queda con la propiedad**: el [flow]({{ "/es/glosario/flow/" | relative_url }}) se puede colectar **una sola vez** (un segundo [`collect`]({{ "/es/glosario/collect/" | relative_url }}) lanza una [`IllegalStateException`]({{ "/es/glosario/illegal-state-exception/" | relative_url }})), y cuando esa colección termina, normalmente, con un error o por cancelación, **cancela el [channel]({{ "/es/glosario/channel/" | relative_url }})**.

```kotlin
// Not found in FAS — standalone example
val progress = Channel<Int>(Channel.CONFLATED)
progress.consumeAsFlow()          // una colección; el channel muere con ella
    .map { "$it%" }
    .collect { label.text = it }
```

## The Senior Nuance (El Matiz Senior)

- **La propiedad es toda la diferencia.** [`receiveAsFlow`]({{ "/es/glosario/receive-as-flow/" | relative_url }}) presta el [channel]({{ "/es/glosario/channel/" | relative_url }}) y lo deja abierto; `consumeAsFlow` se lo da al [collector]({{ "/es/glosario/collector/" | relative_url }}) y lo cierra cuando ese [collector]({{ "/es/glosario/collector/" | relative_url }}) termina.
- **Mala elección para el [channel]({{ "/es/glosario/channel/" | relative_url }}) de [eventos]({{ "/es/glosario/one-shot-event/" | relative_url }}) de un [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}).** Ahí la colección se cancela cada vez que la pantalla pasa a background; con `consumeAsFlow`, esa primera cancelación mata el [channel]({{ "/es/glosario/channel/" | relative_url }}) y la siguiente colección lanza una excepción.
- **Buena elección cuando el [channel]({{ "/es/glosario/channel/" | relative_url }}) existe para una sola colección**, y liberarlo junto con esa colección es exactamente lo que se quiere.
- Ver [receiveAsFlow()]({{ "/es/02-coroutines-flow/receive-as-flow/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
