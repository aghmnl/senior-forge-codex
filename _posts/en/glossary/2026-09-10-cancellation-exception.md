---
layout: post
title: "CancellationException"
date: 2026-09-10 12:00:00 +0000
categories: [en, glossary]
tags: [cancellation, coroutines, error-handling]
lang: en
permalink: /en/glossary/cancellation-exception/
---

## The Theory (The What)

**`CancellationException`** is the exception a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) throws from its next [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}) once its job has been cancelled. It is the mechanism of [cooperative cancellation]({{ "/en/glossary/cooperative-cancellation/" | relative_url }}): unwinding the [state machine]({{ "/en/glossary/state-machine/" | relative_url }}) the same way any exception would, so `finally` blocks and `use { }` run. It is treated specially by the framework — a coroutine that ends with it is considered *cancelled*, not *failed*, and it is never reported to `CoroutineExceptionHandler`.

```kotlin
// From FollowApp Suite — DragToReorder.kt
} catch (e: CancellationException) {
    // Gesture coroutine disposed mid-drag (e.g. composition change)
    state.endDrag(cancelled = true)
    throw e
}
```

Catch it to clean up local state, then **rethrow**. Swallowing it lets the coroutine continue past the point where it was told to stop.

## The Senior Nuance

- **`runCatching` and `catch (e: Exception)` both swallow it.** `CancellationException` extends `IllegalStateException`. A `runCatching { }` around a suspend call turns a cancelled ViewModel into one that keeps writing to disk. Filter it: `catch (e: Exception) { if (e is CancellationException) throw e; ... }`, or use `ensureActive()` after the catch.
- **It is cheap on purpose.** The framework's instance skips stack-trace filling, so cancellation is not an expensive operation.
- **Do not throw it yourself to signal domain errors.** A user cancelling a dialog is a *result*, not a cancellation — FAS's sign-in flow catches `GetCredentialCancellationException`, a different type, for that reason.
- See [Suspend Functions]({{ "/en/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
