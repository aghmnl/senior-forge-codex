---
layout: post
title: "IllegalStateException"
date: 2026-09-18 12:00:00 +0000
categories: [en, glossary]
tags: [error-handling, design-principles]
lang: en
permalink: /en/glossary/illegal-state-exception/
---

## The Theory (The What)

**`IllegalStateException`** is the JVM exception that means "this object is in a state it should never be in": a method was called before initialisation, after teardown, or with an internal [invariant]({{ "/en/glossary/invariant/" | relative_url }}) broken. Kotlin's [`check`]({{ "/en/glossary/check/" | relative_url }}), [`checkNotNull`]({{ "/en/glossary/check-not-null/" | relative_url }}) and `error()` all [throw]({{ "/en/glossary/throw/" | relative_url }}) it. In [Null Safety: Elvis & Safe Calls]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}) it is the recommended replacement for `!!`: `value ?: throw IllegalStateException("reason")` crashes on the same input but leaves a [stack trace]({{ "/en/glossary/stack-trace/" | relative_url }}) that names the violated rule instead of an anonymous [`NullPointerException`]({{ "/en/glossary/null-pointer-exception/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
fun launchPurchase(activity: Activity) {
    val details = productDetails
        ?: throw IllegalStateException("launchPurchase called before queryProductDetails()")
    billingClient.launchBillingFlow(activity, params(details))
}

// Same thing, shorter
val details = checkNotNull(productDetails) { "launchPurchase called before queryProductDetails()" }
```

## The Senior Nuance

- **State vs argument.** `IllegalStateException` blames the object; `IllegalArgumentException` (from [`require`]({{ "/en/glossary/require/" | relative_url }})) blames the caller. Choosing the right one is the first thing a reader of the crash report checks.
- **The message is the value.** An `IllegalStateException` without a message is barely better than an NPE. Name the method that should have been called first, or the field that should have been set.
- **Do not catch it.** It signals a programming error, not a recoverable condition; catching it hides the bug. Let it crash in debug and reach Crashlytics in release.
- See [Null Safety: Elvis & Safe Calls]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
