---
layout: post
title: "Intent Signaling"
date: 2026-08-21 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/intent-signaling/
---

## La Teoría (El Qué)

**Intent signaling** (señalización de intención) es la práctica de elegir construcciones del lenguaje, convenciones de nombres o patrones que comunican el *propósito* del código a futuros lectores — no solo qué hace el código, sino por qué fue escrito de esta manera. En Kotlin, este concepto es particularmente visible con las [scope functions]({{ "/es/01-kotlin-core/scope-functions/" | relative_url }}): usar `apply` señala "estoy configurando este objeto," mientras que `let` señala "estoy transformando este valor." El código compila y ejecuta de forma idéntica de cualquier forma, pero la elección le dice al lector lo que el desarrollador intentaba.

## El Matiz Senior

- El intent signaling es lo que separa el código que "funciona" del código que es mantenible. Un ingeniero Senior escribe código para el próximo desarrollador, no solo para el compilador.
- Más allá de las scope functions, el intent signaling aplica a: elegir `val` sobre `var` (señalando inmutabilidad), usar [sealed classes]({{ "/es/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}) sobre enums (señalando que los subtipos llevan datos), nombrar una función `computeX` vs. `getX` (señalando costo), o retornar `Result<T>` vs. lanzar excepciones (señalando fallo esperado).
- En code reviews, las señales de intención desalineadas son un flag común: código que usa `apply` pero realmente transforma, o código que usa `also` pero modifica el objeto, sugiere que el desarrollador no consideró completamente la naturaleza de la operación.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
