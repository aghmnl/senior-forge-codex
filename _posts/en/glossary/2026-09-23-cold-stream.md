---
layout: post
title: "Cold Stream"
date: 2026-09-23 12:00:00 +0000
categories: [en, glossary]
tags: [flow, coroutines, performance]
lang: en
permalink: /en/glossary/cold-stream/
---

## The Theory (The What)

A **cold stream** produces its values only when somebody consumes it, and produces them again, from scratch, for every consumer. A [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) is the Kotlin example: building it and chaining operators executes nothing; the producer starts at the [terminal operator]({{ "/en/glossary/terminal-operations/" | relative_url }}) and stops when the collector's scope is cancelled. The opposite is a *hot* stream — [`StateFlow`]({{ "/en/glossary/stateflow/" | relative_url }}), `SharedFlow`, a `Channel` — which is running and holding values whether anyone is listening or not.

```kotlin
// Not found in FAS — standalone example
val cold = flow {
    println("producing")     // printed once PER collector
    emit(1)
}

cold.collect { }             // prints "producing"
cold.collect { }             // prints "producing" again — independent execution
```

## The Senior Nuance

- **Cold means duplicated work, not shared work.** Two collectors on a [Room]({{ "/en/glossary/room/" | relative_url }})-backed flow are two queries and two observers. Sharing one execution is what `shareIn`/`stateIn` are for.
- **Cold means no side effect on creation.** A repository can return a stream without owning a [scope]({{ "/en/glossary/coroutine-scope/" | relative_url }}) or a lifecycle, which is what makes the data layer easy to test.
- **A cold stream that nobody collects does nothing, silently.** No error and no log — the most common "my flow is not working" cause.
- See [Flow (Cold Streams)]({{ "/en/02-coroutines-flow/flow-cold-streams/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
