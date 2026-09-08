---
layout: post
title: "asSequence"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/as-sequence/
---

## The Theory (The What)

**`asSequence()`** wraps a [collection]({{ "/en/glossary/collections/" | relative_url }}) (or an `Iterator`) in a [`Sequence`]({{ "/en/glossary/sequences/" | relative_url }}), switching the [collection operators]({{ "/en/glossary/collection-operators/" | relative_url }}) that follow from eager to lazy: nothing is computed until a terminal operation pulls elements through the chain one at a time.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Find the next date matching the recurrence rule: stops at the first hit
val seed = (0..6).asSequence()
    .map { today.plusDays(it.toLong()) }
    .first { it.dayOfWeek in rule.weekdays }

// From FollowApp Suite — TaskMapper.kt
obj.keys().asSequence().associate { key -> /* ... */ }
```

## The Senior Nuance

- The two reasons to reach for it are short-circuiting and adapting a non-collection source. The first snippet maps only until the predicate matches; the second is the idiomatic bridge from a Java `Iterator` (`JSONObject.keys()`) into Kotlin operators without materialising a list first.
- It is not a default optimisation. Below roughly a thousand elements the per-element [overhead]({{ "/en/glossary/overhead/" | relative_url }}) of the iterator chain exceeds the [allocations]({{ "/en/glossary/allocations/" | relative_url }}) it saves, and a chain ending in [`sorted`]({{ "/en/glossary/sorted/" | relative_url }}) or [`groupBy`]({{ "/en/glossary/group-by/" | relative_url }}) materialises everything anyway.
- The result is single-pass: iterating the same sequence twice throws. Call [`toList`]({{ "/en/glossary/to-list/" | relative_url }}) at the boundary before storing it anywhere.

**Kotlin docs:** [`kotlin.collections.asSequence`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/as-sequence.html) · [Sequences](https://kotlinlang.org/docs/sequences.html)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
