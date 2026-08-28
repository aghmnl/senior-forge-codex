---
layout: post
title: "Data Transformation"
date: 2026-08-21 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/data-transformation/
---

## The Theory (The What)

A **data transformation** is any operation that takes a value of one type or shape and produces a value of a different type or shape. In Kotlin, transformations are everywhere: `map` converts a `List<A>` to `List<B>`, `let` transforms a nullable value into a result, and mapper functions convert between data layers (`Entity → Domain → UI Model`).

The key property of a transformation is that it produces a **new value** rather than modifying the original in place. This aligns with Kotlin's preference for immutability and functional style.

## The Senior Nuance

- In Android architecture, the **Mapper pattern** is a transformation pipeline: `NetworkResponse → Entity → DomainModel → UiState`. Each layer has its own model, and transformations happen at the boundaries. This keeps layers decoupled.
- [Scope functions]({{ "/en/01-kotlin-core/scope-functions/" | relative_url }}) encode the transformation distinction in their return type: `let` and `run` return the lambda result (transformation), while `apply` and `also` return the context object (configuration/side effect). Mixing them up is a common bug — using `apply` when you meant to transform means the transformed value is silently discarded.
- Kotlin's collection operators (`map`, `filter`, `flatMap`, `groupBy`) are all transformations. Understanding that they create new collections (not modify the original) is fundamental to reasoning about performance and thread safety.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
