---
layout: post
title: "Arrangement"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, layout]
lang: en
permalink: /en/glossary/arrangement/
---

## The Theory (The What)

**`Arrangement`** decides how a [`Row`]({{ "/en/glossary/row/" | relative_url }}) or [`Column`]({{ "/en/glossary/column/" | relative_url }}) **distributes its children along its [main axis]({{ "/en/glossary/main-axis-cross-axis/" | relative_url }})**: `Start`, `End`, `Center`, `SpaceBetween`, `SpaceAround`, `SpaceEvenly`, or a fixed gap with `spacedBy(8.dp)`.

```kotlin
// Not found in FAS — standalone example
Row(horizontalArrangement = Arrangement.SpaceBetween) { Text("Total"); Text("$42") }
```

## The Senior Nuance

- **`spacedBy` is better than padding on each child**: the spacing belongs to the parent, so adding or removing children keeps it consistent.
- See [Modifiers: Order & Alignment]({{ "/en/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
