---
layout: post
title: "getAndUpdate"
date: 2026-09-28 12:00:00 +0000
categories: [en, glossary]
tags: [concurrency, state-management, flow]
lang: en
permalink: /en/glossary/get-and-update/
---

## The Theory (The What)

**`getAndUpdate { }`** is a variant of [update {}]({{ "/en/glossary/update/" | relative_url }}) for [MutableStateFlow]({{ "/en/glossary/mutable-state-flow/" | relative_url }}) that applies the change atomically and **returns the value it had before the change**. It works exactly like `update`: it computes the next value from the current one and stores it with [compareAndSet]({{ "/en/glossary/compare-and-set/" | relative_url }}), retrying if another writer got there first.

```kotlin
// Not found in FAS — standalone example
private val _pending = MutableStateFlow<List<Upload>>(emptyList())

// Take every pending upload and leave the list empty, in one atomic step:
// no upload can be added in between and lost
fun drainPending(): List<Upload> = _pending.getAndUpdate { emptyList() }
```

## The Senior Nuance

- **Use it when you need the old value.** The typical case is "take and reset": read what was there and replace it, without another writer slipping in between the read and the reset.
- **The same rules as `update` apply.** The lambda can run more than once, so it must be pure and short.
- Its sibling [updateAndGet]({{ "/en/glossary/update-and-get/" | relative_url }}) returns the value **after** the change instead.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
