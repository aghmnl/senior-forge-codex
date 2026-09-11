---
layout: post
title: "Persistent Collections"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
tags: [collections, immutability, compose]
lang: en
permalink: /en/glossary/persistent-collections/
---

## The Theory (The What)

**Persistent collections** (`kotlinx.collections.immutable`: `PersistentList`, `PersistentSet`, `PersistentMap`) are genuinely [immutable]({{ "/en/glossary/immutability/" | relative_url }}) [collections]({{ "/en/glossary/collections/" | relative_url }}). Every "modification" returns a *new* collection that shares most of its internal structure with the old one, so [`add`]({{ "/en/glossary/add/" | relative_url }}) is not an `O(n)` copy.

```kotlin
// Not found in FAS — standalone example
val selected: PersistentSet<String> = persistentSetOf("a", "b")
val next = selected.add("c")   // new value; `selected` is unchanged
```

## The Senior Nuance

- They close the gap Kotlin's own hierarchy leaves open: [`List`]({{ "/en/glossary/list/" | relative_url }}) is only a [read-only view]({{ "/en/glossary/read-only-view/" | relative_url }}), while `PersistentList` is a value nobody can mutate — no [defensive copy]({{ "/en/glossary/defensive-copy/" | relative_url }}) needed at any boundary.
- Compose is the strongest practical reason to adopt them. `ImmutableList` is annotated [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}), so a composable taking one is skippable; a plain [`List<T>`]({{ "/en/glossary/list/" | relative_url }}) parameter is treated as unstable, which silently disables recomposition skipping for that composable.
- The cost is a dependency and a slightly slower single-element read than [`ArrayList`]({{ "/en/glossary/arraylist/" | relative_url }}) (tree traversal instead of array indexing). For UI state — many reads, occasional structural updates, shared across threads — the trade is almost always worth it.

**Kotlin docs:** [kotlinx.collections.immutable](https://github.com/Kotlin/kotlinx.collections.immutable)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
