---
layout: post
title: "One-shot Event"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [architecture, state-management, flow]
lang: en
permalink: /en/glossary/one-shot-event/
---

## The Theory (The What)

A **one-shot event** is something the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) wants the UI to do **exactly once**: navigate, show a snackbar, open a dialog. Unlike state, it is not "how the screen looks now" but "something that happened", and handling it twice (navigating twice after a rotation) or zero times (dropping it while the screen is in the background) is a bug.

```kotlin
// Not found in FAS — standalone example
private val _events = Channel<UiEvent>(Channel.BUFFERED)
val events: Flow<UiEvent> = _events.receiveAsFlow()
```

## The Senior Nuance

- **There is no perfect primitive.** A [`SharedFlow`]({{ "/en/glossary/sharedflow/" | relative_url }}) without replay drops events with no [collector]({{ "/en/glossary/collector/" | relative_url }}); with replay it repeats them. A buffered [channel]({{ "/en/glossary/channel/" | relative_url }}) with `receiveAsFlow()` delivers later and once, but can still lose an event if the [collector]({{ "/en/glossary/collector/" | relative_url }}) is cancelled after receiving it.
- **Google prefers modeling it as state**: the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) exposes "navigate to X" in the UI state, the UI acts on it and tells the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) to clear it. That survives rotation and process death and is easy to test.
- See [receiveAsFlow()]({{ "/en/02-coroutines-flow/receive-as-flow/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
