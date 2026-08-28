---
layout: post
title: "Intent Signaling"
date: 2026-08-21 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/intent-signaling/
---

## The Theory (The What)

**Intent signaling** is the practice of choosing language constructs, naming conventions, or patterns that communicate the *purpose* of the code to future readers — not just what the code does, but why it was written this way. In Kotlin, this concept is particularly visible with [scope functions]({{ "/en/01-kotlin-core/scope-functions/" | relative_url }}): using `apply` signals "I am configuring this object," while `let` signals "I am transforming this value." The code compiles and runs identically either way, but the choice tells the reader what the developer intended.

## The Senior Nuance

- Intent signaling is what separates code that "works" from code that is maintainable. A Senior Engineer writes code for the next developer, not just the compiler.
- Beyond scope functions, intent signaling applies to: choosing `val` over `var` (signaling immutability), using [sealed classes]({{ "/en/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}) over enums (signaling that subtypes carry data), naming a function `computeX` vs. `getX` (signaling cost), or returning `Result<T>` vs. throwing exceptions (signaling expected failure).
- In code reviews, mismatched intent signals are a common flag: code that uses `apply` but actually transforms, or code that uses `also` but modifies the object, suggests the developer didn't fully consider the operation's nature.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
