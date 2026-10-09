---
layout: post
title: "MutableState"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [compose, state-management]
lang: en
permalink: /en/glossary/mutable-state/
---

## The Theory (The What)

**`MutableState<T>`** is Compose's observable state holder, created with `mutableStateOf(value)`. Reading `.value` during [composition]({{ "/en/glossary/composition/" | relative_url }}) registers that read in the [snapshot system]({{ "/en/glossary/snapshot-system/" | relative_url }}); writing a new value invalidates exactly the scopes that read it, which then recompose. Specialized versions (`mutableIntStateOf`, `mutableFloatStateOf`) avoid boxing [primitives]({{ "/en/glossary/primitives/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
var count by remember { mutableStateOf(0) }
Button(onClick = { count++ }) { Text("Clicked $count times") }
```

## The Senior Nuance

- **Without [`remember`]({{ "/en/glossary/remember/" | relative_url }}), it resets on every [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}).** `mutableStateOf` creates the holder; [`remember`]({{ "/en/glossary/remember/" | relative_url }}) keeps the same holder across recompositions.
- **Changes are detected by assignment.** Mutating an object inside the state (adding to a [`MutableList`]({{ "/en/glossary/mutable-list/" | relative_url }}) stored in it) does not notify anyone; assign a new value or use [`mutableStateListOf`]({{ "/en/glossary/mutable-state-list-of/" | relative_url }}).
- See [Recomposition & Stability]({{ "/en/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
