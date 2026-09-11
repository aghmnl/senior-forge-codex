---
layout: post
title: "ArrayList"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
tags: [collections, performance, memory]
lang: en
permalink: /en/glossary/arraylist/
---

## The Theory (The What)

**`ArrayList<E>`** is the concrete, array-backed implementation behind almost every [`MutableList`]({{ "/en/glossary/mutable-list/" | relative_url }}) in Kotlin — `mutableListOf()`, [`toMutableList`]({{ "/en/glossary/to-mutable-list/" | relative_url }}) and [`buildList`]({{ "/en/glossary/build-list/" | relative_url }}) all return one. Indexed access is `O(1)`; [`add`]({{ "/en/glossary/add/" | relative_url }}) is amortised `O(1)`, growing by copying into a larger array when full.

```kotlin
// From FollowApp Suite — LegacyTaskReader.kt
val tasks = ArrayList<LegacyTask>(cursor.count)   // pre-sized: no growth copies
while (cursor.moveToNext()) {
    tasks.add(LegacyTask(/* ... */))
}
```

## The Senior Nuance

- Naming `ArrayList` explicitly is justified exactly when you know the size up front, as above: pre-sizing the backing array turns a sequence of grow-and-copy [allocations]({{ "/en/glossary/allocations/" | relative_url }}) into one. Everywhere else, `mutableListOf()` says the same thing about intent and less about implementation.
- `removeAt(0)` and `add(0, e)` shift every remaining element — `O(n)`. A list used as a queue should be an `ArrayDeque`, not an `ArrayList`.
- It is the reason a [read-only view]({{ "/en/glossary/read-only-view/" | relative_url }}) is not [immutability]({{ "/en/glossary/immutability/" | relative_url }}): a [`List`]({{ "/en/glossary/list/" | relative_url }}) returned from a function is, at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}), usually a plain `ArrayList` that Java interop can happily write to.

**Kotlin docs:** [`kotlin.collections.ArrayList`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-array-list/)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
