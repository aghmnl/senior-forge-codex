---
layout: post
title: "?: (Elvis Operator)"
date: 2026-09-18 12:00:00 +0000
categories: [en, glossary]
tags: [null-safety, syntax]
lang: en
permalink: /en/glossary/elvis-operator/
---

## The Theory (The What)

**`?:`** — the Elvis operator — evaluates to its left operand when that is not [`null`]({{ "/en/glossary/null/" | relative_url }}), and to its right operand otherwise: `a ?: b`. The right side can be any expression, including [`throw`]({{ "/en/glossary/throw/" | relative_url }}), `return`, `continue` or `break`, because those have type `Nothing` and collapse the result to the non-null type. It is the second core operator of [Null Safety: Elvis & Safe Calls]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}), usually chained after a [safe call]({{ "/en/glossary/safe-call/" | relative_url }}): `user?.name ?: "Anonymous"`. The name comes from the emoticon `?:` looking like Elvis Presley's hair.

```kotlin
// From FollowApp Suite — PresetRepositoryImpl
// Elvis as default: safe fallback in production
fun resolvePosition(existing: Preset?): Int {
    return existing?.position ?: dao.nextPosition()
}

// From FollowApp Suite — BillingConnector
// Elvis as guard clause: exits the function when null
val details = productDetails ?: return false
```

## The Senior Nuance

- **Three idioms, one operator.** Default value (`?: 0`), early exit ([`?: return`]({{ "/en/glossary/elvis-return/" | relative_url }})) and named failure (`?: throw`[`IllegalStateException`]({{ "/en/glossary/illegal-state-exception/" | relative_url }})`(...)`). Each replaces a `!!` with a stated decision about what null means here.
- **The right side is evaluated lazily.** `cache ?: load()` only calls `load()` on a miss, so Elvis doubles as a cheap memoisation pattern.
- **Watch `?.let { } ?: else`.** If the `let` block returns null, the Elvis branch runs too. Use `if/else` when the block's result can be null.
- See [Null Safety: Elvis & Safe Calls]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
