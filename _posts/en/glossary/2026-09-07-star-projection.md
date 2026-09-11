---
layout: post
title: "Star Projection"
date: 2026-09-07 12:00:00 +0000
categories: [en, glossary]
tags: [generics, type-system]
lang: en
permalink: /en/glossary/star-projection/
---

## The Theory (The What)

A **star projection** — written `Foo<*>` — says "this is a `Foo` of *some* concrete type, and I do not know which one". It is Kotlin's [type-safe]({{ "/en/glossary/type-safety/" | relative_url }}) replacement for Java's [raw types]({{ "/en/glossary/raw-types/" | relative_url }}).

The compiler keeps tracking that a real type argument exists, and enforces an asymmetry:

- **Reads** are allowed, widened to the [upper bound]({{ "/en/glossary/upper-bound/" | relative_url }}).
- **Writes** are forbidden, because no value can be proven to match the unknown type.

```kotlin
// Not found in FAS — standalone example
fun logDragActivity(state: ReorderState<*>) {
    // Read: K? widens to the upper bound, Any?
    val key: Any? = state.draggingKey
    println("dragging: $key")

    // state.isDragging(someKey)   // does not compile: K is unknown for writes
}
```

Star projection is also the only generic check that survives [Type Erasure]({{ "/en/glossary/type-erasure/" | relative_url }}): `list is List<*>` compiles, `list is List<String>` does not.

## The Senior Nuance

- **`<*>` is not a [raw type]({{ "/en/glossary/raw-types/" | relative_url }}).** A Java raw `List` lets you both read and write unchecked, deferring failure to a [`ClassCastException`]({{ "/en/glossary/class-cast-exception/" | relative_url }}). `List<*>` refuses the write at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}). The difference is where the bug surfaces.
- **It is per-parameter.** For `Map<K, V>`, `Map<*, *>` projects both, but `Map<String, *>` projects only the value type — useful when you know one half of the signature.
- **The read type is the [upper bound]({{ "/en/glossary/upper-bound/" | relative_url }}), not `Any?` by default.** `ReorderState<*>.draggingKey` reads as `Any?` because the bound is `Any` and the property is nullable; a `Foo<T : CharSequence>` star-projected would read as `CharSequence`. Tighter bounds make star projection genuinely usable.
- **Reach for it before reaching for [`reified`]({{ "/en/glossary/reified/" | relative_url }}).** Much code that "needs the type at [Runtime]({{ "/en/glossary/runtime/" | relative_url }})" only needs to *not care* about it. Logging, counting, and clearing a generic container are all star-projection jobs, and they carry none of the [code bloat]({{ "/en/glossary/code-bloat/" | relative_url }}) that [inline]({{ "/en/glossary/inline-functions/" | relative_url }}) reification does.
- **`<*>` differs from `<Any?>`.** `MutableList<Any?>` is a list that genuinely accepts anything, so writes are legal. `MutableList<*>` is a list of one unknown specific type, so writes are not. Confusing the two is a common source of "why won't this compile" in review.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
