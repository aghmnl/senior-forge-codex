---
layout: post
title: "Continuation-Passing Style (CPS)"
date: 2026-09-10 12:00:00 +0000
categories: [en, glossary]
tags: [coroutines, compiler]
lang: en
permalink: /en/glossary/continuation-passing-style/
---

## The Theory (The What)

**Continuation-Passing Style (CPS)** is the transformation the Kotlin compiler applies to every [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}): instead of *returning* a value, the function receives a [Continuation]({{ "/en/glossary/continuation/" | relative_url }}) parameter and eventually *calls* it with the result. The visible signature `suspend fun load(id: String): Task` becomes `fun load(id: String, cont: Continuation<Task>): Any?` in [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
// What you write:
suspend fun load(id: String): Task

// What the compiler emits (JVM signature):
fun load(id: String, cont: Continuation<Task>): Any?
```

The [return type]({{ "/en/glossary/return-type/" | relative_url }}) widens to `Any?` because the function has two ways to finish: return the actual `Task` synchronously, or return the `COROUTINE_SUSPENDED` marker meaning "I will call `cont.resume` later".

## The Senior Nuance

- **CPS is what makes `suspend` a compile-time contract.** A caller without a continuation to pass cannot invoke the function — that is the literal reason suspend functions need a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}).
- **It is the [callback]({{ "/en/glossary/callbacks/" | relative_url }}) pattern, automated.** Callback-style code is hand-written CPS. Coroutines let the compiler write it, then hide it behind a sequential syntax — which is why they eliminate [callback hell]({{ "/en/glossary/callback-hell/" | relative_url }}) without changing the underlying model.
- **Java interop shows the seam.** Calling a Kotlin suspend function from Java exposes the `Continuation` parameter directly; libraries like `kotlinx-coroutines-jdk8` exist to hide it.
- The paired transformation is the [state machine]({{ "/en/glossary/state-machine/" | relative_url }}); see [Suspend Functions]({{ "/en/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
