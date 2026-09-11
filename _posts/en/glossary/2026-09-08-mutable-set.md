---
layout: post
title: "MutableSet"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
tags: [collections, immutability]
lang: en
permalink: /en/glossary/mutable-set/
---

## The Theory (The What)

**`MutableSet<E>`** extends [`Set`]({{ "/en/glossary/sets/" | relative_url }}) with [`add`]({{ "/en/glossary/add/" | relative_url }}), [`remove`]({{ "/en/glossary/remove/" | relative_url }}) and [`clear`]({{ "/en/glossary/clear/" | relative_url }}). `mutableSetOf()` is backed by a `LinkedHashSet`, so iteration order is insertion order; `hashSetOf()` gives no order guarantee at all.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
val parentIds = if (hasSubtasksFilter != null) {
    tasks.mapNotNullTo(mutableSetOf()) { it.parentTaskId }
} else emptySet()
```

## The Senior Nuance

- `mapNotNullTo(mutableSetOf())` is the idiomatic fused form: it maps and collects into the target [collection]({{ "/en/glossary/collections/" | relative_url }}) in one pass, with no intermediate list — and the result is immediately typed back down to `Set`.
- [`add`]({{ "/en/glossary/add/" | relative_url }}) returns `false` when the element is already present, which makes a `MutableSet` a clean deduplicating accumulator: `if (seen.add(id)) { /* first time */ }` replaces a `contains` + `add` pair with one hash lookup.
- Mutating an element after inserting it corrupts the set: its `hashCode` changes, so the element lands in the wrong bucket and [`contains`]({{ "/en/glossary/contains/" | relative_url }}) returns `false` for an object that is physically inside. Set elements must be [immutable]({{ "/en/glossary/immutability/" | relative_url }}).

**Kotlin docs:** [`kotlin.collections.MutableSet`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-mutable-set/)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
