---
layout: post
title: "requiredSize"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, layout]
lang: en
permalink: /en/glossary/required-size/
---

## The Theory (The What)

**`Modifier.requiredSize(...)`** sets a size that **ignores the incoming [constraints]({{ "/en/glossary/constraints/" | relative_url }})**, unlike `size`, which respects them. If the required size does not fit, the composable overflows and is centered on the space it was given.

```kotlin
// Not found in FAS — standalone example
Box(Modifier.size(50.dp).requiredSize(80.dp))   // 80 dp, overflowing the 50 dp slot
```

## The Senior Nuance

- **A tool for exceptions**, such as a badge that must keep its size; using it often usually hides a layout problem.
- See [Modifiers: Order & Alignment]({{ "/en/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
