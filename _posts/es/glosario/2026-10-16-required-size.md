---
layout: post
title: "requiredSize"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, layout]
lang: es
permalink: /es/glosario/required-size/
---

## The Theory (El Qué)

**`Modifier.requiredSize(...)`** fija un tamaño que **ignora las [constraints]({{ "/es/glosario/constraints/" | relative_url }}) recibidas**, a diferencia de `size`, que las respeta. Si el tamaño requerido no entra, el composable desborda y queda centrado sobre el espacio que le dieron.

```kotlin
// Not found in FAS — standalone example
Box(Modifier.size(50.dp).requiredSize(80.dp))   // 80 dp, overflowing the 50 dp slot
```

## The Senior Nuance (El Matiz Senior)

- **Una herramienta para excepciones**, como un badge que tiene que mantener su tamaño; usarla seguido suele esconder un problema de layout.
- Ver [Modifiers: Order & Alignment]({{ "/es/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
