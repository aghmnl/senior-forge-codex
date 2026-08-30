---
layout: post
title: "Constructor"
date: 2026-08-30 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/constructor/
---

## The Theory (The What)

A **constructor** is a special function that initializes a new instance of a class. Kotlin distinguishes between the **primary constructor** (declared in the class header) and **secondary constructors** (declared inside the class body with `constructor`). The [primary constructor]({{ "/en/glossary/primary-constructor/" | relative_url }}) is the idiomatic Kotlin approach: its parameters can be `val`/`var` properties directly, and the `init` block runs as part of its execution.

```kotlin
// From FollowApp Suite — RecurrenceRule.kt
// Primary constructor with default values — the Kotlin-idiomatic way
data class RecurrenceRule(
    val frequency: RecurrenceFrequency,
    val interval: Int = 1,
    val weekdays: Set<DayOfWeek> = emptySet(),
    val end: RecurrenceEnd = RecurrenceEnd.Never,
    val pattern: RecurrencePattern? = null
)

// From FollowApp Suite — MyTasksDatabase.kt
// Abstract class with no explicit constructor — Room generates the implementation
abstract class MyTasksDatabase : RoomDatabase() {
    abstract fun taskDao(): TaskDao
    abstract fun labelDao(): LabelDao
    abstract fun presetDao(): PresetDao
}
```

## The Senior Nuance

- In Kotlin, the primary constructor is the default and preferred way to initialize classes. Secondary constructors exist mainly for Java interop and framework requirements (e.g., Android `View` subclasses needing multiple constructors for XML inflation).
- Constructors are the dividing line between `sealed class` and `sealed interface`: a sealed class can define a constructor (primary or secondary) with shared parameters and an `init` block, forcing subtypes to provide those values. A sealed interface has no constructor at all — each implementation is structurally independent. See [Sealed Classes vs Sealed Interfaces]({{ "/en/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}).
- `data class` constructors get special treatment: the compiler generates `copy()`, `equals()`, `hashCode()`, `toString()`, and `componentN()` from the primary constructor parameters. This is why `data class` + primary constructor is the standard pattern for immutable state objects in [MVI]({{ "/en/glossary/mvi-pattern/" | relative_url }}).
- [Abstract classes]({{ "/en/glossary/abstract-class/" | relative_url }}) can declare `abstract` constructor parameters that subtypes must provide. This is how sealed classes enforce shared state across variants — each subtype's constructor supplies the required values.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
