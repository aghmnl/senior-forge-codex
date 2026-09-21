---
layout: post
title: "== (Structural Equality)"
date: 2026-09-21 12:00:00 +0000
categories: [en, glossary]
tags: [type-system, data-classes, syntax]
lang: en
permalink: /en/glossary/structural-equality/
---

## The Theory (The What)

**`==`** is structural equality: `a == b` compiles to `a?.equals(b) ?: (b === null)`, so it asks the object whether it is *equivalent*, not whether it is the same instance. `Any.equals` defaults to identity, a [Data Classes: copy, equals, toString]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}) generates it from the [primary constructor]({{ "/en/glossary/primary-constructor/" | relative_url }}) properties, and a [`data object`]({{ "/en/glossary/data-object/" | relative_url }}) inherits the singleton's identity — where structural and [referential equality]({{ "/en/glossary/referential-equality/" | relative_url }}) coincide. `!=` is its negation.

```kotlin
// Not found in FAS — standalone example
data class TaskId(val value: String)
TaskId("a") == TaskId("a")     // true  — equivalent content
TaskId("a") === TaskId("a")    // false — two instances

data object Loading
val a: Any = Loading; val b: Any = Loading
a == b                          // true
a === b                         // true — one instance, so both agree
```

## The Senior Nuance

- **Kotlin's `==` is Java's `.equals`, safely.** The null check is built in, so the Java habit of `Objects.equals(a, b)` is unnecessary — and comparing [strings]({{ "/en/glossary/string/" | relative_url }}) with `==` compares content, not references.
- **`==` is only as good as `equals`.** On a plain class it falls back to identity, which is why hand-written models that "look equal" fail assertions; on a data class it ignores properties declared in the class body.
- **It travels with [`hashCode`]({{ "/en/glossary/hash-code/" | relative_url }}).** Two objects that are `==` must return the same `hashCode`, or hash collections misbehave.
- See [Data Classes: copy, equals, toString]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
