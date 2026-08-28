---
layout: post
title: "Assertion"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/assertion/
---

## The Theory (The What)

An **assertion** is a statement that declares a condition the developer believes to be true at a given point. If the condition is false, the program fails immediately. In Kotlin, assertions include `require` (validates function arguments, throws `IllegalArgumentException`), `check` (validates object state, throws `IllegalStateException`), `assert` (JVM assertion, disabled by default), and the non-null assertion `!!` (throws [NullPointerException]({{ "/en/glossary/null-pointer-exception/" | relative_url }})).

## The Senior Nuance

- `require` and `check` are the preferred assertion functions in Kotlin because they produce meaningful exception messages: `require(age >= 0) { "Age must be non-negative: $age" }`. They document the contract in code.
- The non-null assertion `!!` is the weakest form of assertion: it makes a claim about nullability but provides no message when wrong. Prefer `requireNotNull(value) { "reason" }` or `checkNotNull(value) { "reason" }` — they serve the same purpose with a meaningful [stack trace]({{ "/en/glossary/stack-trace/" | relative_url }}).
- Assertions belong at system boundaries (API input, configuration parsing, deserialization). Inside a well-typed internal API, the type system should make impossible states unrepresentable, eliminating the need for runtime assertions.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
