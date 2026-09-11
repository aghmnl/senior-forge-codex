---
layout: post
title: "mutableStateListOf"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
tags: [compose, collections, state-management]
lang: en
permalink: /en/glossary/mutable-state-list-of/
---

## The Theory (The What)

**`mutableStateListOf()`** creates a [snapshot state list]({{ "/en/glossary/snapshot-state-list/" | relative_url }}) — a [`MutableList`]({{ "/en/glossary/mutable-list/" | relative_url }}) wired into the Compose [snapshot system]({{ "/en/glossary/snapshot-system/" | relative_url }}), so [`add`]({{ "/en/glossary/add/" | relative_url }}), [`remove`]({{ "/en/glossary/remove/" | relative_url }}), `set` and [`clear`]({{ "/en/glossary/clear/" | relative_url }}) recompose the composables that read it.

```kotlin
// From FollowApp Suite — TasksScreen.kt
val localTasks = remember { mutableStateListOf<Task>() }
// ...
localTasks.add(toIdx, localTasks.removeAt(fromIdx))   // recomposes immediately
```

## The Senior Nuance

- Always inside `remember { }` — otherwise a new list is created on every recomposition and the state resets. It has no state saver, so it does not survive process death; use `rememberSaveable` with an explicit saver, or hoist to a [ViewModel]({{ "/en/glossary/viewmodel-store/" | relative_url }}).
- It observes *structural* change only. Mutating a field of an element changes nothing — the element must be replaced (`list[i] = newValue`), which is exactly what the FollowApp Suite re-sync loop does.
- It is the one legitimate mutable [collection]({{ "/en/glossary/collections/" | relative_url }}) in UI code, and only as local optimistic state: the [ViewModel]({{ "/en/glossary/viewmodel-store/" | relative_url }}) stays the source of truth, and what leaves the composable is an ordinary read-only [`List`]({{ "/en/glossary/list/" | relative_url }}). Compare `mutableStateOf(listOf())`, which replaces the whole list per change and is the right default when there is no per-item gesture.

**Kotlin docs:** [`mutableStateListOf`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/package-summary#mutableStateListOf()) · [`SnapshotStateList`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/snapshots/SnapshotStateList)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
