---
layout: post
title: "Backpressure"
date: 2026-09-23 12:00:00 +0000
categories: [es, glosario]
tags: [flow, coroutines, performance]
lang: es
permalink: /es/glosario/backpressure/
---

## The Theory (El Qué)

**Backpressure** (contrapresión) es lo que ocurre cuando un productor emite más rápido de lo que su consumidor puede procesar. Un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) lo resuelve por construcción: [`emit`]({{ "/es/glosario/emit/" | relative_url }}) es una función suspendible que no retorna hasta que el colector terminó con ese valor, así que un consumidor lento simplemente frena al productor — ninguna cola crece, ningún valor se descarta, nada se pierde. Salirse de eso es explícito: [`buffer`]({{ "/es/glosario/buffer/" | relative_url }}) los desacopla con un channel, `conflate()` se queda solo con el último, y [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) bufferea como efecto secundario.

```kotlin
// Not found in FAS — standalone example
// Secuencial: tiempo total ≈ productor + consumidor
pages().collect { render(it) }

// Desacoplado: el productor se adelanta, la memoria crece
pages().buffer().collect { render(it) }

// Solo el último: no crece, se descartan los valores intermedios
pages().conflate().collect { render(it) }
```

## The Senior Nuance (El Matiz Senior)

- **El default es el seguro.** El backpressure por suspensión no puede desbordar la memoria, a diferencia de una API de callbacks que sigue empujando. Ese es uno de los argumentos más fuertes a favor de los flows sobre los listeners.
- **Para estado de UI, `conflate()` suele ser lo correcto.** Renderizar cada valor intermedio de un stream rápido es trabajo desperdiciado: la pantalla solo muestra el último.
- **Un buffer sin límite es un leak disfrazado.** `buffer(Channel.UNLIMITED)` delante de un colector lento crece hasta que el proceso muere; elegí una capacidad o conflatá.
- Ver [Flow (Cold Streams)]({{ "/es/02-coroutines-flow/flow-cold-streams/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
