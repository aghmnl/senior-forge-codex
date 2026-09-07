---
layout: post
title: "Immutability"
date: 2026-09-04 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/immutability/
---

## The Theory (The What)

**Immutability** means that once a value is created, it cannot be changed. In Kotlin, immutability is expressed at multiple levels:

- **`val` vs `var`** — `val` declares a read-only reference (the reference cannot be reassigned, though the object it points to may still be mutable internally).
- **Immutable [collections]({{ "/en/glossary/collections/" | relative_url }})** — `List`, `Set`, `Map` expose no mutation methods. `MutableList`, `MutableSet`, `MutableMap` add them.
- **[Data classes]({{ "/en/01-kotlin-core/data-classes/" | relative_url }})** — when all properties are `val`, the instance is effectively immutable. The `copy()` function produces a new instance with selected fields changed, preserving the original.
- **Kotlinx Immutable Collections** — `persistentListOf()`, `toImmutableList()` provide structurally immutable collections that the Compose compiler can recognize as [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}).

Immutability is a cornerstone of [functional style]({{ "/en/glossary/functional-style/" | relative_url }}) programming: [data transformations]({{ "/en/glossary/data-transformation/" | relative_url }}) produce new values rather than modifying existing ones.

## The Senior Nuance

- A Senior distinguishes between **reference immutability** (`val`) and **object immutability** (no mutable state inside). A `val list: MutableList<Int>` is a read-only reference to a mutable object — a common source of bugs when the list is exposed from a ViewModel.
- In Compose, immutability drives skip optimization: if all parameters to a composable are [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}) or [primitives]({{ "/en/glossary/primitives/" | relative_url }}), the runtime can skip recomposition when inputs haven't changed. Passing a `MutableList` breaks this contract even if the contents didn't change, because Compose cannot prove stability.
- Immutability simplifies [thread safety]({{ "/en/glossary/thread-safety/" | relative_url }}): an object that cannot change needs no synchronization. This is why `StateFlow` holds immutable snapshots of state, and why `copy()` on a [data class]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}) is the idiomatic way to update state in a ViewModel.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
