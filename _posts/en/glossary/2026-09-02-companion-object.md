---
layout: post
title: "Companion Object"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/companion-object/
---

## The Theory (The What)

A **companion object** is Kotlin's replacement for Java's `static` members. It is a [singleton]({{ "/en/glossary/singleton/" | relative_url }}) object declared inside a class using `companion object { ... }`. Its members can be accessed via the class name without creating an instance — `MyClass.MY_CONSTANT` — making it the standard place for constants, factory methods, and shared utility functions.

Unlike Java's `static`, a companion object is a real object: it has a class, can implement interfaces, and can be passed around. At the [JVM]({{ "/en/glossary/jvm/" | relative_url }}) level, the companion's members live on a nested `Companion` class, and accessing them involves an extra indirection through the companion instance — unless annotated with [`@JvmStatic`]({{ "/en/glossary/jvm-static/" | relative_url }}).

```kotlin
// From FollowApp Suite — RecurrencePattern in RecurrenceRule.kt
sealed class RecurrencePattern {
    data class DayOfMonth(val day: Int) : RecurrencePattern()
    data class NthWeekday(val ordinal: Int, val day: DayOfWeek) : RecurrencePattern()
    data class NthBusinessDay(val ordinal: Int) : RecurrencePattern()

    companion object {
        const val LAST = -1
    }
}
```

```kotlin
// From FollowApp Suite — LegacyTaskReader.kt
class LegacyTaskReader(private val context: Context) {

    companion object {
        const val LEGACY_DB_NAME = "TaskDatabase"
        private const val LEGACY_TABLE = "TasksTable"
        private const val TAG = "LegacyTaskReader"
    }
}
```

```kotlin
// From FollowApp Suite — TasksViewPreferences.kt
companion object {
    const val UNSAVED_PRESET_KEY = "none"

    private val keySortOrder = stringPreferencesKey("tasks_view_sort_order")
    private val keyGroupBy = stringPreferencesKey("tasks_view_group_by")
    private val keyDoneFilter = stringPreferencesKey("tasks_view_done_filter")
}
```

## The Senior Nuance

- **Constants go here**: `const val` inside a companion object compiles to a true JVM `static final` field — zero overhead, no companion instance involved. Regular `val` properties in the companion still go through the companion object's getter.
- **Factory pattern**: Companion objects are the idiomatic place for factory methods (`MyClass.from(...)`, `MyClass.create(...)`) because they can access the class's `private` [constructor]({{ "/en/glossary/constructor/" | relative_url }}). This is more expressive than overloaded constructors.
- **Interface implementation**: A companion object can implement an interface (`companion object : Serializer<MyClass>`), which is useful for providing a default serializer or a type-safe factory that can be referenced as `MyClass` itself.
- **DataStore keys pattern**: In FollowApp Suite, `companion object` is the canonical place for DataStore `PreferencesKey` declarations — keeping them colocated with the class that reads/writes them while making them accessible without an instance.
- **[Static dispatch]({{ "/en/glossary/static-dispatch/" | relative_url }})**: Companion object functions use [static dispatch]({{ "/en/glossary/static-dispatch/" | relative_url }}) — the call is resolved at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}), no [vtable]({{ "/en/glossary/vtable/" | relative_url }}) lookup. Adding [`@JvmStatic`]({{ "/en/glossary/jvm-static/" | relative_url }}) makes the JVM bytecode a true static method, which matters for Java interop and framework reflection.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
