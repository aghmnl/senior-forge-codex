---
layout: post
title: "MutableList"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/mutable-list/
---

## The Theory (The What)

**`MutableList<E>`** extends [`List`]({{ "/en/glossary/list/" | relative_url }}) with the structural operations: [`add`]({{ "/en/glossary/add/" | relative_url }}), `add(index, element)`, [`remove`]({{ "/en/glossary/remove/" | relative_url }}), `removeAt`, `set`/`[]=` and [`clear`]({{ "/en/glossary/clear/" | relative_url }}). `mutableListOf()` and [`toMutableList`]({{ "/en/glossary/to-mutable-list/" | relative_url }}) return one, backed by an [`ArrayList`]({{ "/en/glossary/arraylist/" | relative_url }}).

```kotlin
// From FollowApp Suite — StringListTypeConverter.kt
val list = mutableListOf<String>()
for (i in 0 until jsonArray.length()) {
    list.add(jsonArray.getString(i))
}
return list          // published as List<String>
```

## The Senior Nuance

- The rule that survives review: build with a `MutableList` inside a function, declare the [return type]({{ "/en/glossary/return-type/" | relative_url }}) as [`List`]({{ "/en/glossary/list/" | relative_url }}). The [mutation]({{ "/en/glossary/mutation/" | relative_url }}) is confined to one [stack frame]({{ "/en/glossary/stack-frame/" | relative_url }}) that no other thread can observe.
- It is [invariant]({{ "/en/glossary/invariance/" | relative_url }}) — `MutableList<Task>` is not a `MutableList<Any>` — because `E` appears in both read and write positions. See [Generics, Variance & Reification]({{ "/en/01-kotlin-core/generics-variance-reification/" | relative_url }}).
- A `MutableList` stored as shared state is a [concurrency]({{ "/en/glossary/concurrency/" | relative_url }}) bug waiting to happen: it is not [thread-safe]({{ "/en/glossary/thread-safety/" | relative_url }}), and structural modification during iteration throws `ConcurrentModificationException`. If it must escape, take a [defensive copy]({{ "/en/glossary/defensive-copy/" | relative_url }}).
- In Compose it is also invisible: a plain `MutableList` is not [observable]({{ "/en/glossary/observable-state/" | relative_url }}), so mutating it recomposes nothing. The observable equivalent is [`mutableStateListOf`]({{ "/en/glossary/mutable-state-list-of/" | relative_url }}).

**Kotlin docs:** [`kotlin.collections.MutableList`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/-mutable-list/)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
