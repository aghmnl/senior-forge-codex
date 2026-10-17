---
layout: post
title: "background"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, layout]
lang: en
permalink: /en/glossary/background/
---

## The Theory (The What)

**`Modifier.background(color, shape)`** draws a color (or a brush) behind the content, over the area the [modifier]({{ "/en/glossary/modifier/" | relative_url }}) wraps. A [`padding`]({{ "/en/glossary/padding/" | relative_url }}) before it shrinks that area; a [`clip`]({{ "/en/glossary/clip/" | relative_url }}) before it gives it a shape.

```kotlin
// Not found in FAS — standalone example
Box(Modifier.clip(RoundedCornerShape(12.dp)).background(Color.LightGray).padding(16.dp))
```

## The Senior Nuance

- **It only paints**: it does not add size, [padding]({{ "/en/glossary/padding/" | relative_url }}) or a shape on its own.
- **A square background on a rounded card is an ordering bug**: the [`clip`]({{ "/en/glossary/clip/" | relative_url }}) or the `shape` argument is missing.
- See [Modifiers: Order & Alignment]({{ "/en/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
