---
layout: post
title: "Compose Phases"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, layout, performance]
lang: es
permalink: /es/glosario/compose-phases/
---

## The Theory (El Qué)

Compose dibuja un frame en tres fases: **[composition]({{ "/es/glosario/composition/" | relative_url }})** (ejecutar los composables y decidir qué mostrar), **layout** (medir y ubicar cada elemento) y **dibujo** (pintar los píxeles). El estado que se lee en una fase solo vuelve a correr esa fase y las siguientes, y por eso los [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) con lambda como `offset { }`, `graphicsLayer { }` y `drawBehind { }` son más baratos para valores que cambian en cada frame.

## The Senior Nuance (El Matiz Senior)

- **Diferir las lecturas de estado a la última fase que las necesita**: la [composition]({{ "/es/glosario/composition/" | relative_url }}) es la más cara de volver a correr, el dibujo la más barata.
- Ver [Modifiers: Order & Alignment]({{ "/es/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
