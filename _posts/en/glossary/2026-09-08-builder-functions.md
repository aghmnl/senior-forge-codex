---
layout: post
title: "Builder Functions"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/builder-functions/
---

## The Theory (The What)

**Builder functions** — `buildList {}`, `buildSet {}`, `buildMap {}`, `buildString {}` — are [standard library]({{ "/en/glossary/standard-library/" | relative_url }}) [inline functions]({{ "/en/glossary/inline-functions/" | relative_url }}) that give you a mutable receiver inside a [lambda with receiver]({{ "/en/glossary/lambda-with-receiver/" | relative_url }}) and return the read-only supertype.

```kotlin
// From FollowApp Suite — LabelsListScreen.kt
val actions = buildList {
    add(ToolbarAction(icon = UiIcons.Delete, /* ... */))
    if (allTags) {
        add(ToolbarAction(icon = UiIcons.ConvertToScale, /* ... */))
    }
}
```

## The Senior Nuance

- They encode the "mutate locally, publish [immutably]({{ "/en/glossary/immutability/" | relative_url }})" rule in the type system: the `MutableList` receiver exists only inside the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}), so it cannot escape as a [read-only view]({{ "/en/glossary/read-only-view/" | relative_url }}) over live state. After the builder returns, the collection is frozen — writing to a captured reference throws `UnsupportedOperationException`.
- They are the right answer when construction is conditional. A chain of `listOfNotNull` plus `takeIf` reads worse than three `add` calls guarded by `if`, and allocates more.
- `buildList(capacity)` pre-sizes the backing array, which matters in [hot loops]({{ "/en/glossary/hot-loops/" | relative_url }}) where repeated growth would copy. Because they are [`inline`]({{ "/en/glossary/inline-functions/" | relative_url }}), there is no [overhead]({{ "/en/glossary/overhead/" | relative_url }}) from the lambda itself.

**Kotlin docs:** [`buildList`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/build-list.html) · [`buildMap`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/build-map.html)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
