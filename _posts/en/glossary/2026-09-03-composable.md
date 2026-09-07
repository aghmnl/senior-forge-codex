---
layout: post
title: "@Composable"
date: 2026-09-03 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/composable/
---

## The Theory (The What)

**`@Composable`** is the annotation that marks a function as part of [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }})'s declarative UI system. A `@Composable` function describes a piece of UI; it does not return a view — instead, it emits UI nodes into Compose's slot table during composition.

```kotlin
@Composable
fun Greeting(name: String) {
    Text("Hello, $name!")
}
```

The Compose compiler plugin transforms `@Composable` functions at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}): it injects a hidden `Composer` parameter and wraps the body in group/slot management calls. This transformation enables Compose's **recomposition** — the ability to re-execute only the parts of the UI tree that need updating when state changes.

`@Composable` functions can only be called from other `@Composable` functions. This restriction is enforced by the compiler, not the [Runtime]({{ "/en/glossary/runtime/" | relative_url }}), creating a separate "composable world" that cannot be entered from regular code except through composition entry points like `setContent {}`.

## The Senior Nuance

- A Senior understands that `@Composable` is not just an annotation — the compiler plugin gives it the weight of a [keyword]({{ "/en/glossary/keyword/" | relative_url }}). It changes the function's [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) signature (adding the `Composer` parameter), making `@Composable` functions binary-incompatible with their non-composable signatures.
- Composable functions must be **idempotent** and **side-effect free**: given the same inputs, they should emit the same UI. Side effects (network calls, database reads, logging) belong in `LaunchedEffect`, `SideEffect`, or `DisposableEffect` blocks, which are lifecycle-aware wrappers that Compose manages.
- When using [delegated properties]({{ "/en/01-kotlin-core/delegated-properties/" | relative_url }}) like `by remember { mutableStateOf() }` inside a `@Composable`, the `remember` call anchors the state to the composable's position in the slot table. Moving the composable in the tree (e.g., conditional rendering) can reset this state — a subtlety that [`key()`]({{ "/en/glossary/jetpack-compose/" | relative_url }}) addresses.
- `@Composable` lambdas — like the `content` parameter of `Column { ... }` — carry the same compiler transformation. This is why you cannot pass a `@Composable` [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) where a regular `() -> Unit` is expected.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
