---
layout: page
title: Scope Functions
lang: en
permalink: /en/01-kotlin-core/scope-functions/
order: 8
---

## The Theory (The What)

[Scope]({{ "/en/glossary/scope/" | relative_url }}) functions (`let`, `run`, `with`, `apply`, and `also`) execute a block of code within the [context]({{ "/en/glossary/context-programming/" | relative_url }}) of an object. They are [higher-order functions]({{ "/en/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) built into the Kotlin standard library. Their primary distinction lies in two factors:

- **How the context object is referenced**: as `this` (implicit [receiver]({{ "/en/glossary/receiver-type/" | relative_url }})) or as `it` ([lambda]({{ "/en/glossary/lambdas/" | relative_url }}) argument).
- **What the function returns**: the context object itself, or the result of the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}).

These functions do not introduce new technical capabilities but provide a concise way to manage object state and [transformations]({{ "/en/glossary/data-transformation/" | relative_url }}) within a temporary [scope]({{ "/en/glossary/scope/" | relative_url }}).

### Quick Reference

| Function | Object ref | Returns        | Typical use                          |
|----------|-----------|----------------|--------------------------------------|
| `let`    | `it`      | Lambda result  | [Null-safe]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}) chains, transformations |
| `run`    | `this`    | Lambda result  | Scoped computation, initialization   |
| `with`   | `this`    | Lambda result  | Multiple operations on same object   |
| `apply`  | `this`    | Context object | Object configuration, builder setup  |
| `also`   | `it`      | Context object | Side effects (logging, caching)      |

## The Senior Perspective (The Why)

A Senior Developer views [scope]({{ "/en/glossary/scope/" | relative_url }}) functions as tools for [intent signaling]({{ "/en/glossary/intent-signaling/" | relative_url }}) rather than just [syntactic sugar]({{ "/en/glossary/syntax-sugar/" | relative_url }}). Choosing the wrong function is a common code smell that degrades maintainability.

- **Intent Clarity**: Each [scope]({{ "/en/glossary/scope/" | relative_url }}) function communicates a different purpose. Using `apply` signals "I am configuring this object"; using `let` signals "I am transforming this value". Picking the right one makes the code self-documenting.
- **Avoiding Nested Scopes**: Nesting multiple [scope]({{ "/en/glossary/scope/" | relative_url }}) functions is a significant anti-pattern. It obscures the context of `this` or `it`, making the code prone to logic errors and reducing readability. When you find yourself nesting, extract the inner block into a named function.
- **Side Effects vs. Transformations**: Use `also` specifically for side effects (like logging or caching) that do not alter the object's primary flow, ensuring a clear separation of concerns. This is the scope function equivalent of the [Single Responsibility Principle]({{ "/en/glossary/single-responsibility-principle/" | relative_url }}).
- **Performance**: All five [scope]({{ "/en/glossary/scope/" | relative_url }}) functions are declared as [inline]({{ "/en/glossary/inline-functions/" | relative_url }}) in the standard library, which means the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) is inlined at the call site — zero object [allocation]({{ "/en/glossary/allocations/" | relative_url }}) overhead, zero [Garbage Collector]({{ "/en/glossary/garbage-collector/" | relative_url }}) pressure. Use them freely in hot paths.

## Code in Action

### `apply` — Object configuration

Returns the context object after configuring it. Ideal for builders, Intents, and serialization.

```kotlin
// From FollowApp Suite — BackupSerializer.kt
private fun taskToJson(task: TaskEntity): JSONObject = JSONObject().apply {
    put("id", task.id)
    put("title", task.title)
    put("description", task.description)
    put("status", task.status)
    put("isCompleted", task.isCompleted)
    put("dueDate", task.dueDate)
    put("createdAt", task.createdAt)
    put("updatedAt", task.updatedAt)
}
```

### `also` — Side effects without altering the flow

Returns the context object. The block performs a side effect (caching, logging) while the object passes through unchanged.

```kotlin
// From FollowApp Suite — AppIcons.kt
private var _mountainFlag: ImageVector? = null

val MountainFlag: ImageVector
    get() = _mountainFlag ?: SvgToImageVector.createImageVectorFromSvg(
        AppSvgs.MountainFlag
    ).also { _mountainFlag = it }
```

### `let` — Null-safe transformation

Returns the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) result. The context object is available as `it` (or a named parameter), which makes it ideal for nullable chains using the [safe call]({{ "/en/glossary/safe-call/" | relative_url }}) operator `?.`.

```kotlin
// From FollowApp Suite — DatePickerField.kt
val dateText = dueDate?.let { date ->
    Instant.ofEpochMilli(date)
        .atZone(ZoneId.systemDefault())
        .format(formatter)
}
```

### `with` — Multiple operations using a shared receiver

Returns the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) result. Unlike the others, `with` takes the context object as an argument, not as a [receiver]({{ "/en/glossary/receiver-type/" | relative_url }}).

```kotlin
// From FollowApp Suite — TaskFormSheet.kt
val density = LocalDensity.current
val screenHeightPx = with(density) { LocalConfiguration.current.screenHeightDp.dp.toPx() }
val peekHeightPx = with(density) { PeekHeight.toPx() }
```

### `run` — Scoped computation that returns a result

Like `with`, but called on the object directly. Useful when you need `this` access and want to return a computed value.

```kotlin
val displayLabel = notification.run {
    if (title.isBlank()) body.take(50)
    else "$title: ${body.take(30)}"
}
```

## The Interview (The Hot Seat)

**Question**: When would you strictly prefer `run` over `let`, and what is the risk of using `apply` for data [transformations]({{ "/en/glossary/data-transformation/" | relative_url }})?

**Senior Answer**: I prefer `run` over `let` when the operation requires accessing the object's members directly via `this` instead of the argument `it`, which is cleaner for complex initializations that return a result. The risk of using `apply` for [transformations]({{ "/en/glossary/data-transformation/" | relative_url }}) is that it always returns the context object itself regardless of the [lambda]({{ "/en/glossary/lambdas/" | relative_url }})'s logic; if the intent was to transform the object into a different type or value, `apply` will silently ignore that result, leading to subtle bugs where the original object flows downstream instead of the transformed value. The [intent signaling]({{ "/en/glossary/intent-signaling/" | relative_url }}) rule is simple: `apply` configures, `run`/`let` transform.

---

[Back to Chapters]({{ "/" | relative_url }})
