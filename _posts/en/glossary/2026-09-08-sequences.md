---
layout: post
title: "Sequences"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
tags: [collections, functional, performance]
lang: en
permalink: /en/glossary/sequences/
---

## The Theory (The What)

A **`Sequence<T>`** is the lazily evaluated counterpart to a [collection]({{ "/en/glossary/collections/" | relative_url }}). [Collection operators]({{ "/en/glossary/collection-operators/" | relative_url }}) on a `List` are *eager*: each `map` or `filter` walks the whole input and allocates a new list. On a `Sequence` they are *intermediate* operations that build a pipeline; nothing runs until a terminal operation (`toList`, `first`, `sum`, `any`) pulls elements through it, one at a time.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
val seed = (0..6).asSequence()
    .map { today.plusDays(it.toLong()) }
    .first { it.dayOfWeek in rule.weekdays }   // stops at the first match
```

## The Senior Nuance

- The win is twofold: no intermediate [allocations]({{ "/en/glossary/allocations/" | relative_url }}), and short-circuiting on [terminal operations]({{ "/en/glossary/terminal-operations/" | relative_url }}) — `first` above may map a single element instead of the whole range.
- The cost is per-element [overhead]({{ "/en/glossary/overhead/" | relative_url }}): every step is an iterator with a virtual call and a captured [lambda]({{ "/en/glossary/lambdas/" | relative_url }}). Below roughly a thousand elements, or for a one- or two-step chain, the eager list version is usually faster. Measure rather than assume.
- Some operations are inherently eager and force the whole pipeline: `sorted`, `groupBy`, `distinct` must materialise everything. A sequence ending in `sorted` buys almost nothing.
- A `Sequence` is single-pass by default — iterating it twice throws. This makes it the wrong type to store in a UI state object; convert with `toList()` at the boundary.

**Kotlin docs:** [`kotlin.sequences.Sequence`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.sequences/-sequence/) · [Sequences](https://kotlinlang.org/docs/sequences.html)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
