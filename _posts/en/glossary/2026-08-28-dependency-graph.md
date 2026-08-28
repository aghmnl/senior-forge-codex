---
layout: post
title: "Dependency Graph"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/dependency-graph/
---

## The Theory (The What)

A **dependency graph** is a directed graph where nodes represent components (classes, modules, libraries) and edges represent "depends on" relationships. In dependency injection frameworks like Dagger/Hilt, the graph is built and validated at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) through [annotation processing]({{ "/en/glossary/annotation-processing/" | relative_url }}): every `@Inject` constructor, `@Module`, `@Provides`, and `@Binds` declaration becomes a node or edge. If any dependency is missing or circular, the build fails — before the app ever runs.

## The Senior Nuance

- Dagger/Hilt generates the entire dependency graph as concrete [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) at compile time. Unlike service locators (Koin), there is no [runtime]({{ "/en/glossary/runtime/" | relative_url }}) resolution or reflection — every dependency lookup is a direct method call, which is both type-safe and fast.
- The graph structure mirrors application architecture: `SingletonComponent` holds app-scoped dependencies, `ViewModelComponent` holds ViewModel-scoped ones, and `ActivityComponent` / `FragmentComponent` handle UI-scoped instances. Understanding scoping is understanding the graph's lifecycle boundaries.
- Gradle module boundaries also form a dependency graph — `core:domain` depends on nothing, `core:data` depends on `core:domain`, and `app:mytasks` depends on both. Circular module dependencies cause build failures and signal architectural issues.
- In a well-structured Android project, the DI dependency graph and the Gradle module graph reinforce each other: modules expose interfaces, DI binds implementations, and no layer reaches "down" the graph.

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
    abstract fun bindPremiumRepository(
        premiumRepositoryImpl: PremiumRepositoryImpl
    ): PremiumRepository
}
```

Each `@Binds` declaration adds an edge to the dependency graph: `TaskRepository → TaskRepositoryImpl`, `PremiumRepository → PremiumRepositoryImpl`. Hilt's annotation processor validates at compile time that every `@Inject constructor` in each implementation can be satisfied.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
