---
layout: post
title: "ClassCastException"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/class-cast-exception/
---

## The Theory (The What)

A **ClassCastException** is a runtime exception thrown when an unsafe [cast]({{ "/en/glossary/cast/" | relative_url }}) (`as`) fails — the object's actual type is not compatible with the target type. It is the casting equivalent of [NullPointerException]({{ "/en/glossary/null-pointer-exception/" | relative_url }}): a crash caused by a wrong assumption about a value's type at runtime.

## The Senior Nuance

- In Kotlin, the safe cast `as?` returns `null` instead of throwing `ClassCastException`, making it the preferred choice when type uncertainty exists.
- [Smart casts]({{ "/en/01-kotlin-core/smart-casts/" | relative_url }}) eliminate `ClassCastException` entirely for most patterns: after an `is` check, the compiler guarantees the cast is valid.
- `ClassCastException` can still occur through generic type erasure: `listOf(1, 2) as List<String>` succeeds at the cast (the JVM only sees `List`) but throws `ClassCastException` later when elements are accessed as `String`.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
