---
layout: post
title: "Snapshot System"
date: 2026-09-04 12:00:00 +0000
categories: [en, glossary]
tags: [compose, state-management, concurrency]
lang: en
permalink: /en/glossary/snapshot-system/
---

## The Theory (The What)

The **snapshot system** is [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }})'s change-tracking mechanism. It is the engine behind Compose's reactive UI: when a [`@Composable`]({{ "/en/glossary/composable/" | relative_url }}) function reads a snapshot-backed value and that value later changes, Compose automatically schedules recomposition of that function.

At its core, a snapshot is an isolated view of mutable state. Compose creates snapshots during composition and applies changes atomically. The key types:

- **`MutableState<T>`** / **`mutableStateOf()`** — the primary snapshot-backed wrapper. Reading it inside a composition registers a read observation; writing it triggers invalidation of all readers.
- **`SnapshotStateList`** / **`SnapshotStateMap`** — snapshot-aware [collections]({{ "/en/glossary/collections/" | relative_url }}) returned by `mutableStateListOf()` and `mutableStateMapOf()`.
- **`derivedStateOf {}`** — a computed snapshot value that only invalidates when its dependencies change.

When you write `var count by mutableStateOf(0)` using the [`by`]({{ "/en/glossary/by-delegation/" | relative_url }}) [keyword]({{ "/en/glossary/keyword/" | relative_url }}), the [property delegate]({{ "/en/glossary/property-delegate/" | relative_url }}) wraps a `SnapshotMutableState` — every read and write goes through the snapshot system. See [Delegated Properties]({{ "/en/01-kotlin-core/delegated-properties/" | relative_url }}).

## The Senior Nuance

- A Senior understands that snapshots are not just Compose UI state — they are a general-purpose multiversion concurrency control (MVCC) system. Composition runs in a snapshot isolated from the main thread's state; changes are merged atomically when composition completes. This is what makes recomposition safe from concurrent writes.
- Snapshot reads are tracked, not snapshot objects. If you read `state.value` inside a composable, that composable is registered as a reader. If you copy the value into a local `val` and pass it around, downstream code no longer has a tracking relationship with the snapshot.
- [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}) classes with `by mutableStateOf()` properties participate in the snapshot system without needing `remember` — their [lifetime]({{ "/en/glossary/composition-lifetime/" | relative_url }}) is managed by the class instance, not the [slot table]({{ "/en/glossary/slot-table/" | relative_url }}).
- Writing to snapshot state outside composition (e.g., in a ViewModel or callback) is safe: the snapshot system defers invalidation to the next composition pass. This is why `mutableStateOf` works in [state holders]({{ "/en/glossary/state-holder/" | relative_url }}) that live beyond the composition.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
