---
layout: post
title: "emptyList"
date: 2026-09-25 12:00:00 +0000
categories: [en, glossary]
tags: [collections, immutability, memory]
lang: en
permalink: /en/glossary/empty-list/
---

## The Theory (The What)

**`emptyList<T>()`** is the [standard library]({{ "/en/glossary/standard-library/" | relative_url }}) function that returns a **read-only, empty [List]({{ "/en/glossary/list/" | relative_url }})**. It does not allocate: every call returns the same internal singleton object, whatever the type argument. `listOf()` with no arguments returns the same thing. When the type cannot be inferred it needs it explicitly: `emptyList<Task>()`.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// A typed empty list as the initial value of a StateFlow
private val _selectedLabels = MutableStateFlow<List<String>>(emptyList())
```

## The Senior Nuance

- **Empty is a value, not an absence.** As the initial value of a [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}), `emptyList()` says "there are no items", which is a lie while the data is still loading. "Not loaded yet" needs its own representation: an `isLoading` flag, a `Loading` state, or `null`.
- **Equality is structural.** `emptyList<Int>() == ArrayList<Int>()` is `true`, because list [equality]({{ "/en/glossary/equals/" | relative_url }}) compares content. Replacing one empty list with another does not make a `StateFlow` emit.
- **Read-only, not mutable.** Casting it to `MutableList` and calling [add]({{ "/en/glossary/add/" | relative_url }}) throws `UnsupportedOperationException`. Use [mutableListOf()]({{ "/en/glossary/mutable-list/" | relative_url }}) when the list must grow.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
