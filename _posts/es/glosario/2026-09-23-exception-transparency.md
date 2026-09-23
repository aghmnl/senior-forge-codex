---
layout: post
title: "Exception Transparency"
date: 2026-09-23 12:00:00 +0000
categories: [es, glosario]
tags: [flow, error-handling, coroutines]
lang: es
permalink: /es/glosario/exception-transparency/
---

## The Theory (El Qué)

La **transparencia a las excepciones** es el contrato de [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) que exige que un productor deje viajar las excepciones hasta su colector en vez de atrapar sus propias emisiones. Un builder `flow { }` que envuelve su [`emit`]({{ "/es/glosario/emit/" | relative_url }}) en un `try/catch` lo viola y falla en runtime con `Flow exception transparency is violated`. La forma autorizada de manejar una falla es el operador [`catch`]({{ "/es/glosario/catch/" | relative_url }}), y por eso `catch` solo ve su [upstream]({{ "/es/glosario/upstream/" | relative_url }}): el pipeline sigue siendo una cadena de declaraciones cuyas fallas son atribuibles a un segmento concreto.

```kotlin
// Not found in FAS — standalone example
// Viola la transparencia: lanza "Flow exception transparency is violated"
flow {
    try { emit(load()) } catch (e: IOException) { emit(fallback()) }
}

// Correcto: el productor se mantiene transparente, catch lo maneja downstream
flow { emit(load()) }
    .catch { emit(fallback()) }
```

## The Senior Nuance (El Matiz Senior)

- **Es lo que hace predecible a `catch`.** Como ningún operador puede tragarse sus propias emisiones, una falla siempre aparece en el primer `catch` debajo del segmento que la produjo — podés leer la cadena y saber quién maneja qué.
- **`catch` no puede alcanzar el [downstream]({{ "/es/glosario/downstream/" | relative_url }}).** Una excepción lanzada adentro de `collect` no es una falla del productor, así que el operador de arriba no la ve. Es la misma regla, vista desde el otro extremo.
- **Un `try/catch` alrededor de tu propio trabajo que *no* emite está bien.** La transparencia es sobre las emisiones, no sobre cada sentencia dentro del builder.
- Ver [Error Handling: try-catch & .catch]({{ "/es/02-coroutines-flow/error-handling/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
