---
layout: post
title: "Modifier.offset"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [compose, performance]
lang: es
permalink: /es/glosario/modifier-offset/
---

## The Theory (El Qué)

**`Modifier.offset`** desplaza un composable de su posición de layout. Tiene dos formas: `offset(x, y)` recibe los valores directamente, así que leer un estado que cambia para pasarlos recompone el composable; `offset { IntOffset(x, y) }` recibe una [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) que se evalúa en la **fase de layout**, así que un valor que cambia se lee ahí y la [composition]({{ "/es/glosario/composition/" | relative_url }}) no vuelve a correr.

```kotlin
// Not found in FAS — standalone example
Box(Modifier.offset { IntOffset(0, scrollState.value / 2) })   // sin recomposition por pixel
```

## The Senior Nuance (El Matiz Senior)

- **Preferir la forma con [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) para valores que cambian en cada frame** (scroll, arrastre, animación). Es el ejemplo clásico de diferir una lectura de estado a una fase posterior.
- **La misma idea aplica a `graphicsLayer { }` y `drawBehind { }`**, que leen el estado en la fase de dibujo.
- Ver [Recomposition & Stability]({{ "/es/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
