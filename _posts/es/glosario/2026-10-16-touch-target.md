---
layout: post
title: "Touch Target"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, layout, design-principles]
lang: es
permalink: /es/glosario/touch-target/
---

## The Theory (El Qué)

El **touch target** (área táctil) es la zona de la pantalla que responde a un toque. Las guías de accesibilidad de Android piden por lo menos **48 x 48 dp**, aunque el elemento visible sea más chico. `Modifier.minimumInteractiveComponentSize()` agranda el área táctil hasta ese mínimo sin cambiar cómo se ve el elemento.

```kotlin
// Not found in FAS — standalone example
Icon(Icons.Default.Close, null, Modifier.minimumInteractiveComponentSize().clickable { onClose() })
```

## The Senior Nuance (El Matiz Senior)

- **Un ícono chico no es un área táctil chica**: un ícono de 18 dp puede y debe tener un área de 48 dp.
- **Los componentes de Material ya lo hacen**; los elementos clickeables propios lo tienen que hacer ellos mismos.
- Ver [Modifiers: Order & Alignment]({{ "/es/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
