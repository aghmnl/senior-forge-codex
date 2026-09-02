---
layout: post
title: "@DslMarker"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/dsl-marker/
---

## The Theory (The What)

**`@DslMarker`** is a Kotlin meta-annotation that prevents implicit access to outer [receivers]({{ "/en/glossary/receiver-type/" | relative_url }}) when [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}) with receivers are nested inside a [DSL]({{ "/en/glossary/dsl/" | relative_url }}). Without it, code inside an inner lambda can accidentally call methods from outer receivers — the compiler silently resolves to the outermost match. `@DslMarker` makes this a [compile-time]({{ "/en/glossary/compile-time/" | relative_url }}) error: if you really need the outer receiver, you must write [`this@label`]({{ "/en/glossary/this-at-label/" | relative_url }}) explicitly.

You create a `@DslMarker` by annotating your own annotation with `@DslMarker`, then applying that annotation to every [receiver type]({{ "/en/glossary/receiver-type/" | relative_url }}) in your DSL. All types annotated with the same marker form a "scope group" — inside a nested lambda, only the innermost scope group member is implicitly available.

```kotlin
// Not found in FAS — standalone example
@DslMarker
annotation class HtmlDsl

@HtmlDsl
class HtmlBuilder {
    fun body(block: BodyBuilder.() -> Unit) { /* ... */ }
}

@HtmlDsl
class BodyBuilder {
    fun p(text: String) { /* ... */ }
    fun div(block: DivBuilder.() -> Unit) { /* ... */ }
}

@HtmlDsl
class DivBuilder {
    fun span(text: String) { /* ... */ }
}

fun html(block: HtmlBuilder.() -> Unit): String { /* ... */ }

// Usage — @DslMarker prevents scope leakage:
html {
    body {
        div {
            span("Hello")
            // p("World")  // ERROR: p() is on BodyBuilder, not DivBuilder
            // this@body.p("World")  // OK: explicit qualification
        }
    }
}
```

## The Senior Nuance

- **Compose's `@LayoutScopeMarker`**: [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) uses `@LayoutScopeMarker` (a `@DslMarker`) on `ColumnScope`, `RowScope`, `BoxScope`, etc. This is why `Modifier.weight()` is available inside `Column {}` but not inside a nested `Row {}` — the marker restricts each [scope]({{ "/en/glossary/scope/" | relative_url }}) to its own receiver's methods.
- **[Gradle Kotlin DSL]({{ "/en/glossary/gradle-kotlin-dsl/" | relative_url }})**: Gradle applies a similar mechanism (`@HasImplicitReceiver`) to prevent build script blocks from accidentally accessing outer [scopes]({{ "/en/glossary/scope/" | relative_url }}). The `android {}` block cannot call `dependencies {}` methods directly, even though both are nested inside the same file.
- **When to apply it**: Any time you design a [DSL]({{ "/en/glossary/dsl/" | relative_url }}) with more than one level of nesting. Without `@DslMarker`, users of your DSL will write code that compiles but does something unexpected — calling a method on the wrong receiver. This is one of the most common sources of bugs in custom Kotlin DSLs.
- **Relation to `this@label`**: `@DslMarker` does not block outer receivers entirely — it blocks *implicit* access. Explicit [`this@label`]({{ "/en/glossary/this-at-label/" | relative_url }}) still works, which means the developer must consciously opt in to cross-scope calls. This is the "pit of success" design: the safe path is the default.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
