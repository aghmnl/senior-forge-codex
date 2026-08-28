---
layout: post
title: "Static Dispatch"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/static-dispatch/
---

## The Theory (The What)

**Static dispatch** means the function to call is determined at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}), based on the declared type of the variable — not the actual object at [runtime]({{ "/en/glossary/runtime/" | relative_url }}). This is the opposite of virtual (dynamic) dispatch, where the [JVM]({{ "/en/glossary/jvm/" | relative_url }}) looks up the correct overridden method in the object's vtable at runtime.

In Kotlin, [extension functions]({{ "/en/glossary/extension-functions/" | relative_url }}) are the most prominent example of static dispatch: they compile to static [JVM]({{ "/en/glossary/jvm/" | relative_url }}) methods where the [receiver type]({{ "/en/glossary/receiver-type/" | relative_url }}) becomes the first parameter.

## The Senior Nuance

- The practical impact: if `fun Animal.greet()` and `fun Dog.greet()` both exist, and you call `greet()` on a variable declared as `Animal` that holds a `Dog`, the `Animal` version is called. The compiler chose it at compile time — the runtime type is irrelevant. This surprises developers who expect [polymorphism]({{ "/en/glossary/polymorphism/" | relative_url }}).
- Static dispatch has zero overhead — no vtable lookup, no indirection. This is why extension functions are as fast as regular static utility methods.
- The `companion object` functions, top-level functions, and `@JvmStatic` methods also use static dispatch. Understanding which calls are static vs. virtual is essential for reasoning about both performance and correctness in Kotlin.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
