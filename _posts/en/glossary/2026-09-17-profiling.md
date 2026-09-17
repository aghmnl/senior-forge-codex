---
layout: post
title: "Profiling"
date: 2026-09-17 12:00:00 +0000
categories: [en, glossary]
tags: [performance, threading]
lang: en
permalink: /en/glossary/profiling/
---

## The Theory (The What)

**Profiling** is measuring where a program actually spends time, memory or energy, instead of reasoning about it from the source. On Android the tools are the Android Studio Profiler (CPU, memory, energy), **Perfetto** / system traces for frame-level timelines, `Trace.beginSection()` / `trace()` for custom markers, and Macrobenchmark for repeatable startup and scroll measurements. For main-safety the question profiling answers is precise: *which call, on which thread, held the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) for how many milliseconds?*

```kotlin
// From FollowApp Suite — ConsentManager.kt
// MobileAds.initialize does ~700 ms of synchronous SDK bootstrap on
// the caller thread even though it exposes an async callback.
```

## The Senior Nuance

- **Signatures lie; traces do not.** The 700 ms above was found by measuring, not by reading `initialize(context, listener)`. Any [SDK]({{ "/en/glossary/sdk/" | relative_url }}) or framework call you have not profiled is a main-safety assumption.
- **Profile release-like builds on a slow device.** Debug builds disable optimisations and a flagship hides [jank]({{ "/en/glossary/jank/" | relative_url }}) that a mid-range phone shows every time.
- **Keep the numbers next to the code.** A comment with the measured cost turns "why is this on IO?" from archaeology into a one-line answer.
- See [Main-Safety]({{ "/en/02-coroutines-flow/main-safety/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
