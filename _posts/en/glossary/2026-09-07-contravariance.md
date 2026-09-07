---
layout: post
title: "Contravariance"
date: 2026-09-07 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/contravariance/
---

## The Theory (The What)

**Contravariance** is the [variance]({{ "/en/glossary/variance/" | relative_url }}) that *reverses* subtyping direction: if `Cat` is a subtype of `Animal`, then `Consumer<Animal>` is a subtype of `Consumer<Cat>`. Kotlin declares it with `in`:

```kotlin
// Not found in FAS — standalone example
interface Consumer<in T> {
    fun consume(item: T)     // T only in a parameter — legal
    // fun produce(): T      // ERROR: T in an "out" position
}

val animalSink: Consumer<Animal> = AnimalLogger()
val catSink: Consumer<Cat> = animalSink   // OK: contravariance
```

The reversal is intuitive once stated in plain language: something that can handle *any* `Animal` can certainly handle a `Cat`. A consumer of a broader type is usable wherever a consumer of a narrower type is required.

## The Senior Nuance

- **It corresponds to Java's `? super T`** — the "Consumer-Super" half of PECS. `Comparable<in T>` is the canonical example in both languages: a `Comparable<Any>` can compare `String`s, so it is safely usable as a `Comparable<String>`.
- **Contravariance is much rarer than [covariance]({{ "/en/glossary/covariance/" | relative_url }}) in application code**, because most generic types you write hand values *out* rather than swallow them. Where it shows up is in [callbacks]({{ "/en/glossary/callbacks/" | relative_url }}), comparators and event sinks — anything whose whole job is to receive.
- **Function parameters are contravariant, and you rely on this daily.** `(T) -> R` compiles to `Function1<in P1, out R>`. That is why a handler typed `(Any) -> Unit` can be passed where `(Task) -> Unit` is expected, but not the reverse. Every [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) parameter in a generic API — `itemKey: (T) -> String`, `onMove: (K, K) -> Boolean` — inherits this without any annotation.
- **The override rule mirrors it.** A [return type]({{ "/en/glossary/return-type/" | relative_url }}) may be narrowed when overriding; a parameter type may not, because parameters sit in the contravariant position. Attempting it produces an overload, not an override — a classic silent bug that [`function overloading`]({{ "/en/glossary/function-overloading/" | relative_url }}) rules will happily let you ship.
- **A type that both consumes and produces cannot be `in`.** If `T` appears in even one [return type]({{ "/en/glossary/return-type/" | relative_url }}), the class must stay [invariant]({{ "/en/glossary/invariance/" | relative_url }}). The positional rule is symmetric and admits no exceptions outside `@UnsafeVariance`.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
