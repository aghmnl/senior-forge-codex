---
layout: post
title: "CoroutineStart"
date: 2026-09-16 12:00:00 +0000
categories: [es, glosario]
tags: [coroutines, syntax]
lang: es
permalink: /es/glosario/coroutine-start/
---

## The Theory (El Qué)

**`CoroutineStart`** es el enum que se pasa como parámetro `start` de [`launch`]({{ "/es/glosario/launch/" | relative_url }}) y [`async`]({{ "/es/glosario/async/" | relative_url }}) y decide *cuándo* empieza a ejecutarse el bloque de la coroutine nueva:

- **`DEFAULT`** — se agenda de inmediato en el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}); corre en su primera oportunidad.
- **`LAZY`** — se crea pero no se arranca. Corre solo cuando alguien llama a [`start()`]({{ "/es/glosario/start/" | relative_url }}), [`join()`]({{ "/es/glosario/join/" | relative_url }}) o [`await()`]({{ "/es/glosario/await/" | relative_url }}) sobre ella. Un [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) lazy es un cómputo memoizado, cancelable y bajo demanda.
- **`ATOMIC`** — como `DEFAULT`, pero no se puede cancelar antes de su primer [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}). Rara vez necesario.
- **`UNDISPATCHED`** — empieza a ejecutarse *en el thread del llamador* hasta la primera suspensión, y después sigue en el dispatcher. Nivel framework.

```kotlin
// Not found in FAS — standalone example
val config = async(start = CoroutineStart.LAZY) { loadConfig() }   // nothing runs yet
// ... later, only if actually needed:
val c = config.await()                                              // starts it now
```

## The Senior Nuance (El Matiz Senior)

- **`LAZY` es el que vale la pena conocer.** Expresa "calculá esto a lo sumo una vez, solo si alguien lo pide" sin un `by lazy` manual más malabares de scope.
- **Un hijo lazy que nunca se arranca bloquea a su padre.** [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) espera a todos los hijos, incluido uno `LAZY` que nadie esperó — el padre nunca completa. O lo esperás, o `start()`, o `cancel()`.
- **El resto es para código de librería.** `ATOMIC` y `UNDISPATCHED` están marcados como delicados por algo; en código de aplicación la respuesta es casi siempre `DEFAULT`.
- Ver [Launch vs Async/Await]({{ "/es/02-coroutines-flow/launch-vs-async-await/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
