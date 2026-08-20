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

- **Subtype (Runtime) Polymorphism**: A parent type reference can point to any subclass instance. Method dispatch happens at runtime via the virtual method table (vtable). This is the most common form — e.g., a `List<Animal>` holding `Dog` and `Cat` instances.
- **Ad-hoc Polymorphism**: Function overloading — multiple functions with the same name but different parameter signatures. Resolved at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}).
- **Parametric Polymorphism**: Generics — a single class or function works with any type parameter (`List<T>`). On the JVM, type parameters are erased at runtime (type erasure), except when using Kotlin's `reified` inline functions.

## The Senior Nuance

- In Android, polymorphism is everywhere: `ViewModel`, `Fragment`, `RecyclerView.Adapter` are all designed around subtype polymorphism. Understanding vtable dispatch helps explain why `final` (or Kotlin's default closed classes) can be a performance advantage.
- Sealed classes combine polymorphism with exhaustiveness — the compiler knows all subtypes, so `when` expressions are safe without `else`.
- Extension functions in Kotlin are **not** polymorphic — they are resolved statically at compile time based on the declared type, not the runtime type. This is a common interview question.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
