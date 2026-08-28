---
layout: post
title: "Decorator"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/decorator/
---

## The Theory (The What)

The **Decorator** pattern adds behavior to an object dynamically by wrapping it in another object that implements the same interface. The wrapper delegates calls to the original and adds its own logic before or after. In classic OOP, this avoids the combinatorial explosion of subclassing: instead of creating `LoggingCachingRepository`, `LoggingRepository`, and `CachingRepository` as separate subclasses, you stack decorators.

In Kotlin, the `by` keyword makes delegation trivial:

```kotlin
class LoggingRepository(
    private val delegate: TaskRepository
) : TaskRepository by delegate {
    override fun save(task: Task) {
        log("Saving task ${task.id}")
        delegate.save(task)
    }
}
```

## The Senior Nuance

- Kotlin's [extension functions]({{ "/en/glossary/extension-functions/" | relative_url }}) often replace the Decorator pattern for simpler cases. When you need to add behavior to a type without wrapping it — and you don't need to intercept every method — an extension is lighter and more idiomatic.
- The key distinction: a Decorator wraps and controls access to the original object (it can intercept *any* method call). An extension function adds a new function but cannot intercept existing ones. Choose Decorator when you need to modify or observe behavior of existing methods; choose extensions when you are adding new behavior.
- In Android, the Decorator pattern appears naturally in repository layers (adding caching, logging, or error handling around a data source) and in `InputStream`/`OutputStream` chains from Java's I/O library.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
