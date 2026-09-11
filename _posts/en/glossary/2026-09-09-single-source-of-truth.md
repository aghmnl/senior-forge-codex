---
layout: post
title: "Single Source of Truth"
date: 2026-09-09 12:00:00 +0000
categories: [en, glossary]
tags: [state-management, architecture, design-principles]
lang: en
permalink: /en/glossary/single-source-of-truth/
---

## The Theory (The What)

**Single source of truth** (SSOT) is the rule that every piece of state has exactly one owner, and everything else derives from it. Duplicated state is not "a copy" — it is a second truth that will eventually disagree with the first.

```kotlin
// From FollowApp Suite — TasksUiState.kt
// Derived, not stored: no isSelectionMode flag to keep in sync with the set
val isSelectionMode: Boolean get() = selectedTaskIds.isNotEmpty()
val selectedTasks: List<Task> get() = activeTasks.filter { it.id in selectedTaskIds }
```

## The Senior Nuance

- The bug SSOT prevents is the *impossible state*: `isSelectionMode = true` with `selectedTaskIds = emptySet()`. If both are stored, some code path will eventually update one and not the other. If one is a computed property, that state cannot be expressed at all.
- Derived properties on the state class run on every read, so they must stay cheap. `selectedTasks` filtering a few hundred tasks per recomposition is fine; a `sortedBy` over ten thousand is not — that belongs upstream in the [ViewModel]({{ "/en/glossary/viewmodel-store/" | relative_url }}), computed once when its inputs change.
- SSOT also decides *where* truth lives, not just how many copies. In FollowApp Suite the database is the truth for tasks, the [ViewModel]({{ "/en/glossary/viewmodel-store/" | relative_url }})'s [`StateFlow`]({{ "/en/glossary/stateflow/" | relative_url }}) is the truth for the screen, and any local [Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) state is explicitly a derived, resynchronised copy — never authoritative.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
