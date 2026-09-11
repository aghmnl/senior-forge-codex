---
layout: post
title: "MutableMap"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
tags: [collections, generics]
lang: en
permalink: /en/glossary/mutable-map/
---

## The Theory (The What)

**`MutableMap<K, V>`** extends [`Map`]({{ "/en/glossary/maps/" | relative_url }}) with [`put`]({{ "/en/glossary/put/" | relative_url }}) (also written `map[key] = value`), [`remove`]({{ "/en/glossary/remove/" | relative_url }}), [`clear`]({{ "/en/glossary/clear/" | relative_url }}) and the helpers `getOrPut` and `merge`. `mutableMapOf()` is backed by a `LinkedHashMap`.

```kotlin
// From FollowApp Suite — GetLabelReferenceCounts.kt
val refCounts = mutableMapOf<String, Int>()
tasks.forEach { task ->
    // ...
    refCounts[label] = (refCounts[label] ?: 0) + 1
}
return refCounts     // published as Map<String, Int>
```

## The Senior Nuance

- Counting and grouping are the two jobs where a `MutableMap` beats a [collection operator]({{ "/en/glossary/collection-operators/" | relative_url }}) chain: the in-place update is one hash lookup per element, where [`groupBy`]({{ "/en/glossary/group-by/" | relative_url }}) plus `mapValues` builds an intermediate map of lists first.
- `refCounts[k] = (refCounts[k] ?: 0) + 1` reads and writes; `getOrPut(k) { 0 }` is the same idea with one lookup instead of two. Neither is atomic — a `MutableMap` under [concurrency]({{ "/en/glossary/concurrency/" | relative_url }}) needs confinement to a single [stack frame]({{ "/en/glossary/stack-frame/" | relative_url }}), not a `ConcurrentHashMap` bolted on afterwards.
- `Map<K, out V>` is [covariant]({{ "/en/glossary/covariance/" | relative_url }}) in its *value* only; `MutableMap<K, V>` is fully [invariant]({{ "/en/glossary/invariance/" | relative_url }}). Keys are never covariant, in either version, because they are hashed and compared.

**Kotlin docs:** [`kotlin.collections.MutableMap`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-mutable-map/)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
