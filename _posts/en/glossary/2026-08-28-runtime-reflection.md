---
layout: post
title: "Runtime Reflection"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/runtime-reflection/
---

## The Theory (The What)

**Runtime reflection** is the ability of a program to inspect and manipulate its own structure — classes, functions, properties, annotations — while it is [running]({{ "/en/glossary/runtime/" | relative_url }}). On the [JVM]({{ "/en/glossary/jvm/" | relative_url }}), this is provided by `java.lang.reflect` and Kotlin's `kotlin.reflect` (`KClass`, `KFunction`, `KProperty`). Reflection bypasses [compile-time]({{ "/en/glossary/compile-time/" | relative_url }}) type checking: instead of the compiler resolving a method call, the program discovers and invokes it at runtime by name or signature.

## The Senior Nuance

- Reflection is **powerful but expensive**: creating `KClass`/`KFunction` instances, resolving methods, and invoking them reflectively can be 10–100× slower than a direct call. It also bypasses compile-time safety — a typo in a method name becomes a runtime crash, not a build error.
- **[R8]({{ "/en/glossary/r8/" | relative_url }})/[ProGuard]({{ "/en/glossary/proguard/" | relative_url }}) and reflection conflict**: [R8]({{ "/en/glossary/r8/" | relative_url }}) renames and removes classes/methods that appear unused. If your code accesses them only via reflection, [R8]({{ "/en/glossary/r8/" | relative_url }}) doesn't see the reference and removes them. This is why libraries using reflection (Gson, Retrofit with converters) require [ProGuard]({{ "/en/glossary/proguard/" | relative_url }}) keep rules.
- Prefer [compile-time]({{ "/en/glossary/compile-time/" | relative_url }}) alternatives to reflection whenever possible: [annotation processing]({{ "/en/glossary/annotation-processing/" | relative_url }}) ([Dagger]({{ "/en/glossary/dagger/" | relative_url }})/[Hilt]({{ "/en/glossary/hilt/" | relative_url }}) generates code instead of reflecting), sealed class hierarchies (exhaustive `when` instead of reflective dispatch), and [`reified`]({{ "/en/glossary/reified/" | relative_url }}) type parameters (compile-time type substitution instead of runtime type checks).
- `::class` in Kotlin gives you a `KClass` reference. `::class.java` gives the Java `Class` object. Both are runtime reflection entry points. Common uses: `[Room]({{ "/en/glossary/room/" | relative_url }}).inMemoryDatabaseBuilder(ctx, MyDb::class.java)`, `startActivity(Intent(this, TargetActivity::class.java))`, serialization frameworks.
- Kotlin's `kotlin-reflect` library adds full Kotlin reflection support (property metadata, nullability, etc.) but is ~2.5 MB — significant on Android. For most Android use cases, `java.lang.reflect` or annotation-processed code is preferred.

```kotlin
// From FollowApp Suite — TaskDaoSortTest.kt
db = Room.inMemoryDatabaseBuilder(context, MyTasksDatabase::class.java)
    .allowMainThreadQueries()
    .build()
```

`::class.java` is a lightweight reflection entry point — [Room]({{ "/en/glossary/room/" | relative_url }}) uses the `Class` token to locate the generated `_Impl` class produced by [annotation processing]({{ "/en/glossary/annotation-processing/" | relative_url }}), not to reflectively scan the database class.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
