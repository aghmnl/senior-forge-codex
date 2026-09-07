---
layout: post
title: "Return Type"
date: 2026-09-07 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/return-type/
---

## The Theory (The What)

The **return type** is the type of the value a function hands back to its caller. In Kotlin it is written after the parameter list (`fun size(): Int`), or inferred when the function uses expression-body syntax (`fun size() = items.count()`). A function that returns nothing meaningful has the return type `Unit`, which is a real type with a single instance — not Java's `void`.

```kotlin
// From FollowApp Suite — BackupSerializer.kt
// Return type List<T>: T appears in an "out" position.
private fun <T> JSONArray.mapObjects(transform: (JSONObject) -> T): List<T> =
    (0 until length()).map { transform(getJSONObject(it)) }
```

In the [variance]({{ "/en/glossary/variance/" | relative_url }}) rules, the return type is the canonical **out position**: it is where a type is *produced* and handed outward.

## The Senior Nuance

- **Return type = out position.** A [generic type parameter]({{ "/en/glossary/generic-type-parameters/" | relative_url }}) may be declared [covariant]({{ "/en/glossary/covariance/" | relative_url }}) (`out T`) only if it appears exclusively in return types. The moment it also appears as a parameter, the class must stay [invariant]({{ "/en/glossary/invariance/" | relative_url }}). This positional rule is the whole of PECS, restated precisely.
- **Return types are covariant under overriding.** An override may narrow the return type — if the base declares `fun load(): Task`, an override may return `CompletedTask`. It may *not* narrow a parameter type, for the mirror-image reason: parameters are in positions.
- **Explicit return types on public API.** Expression bodies infer the return type, which is convenient internally but brittle across module boundaries: changing an implementation detail can silently change a published signature and break binary compatibility. A Senior writes the return type explicitly on anything public.
- **`Nothing` is the bottom type.** A function that always throws has return type `Nothing`, which is a subtype of every type. This is what lets `val x: String = value ?: throw IllegalStateException()` typecheck — the `throw` branch conforms to `String` because `Nothing` conforms to everything.
- **Return type drives [Type Inference]({{ "/en/glossary/type-inference/" | relative_url }}).** In `mapObjects(::taskFromJson)`, `T` is inferred from the *return* type of the function reference, not from any argument. Generic inference flows backwards through return types as readily as forwards through parameters.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
