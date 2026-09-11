---
layout: post
title: "Data Transformation"
date: 2026-08-21 12:00:00 +0000
categories: [en, glossary]
tags: [functional, architecture, collections]
lang: en
permalink: /en/glossary/data-transformation/
---

## The Theory (The What)

A **data transformation** is any operation that takes a value of one type or shape and produces a value of a different type or shape. In Kotlin, transformations are everywhere: `map` converts a `List<A>` to `List<B>`, `let` transforms a nullable value into a result, and [mapper functions]({{ "/en/glossary/mapper-function/" | relative_url }}) convert between [data layers]({{ "/en/glossary/data-layer/" | relative_url }}) (`Entity → Domain → UI Model`).

The key property of a transformation is that it produces a **new value** rather than modifying the original in place. This aligns with Kotlin's preference for [immutability]({{ "/en/glossary/immutability/" | relative_url }}) and [functional style]({{ "/en/glossary/functional-style/" | relative_url }}).

## The Senior Nuance

- In Android architecture, the **[Mapper pattern]({{ "/en/glossary/mapper-pattern/" | relative_url }})** is a transformation [pipeline]({{ "/en/glossary/pipeline/" | relative_url }}): `NetworkResponse → Entity → DomainModel → UiState`. Each [data layer]({{ "/en/glossary/data-layer/" | relative_url }}) has its own model, and transformations happen at the boundaries. This keeps [data layers]({{ "/en/glossary/data-layer/" | relative_url }}) decoupled.
- [Scope functions]({{ "/en/01-kotlin-core/scope-functions/" | relative_url }}) encode the transformation distinction in their return type: `let` and `run` return the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) result (transformation), while `apply` and `also` return the context object (configuration/side effect). Mixing them up is a common bug — using `apply` when you meant to transform means the transformed value is silently discarded.
- Kotlin's [collection operators]({{ "/en/glossary/collection-operators/" | relative_url }}) (`map`, `filter`, `flatMap`, `groupBy`) are all transformations. Understanding that they create new [collections]({{ "/en/glossary/collections/" | relative_url }}) (not modify the original) is fundamental to reasoning about performance and [thread safety]({{ "/en/glossary/thread-safety/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
