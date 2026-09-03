---
layout: post
title: "this@label"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/this-at-label/
---

## The Theory (The What)

**`this@label`** is Kotlin's qualified `this` syntax for disambiguating which [receiver]({{ "/en/glossary/receiver-type/" | relative_url }}) you are referring to when multiple receivers are in [scope]({{ "/en/glossary/scope/" | relative_url }}). When [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}) with receivers are nested — a common occurrence in [DSLs]({{ "/en/glossary/dsl/" | relative_url }}) like [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) — the innermost receiver shadows the outer ones. Writing `this@outerLabel` explicitly selects the outer receiver.

The label is the name of the function or class that introduced the receiver. For an [extension function]({{ "/en/glossary/extension-functions/" | relative_url }}) like `drawWithContent {}`, the label is `drawWithContent`. For a class method, the label is the class name.

```kotlin
// From FollowApp Suite — AnimatedSearchBar.kt
.drawWithContent {
    val reveal = size.width * searchFraction
    clipRect(
        left = size.width - reveal,
        top = 0f,
        right = size.width,
        bottom = size.height
    ) {
        // Inside clipRect {}, 'this' is ClipScope.
        // We need to call drawContent() on the outer DrawScope.
        this@drawWithContent.drawContent()
    }
}
```

Without `this@drawWithContent`, the compiler would look for `drawContent()` on the `ClipScope` receiver (the innermost lambda) and fail — `drawContent()` belongs to the outer `ContentDrawScope`.

## The Senior Nuance

- **When to use it**: Whenever you nest [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}) with different [receiver types]({{ "/en/glossary/receiver-type/" | relative_url }}) and need a method from an outer layer. This is common in Compose's drawing APIs (`drawWithContent`, `drawBehind` + `clipRect`), Canvas scoping, and custom [DSLs]({{ "/en/glossary/dsl/" | relative_url }}).
- **Relation to `@DslMarker`**: [`@DslMarker`]({{ "/en/glossary/dsl-marker/" | relative_url }}) prevents *implicit* access to outer receivers — the compiler forces you to write `this@label` explicitly if you really need it. Without `@DslMarker`, the outer receiver is silently accessible, which leads to subtle bugs in nested [DSLs]({{ "/en/glossary/dsl/" | relative_url }}).
- **Non-local returns**: In a nested lambda context, `return@label` uses the same label mechanism but for control flow rather than receiver disambiguation. Both features share the labeling convention, but `this@label` selects a receiver while `return@label` exits a specific lambda.
- **Readability rule**: If you find yourself writing `this@label` frequently, the nesting is too deep. Extract the inner block into a named function to flatten the receiver stack.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
