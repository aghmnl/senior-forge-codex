---
layout: post
title: "asSharedFlow"
date: 2026-09-28 12:00:00 +0000
categories: [en, glossary]
tags: [flow, state-management, architecture]
lang: en
permalink: /en/glossary/as-shared-flow/
---

## The Theory (The What)

**`asSharedFlow()`** returns a **read-only view** of a [MutableSharedFlow]({{ "/en/glossary/mutable-shared-flow/" | relative_url }}): a `SharedFlow` that delivers the same emissions but offers no way to emit. It is the [SharedFlow]({{ "/en/glossary/sharedflow/" | relative_url }}) counterpart of [asStateFlow()]({{ "/en/glossary/as-state-flow/" | relative_url }}), and it is how a class exposes a stream it owns without letting callers write into it.

```kotlin
// Not found in FAS — standalone example
class SessionManager {
    private val _sessionExpired = MutableSharedFlow<Unit>(extraBufferCapacity = 1)
    val sessionExpired: SharedFlow<Unit> = _sessionExpired.asSharedFlow()
}
```

## The Senior Nuance

- **Upcasting is not enough.** Declaring `val events: SharedFlow<T> = _events` hides the mutable type from the signature, but any caller can cast it back to [`MutableSharedFlow`]({{ "/en/glossary/mutable-shared-flow/" | relative_url }}) and emit. `asSharedFlow()` returns a different object that cannot be cast back.
- **It enforces [unidirectional data flow]({{ "/en/glossary/unidirectional-data-flow/" | relative_url }}).** Only the owner can produce values; everyone else can only [collect]({{ "/en/glossary/collect/" | relative_url }}). That keeps every emission traceable to one place.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
