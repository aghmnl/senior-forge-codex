---
layout: post
title: "@NonNull"
date: 2026-09-18 12:00:00 +0000
categories: [en, glossary]
tags: [interop, null-safety]
lang: en
permalink: /en/glossary/non-null-annotation/
---

## The Theory (The What)

**`@NonNull`** (also `@NotNull` in JetBrains' set) is the Java annotation that tells the Kotlin compiler a value coming from Java is never [`null`]({{ "/en/glossary/null/" | relative_url }}). Kotlin then treats the Java `String` as a plain `String` instead of a [platform type]({{ "/en/glossary/platform-types/" | relative_url }}) `String!`, so no null handling is required — and, for parameters, Kotlin refuses to pass a nullable into it. Paired with [`@Nullable`]({{ "/en/glossary/nullable-annotation/" | relative_url }}), it makes the Java/Kotlin boundary as strict as pure Kotlin code, which is the point of the interop guidance in [Null Safety: Elvis & Safe Calls]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

```kotlin
// Java side
public @NonNull List<Task> loadTasks(@NonNull String userId) { ... }

// Kotlin side
val tasks: List<Task> = api.loadTasks(userId)   // no ?. needed
// api.loadTasks(null)                            // does not compile
```

## The Senior Nuance

- **Kotlin generates a runtime check for `@NonNull` parameters of Kotlin functions called from Java, not the other way round.** A Java `@NonNull` return that lies still produces an NPE in Kotlin; the annotation is documentation the compiler trusts, so only apply it where the Java code really guarantees it.
- **Annotate the whole public surface of a Java module, not a few methods.** A half-annotated API is worse than none: readers assume the unannotated methods were checked too.
- **Modern option: JSpecify `@NullMarked`.** One package-level annotation makes everything non-null by default and lets you mark only the nullable exceptions.
- See [Null Safety: Elvis & Safe Calls]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
