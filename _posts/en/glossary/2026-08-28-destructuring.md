---
layout: post
title: "Destructuring"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/destructuring/
---

## The Theory (The What)

**Destructuring** in Kotlin allows unpacking an object's properties into separate variables in a single declaration. It works through `componentN()` operator functions: `component1()` maps to the first variable, `component2()` to the second, and so on. Data classes generate these functions automatically for their [primary constructor]({{ "/en/glossary/primary-constructor/" | relative_url }}) properties.

```kotlin
// From FollowApp Suite — TaskConfirmationDialogs.kt
val (titleRes, messageRes) = when (action) {
    is BulkAction.Complete -> R.string.bulk_complete_title to R.string.bulk_complete_message
    is BulkAction.Archive -> R.string.bulk_archive_title to R.string.bulk_archive_message
    is BulkAction.Delete -> R.string.bulk_delete_title to R.string.bulk_delete_message
}
```

## The Senior Nuance

- Destructuring binds by *position*, not by name. If the order of [primary constructor]({{ "/en/glossary/primary-constructor/" | relative_url }}) properties changes, all destructuring sites silently bind to different values — no compiler error. This is a refactoring hazard in large codebases.
- Use `_` to skip components you don't need: `val (_, second) = pair`. This is cleaner than introducing an unused variable and avoids lint warnings.
- Destructuring works in [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}) too: `.map { (key, value) -> ... }` is more readable than `.map { entry -> entry.key ... }` when iterating [maps]({{ "/en/glossary/maps/" | relative_url }}). But avoid deeply nested destructuring — it becomes unreadable fast.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
