---
layout: post
title: "Alignment"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, layout]
lang: en
permalink: /en/glossary/alignment/
---

## The Theory (The What)

**`Alignment`** positions children inside the space they are given. In a [`Box`]({{ "/en/glossary/box/" | relative_url }}) it works in both axes (`TopStart`, `Center`, `BottomEnd`); in a [`Row`]({{ "/en/glossary/row/" | relative_url }}) it is vertical only (`Top`, `CenterVertically`, `Bottom`) and in a [`Column`]({{ "/en/glossary/column/" | relative_url }}) horizontal only, because it applies to the **[cross axis]({{ "/en/glossary/main-axis-cross-axis/" | relative_url }})**.

```kotlin
// Not found in FAS — standalone example
Box(contentAlignment = Alignment.BottomEnd) { /* ... */ }
```

## The Senior Nuance

- **Alignment positions each child; [arrangement]({{ "/en/glossary/arrangement/" | relative_url }}) distributes the group.** Mixing them up is a common source of "why will this not center?".
- See [Modifiers: Order & Alignment]({{ "/en/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
