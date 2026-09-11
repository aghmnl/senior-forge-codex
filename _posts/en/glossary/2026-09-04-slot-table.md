---
layout: post
title: "Slot Table"
date: 2026-09-04 12:00:00 +0000
categories: [en, glossary]
tags: [compose, state-management, memory]
lang: en
permalink: /en/glossary/slot-table/
---

## The Theory (The What)

The **slot table** is [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }})'s internal data structure that stores the state and structure of the composition tree. It is a flat, gap-buffer array where each [`@Composable`]({{ "/en/glossary/composable/" | relative_url }}) function call occupies a range of "slots" that hold:

- **Groups** — markers that delineate each composable's start and end in the tree.
- **State** — values stored via `remember {}`, including [delegated properties]({{ "/en/01-kotlin-core/delegated-properties/" | relative_url }}) created with `by remember { mutableStateOf() }`.
- **Nodes** — the actual UI elements (layout nodes) that Compose renders.

When recomposition runs, the Compose runtime walks the slot table, comparing the current call structure against the stored one. If a composable's inputs haven't changed and it is skippable (all parameters are [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}) or [primitive]({{ "/en/glossary/primitives/" | relative_url }})), Compose skips re-executing it entirely — the existing slots are reused as-is.

## The Senior Nuance

- A Senior knows that `remember {}` is anchored to a position in the slot table, not to a variable name. If the call site moves (e.g., a composable is conditionally included before another), the slot positions shift, and remembered values are reset. The `key()` composable provides stable identity to prevent this.
- The slot table is the reason `by remember { mutableStateOf() }` and `by mutableStateOf()` in a [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}) class have different [lifetimes]({{ "/en/glossary/composition-lifetime/" | relative_url }}): the `remember` version is stored in the slot table and dies when that composable leaves the composition; the `@Stable` class version lives on the [heap]({{ "/en/glossary/heap/" | relative_url }}) as long as the class instance exists.
- The gap buffer design means insertions and deletions at a single point are O(1), but moving the gap is O(n). Compose minimizes gap moves by processing the tree linearly, top-to-bottom. Conditional composition (`if`/`when` blocks) that change frequently in the middle of a large composable tree cause more gap moves — a subtle performance consideration.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
