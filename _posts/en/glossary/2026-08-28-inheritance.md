---
layout: post
title: "Inheritance"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/inheritance/
---

## The Theory (The What)

**Inheritance** is the mechanism by which a class (subclass) acquires the properties and behavior of another class (superclass). In Kotlin, classes are `final` by default — they cannot be inherited from unless explicitly marked `open`. Interfaces, abstract classes, and sealed hierarchies provide controlled forms of inheritance.

```kotlin
// From FollowApp Suite — StateChip.kt
sealed interface ChipState {
    val foreground: Color @Composable get
    val border: BorderStroke? @Composable get
    val strikethrough: Boolean get() = false
    @Composable fun inputColors(): SelectableChipColors
    @Composable fun filterColors(): SelectableChipColors
}

object Full : ChipState {
    override val foreground: Color
        @Composable get() = MaterialTheme.colorScheme.onPrimaryContainer
    override val border: BorderStroke? @Composable get() = null
    // ...
}
```

## The Senior Nuance

- Kotlin's "final by default" is a deliberate design decision: inheritance is the tightest form of coupling. Opening a class creates a permanent contract — every public and protected member becomes an API that subclasses depend on. Use `open` intentionally, not habitually.
- Data classes cannot be `open` (since Kotlin 1.1+). This prevents inheritance from breaking the compiler-generated `equals()`, `hashCode()`, and `copy()` — which depend exclusively on the [primary constructor]({{ "/en/glossary/primary-constructor/" | relative_url }}).
- Prefer composition over inheritance. A sealed interface (like the FAS example) defines a contract without implementation coupling: each implementor is independent. When you need shared behavior, use [extension functions]({{ "/en/glossary/extension-functions/" | relative_url }}) or delegation (`by`) instead of a deep class hierarchy.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
