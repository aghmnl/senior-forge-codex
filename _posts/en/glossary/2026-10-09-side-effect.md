---
layout: post
title: "SideEffect"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [compose, lifecycle]
lang: en
permalink: /en/glossary/side-effect/
---

## The Theory (The What)

**`SideEffect { }`** runs its block **after every successful [recomposition]({{ "/en/glossary/recomposition/" | relative_url }})**, once the changes have been applied. It is the way to publish Compose state to code that is not managed by Compose, such as an analytics object or a view from another framework. A side effect written directly in a composable's body, by contrast, can run during a [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}) that is later discarded.

```kotlin
// Not found in FAS — standalone example
SideEffect { analytics.setUserProperty("theme", theme.name) }
```

## The Senior Nuance

- **It runs on every [recomposition]({{ "/en/glossary/recomposition/" | relative_url }})**, so it fits idempotent updates ("[set]({{ "/en/glossary/sets/" | relative_url }}) this value"), not one-time actions. For "once when shown", use `LaunchedEffect(Unit)`.
- **It never runs for a discarded [recomposition]({{ "/en/glossary/recomposition/" | relative_url }})**, which is exactly why it is safer than writing the call in the body.
- See [Recomposition & Stability]({{ "/en/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
