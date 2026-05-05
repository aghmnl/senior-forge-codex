---
layout: post
title: "Garbage Collector (GC)"
date: 2026-05-04 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/garbage-collector/
---

## The Theory (The What)

The **Garbage Collector (GC)** is an automated memory management system within the Android Runtime (ART) and the Java Virtual Machine (JVM). Its primary responsibility is to identify objects in the heap that are no longer reachable by the application and reclaim their memory, preventing memory leaks and manual memory deallocation errors.



## The Senior Nuance

For a Senior Android Developer, the GC is not just a background process but a performance factor:
- **Generational GC**: ART uses a generational approach, dividing the heap into different regions (Young, Old) based on object lifetime to optimize collection frequency.
- **GC Pauses**: Intensive object allocation (like inside a `onDraw` method or high-frequency loops) can trigger frequent GC cycles, leading to "jank" or dropped frames in the UI.
- **Reachability**: Memory is reclaimed only when an object has no "strong references" leading back to a GC Root. Understanding the difference between Strong, Weak, and Soft references is vital for preventing leaks in complex architectures.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
