---
layout: post
title: "Callbacks"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/callbacks/
---

## The Theory (The What)

A **callback** is a function (or [lambda]({{ "/en/glossary/lambdas/" | relative_url }})) passed as an argument to another function, to be invoked when a specific event occurs or an operation completes. In Kotlin, callbacks are expressed as function types — `() -> Unit`, `(String) -> Unit`, `(Result<T>) -> Unit` — making them first-class values that benefit from [higher-order function]({{ "/en/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) patterns, [inline]({{ "/en/glossary/inline-functions/" | relative_url }}) optimization, and type safety.

```kotlin
// From FollowApp Suite — TasksCallbacks.kt
class TaskFormCallbacks(
    val onFormTitleChange: (String) -> Unit,
    val onFormDescriptionChange: (String) -> Unit,
    val onFormCompletedChange: (Boolean) -> Unit,
    val onFormDueDateChange: (Long?) -> Unit,
    val onFormConfirmed: () -> Unit,
    val onFormDismissed: () -> Unit,
    val onFormRecurrenceChange: (RecurrenceRule?) -> Unit,
    val onAddSubtask: (String) -> Unit,
)
```

## The Senior Nuance

- **Callback consolidation**: In [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}), complex screens can accumulate dozens of lambda callbacks (`onClick`, `onValueChange`, `onDismiss`). Grouping them into a dedicated class (like `TaskFormCallbacks` above) prevents Composable parameter lists from exploding while keeping each callback strongly typed.
- **Callbacks vs Coroutines**: In modern Android, suspend functions and [Flow]({{ "/en/glossary/stateflow/" | relative_url }}) have largely replaced callbacks for async operations. Callbacks survive in UI event handlers (Compose `onClick`, View `OnClickListener`) and framework APIs that predate coroutines. Senior developers prefer coroutines for async work and callbacks only for event wiring.
- Each non-inline callback lambda [allocates]({{ "/en/glossary/allocations/" | relative_url }}) a `Function` object on the [heap]({{ "/en/glossary/heap/" | relative_url }}). In Compose, lambdas passed to composables are captured and compared for equality during recomposition — unstable captures (referencing mutable state) cause unnecessary recomposition. Use `remember { Callbacks(...) }` or stable references to avoid this.
- **[Memory leaks]({{ "/en/glossary/memory-leaks/" | relative_url }})**: A callback registered on a long-lived object (a singleton, a broadcast receiver) that captures an Activity or Fragment reference is a classic leak. Always unregister in `onDestroy()`/`onDestroyView()`, or use lifecycle-aware registration.
- The "callback hell" problem (deeply nested callbacks) is solved in Kotlin by coroutines (`suspendCancellableCoroutine` wraps a callback API into a suspend function), but understanding callbacks is still essential — they're the foundation that coroutines are built on.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
