---
layout: post
title: "DataStore"
date: 2026-09-17 12:00:00 +0000
categories: [en, glossary]
tags: [persistence, coroutines, android-framework]
lang: en
permalink: /en/glossary/datastore/
---

## The Theory (The What)

**Jetpack DataStore** is the replacement for `SharedPreferences`: a small key-value (`Preferences DataStore`) or typed (`Proto DataStore`) store whose entire API is built on [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}) and [`Flow`]({{ "/en/glossary/flow/" | relative_url }}). Reads are a `Flow<Preferences>` you [collect]({{ "/en/glossary/collect/" | relative_url }}) (or `.first()`); writes are a [suspend]({{ "/en/glossary/suspend-functions/" | relative_url }}) `edit { }` that is transactional and atomic. Every operation is **main-safe by construction** — DataStore performs its file I/O on [`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) internally.

```kotlin
// From FollowApp Suite — LanguagePreferences.kt
@Singleton
class LanguagePreferences @Inject constructor(
    private val dataStore: DataStore<Preferences>
) {
    private val languageKey = stringPreferencesKey("language")

    fun getLanguage(): Flow<String> = dataStore.data.map { it[languageKey] ?: "system" }

    suspend fun setLanguage(tag: String) {
        dataStore.edit { it[languageKey] = tag }
    }
}
```

## The Senior Nuance

- **Do not wrap it in `withContext(IO)`.** It already switches; the wrapper is noise and tells the next reader the API is not main-safe.
- **The first read pays a cold file open.** Several preferences in the same file cost *one* open; several files cost several. Group related keys.
- **One `DataStore` instance per file, process-wide.** Two instances on the same file corrupt it — hence the `@Singleton` and the top-level `preferencesDataStore` delegate.
- **`SharedPreferences` reads block; DataStore reads suspend.** That difference is the whole reason it exists.
- See [Main-Safety]({{ "/en/02-coroutines-flow/main-safety/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
