---
layout: post
title: "Context Preservation"
date: 2026-09-21 12:00:00 +0000
categories: [es, glosario]
tags: [flow, coroutines, concurrency]
lang: es
permalink: /es/glosario/context-preservation/
---

## The Theory (El Qué)

La **preservación del contexto** es la invariante de [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) que exige que un flow [emita]({{ "/es/glosario/emit/" | relative_url }}) desde el mismo [contexto de coroutine]({{ "/es/glosario/coroutine-context/" | relative_url }}) en el que es colectado. Emitir desde otro contexto — `flow { withContext(IO) { emit(x) } }` — lanza `IllegalStateException: Flow invariant is violated`. La regla existe para que las emisiones sigan siendo secuenciales y las excepciones rastreables; `flowOn` es la vía autorizada, porque cambia el contexto de todo el [upstream]({{ "/es/glosario/upstream/" | relative_url }}) en vez del de una emisión suelta.

```kotlin
// Not found in FAS — standalone example
// Lanza en runtime: "Flow invariant is violated"
fun roto(): Flow<String> = flow {
    withContext(Dispatchers.IO) { emit(readFile()) }
}

// Correcto: se mueve todo el upstream, las emisiones quedan en un solo contexto
fun correcto(): Flow<String> = flow {
    emit(readFile())
}.flowOn(Dispatchers.IO)
```

## The Senior Nuance (El Matiz Senior)

- **El chequeo es en runtime, no en compilación.** Un `withContext` dentro de un builder `flow { }` compila sin problema y falla en la primera emisión — muchas veces solo en un dispositivo, en un camino que los tests no cubren.
- **`channelFlow` es la vía de escape.** Cuando de verdad necesitás emitir desde varias coroutines (unir callbacks, productores en paralelo), `channelFlow { send(...) }` es seguro para concurrencia por diseño; un `flow { }` común no lo es.
- **La invariante es la razón por la que `flowOn` necesita un channel.** Cruzar un límite de dispatcher obliga a pasar los valores a otra coroutine, que es también lo que le da a `flowOn` su comportamiento de [buffering]({{ "/es/glosario/buffer/" | relative_url }}).
- Ver [withContext vs flowOn]({{ "/es/02-coroutines-flow/with-context-vs-flow-on/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
