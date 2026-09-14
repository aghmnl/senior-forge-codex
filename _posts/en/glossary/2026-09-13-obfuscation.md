---
layout: post
title: "Obfuscation"
date: 2026-09-13 12:00:00 +0000
categories: [en, glossary]
tags: [build-tools, reflection, error-handling]
lang: en
permalink: /en/glossary/obfuscation/
---

## The Theory (The What)

**Obfuscation** is the renaming of classes, methods and fields to short, meaningless identifiers (`a`, `b`, `c.d()`) in a release build. On Android it is one of the three things [R8]({{ "/en/glossary/r8/" | relative_url }}) does alongside shrinking and optimisation, and it is enabled by `isMinifyEnabled = true`. The goals are a smaller `.dex` and a harder target for reverse engineering — not real security, since the [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) remains fully decompilable.

```kotlin
// From FollowApp Suite — build.gradle.kts
release {
    isMinifyEnabled = true
    isShrinkResources = true
    proguardFiles(
        getDefaultProguardFile("proguard-android-optimize.txt"),
        "proguard-rules.pro"
    )
    // Crashlytics reports only from production builds. R8 mapping
    // is uploaded automatically by the Crashlytics Gradle plugin.
    manifestPlaceholders["crashlyticsCollectionEnabled"] = true
}
```

The side effect is that a production [stack trace]({{ "/en/glossary/stack-trace/" | relative_url }}) reads `at c.a.b(Unknown Source:12)`. R8 writes a `mapping.txt` for every build that maps obfuscated names back to the originals; without it the trace is useless.

## The Senior Nuance

- **Keep the mapping file, or the crash is unreadable.** `mapping.txt` is generated per build and differs between builds. Upload it with every release — the [Crashlytics]({{ "/en/glossary/crashlytics/" | relative_url }}) Gradle plugin does it automatically, Play Console accepts it manually — and archive it with the tag.
- **Obfuscation and [reflection]({{ "/en/glossary/runtime-reflection/" | relative_url }}) conflict.** Anything looked up by name at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) (Gson field names, `Class.forName`, JNI symbols, enum `valueOf`) breaks when renamed. That is what `-keep` rules in [ProGuard]({{ "/en/glossary/proguard/" | relative_url }}) syntax are for — FAS keeps enum members for exactly this reason.
- **Test the release build, not just debug.** Obfuscation bugs appear only with `isMinifyEnabled = true`. A Senior runs the minified build regularly, not the night before shipping.
- **It is not encryption.** Strings, resources and control flow survive intact. Secrets do not belong in the APK, obfuscated or not.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
