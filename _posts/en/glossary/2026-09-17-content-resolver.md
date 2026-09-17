---
layout: post
title: "ContentResolver"
date: 2026-09-17 12:00:00 +0000
categories: [en, glossary]
tags: [android-framework, persistence]
lang: en
permalink: /en/glossary/content-resolver/
---

## The Theory (The What)

**`ContentResolver`** is the framework object (obtained from any `Context`) through which an app talks to `ContentProvider`s — its own or other apps' — and to the Storage Access Framework. `openInputStream(uri)` / `openOutputStream(uri)` turn a `content://` URI the user picked into a raw stream; `query`, `insert`, `update`, `delete` speak to providers like Contacts or MediaStore. Every one of these calls crosses a process boundary and touches disk: they are **[blocking calls]({{ "/en/glossary/blocking-call/" | relative_url }})** and must run off the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}).

```kotlin
// From FollowApp Suite — BackupManager.kt
suspend fun exportTo(uri: Uri): Result<Unit> = withContext(Dispatchers.IO) {
    runCatching {
        val json = BackupSerializer.serialize(bundle)
        context.contentResolver.openOutputStream(uri, "wt").use { stream ->
            requireNotNull(stream) { "Cannot open destination" }
            stream.write(json.toByteArray(Charsets.UTF_8))
        }
    }
}
```

## The Senior Nuance

- **It is the scoped-storage way to read and write user files.** Since Android 10 an app cannot open arbitrary paths; the user picks a document, you get a URI, and `ContentResolver` is the only door.
- **The stream can be `null`.** `openOutputStream` returns `null` when the provider cannot serve the URI — hence the `requireNotNull`. Do not `!!` it.
- **Persist the permission if you need the file again.** `takePersistableUriPermission` — otherwise the grant dies with the Activity.
- See [Main-Safety]({{ "/en/02-coroutines-flow/main-safety/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
