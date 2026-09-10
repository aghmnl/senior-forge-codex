---
layout: post
title: "Value Semantics"
date: 2026-09-09 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/value-semantics/
---

## The Theory (The What)

A type has **value semantics** when its identity is its contents: two instances with the same data are interchangeable, and passing one around cannot let anyone change yours. A [`data class`]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}) of immutable properties has value semantics; a class with `var` fields has *reference* semantics — what you hold is a handle to something that can change under you.

```kotlin
// From FollowApp Suite — TasksUiState.kt
data class TasksUiState(
    val isLoading: Boolean = true,
    val activeTasks: List<Task> = emptyList(),
    val selectedTaskIds: Set<String> = emptySet(),
    // ... every property a val, every type read-only
)
```

## The Senior Nuance

- Value semantics is what makes a state object safe to hand to a composable, a coroutine, and a test at the same time. Nobody can corrupt anybody else's copy because there is nothing to corrupt — [thread safety]({{ "/en/glossary/thread-safety/" | relative_url }}) by construction rather than by locking.
- It is also what makes `==` *mean* something. [Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) skipping, [`distinctUntilChanged`]({{ "/en/glossary/distinct-until-changed/" | relative_url }}), [`StateFlow`]({{ "/en/glossary/stateflow/" | relative_url }}) [conflation]({{ "/en/glossary/conflation/" | relative_url }}) and test assertions all ask "is this the same state?" and get a truthful answer only from a value type.
- `val` on the property is half the job; the property's *type* must also be read-only all the way down. `val tasks: MutableList<Task>` is a `val` with reference semantics, and it defeats [`equals`]({{ "/en/glossary/equals/" | relative_url }}), [`copy`]({{ "/en/glossary/copy/" | relative_url }}) and [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}) in one line.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
