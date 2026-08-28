---
layout: post
title: "Extension Functions"
date: 2026-08-28 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/extension-functions/
---

## The Theory (The What)

**Extension functions** allow adding new functions to existing classes without modifying their source code or using inheritance. Syntactically they look like member functions (`receiver.functionName()`), but they are resolved **statically at [compile time]({{ "/en/glossary/compile-time/" | relative_url }})** based on the declared type of the receiver — not the [runtime]({{ "/en/glossary/runtime/" | relative_url }}) type. Under the hood, the Kotlin compiler translates them into static methods where the receiver becomes the first parameter.

## The Senior Nuance

- Because extensions are resolved at compile time, they do **not** participate in virtual dispatch. If a base class and a subclass both have an extension with the same signature, the one called depends on the *declared* type, not the actual type. This is the opposite of overridden member functions.
- Extension functions compile to static [JVM]({{ "/en/glossary/jvm/" | relative_url }}) methods. `fun String.isPalindrome()` becomes `public static boolean isPalindrome(String $this$isPalindrome)` in the [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}). There is zero runtime overhead — no wrapper objects, no reflection.
- In Android/Kotlin codebases, extension functions are the idiomatic way to write mapper/converter utilities — they read naturally and keep domain models free of infrastructure concerns.
- Extensions cannot access `private` or `protected` members of the receiver class. They only see the class's public API, which makes them safer than subclassing.

```kotlin
// From FollowApp Suite — LabelMapper.kt
fun LabelEntity.toDomain(): Label = Label(
    id = this.id,
    name = this.name,
    type = LabelType.valueOf(this.type),
    createdAt = this.createdAt,
    updatedAt = this.updatedAt
)
```

```kotlin
// From FollowApp Suite — ErrorMapping.kt
@StringRes
fun Throwable.toUserMessage(): Int = when {
    this is SQLiteConstraintException && message.orEmpty().contains("UNIQUE") ->
        R.string.error_duplicate_tag
    else -> R.string.error_generic
}
```

Both functions add behavior to existing types (`LabelEntity`, `Throwable`) without modifying those classes. The compiler resolves the call based on the declared type at each call site.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
