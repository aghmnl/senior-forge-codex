---
layout: post
title: "Covariance"
date: 2026-09-07 12:00:00 +0000
categories: [en, glossary]
tags: [generics, type-system, immutability]
lang: en
permalink: /en/glossary/covariance/
---

## The Theory (The What)

**Covariance** is the [variance]({{ "/en/glossary/variance/" | relative_url }}) that preserves subtyping direction: if `Cat` is a subtype of `Animal`, then `Producer<Cat>` is a subtype of `Producer<Animal>`. Kotlin declares it with `out`:

```kotlin
// Not found in FAS — standalone example
interface Producer<out T> {
    fun produce(): T          // T only in a return type — legal
    // fun consume(item: T)   // ERROR: T in an "in" position
}

val cats: Producer<Cat> = CatFactory()
val animals: Producer<Animal> = cats   // OK: covariance
```

The `out` [keyword]({{ "/en/glossary/keyword/" | relative_url }}) is both a permission and a restriction: it grants the subtyping relationship, and in exchange the compiler forbids `T` from appearing anywhere except [return types]({{ "/en/glossary/return-type/" | relative_url }}). The class may only *produce* `T`, never consume it.

The most-used covariant type in Kotlin is the read-only list:

```kotlin
// From FollowApp Suite — SelectableListScaffold.kt
fun <T> SelectableListScaffold(
    items: List<T>,        // List<out E>: covariant, read-only
    itemKey: (T) -> String,
    // ...
)
```

## The Senior Nuance

- **Covariance is sound only without writes.** If `MutableList<E>` were covariant, you could bind a `MutableList<Cat>` to a `MutableList<Animal>` reference and then `add(Dog())` — the list would hold a `Dog` while every reader expects a `Cat`, producing a [`ClassCastException`]({{ "/en/glossary/class-cast-exception/" | relative_url }}) far from the actual bug. Kotlin's read-only/mutable [collections]({{ "/en/glossary/collections/" | relative_url }}) split exists to make covariance safe: `List<out E>` is covariant, `MutableList<E>` is [invariant]({{ "/en/glossary/invariance/" | relative_url }}). This is [immutability]({{ "/en/glossary/immutability/" | relative_url }}) paying for itself in the type system.
- **It corresponds to Java's `? extends T`.** PECS ("Producer-Extends") is the same rule stated at the use site. Kotlin's advantage is that `out` is declared once on the class, so no [call site]({{ "/en/glossary/call-site/" | relative_url }}) has to repeat it.
- **`Flow<out T>` and `Deferred<out T>` are covariant** for exactly this reason: they only emit values. `SendChannel<in E>` is [contravariant]({{ "/en/glossary/contravariance/" | relative_url }}), and `Channel<E>` — which does both — is invariant. Reading the [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}) API through variance tells you which types are producers, consumers, or both, without reading a single method.
- **`out` also expresses ownership.** Declaring a [sealed hierarchy]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}) of results as `sealed interface Result<out T>` lets `Result.Loading` (which carries no `T`) be a `Result<Nothing>` and therefore assignable to any `Result<X>`. That trick is only available because of covariance.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
