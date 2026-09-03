---
layout: post
title: "Type Erasure"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/type-erasure/
---

## The Theory (The What)

**Type erasure** is the [JVM]({{ "/en/glossary/jvm/" | relative_url }})'s mechanism for implementing [generics]({{ "/en/01-kotlin-core/generics-variance-reification/" | relative_url }}): [generic type parameters]({{ "/en/glossary/generic-type-parameters/" | relative_url }}) exist only at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) and are removed (erased) from the [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}). A `List<String>` and a `List<Int>` are both just `List` at the JVM level. This means you cannot check `is List<String>` at runtime — the type argument is gone.

```kotlin
// Not found in FAS — standalone example
fun checkType(list: List<*>) {
    // if (list is List<String>) { }  // ERROR: Cannot check for erased type
    if (list is List<*>) { }          // OK: star-projection survives erasure
}
```

Kotlin's [`reified`]({{ "/en/glossary/reified/" | relative_url }}) type parameters in [inline functions]({{ "/en/glossary/inline-functions/" | relative_url }}) are the workaround: because the function body is inlined at the call site, the compiler substitutes the concrete type directly into the [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}), bypassing erasure.

```kotlin
// reified preserves the type parameter at runtime
inline fun <reified T> List<*>.filterIsInstanceTyped(): List<T> =
    filterIsInstance<T>()

val strings: List<String> = mixedList.filterIsInstanceTyped<String>()
```

## The Senior Nuance

- Type erasure means generic type checks (`is T`) and generic class creation (`T()`) are impossible at runtime without [reified]({{ "/en/glossary/reified/" | relative_url }}). This is why Android's `Gson().fromJson<MyType>(json)` requires a `TypeToken` — it's a workaround for erasure that captures the type at the call site.
- In Kotlin, you can check `is List<*>` (star projection) but not `is List<String>`. The `*` says "I don't care about the type argument" — it compiles to a raw type check.
- Erasure causes "bridge methods": when a class `StringList : List<String>` overrides `get(index: Int): String`, the JVM also generates a synthetic `get(index: Int): Object` bridge method that delegates to the typed version. These bridges are visible in [stack traces]({{ "/en/glossary/stack-trace/" | relative_url }}) and can confuse debugging.
- Kotlin's [reified]({{ "/en/glossary/reified/" | relative_url }}) + [inline]({{ "/en/glossary/inline-functions/" | relative_url }}) combination is the only JVM-level escape from type erasure. It works by pasting the concrete type into the call site's [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}), so the type is never actually passed as a parameter — it's hardcoded.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
