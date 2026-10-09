---
layout: post
title: "receiveAsFlow"
date: 2026-09-28 12:00:00 +0000
categories: [es, glosario]
tags: [flow, concurrency, coroutines]
lang: es
permalink: /es/glosario/receive-as-flow/
---

## The Theory (El Qué)

**`receiveAsFlow()`** expone un [Channel]({{ "/es/glosario/channel/" | relative_url }}) como [Flow]({{ "/es/glosario/flow/" | relative_url }}). [Colectarlo]({{ "/es/glosario/collect/" | relative_url }}) recibe valores del channel, así que el resultado conserva la semántica del channel: es **hot**, los valores enviados antes de que alguien colecte esperan en el buffer del channel, y **cada valor va a exactamente un collector**. Es la forma habitual de exponer un channel de [eventos]({{ "/es/glosario/one-shot-event/" | relative_url }}) de una sola vez desde un ViewModel sin exponer `send`.

```kotlin
// Not found in FAS — standalone example
private val _events = Channel<UiEvent>(Channel.BUFFERED)
val events: Flow<UiEvent> = _events.receiveAsFlow()
```

## The Senior Nuance (El Matiz Senior)

- **Reparto, no difusión.** Con dos collectors, cada valor va a uno de ellos. Si las dos pantallas tienen que ver cada valor, la primitiva es un [SharedFlow]({{ "/es/glosario/sharedflow/" | relative_url }}), no un channel.
- **`receiveAsFlow` vs [`consumeAsFlow`]({{ "/es/glosario/consume-as-flow/" | relative_url }}).** `receiveAsFlow` se puede colectar muchas veces, una tras otra o en paralelo, y cancelar un collector deja el channel abierto. [`consumeAsFlow`]({{ "/es/glosario/consume-as-flow/" | relative_url }}) se puede colectar una sola vez y cancela el channel cuando esa colección termina; una segunda colección lanza una excepción.
- **Un valor tomado es un valor que ya no está.** Una vez que un collector recibe un [evento]({{ "/es/glosario/one-shot-event/" | relative_url }}), sale del channel. Si ese collector se cancela antes de manejarlo, por ejemplo durante un cambio de configuración, el [evento]({{ "/es/glosario/one-shot-event/" | relative_url }}) se pierde.
- Ver [receiveAsFlow()]({{ "/es/02-coroutines-flow/receive-as-flow/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
