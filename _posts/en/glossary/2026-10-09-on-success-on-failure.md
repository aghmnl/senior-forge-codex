---
layout: post
title: "onSuccess / onFailure"
date: 2026-10-09 12:00:00 +0000
categories: [en, glossary]
tags: [callbacks, error-handling]
lang: en
permalink: /en/glossary/on-success-on-failure/
---

## The Theory (The What)

**`onSuccess`** and **`onFailure`** are the usual pair of [callbacks]({{ "/en/glossary/callbacks/" | relative_url }}) of an asynchronous operation that produces **one [result]({{ "/en/glossary/result/" | relative_url }})**: the [API]({{ "/en/glossary/api/" | relative_url }}) calls the first with the value when it works, or the second with the error when it does not. Play services `Task` (`addOnSuccessListener` / `addOnFailureListener`) and many SDKs follow this shape. [Kotlin]({{ "/en/glossary/kotlin/" | relative_url }})'s [`Result`]({{ "/en/glossary/result/" | relative_url }}) has functions with the same names.

```kotlin
// Not found in FAS — standalone example
appUpdateManager.appUpdateInfo
    .addOnSuccessListener { info -> handle(info) }
    .addOnFailureListener { e -> Log.w(TAG, "Check failed", e) }
```

## The Senior Nuance

- **One [result]({{ "/en/glossary/result/" | relative_url }}) means a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}), not a [flow]({{ "/en/glossary/flow/" | relative_url }}).** Wrap the pair with [`suspendCancellableCoroutine`]({{ "/en/glossary/suspend-cancellable-coroutine/" | relative_url }}): resume with the value in `onSuccess`, resume with the exception in `onFailure`, and the caller gets a plain `try`/`catch`.
- **Exactly one of them is called, exactly once.** Code that assumes otherwise (resuming twice) crashes the [continuation]({{ "/en/glossary/continuation/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
