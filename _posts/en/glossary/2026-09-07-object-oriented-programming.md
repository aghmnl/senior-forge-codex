---
layout: post
title: "Object-Oriented Programming"
date: 2026-09-07 12:00:00 +0000
categories: [en, glossary]
tags: [oop, design-principles]
lang: en
permalink: /en/glossary/object-oriented-programming/
---

## The Theory (The What)

**Object-Oriented Programming (OOP)** is the paradigm that models a program as objects — bundles of state and the behaviour that operates on it — rather than as procedures over shared data. It rests on four pillars:

- **Encapsulation** — internal state is private; the object exposes a controlled surface. Kotlin's `private`/`internal` visibility and [backing fields]({{ "/en/glossary/backing-field/" | relative_url }}) are the tooling.
- **Abstraction** — callers depend on an interface or [abstract class]({{ "/en/glossary/abstract-class/" | relative_url }}), not a concrete implementation.
- **[Inheritance]({{ "/en/glossary/inheritance/" | relative_url }})** — a [subclass]({{ "/en/glossary/subclass/" | relative_url }}) reuses and specialises a parent's behaviour.
- **[Polymorphism]({{ "/en/glossary/polymorphism/" | relative_url }})** — one reference type stands for many implementations, resolved by [method dispatch]({{ "/en/glossary/method-dispatch/" | relative_url }}).

```kotlin
// From FollowApp Suite — PremiumLedgerRepositoryImpl.kt
// Abstraction: callers depend on the interface, not this class.
class PremiumLedgerRepositoryImpl(
    private val preferences: PremiumLedgerPreferences
) : PremiumLedgerRepository {
    override fun getLedger(): Flow<PremiumLedger> = preferences.getLedger()
}
```

## The Senior Nuance

- **Kotlin deliberately discourages [inheritance]({{ "/en/glossary/inheritance/" | relative_url }}).** Classes and methods are [`final`]({{ "/en/glossary/final/" | relative_url }}) by default; you must opt in with `open`. This inverts Java's default and encodes "prefer composition over inheritance" into the language rather than leaving it to a style guide.
- **Modern Android is only partly OOP.** [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) is declarative and function-based — a `@Composable` is not a class hierarchy. A Senior reads Android as layered: OOP for the [data layer]({{ "/en/glossary/data-layer/" | relative_url }}) and [state holders]({{ "/en/glossary/state-holder/" | relative_url }}), [functional style]({{ "/en/glossary/functional-style/" | relative_url }}) for transformations, declarative for UI. Insisting on one paradigm everywhere is the mistake.
- **[Sealed hierarchies]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}) are OOP's answer to [algebraic data types]({{ "/en/glossary/algebraic-data-types/" | relative_url }}).** They give [polymorphism]({{ "/en/glossary/polymorphism/" | relative_url }}) plus [exhaustiveness]({{ "/en/glossary/exhaustiveness/" | relative_url }}) — the compiler knows the complete set of [subclasses]({{ "/en/glossary/subclass/" | relative_url }}), so `when` needs no `else`.
- **The [SOLID]({{ "/en/glossary/single-responsibility-principle/" | relative_url }}) principles are OOP design rules, not laws.** They are worth quoting in an interview, but a Senior justifies a design by its coupling and testability, not by naming a principle.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
