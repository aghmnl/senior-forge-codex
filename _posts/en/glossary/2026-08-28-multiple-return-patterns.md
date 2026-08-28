---
layout: post
title: "Multiple Return Patterns"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/multiple-return-patterns/
---

## The Theory (The What)

Kotlin functions return a single value, but **multiple return patterns** allow bundling several values together. The most common approaches are `Pair<A, B>`, `Triple<A, B, C>`, and custom `data class` types. All three support [destructuring]({{ "/en/glossary/destructuring/" | relative_url }}), so callers can unpack the values directly.

```kotlin
// From FollowApp Suite — PremiumUseCaseTest.kt
private fun useCase(
    installedDaysAgo: Int,
    skipFreeTrial: Boolean = false
): Pair<GetPremiumStatusUseCase, FakeLedgerRepository> {
    val ledgerRepo = FakeLedgerRepository(
        System.currentTimeMillis() - installedDaysAgo * dayMs, skipFreeTrial
    )
    return GetPremiumStatusUseCase(ledgerRepo, authRepo) to ledgerRepo
}

// Usage — destructuring the Pair
val (getStatus, _) = useCase(installedDaysAgo = 10)
```

## The Senior Nuance

- `Pair` and `Triple` are convenient but their component names (`first`, `second`, `third`) carry no semantic meaning. For public APIs or when the return values are not obvious from context, prefer a named `data class` — it documents intent and survives refactoring.
- The `to` infix function creates a `Pair`, which is why `mapOf("a" to 1)` works. But `to` allocates a `Pair` object each time — in performance-critical code building large [maps]({{ "/en/glossary/maps/" | relative_url }}), prefer `buildMap { put("a", 1) }`.
- [Destructuring]({{ "/en/glossary/destructuring/" | relative_url }}) is what makes multiple return patterns ergonomic: `val (status, repo) = useCase(10)` reads almost like a multi-assignment. Without destructuring, you would need `result.first` and `result.second`, which is noisy and fragile.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
