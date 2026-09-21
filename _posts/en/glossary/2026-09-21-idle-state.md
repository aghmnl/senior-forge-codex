---
layout: post
title: "Idle (UI State)"
date: 2026-09-21 12:00:00 +0000
categories: [en, glossary]
tags: [state-management, sealed-types, architecture]
lang: en
permalink: /en/glossary/idle-state/
---

## The Theory (The What)

**`Idle`** is the conventional name for the resting member of a sealed UI-state hierarchy: nothing has been requested yet, nothing is loading, nothing failed. It carries no payload, so it is declared as a [`data object`]({{ "/en/glossary/data-object/" | relative_url }}) — one instance, a clean `toString`, zero [allocations]({{ "/en/glossary/allocations/" | relative_url }}) no matter how often it is emitted. Its siblings are typically `Loading`, [`Success`]({{ "/en/glossary/success-state/" | relative_url }}) and `Error`.

```kotlin
// Not found in FAS — standalone example
sealed interface UploadState {
    data object Idle : UploadState          // nothing requested yet
    data object Uploading : UploadState
    data class Done(val url: String) : UploadState
    data class Failed(val cause: String) : UploadState
}
```

## The Senior Nuance

- **`Idle` is not `Empty`.** `Idle` means "we have not asked yet"; `Empty` means "we asked and there is nothing". Collapsing them into one state makes it impossible for the UI to tell a blank first screen from a genuinely empty result.
- **It is the natural initial value.** `MutableStateFlow<UploadState>(UploadState.Idle)` needs no nullable type and no `?:` default at every read.
- **Returning to `Idle` is a real transition.** After an error is dismissed or a flow is cancelled, going back to `Idle` — rather than leaving the last state — is what makes retry behave predictably.
- See [Data Objects: Singleton & Memory Savings]({{ "/en/01-kotlin-core/data-objects/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
