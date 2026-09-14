---
layout: post
title: "Invariant"
date: 2026-09-13 12:00:00 +0000
categories: [en, glossary]
tags: [design-principles, error-handling, type-system]
lang: en
permalink: /en/glossary/invariant/
---

## The Theory (The What)

An **invariant** is a condition that must hold true at a given point of a program — for an object throughout its lifetime, for a function's arguments on entry, for its result on exit. "A `Task` always has a non-blank title", "a backup file has the format we wrote". Invariants are what the code *assumes*; making them explicit is what turns a mysterious crash into a readable one.

```kotlin
// From FollowApp Suite — BackupSerializer.kt
require(root.optString("format") == FORMAT) { "Not a MyTasks backup file" }
require(root.optInt("version", -1) == VERSION) {
    "Unsupported backup version: ${root.optString("version")}"
}
```

Kotlin's [assertion]({{ "/en/glossary/assertion/" | relative_url }}) functions map onto the three kinds: `require` (argument invariant → `IllegalArgumentException`), `check` (state invariant → `IllegalStateException`), and `?: throw` / `error()` for anything else. Each takes a lazy message, which is the invariant written in plain language.

## The Senior Nuance

- **The best invariant is one the type system enforces.** A non-nullable parameter, a [sealed hierarchy]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}) or a value class removes the need for a runtime check altogether. Reach for `require`/`check` only where the type cannot say it — input parsed from the outside world, ordering constraints, cross-field rules.
- **Assert at boundaries, trust inside.** Validate once at the edge (deserialisation, API input, user forms) and let the interior assume the invariant. Re-checking at every layer is noise that hides which layer actually owns the rule.
- **The message is the point.** `?: throw IllegalStateException("order required at checkout")` produces a [stack trace]({{ "/en/glossary/stack-trace/" | relative_url }}) that explains *which* invariant broke; `!!` produces a [NullPointerException]({{ "/en/glossary/null-pointer-exception/" | relative_url }}) that only says *where*. See [Null Safety: Elvis & Safe Calls]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).
- **Immutable state makes invariants cheap.** With a [data class]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}) built once through a factory, the invariant is checked at construction and can never be broken afterwards — unless `copy()` bypasses the factory, which is the one hole to watch.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
