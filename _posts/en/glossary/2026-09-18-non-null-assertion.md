---
layout: post
title: "!! (Non-Null Assertion)"
date: 2026-09-18 12:00:00 +0000
categories: [en, glossary]
tags: [null-safety, error-handling]
lang: en
permalink: /en/glossary/non-null-assertion/
---

## The Theory (The What)

**`!!`** is the non-null [assertion]({{ "/en/glossary/assertion/" | relative_url }}) operator: `x!!` converts a `T?` into a `T` by throwing [`NullPointerException`]({{ "/en/glossary/null-pointer-exception/" | relative_url }}) if `x` is [`null`]({{ "/en/glossary/null/" | relative_url }}). It is the one place where Kotlin lets you opt out of null safety, and the [Null Safety: Elvis & Safe Calls]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}) article's position is that it should never appear in production code: it trades a [compile-time]({{ "/en/glossary/compile-time/" | relative_url }}) guarantee for a [runtime]({{ "/en/glossary/runtime/" | relative_url }}) crash whose [stack trace]({{ "/en/glossary/stack-trace/" | relative_url }}) says *where* but never *why*.

```kotlin
// Not found in FAS — standalone example
val details = productDetails!!          // NPE with no message if null

// Each alternative says *why* the value must exist
val details = productDetails ?: return false                       // guard clause
val details = checkNotNull(productDetails) { "connect() not called" } // named invariant
val details = requireNotNull(productDetails) { "details required" }   // named precondition
```

## The Senior Nuance

- **`!!` is a claim that you know more than the compiler.** Sometimes true — but then encode the knowledge: redesign so the type is non-null, or use [`checkNotNull`]({{ "/en/glossary/check-not-null/" | relative_url }}) / [`requireNotNull`]({{ "/en/glossary/require-not-null/" | relative_url }}) with a message. Same crash, useful diagnostics.
- **Legitimate-looking uses are usually design smells.** `_binding!!` in Fragments, `intent.extras!!`, `map[key]!!`: each one hides a lifecycle or data assumption that a [`?: return`]({{ "/en/glossary/elvis-return/" | relative_url }}) or an [Elvis]({{ "/en/glossary/elvis-operator/" | relative_url }}) default would make explicit.
- **Tests are the exception.** In a test, `!!` on a value the test just set up is acceptable: a failure there is a test bug, and the NPE points at it directly.
- See [Null Safety: Elvis & Safe Calls]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
