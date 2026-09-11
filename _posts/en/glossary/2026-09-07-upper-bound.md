---
layout: post
title: "Upper Bound"
date: 2026-09-07 12:00:00 +0000
categories: [en, glossary]
tags: [generics, type-system]
lang: en
permalink: /en/glossary/upper-bound/
---

## The Theory (The What)

An **upper bound** constrains which types may be substituted for a [generic type parameter]({{ "/en/glossary/generic-type-parameters/" | relative_url }}). It is written with a colon: `<K : Any>` means "any `K`, as long as it is a subtype of `Any`".

Without an explicit bound, the implicit upper bound is `Any?` — which allows nullable types. Declaring `: Any` is therefore how you require non-null:

```kotlin
// From FollowApp Suite — DragToReorder.kt
// K is used as a map key, so it must be non-null.
class ReorderState<K : Any> internal constructor(/* ... */) {
    private val itemCoords = mutableMapOf<K, LayoutCoordinates>()
}

@Composable
fun <K : Any> rememberReorderState(
    keys: List<K>,
    onMove: (fromKey: K, toKey: K) -> Boolean,
    // ...
): ReorderState<K>
```

Multiple bounds require the `where` clause, since only one bound fits in the angle brackets:

```kotlin
// Not found in FAS — standalone example
fun <T> sortAndLog(items: List<T>): List<T>
    where T : Comparable<T>,
          T : CharSequence = items.sorted()
```

## The Senior Nuance

- **The bound is what the compiler knows.** Inside a generic function, you may only call members guaranteed by the upper bound. With `<T>` (bound `Any?`) you cannot even call `toString()` without a null check; with `<T : Any>` you can. Choosing the bound is choosing the API available in the body.
- **`: Any` is the most common bound in Android code**, because map keys, [collection]({{ "/en/glossary/collections/" | relative_url }}) elements used for identity, and anything compared with `==` behave badly when null is permitted. `ReorderState<K : Any>` is exactly that case: keys index a `mutableMapOf`.
- **Bounds must be repeated on every declaration in the API.** The [extension functions]({{ "/en/glossary/extension-functions/" | relative_url }}) that consume `ReorderState` all restate `<K : Any>`, which is what keeps `K` a single consistent type across the whole gesture API rather than degrading to `Any?` at some boundary.
- **[Star projection]({{ "/en/glossary/star-projection/" | relative_url }}) reads widen to the upper bound.** Given `ReorderState<*>`, `draggingKey` comes back typed as `Any?` — the bound, not the real type. The tighter the bound, the more useful star-projected reads are.
- **Bounds are erased too.** After [Type Erasure]({{ "/en/glossary/type-erasure/" | relative_url }}), a `<T : CharSequence>` parameter is compiled as `CharSequence` rather than `Object`. This is occasionally visible in [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) and in Java interop signatures.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
