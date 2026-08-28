---
layout: post
title: "Primary Constructor"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/primary-constructor/
---

## The Theory (The What)

A **primary constructor** in Kotlin is declared directly in the class header, after the class name. Its parameters can be promoted to properties with `val` or `var`, and the compiler uses them to define the class's initialization contract. Unlike Java, where constructors live inside the class body, Kotlin's primary constructor is part of the class signature itself.

```kotlin
// From FollowApp Suite — BillingConnector.kt
class BillingConnector(
    context: Context,
    private val productId: String
) {
    private val _isOwned = MutableStateFlow<Boolean?>(null)
    val isOwned: StateFlow<Boolean?> = _isOwned.asStateFlow()
}
```

## The Senior Nuance

- In a `data class`, the primary constructor is critical: the compiler generates `equals()`, `hashCode()`, `toString()`, `copy()`, and `componentN()` exclusively from its parameters. Properties declared in the body are invisible to these generated methods — a common source of subtle bugs.
- Primary constructor parameters without `val`/`var` are just constructor arguments, accessible only during initialization (in `init` blocks and property initializers). Adding `val`/`var` promotes them to class properties with backing fields. This distinction matters for memory and visibility.
- A class can have secondary constructors (declared with `constructor` in the body), but they must delegate to the primary constructor — either directly or through another secondary constructor. This ensures the primary constructor's contract is always fulfilled.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
