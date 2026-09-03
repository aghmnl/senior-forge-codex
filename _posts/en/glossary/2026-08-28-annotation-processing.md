---
layout: post
title: "Annotation Processing"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/annotation-processing/
---

## The Theory (The What)

**Annotation processing** is a [compile-time]({{ "/en/glossary/compile-time/" | relative_url }}) mechanism that reads annotations in [source code]({{ "/en/glossary/source-code/" | relative_url }}) and generates additional code or resources before the final [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) is produced. On the [JVM]({{ "/en/glossary/jvm/" | relative_url }})/Android, two major tools handle this: **[kapt]({{ "/en/glossary/kapt/" | relative_url }})** (Kotlin Annotation Processing Tool), which bridges Kotlin to the Java annotation processing API, and **[KSP]({{ "/en/glossary/ksp/" | relative_url }})** (Kotlin Symbol Processing), which operates directly on Kotlin's compiler symbols and is significantly faster.

## The Senior Nuance

- Annotation processing generates code **at compile time**, which means errors in the generated code surface as build failures — not [runtime]({{ "/en/glossary/runtime/" | relative_url }}) crashes. This is a major safety advantage.
- **[Dagger]({{ "/en/glossary/dagger/" | relative_url }})/[Hilt]({{ "/en/glossary/hilt/" | relative_url }})** uses annotation processing to build [dependency graphs]({{ "/en/glossary/dependency-graph/" | relative_url }}) — every [`@Inject`]({{ "/en/glossary/inject/" | relative_url }}), [`@Module`]({{ "/en/glossary/module-annotation/" | relative_url }}), and [`@Binds`]({{ "/en/glossary/binds/" | relative_url }}) is resolved at compile time, guaranteeing that all dependencies are satisfiable before the app runs.
- **[kapt]({{ "/en/glossary/kapt/" | relative_url }})** works by generating Java [stubs]({{ "/en/glossary/stubs/" | relative_url }}) from Kotlin source and then running Java's `javax.annotation.processing` API. This [stub]({{ "/en/glossary/stubs/" | relative_url }}) generation step is the primary reason [kapt]({{ "/en/glossary/kapt/" | relative_url }}) is slow. **[KSP]({{ "/en/glossary/ksp/" | relative_url }})** avoids [stubs]({{ "/en/glossary/stubs/" | relative_url }}) entirely, processing Kotlin symbols directly — typically 2× faster.
- [Room]({{ "/en/glossary/room/" | relative_url }}) [DAO]({{ "/en/glossary/dao/" | relative_url }}) implementations, [Moshi]({{ "/en/glossary/moshi/" | relative_url }})/Kotlinx.Serialization adapters, and [navigation]({{ "/en/glossary/navigation-component/" | relative_url }}) [Safe Args]({{ "/en/glossary/safe-args/" | relative_url }}) are all generated via annotation processing.

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

In this example, [`@Module`]({{ "/en/glossary/module-annotation/" | relative_url }}), [`@InstallIn`]({{ "/en/glossary/install-in/" | relative_url }}), and [`@Binds`]({{ "/en/glossary/binds/" | relative_url }}) are all processed at compile time by [Hilt]({{ "/en/glossary/hilt/" | relative_url }})'s annotation processor, which generates the wiring code that connects interfaces to their implementations.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
