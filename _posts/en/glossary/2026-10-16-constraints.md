---
layout: post
title: "Constraints"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, layout, performance]
lang: en
permalink: /en/glossary/constraints/
---

## The Theory (The What)

**Constraints** are the minimum and maximum width and height a parent allows its child to have during layout. They flow down the [modifier]({{ "/en/glossary/modifier/" | relative_url }}) chain and the tree; each size [modifier]({{ "/en/glossary/modifier/" | relative_url }}) narrows them for what comes after it, and the child picks a size within them. That is why in `Modifier.size(100.dp).size(50.dp)` the first size wins.

```kotlin
// Not found in FAS — standalone example
Box(Modifier.size(100.dp).size(50.dp))   // 100 dp
```

## The Senior Nuance

- **Constraints go down, sizes go up**: parents constrain, children choose, parents place.
- **To break out of the incoming constraints** use `requiredSize`, and do it knowingly: the child may overflow its parent.
- See [Modifiers: Order & Alignment]({{ "/en/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
