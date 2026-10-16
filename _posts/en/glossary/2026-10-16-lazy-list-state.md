---
layout: post
title: "LazyListState"
date: 2026-10-16 12:00:00 +0000
categories: [en, glossary]
tags: [compose, state-management]
lang: en
permalink: /en/glossary/lazy-list-state/
---

## The Theory (The What)

**`LazyListState`** is the [state holder]({{ "/en/glossary/state-holder/" | relative_url }}) of a [`LazyColumn`]({{ "/en/glossary/lazy-column/" | relative_url }}) or `LazyRow`: it knows the first visible item, its scroll offset and whether the list is scrolling, and it exposes `scrollToItem` and `animateScrollToItem`. It is created with `rememberLazyListState()` and passed to the list through its `state` parameter, which is state hoisting for the list's UI logic.

## The Senior Nuance

- **It is the model of a plain [state holder]({{ "/en/glossary/state-holder/" | relative_url }}) class**: UI logic complex enough to deserve its own class, created and remembered by a `rememberXState()` function.
- **Hoist it only as high as needed**, for example to the screen that also shows a "back to top" button.
- See [State Hoisting]({{ "/en/03-jetpack-compose/state-hoisting/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
