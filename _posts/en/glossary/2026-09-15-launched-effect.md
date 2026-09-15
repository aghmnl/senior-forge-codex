---
layout: post
title: "LaunchedEffect"
date: 2026-09-15 12:00:00 +0000
categories: [en, glossary]
tags: [compose, coroutines, lifecycle]
lang: en
permalink: /en/glossary/launched-effect/
---

## The Theory (The What)

**`LaunchedEffect(key) { }`** is the [composable]({{ "/en/glossary/composable/" | relative_url }}) that launches a coroutine tied to the [composition]({{ "/en/glossary/composition-lifetime/" | relative_url }}): the block starts when the effect enters the composition, is **cancelled when it leaves**, and is cancelled-and-restarted whenever any `key` changes. It is structured concurrency applied to UI — the composition is the parent, and the coroutine cannot outlive it.

```kotlin
// From FollowApp Suite — TasksScreen.kt
LaunchedEffect(toastMessage) {
    if (toastMessage == null) return@LaunchedEffect
    Toast.makeText(context, toastMessage, Toast.LENGTH_SHORT).show()
    onToastShown()
}
```

## The Senior Nuance

- **The keys are the restart policy.** `LaunchedEffect(Unit)` runs once per composition; `LaunchedEffect(state.value)` restarts on every change. Choosing the wrong key either misses updates or cancels work mid-flight.
- **Cancellation is a [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) at the next [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}).** A `while` loop inside must suspend (`withFrameNanos`, `delay`) or check [`isActive`]({{ "/en/glossary/is-active/" | relative_url }}) to be [cooperative]({{ "/en/glossary/cooperative-cancellation/" | relative_url }}).
- **For event handlers, use `rememberCoroutineScope()` instead.** `LaunchedEffect` is for work that should run *because* a state is a certain way; a scope is for work that starts *because* the user did something.
- See [Structured Concurrency]({{ "/en/02-coroutines-flow/structured-concurrency/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
