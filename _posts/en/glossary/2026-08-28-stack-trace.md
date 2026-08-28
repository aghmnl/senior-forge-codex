---
layout: post
title: "Stack Trace"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/stack-trace/
---

## The Theory (The What)

A **stack trace** is the snapshot of the call stack at the moment an exception is thrown. It lists every function call (frame) from the point of failure back to the entry point, showing the file name and line number for each frame. On the JVM, `Throwable.stackTrace` captures this information automatically.

## The Senior Nuance

- A meaningful stack trace is the difference between a 5-minute fix and an hour of guesswork. This is why `?: throw IllegalStateException("order required at checkout")` is better than `!!` — the `!!` crash produces a generic [NullPointerException]({{ "/en/glossary/null-pointer-exception/" | relative_url }}) with no context, while the explicit throw tells you exactly which invariant was violated.
- Coroutine stack traces are fragmented by default because `suspend` functions desugar into state machines. Libraries like `kotlinx-coroutines-debug` reconstruct the logical call chain across suspension points.
- On Android, stack traces from release builds are obfuscated by R8/ProGuard. A Senior maintains mapping files and uploads them to Crashlytics so production stack traces are readable.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
