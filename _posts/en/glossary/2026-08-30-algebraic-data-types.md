---
layout: post
title: "Algebraic Data Types (ADTs)"
date: 2026-08-30 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/algebraic-data-types/
---

## The Theory (The What)

**Algebraic Data Types (ADTs)** are composite types formed by combining other types through two fundamental operations: **sum types** (a value is one of several variants) and **product types** (a value contains several fields). In Kotlin, sum types are modeled with `sealed class` / `sealed interface` ([sealed hierarchies]({{ "/en/glossary/sealed-hierarchy/" | relative_url }})), and product types are modeled with `data class` (where each constructor parameter is a "factor" of the product). Together they let you define a closed, exhaustive domain model that the compiler can verify.

```kotlin
// From FollowApp Suite — RecurrenceRule.kt
// Sum type: RecurrenceEnd is exactly one of these three variants
sealed class RecurrenceEnd {
    data object Never : RecurrenceEnd()                          // unit variant (no data)
    data class AfterOccurrences(val remaining: Int) : RecurrenceEnd()  // product: 1 field
    data class UntilDate(val date: Long) : RecurrenceEnd()             // product: 1 field
}

// From FollowApp Suite — ArchiveUiState.kt
// Sum type: each action is a data object (stateless variant)
sealed class ArchiveBulkAction {
    data object Unarchive : ArchiveBulkAction()
    data object Delete : ArchiveBulkAction()
}
```

## The Senior Nuance

- The power of ADTs is exhaustiveness: a `when` expression over a sealed hierarchy requires handling every variant. Adding a new variant is a compile-time breaking change — the compiler flags every unhandled branch. This is why ADTs are the foundation of safe [state transitions]({{ "/en/glossary/state-transitions/" | relative_url }}).
- `data object` variants are the ADT equivalent of unit types (variants that carry no data). They are [singletons]({{ "/en/glossary/singleton/" | relative_url }}) and create zero [allocations]({{ "/en/glossary/allocations/" | relative_url }}) when emitted, which matters in high-frequency [state emission patterns]({{ "/en/glossary/state-emission-patterns/" | relative_url }}).
- Kotlin's ADTs are not as powerful as Haskell's or Rust's `enum` — they lack automatic pattern destructuring and recursive type definitions. But combined with smart casts in `when`, they provide the same practical safety for Android state modeling.
- When designing an ADT, ask: "Can I enumerate every legal state?" If yes, use a sealed hierarchy. If the set of states is open-ended (plugins, user-defined types), use an interface or [abstract class]({{ "/en/glossary/abstract-class/" | relative_url }}) instead.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
