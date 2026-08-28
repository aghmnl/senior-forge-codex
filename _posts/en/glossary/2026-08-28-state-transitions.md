---
layout: post
title: "State Transitions"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/state-transitions/
---

## The Theory (The What)

A **state transition** is the change from one defined state to another in response to an event or action. In Kotlin, state transitions are commonly modeled with `sealed class` or `sealed interface` hierarchies, where each subclass represents a discrete state, and `when` expressions ensure exhaustive handling of all possible transitions.

```kotlin
// From FollowApp Suite — FilterState.kt
sealed class ScaleFilterState {
    object Off : ScaleFilterState()
    data class Include(val values: Set<String>) : ScaleFilterState()
    object Exclude : ScaleFilterState()
}

// From FollowApp Suite — PresetMapper.kt
when (state) {
    is ScaleFilterState.Off -> json.put(key, JSONObject().put("type", "OFF"))
    is ScaleFilterState.Include -> { /* serialize values */ }
    is ScaleFilterState.Exclude -> json.put(key, JSONObject().put("type", "EXCLUDE"))
}
```

## The Senior Nuance

- Sealed hierarchies + `when` create a compile-time guarantee: adding a new state forces you to handle it everywhere. This is the Kotlin equivalent of a state machine — the compiler is the verifier.
- In [unidirectional data flow]({{ "/en/glossary/unidirectional-data-flow/" | relative_url }}) architectures, state transitions happen through `copy()` on immutable `data class` state objects, never through [mutation]({{ "/en/glossary/mutation/" | relative_url }}). This makes every transition explicit, auditable, and reproducible in tests.
- A common Senior pattern is modeling *illegal* transitions as compile errors: if `Loading` can only transition to `Success` or `Error`, make those the only subtypes of a sealed class. If a developer tries to go from `Error` back to `Loading`, the type system rejects it — not a runtime check.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
