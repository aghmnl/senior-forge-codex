---
layout: post
title: "data object"
date: 2026-09-21 12:00:00 +0000
categories: [en, glossary]
tags: [sealed-types, state-management, oop]
lang: en
permalink: /en/glossary/data-object/
---

## The Theory (The What)

**`data object`** (stable since Kotlin 1.9) is an [object declaration]({{ "/en/glossary/object/" | relative_url }}) with compiler-generated `toString`, `equals` and `hashCode`. The `toString` prints just the declaration name — `Loading` instead of `Loading@3a71f4dd` — which is the whole reason it exists. It does **not** generate `copy()` or `componentN()`: a [singleton]({{ "/en/glossary/singleton/" | relative_url }}) has no constructor properties to copy or destructure, which is the exact line that separates it from a [Data Classes: copy, equals, toString]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}).

```kotlin
// From FollowApp Suite — RecurrenceRule.kt
sealed class RecurrenceEnd {
    data object Never : RecurrenceEnd()                   // no payload → data object
    data class AfterOccurrences(val remaining: Int) : RecurrenceEnd()
    data class UntilDate(val date: Long) : RecurrenceEnd()
}

println(RecurrenceEnd.Never)      // "Never", not "Never@3a71f4dd"
```

## The Senior Nuance

- **The convention for sealed hierarchies:** `data object` for stateless members, `data class` for members carrying data. That split is what makes logs, crash reports and test assertion messages readable.
- **Zero [allocations]({{ "/en/glossary/allocations/" | relative_url }}) for stateless states.** A `Loading` emitted a thousand times by a [`StateFlow`]({{ "/en/glossary/stateflow/" | relative_url }}) reuses one instance; a `data class Loading()` would allocate a thousand objects for the GC.
- **It must stay immutable.** A `var` inside a `data object` is global state with the process's lifetime, and it also breaks the [`hashCode`]({{ "/en/glossary/hash-code/" | relative_url }}) contract if the object sits in a hash collection.
- See [Data Objects: Singleton & Memory Savings]({{ "/en/01-kotlin-core/data-objects/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
