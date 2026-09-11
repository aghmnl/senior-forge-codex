---
layout: post
title: "Read-Only View"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
tags: [collections, immutability, generics]
lang: en
permalink: /en/glossary/read-only-view/
---

## The Theory (The What)

A **read-only view** is a reference whose *type* omits mutating operations, over an object that may still be mutable. Kotlin's [collections]({{ "/en/glossary/collections/" | relative_url }}) are built this way: `List<out E>` declares no `add` or `remove`, and `MutableList<E>` extends it with them. Upcasting a `MutableList` to `List` produces a read-only view — not a new, [immutable]({{ "/en/glossary/immutability/" | relative_url }}) object.

```kotlin
// From FollowApp Suite — GetLabelReferenceCounts.kt
operator fun invoke(tasks: List<Task>, scaleName: String): Map<String, Int> {
    val refCounts = mutableMapOf<String, Int>()
    // ...populate in place...
    return refCounts     // returned as a read-only view of a LinkedHashMap
}
```

## The Senior Nuance

- The view is safe only while the underlying object is unreachable by anyone who could [mutate]({{ "/en/glossary/mutation/" | relative_url }}) it. Returning a local accumulator (as above) is safe: the mutable reference dies with the [stack frame]({{ "/en/glossary/stack-frame/" | relative_url }}). Exposing a long-lived private `MutableList` through a read-only property is not — callers get a live window that can change under them.
- A read-only view is exactly what makes [covariance]({{ "/en/glossary/covariance/" | relative_url }}) sound. `List<out E>` can be [covariant]({{ "/en/glossary/covariance/" | relative_url }}) because there is no write position for `E`; `MutableList<E>` must remain [invariant]({{ "/en/glossary/invariance/" | relative_url }}).
- To turn a view into a value, take a [defensive copy]({{ "/en/glossary/defensive-copy/" | relative_url }}) with `toList()`, or use a [persistent collection]({{ "/en/glossary/persistent-collections/" | relative_url }}). Java interop bypasses the view entirely: a `List<String>` handed to Java code is just a `java.util.List` and can be written to.

**Kotlin docs:** [Collection types: read-only vs mutable](https://kotlinlang.org/docs/collections-overview.html#collection-types)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
