---
layout: post
title: "by (Delegation)"
date: 2026-09-04 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/by-delegation/
---

## The Theory (The What)

**`by`** is the Kotlin [keyword]({{ "/en/glossary/keyword/" | relative_url }}) that connects a property to its [property delegate]({{ "/en/glossary/property-delegate/" | relative_url }}). It is a soft keyword — it has special meaning only after a property declaration (`val`/`var`) and can be used as a regular identifier elsewhere.

```kotlin
val name: String by lazy { computeName() }
var count by mutableStateOf(0)
val host: String by configMap
```

When the compiler encounters `by`, it:

1. Evaluates the expression on the right to obtain the delegate object.
2. If the delegate defines `provideDelegate`, calls it first to obtain the actual delegate.
3. Generates a hidden field to store the delegate instance.
4. Rewrites every property access into a call to the delegate's `operator fun getValue` (and `setValue` for `var`), passing the owner instance (`thisRef`) and a [KProperty]({{ "/en/glossary/kproperty/" | relative_url }}) metadata object.

`by` is also used for class delegation (`class MyList<T>(inner: List<T>) : List<T> by inner`), which delegates interface implementation to another object. This is a separate mechanism but shares the same [keyword]({{ "/en/glossary/keyword/" | relative_url }}).

## The Senior Nuance

- A Senior recognizes that `by` is resolved entirely at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}): the compiler looks for `operator fun getValue`/`setValue` via [operator overloading]({{ "/en/glossary/operator-overloading/" | relative_url }}) conventions, not through an interface check. This means a delegate does not need to implement `ReadOnlyProperty` — it just needs the right operator signatures.
- In Compose, `by` has a dual role: `by remember { mutableStateOf() }` delegates to the [snapshot system]({{ "/en/glossary/snapshot-system/" | relative_url }}), making the variable both readable and writable with automatic recomposition. Without `by`, you write `state.value` everywhere. The `by` keyword here turns a `State<T>` wrapper into what looks like a plain variable.
- Understanding that `by` creates a hidden delegate field is essential for debugging: when inspecting an object in the debugger, delegated properties appear as their delegate wrapper, not as their unwrapped value. The actual value is inside the delegate's internal field.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
