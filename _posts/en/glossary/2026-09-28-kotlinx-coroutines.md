---
layout: post
title: "kotlinx.coroutines"
date: 2026-09-28 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, build-tools, concurrency]
lang: en
permalink: /en/glossary/kotlinx-coroutines/
---

## The Theory (The What)

**kotlinx.coroutines** is the official JetBrains **library** that turns the language's [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}) into something usable. [Kotlin]({{ "/en/glossary/kotlin/" | relative_url }}) itself only provides the `suspend` keyword and the basic types behind it, in its [`kotlin.coroutines`]({{ "/en/glossary/coroutines/" | relative_url }}) package. Everything else comes from this separate dependency: [CoroutineScope]({{ "/en/glossary/coroutine-scope/" | relative_url }}), [launch]({{ "/en/glossary/launch/" | relative_url }}), [async]({{ "/en/glossary/async/" | relative_url }}), [Job]({{ "/en/glossary/job/" | relative_url }}), [SupervisorJob]({{ "/en/glossary/supervisor-job/" | relative_url }}), [dispatchers]({{ "/en/glossary/dispatcher/" | relative_url }}), [withContext]({{ "/en/glossary/with-context/" | relative_url }}), [Flow]({{ "/en/glossary/flow/" | relative_url }}), [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}), [SharedFlow]({{ "/en/glossary/sharedflow/" | relative_url }}) and [Channel]({{ "/en/glossary/channel/" | relative_url }}). The `x` in `kotlinx` marks official libraries that are not part of the standard library, like `kotlinx.serialization` or `kotlinx.datetime`.

```kotlin
// From FollowApp Suite — libs.versions.toml
// A pure-Kotlin module does not get the library for free: it declares it
# Flow in :core:domain repository contracts; the module has no Android dependency to inherit it from
kotlinx-coroutines-core = { module = "org.jetbrains.kotlinx:kotlinx-coroutines-core", version = "1.8.1" }

// From FollowApp Suite — TasksViewModel.kt
// Every one of these imports is the library, not the language
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
```

## The Senior Nuance

- **Language vs library is a real interview question.** "Are coroutines part of Kotlin?" The honest answer has two halves: suspension is a language feature, implemented by the compiler; scopes, dispatchers, cancellation and streams are a library. That is why the library has its own version number, separate from the Kotlin version.
- **It is split into modules.** `kotlinx-coroutines-core` has the platform-independent API; `kotlinx-coroutines-android` provides `Dispatchers.Main` on top of the Android main looper; `kotlinx-coroutines-test` provides `runTest` and test dispatchers. Without the Android module, touching `Dispatchers.Main` fails at runtime because no main dispatcher is available.
- **Android modules usually get it transitively.** Jetpack libraries such as `lifecycle-viewmodel-ktx` depend on it, which is where `viewModelScope` and `lifecycleScope` come from. A pure-Kotlin domain module has no such dependency and must declare `kotlinx-coroutines-core` explicitly.
- **Library APIs evolve; language semantics do not.** Operators like [flatMapLatest]({{ "/en/glossary/flat-map-latest/" | relative_url }}) are marked experimental in the library and can change between versions, while `suspend` itself is stable. Reading the library's changelog is part of upgrading a codebase.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
