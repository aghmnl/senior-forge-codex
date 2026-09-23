---
layout: post
title: "Throwable"
date: 2026-09-23 12:00:00 +0000
categories: [en, glossary]
tags: [error-handling, jvm]
lang: en
permalink: /en/glossary/throwable/
---

## The Theory (The What)

**`Throwable`** is the root of the JVM's error hierarchy: everything that can be thrown is a `Throwable`, split into `Exception` (recoverable conditions, including [`RuntimeException`]({{ "/en/glossary/runtime-exception/" | relative_url }})) and `Error` (`OutOfMemoryError`, `StackOverflowError` — failures an application is not expected to handle). Catching `Throwable` therefore catches *everything*, which is why [`runCatching`]({{ "/en/glossary/run-catching/" | relative_url }}) is dangerous in [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) code: `Throwable` includes [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}).

```kotlin
// From FollowApp Suite — ErrorMapping.kt
// Throwable is the right receiver for a mapper: it must accept anything
fun Throwable.toUserMessage(): Int = when {
    this is SQLiteConstraintException && message.orEmpty().contains("UNIQUE") ->
        R.string.error_duplicate_tag
    else -> R.string.error_generic
}
```

## The Senior Nuance

- **`Throwable` is the right type to *receive*, the wrong one to *catch*.** A mapper, a logger or a crash reporter should accept `Throwable`; a `catch` block almost never should.
- **`Error` is not yours to handle.** Catching `OutOfMemoryError` to "keep going" usually produces a zombie process that fails in a stranger way a second later.
- **The [stack trace]({{ "/en/glossary/stack-trace/" | relative_url }}) is the payload.** Whatever you do with a `Throwable`, keep the cause chain: logging `e.message` alone throws away the part that identifies the bug.
- See [Error Handling: try-catch & .catch]({{ "/en/02-coroutines-flow/error-handling/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
