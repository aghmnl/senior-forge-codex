---
layout: post
title: "@JvmOverloads"
date: 2026-09-07 12:00:00 +0000
categories: [en, glossary]
tags: [interop, dispatch, android-framework]
lang: en
permalink: /en/glossary/jvm-overloads/
---

## The Theory (The What)

`@JvmOverloads` instructs the Kotlin compiler to generate, for a function with default parameter values, one additional [JVM]({{ "/en/glossary/jvm/" | relative_url }}) method per omitted parameter. Kotlin's default arguments are a *language* feature the JVM has no concept of: without the annotation, Kotlin emits a single method plus a synthetic bridge, and Java callers must pass every argument.

```kotlin
// Not found in FAS — standalone example
class CustomChip @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0
) : View(context, attrs, defStyleAttr)
```

That single declaration generates three constructors in the [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) — `(Context)`, `(Context, AttributeSet?)` and `(Context, AttributeSet?, Int)` — which is a form of ad-hoc [polymorphism]({{ "/en/glossary/polymorphism/" | relative_url }}) resolved by [static dispatch]({{ "/en/glossary/static-dispatch/" | relative_url }}) at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}).

## The Senior Nuance

- **Its classic use is custom Views.** The Android layout inflater reflectively looks for specific constructor signatures, so a custom `View` written in Kotlin with default arguments will inflate correctly from XML only if `@JvmOverloads` generated them. This is a real crash, not a theoretical concern — and it is largely historical now that [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) replaces custom Views.
- **It is a Java-interop tool, and pure-Kotlin modules do not need it.** Kotlin callers resolve default arguments at the [call site]({{ "/en/glossary/call-site/" | relative_url }}) without any generated overloads. Adding the annotation to code no Java consumer touches is [code bloat]({{ "/en/glossary/code-bloat/" | relative_url }}) for nothing — every generated method costs method-count and APK size.
- **It generates a linear chain, not a combinatorial one.** For `f(a, b = 1, c = 2)` you get `f(a)`, `f(a, b)` and `f(a, b, c)` — never `f(a, c)`. Parameters can only be dropped from the right. If Java callers need to skip a middle parameter, write the overload by hand.
- **It interacts badly with adding parameters later.** Inserting a new default parameter in the middle silently changes which generated signature means what, breaking already-compiled Java callers at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) rather than at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}). Append new defaults at the end.
- **On a constructor the annotation goes on the `constructor` [keyword]({{ "/en/glossary/keyword/" | relative_url }})**, which is why the [primary constructor]({{ "/en/glossary/primary-constructor/" | relative_url }}) must be written out explicitly rather than in its usual implicit form.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
