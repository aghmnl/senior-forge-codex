---
layout: post
title: "graphicsLayer"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, layout, performance]
lang: en
permalink: /en/glossary/graphics-layer/
---

## The Theory (The What)

**`Modifier.graphicsLayer { }`** applies transformations at drawing time: scale, rotation, translation, alpha, shadow and clipping. Its lambda form reads state in the **[drawing phase]({{ "/en/glossary/compose-phases/" | relative_url }})**, so animating these values does not recompose or re-layout the composable.

```kotlin
// Not found in FAS — standalone example
Box(Modifier.graphicsLayer { alpha = fade.value; scaleX = zoom.value })
```

## The Senior Nuance

- **The cheapest way to animate visual properties**, because only the [drawing phase]({{ "/en/glossary/compose-phases/" | relative_url }}) runs again.
- **It does not change layout**: a scaled element still occupies its original space.
- See [Modifiers: Order & Alignment]({{ "/en/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
