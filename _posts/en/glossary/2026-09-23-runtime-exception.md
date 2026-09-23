---
layout: post
title: "RuntimeException"
date: 2026-09-23 12:00:00 +0000
categories: [en, glossary]
tags: [error-handling, jvm]
lang: en
permalink: /en/glossary/runtime-exception/
---

## The Theory (The What)

**`RuntimeException`** is the JVM base class for *unchecked* exceptions — those a method does not have to declare and a caller is not forced to handle: `NullPointerException`, `IllegalStateException`, `IllegalArgumentException`. In Kotlin every exception is effectively unchecked, so the distinction matters less than in Java, with one sharp exception: [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) extends `RuntimeException`, which is why a broad `catch (e: Exception)` silently swallows cancellation.

```kotlin
// Not found in FAS — standalone example
// Catches real failures AND the cancellation signal — the coroutine survives
// its own cancellation and the scope never completes
try { work() } catch (e: Exception) { log(e) }

// Correct: let cancellation through
try { work() } catch (e: Exception) {
    if (e is CancellationException) throw e
    log(e)
}
```

## The Senior Nuance

- **"Unchecked" does not mean "unimportant".** It means the compiler will not remind you. In Kotlin, the KDoc and the tests are the only record of what a function can throw.
- **The cancellation trap is the practical consequence.** Any broad catch in [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) code has to let `CancellationException` through, and so does [`runCatching`]({{ "/en/glossary/run-catching/" | relative_url }}), which catches `Throwable`.
- **Prefer narrow catches.** Catching the exception a call can actually produce documents the failure mode; catching `Exception` documents nothing.
- See [Error Handling: try-catch & .catch]({{ "/en/02-coroutines-flow/error-handling/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
