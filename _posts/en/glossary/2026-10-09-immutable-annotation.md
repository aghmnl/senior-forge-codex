---
layout: post
title: "@Immutable"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [compose, immutability]
lang: en
permalink: /en/glossary/immutable-annotation/
---

## The Theory (The What)

**`@Immutable`** is a Compose annotation that promises a class will **never change** after it is created: all its public properties are [`val`]({{ "/en/glossary/val/" | relative_url }})s whose values never change. The compiler then treats the class as [stable]({{ "/en/glossary/stability/" | relative_url }}) and compares it with [`equals`]({{ "/en/glossary/equals/" | relative_url }}) during [skipping]({{ "/en/glossary/skipping/" | relative_url }}). It is stronger than [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}), which allows changes as long as they are observable through snapshot state.

```kotlin
// Not found in FAS — standalone example
@Immutable
data class TaskRow(val id: String, val title: String, val tags: List<String>)
```

## The Senior Nuance

- **It is a promise, not a check.** Nothing verifies it. If the `tags` [list]({{ "/en/glossary/list/" | relative_url }}) above were mutated, Compose would skip the row and show stale data.
- **Use it only when the compiler cannot infer what is true**, typically for a [`List`]({{ "/en/glossary/list/" | relative_url }}) you know is never mutated. Real immutability or a [stability]({{ "/en/glossary/stability/" | relative_url }}) configuration file are safer.
- See [Recomposition & Stability]({{ "/en/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
