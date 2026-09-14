---
layout: post
title: "Dispatchers.Main.immediate"
date: 2026-09-14 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, threading, state-management]
lang: en
permalink: /en/glossary/dispatchers-main-immediate/
---

## The Theory (The What)

**`Dispatchers.Main.immediate`** is [`Dispatchers.Main`]({{ "/en/glossary/dispatchers-main/" | relative_url }}) with one optimisation: if the coroutine is *already* on the main thread when it is dispatched, it runs synchronously instead of posting to the [`Looper`]({{ "/en/glossary/looper/" | relative_url }}) queue. Off Main it behaves exactly like `Main`. [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) and `lifecycleScope` use it, so a [`launch`]({{ "/en/glossary/launch/" | relative_url }}) from a click handler executes up to its first [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}) before the handler returns.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Reset the form FIRST, then trigger the suggestion recompute.
// viewModelScope uses Main.immediate, so the combine collector may run
// synchronously when a source flow is set — if the form reset came after,
// it would wipe the freshly computed labelSearchResults.
_uiState.update { it.copy(isFormVisible = true, form = TaskFormState()) }
_formOpenTrigger.value = System.currentTimeMillis()
```

## The Senior Nuance

- **It is an ordering guarantee.** Because the coroutine runs synchronously to its first suspension, statements after the `launch` observe its first effects — and a Flow collector on `Main.immediate` can run *inside* the `value =` that triggered it. Statement order becomes load-bearing; comment it.
- **It saves a frame of latency**, which is the reason the lifecycle scopes chose it: state set in a click handler is visible on the next frame, not the one after.
- **It cannot escape a busy Main.** If Main is saturated (cold start, first composition) the resume still queues. Overriding with `launch(Dispatchers.IO)` is the fix when the work is thread-safe.
- See [Context & Dispatchers]({{ "/en/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
