---
layout: post
title: "State Holder"
date: 2026-09-04 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/state-holder/
---

## The Theory (The What)

A **state holder** is a class responsible for owning, producing, and managing UI state. In Android architecture, state holders centralize state logic that would otherwise be scattered across composables or fragments, making state testable and survivable across configuration changes.

There are two main categories:

- **ViewModel-based state holders** — subclass `ViewModel`, scoped to a [ViewModelStore]({{ "/en/glossary/viewmodel-store/" | relative_url }}), survive configuration changes. Hold business logic and domain state. Injected via [`by viewModels()`]({{ "/en/01-kotlin-core/delegated-properties/" | relative_url }}) in Fragments or `hiltViewModel()` in Compose.
- **Plain class state holders** — regular classes (often annotated [`@Stable`]({{ "/en/glossary/stable/" | relative_url }})) that hold UI-specific state: scroll positions, animation state, expanded/collapsed flags. Created via `remember { MyStateHolder() }` or `rememberSaveable`. Do not survive process death unless explicitly saved.

A state holder typically exposes [observable state]({{ "/en/glossary/observable-state/" | relative_url }}) — either [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}) for ViewModel-based holders or `mutableStateOf()` for Compose-level holders — and functions that modify state in response to events.

## The Senior Nuance

- A Senior separates **business state holders** (ViewModels: data loading, user actions, navigation events) from **UI state holders** (scroll state, drag state, form input). Mixing the two leads to ViewModels that know about pixel positions and plain classes that call repositories.
- Compose's [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}) state holders with [`by mutableStateOf()`]({{ "/en/01-kotlin-core/delegated-properties/" | relative_url }}) participate in the [snapshot system]({{ "/en/glossary/snapshot-system/" | relative_url }}) directly. Their [lifetime]({{ "/en/glossary/composition-lifetime/" | relative_url }}) is tied to the class instance, not a [slot table]({{ "/en/glossary/slot-table/" | relative_url }}) position — making them shareable across multiple composables without `remember`.
- Google's official architecture guidance (Now in Android, architecture samples) recommends hoisting state holders to the lowest common ancestor. A state holder scoped too high wastes memory; scoped too low, it's recreated on every recomposition or navigation.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
