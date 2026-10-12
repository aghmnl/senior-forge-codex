---
layout: post
title: "rememberLazyListState"
date: 2026-10-12 12:00:00 +0000
categories: [en, glossary]
tags: [compose, state-management]
lang: en
permalink: /en/glossary/remember-lazy-list-state/
---

## The Theory (The What)

**`rememberLazyListState()`** creates and remembers the `LazyListState` of a [`LazyColumn`]({{ "/en/glossary/lazy-column/" | relative_url }}) or `LazyRow`: the first visible item, its scroll offset, and functions like `scrollToItem` and `animateScrollToItem`. It is built on [`rememberSaveable`]({{ "/en/glossary/remember-saveable/" | relative_url }}), so the scroll position survives [configuration changes]({{ "/en/glossary/configuration-change/" | relative_url }}) and [process death]({{ "/en/glossary/process-death/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
val listState = rememberLazyListState()
LazyColumn(state = listState) { /* ... */ }
```

## The Senior Nuance

- **Hoist it when someone else needs it**, such as a "back to top" button or a toolbar that reacts to scroll.
- **Reading `firstVisibleItemIndex` directly recomposes on every scroll**; wrap derived values in [`derivedStateOf`]({{ "/en/glossary/derived-state/" | relative_url }}).
- See [remember & rememberSaveable]({{ "/en/03-jetpack-compose/remember-remembersaveable/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
