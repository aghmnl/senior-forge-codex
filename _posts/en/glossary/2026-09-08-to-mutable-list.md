---
layout: post
title: "toMutableList"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
tags: [collections, immutability]
lang: en
permalink: /en/glossary/to-mutable-list/
---

## The Theory (The What)

**`toMutableList()`** returns a new [`MutableList`]({{ "/en/glossary/mutable-list/" | relative_url }}) — an [`ArrayList`]({{ "/en/glossary/arraylist/" | relative_url }}) — containing the receiver's elements. It is the *inbound* [defensive copy]({{ "/en/glossary/defensive-copy/" | relative_url }}): you take a copy precisely because you intend to [mutate]({{ "/en/glossary/mutation/" | relative_url }}) it and must not touch the original.

```kotlin
// From FollowApp Suite — TasksScreen.kt
val source = localGroups[originIdx].tasks.toMutableList()
val target = localGroups[targetIdx].tasks.toMutableList()
```

## The Senior Nuance

- Reaching for it is a signal to check ownership. Here the group's `tasks` is a read-only [`List`]({{ "/en/glossary/list/" | relative_url }}) owned by a state object, so a cross-group drag copies, edits the copies, and publishes new groups — the state object is never written through.
- `LabelsListViewModel` uses the same shape for reordering scale options: copy, `add`/`removeAt`, then emit a new state. The mutable list lives inside one [stack frame]({{ "/en/glossary/stack-frame/" | relative_url }}) and is never stored.
- It always copies, even when the receiver is already mutable — that is the point, but it also means calling it inside a loop over `n` groups is `n` array copies. Copy once, outside.

**Kotlin docs:** [`kotlin.collections.toMutableList`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/to-mutable-list.html)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
