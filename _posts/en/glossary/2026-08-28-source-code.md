---
layout: post
title: "Source Code"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/source-code/
---

## The Theory (The What)

**Source code** is the human-readable text that programmers write in a programming language (Kotlin, Java, C, etc.). It is the input to the compiler, which translates it into [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) or machine code at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}). Source code is where all design decisions — type definitions, algorithms, architecture — are expressed. It is versioned in repositories (Git), reviewed in pull requests, and is the single source of truth for what a program does.

## The Senior Nuance

- Source code is what exists **before** compilation. After [compile time]({{ "/en/glossary/compile-time/" | relative_url }}), it becomes [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) (on the [JVM]({{ "/en/glossary/jvm/" | relative_url }})) or native machine code. Many Kotlin features (extension functions, data classes, default parameters) exist only in source code — they are desugared or transformed during compilation.
- [Annotation processing]({{ "/en/glossary/annotation-processing/" | relative_url }}) reads source code annotations and generates *additional* source code (or bytecode) at compile time. The generated code is compiled alongside the handwritten code.
- Source code and bytecode can diverge significantly: a Kotlin `data class` with five properties generates `equals()`, `hashCode()`, `toString()`, `copy()`, and `componentN()` functions in bytecode that are invisible in the source. Understanding this gap is key to debugging decompiled code.
- In Kotlin Multiplatform, the same source code (in `commonMain`) compiles to JVM bytecode, JavaScript, or native binaries depending on the target — the source is platform-agnostic, the output is not.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
