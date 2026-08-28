---
layout: post
title: "AOT Compilation"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/aot-compilation/
---

## The Theory (The What)

**Ahead-of-Time (AOT) compilation** is the process of translating [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) into native machine code *before* the application runs, rather than during [runtime]({{ "/en/glossary/runtime/" | relative_url }}). On Android, AOT compilation happens at app install time (or during idle maintenance) as part of the Android Runtime (ART) pipeline. The result is a native `.oat` file that the device executes directly, avoiding the overhead of interpreting or [JIT-compiling]({{ "/en/glossary/jit-compilation/" | relative_url }}) bytecode on every launch.

## The Senior Nuance

- Android's ART uses a **hybrid strategy**: AOT compilation at install time for baseline performance, [JIT compilation]({{ "/en/glossary/jit-compilation/" | relative_url }}) for hot paths discovered at runtime, and [profile-guided optimization (PGO)]({{ "/en/glossary/pgo/" | relative_url }}) to refine AOT compilation on subsequent installs or updates. Understanding this pipeline explains why "first run after install" can behave differently than subsequent runs.
- AOT compilation eliminates the startup penalty of interpreting bytecode, but increases install time and storage footprint — the native `.oat` code is larger than the original `.dex` [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}). This trade-off is why Android doesn't AOT-compile everything — it uses profiles to identify which methods are worth compiling ahead of time.
- R8/D8 (which run at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) on the developer's machine) produce optimized `.dex` bytecode. ART's AOT compiler then translates that `.dex` into native code for the specific device architecture (ARM64, x86). These are two separate compilation stages with different optimization goals.
- Kotlin/Native uses AOT compilation exclusively (no JVM, no interpreter) to produce standalone binaries for iOS, macOS, Linux, etc. There is no JIT phase — all optimizations must happen at compile time.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
