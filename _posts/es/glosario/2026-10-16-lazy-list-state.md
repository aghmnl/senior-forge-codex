---
layout: post
title: "LazyListState"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, state-management]
lang: es
permalink: /es/glosario/lazy-list-state/
---

## The Theory (El Qué)

**`LazyListState`** es el [state holder]({{ "/es/glosario/state-holder/" | relative_url }}) de un [`LazyColumn`]({{ "/es/glosario/lazy-column/" | relative_url }}) o `LazyRow`: sabe cuál es el primer ítem visible, su offset de scroll y si la lista se está moviendo, y expone `scrollToItem` y `animateScrollToItem`. Se crea con `rememberLazyListState()` y se pasa a la lista con su parámetro `state`, que es state hoisting de la lógica de UI de la lista.

## The Senior Nuance (El Matiz Senior)

- **Es el modelo de una clase [state holder]({{ "/es/glosario/state-holder/" | relative_url }}) común**: lógica de UI lo bastante compleja para merecer su propia clase, creada y recordada con una función `rememberXState()`.
- **Elevarlo solo hasta donde haga falta**, por ejemplo a la pantalla que también muestra un botón de "volver arriba".
- Ver [State Hoisting]({{ "/es/03-jetpack-compose/state-hoisting/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
