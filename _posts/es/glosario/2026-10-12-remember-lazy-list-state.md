---
layout: post
title: "rememberLazyListState"
date: 2026-10-12 12:00:00 +0000
categories: [es, glosario]
tags: [compose, state-management]
lang: es
permalink: /es/glosario/remember-lazy-list-state/
---

## The Theory (El Qué)

**`rememberLazyListState()`** crea y recuerda el `LazyListState` de un [`LazyColumn`]({{ "/es/glosario/lazy-column/" | relative_url }}) o `LazyRow`: el primer ítem visible, su offset de scroll, y funciones como `scrollToItem` y `animateScrollToItem`. Está construido sobre [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}), así que la posición del scroll sobrevive a los [cambios de configuración]({{ "/es/glosario/configuration-change/" | relative_url }}) y a la [muerte del proceso]({{ "/es/glosario/process-death/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
val listState = rememberLazyListState()
LazyColumn(state = listState) { /* ... */ }
```

## The Senior Nuance (El Matiz Senior)

- **Elevarlo cuando otro lo necesita**, como un botón de "volver arriba" o una toolbar que reacciona al scroll.
- **Leer `firstVisibleItemIndex` directamente recompone en cada scroll**; los valores derivados van en [`derivedStateOf`]({{ "/es/glosario/derived-state/" | relative_url }}).
- Ver [remember & rememberSaveable]({{ "/es/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
