---
layout: post
title: "Derived State"
date: 2026-09-09 12:00:00 +0000
categories: [en, glossary]
tags: [state-management, data-classes, compose]
lang: en
permalink: /en/glossary/derived-state/
---

## The Theory (The What)

**Derived state** is state that is *computed* from other state rather than stored alongside it. In an immutable state class it takes the form of a property with a getter and no [backing field]({{ "/en/glossary/backing-field/" | relative_url }}) — it cannot go stale, because it is recomputed from the truth on every read.

```kotlin
// From FollowApp Suite — TasksUiState.kt
val isSelectionMode: Boolean get() = selectedTaskIds.isNotEmpty()
val selectedTasks: List<Task> get() = activeTasks.filter { it.id in selectedTaskIds }
```

## The Senior Nuance

- The alternative — storing `isSelectionMode` as a `val` in the constructor — creates a synchronisation obligation at every [`copy`]({{ "/en/glossary/copy/" | relative_url }}) site. Derivation makes the inconsistent combination unrepresentable, which is the strongest form of [Single Source of Truth]({{ "/en/glossary/single-source-of-truth/" | relative_url }}).
- A getter is invisible to [`equals`]({{ "/en/glossary/equals/" | relative_url }}), [`copy`]({{ "/en/glossary/copy/" | relative_url }}) and `toString`, because `data class` only generates those over the *primary constructor* properties. That is a feature here: derived values cannot desynchronise state comparison, so [Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) skipping stays correct.
- The cost is that the getter runs on every read, including every [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}). Cheap predicates belong on the state class; expensive derivations (sorting, grouping, joining large [collections]({{ "/en/glossary/collections/" | relative_url }})) belong upstream in the [ViewModel]({{ "/en/glossary/viewmodel-store/" | relative_url }}) where they are computed once per input change — or in `derivedStateOf` when the source is Compose state.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
