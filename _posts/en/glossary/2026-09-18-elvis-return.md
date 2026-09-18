---
layout: post
title: "?: return (Elvis Early Return)"
date: 2026-09-18 12:00:00 +0000
categories: [en, glossary]
tags: [null-safety, design-principles, syntax]
lang: en
permalink: /en/glossary/elvis-return/
---

## The Theory (The What)

**`?: return`** is the [Elvis operator]({{ "/en/glossary/elvis-operator/" | relative_url }}) with `return` as its right-hand side: `val x = nullable ?: return`. Because `return` has type `Nothing`, the expression's type collapses to the non-null `T`, and the function exits immediately when the value is [`null`]({{ "/en/glossary/null/" | relative_url }}). It is the idiomatic [guard clause]({{ "/en/glossary/guard-clause/" | relative_url }}) in Kotlin — it removes nullability from the rest of the function [scope]({{ "/en/glossary/scope/" | relative_url }}) in one line, keeps the happy path flat, and is the first alternative [Null Safety: Elvis & Safe Calls]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}) gives to `!!`. The same shape works with `?: continue`, `?: break` and `?: throw`.

```kotlin
// From FollowApp Suite — BillingConnector
// Guard clause with Elvis: eliminates null from the rest of the scope
fun launchPurchase(activity: Activity): Boolean {
    val details = productDetails ?: return false
    // details: ProductDetails (non-null) from here on
    ...
}

// From FollowApp Suite — TasksViewModel
fun onCascadeConfirmed() {
    val action = _uiState.value.pendingCascadeAction ?: return
    ...
}
```

## The Senior Nuance

- **It changes the type, not just the flow.** After `val details = productDetails ?: return false`, `details` is `ProductDetails`, not `ProductDetails?`; every later line is free of `?.`. That is the difference between a guard clause and an `if (x == null) return` that leaves `x` nullable.
- **Put it at the top.** Guard clauses belong in the first lines of the function so the reader learns the preconditions before the logic. A `?: return` buried mid-function is a hidden exit.
- **Return a meaningful value.** `?: return false`, `?: return emptyList()`, `?: return@launch`: the value (or label) documents what "nothing to do" means for this function.
- See [Null Safety: Elvis & Safe Calls]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
