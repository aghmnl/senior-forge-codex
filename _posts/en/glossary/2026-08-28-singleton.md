---
layout: post
title: "Singleton"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/singleton/
---

## The Theory (The What)

A **Singleton** is a design pattern that guarantees exactly one instance of a class exists throughout the application's lifetime. In Kotlin, the `object` declaration is the idiomatic way to create a singleton — the compiler handles thread-safe lazy initialization and prevents additional instantiation. No constructor is needed or allowed.

```kotlin
// From FollowApp Suite — BackupSerializer.kt
object BackupSerializer {
    private const val FORMAT = "followapp-mytasks-backup"
    private const val VERSION = 1

    fun serialize(bundle: BackupBundle): String {
        val root = JSONObject()
        root.put("format", FORMAT)
        root.put("version", VERSION)
        root.put("exportedAt", System.currentTimeMillis())
        root.put("tasks", JSONArray(bundle.tasks.map(::taskToJson)))
        root.put("labels", JSONArray(bundle.labels.map(::labelToJson)))
        return root.toString()
    }
}
```

## The Senior Nuance

- Kotlin's `object` compiles to a Java class with a `private` constructor and a `static final INSTANCE` field, initialized in a `static {}` block. This is thread-safe by [JVM]({{ "/en/glossary/jvm/" | relative_url }}) specification — no `synchronized` or `volatile` needed.
- In [sealed hierarchies]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}), `object` (or `data object`) is used for stateless leaves — branches that carry no data. Since they are singletons, they produce zero allocations when emitted through `StateFlow` or compared in [collections]({{ "/en/glossary/collections/" | relative_url }}).
- The main danger of singletons is hidden global state. A stateless singleton with pure functions (like the FAS example) is safe. A singleton holding mutable state becomes a shared mutable dependency — hard to test, hard to reason about in concurrent code. Prefer dependency injection for stateful services.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
