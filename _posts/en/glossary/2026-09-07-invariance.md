---
layout: post
title: "Invariance"
date: 2026-09-07 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/invariance/
---

## The Theory (The What)

**Invariance** is Kotlin's default [variance]({{ "/en/glossary/variance/" | relative_url }}): `Box<Cat>` and `Box<Animal>` have *no* subtyping relationship in either direction, even though `Cat` is a subtype of `Animal`. A [generic type parameter]({{ "/en/glossary/generic-type-parameters/" | relative_url }}) written without `in` or `out` is invariant.

It is the correct answer whenever the type is both produced and consumed:

```kotlin
// From FollowApp Suite — DragToReorder.kt
@Stable
class ReorderState<K : Any> internal constructor(
    private val onMove: (fromKey: K, toKey: K) -> Boolean,   // K consumed
    private val onLongPressOnly: (K) -> Unit                 // K consumed
) {
    var draggingKey: K? by mutableStateOf(null)              // K produced
        private set

    internal var liveKeys: List<K> = emptyList()             // K produced

    fun isDragging(key: K): Boolean = key == draggingKey     // K consumed
}
```

`ReorderState` cannot be `out K` (`isDragging` takes a `K`) and cannot be `in K` (`draggingKey` returns one). Invariance is not a missing annotation here — it is the type system correctly reporting that this object owns `K` in both directions.

## The Senior Nuance

- **Invariance is a signal, not a failure.** When the compiler rejects `out`, it is telling you the class consumes the type somewhere. Forcing variance and patching the holes with unchecked casts converts a [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) error into a [`ClassCastException`]({{ "/en/glossary/class-cast-exception/" | relative_url }}) at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) — strictly worse.
- **`MutableList<E>` is the everyday example.** It is invariant because it both reads and writes; `List<out E>` is [covariant]({{ "/en/glossary/covariance/" | relative_url }}) because it only reads. The same class pair explains `Channel<E>` (invariant) against `Flow<out T>` (covariant) in [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}).
- **The escape hatch is projection, not casting.** If a caller genuinely does not care about the type argument, give it a [star projection]({{ "/en/glossary/star-projection/" | relative_url }}) (`ReorderState<*>`) or a use-site projection (`Array<out Any>`). Both keep [type safety]({{ "/en/glossary/type-safety/" | relative_url }}) by restricting which operations remain available, instead of discarding it.
- **Arrays are invariant in Kotlin and covariant in Java** — a deliberate fix. Java's `Object[] a = new String[1]; a[0] = 1;` compiles and throws `ArrayStoreException` at runtime. Kotlin's `Array<T>` is invariant, so the same mistake is a compile error. This is a favourite interview follow-up.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
