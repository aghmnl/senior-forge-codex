---
layout: post
title: "Success (UI State)"
date: 2026-09-18 12:00:00 +0000
categories: [en, glossary]
tags: [state-management, sealed-types, architecture]
lang: en
permalink: /en/glossary/success-state/
---

## The Theory (The What)

**`Success`** is the conventional name for the subtype of a sealed UI-state hierarchy that carries the loaded data: `sealed interface UiState { object Loading; data class Success(val items: List<Item>); data class Error(val message: String) }`. It is a `data class` rather than an `object` because it holds payload, and it lives next to its siblings so a [`when`]({{ "/en/glossary/when-expression/" | relative_url }}) over the [sealed hierarchy]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}) is [exhaustive]({{ "/en/glossary/exhaustiveness/" | relative_url }}). Matching `is UiState.Success` smart-casts the state, giving direct access to `state.items` with no [cast]({{ "/en/glossary/cast/" | relative_url }}) — the pattern [MVI]({{ "/en/glossary/mvi-pattern/" | relative_url }}) and [UDF]({{ "/en/glossary/unidirectional-data-flow/" | relative_url }}) screens are built on.

```kotlin
// Not found in FAS — standalone example
sealed interface ScreenState {
    data object Loading : ScreenState
    data class Success(val items: List<String>) : ScreenState
    data class Error(val message: String) : ScreenState
}

fun render(state: ScreenState) = when (state) {
    is ScreenState.Loading -> showSpinner()
    is ScreenState.Success -> showData(state.items)   // smart cast: state is Success here
    is ScreenState.Error   -> showError(state.message)
}
```

## The Senior Nuance

- **`Success` is where the payload lives, so it is the branch that needs the smart cast.** `Loading` and `Error` are often objects; `Success` almost never is. The whole point of the sealed design is that `state.items` is only reachable after the compiler has proven the state is `Success`.
- **Model "success with nothing" explicitly.** An empty list inside `Success` and a separate `Empty` state are different UX decisions; do not encode the difference as a nullable field.
- **One `Success` per screen, not per request.** If a screen combines two calls, `Success` holds both results; two parallel sealed states force the UI to reason about their cross product.
- See [Smart Casts]({{ "/en/01-kotlin-core/smart-casts/" | relative_url }}) and [UI State Modeling]({{ "/en/05-architecture/ui-state-modeling/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
