---
layout: post
title: "background"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, layout]
lang: es
permalink: /es/glosario/background/
---

## The Theory (El Qué)

**`Modifier.background(color, shape)`** dibuja un color (o un brush) detrás del contenido, sobre el área que envuelve el [modifier]({{ "/es/glosario/modifier/" | relative_url }}). Un [`padding`]({{ "/es/glosario/padding/" | relative_url }}) antes la achica; un [`clip`]({{ "/es/glosario/clip/" | relative_url }}) antes le da una forma.

```kotlin
// Not found in FAS — standalone example
Box(Modifier.clip(RoundedCornerShape(12.dp)).background(Color.LightGray).padding(16.dp))
```

## The Senior Nuance (El Matiz Senior)

- **Solo pinta**: por sí solo no agrega tamaño, [padding]({{ "/es/glosario/padding/" | relative_url }}) ni forma.
- **Un fondo cuadrado en una tarjeta redondeada es un bug de orden**: falta el [`clip`]({{ "/es/glosario/clip/" | relative_url }}) o el argumento `shape`.
- Ver [Modifiers: Order & Alignment]({{ "/es/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
