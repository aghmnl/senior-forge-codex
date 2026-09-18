---
layout: post
title: "requireNotNull"
date: 2026-09-18 12:00:00 +0000
categories: [en, glossary]
tags: [null-safety, error-handling]
lang: en
permalink: /en/glossary/require-not-null/
---

## The Theory (The What)

**`requireNotNull(value) { "message" }`** throws `IllegalArgumentException` if `value` is null and otherwise returns it as a non-null type. It is [`require`]({{ "/en/glossary/require/" | relative_url }}) specialised for nullability, and the explicit alternative to `!!` when a null *argument* is a caller bug. Its [contract]({{ "/en/glossary/contract/" | relative_url }}) (`returns() implies (value != null)`) means that after the call the original variable is also [Smart Casts]({{ "/en/01-kotlin-core/smart-casts/" | relative_url }}) smart-cast to non-null — you can use the return value or keep using the variable.

```kotlin
// Not found in FAS — standalone example
fun openTask(taskId: String?) {
    val id = requireNotNull(taskId) { "openTask needs a taskId" }   // id: String
    // taskId is also smart-cast to String from here on
    repository.load(id)
}
```

## The Senior Nuance

- **The message is the whole point.** `taskId!!` and `requireNotNull(taskId)` crash on the same input; only the second one leaves a [stack trace]({{ "/en/glossary/stack-trace/" | relative_url }}) that says *what* was expected. It converts a generic [`NullPointerException`]({{ "/en/glossary/null-pointer-exception/" | relative_url }}) into a named precondition.
- **Prefer redesign when you can.** If a parameter must never be null, declare it `String` and let the type system reject the call at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}). `requireNotNull` is for boundaries where the nullable type is imposed (Java APIs, `Intent` extras, [platform types]({{ "/en/glossary/platform-types/" | relative_url }})).
- **Argument → `requireNotNull`; state → [`checkNotNull`]({{ "/en/glossary/check-not-null/" | relative_url }}).** Same rule as `require` vs `check`.
- See [Smart Casts]({{ "/en/01-kotlin-core/smart-casts/" | relative_url }}) and [Null Safety]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
