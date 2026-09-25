---
layout: post
title: "collectAsStateWithLifecycle"
date: 2026-09-25 12:00:00 +0000
categories: [en, glossary]
tags: [compose, lifecycle, flow]
lang: en
permalink: /en/glossary/collect-as-state-with-lifecycle/
---

## The Theory (The What)

**`collectAsStateWithLifecycle()`** is a [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) extension (from `androidx.lifecycle:lifecycle-runtime-compose`) that collects a [Flow]({{ "/en/glossary/flow/" | relative_url }}) into a Compose `State` **only while the [lifecycle]({{ "/en/glossary/lifecycle/" | relative_url }}) is at least `STARTED`**. Below that state (the app in the background, the screen covered) it cancels the collection; when the lifecycle comes back it starts collecting again. On a [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}) the first value comes from `.value`, so the UI has something to draw immediately. Internally it runs the collection inside [repeatOnLifecycle]({{ "/en/glossary/repeat-on-lifecycle/" | relative_url }}).

```kotlin
// From FollowApp Suite — TasksScreen.kt
// Every screen-level StateFlow is collected with lifecycle awareness
val uiState by viewModel.uiState.collectAsStateWithLifecycle()
val settingsState by settingsViewModel.uiState.collectAsStateWithLifecycle()
val isTemplatePickerVisible by viewModel.isTemplatePickerVisible.collectAsStateWithLifecycle()
```

## The Senior Nuance

- **It is the default for collecting in Compose.** `collectAsState()` collects for as long as the composable is in the composition, and the composition stays alive while the app is in the background. `collectAsStateWithLifecycle()` is the [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) version and should be the reflex choice.
- **The saving is not in the collector; it is in the [upstream]({{ "/en/glossary/upstream/" | relative_url }}).** For a plain `MutableStateFlow` the difference is small. For a `StateFlow` built with [stateIn]({{ "/en/glossary/state-in/" | relative_url }}) and [WhileSubscribed]({{ "/en/glossary/while-subscribed/" | relative_url }}), stopping the collector is the only thing that lets the upstream (a query, location updates, a socket) stop too.
- **`minActiveState` is configurable.** `STARTED` is the default; `RESUMED` is useful for work that should pause when a dialog or another window partially covers the screen.
- For a cold [Flow]({{ "/en/glossary/flow/" | relative_url }}) it needs an explicit `initialValue`, because there is no `.value` to read before the first emission.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
