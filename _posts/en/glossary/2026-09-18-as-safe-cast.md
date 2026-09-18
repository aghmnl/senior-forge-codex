---
layout: post
title: "as? (Safe Cast)"
date: 2026-09-18 12:00:00 +0000
categories: [en, glossary]
tags: [type-system, null-safety]
lang: en
permalink: /en/glossary/as-safe-cast/
---

## The Theory (The What)

**`as?`** is the *safe* [cast]({{ "/en/glossary/cast/" | relative_url }}) operator: `x as? Foo` returns `x` typed as `Foo?` when the cast succeeds and `null` when it does not — it never throws [`ClassCastException`]({{ "/en/glossary/class-cast-exception/" | relative_url }}). The result is nullable by design, so it composes with the [safe call]({{ "/en/glossary/safe-call/" | relative_url }}) `?.` and the Elvis operator `?:` into one-line expressions: `(value as? Long)?.toInt() ?: 0`. It is the fallback the [Smart Casts]({{ "/en/01-kotlin-core/smart-casts/" | relative_url }}) article prescribes when a smart cast is unavailable and the type is legitimately uncertain.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// as? returns null if the LabelValue is Scale (not Tag); ?. and ?: handle the null
val taskLabels = (task.customLabels["labels"] as? LabelValue.Tag)
    ?.values?.toSet() ?: emptySet()

// From FollowApp Suite — RecurrenceCalculator.kt
val until = (rule.end as? RecurrenceEnd.UntilDate)?.date
```

## The Senior Nuance

- **`as?` turns a type question into a null question.** That is its strength — Kotlin has excellent tooling for nulls — and its trap: the null now needs a decision (`?:` default, early return, `let`). A bare `as?` whose result is later hit with `!!` is worse than the [`as`]({{ "/en/glossary/as-cast/" | relative_url }}) it replaced.
- **Expression vs control flow.** `as?` shines inside expressions (`?.let`, `?:`, mapping); when you are already branching, `if (x is Foo)` gives a non-null `Foo` and reads better than `(x as? Foo)?.let { }`.
- **A null from `as?` can hide a bug.** If a value should *always* be that type, `as?` silently returns null and the failure surfaces far away. Use `as` (or `check(x is Foo)`) when a wrong type is a programming error.
- See [Smart Casts]({{ "/en/01-kotlin-core/smart-casts/" | relative_url }}) and [Null Safety]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
