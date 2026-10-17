---
layout: post
title: "clickable"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, layout, callbacks]
lang: es
permalink: /es/glosario/clickable/
---

## The Theory (El Qué)

**`Modifier.clickable { }`** hace que un elemento responda a toques, muestra la indicación de presión (el [ripple]({{ "/es/glosario/ripple/" | relative_url }})), y lo expone a los servicios de accesibilidad como un botón. Su [área táctil]({{ "/es/glosario/touch-target/" | relative_url }}) es el espacio que envuelve, así que su posición en la cadena decide cuánto del elemento se puede tocar.

```kotlin
// Not found in FAS — standalone example
Icon(Icons.Default.Close, null, Modifier.clickable { onClose() }.padding(12.dp))   // padding is tappable
```

## The Senior Nuance (El Matiz Senior)

- **Antes de un padding, el padding es tocable; después, no.**
- **Poner [`clip`]({{ "/es/glosario/clip/" | relative_url }}) antes** para que el [ripple]({{ "/es/glosario/ripple/" | relative_url }}) siga la forma.
- Ver [Modifiers: Order & Alignment]({{ "/es/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
