---
layout: post
title: "Structural Sharing"
date: 2026-09-09 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/structural-sharing/
---

## The Theory (The What)

**Structural sharing** is the technique that makes immutable data cheap: a "modified" copy reuses every unchanged part of the original instead of duplicating it. Only the nodes on the path to the change are new.

```kotlin
// state and next share activeTasks, availableLabels, form, presets... everything
// except the one property that actually changed. One small allocation, not a deep copy.
val next = state.copy(isDrawerOpen = true)
```

## The Senior Nuance

- This is why "immutable state is too slow" is almost always wrong for UI state. A [`copy`]({{ "/en/glossary/copy/" | relative_url }}) of a thirty-field state class allocates one object holding thirty references — a few hundred bytes — regardless of how large the referenced lists are.
- It is also why immutable state and [`equals`]({{ "/en/glossary/equals/" | relative_url }}) comparison get along. Shared subtrees are reference-identical, so a structural comparison short-circuits on `===` for every branch that did not change. [Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) skips whole subtrees on exactly this signal.
- Kotlin's built-in [collections]({{ "/en/glossary/collections/" | relative_url }}) do **not** share structure: `list + item` copies the entire backing array, so an `O(1)`-looking operation is `O(n)`. Genuine structural sharing inside a collection requires [persistent collections]({{ "/en/glossary/persistent-collections/" | relative_url }}) (`kotlinx.collections.immutable`), whose trie-based `add` reuses all but a handful of nodes.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
