---
layout: post
title: "drawBehind"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, layout, performance]
lang: es
permalink: /es/glosario/draw-behind/
---

## The Theory (El Qué)

**`Modifier.drawBehind { }`** dibuja gráficos propios detrás del contenido, usando un `DrawScope` (líneas, círculos, paths). El estado que se lee adentro de su lambda se lee en la **[fase de dibujo]({{ "/es/glosario/compose-phases/" | relative_url }})**, así que un valor que cambia seguido solo vuelve a dibujar, sin [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
Box(Modifier.drawBehind { drawCircle(color, radius = progress.value * size.minDimension / 2) })
```

## The Senior Nuance (El Matiz Senior)

- **`drawWithContent`** es su hermano cuando hay que dibujar tanto detrás como encima del contenido.
- Ver [Modifiers: Order & Alignment]({{ "/es/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
