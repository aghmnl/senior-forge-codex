---
layout: post
title: "Pure Function"
date: 2026-09-28 12:00:00 +0000
categories: [en, glossary]
tags: [functional, design-principles, testing]
lang: en
permalink: /en/glossary/pure-function/
---

## The Theory (The What)

A **pure function** is a function that **always returns the same result for the same inputs** and **has no side effects**: it does not change anything outside itself (no writes to state, no logs, no network calls, no database) and does not depend on anything that is not in its parameters, such as the current time. Its result depends only on its arguments.

```kotlin
// From FollowApp Suite — PremiumLifecycle.kt
// Pure: "now" comes in as a parameter instead of being read from the clock,
// so the same inputs always give the same answer
fun isPremium(now: Long, premiumUntil: Long, isSignedIn: Boolean = false): Boolean {
    val effectiveUntil = if (isSignedIn) premiumUntil + SIGN_IN_REWARD_DAYS * DAY_MS else premiumUntil
    return now < effectiveUntil
}
```

## The Senior Nuance

- **Pure functions are trivial to test.** No mocks, no setup, no clock: call it with inputs and check the output. Passing "now" as a parameter, as in the example, is what makes time-based logic testable.
- **Some APIs require them.** The lambda of [update {}]({{ "/en/glossary/update/" | relative_url }}) can run more than once, so a side effect inside it can happen twice. Keeping it pure is what makes the retry safe.
- **A whole app cannot be pure, and that is fine.** The goal is to keep the logic pure and push side effects (I/O, database, UI) to the edges, where they are few and easy to see.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
