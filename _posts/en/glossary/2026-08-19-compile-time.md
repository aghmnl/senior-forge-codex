---
layout: post
title: "Compile Time"
date: 2026-08-19 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/compile-time/
---

## The Theory (The What)

**Compile time** is the phase when [source code]({{ "/en/glossary/source-code/" | relative_url }}) is translated into [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) (on the [JVM]({{ "/en/glossary/jvm/" | relative_url }})) or machine code (in native compilation). During this phase, the compiler performs type checking, [type inference]({{ "/en/glossary/type-inference/" | relative_url }}), [overload resolution]({{ "/en/glossary/overload-resolution/" | relative_url }}), generic type erasure, [annotation processing]({{ "/en/glossary/annotation-processing/" | relative_url }}) (kapt/KSP), and optimization. Errors caught at compile time — type mismatches, unresolved references, exhaustiveness violations in `when` — are the cheapest errors to fix because they prevent the code from ever running incorrectly.

## The Senior Nuance

- Kotlin's design philosophy pushes as many checks as possible to compile time: null safety, sealed `when` exhaustiveness, smart casts, and [`reified`]({{ "/en/glossary/reified/" | relative_url }}) type parameters are all compile-time mechanisms that eliminate entire categories of [runtime]({{ "/en/glossary/runtime/" | relative_url }}) errors.
- **[Extension functions]({{ "/en/glossary/extension-functions/" | relative_url }})** are resolved at compile time based on the declared type of the receiver, not its runtime type. This is a key distinction from virtual method dispatch (which happens at runtime).
- **[Annotation processing]({{ "/en/glossary/annotation-processing/" | relative_url }})** (kapt, KSP) runs at compile time to generate code — Dagger/Hilt [dependency graphs]({{ "/en/glossary/dependency-graph/" | relative_url }}), Room DAO implementations, and Moshi adapters are all compile-time generated.
- **Compile-time constants** (`const val`) are inlined directly into the [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}), avoiding any runtime lookup. Only [primitives]({{ "/en/glossary/primitives/" | relative_url }}) and `String` qualify.
- Understanding the compile-time vs. runtime boundary helps explain why generics are erased (the [JVM]({{ "/en/glossary/jvm/" | relative_url }}) doesn't retain type parameters at runtime) and why [`reified`]({{ "/en/glossary/reified/" | relative_url }}) only works with [`inline` functions]({{ "/en/glossary/inline-functions/" | relative_url }}) (the compiler substitutes the actual type at each call site).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
