---
layout: post
title: "@JvmStatic"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/jvm-static/
---

## The Theory (The What)

**`@JvmStatic`** is a Kotlin annotation that instructs the compiler to generate a true JVM `static` method on the enclosing class, in addition to the regular instance method on the [companion object]({{ "/en/glossary/companion-object/" | relative_url }}). Without it, a companion function `MyClass.Companion.doSomething()` exists as an instance method on the `Companion` class — Java callers must write `MyClass.Companion.doSomething()` instead of `MyClass.doSomething()`.

`@JvmStatic` can be applied to functions and property accessors inside a `companion object` or a named `object`.

```kotlin
// Not found in FAS — standalone example
class AppConfig {
    companion object {
        @JvmStatic
        fun defaultTimeout(): Long = 30_000L

        @JvmStatic
        val version: String = "2.1.0"
    }
}

// Kotlin: AppConfig.defaultTimeout() — works with or without @JvmStatic
// Java:   AppConfig.defaultTimeout() — works ONLY with @JvmStatic
// Java without @JvmStatic: AppConfig.Companion.defaultTimeout()
```

## The Senior Nuance

- **Java interop**: `@JvmStatic` is essential when your Kotlin code is consumed by Java callers. Without it, Java code must go through the `.Companion` singleton, which is awkward and breaks the API contract you intended. In a mixed Kotlin/Java codebase, every public [companion object]({{ "/en/glossary/companion-object/" | relative_url }}) function that Java calls should have `@JvmStatic`.
- **Framework reflection**: Some Android frameworks (especially older ones) use reflection to find static methods — `@JvmStatic` ensures the method appears at the class level in [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}), satisfying those lookups. This applies to JUnit `@BeforeClass`/`@AfterClass` methods and `@Provides` methods in some Dagger configurations.
- **[Static dispatch]({{ "/en/glossary/static-dispatch/" | relative_url }})**: Both annotated and non-annotated companion functions use [static dispatch]({{ "/en/glossary/static-dispatch/" | relative_url }}) from the Kotlin perspective — the compiler resolves the call at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}). The difference is at the [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) level: `@JvmStatic` generates a true `static` method (one less indirection), while the default generates an instance method on the `Companion` class.
- **`const val` does not need it**: Properties declared as `const val` in a companion object already compile to JVM `static final` fields directly on the enclosing class — `@JvmStatic` is redundant and actually a compiler error on `const val`.
- **Named objects too**: `@JvmStatic` also works on named `object` declarations ([singletons]({{ "/en/glossary/singleton/" | relative_url }})), which is useful for utility objects that Java code needs to call without `.INSTANCE`.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
