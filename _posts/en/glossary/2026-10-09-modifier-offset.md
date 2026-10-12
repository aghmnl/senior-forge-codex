---
layout: post
title: "Modifier.offset"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [compose, performance]
lang: en
permalink: /en/glossary/modifier-offset/
---

## The Theory (The What)

**`Modifier.offset`** moves a composable from its laid-out position. It has two forms: `offset(x, y)` takes the values directly, so reading a changing state to pass them recomposes the composable; `offset { IntOffset(x, y) }` takes a [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) that is evaluated in the **layout phase**, so a changing value is read there and [composition]({{ "/en/glossary/composition/" | relative_url }}) does not run again.

```kotlin
// Not found in FAS — standalone example
Box(Modifier.offset { IntOffset(0, scrollState.value / 2) })   // no recomposition per pixel
```

## The Senior Nuance

- **Prefer the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) form for values that change every frame** (scroll, drag, animation). It is the standard example of deferring a state read to a later phase.
- **The same idea applies to `graphicsLayer { }` and `drawBehind { }`**, which read state in the drawing phase.
- See [Recomposition & Stability]({{ "/en/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
