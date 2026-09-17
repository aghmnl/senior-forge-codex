---
layout: post
title: "produceState"
date: 2026-09-17 12:00:00 +0000
categories: [en, glossary]
tags: [compose, coroutines, state-management]
lang: en
permalink: /en/glossary/produce-state/
---

## The Theory (The What)

**`produceState(initialValue) { }`** is the [composable]({{ "/en/glossary/composable/" | relative_url }}) that turns a coroutine into a `State<T>`: it launches the block in a coroutine scoped to the composition (like [`LaunchedEffect`]({{ "/en/glossary/launched-effect/" | relative_url }})), and every assignment to `value` inside it triggers [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}). The coroutine is cancelled when the composable leaves the composition, and restarted when any key changes. It runs on the composition's [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) — Main — so blocking work inside it needs [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}).

```kotlin
// From FollowApp Suite — AboutScreen.kt
val licenses by produceState<List<License>?>(initialValue = null, key1 = context) {
    value = withContext(Dispatchers.IO) { loadLicenses(context) }
}
```

## The Senior Nuance

- **It is `LaunchedEffect` + `remember { mutableStateOf() }` in one call.** Use it when the effect's only job is to produce a value for the UI.
- **The `withContext` is not optional for blocking loaders.** Without it the first frame of the screen waits on disk — that is [jank]({{ "/en/glossary/jank/" | relative_url }}) on entry, and main-safety applies exactly as in a repository.
- **For long-lived streams prefer `collectAsStateWithLifecycle`.** `produceState` is for one-shot or key-driven loads; a [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) that should stop when the app is backgrounded wants the lifecycle-aware collector.
- See [Main-Safety]({{ "/en/02-coroutines-flow/main-safety/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
