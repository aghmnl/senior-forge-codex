---
layout: post
title: "Stack Trace"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
tags: [error-handling, jvm, coroutines]
lang: en
permalink: /en/glossary/stack-trace/
---

## The Theory (The What)

A **stack trace** is the snapshot of the [call stack]({{ "/en/glossary/call-stack/" | relative_url }}) at the moment an exception is thrown. It lists every function call ([frame]({{ "/en/glossary/stack-frame/" | relative_url }})) from the point of failure back to the entry point, showing the file name and line number for each [frame]({{ "/en/glossary/stack-frame/" | relative_url }}). On the JVM, `Throwable.stackTrace` captures this information automatically.

## The Senior Nuance

- A meaningful stack trace is the difference between a 5-minute fix and an hour of guesswork. This is why `?: throw IllegalStateException("order required at checkout")` is better than `!!` — the `!!` crash produces a generic [NullPointerException]({{ "/en/glossary/null-pointer-exception/" | relative_url }}) with no context, while the explicit throw tells you exactly which [invariant]({{ "/en/glossary/invariant/" | relative_url }}) was violated.
- [Coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) stack traces are fragmented by default because [`suspend` functions]({{ "/en/glossary/suspend-functions/" | relative_url }}) desugar into [state machines]({{ "/en/glossary/state-machine/" | relative_url }}). Libraries like `kotlinx-coroutines-debug` reconstruct the logical call chain across [suspension points]({{ "/en/glossary/suspension-point/" | relative_url }}).
- On Android, stack traces from release builds are [obfuscated]({{ "/en/glossary/obfuscation/" | relative_url }}) by [R8]({{ "/en/glossary/r8/" | relative_url }})/[ProGuard]({{ "/en/glossary/proguard/" | relative_url }}). A Senior maintains mapping files and uploads them to [Crashlytics]({{ "/en/glossary/crashlytics/" | relative_url }}) so production stack traces are readable.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
