---
layout: post
title: "drawBehind"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, layout, performance]
lang: en
permalink: /en/glossary/draw-behind/
---

## The Theory (The What)

**`Modifier.drawBehind { }`** draws custom graphics behind the content, using a `DrawScope` (lines, circles, paths). State read inside its lambda is read in the **[drawing phase]({{ "/en/glossary/compose-phases/" | relative_url }})**, so a frequently changing value only redraws, without [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
Box(Modifier.drawBehind { drawCircle(color, radius = progress.value * size.minDimension / 2) })
```

## The Senior Nuance

- **`drawWithContent`** is its sibling when you need to draw both behind and on top of the content.
- See [Modifiers: Order & Alignment]({{ "/en/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
