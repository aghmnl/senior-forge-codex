---
layout: post
title: "updateAndGet"
date: 2026-09-28 12:00:00 +0000
categories: [en, glossary]
tags: [concurrency, state-management, flow]
lang: en
permalink: /en/glossary/update-and-get/
---

## The Theory (The What)

**`updateAndGet { }`** is a variant of [update {}]({{ "/en/glossary/update/" | relative_url }}) for [MutableStateFlow]({{ "/en/glossary/mutable-state-flow/" | relative_url }}) that applies the change atomically and **returns the new value**, the one that was actually stored. It works exactly like `update`: it computes the next value from the current one and stores it with [compareAndSet]({{ "/en/glossary/compare-and-set/" | relative_url }}), retrying if another writer got there first.

```kotlin
// Not found in FAS — standalone example
private val _attempts = MutableStateFlow(0)

fun onRetry() {
    // The returned number is the one this call stored, even if
    // other threads are incrementing at the same time
    val attempt = _attempts.updateAndGet { it + 1 }
    if (attempt >= MAX_ATTEMPTS) showGiveUpMessage()
}
```

## The Senior Nuance

- **Use it when you need the result of your own change.** Reading `.value` right after `update` is not the same: by then another writer may have changed it again.
- **The same rules as `update` apply.** The lambda can run more than once, so it must be pure and short.
- Its sibling [getAndUpdate]({{ "/en/glossary/get-and-update/" | relative_url }}) returns the value **before** the change instead.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
