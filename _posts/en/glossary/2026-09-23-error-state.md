---
layout: post
title: "Error (UI State)"
date: 2026-09-23 12:00:00 +0000
categories: [en, glossary]
tags: [state-management, sealed-types, architecture]
lang: en
permalink: /en/glossary/error-state/
---

## The Theory (The What)

**`Error`** is the member of a sealed UI-state hierarchy that represents a failure the screen must show: `data class Error(val messageRes: Int)`, alongside `Loading`, [`Idle`]({{ "/en/glossary/idle-state/" | relative_url }}) and [`Success`]({{ "/en/glossary/success-state/" | relative_url }}). Modelling failure as a *state* rather than a log line is what turns a [`catch`]({{ "/en/glossary/catch/" | relative_url }}) block into something the user can see — without it, a failed load leaves the screen spinning forever.

```kotlin
// From FollowApp Suite — LabelsListViewModel.kt
// The catch block moves the state holder into an error state
.catch { e ->
    Log.e(TAG, "Error loading labels", e)
    _uiState.update { it.copy(isLoading = false, errorMessageRes = e.toUserMessage()) }
}
```

## The Senior Nuance

- **Carry a message resource, not a `Throwable`.** The state is for the UI, so it holds what the UI needs: a string resource id that respects the locale. The exception belongs in the log and in Crashlytics.
- **An error state needs a way out.** Retry, dismiss, or a fallback to cached data — an `Error` with no recovery path is a dead end the user can only escape by killing the app.
- **Distinguish "failed" from "empty".** A failed load and a legitimately empty list look identical if both render as an empty screen, and the user cannot tell whether to retry.
- See [Error Handling: try-catch & .catch]({{ "/en/02-coroutines-flow/error-handling/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
