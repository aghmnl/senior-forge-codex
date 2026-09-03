---
layout: post
title: "@InstallIn"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/install-in/
---

## The Theory (The What)

**`@InstallIn`** is a [Hilt]({{ "/en/glossary/hilt/" | relative_url }}) annotation that declares which component a [`@Module`]({{ "/en/glossary/module-annotation/" | relative_url }}) belongs to. It connects the module's bindings to a specific scope in the [dependency graph]({{ "/en/glossary/dependency-graph/" | relative_url }}). Without `@InstallIn`, [Hilt]({{ "/en/glossary/hilt/" | relative_url }}) doesn't know where to install the module and the build fails.

```kotlin
// From FollowApp Suite — DatabaseModule.kt
@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {
    // bindings scoped to the app's SingletonComponent
}
```

## The Senior Nuance

- **Component hierarchy**: Hilt defines a fixed component tree — `SingletonComponent` (app-wide), `ActivityRetainedComponent` (survives config changes), `ViewModelComponent`, `ActivityComponent`, `FragmentComponent`, `ViewComponent`, `ServiceComponent`. Each component inherits bindings from its parent.
- **Scope matching**: `@InstallIn(SingletonComponent::class)` makes bindings available app-wide. `@InstallIn(ViewModelComponent::class)` scopes them per-ViewModel. Choosing the wrong component causes either over-sharing (a ViewModel-specific binding available everywhere) or under-availability (a binding missing where it's needed).
- **One module, one component**: A module is installed in exactly one component. If the same binding is needed in multiple scopes, either install in the broadest applicable component or create separate modules.
- **`@InstallIn` is Hilt-specific**: Plain [Dagger]({{ "/en/glossary/dagger/" | relative_url }}) doesn't use `@InstallIn` — modules are added to components manually via `@Component(modules = [...])`. [Hilt]({{ "/en/glossary/hilt/" | relative_url }}) automates this wiring, which is why `@InstallIn` exists.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
