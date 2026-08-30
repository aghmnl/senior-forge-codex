---
layout: post
title: "Abstract Class"
date: 2026-08-30 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/abstract-class/
---

## The Theory (The What)

An **abstract class** is a class that cannot be instantiated directly — it exists to be subclassed. It can declare `abstract` members (properties and functions without a body) that every subtype must implement, and it can provide concrete members (default implementations, shared state, `init` blocks) that subtypes inherit. In Kotlin, `sealed class` is a specialized abstract class that additionally restricts which classes can extend it to those in the same package and module.

```kotlin
// From FollowApp Suite — TasksUiState.kt
// CascadeAction is a sealed (abstract) class:
// abstract properties enforce shared state across all variants
sealed class CascadeAction {
    abstract val taskId: String
    abstract val childCount: Int

    data class Complete(
        override val taskId: String,
        val isCompleted: Boolean,
        override val childCount: Int
    ) : CascadeAction()

    data class Delete(
        override val taskId: String,
        override val childCount: Int
    ) : CascadeAction()
}

// From FollowApp Suite — MyTasksDatabase.kt
// Room requires an abstract class — it generates the implementation at compile time
abstract class MyTasksDatabase : RoomDatabase() {
    abstract fun taskDao(): TaskDao
    abstract fun labelDao(): LabelDao
    abstract fun presetDao(): PresetDao
}
```

## The Senior Nuance

- Abstract class vs interface: an abstract class can hold state (properties with backing fields), [constructors]({{ "/en/glossary/constructor/" | relative_url }}), and `init` blocks. An interface cannot hold state — only abstract or default-implemented functions and abstract properties (no backing fields). Use an abstract class when subtypes need shared internal state; use an interface when you only need a contract.
- Abstract class vs sealed class: both are abstract, but a sealed class restricts subtyping to a closed set (same package and module), enabling exhaustive `when`. A regular abstract class allows anyone, anywhere, to extend it. For [algebraic data types (ADTs)]({{ "/en/glossary/algebraic-data-types/" | relative_url }}), always prefer sealed hierarchies — they give you the compiler-enforced exhaustiveness that a regular abstract class cannot.
- In Android, abstract classes are common in framework APIs: `RoomDatabase`, `ViewModel`, `BroadcastReceiver`, `View`. These are not design choices you make — they are framework requirements. In your own domain code, prefer composition over [inheritance]({{ "/en/glossary/inheritance/" | relative_url }}): inject dependencies rather than inheriting shared behavior from a base class.
- A class can extend only **one** abstract class but implement **multiple** interfaces. This single-[inheritance]({{ "/en/glossary/inheritance/" | relative_url }}) constraint is why `sealed interface` is preferred over `sealed class` when no shared state is needed.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
