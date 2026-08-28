---
layout: post
title: "NullPointerException"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/null-pointer-exception/
---

## The Theory (The What)

A **NullPointerException** (NPE) is a runtime exception thrown when code attempts to use a reference that points to `null` — calling a method, accessing a property, or indexing on a null object. On the JVM, it is the single most common cause of application crashes.

## The Senior Nuance

- Kotlin's [null safety]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}) system was designed specifically to eliminate NPEs at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}). Nullable types (`String?`) and non-nullable types (`String`) are distinct in the type system, so the compiler refuses code that could dereference null without a check.
- Kotlin code can still throw NPE in four situations: explicit `!!` usage, Java interop with unannotated platform types, uninitialized `lateinit` access, and incorrect `equals` implementations. A Senior treats each as a boundary to defend.
- On Android, NPE is the top crash category in production. Firebase Crashlytics reports consistently show that most NPEs originate at Java/Kotlin interop boundaries — particularly when Android framework callbacks return platform types.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
