---
layout: post
title: "TestScope"
date: 2026-09-28 12:00:00 +0000
categories: [en, glossary]
tags: [testing, coroutines]
lang: en
permalink: /en/glossary/test-scope/
---

## The Theory (The What)

**`TestScope`** is the [CoroutineScope]({{ "/en/glossary/coroutine-scope/" | relative_url }}) that `kotlinx-coroutines-test` provides for tests. [runTest]({{ "/en/glossary/run-test/" | relative_url }}) creates one and runs the test body with it as the receiver. Its [test dispatcher]({{ "/en/glossary/test-dispatcher/" | relative_url }}) is driven by a virtual clock: `delay` does not wait in real time, it advances virtual time, so a test covering a five-minute timeout finishes in milliseconds. It also collects uncaught exceptions from its [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}) and fails the test with them.

```kotlin
// From FollowApp Suite — AuthUseCaseTest.kt
// The body of runTest runs inside a TestScope: suspend calls and
// first() work directly, with no runBlocking and no real waiting
@Test
fun `signing out clears the session`() = runTest {
    saveSession(session)
    signOut()
    assertNull(getSession().first())
}
```

## The Senior Nuance

- **Virtual time is explicit.** With the default `StandardTestDispatcher`, launched coroutines do not run until the test lets them: [advanceUntilIdle()]({{ "/en/glossary/advance-until-idle/" | relative_url }}) runs everything pending, `advanceTimeBy(ms)` moves the clock, `runCurrent()` runs what is due now, and `currentTime` reads the clock.
- **`backgroundScope` for endless work.** A coroutine collecting a [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}) never finishes, and `runTest` fails when work is still running at the end. Launching such collectors in `backgroundScope` cancels them automatically when the test ends.
- **Share the scheduler.** Code under test that creates its own dispatcher must use the same `TestCoroutineScheduler`; otherwise virtual time does not reach it and `delay` really waits. Replacing `Dispatchers.Main` with [Dispatchers.setMain]({{ "/en/glossary/set-main/" | relative_url }}) and injecting dispatchers are how that sharing happens.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
