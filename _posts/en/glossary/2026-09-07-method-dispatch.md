---
layout: post
title: "Method Dispatch"
date: 2026-09-07 12:00:00 +0000
categories: [en, glossary]
tags: [dispatch, oop, jvm]
lang: en
permalink: /en/glossary/method-dispatch/
---

## The Theory (The What)

**Method dispatch** is how the [JVM]({{ "/en/glossary/jvm/" | relative_url }}) decides *which* implementation of a method actually runs for a given call. There are two mechanisms, and the difference is *when* the decision is made:

- **[Static dispatch]({{ "/en/glossary/static-dispatch/" | relative_url }})** — resolved at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) from the *declared* type. Used for [`final`]({{ "/en/glossary/final/" | relative_url }}), `private`, top-level and [extension functions]({{ "/en/glossary/extension-functions/" | relative_url }}), and for [function overloading]({{ "/en/glossary/function-overloading/" | relative_url }}).
- **[Virtual dispatch]({{ "/en/glossary/virtual-dispatch/" | relative_url }})** — resolved at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) from the *actual* object, by looking the method up in the [vtable]({{ "/en/glossary/vtable/" | relative_url }}). This is what makes [polymorphism]({{ "/en/glossary/polymorphism/" | relative_url }}) work.

```kotlin
// From FollowApp Suite — StateChip.kt
// Virtual dispatch: the ChipState reference is resolved at runtime
// to Full, Outline or Partial, each with its own inputColors().
sealed interface ChipState {
    @Composable fun inputColors(): SelectableChipColors
}
```

## The Senior Nuance

- **[Extension functions]({{ "/en/glossary/extension-functions/" | relative_url }}) are statically dispatched, and this is a classic interview trap.** `fun Animal.speak() = "..."` and `fun Dog.speak() = "woof"` called on a variable *declared* `Animal` will always run the `Animal` version, regardless of the runtime object. Extensions are compiled to static functions taking the [receiver]({{ "/en/glossary/receiver-type/" | relative_url }}) as the first parameter — they do not enter the [vtable]({{ "/en/glossary/vtable/" | relative_url }}) and cannot be overridden.
- **[Overload resolution]({{ "/en/glossary/overload-resolution/" | relative_url }}) is a compile-time decision too.** Given `fun log(a: Any)` and `fun log(s: String)`, calling with a variable typed `Any` that holds a `String` picks the `Any` overload. Overloading is *ad-hoc* [polymorphism]({{ "/en/glossary/polymorphism/" | relative_url }}); only overriding is dynamic.
- **Kotlin's [`final`]({{ "/en/glossary/final/" | relative_url }})-by-default is a dispatch optimisation.** Non-open methods are candidates for devirtualisation by the [JIT compiler]({{ "/en/glossary/jit-compilation/" | relative_url }}) and by [R8]({{ "/en/glossary/r8/" | relative_url }}) — the [virtual dispatch]({{ "/en/glossary/virtual-dispatch/" | relative_url }}) becomes [static dispatch]({{ "/en/glossary/static-dispatch/" | relative_url }}), and the body is often inlined. In [hot loops]({{ "/en/glossary/hot-loops/" | relative_url }}) this is measurable.
- **Interface dispatch is the slowest of the three.** The JVM uses `invokeinterface`, which cannot rely on a fixed [vtable]({{ "/en/glossary/vtable/" | relative_url }}) slot the way class [virtual dispatch]({{ "/en/glossary/virtual-dispatch/" | relative_url }}) does. Modern JITs mitigate it with inline caches, so it is rarely worth designing around — but it is worth knowing when asked.
- **[`inline` functions]({{ "/en/glossary/inline-functions/" | relative_url }}) have no dispatch at all.** The body is copied into the [call site]({{ "/en/glossary/call-site/" | relative_url }}), which is exactly why [`reified`]({{ "/en/glossary/reified/" | relative_url }}) can work there.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
