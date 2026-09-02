---
layout: post
title: "Polymorphism"
date: 2026-08-19 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/polymorphism/
---

## The Theory (The What)

**Polymorphism** (from Greek: "many forms") is a fundamental principle of object-oriented programming where a single interface or reference type can represent different underlying implementations. In Kotlin and the JVM, polymorphism manifests in three main forms:

- **Subtype (Runtime) Polymorphism**: A parent type reference can point to any subclass instance. Method dispatch happens at runtime via the [virtual dispatch]({{ "/en/glossary/virtual-dispatch/" | relative_url }}) mechanism and the [vtable]({{ "/en/glossary/vtable/" | relative_url }}). This is the most common form — e.g., a `List<Animal>` holding `Dog` and `Cat` instances.
- **Ad-hoc Polymorphism**: [Function overloading]({{ "/en/glossary/function-overloading/" | relative_url }}) — multiple functions with the same name but different parameter signatures. Resolved at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) via [static dispatch]({{ "/en/glossary/static-dispatch/" | relative_url }}).
- **Parametric Polymorphism**: Generics — a single class or function works with any type parameter (`List<T>`). On the JVM, type parameters are erased at runtime ([type erasure]({{ "/en/glossary/type-erasure/" | relative_url }})), except when using Kotlin's `reified` inline functions.

## The Senior Nuance

- In Android, polymorphism is everywhere: `ViewModel`, `Fragment`, `RecyclerView.Adapter` are all designed around subtype polymorphism. Understanding [vtable]({{ "/en/glossary/vtable/" | relative_url }}) dispatch helps explain why [final]({{ "/en/glossary/final/" | relative_url }}) (or Kotlin's default closed classes) can be a performance advantage — the JIT compiler can devirtualize [final]({{ "/en/glossary/final/" | relative_url }}) methods into [static dispatch]({{ "/en/glossary/static-dispatch/" | relative_url }}).
- [Sealed classes]({{ "/en/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}) combine polymorphism with [exhaustiveness]({{ "/en/glossary/exhaustiveness/" | relative_url }}) — the compiler knows all subtypes, so `when` expressions are safe without `else`. Adding a new subtype triggers a [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) error at every unhandled `when`.
- [Extension functions]({{ "/en/glossary/extension-functions/" | relative_url }}) in Kotlin are **not** polymorphic — they are resolved statically at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) based on the declared type, not the runtime type. This is a common interview question that tests whether a candidate truly understands [static dispatch]({{ "/en/glossary/static-dispatch/" | relative_url }}) vs [virtual dispatch]({{ "/en/glossary/virtual-dispatch/" | relative_url }}).
- [Type erasure]({{ "/en/glossary/type-erasure/" | relative_url }}) limits parametric polymorphism at runtime: you cannot check `is List<String>` because the type argument is erased. Kotlin's `reified` + `inline` is the escape hatch.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
