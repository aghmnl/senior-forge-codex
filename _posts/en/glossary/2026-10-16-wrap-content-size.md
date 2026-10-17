---
layout: post
title: "wrapContentSize"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, layout]
lang: en
permalink: /en/glossary/wrap-content-size/
---

## The Theory (The What)

**`Modifier.wrapContentSize()`** lets the content be **smaller than the minimum [constraints]({{ "/en/glossary/constraints/" | relative_url }})** it receives, and aligns it inside that space (centered by default, or with an `align` argument). Without it, a child forced to a minimum size stretches to fill it.

```kotlin
// Not found in FAS — standalone example
Box(Modifier.size(100.dp).wrapContentSize(Alignment.TopStart).size(40.dp))
```

## The Senior Nuance

- **Useful after a [modifier]({{ "/en/glossary/modifier/" | relative_url }}) that imposes a minimum**, to keep the content at its natural size and decide where it sits.
- See [Modifiers: Order & Alignment]({{ "/en/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
