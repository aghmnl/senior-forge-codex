---
layout: page
title: Higher-Order Functions & Lambdas
lang: en
permalink: /en/01-kotlin-core/higher-order-functions-lambdas/
order: 7
---

## The Theory (The What)

Higher-order functions (HOFs) are functions that take other functions as parameters or return them as results. In Kotlin, functions are first-class citizens — they can be stored in variables, passed into functions, or returned. [Lambdas]({{ "/en/glossary/lambdas/" | relative_url }}) are function literals: blocks of code that are not declared as traditional functions but are passed immediately as expressions.

A function type like `(Task) -> Boolean` describes a lambda that receives a `Task` and returns a `Boolean`. When a function accepts such a type as a parameter, it becomes a higher-order function. This mechanism is the foundation of Kotlin's [Collections]({{ "/en/glossary/collections/" | relative_url }}) API (`map`, `filter`, `count`), [Scope Functions]({{ "/en/01-kotlin-core/scope-functions/" | relative_url }}) (`let`, `run`, `apply`, `also`, `with`), and the declarative syntax of [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}).

Function types can also have a receiver — `T.() -> R` — meaning the lambda executes with `this` bound to the receiver object. This pattern, combined with HOFs, is the backbone of Kotlin [DSLs]({{ "/en/glossary/dsl/" | relative_url }}).

## The Senior Perspective (The Why)

A Senior Engineer evaluates higher-order functions through the lens of **abstraction versus [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) performance**.

- **Memory Overhead**: Every time a [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) is passed without being [inlined]({{ "/en/glossary/inline-functions/" | relative_url }}), the compiler creates a new instance of a `Function` class (e.g., `Function0`, `Function1`). In high-frequency operations — inside `LazyColumn` item builders or tight loops over large [Collections]({{ "/en/glossary/collections/" | relative_url }}) — this increases pressure on the [Garbage Collector]({{ "/en/glossary/garbage-collector/" | relative_url }}).
- **The [`inline`]({{ "/en/glossary/inline-functions/" | relative_url }}) Power**: Using the `inline` keyword instructs the compiler to replace the function call with the actual [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) of the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}). This eliminates object [allocations]({{ "/en/glossary/allocations/" | relative_url }}) and enables non-local returns (using `return` inside a lambda to exit the calling function). See the [Inline Functions]({{ "/en/glossary/inline-functions/" | relative_url }}) glossary entry for the full mechanics.
- **Control over Inlining**: [`crossinline`]({{ "/en/glossary/crossinline/" | relative_url }}) prevents non-local returns when the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) escapes to another execution context (a local object or a different thread). [`noinline`]({{ "/en/glossary/noinline/" | relative_url }}) keeps a specific lambda as an object when you need to store it or pass it further.
- **[Callback]({{ "/en/glossary/callbacks/" | relative_url }}) Consolidation**: In large screens, grouping related [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) [callbacks]({{ "/en/glossary/callbacks/" | relative_url }}) into a dedicated class prevents parameter-list explosion in Composable functions — each [callback]({{ "/en/glossary/callbacks/" | relative_url }}) is still a higher-order function type, but the screen signature stays clean.
- **Declarative DSLs**: HOFs combined with function types with [receivers]({{ "/en/glossary/receiver-type/" | relative_url }}) are the foundation of modern Android development, enabling the declarative [DSL]({{ "/en/glossary/dsl/" | relative_url }}) syntax seen in [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) and [Hilt]({{ "/en/glossary/hilt/" | relative_url }}) configurations.

## Code in Action

### HOF with a transform lambda — optimistic UI updates

A private function that takes a `(Task) -> Task` [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) to apply a transformation to selected tasks in memory, so the UI reacts instantly without waiting for the database [round-trip]({{ "/en/glossary/round-trip/" | relative_url }}).

```kotlin
// From FollowApp Suite — TasksViewModel.kt
private fun updateSelectedTasksOptimistically(transform: (Task) -> Task) {
    _uiState.update { state ->
        val tasks = state.activeTasks.map { task ->
            if (task.id in state.selectedTaskIds) transform(task) else task
        }
        val groups = state.groupBy?.let { computeTaskGroups(tasks, it) } ?: emptyList()
        state.copy(activeTasks = tasks, taskGroups = groups)
    }
}
```

### HOF with a predicate lambda — tri-state bulk selection

A function that accepts a `(Task) -> Boolean` predicate to compute whether a chip in the bulk sheet should be FULL, OUTLINE, or PARTIAL based on the current selection.

```kotlin
// From FollowApp Suite — BulkSelection.kt
private fun triState(tasks: List<Task>, predicate: (Task) -> Boolean): BulkChipState {
    if (tasks.isEmpty()) return BulkChipState.OUTLINE
    val count = tasks.count(predicate)
    return when (count) {
        0 -> BulkChipState.OUTLINE
        tasks.size -> BulkChipState.FULL
        else -> BulkChipState.PARTIAL
    }
}

internal fun bulkTagState(tasks: List<Task>, tag: String): BulkChipState =
    triState(tasks) { task ->
        tag in ((task.customLabels["labels"] as? LabelValue.Tag)?.values ?: emptyList())
    }
```

### Generic HOF with extension + transform — JSON deserialization

A [generic]({{ "/en/01-kotlin-core/generics-variance-reification/" | relative_url }}) [extension function]({{ "/en/01-kotlin-core/extension-functions/" | relative_url }}) that takes a `(JSONObject) -> T` transform to convert a `JSONArray` into a typed `List<T>`.

```kotlin
// From FollowApp Suite — BackupSerializer.kt
private fun <T> JSONArray.mapObjects(transform: (JSONObject) -> T): List<T> =
    (0 until length()).map { transform(getJSONObject(it)) }
```

### Callback consolidation — taming Composable parameter lists

When a screen requires dozens of [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) [callbacks]({{ "/en/glossary/callbacks/" | relative_url }}), grouping them into a class prevents signature explosion while keeping each [callback]({{ "/en/glossary/callbacks/" | relative_url }}) as a first-class function type.

```kotlin
// From FollowApp Suite — TasksCallbacks.kt
class TaskFormCallbacks(
    val onFormTitleChange: (String) -> Unit,
    val onFormDescriptionChange: (String) -> Unit,
    val onFormCompletedChange: (Boolean) -> Unit,
    val onFormDueDateChange: (Long?) -> Unit,
    val onFormConfirmed: () -> Unit,
    val onFormDismissed: () -> Unit,
    val onFormRecurrenceChange: (RecurrenceRule?) -> Unit,
    val onAddSubtask: (String) -> Unit,
)
```

## The Interview (The Hot Seat)

**Question**: Why would you avoid using the [`inline`]({{ "/en/glossary/inline-functions/" | relative_url }}) keyword for every single higher-order function in a large project?

**Senior Answer**: While [`inline`]({{ "/en/glossary/inline-functions/" | relative_url }}) prevents object [allocation]({{ "/en/glossary/allocations/" | relative_url }}), it causes the compiler to copy the function's [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) into every call site. If the function body is large and called in many places, it produces [code bloat]({{ "/en/glossary/code-bloat/" | relative_url }}), significantly increasing the final binary size (APK/AAB). Additionally, [inline functions]({{ "/en/glossary/inline-functions/" | relative_url }}) cannot access `private` members of the class they are in (and parameters marked [`crossinline`]({{ "/en/glossary/crossinline/" | relative_url }}) or [`noinline`]({{ "/en/glossary/noinline/" | relative_url }}) add further constraints), which can limit architectural choices. I only [inline]({{ "/en/glossary/inline-functions/" | relative_url }}) functions that take [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}) as parameters and whose body is small enough to justify the trade-off — typically utility functions like `onSuccess`, `runCatching`, or custom [scope functions]({{ "/en/01-kotlin-core/scope-functions/" | relative_url }}).

---

[Back to Chapters]({{ "/" | relative_url }})
