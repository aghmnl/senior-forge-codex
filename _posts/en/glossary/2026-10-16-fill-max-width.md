---
layout: post
title: "fillMaxWidth"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, layout]
lang: en
permalink: /en/glossary/fill-max-width/
---

## The Theory (The What)

**`Modifier.fillMaxWidth()`** makes a composable take **all the width its [constraints]({{ "/en/glossary/constraints/" | relative_url }}) allow**. `fillMaxHeight()` and `fillMaxSize()` do the same for height and both dimensions, and a fraction (`fillMaxWidth(0.5f)`) takes part of it.

```kotlin
// Not found in FAS — standalone example
Button(onClick = {}, modifier = Modifier.fillMaxWidth()) { Text("Save") }
```

## The Senior Nuance

- **Inside a scrollable container it has no limit to fill**: in a vertically scrolling [column]({{ "/en/glossary/column/" | relative_url }}), `fillMaxHeight` has an infinite maximum and does not work as expected.
- See [Modifiers: Order & Alignment]({{ "/en/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
