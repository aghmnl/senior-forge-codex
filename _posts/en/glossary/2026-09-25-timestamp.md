---
layout: post
title: "Timestamp"
date: 2026-09-25 12:00:00 +0000
categories: [en, glossary]
tags: [jvm, state-management]
lang: en
permalink: /en/glossary/timestamp/
---

## The Theory (The What)

A **timestamp** is a number that identifies a moment in time. On the [JVM]({{ "/en/glossary/jvm/" | relative_url }}) and Android the most common one is `System.currentTimeMillis()`: milliseconds since the Unix epoch (1970-01-01 UTC), according to the device's **wall clock**. Android also offers monotonic clocks that only move forward — `SystemClock.elapsedRealtime()` and `System.nanoTime()` — which measure elapsed time but do not correspond to a calendar date.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// A timestamp used as a "fire again" trigger: each form open writes
// a new value, so the StateFlow does not drop it as equal to the last one
_formOpenTrigger.value = System.currentTimeMillis()
```

## The Senior Nuance

- **The wall clock can jump.** The user can change the time, and network time sync can move it backwards. Measuring a duration as the difference of two `currentTimeMillis()` values can give negative or absurd results; durations belong to `elapsedRealtime()` or `nanoTime()`.
- **As a trigger, a timestamp is only "probably distinct".** Two writes in the same millisecond produce the same value, and a [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}) drops the second one. A counter that increments is guaranteed to be distinct.
- **Injecting "now" makes code testable.** Code that calls `System.currentTimeMillis()` deep inside is hard to test; passing `now` as a parameter, or injecting a clock, makes time controllable.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
