---
layout: post
title: "Android Runtime (ART)"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/android-runtime/
---

## The Theory (The What)

**Android Runtime (ART)** is the managed runtime that executes Android apps. It replaced Dalvik in Android 5.0 (Lollipop). ART compiles [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) (`.dex` files) into native machine code, manages the [heap]({{ "/en/glossary/heap/" | relative_url }}), runs the [Garbage Collector]({{ "/en/glossary/garbage-collector/" | relative_url }}), and enforces security sandboxing. Unlike the [JVM]({{ "/en/glossary/jvm/" | relative_url }}), ART is designed specifically for mobile: it optimizes for battery, memory, and startup latency.

ART uses a hybrid compilation strategy:

- **AOT (Ahead-of-Time)**: at install time or during idle maintenance, ART compiles hot methods into native code stored in `.oat`/`.art` files.
- **[JIT (Just-in-Time)]({{ "/en/glossary/jit-compilation/" | relative_url }})**: at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}), ART compiles frequently executed methods on the fly, using profile data to guide optimization.
- **Baseline profiles**: developer-supplied hints that tell ART which methods to AOT-compile on first install, eliminating the cold-start JIT penalty.

## The Senior Nuance

- ART's GC is concurrent, generational, and moving (compacting). "Moving" means object addresses change during compaction — this is why JNI code must use `GetObjectRefType` and global references carefully; local references can become invalid after a GC.
- ART's [heap]({{ "/en/glossary/heap/" | relative_url }}) is capped per app (typically 256–512 MB). Unlike desktop JVMs, you cannot tune `-Xmx`. The `largeHeap` manifest flag raises the cap but signals poor memory hygiene — prefer fixing [memory leaks]({{ "/en/glossary/memory-leaks/" | relative_url }}) over requesting more heap.
- Baseline Profiles (introduced with Jetpack ProfileInstaller) let you ship a profile that ART uses for AOT compilation on first install. This directly reduces cold-start jank and is a key senior-level optimization for production apps.
- ART enforces strict hidden-API restrictions starting in Android 9. Accessing private framework methods via reflection triggers warnings or hard failures — a constraint that doesn't exist on the standard [JVM]({{ "/en/glossary/jvm/" | relative_url }}).
- R8 (the build-time optimizer) works hand-in-hand with ART: it shrinks, obfuscates, and optimizes the `.dex` bytecode that ART will then compile to native code. Understanding the R8 → ART pipeline is essential for debugging production crashes where stack traces are obfuscated.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
