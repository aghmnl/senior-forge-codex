---
layout: post
title: "componentN"
date: 2026-09-19 12:00:00 +0000
categories: [en, glossary]
tags: [data-classes, syntax, compiler]
lang: en
permalink: /en/glossary/component-n/
---

## The Theory (The What)

**`componentN()`** are the `operator fun component1()`, `component2()`, … that a [Data Classes: copy, equals, toString]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}) generates, one per [primary constructor]({{ "/en/glossary/primary-constructor/" | relative_url }}) property, in declaration order. They are what [destructuring declarations]({{ "/en/glossary/destructuring/" | relative_url }}) compile to: `val (name, age) = user` becomes `val name = user.component1(); val age = user.component2()`. Any class can opt in by declaring those operators by hand — destructuring is a convention, not a data-class privilege.

```kotlin
// From FollowApp Suite — MyTasksApplication.kt
// Triple is a data class: component1/2/3 make this destructuring work
val (language, themeMode, contrastLevel) = runBlocking { ... }

// Opting in without a data class
class Size(val w: Int, val h: Int) {
    operator fun component1() = w
    operator fun component2() = h
}
val (w, h) = Size(1080, 1920)
```

## The Senior Nuance

- **Positional, not by name.** `val (a, b) = point` binds by *position*; reordering the primary constructor silently swaps the variables at every destructuring site and still compiles. That is the argument against destructuring classes with several same-typed properties.
- **Great for pairs, entries and lambdas.** `map.forEach { (k, v) -> }`, `list.withIndex()`, [`Triple`]({{ "/en/glossary/triple/" | relative_url }}) returns: here the meaning of each position is obvious and destructuring removes noise.
- **Use `_` to skip.** `val (_, themeMode, _) = config` documents that you only need the middle value.
- See [Data Classes: copy, equals, toString]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
