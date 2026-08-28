---
layout: post
title: "Context (Programming)"
date: 2026-08-21 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/context-programming/
---

## The Theory (The What)

In programming, a **context** is the surrounding state, environment, or object that provides meaning and resources to a piece of code. The term is overloaded across different levels:

- **Language level**: In Kotlin's [scope functions]({{ "/en/01-kotlin-core/scope-functions/" | relative_url }}), the "context object" is the object the function operates on — available as `this` or `it` inside the lambda.
- **Android level**: `android.content.Context` is the system's gateway to application resources, services, databases, and the operating system. Every Activity, Service, and Application is a Context.
- **Coroutine level**: `CoroutineContext` is a set of elements (dispatcher, job, exception handler) that define how and where a coroutine executes.

## The Senior Nuance

- **Android Context hierarchy**: `Application` context lives for the entire app lifetime; `Activity` context is tied to a screen. Using an Activity context in a long-lived singleton causes memory leaks. Using Application context for UI operations (like inflating a themed view) gives wrong results because it lacks the Activity's theme.
- In scope functions, the "context object" concept is unrelated to Android's `Context` class — a frequent source of confusion for developers new to Kotlin on Android.
- **Coroutine context** is additive: contexts can be combined with `+` (`Dispatchers.IO + SupervisorJob()`). Understanding this composition is essential for structured concurrency.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
