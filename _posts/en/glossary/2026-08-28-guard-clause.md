---
layout: post
title: "Guard Clause"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/guard-clause/
---

## The Theory (The What)

A **guard clause** is an early return at the top of a function that rejects invalid or edge-case inputs before the main logic runs. By handling the exceptional case first and returning immediately, the rest of the function can assume the happy path without nested conditionals.

## The Senior Nuance

- In Kotlin, the Elvis operator with `return` (`val x = nullable ?: return`) is the idiomatic guard clause for null checks. It eliminates the nullable type from the rest of the [scope]({{ "/en/glossary/scope/" | relative_url }}), making the remaining code work with non-null types only — no `!!`, no nested `if`.
- Guard clauses can also return a value (`?: return false`), throw (`?: throw IllegalArgumentException("reason")`), or continue a loop (`?: continue`). Each communicates a different contract.
- Overusing guard clauses can fragment a function's exit points. A Senior balances early returns with readability: if a function has more than three guards, the caller might be responsible for validation instead.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
