---
layout: post
title: "Snapshot State List"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/snapshot-state-list/
---

## The Theory (The What)

A **snapshot state list** — `mutableStateListOf()`, of type `SnapshotStateList<T>` — is a `MutableList` integrated with the Compose [snapshot system]({{ "/en/glossary/snapshot-system/" | relative_url }}). Structural changes (`add`, `remove`, `clear`, `set`) are recorded as [observable state]({{ "/en/glossary/observable-state/" | relative_url }}) [mutations]({{ "/en/glossary/mutation/" | relative_url }}) and recompose exactly the composables that read the list.

```kotlin
// From FollowApp Suite — TasksScreen.kt
val localTasks = remember { mutableStateListOf<Task>() }
// ...
localTasks.add(toIdx, localTasks.removeAt(fromIdx))   // recomposes immediately
```

## The Senior Nuance

- It is the exception to "no mutable [collections]({{ "/en/glossary/collections/" | relative_url }}) in UI code" — and only for *local, optimistic* state. In FollowApp Suite it exists so a drag gesture can reorder rows synchronously without a [ViewModel]({{ "/en/glossary/viewmodel-store/" | relative_url }}) round-trip per move; the ViewModel remains the source of truth and is notified once on drop.
- It must be re-synchronised from that source of truth (a `LaunchedEffect` keyed on the incoming state), or the two diverge — the classic bug where the UI shows an order the data layer never accepted.
- `remember { mutableStateListOf() }` takes no state saver, so it does not survive process death; and mutating it observes only *structural* change — mutating a field of an element does nothing unless the element is itself observable or replaced. Never expose one across a module boundary: hand back an ordinary read-only `List` instead.

**Kotlin docs:** [`SnapshotStateList`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/snapshots/SnapshotStateList)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
