---
layout: post
title: "Composition"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [compose, state-management]
lang: es
permalink: /es/glosario/composition/
---

## The Theory (El Qué)

La **Composition** (composición) es el árbol que [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) construye al ejecutar funciones [`@Composable`]({{ "/es/glosario/composable/" | relative_url }}). Registra qué emitió cada función (los nodos de UI), los valores que recordó con [`remember`]({{ "/es/glosario/remember/" | relative_url }}) y qué estado leyó. Compose la mantiene en memoria y la actualiza en el lugar: la [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}) cambia las partes cuyo estado cambió, en lugar de construirla de nuevo.

## The Senior Nuance (El Matiz Senior)

- **Es una descripción, no la pantalla.** La composition es la primera de tres fases (composition, layout, dibujo). Un cambio que solo afecta el layout o el dibujo puede saltearse esta fase por completo.
- **Salir de la composition termina la vida de un composable**: sus valores recordados se olvidan y sus efectos se cancelan o se liberan.
- Ver [Recomposition & Stability]({{ "/es/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
