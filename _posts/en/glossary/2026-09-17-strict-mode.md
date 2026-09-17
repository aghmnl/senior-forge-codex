---
layout: post
title: "StrictMode"
date: 2026-09-17 12:00:00 +0000
categories: [en, glossary]
tags: [android-framework, threading, performance]
lang: en
permalink: /en/glossary/strict-mode/
---

## The Theory (The What)

**`StrictMode`** is a developer tool in the Android framework that detects accidental disk and network access on the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) (thread policy) and leaked objects such as unclosed `Cursor`s or `Activity` instances (VM policy). You enable it in [`Application.onCreate()`]({{ "/en/glossary/application-on-create/" | relative_url }}) for debug builds and choose a penalty: log, flash the screen, show a dialog, or crash (`penaltyDeath()`). It is the cheapest way to make a non-main-safe call *loud* long before it becomes an [ANR]({{ "/en/glossary/anr/" | relative_url }}) in production.

```kotlin
// Not found in FAS — standalone example
if (BuildConfig.DEBUG) {
    StrictMode.setThreadPolicy(
        StrictMode.ThreadPolicy.Builder()
            .detectDiskReads().detectDiskWrites().detectNetwork()
            .penaltyLog().penaltyFlashScreen()
            .build()
    )
}
```

## The Senior Nuance

- **It catches the `suspend fun` that never suspends.** `File(path).readText()` inside a coroutine on Main is invisible to the compiler and to a `TestDispatcher`; `StrictMode` flags it the first time it runs on a device.
- **Debug builds only.** The checks cost a few percent of throughput and the penalties are for developers, not users.
- **Expect noise from libraries.** Some framework and SDK code does small disk reads on Main by design; `permitDiskReads()` around a known-benign call keeps the signal useful.
- See [Main-Safety]({{ "/en/02-coroutines-flow/main-safety/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
