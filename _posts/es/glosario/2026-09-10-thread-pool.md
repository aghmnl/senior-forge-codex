---
layout: post
title: "Thread Pool"
date: 2026-09-10 12:00:00 +0000
categories: [es, glosario]
tags: [threading, coroutines]
lang: es
permalink: /es/glosario/thread-pool/
---

## The Theory (El Qué)

Un **thread pool** es un conjunto fijo o acotado de [threads]({{ "/es/glosario/thread/" | relative_url }}) pre-creados que toman tareas de una cola compartida, de modo que el trabajo puede agendarse sin pagar la creación de un thread en cada llamada. `Dispatchers.Default` es un pool dimensionado según la cantidad de cores (mínimo 2); `Dispatchers.IO` comparte los mismos threads subyacentes pero permite hasta 64 (o la cantidad de cores, lo que sea mayor) detenidos en [llamadas bloqueantes]({{ "/es/glosario/blocking-call/" | relative_url }}) a la vez. El executor de queries de Room y el dispatcher de conexiones de OkHttp también son pools.

Cuando una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) se reanuda después de un [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}), su [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) encola la [Continuation]({{ "/es/glosario/continuation/" | relative_url }}) en el pool; el próximo thread libre la corre.

## The Senior Nuance (El Matiz Senior)

- **Los pools son la razón por la que "¿en qué thread estoy?" es la pregunta equivocada.** Estás en *un* thread del pool `IO`. Puede ser distinto del que tenías antes de la última suspensión.
- **`IO` está dimensionado para detenerse, `Default` para computar.** Bloquear en `Default` deja sin recursos al trabajo de CPU porque hay tantos threads como cores. Los loops pesados de CPU en `IO` son un desperdicio pero no dañinos. Elegí según la naturaleza del trabajo.
- **`limitedParallelism(n)` talla un sub-pool.** `Dispatchers.IO.limitedParallelism(1)` te da confinamiento single-thread para un SDK legacy no thread-safe sin crear un thread nuevo.
- **Los pools no hacen el código thread-safe.** Dos coroutines en `Default` pueden correr en el mismo instante; el estado mutable compartido necesita [thread safety]({{ "/es/glosario/thread-safety/" | relative_url }}) por construcción.
- Ver [Suspend Functions]({{ "/es/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
