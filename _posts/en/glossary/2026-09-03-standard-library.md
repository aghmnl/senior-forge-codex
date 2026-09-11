---
layout: post
title: "Standard Library"
date: 2026-09-03 12:00:00 +0000
categories: [en, glossary]
tags: [collections, functional, inlining]
lang: en
permalink: /en/glossary/standard-library/
---

## The Theory (The What)

The **Kotlin Standard Library** (`kotlin-stdlib`) is the set of core APIs that ship with every Kotlin project. It provides fundamental types (`String`, `Int`, [collections]({{ "/en/glossary/collections/" | relative_url }})), utility functions ([scope functions]({{ "/en/01-kotlin-core/scope-functions/" | relative_url }}), `let`, `run`, `apply`, `also`, `with`), I/O primitives, and property delegates (`lazy`, `observable`, `vetoable`, `notNull`).

Unlike Java's standard library, Kotlin's is designed to be cross-platform: the same API surface is available on JVM, JS, Native, and Wasm targets. Platform-specific extensions (like `kotlin.jvm` or `kotlin.js` packages) are segregated into subpackages.

Key areas of the [standard library]({{ "/en/01-kotlin-core/delegated-properties/" | relative_url }}) relevant to Android development:

- **`kotlin.collections`** — [Collections]({{ "/en/glossary/collections/" | relative_url }}), [Maps]({{ "/en/glossary/maps/" | relative_url }}), [Sets]({{ "/en/glossary/sets/" | relative_url }}), and all transformation/filter/fold [extension functions]({{ "/en/glossary/extension-functions/" | relative_url }}).
- **`kotlin.properties`** — `ReadOnlyProperty`, `ReadWriteProperty`, and `Delegates` (used by [delegated properties]({{ "/en/01-kotlin-core/delegated-properties/" | relative_url }})).
- **`kotlin.text`** — String manipulation, regex, and formatting.
- **`kotlin.sequences`** — Lazy evaluation for large data pipelines, avoiding intermediate [allocations]({{ "/en/glossary/allocations/" | relative_url }}).

## The Senior Nuance

- A Senior distinguishes between the standard library (bundled with the Kotlin compiler, always available) and Jetpack/AndroidX libraries (added as Gradle dependencies). Knowing what lives in `stdlib` avoids unnecessary dependencies — for instance, `buildList`, `buildMap`, `groupBy`, and `associate` are all stdlib, not Guava or Apache Commons.
- The standard library is aggressively [inlined]({{ "/en/glossary/inline-functions/" | relative_url }}): many of its [higher-order functions]({{ "/en/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) (`map`, `filter`, `let`, `apply`) are `inline`, eliminating [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) [allocation]({{ "/en/glossary/allocations/" | relative_url }}) overhead at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}).
- The `kotlin-stdlib` artifact was unified in Kotlin 1.8 — `kotlin-stdlib-jdk7` and `kotlin-stdlib-jdk8` are now part of the main artifact. Knowing this avoids redundant dependency declarations in Gradle.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
