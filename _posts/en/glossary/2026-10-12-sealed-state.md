---
layout: post
title: "Sealed State"
date: 2026-10-12 12:00:00 +0000
categories: [en, glossary]
tags: [state-management, sealed-types, architecture]
lang: en
permalink: /en/glossary/sealed-state/
---

## The Theory (The What)

A **sealed state** models a screen's UI state as a [`sealed interface`]({{ "/en/glossary/sealed-interface/" | relative_url }}) (or [`sealed class`]({{ "/en/glossary/sealed-class/" | relative_url }})) whose subtypes are mutually exclusive states, such as `Loading`, [`Success`]({{ "/en/glossary/success-state/" | relative_url }}) and [`Error`]({{ "/en/glossary/error-state/" | relative_url }}). The screen is always exactly one of them, each subtype carries only its own data, and a `when` without `else` must handle every subtype.

```kotlin
// Not found in FAS — standalone example
sealed interface DetailState {
    data object Loading : DetailState
    data class Success(val task: Task) : DetailState
    data class Error(val message: String) : DetailState
}
```

## The Senior Nuance

- **It cannot represent impossible combinations**: there is no value that is loading and failed at the same time.
- **It struggles when concerns overlap.** Data shared by several states (a search query, a selection) has to be duplicated in each subtype or is lost on every transition.
- See [UI State Modeling: Sealed vs Flat Data Class]({{ "/en/05-architecture/ui-state-modeling/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
