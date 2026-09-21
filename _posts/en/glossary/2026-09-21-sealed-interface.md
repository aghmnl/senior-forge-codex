---
layout: post
title: "sealed interface"
date: 2026-09-21 12:00:00 +0000
categories: [en, glossary]
tags: [sealed-types, oop, architecture]
lang: en
permalink: /en/glossary/sealed-interface/
---

## The Theory (The What)

**`sealed interface`** (Kotlin 1.5+) declares a [sealed hierarchy]({{ "/en/glossary/sealed-hierarchy/" | relative_url }}) as an interface: the set of implementations is closed to the same package and module, so a [`when`]({{ "/en/glossary/when-expression/" | relative_url }}) over it is exhaustive without an `else`. Unlike a [`sealed class`]({{ "/en/glossary/sealed-class/" | relative_url }}) it has no constructor, no [`init`]({{ "/en/glossary/init/" | relative_url }}) block and no state — but a type can implement **several** sealed interfaces at once, which single inheritance makes impossible for classes. That is why it is the better default for UI state, navigation events and domain actions.

```kotlin
// From FollowApp Suite — StateChip.kt
// No shared state: each implementation defines its own colours and behaviour,
// and is free to implement other interfaces as well
sealed interface ChipState {
    val foreground: Color @Composable get
    val strikethrough: Boolean get() = false
    @Composable fun filterColors(): SelectableChipColors
}
```

## The Senior Nuance

- **Default to it; escalate to a [`sealed class`]({{ "/en/glossary/sealed-class/" | relative_url }}) only for shared state.** Most hierarchies are just a closed set of independent shapes, and starting with an interface keeps the door open for a second contract later.
- **It can still carry behaviour, just not state.** Default implementations (`val strikethrough: Boolean get() = false`) are allowed; backing fields are not.
- **Multiple membership is the feature.** A type can be both a `UiState` and an `Analytics` event; with sealed classes you would have to pick one hierarchy and bolt the rest on.
- See [Sealed Classes vs Sealed Interfaces]({{ "/en/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
