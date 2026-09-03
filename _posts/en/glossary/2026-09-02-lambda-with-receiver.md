---
layout: post
title: "Lambda with Receiver"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/lambda-with-receiver/
---

## The Theory (The What)

A **lambda with receiver** is a [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) whose body executes in the [scope]({{ "/en/glossary/scope/" | relative_url }}) of a [receiver type]({{ "/en/glossary/receiver-type/" | relative_url }}). Its signature is `T.() -> R` — inside the lambda, `this` refers to the receiver instance of type `T`, so you can call its members without qualification. This is the core mechanism behind Kotlin [DSLs]({{ "/en/glossary/dsl/" | relative_url }}), [scope functions]({{ "/en/01-kotlin-core/scope-functions/" | relative_url }}) (`apply`, `run`, `with`), and builder APIs.

```kotlin
// From FollowApp Suite — BackupSerializer.kt
// apply {} is a lambda with receiver: 'this' is the JSONObject
private fun taskToJson(task: TaskEntity): JSONObject = JSONObject().apply {
    put("id", task.id)
    put("title", task.title)
    put("description", task.description)
    put("parentTaskId", task.parentTaskId)
    put("status", task.status)
    put("isCompleted", task.isCompleted)
}
```

```kotlin
// From FollowApp Suite — TasksNavDrawer.kt
// ColumnScope.() -> Unit — Compose's scoped lambda with receiver
@Composable
private fun DropUpMenu(
    expanded: Boolean,
    onDismissRequest: () -> Unit,
    content: @Composable ColumnScope.() -> Unit  // lambda with receiver
) {
    // inside 'content', 'this' is ColumnScope — weight(), align() are available
}
```

The difference between a regular lambda (`(T) -> R`) and a lambda with receiver (`T.() -> R`) is syntactic, not semantic: both receive an argument of type `T`, but the receiver version exposes it as `this` instead of as a named parameter. The compiler desugars `T.() -> R` to `Function1<T, R>` in [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}).

## The Senior Nuance

- [Scope functions]({{ "/en/01-kotlin-core/scope-functions/" | relative_url }}) split into two families based on this: `apply`/`run`/`with` use a lambda with receiver (`this`), while `let`/`also` use a regular lambda (`it`). Choosing between them signals intent — [intent signaling]({{ "/en/glossary/intent-signaling/" | relative_url }}).
- When nesting lambdas with receiver (e.g., `Column { Row { ... } }` in [Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }})), the innermost receiver shadows the outer ones. Use [`this@label`]({{ "/en/glossary/this-at-label/" | relative_url }}) to access an outer receiver explicitly: `this@Column.align(...)`.
- [`@DslMarker`]({{ "/en/glossary/dsl-marker/" | relative_url }}) and [`@LayoutScopeMarker`]({{ "/en/glossary/layout-scope-marker/" | relative_url }}) prevent accidental scope leakage in nested lambdas with receiver. Without them, inner lambdas can silently call methods from outer receivers — a subtle source of bugs.
- Lambdas with receiver are the foundation of type-safe builders: `buildList {}` (receiver: `MutableList<T>`), `buildString {}` (receiver: `StringBuilder`), `buildMap {}` (receiver: `MutableMap<K, V>`). The receiver constrains what operations are valid, so the compiler catches misuse instead of the developer.
- [Higher-order functions]({{ "/en/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) that accept lambdas with receiver are typically marked [`inline`]({{ "/en/glossary/inline-functions/" | relative_url }}), eliminating the [allocation]({{ "/en/glossary/allocations/" | relative_url }}) overhead of the lambda object entirely.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
