---
layout: post
title: "fillMaxWidth"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, layout]
lang: es
permalink: /es/glosario/fill-max-width/
---

## The Theory (El Qué)

**`Modifier.fillMaxWidth()`** hace que un composable tome **todo el ancho que permiten sus [constraints]({{ "/es/glosario/constraints/" | relative_url }})**. `fillMaxHeight()` y `fillMaxSize()` hacen lo mismo con el alto y con las dos dimensiones, y una fracción (`fillMaxWidth(0.5f)`) toma una parte.

```kotlin
// Not found in FAS — standalone example
Button(onClick = {}, modifier = Modifier.fillMaxWidth()) { Text("Save") }
```

## The Senior Nuance (El Matiz Senior)

- **Adentro de un contenedor con scroll no tiene límite para llenar**: en una columna con scroll vertical, `fillMaxHeight` tiene un máximo infinito y no funciona como se espera.
- Ver [Modifiers: Order & Alignment]({{ "/es/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
