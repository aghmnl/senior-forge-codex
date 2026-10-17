---
layout: post
title: "wrapContentSize"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, layout]
lang: es
permalink: /es/glosario/wrap-content-size/
---

## The Theory (El Qué)

**`Modifier.wrapContentSize()`** permite que el contenido sea **más chico que las [constraints]({{ "/es/glosario/constraints/" | relative_url }}) mínimas** que recibe, y lo alinea adentro de ese espacio (centrado por defecto, o con un argumento `align`). Sin él, un hijo forzado a un tamaño mínimo se estira para llenarlo.

```kotlin
// Not found in FAS — standalone example
Box(Modifier.size(100.dp).wrapContentSize(Alignment.TopStart).size(40.dp))
```

## The Senior Nuance (El Matiz Senior)

- **Útil después de un [modifier]({{ "/es/glosario/modifier/" | relative_url }}) que impone un mínimo**, para mantener el contenido en su tamaño natural y decidir dónde queda.
- Ver [Modifiers: Order & Alignment]({{ "/es/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
