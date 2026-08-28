---
layout: post
title: "Señalización de Intención (Intent Signaling)"
date: 2026-08-21 12:00:00 +0000
categories: [es, glossary]
lang: es
permalink: /es/glosario/intent-signaling/
---

## The Theory (El Qué)

La **señalización de intención** (intent signaling) es la práctica de elegir construcciones del lenguaje, convenciones de nombres o patrones que comuniquen el *propósito* del código a futuros lectores — no solo qué hace el código, sino por qué fue escrito de esta manera. En Kotlin, este concepto es particularmente visible con las [scope functions]({{ "/es/01-kotlin-core/scope-functions/" | relative_url }}): usar `apply` señala "estoy configurando este objeto," mientras que `let` señala "estoy transformando este valor." El código compila y ejecuta de forma idéntica en ambos casos, pero la elección le dice al lector qué intentó el desarrollador.

## The Senior Nuance (El Matiz Senior)

- La señalización de intención es lo que separa el código que "funciona" del código mantenible. Un ingeniero Senior escribe código para el siguiente desarrollador, no solo para el compilador.
- Más allá de las scope functions, la señalización de intención aplica a: elegir `val` sobre `var` (señala inmutabilidad), usar [sealed classes]({{ "/es/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}) sobre enums (señala que los subtipos llevan datos), nombrar una función `computeX` vs. `getX` (señala costo), o devolver `Result<T>` en vez de lanzar excepciones (señala fallo esperado).
- En code reviews, las señales de intención desalineadas son una bandera común: código que usa `apply` pero en realidad transforma, o código que usa `also` pero modifica el objeto, sugiere que el desarrollador no consideró completamente la naturaleza de la operación.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
