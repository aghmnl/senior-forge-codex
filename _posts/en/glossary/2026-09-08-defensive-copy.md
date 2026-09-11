---
layout: post
title: "Defensive Copy"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
tags: [immutability, collections, concurrency]
lang: en
permalink: /en/glossary/defensive-copy/
---

## The Theory (The What)

A **defensive copy** duplicates a mutable object at a boundary so that neither side can observe the other's [mutations]({{ "/en/glossary/mutation/" | relative_url }}). In Kotlin the idiom is `toList()`, `toSet()`, `toMap()` on the way *out* of a component, and `toMutableList()` on the way *in* when you intend to modify.

```kotlin
// From FollowApp Suite — TasksScreen.kt
val source = localGroups[originIdx].tasks.toMutableList()
val target = localGroups[targetIdx].tasks.toMutableList()
```

## The Senior Nuance

- A copy is what upgrades a [read-only view]({{ "/en/glossary/read-only-view/" | relative_url }}) into an actual value. `_items.toList()` costs one array copy and removes an entire class of `ConcurrentModificationException` and stale-render bugs.
- The copy is **shallow**: the new [collection]({{ "/en/glossary/collections/" | relative_url }}) holds the same element references. Copying a `List<TaskEntity>` protects the list structure, not the entities — which is why the elements themselves should be [immutable]({{ "/en/glossary/immutability/" | relative_url }}) [data classes]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}).
- Copying at every boundary is not free: on a hot path it is real [allocation]({{ "/en/glossary/allocations/" | relative_url }}) pressure. The alternative is not skipping the copy — it is never creating a mutable object that escapes in the first place, or using a [persistent collection]({{ "/en/glossary/persistent-collections/" | relative_url }}) that shares structure instead of copying.

**Kotlin docs:** [`kotlin.collections.toList`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/to-list.html)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
