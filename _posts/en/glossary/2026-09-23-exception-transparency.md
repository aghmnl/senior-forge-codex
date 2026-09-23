---
layout: post
title: "Exception Transparency"
date: 2026-09-23 12:00:00 +0000
categories: [en, glossary]
tags: [flow, error-handling, coroutines]
lang: en
permalink: /en/glossary/exception-transparency/
---

## The Theory (The What)

**Exception transparency** is the [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) contract that a producer must let exceptions travel to its collector instead of catching its own emissions. A `flow { }` builder that wraps its [`emit`]({{ "/en/glossary/emit/" | relative_url }}) in a `try/catch` violates it and fails at runtime with `Flow exception transparency is violated`. The sanctioned way to handle a failure is the [`catch`]({{ "/en/glossary/catch/" | relative_url }}) operator, which is why `catch` only ever sees its [upstream]({{ "/en/glossary/upstream/" | relative_url }}): the pipeline stays a chain of declarations whose failures are attributable to a specific segment.

```kotlin
// Not found in FAS — standalone example
// Violates transparency: throws "Flow exception transparency is violated"
flow {
    try { emit(load()) } catch (e: IOException) { emit(fallback()) }
}

// Correct: the producer stays transparent, catch handles it downstream
flow { emit(load()) }
    .catch { emit(fallback()) }
```

## The Senior Nuance

- **It is what makes `catch` predictable.** Because no operator may swallow its own emissions, a failure always surfaces at the first `catch` below the segment that produced it — you can read the chain and know who handles what.
- **`catch` cannot reach [downstream]({{ "/en/glossary/downstream/" | relative_url }}).** An exception thrown inside `collect` is not the producer's failure, so the operator above it does not see it. That is the same rule, viewed from the other end.
- **`try/catch` around your *own* non-emitting work is fine.** Transparency is about emissions, not about every statement inside the builder.
- See [Error Handling: try-catch & .catch]({{ "/en/02-coroutines-flow/error-handling/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
