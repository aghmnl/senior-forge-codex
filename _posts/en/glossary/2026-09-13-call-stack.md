---
layout: post
title: "Call Stack"
date: 2026-09-13 12:00:00 +0000
categories: [en, glossary]
tags: [jvm, memory, error-handling]
lang: en
permalink: /en/glossary/call-stack/
---

## The Theory (The What)

The **call stack** is the region of memory where a [thread]({{ "/en/glossary/thread/" | relative_url }}) records the chain of function calls currently in progress. Each call pushes a [stack frame]({{ "/en/glossary/stack-frame/" | relative_url }}) — parameters, locals and the return address — and each return pops it. The frame on top is the function running right now; the one at the bottom is the entry point (`main`, or an Android lifecycle callback). A [stack trace]({{ "/en/glossary/stack-trace/" | relative_url }}) is a printed snapshot of this structure at the moment an exception is thrown.

```kotlin
// Not found in FAS — standalone example
fun main() { load("42") }                 // frame 3 (bottom)
fun load(id: String) = parse(fetch(id))   // frame 2
fun parse(raw: String): Task = TODO()     // frame 1 (top: where the exception is thrown)
```

Every thread has its own call stack (~1 MB on Android), which is why [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}) — which keep their state on the [heap]({{ "/en/glossary/heap/" | relative_url }}) instead — can be so much cheaper than threads.

## The Senior Nuance

- **Depth is bounded.** A recursion with no base case, or a property setter that assigns `this.property = value` instead of `field = value`, grows the stack until `StackOverflowError`. The trace shows the same frame repeated hundreds of times — the signature of the bug.
- **Locals die with the frame.** A mutable object referenced only from one frame is unreachable from any other thread, which is what makes "mutate locally, publish [immutably]({{ "/en/glossary/immutability/" | relative_url }})" safe without locks.
- **Coroutines do not have a real call stack across suspension.** After a [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}) the physical stack has unwound; the logical chain lives in [continuations]({{ "/en/glossary/continuation/" | relative_url }}). That is why coroutine stack traces look fragmented unless `kotlinx-coroutines-debug` reconstructs them.
- **[Inline functions]({{ "/en/glossary/inline-functions/" | relative_url }}) leave no frame.** Their body is copied into the caller, so they never appear in a trace — convenient for `let`/`apply`, occasionally confusing when a line number points into the caller.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
