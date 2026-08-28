---
layout: post
title: "Annotation Processing"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/annotation-processing/
---

## The Theory (The What)

**Annotation processing** is a [compile-time]({{ "/en/glossary/compile-time/" | relative_url }}) mechanism that reads annotations in [source code]({{ "/en/glossary/source-code/" | relative_url }}) and generates additional code or resources before the final [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) is produced. On the [JVM]({{ "/en/glossary/jvm/" | relative_url }})/Android, two major tools handle this: **kapt** (Kotlin Annotation Processing Tool), which bridges Kotlin to the Java annotation processing API, and **KSP** (Kotlin Symbol Processing), which operates directly on Kotlin's compiler symbols and is significantly faster.

## The Senior Nuance

- Annotation processing generates code **at compile time**, which means errors in the generated code surface as build failures — not [runtime]({{ "/en/glossary/runtime/" | relative_url }}) crashes. This is a major safety advantage.
- **Dagger/Hilt** uses annotation processing to build [dependency graphs]({{ "/en/glossary/dependency-graph/" | relative_url }}) — every `@Inject`, `@Module`, and `@Binds` is resolved at compile time, guaranteeing that all dependencies are satisfiable before the app runs.
- **kapt** works by generating Java stubs from Kotlin source and then running Java's `javax.annotation.processing` API. This stub generation step is the primary reason kapt is slow. **KSP** avoids stubs entirely, processing Kotlin symbols directly — typically 2× faster.
- Room DAO implementations, Moshi/Kotlinx.Serialization adapters, and navigation Safe Args are all generated via annotation processing.

```kotlin
// From FollowApp Suite — RepositoryModule.kt
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    abstract fun bindTaskRepository(
        taskRepositoryImpl: TaskRepositoryImpl
    ): TaskRepository

    @Binds
    abstract fun bindLabelRepository(
        labelRepositoryImpl: LabelRepositoryImpl
    ): LabelRepository
}
```

In this example, `@Module`, `@InstallIn`, and `@Binds` are all processed at compile time by Hilt's annotation processor, which generates the wiring code that connects interfaces to their implementations.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
