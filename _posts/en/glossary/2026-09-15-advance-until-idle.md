---
layout: post
title: "advanceUntilIdle"
date: 2026-09-15 12:00:00 +0000
categories: [en, glossary]
tags: [testing, coroutines]
lang: en
permalink: /en/glossary/advance-until-idle/
---

## The Theory (The What)

**`advanceUntilIdle()`** is the [`runTest`]({{ "/en/glossary/run-test/" | relative_url }}) / `TestScope` call that runs the virtual-time scheduler until no coroutine on the [`TestDispatcher`]({{ "/en/glossary/test-dispatcher/" | relative_url }}) has pending work. It fast-forwards every `delay`, drains every queued task, and returns — so the assertion after it sees the state that "eventually" would have appeared.

```kotlin
// From FollowApp Suite — SettingsViewModelTest.kt
@Test
fun `init loads language from use case`() = runTest {
    languageFlow.value = "es"
    val vm = createViewModel()
    advanceUntilIdle()

    assertEquals("es", vm.uiState.value.currentLanguage)
}
```

## The Senior Nuance

- **It only drains what the test dispatcher owns.** A coroutine on real `Dispatchers.IO` or on `GlobalScope` is invisible to it: the test either races or hangs. That is the symptom of an unstructured scope.
- **`StandardTestDispatcher` needs it; `UnconfinedTestDispatcher` mostly does not.** With the standard dispatcher nothing runs until you advance; with unconfined, coroutines run eagerly up to their first suspension.
- **It is the test-side view of "the parent waits for its children".** `runTest` itself fails if a child is still active when the block ends; `advanceUntilIdle` is how you get there deterministically.
- See [Structured Concurrency]({{ "/en/02-coroutines-flow/structured-concurrency/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
