---
layout: post
title: "Atomicity"
date: 2026-09-09 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/atomicity/
---

## The Theory (The What)

An operation is **atomic** when it is indivisible from the point of view of every other thread: it either happened completely or not at all, and no observer can see an intermediate state. Reading a value, deciding something from it, and writing a new value is *three* operations — atomic individually, not atomic together.

```kotlin
// NOT atomic: read, compute, write — another thread can interleave between them
_uiState.value = _uiState.value.copy(count = _uiState.value.count + 1)

// Atomic: the whole read-modify-write is one indivisible step
_uiState.update { it.copy(count = it.count + 1) }
```

## The Senior Nuance

- `MutableStateFlow.value` is `@Volatile`-backed, so an individual get or set is atomic and visible across threads. That is exactly why the compound `value = value.copy(...)` reads *safe* and is not: each half is atomic, the pair is a [race condition]({{ "/en/glossary/race-condition/" | relative_url }}).
- Atomicity is achieved without locks through [compare-and-set]({{ "/en/glossary/compare-and-set/" | relative_url }}): read the current value, compute the next, publish it only if the current value has not changed; retry otherwise. This is what [`update`]({{ "/en/glossary/update/" | relative_url }}) does under the hood.
- Atomicity only composes with [immutability]({{ "/en/glossary/immutability/" | relative_url }}). CAS compares *references*; if the state object can be mutated in place, the reference stays the same while the contents change, and the compare succeeds on a value that is no longer what was read. Immutable state is the precondition, not a stylistic preference.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
