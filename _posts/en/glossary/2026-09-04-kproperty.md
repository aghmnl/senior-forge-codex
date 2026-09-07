---
layout: post
title: "KProperty"
date: 2026-09-04 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/kproperty/
---

## The Theory (The What)

**`KProperty<*>`** is the [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) reflection type that represents a Kotlin property. It is part of the `kotlin.reflect` package and carries metadata about the property: its name, return type, visibility, and whether it is `lateinit`, `const`, or a [delegated property]({{ "/en/01-kotlin-core/delegated-properties/" | relative_url }}).

Every [delegated property]({{ "/en/01-kotlin-core/delegated-properties/" | relative_url }}) operator — `getValue`, `setValue`, and `provideDelegate` — receives a `KProperty<*>` parameter. The compiler generates this object automatically at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) and passes it on every access:

```kotlin
operator fun <T> ReadOnlyProperty<Any?, T>.getValue(
    thisRef: Any?,
    property: KProperty<*>
): T
```

The hierarchy is: `KCallable` → `KProperty` → `KProperty0` (top-level) / `KProperty1` (member) / `KProperty2` (extension). Mutable variants are `KMutableProperty0`, etc.

## The Senior Nuance

- A Senior uses `property.name` inside custom delegates for automatic key derivation — for instance, mapping property names to SharedPreferences keys or database column names without hardcoded strings. This is one of the most practical uses of the `KProperty` parameter.
- Accessing `KProperty` metadata does not require the full `kotlin-reflect` dependency. The basic `KProperty` interface and its `name` field are part of `kotlin-stdlib`. Full reflection (annotations, type parameters, generic bounds) requires the `kotlin-reflect` artifact.
- In [delegated properties]({{ "/en/01-kotlin-core/delegated-properties/" | relative_url }}), the `KProperty<*>` instance is created once per property declaration (not per access) and reused. The [overhead]({{ "/en/glossary/overhead/" | relative_url }}) is a single static field per delegated property — negligible in practice.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
