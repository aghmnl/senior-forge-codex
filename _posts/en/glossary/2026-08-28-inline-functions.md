---
layout: post
title: "Inline Functions"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/inline-functions/
---

## The Theory (The What)

An **inline function** is a function marked with the `inline` keyword that the Kotlin compiler copies (inlines) at every call site during [compile time]({{ "/en/glossary/compile-time/" | relative_url }}), rather than generating a regular function call. The function body — and crucially, any lambda parameters — are substituted directly into the caller's [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}). This eliminates the overhead of creating lambda objects and the indirect call to `invoke()`, making inline functions the mechanism behind zero-cost abstractions in Kotlin.

## The Senior Nuance

- The primary benefit of `inline` is **lambda inlining**, not the function body itself. Without `inline`, each lambda creates an anonymous class instance on the [JVM]({{ "/en/glossary/jvm/" | relative_url }}). With `inline`, the lambda's code is pasted directly into the call site — no object allocation, no virtual dispatch.
- [`reified`]({{ "/en/glossary/reified/" | relative_url }}) type parameters are **only** possible with inline functions. Because the function body is copied at each call site, the compiler can substitute the actual type argument — circumventing the JVM's type erasure that normally removes generic type information from bytecode.
- `noinline` marks a lambda parameter that should *not* be inlined (e.g., when it needs to be stored in a field or passed to a non-inline function). `crossinline` marks a lambda that will be inlined but called from a context where non-local returns are forbidden (e.g., inside another lambda).
- Kotlin's standard library scoping functions (`let`, `run`, `with`, `apply`, `also`) are all `inline`. This means using `someValue.let { transform(it) }` compiles to the same bytecode as writing the transformation directly — zero overhead.
- Overusing `inline` on large functions increases bytecode size (the body is duplicated at every call site). The compiler warns when `inline` provides no benefit (no lambda parameters, no reified types).

```kotlin
// Not found in FAS — standalone example
inline fun <reified T> List<*>.filterByType(): List<T> =
    filterIsInstance<T>()

val strings = listOf("a", 1, "b", 2).filterByType<String>()
// Compiler inlines the body AND substitutes String for T at this call site
```

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
