---
layout: post
title: "runBlocking"
date: 2026-09-10 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, threading, testing]
lang: en
permalink: /en/glossary/run-blocking/
---

## The Theory (The What)

**`runBlocking { }`** is a coroutine builder that starts a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) and **blocks the current [thread]({{ "/en/glossary/thread/" | relative_url }})** until it completes. It is the bridge between the non-coroutine world (`main()`, JUnit, `Application.onCreate`) and [suspend functions]({{ "/en/glossary/suspend-functions/" | relative_url }}) — the one builder that turns suspending code back into a [blocking call]({{ "/en/glossary/blocking-call/" | relative_url }}).

```kotlin
// From FollowApp Suite — MyTasksApplication.kt
val (language, themeMode, contrastLevel) = runBlocking {
    Triple(
        languagePreferences.getLanguage().first(),
        themePreferences.getThemeMode().first(),
        themePreferences.getContrastLevel().first()
    )
}
```

FAS uses it exactly here, with a comment: the locale and night mode must be known before the first Activity inflates, so the read must complete synchronously.

## The Senior Nuance

- **Never in a ViewModel, Composable, or repository.** Those already have a scope; `runBlocking` there is a [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) block dressed as a coroutine. Use `launch`/`withContext` instead.
- **`runBlocking` on Main can deadlock.** If the block awaits something that needs `Dispatchers.Main` to run, both wait forever. `Dispatchers.Main.immediate` does not save you.
- **Every production use gets a comment and a reason.** The acceptable reasons are short: a value required before the first frame; a legacy synchronous API you cannot change; a CLI entry point.
- **In tests, prefer `runTest`.** It skips `delay`s virtually and fails on leaked coroutines; `runBlocking` does neither.
- See [Suspend Functions]({{ "/en/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
