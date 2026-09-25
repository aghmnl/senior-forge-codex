---
layout: post
title: "Hot Stream"
date: 2026-09-25 12:00:00 +0000
categories: [en, glossary]
tags: [flow, coroutines, performance]
lang: en
permalink: /en/glossary/hot-stream/
---

## The Theory (The What)

A **hot stream** exists and produces (or holds) values **independently of whether anyone is consuming them**. Subscribers join a stream that is already running and see what happens from that moment on — plus, depending on the type, some replayed past values. It is the opposite of a [cold stream]({{ "/en/glossary/cold-stream/" | relative_url }}), where each consumer triggers its own execution from scratch. In Kotlin the hot streams are [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}), [SharedFlow]({{ "/en/glossary/sharedflow/" | relative_url }}) and [Channel]({{ "/en/glossary/channel/" | relative_url }}); [stateIn]({{ "/en/glossary/state-in/" | relative_url }}) and `shareIn` turn a cold [Flow]({{ "/en/glossary/flow/" | relative_url }}) into a hot one.

```kotlin
// Not found in FAS — standalone example
val hot = MutableStateFlow(0)
hot.value = 1                  // happens with nobody listening

scope.launch { hot.collect { println(it) } }   // prints 1: joins the present
hot.value = 2                                   // prints 2
```

## The Senior Nuance

- **Hot means shared work.** One producer, many consumers: three screens observing a hot stream cost one execution, where three collectors of a cold stream cost three.
- **Hot means the lifetime is not the collector's.** The stream lives in the scope that created it (usually a ViewModel). That is what lets it survive a rotation, and also what makes a forgotten hot stream a leak.
- **Joining late has consequences.** A subscriber of a hot stream can miss values emitted before it arrived. Whether that is fine depends on the type: a `StateFlow` always hands over its current value; a `SharedFlow` without replay does not.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
