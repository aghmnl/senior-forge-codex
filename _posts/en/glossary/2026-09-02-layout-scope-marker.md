---
layout: post
title: "@LayoutScopeMarker"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/layout-scope-marker/
---

## The Theory (The What)

**`@LayoutScopeMarker`** is [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }})'s application of [`@DslMarker`]({{ "/en/glossary/dsl-marker/" | relative_url }}) to layout scopes. It annotates `ColumnScope`, `RowScope`, `BoxScope`, and other layout scope interfaces. The effect: inside a [lambda with receiver]({{ "/en/glossary/lambda-with-receiver/" | relative_url }}) scoped to one layout, you cannot accidentally call members from an outer layout's [scope]({{ "/en/glossary/scope/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
Column {
    Text("Inside ColumnScope")
    Row {
        Text("Inside RowScope")
        // Modifier.weight() is ColumnScope-only — this would NOT compile:
        // Text(modifier = Modifier.weight(1f), text = "Wrong scope")

        // Must qualify if you truly need the outer scope:
        // this@Column.run { Modifier.weight(1f) }
    }
}
```

Without `@LayoutScopeMarker`, the inner `Row` lambda could see `ColumnScope`'s `weight()` through implicit receiver resolution — a silent, hard-to-spot bug. The marker restricts each [receiver type]({{ "/en/glossary/receiver-type/" | relative_url }}) to its own scope boundary.

## The Senior Nuance

- `@LayoutScopeMarker` is defined as `@DslMarker annotation class LayoutScopeMarker` — it's a one-line annotation that inherits all behavior from the [`@DslMarker`]({{ "/en/glossary/dsl-marker/" | relative_url }}) meta-annotation. Any two scope interfaces that share the same `@DslMarker` annotation cannot be implicitly combined in nested lambdas.
- This is a [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) constraint, not a [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) check. The compiler refuses to resolve members from outer receivers marked with the same `@DslMarker`, forcing [`this@label`]({{ "/en/glossary/this-at-label/" | relative_url }}) or an explicit variable to cross scope boundaries.
- In practice, `@LayoutScopeMarker` prevents one of the most common Compose mistakes: calling `Modifier.weight()` (a `ColumnScope`/`RowScope` extension) from the wrong parent. In XML layouts this kind of mismatch was a silent runtime error; in Compose it's a compilation error.
- When writing your own Compose layout with a custom scope, apply `@LayoutScopeMarker` (not a new `@DslMarker`) so that your scope participates in the same safety boundary as the built-in layouts — a `Column` inside your custom layout still can't leak `ColumnScope` into your scope.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
