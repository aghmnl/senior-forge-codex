---
layout: post
title: "Protected State"
date: 2026-08-30 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/protected-state/
---

## The Theory (The What)

**Protected state** refers to properties or fields declared with the `protected` visibility modifier, making them accessible only within the class itself and its subclasses. In Kotlin, `protected` members are invisible to code outside the [inheritance]({{ "/en/glossary/inheritance/" | relative_url }}) chain — unlike Java, where `protected` also grants package-level access. Protected state is a key differentiator between `sealed class` and `sealed interface`: a sealed class can hold protected properties and `init` blocks that subclasses inherit, while a sealed interface cannot hold any state at all.

```kotlin
// sealed class WITH protected state — subtypes inherit shared fields
sealed class NetworkResult {
    protected val timestamp: Long = System.currentTimeMillis()

    data class Success(val data: String) : NetworkResult()
    data class Error(val code: Int) : NetworkResult()
}

// sealed interface — NO protected state possible.
// Each implementation is structurally independent
sealed interface UIEvent
```

## The Senior Nuance

- The presence or absence of protected state is the decision criterion for choosing between `sealed class` and `sealed interface`. If subtypes need shared internal state (properties, `init` blocks, helper methods), use a [sealed class]({{ "/en/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}). If they don't, prefer a sealed interface for its multiple-[inheritance]({{ "/en/glossary/inheritance/" | relative_url }}) flexibility.
- In Android architecture, protected state in ViewModels or base classes is a code smell: it creates implicit coupling between parent and child, making behavior harder to trace. Prefer composition (injecting dependencies) over protected state in most cases.
- Kotlin's `protected` is stricter than Java's: it does not grant package-level access. A `protected` property in a Kotlin class is truly visible only to subclasses, making it a tighter encapsulation boundary.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
