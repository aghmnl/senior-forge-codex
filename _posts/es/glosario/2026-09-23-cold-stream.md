---
layout: post
title: "Cold Stream"
date: 2026-09-23 12:00:00 +0000
categories: [es, glosario]
tags: [flow, coroutines, performance]
lang: es
permalink: /es/glosario/cold-stream/
---

## The Theory (El Qué)

Un **cold stream** (stream frío) produce sus valores solo cuando alguien lo consume, y los vuelve a producir desde cero para cada consumidor. Un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) es el ejemplo de Kotlin: construirlo y encadenarle operadores no ejecuta nada; el productor arranca en el [operador terminal]({{ "/es/glosario/terminal-operations/" | relative_url }}) y se detiene cuando se cancela el scope del colector. Lo opuesto es un stream *hot* — [`StateFlow`]({{ "/es/glosario/stateflow/" | relative_url }}), `SharedFlow`, un `Channel` — que está corriendo y manteniendo valores haya o no alguien escuchando.

```kotlin
// Not found in FAS — standalone example
val cold = flow {
    println("produciendo")   // se imprime una vez POR colector
    emit(1)
}

cold.collect { }             // imprime "produciendo"
cold.collect { }             // vuelve a imprimirlo — ejecución independiente
```

## The Senior Nuance (El Matiz Senior)

- **Cold significa trabajo duplicado, no compartido.** Dos colectores sobre un flow respaldado por [Room]({{ "/es/glosario/room/" | relative_url }}) son dos queries y dos observadores. Compartir una sola ejecución es para lo que están `shareIn`/`stateIn`.
- **Cold significa cero efectos secundarios al crearlo.** Un repositorio puede devolver un stream sin ser dueño de un [scope]({{ "/es/glosario/coroutine-scope/" | relative_url }}) ni de un ciclo de vida, y eso es lo que hace fácil de testear la capa de datos.
- **Un cold stream que nadie colecta no hace nada, en silencio.** Sin error y sin log — la causa más común de "mi flow no funciona".
- Ver [Flow (Cold Streams)]({{ "/es/02-coroutines-flow/flow-cold-streams/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
