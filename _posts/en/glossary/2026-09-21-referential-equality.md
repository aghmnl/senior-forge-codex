---
layout: post
title: "=== (Referential Equality)"
date: 2026-09-21 12:00:00 +0000
categories: [en, glossary]
tags: [type-system, jvm, syntax]
lang: en
permalink: /en/glossary/referential-equality/
---

## The Theory (The What)

**`===`** is referential equality: it is `true` only when both operands point to the *same instance*, and it can never be overridden. It is the counterpart of [`==`]({{ "/en/glossary/structural-equality/" | relative_url }}), which asks about equivalence. For a [`data object`]({{ "/en/glossary/data-object/" | relative_url }}) the two always agree, because there is exactly one instance; for a [Data Classes: copy, equals, toString]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}) with identical contents they disagree — `==` is `true`, `===` is `false`. `!==` is its negation.

```kotlin
// Not found in FAS — standalone example
data class Loading0()            // a class, so a new instance every time
Loading0() == Loading0()         // true  — equals over zero properties
Loading0() === Loading0()        // false — two allocations

data object Loading1             // a singleton
val x: Any = Loading1
x === Loading1                   // true  — and == agrees
```

## The Senior Nuance

- **Use it to prove identity, not equivalence.** Checking that a cached instance was reused, that [`copy()`]({{ "/en/glossary/copy/" | relative_url }}) did not copy, or that a singleton really is one: those are `===` questions. Everything else is `==`.
- **It is why a stateless `data class` is the wrong tool.** `data class Loading()` gives you `==` true but `===` false plus one [allocation]({{ "/en/glossary/allocations/" | relative_url }}) per use; a `data object` gives you both and zero allocations.
- **Compose reads identity too.** Skipping recomposition relies on instance comparison for unstable types, so gratuitously new instances of "the same" state defeat it.
- See [Data Objects: Singleton & Memory Savings]({{ "/en/01-kotlin-core/data-objects/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
