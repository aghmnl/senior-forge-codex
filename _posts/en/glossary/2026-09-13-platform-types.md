---
layout: post
title: "Platform Types"
date: 2026-09-13 12:00:00 +0000
categories: [en, glossary]
tags: [null-safety, interop, type-system]
lang: en
permalink: /en/glossary/platform-types/
---

## The Theory (The What)

A **platform type** is the type Kotlin assigns to a value that comes from Java (or any JVM code) whose nullability the compiler cannot determine. It is written `String!` in error messages and IDE hints, and it means "either `String` or `String?` — you decide". The compiler applies neither check: you may call members on it directly, assign it to a non-nullable variable, or treat it as nullable, and it will accept all three. Nullability is enforced at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) instead, with a [NullPointerException]({{ "/en/glossary/null-pointer-exception/" | relative_url }}) at the point where a `null` reaches a non-nullable Kotlin type.

Platform types exist because Java's type system has no notion of nullability. When a Java method carries a nullability annotation the compiler recognises — `@Nullable`/`@NonNull` from AndroidX, JetBrains, JSR-305 or `jspecify` — Kotlin maps it to an ordinary `T?` or `T`. Without one, the platform type is the honest answer.

```kotlin
// From FollowApp Suite — AboutScreen.kt
val licenseObj = firstLicenseId?.let { licensesMap.optJSONObject(it) }
License(
    licenseName = licenseObj?.optString("name")?.ifBlank { firstLicenseId }
        ?: firstLicenseId ?: "Unknown",
    licenseText = licenseObj?.optString("content").orEmpty()
)
```

`org.json` is unannotated, so `optString` returns `String!` and `optJSONObject` returns `JSONObject!`. The code treats both as nullable on purpose: [safe calls]({{ "/en/glossary/safe-call/" | relative_url }}), Elvis fallbacks and `orEmpty()` turn the ambiguity into an explicit non-null `String` at the boundary.

## The Senior Nuance

- **The danger is the silent path, not the crash.** `val name: String = javaApi.getName()` compiles without a warning. If Java returns `null`, the failure is an NPE at the assignment — or worse, several frames later, once the value has been stored and passed around. Every `!!` the compiler *would* have demanded is simply absent.
- **Resolve the type at the boundary, once.** Wrap unannotated Java calls in a Kotlin function whose signature states the truth (`fun readName(): String?`), or declare the receiving variable explicitly (`val name: String? = javaApi.getName()`). Platform types should never propagate into the [data layer]({{ "/en/glossary/data-layer/" | relative_url }}) or into a [data class]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}).
- **Most of the Android SDK and Jetpack are annotated.** `ContentResolver.openOutputStream` is `@Nullable`, which is why FAS must write `requireNotNull(stream) { "Cannot open destination" }` — the compiler sees `OutputStream?`, not a platform type. The gaps are older framework APIs, `org.json`, and third-party Java libraries; treat those as nullable by default.
- **Annotate your own Java, or generate none.** Java code you control should carry `@Nullable`/`@NonNull` so Kotlin callers get real types; annotation-processed code (Room, Hilt) already does. [Raw types]({{ "/en/glossary/raw-types/" | relative_url }}) are the generic-argument twin of the same problem — a `List<!>` from Java suppresses both nullability and type-argument checks.
- **Interview framing:** platform types are one of the four ways Kotlin code still throws an NPE (with `!!`, uninitialised `lateinit` and broken `equals`). See [Null Safety: Elvis & Safe Calls]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
