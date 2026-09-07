---
layout: post
title: "Collection Operators"
date: 2026-09-04 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/collection-operators/
---

## The Theory (The What)

**Collection operators** are [extension functions]({{ "/en/glossary/extension-functions/" | relative_url }}) on Kotlin's [collections]({{ "/en/glossary/collections/" | relative_url }}) (`List`, `Set`, `Map`, `Sequence`) that express [data transformations]({{ "/en/glossary/data-transformation/" | relative_url }}) declaratively. The most common operators are:

- **`map`** — transforms each element: `List<A> → List<B>`.
- **`filter`** — keeps elements that match a predicate.
- **`flatMap`** — maps each element to a collection and flattens the results.
- **`groupBy`** — partitions elements into a `Map<K, List<V>>` by a key selector.
- **`fold` / `reduce`** — accumulates elements into a single value.
- **`associate` / `associateBy`** — builds a `Map` from elements.
- **`sortedBy` / `sortedWith`** — produces a sorted copy.
- **`distinct` / `distinctBy`** — removes duplicates.

All these operators return **new** collections — they do not mutate the original. This aligns with Kotlin's preference for [immutability]({{ "/en/glossary/immutability/" | relative_url }}) and [functional style]({{ "/en/glossary/functional-style/" | relative_url }}).

## The Senior Nuance

- A Senior chains operators into [pipelines]({{ "/en/glossary/pipeline/" | relative_url }}) that read as a specification: `tasks.filter { !it.isDone }.sortedBy { it.dueDate }.map { it.toUiModel() }`. Each step is a pure transformation, trivially testable in isolation.
- Eager operators (`list.map { }`) create a new `List` at every step. For large collections or long chains, `asSequence()` avoids intermediate allocations by evaluating lazily. But sequences have [overhead]({{ "/en/glossary/overhead/" | relative_url }}) per element, so for small collections (<100 elements), eager is faster.
- Flow operators (`map`, `filter`, `flatMapLatest`) mirror collection operators but operate on asynchronous streams. A Senior recognizes the conceptual symmetry: the same [functional style]({{ "/en/glossary/functional-style/" | relative_url }}) applies whether data arrives all at once (collections) or over time (Flow).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
