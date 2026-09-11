---
layout: post
title: "Property Delegate"
date: 2026-09-04 12:00:00 +0000
categories: [en, glossary]
tags: [delegation, syntax, memory]
lang: en
permalink: /en/glossary/property-delegate/
---

## The Theory (The What)

A **property delegate** (also called a delegate class) is any object that handles the `get` and/or `set` logic of a property on behalf of its owner. In Kotlin, a property delegate is connected to its property via the [`by`]({{ "/en/glossary/by-delegation/" | relative_url }}) [keyword]({{ "/en/glossary/keyword/" | relative_url }}):

```kotlin
val name: String by MyDelegate()
```

The delegate must provide `operator fun getValue(thisRef: T, property: KProperty<*>): R`. For mutable properties, it must also provide `operator fun setValue(thisRef: T, property: KProperty<*>, value: R)`. Kotlin's [standard library]({{ "/en/glossary/standard-library/" | relative_url }}) provides the `ReadOnlyProperty<T, R>` and `ReadWriteProperty<T, R>` interfaces for [type safety]({{ "/en/glossary/type-safety/" | relative_url }}), but implementing them is optional — the convention is structural, resolved via [operator overloading]({{ "/en/glossary/operator-overloading/" | relative_url }}).

Built-in property delegates include `lazy`, `Delegates.observable`, `Delegates.vetoable`, and `Delegates.notNull`. The Android ecosystem adds `viewModels()`, `activityViewModels()`, and Compose's `mutableStateOf()`. See [Delegated Properties]({{ "/en/01-kotlin-core/delegated-properties/" | relative_url }}) for the full treatment.

## The Senior Nuance

- A Senior designs custom property delegates to encapsulate cross-cutting concerns: logging every property access, synchronizing reads with a lock, reading from SharedPreferences with automatic key derivation via [KProperty]({{ "/en/glossary/kproperty/" | relative_url }}).`name`, or validating values before storage.
- The `provideDelegate` operator allows the delegate to customize itself at installation time — for instance, verifying that the property name matches an expected configuration key. This is the difference between a generic delegate and one that is aware of its installation context.
- Property delegates are objects that live on the [heap]({{ "/en/glossary/heap/" | relative_url }}). Each `by` declaration creates one delegate instance per property. A Senior is mindful of this [overhead]({{ "/en/glossary/overhead/" | relative_url }}) in classes with many delegated properties instantiated in tight loops.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
