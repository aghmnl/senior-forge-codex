---
layout: post
title: "@Module"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/module-annotation/
---

## The Theory (The What)

**`@Module`** is a [Dagger]({{ "/en/glossary/dagger/" | relative_url }}) annotation that marks a class as a provider of dependency bindings. A module tells the [annotation processing]({{ "/en/glossary/annotation-processing/" | relative_url }}) pipeline how to supply types that cannot be constructor-injected — interfaces (via [`@Binds`]({{ "/en/glossary/binds/" | relative_url }})), third-party classes, or instances that require custom creation logic (via `@Provides`). In [Hilt]({{ "/en/glossary/hilt/" | relative_url }}), every `@Module` must also declare [`@InstallIn`]({{ "/en/glossary/install-in/" | relative_url }}) to specify which component (scope) the bindings belong to.

```kotlin
// From FollowApp Suite — DatabaseModule.kt
@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    @Provides
    @Singleton
    fun provideMyTasksDatabase(
        @ApplicationContext context: Context
    ): MyTasksDatabase {
        return Room.databaseBuilder(
            context,
            MyTasksDatabase::class.java,
            "mytasks_database.db"
        )
            .addMigrations(MIGRATION_1_2)
            .build()
    }
}
```

## The Senior Nuance

- **`object` vs `abstract class`**: Use `object` for modules with `@Provides` methods (concrete implementations). Use `abstract class` for modules with [`@Binds`]({{ "/en/glossary/binds/" | relative_url }}) methods (interface-to-implementation mappings). Mixing both in one module is possible but usually a code smell.
- **`@Provides` creates instances**: Each `@Provides` function is a factory. [Dagger]({{ "/en/glossary/dagger/" | relative_url }}) generates code that calls it when the return type is needed. Pair with `@Singleton` (or another scope) to cache the instance.
- **Module organization**: Group related bindings in the same module (e.g., `DatabaseModule` for all [DAO]({{ "/en/glossary/dao/" | relative_url }}) providers, `RepositoryModule` for all repository bindings). This keeps the [dependency graph]({{ "/en/glossary/dependency-graph/" | relative_url }}) readable.
- **Compile-time safety**: If a binding is missing, the build fails — [Dagger]({{ "/en/glossary/dagger/" | relative_url }})'s processor emits a clear error listing the unsatisfied dependency. This is a key advantage over [runtime reflection]({{ "/en/glossary/runtime-reflection/" | relative_url }})-based DI frameworks.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
