---
layout: post
title: "graphicsLayer"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, layout, performance]
lang: es
permalink: /es/glosario/graphics-layer/
---

## The Theory (El Qué)

**`Modifier.graphicsLayer { }`** aplica transformaciones al momento de dibujar: escala, rotación, traslación, alpha, sombra y recorte. Su forma con lambda lee el estado en la **[fase de dibujo]({{ "/es/glosario/compose-phases/" | relative_url }})**, así que animar estos valores no recompone ni vuelve a hacer el layout del composable.

```kotlin
// Not found in FAS — standalone example
Box(Modifier.graphicsLayer { alpha = fade.value; scaleX = zoom.value })
```

## The Senior Nuance (El Matiz Senior)

- **La forma más barata de animar propiedades visuales**, porque solo vuelve a correr la [fase de dibujo]({{ "/es/glosario/compose-phases/" | relative_url }}).
- **No cambia el layout**: un elemento escalado sigue ocupando su espacio original.
- Ver [Modifiers: Order & Alignment]({{ "/es/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
