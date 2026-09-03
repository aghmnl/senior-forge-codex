---
layout: post
title: "Garbage Collector (GC)"
date: 2026-05-04 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/garbage-collector/
---

## The Theory (The What)

The **Garbage Collector (GC)** is an automated memory management system within the [Android Runtime (ART)]({{ "/en/glossary/android-runtime/" | relative_url }}) and the [Java Virtual Machine (JVM)]({{ "/en/glossary/jvm/" | relative_url }}). Its primary responsibility is to identify objects on the [heap]({{ "/en/glossary/heap/" | relative_url }}) that are no longer reachable by the application and reclaim their memory, preventing [memory leaks]({{ "/en/glossary/memory-leaks/" | relative_url }}) and manual memory deallocation errors.

The GC works by tracing from a set of **GC roots** (static fields, thread stacks, JNI references) and marking every reachable object. Anything not marked is unreachable and can be swept. Modern GCs (like ART's) are concurrent and generational — they collect short-lived objects in the young generation frequently (minor GC) and long-lived objects in the old generation less often (major GC).

## The Senior Nuance

- **Generational GC**: [ART]({{ "/en/glossary/android-runtime/" | relative_url }}) uses a generational approach, dividing the [heap]({{ "/en/glossary/heap/" | relative_url }}) into different regions (Young, Old) based on object lifetime to optimize collection frequency. Most objects die young (the "generational hypothesis"), so minor GCs are fast and cheap.
- **GC Pauses**: Intensive object [allocation]({{ "/en/glossary/allocations/" | relative_url }}) (like inside `onDraw()` or [hot loops]({{ "/en/glossary/hot-loops/" | relative_url }})) can trigger frequent GC cycles, leading to "jank" or dropped frames in the UI. The 16ms frame budget leaves no room for GC pauses — use [inline functions]({{ "/en/glossary/inline-functions/" | relative_url }}), [`IntArray`]({{ "/en/glossary/intarray/" | relative_url }}) over `List<Int>`, and pre-allocated objects to minimize [allocations]({{ "/en/glossary/allocations/" | relative_url }}) in hot paths.
- **Reachability**: Memory is reclaimed only when an object has no strong references leading back to a GC root. Understanding the difference between Strong, Weak (`WeakReference`), and Soft (`SoftReference`) references is vital for preventing [memory leaks]({{ "/en/glossary/memory-leaks/" | relative_url }}) in complex architectures — especially when singletons, static fields, or long-lived callbacks hold references to Activities or Views.
- **[Autoboxing]({{ "/en/glossary/autoboxing/" | relative_url }})** is a hidden GC tax: every `Int?` or `List<Int>` element creates a boxed `Integer` object on the [heap]({{ "/en/glossary/heap/" | relative_url }}). In [hot loops]({{ "/en/glossary/hot-loops/" | relative_url }}), this churn can dominate GC activity.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
