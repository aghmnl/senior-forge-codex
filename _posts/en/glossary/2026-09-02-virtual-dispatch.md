---
layout: post
title: "Virtual Dispatch"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/virtual-dispatch/
---

## The Theory (The What)

**Virtual dispatch** (also called dynamic dispatch) means the function to call is determined at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}), based on the actual type of the object — not the declared type of the variable. The [JVM]({{ "/en/glossary/jvm/" | relative_url }}) uses a [vtable]({{ "/en/glossary/vtable/" | relative_url }}) (virtual method table) to look up the correct overridden method for the object's concrete class. This is the mechanism behind [polymorphism]({{ "/en/glossary/polymorphism/" | relative_url }}): calling `animal.sound()` on a `Dog` instance runs `Dog.sound()`, even when the variable is typed as `Animal`.

This is the opposite of [static dispatch]({{ "/en/glossary/static-dispatch/" | relative_url }}), where the compiler resolves the call at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) based on the declared type alone.

```kotlin
// Virtual dispatch in action
open class Animal {
    open fun sound() = "..."
}

class Dog : Animal() {
    override fun sound() = "Woof"
}

val animal: Animal = Dog()
animal.sound() // "Woof" — resolved at runtime via vtable
```

## The Senior Nuance

- In Kotlin, all non-`final` member functions use virtual dispatch. Since Kotlin classes and methods are `final` by default (you must write `open`), the compiler can often devirtualize calls — replacing virtual dispatch with a direct call when it can prove the concrete type. This is a JIT optimization that the [JVM]({{ "/en/glossary/jvm/" | relative_url }}) performs automatically.
- [Extension functions]({{ "/en/glossary/extension-functions/" | relative_url }}) do **not** use virtual dispatch — they use [static dispatch]({{ "/en/glossary/static-dispatch/" | relative_url }}). This is the most important behavioral difference and a common interview trap: `fun Animal.greet()` vs `fun Dog.greet()` always resolves to the *declared* type, not the runtime type.
- The cost of virtual dispatch is one pointer indirection (the [vtable]({{ "/en/glossary/vtable/" | relative_url }}) lookup). In practice, the JIT compiler's inline caches make this nearly free for monomorphic call sites (only one concrete type ever observed). Performance only becomes a concern for megamorphic sites (many different types) in tight loops.
- Interface dispatch is slightly more expensive than class dispatch because the [JVM]({{ "/en/glossary/jvm/" | relative_url }}) uses an itable (interface method table) lookup that involves a search, whereas class vtable lookups are a direct index.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
