---
layout: post
title: "Composition Lifetime"
date: 2026-09-04 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/composition-lifetime/
---

## The Theory (The What)

**Composition lifetime** refers to how long a composable — and its remembered state — exists in the composition tree. A composable enters the composition when it is first called and leaves when its parent no longer calls it (e.g., a conditional branch changes, a list item is removed, or navigation moves to another screen).

State created with `remember {}` (including [delegated properties]({{ "/en/01-kotlin-core/delegated-properties/" | relative_url }}) like `by remember { mutableStateOf() }`) is stored in the [slot table]({{ "/en/glossary/slot-table/" | relative_url }}) and shares the composable's lifetime — it is created on entry, preserved across recompositions, and destroyed on exit.

This differs from other Android lifetimes:

- **Activity/Fragment lifecycle** — tied to OS events (create, start, resume, pause, stop, destroy). Can survive configuration changes via `ViewModel`.
- **ViewModel lifetime** — tied to the [ViewModelStore]({{ "/en/glossary/viewmodel-store/" | relative_url }}) owner (Activity, Fragment, or [back stack]({{ "/en/glossary/back-stack/" | relative_url }}) entry). Survives configuration changes, dies on final destruction.
- **Process lifetime** — the longest scope; `SavedStateHandle` / `rememberSaveable` bridge state across process death.

## The Senior Nuance

- A Senior recognizes that composition lifetime is the most granular scope: a composable's state is destroyed the moment the composable leaves the tree, even if the screen is still visible. This is why navigating between tabs can destroy composition state if the tab's composable is removed — `rememberSaveable` or ViewModel-backed state is needed for persistence.
- [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}) [state holders]({{ "/en/glossary/state-holder/" | relative_url }}) with `by mutableStateOf()` decouple from composition lifetime: their state lives on the [heap]({{ "/en/glossary/heap/" | relative_url }}) as long as the instance is referenced. If passed down as a parameter, their state survives the remover-caller's recomposition.
- Understanding composition lifetime is essential for effect cleanup: `DisposableEffect` runs its `onDispose` when the composable leaves the composition, while `LaunchedEffect` cancels its coroutine. Mismatching effect scope with the intended lifetime causes either leaked resources or premature cleanup.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
