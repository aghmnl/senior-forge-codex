---
layout: post
title: "@IoDispatcher"
date: 2026-09-14 12:00:00 +0000
categories: [en, glossary]
tags: [di, coroutines, testing]
lang: en
permalink: /en/glossary/io-dispatcher/
---

## The Theory (The What)

**`@IoDispatcher`** is the conventional Hilt/Dagger *qualifier* annotation used to inject [`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) as a `CoroutineDispatcher` dependency instead of referencing the singleton directly. Siblings `@DefaultDispatcher` and `@MainDispatcher` follow the same pattern. The names come from Google's architecture samples; nothing in the library defines them — you declare them.

```kotlin
// Not found in FAS — standalone example
@Qualifier @Retention(AnnotationRetention.BINARY) annotation class IoDispatcher

@Module @InstallIn(SingletonComponent::class)
object DispatchersModule {
    @Provides @IoDispatcher fun provideIo(): CoroutineDispatcher = Dispatchers.IO
}

class BackupManager @Inject constructor(@IoDispatcher private val io: CoroutineDispatcher) {
    suspend fun exportTo(uri: Uri) = withContext(io) { /* ... */ }
}
```

## The Senior Nuance

- **The point is testability.** With the dispatcher injected, a unit test passes `StandardTestDispatcher(testScheduler)` and the whole class runs on virtual time under [`runTest`]({{ "/en/glossary/run-test/" | relative_url }}). Hard-coded `Dispatchers.IO` cannot be intercepted.
- **A qualifier is needed because the type is the same.** `CoroutineDispatcher` for IO, Default and Main are indistinguishable to [Hilt]({{ "/en/glossary/hilt/" | relative_url }}) without one; the annotation is what disambiguates the binding.
- **Provide all three from one module**, `@Singleton`-free — the dispatchers are already singletons.
- See [Context & Dispatchers]({{ "/en/02-coroutines-flow/context-dispatchers/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
