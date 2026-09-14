---
layout: post
title: "TestDispatcher"
date: 2026-09-14 12:00:00 +0000
categories: [en, glossary]
tags: [testing, coroutines, threading]
lang: en
permalink: /en/glossary/test-dispatcher/
---

## The Theory (The What)

A **`TestDispatcher`** (`StandardTestDispatcher`, `UnconfinedTestDispatcher`) is a [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) from `kotlinx-coroutines-test` that runs coroutines on the test thread under a virtual-time scheduler: `delay` completes instantly, execution order is deterministic, and `runTest` fails if a coroutine is still running at the end. It replaces real [thread pools]({{ "/en/glossary/thread-pool/" | relative_url }}) in unit tests.

```kotlin
// From FollowApp Suite — SettingsViewModelTest.kt
@Before
fun setup() {
    Dispatchers.setMain(testDispatcher)
}

@After
fun tearDown() {
    Dispatchers.resetMain()
}
```

`Dispatchers.setMain` swaps the global `Main` for the test dispatcher, which is what makes [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) controllable in a JVM test. It does nothing for `Dispatchers.IO` or `Default`.

## The Senior Nuance

- **Inject dispatchers, or the test cannot reach them.** A hard-coded `withContext(Dispatchers.IO)` inside a class under test hops to a real thread that `runTest` does not control; the test either races or sleeps. Constructor-inject a `CoroutineDispatcher` and pass `StandardTestDispatcher(testScheduler)` in tests — FAS does not do this yet, which is why its `BackupManager` is only testable through instrumented tests.
- **`Standard` vs `Unconfined`.** `StandardTestDispatcher` queues work until the test calls `advanceUntilIdle()` / `runCurrent()`, giving explicit control over ordering. `UnconfinedTestDispatcher` runs eagerly, which reads more like production `Main.immediate` but hides ordering bugs.
- **`setMain` is process-global.** Always pair it with `resetMain()` in `@After`, or the next test class inherits the dispatcher.
- **Prefer `runTest` over [`runBlocking`]({{ "/en/glossary/run-blocking/" | relative_url }})** in tests: it provides the scheduler, skips delays, and detects leaked coroutines.
- See [Context & Dispatchers]({{ "/en/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
