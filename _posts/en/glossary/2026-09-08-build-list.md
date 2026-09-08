---
layout: post
title: "buildList"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/build-list/
---

## The Theory (The What)

**`buildList { }`** is an [inline]({{ "/en/glossary/inline-functions/" | relative_url }}) [builder function]({{ "/en/glossary/builder-functions/" | relative_url }}) that gives you a [`MutableList`]({{ "/en/glossary/mutable-list/" | relative_url }}) as the [lambda's receiver]({{ "/en/glossary/lambda-with-receiver/" | relative_url }}) and returns a read-only [`List`]({{ "/en/glossary/list/" | relative_url }}). It encodes "mutate locally, publish immutably" in a single expression.

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

- Conditional construction is where it wins. The alternative — `listOfNotNull` plus `takeIf`, or a `+` chain that reallocates per step — reads worse and allocates more.
- After the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) returns, the list is frozen: writing through a reference captured inside throws `UnsupportedOperationException`. That is what makes it stronger than a hand-rolled `mutableListOf` returned as `List`, which is only a [read-only view]({{ "/en/glossary/read-only-view/" | relative_url }}).
- `buildList(capacity) { }` pre-sizes the backing [`ArrayList`]({{ "/en/glossary/arraylist/" | relative_url }}). Being [`inline`]({{ "/en/glossary/inline-functions/" | relative_url }}), the builder itself adds no [overhead]({{ "/en/glossary/overhead/" | relative_url }}) — no lambda object is allocated.

**Kotlin docs:** [`kotlin.collections.buildList`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.collections/build-list.html)

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
