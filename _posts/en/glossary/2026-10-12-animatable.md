---
layout: post
title: "Animatable"
date: 2026-10-12 12:00:00 +0000
categories: [en, glossary]
tags: [compose, coroutines]
lang: en
permalink: /en/glossary/animatable/
---

## The Theory (The What)

**`Animatable`** holds a value (usually a `Float`) that can be animated from [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}): `animateTo(target)` suspends while it animates, `snapTo(value)` jumps immediately, and reading `.value` is observable, so composables recompose as it moves. It is the low-level tool for gestures and animations driven by code.

```kotlin
// Not found in FAS — standalone example
val offset = remember { Animatable(0f) }
LaunchedEffect(open) { offset.animateTo(if (open) 300f else 0f) }
```

## The Senior Nuance

- **Store it with [`remember`]({{ "/en/glossary/remember/" | relative_url }}), not [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }}).** It is animation state; after a recreation it should start again from the current UI state.
- **A new `animateTo` cancels the running one**, which makes it natural for gestures that interrupt an animation.
- See [remember & rememberSaveable]({{ "/en/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
