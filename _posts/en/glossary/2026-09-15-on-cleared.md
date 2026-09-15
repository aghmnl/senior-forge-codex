---
layout: post
title: "onCleared"
date: 2026-09-15 12:00:00 +0000
categories: [en, glossary]
tags: [lifecycle, android-framework, coroutines]
lang: en
permalink: /en/glossary/on-cleared/
---

## The Theory (The What)

**`onCleared()`** is the `ViewModel` callback invoked once, when the [`ViewModelStore`]({{ "/en/glossary/viewmodel-store/" | relative_url }}) that owns it is cleared — the Activity finishes for good, or the navigation destination leaves the [back stack]({{ "/en/glossary/back-stack/" | relative_url }}). It is the ViewModel's only [lifecycle]({{ "/en/glossary/lifecycle/" | relative_url }}) hook, and the moment [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) is cancelled: every coroutine launched on it, and every child of those, receives a [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) at its next [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
override fun onCleared() {
    super.onCleared()
    // viewModelScope is already being cancelled by the framework.
    // Only non-coroutine resources need explicit release here.
    listenerRegistration.remove()
}
```

## The Senior Nuance

- **You rarely need to override it.** Since `viewModelScope` is cancelled automatically, the override is only for resources that are not coroutines: listeners, closeables, custom scopes.
- **It is the root of the tree for a screen.** The reason a `Job?` field or a long collector in a ViewModel is not a leak is that `onCleared` reaches it through the [`Job`]({{ "/en/glossary/job/" | relative_url }}) hierarchy — provided nothing swallowed the cancellation.
- **It does not run on configuration changes.** A rotation keeps the ViewModel; only a real teardown clears it.
- See [Structured Concurrency]({{ "/en/02-coroutines-flow/structured-concurrency/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
