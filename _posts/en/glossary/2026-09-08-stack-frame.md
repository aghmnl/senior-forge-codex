---
layout: post
title: "Stack Frame"
date: 2026-09-08 12:00:00 +0000
categories: [en, glossary]
tags: [jvm, memory, concurrency]
lang: en
permalink: /en/glossary/stack-frame/
---

## The Theory (The What)

A **stack frame** is the block the [JVM]({{ "/en/glossary/jvm/" | relative_url }}) pushes onto the call stack for each method invocation: its parameters, its local variables and its return address. The frame is popped when the method returns, and every local reference in it dies with it.

```kotlin
// From FollowApp Suite — GetLabelReferenceCounts.kt
operator fun invoke(tasks: List<Task>, scaleName: String): Map<String, Int> {
    val refCounts = mutableMapOf<String, Int>()   // local to this frame
    // ...mutated freely: no other thread can reach it...
    return refCounts                              // published read-only
}
```

## The Senior Nuance

- This is the mechanism behind "mutate locally, publish [immutably]({{ "/en/glossary/immutability/" | relative_url }})". A [`MutableMap`]({{ "/en/glossary/mutable-map/" | relative_url }}) referenced only from one frame is unreachable from any other thread, so the [mutation]({{ "/en/glossary/mutation/" | relative_url }}) is [thread-safe]({{ "/en/glossary/thread-safety/" | relative_url }}) by construction — no [synchronized block]({{ "/en/glossary/synchronized-block/" | relative_url }}) required.
- The frame holds the *reference*; the object lives on the [heap]({{ "/en/glossary/heap/" | relative_url }}). Confinement therefore lasts only as long as no other reference escapes — return it, store it in a field, or capture it in a [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) that outlives the call, and the guarantee is gone.
- Frames are also what a [stack trace]({{ "/en/glossary/stack-trace/" | relative_url }}) prints, and what [`inline`]({{ "/en/glossary/inline-functions/" | relative_url }}) removes by copying a function body into the [call site]({{ "/en/glossary/call-site/" | relative_url }}) — which is also why a [`reified`]({{ "/en/glossary/reified/" | relative_url }}) type cannot escape its inlined frame.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
