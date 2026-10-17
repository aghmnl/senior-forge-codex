---
layout: post
title: "Arrangement"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, layout]
lang: es
permalink: /es/glosario/arrangement/
---

## The Theory (El Qué)

**`Arrangement`** decide cómo un [`Row`]({{ "/es/glosario/row/" | relative_url }}) o un [`Column`]({{ "/es/glosario/column/" | relative_url }}) **distribuye a sus hijos sobre su [eje principal]({{ "/es/glosario/main-axis-cross-axis/" | relative_url }})**: `Start`, `End`, `Center`, `SpaceBetween`, `SpaceAround`, `SpaceEvenly`, o un espacio fijo con `spacedBy(8.dp)`.

```kotlin
// Not found in FAS — standalone example
Row(horizontalArrangement = Arrangement.SpaceBetween) { Text("Total"); Text("$42") }
```

## The Senior Nuance (El Matiz Senior)

- **`spacedBy` es mejor que padding en cada hijo**: el espaciado le pertenece al padre, así que agregar o quitar hijos lo mantiene consistente.
- Ver [Modifiers: Order & Alignment]({{ "/es/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
