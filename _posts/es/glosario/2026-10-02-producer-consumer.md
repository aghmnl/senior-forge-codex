---
layout: post
title: "Producer-Consumer"
date: 2026-10-02 12:00:00 +0000
categories: [es, glosario]
tags: [concurrency, design-patterns, coroutines]
lang: es
permalink: /es/glosario/producer-consumer/
---

## The Theory (El Qué)

**Productor-consumidor** es el patrón donde una parte del código, el **productor**, genera valores, y otra parte, el **consumidor**, los procesa, conectados por una cola en el medio. Cada lado trabaja a su ritmo: la cola absorbe la diferencia. En coroutines esa cola suele ser un [Channel]({{ "/es/glosario/channel/" | relative_url }}): el productor llama a [send]({{ "/es/glosario/send/" | relative_url }}) y el consumidor [recibe]({{ "/es/glosario/receive/" | relative_url }}). Cuando el productor es más rápido y la cola se llena, el [backpressure]({{ "/es/glosario/backpressure/" | relative_url }}) lo hace esperar.

```kotlin
// Not found in FAS — standalone example
val pages = Channel<List<Task>>(capacity = 2)

launch {                                   // productor
    for (n in 0 until pageCount) pages.send(api.fetchPage(n))
    pages.close()
}
launch {                                   // consumidor
    for (page in pages) dao.insertAll(page)
}
```

## The Senior Nuance (El Matiz Senior)

- **La cola desacopla los ritmos, no borra la diferencia.** Si el productor es siempre más rápido, una cola acotada lo hace esperar, y una sin límite crece hasta que se acaba la memoria.
- **Varios consumidores sobre una misma cola se reparten el trabajo:** eso es [fan-out]({{ "/es/glosario/fan-out/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
