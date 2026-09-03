---
layout: post
title: "Crossinline"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/crossinline/
---

## The Theory (The What)

**`crossinline`** is a modifier for [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) parameters of [inline functions]({{ "/en/glossary/inline-functions/" | relative_url }}) that forbids non-local returns from that lambda. When a function is marked `inline`, its lambda parameters are inlined at the call site, which normally allows the lambda to use `return` to exit the *calling* function (a non-local return). `crossinline` disables this when the lambda escapes the inline function's own execution flow — typically because it's passed to another execution context like a local `object`, a `Runnable`, or a coroutine builder.

```kotlin
// Not found in FAS — standalone example
inline fun runOnUiThread(crossinline action: () -> Unit) {
    handler.post(Runnable { action() })  // action escapes into a Runnable
    // Without crossinline, 'return' inside action would try to exit
    // the calling function — but that's impossible from inside a Runnable
}

fun loadData() {
    runOnUiThread {
        updateUI()
        // return  // ERROR: not allowed — crossinline prevents non-local return
    }
}
```

## The Senior Nuance

- `crossinline` solves a specific problem: when an [inline function]({{ "/en/glossary/inline-functions/" | relative_url }}) passes its lambda to a context where a non-local return is structurally impossible (the call stack won't match). Without `crossinline`, the compiler would allow `return` inside the lambda, which would fail at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}). The modifier makes this a [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) error instead.
- The most common use case is inline functions that delegate lambdas to `Runnable`, `Executor.execute {}`, or coroutine builders like `launch {}`. The lambda is still inlined (no [allocation]({{ "/en/glossary/allocations/" | relative_url }})), but `return` is restricted to `return@label` (local return) only.
- Contrast with [`noinline`]({{ "/en/glossary/noinline/" | relative_url }}): `crossinline` still inlines the lambda body (zero allocation), it just blocks non-local `return`. `noinline` prevents inlining entirely — the lambda becomes a regular `Function` object on the [heap]({{ "/en/glossary/heap/" | relative_url }}).
- In practice, if the compiler tells you "Can't inline 'action' here: it may contain non-local return," adding `crossinline` is the fix. It's a precision tool — use it exactly when the lambda needs to be inlined but also needs to cross an execution boundary.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
