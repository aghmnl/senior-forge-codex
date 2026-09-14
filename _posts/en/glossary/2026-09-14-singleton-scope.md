---
layout: post
title: "@Singleton"
date: 2026-09-14 12:00:00 +0000
categories: [en, glossary]
tags: [di, lifecycle, architecture]
lang: en
permalink: /en/glossary/singleton-scope/
---

## The Theory (The What)

**`@Singleton`** is the JSR-330 scope annotation that tells [Hilt]({{ "/en/glossary/hilt/" | relative_url }})/[Dagger]({{ "/en/glossary/dagger/" | relative_url }}) to create exactly one instance of a binding per component and reuse it for every injection. In Hilt it belongs to `SingletonComponent`, whose lifetime is the `Application`'s — so a `@Singleton` object lives as long as the process.

```kotlin
// From FollowApp Suite — PremiumRepositoryImpl.kt
@Singleton
class PremiumRepositoryImpl @Inject constructor(
    private val premiumPreferences: PremiumPreferences,
    private val billingConnector: BillingConnector
) : PremiumRepository {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    // ...
}
```

It is a DI *scope*, not the Kotlin `object` [singleton pattern]({{ "/en/glossary/singleton/" | relative_url }}): the class is ordinary and testable; the framework enforces the one-instance rule.

## The Senior Nuance

- **Process lifetime is why a `@Singleton` may own a [`CoroutineScope`]({{ "/en/glossary/coroutine-scope/" | relative_url }}).** Nothing outlives it to cancel it, so a scope that is never cancelled is acceptable here — and only here. Anything shorter-lived must use a lifecycle-bound scope.
- **Everything a `@Singleton` holds is held forever.** A reference to an Activity `Context`, a View or a Fragment inside one is a guaranteed [memory leak]({{ "/en/glossary/memory-leaks/" | relative_url }}); inject `@ApplicationContext`.
- **Unscoped is the default.** Without the annotation Hilt creates a new instance per injection. Scope only what must be shared: repositories, database, HTTP client — not use cases with no state.
- **The scope must match the component.** `@Singleton` on a `ViewModelComponent` binding is a compile error; use `@ViewModelScoped` there.
- See [Context & Dispatchers]({{ "/en/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
