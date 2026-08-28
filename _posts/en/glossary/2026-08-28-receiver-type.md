---
layout: post
title: "Receiver Type"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/receiver-type/
---

## The Theory (The What)

A **receiver type** is the type that an [extension function]({{ "/en/glossary/extension-functions/" | relative_url }}) or a lambda with receiver operates on. In `fun String.isPalindrome()`, `String` is the receiver type — inside the function body, `this` refers to the `String` instance. Kotlin also supports *lambda with receiver* (`T.() -> R`), where the lambda body executes in the [scope]({{ "/en/glossary/scope/" | relative_url }}) of the receiver, enabling [DSL]({{ "/en/glossary/dsl/" | relative_url }})-style APIs.

```kotlin
// From FollowApp Suite — BackupSerializer.kt
private fun JSONObject.optStringOrNull(key: String): String? =
    if (isNull(key)) null else getString(key)

private fun JSONObject.optLongOrNull(key: String): Long? =
    if (isNull(key)) null else getLong(key)
```

```kotlin
// From FollowApp Suite — FollowAppLoadingGear.kt
private fun DrawScope.drawLoadingGear(colors: List<Color>, rotationDeg: Float) {
    // 'this' is the DrawScope — direct access to drawArc, drawCircle, etc.
}
```

## The Senior Nuance

- The receiver type determines which `this` is available inside the function body. When nesting multiple lambdas with receivers (e.g., Compose's `Column { Row { ... } }`), the innermost receiver shadows the outer ones. Use `this@label` to disambiguate, or apply `@DslMarker` to prevent accidental access to outer scopes.
- Extension functions are resolved [statically]({{ "/en/glossary/static-dispatch/" | relative_url }}) based on the *declared* receiver type, not the runtime type. If you declare `fun Animal.sound()` and `fun Dog.sound()`, calling `sound()` on a variable typed as `Animal` always calls the `Animal` version — even if the actual object is a `Dog`. This is the opposite of [polymorphism]({{ "/en/glossary/polymorphism/" | relative_url }}) via virtual dispatch.
- The `ColumnScope.() -> Unit` pattern in Compose restricts what composables are available inside a `Column`: you can call `Modifier.weight()` only because `ColumnScope` is the receiver. This is a compile-time constraint, not a runtime check.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
