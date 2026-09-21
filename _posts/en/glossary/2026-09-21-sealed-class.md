---
layout: post
title: "sealed class"
date: 2026-09-21 12:00:00 +0000
categories: [en, glossary]
tags: [sealed-types, oop, state-management]
lang: en
permalink: /en/glossary/sealed-class/
---

## The Theory (The What)

**`sealed class`** declares a [sealed hierarchy]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}) whose direct subtypes must all live in the same package and module. Being a class, it can carry shared structure: [constructor]({{ "/en/glossary/primary-constructor/" | relative_url }}) properties, [`abstract`]({{ "/en/glossary/abstract-class/" | relative_url }}) members that every subtype must provide, concrete methods, an [`init`]({{ "/en/glossary/init/" | relative_url }}) block and a [companion object]({{ "/en/glossary/companion-object/" | relative_url }}). That is what separates it from a [`sealed interface`]({{ "/en/glossary/sealed-interface/" | relative_url }}) — and the price is the JVM's single inheritance, so a subtype can extend only one of them.

```kotlin
// From FollowApp Suite — CascadeAction in TasksUiState.kt
// Shared state declared once in the base, provided by each variant
sealed class CascadeAction {
    abstract val taskId: String
    abstract val childCount: Int

    data class Archive(
        override val taskId: String,
        override val childCount: Int
    ) : CascadeAction()
}
```

## The Senior Nuance

- **Reach for it only when the hierarchy genuinely shares something.** Shared properties, a common method, an `init` validation or a companion with constants. Without one of those, a [`sealed interface`]({{ "/en/glossary/sealed-interface/" | relative_url }}) is the better default.
- **`abstract val` in the base, `override val` in each variant.** That declares the shared contract once instead of repeating fields — and the compiler enforces it.
- **Single inheritance is the real constraint.** If a variant must also satisfy a second contract (analytics, logging), the sealed class cannot provide it; the variants implement an interface as well, or the whole hierarchy becomes a sealed interface.
- See [Sealed Classes vs Sealed Interfaces]({{ "/en/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
