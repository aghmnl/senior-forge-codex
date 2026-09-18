---
layout: post
title: "@Nullable"
date: 2026-09-18 12:00:00 +0000
categories: [en, glossary]
tags: [interop, null-safety]
lang: en
permalink: /en/glossary/nullable-annotation/
---

## The Theory (The What)

**`@Nullable`** is a Java annotation (from `androidx.annotation`, JetBrains, JSpecify or JSR-305) that tells the Kotlin compiler a Java parameter, field or return value may be [`null`]({{ "/en/glossary/null/" | relative_url }}). Without it, values crossing from Java arrive as [platform types]({{ "/en/glossary/platform-types/" | relative_url }}) (`String!`) and Kotlin cannot enforce anything; with it, the value is seen as `String?` and every use must handle the null. Its counterpart is [`@NonNull`]({{ "/en/glossary/non-null-annotation/" | relative_url }}). Annotating the Java side is the [Null Safety: Elvis & Safe Calls]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}) article's first tool for closing the interop boundary.

```kotlin
// Java side (library or legacy module)
public class LegacyUserStore {
    public @Nullable String getPhotoUrl() { ... }   // Kotlin sees String?
    public @NonNull  String getEmail()    { ... }   // Kotlin sees String
}

// Kotlin side: the compiler now forces the null handling
val url: String? = store.photoUrl
val length = url?.length ?: 0
```

## The Senior Nuance

- **An annotation is a promise Kotlin enforces on the caller, not on the Java body.** If a `@NonNull` method returns null anyway, Kotlin still crashes — but at the call site, with an `IllegalStateException`-style message naming the parameter, which is far better than a distant NPE.
- **When you cannot edit the Java code, wrap it.** A one-line Kotlin function that returns `String?` documents the boundary and keeps the platform type out of the rest of the codebase.
- **Prefer the AndroidX annotations on Android.** `androidx.annotation.Nullable`/`NonNull` are what Lint, the IDE and the Kotlin compiler all understand.
- See [Null Safety: Elvis & Safe Calls]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
