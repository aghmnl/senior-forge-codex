---
layout: post
title: "Terminal Operations"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/terminal-operations/
---

## The Theory (The What)

A **terminal operation** is the one that consumes a chain and produces a value instead of another chain: `first`, `firstOrNull`, `any`, `all`, `none`, `count`, `sum`, `fold`, [`toList`]({{ "/en/glossary/to-list/" | relative_url }}), [`toSet`]({{ "/en/glossary/to-set/" | relative_url }}). On a [`Sequence`]({{ "/en/glossary/sequences/" | relative_url }}) nothing runs until one is called; on an ordinary [collection]({{ "/en/glossary/collections/" | relative_url }}) every step already ran eagerly, and the terminal is simply the last one.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Short-circuits: stops at the first matching day
val seed = (0..6).asSequence()
    .map { today.plusDays(it.toLong()) }
    .first { it.dayOfWeek in rule.weekdays }

// From FollowApp Suite — TasksViewModel.kt
val hasSubtask = tasks.any { it.parentTaskId != null }
val duplicate = state.activeTasks.any { it.title.equals(title, ignoreCase = true) }
```

## The Senior Nuance

- `any`, `all`, `none`, `first` and `find` **short-circuit**: they stop at the deciding element. `tasks.any { it.parentTaskId != null }` is `O(1)` on a list whose first task has a parent — while `tasks.filter { ... }.isNotEmpty()` always walks everything and allocates a list to throw away.
- `first { }` throws `NoSuchElementException` when nothing matches; `firstOrNull { }` returns `null`. Choosing between them is an [intent-signaling]({{ "/en/glossary/intent-signaling/" | relative_url }}) decision — throw when absence is a bug, return `null` when it is an expected state.
- Terminals are also where a [`Sequence`]({{ "/en/glossary/sequences/" | relative_url }}) is spent: it is single-pass, so a second terminal on the same sequence throws. And [`sorted`]({{ "/en/glossary/sorted/" | relative_url }})/[`groupBy`]({{ "/en/glossary/group-by/" | relative_url }}) sit in between — intermediate in the API, but forced to buffer everything, which cancels the laziness.
- Placing the terminal correctly is most of the optimisation: `map { }.first { }` over a list maps every element, while the same chain over [`asSequence`]({{ "/en/glossary/as-sequence/" | relative_url }}) maps only until the match.

**Kotlin docs:** [`first`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/first.html) · [`any`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/any.html) · [Collection operations overview](https://kotlinlang.org/docs/collection-operations.html)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
