---
layout: post
title: "JIT Compilation"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/jit-compilation/
---

## The Theory (The What)

**Just-In-Time (JIT) compilation** is the process of translating [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) into native machine code *during* [runtime]({{ "/en/glossary/runtime/" | relative_url }}), as the code is being executed. The [JVM]({{ "/en/glossary/jvm/" | relative_url }}) and Android's ART both use JIT compilers: they start by interpreting bytecode, identify "hot" methods that are called frequently, and compile those methods to native code on the fly. The compiled code is cached in memory so subsequent calls execute at native speed.

## The Senior Nuance

- JIT compilation is the middle ground between interpretation (slow but no compile cost) and [AOT compilation]({{ "/en/glossary/aot-compilation/" | relative_url }}) (fast execution but upfront cost). Android's ART uses all three: interpreting cold code, JIT-compiling hot paths, and AOT-compiling profiled methods at install time.
- JIT has access to runtime information that [compile-time]({{ "/en/glossary/compile-time/" | relative_url }}) optimization cannot know: actual call frequencies, branch probabilities, which virtual method is called most often at a given call site (monomorphic dispatch). This lets JIT make speculative optimizations — inlining a virtual call with a guard, for example — that static compilers cannot.
- **Warm-up time**: JIT compilation adds latency during the first execution of a method. On Android, this is why app startup can feel sluggish on first launch after install — the JIT hasn't compiled the critical path yet. [Baseline Profiles]({{ "/en/glossary/pgo/" | relative_url }}) exist specifically to mitigate this.
- JIT-compiled code lives only in memory and is lost when the process dies. On Android, ART saves the profiling *data* (not the compiled code) to disk, and a later [AOT pass]({{ "/en/glossary/aot-compilation/" | relative_url }}) uses it via [PGO]({{ "/en/glossary/pgo/" | relative_url }}) to persist the optimization decisions.
- The standard JVM's HotSpot JIT can perform optimizations like escape analysis (eliminating heap allocations when an object doesn't escape a method), loop unrolling, and devirtualization — optimizations that are difficult or impossible at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) because they depend on runtime behavior.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
