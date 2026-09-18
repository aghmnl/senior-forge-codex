---
layout: post
title: "checkNotNull"
date: 2026-09-18 12:00:00 +0000
categories: [en, glossary]
tags: [null-safety, error-handling]
lang: en
permalink: /en/glossary/check-not-null/
---

## The Theory (The What)

**`checkNotNull(value) { "message" }`** throws `IllegalStateException` if `value` is null and otherwise returns it as non-null. It is [`check`]({{ "/en/glossary/check/" | relative_url }}) specialised for nullability: use it when a null means the *object's own state* is broken (a field that should have been initialised, a lookup that must succeed), not that the caller passed a bad argument — that is [`requireNotNull`]({{ "/en/glossary/require-not-null/" | relative_url }}). Its [contract]({{ "/en/glossary/contract/" | relative_url }}) makes the compiler [Smart Casts]({{ "/en/01-kotlin-core/smart-casts/" | relative_url }}) smart-cast the checked variable to non-null after the call.

```kotlin
// Not found in FAS — standalone example
class SessionHolder {
    private var current: UserSession? = null

    fun currentUserId(): String {
        val session = checkNotNull(current) { "currentUserId() called before signIn()" }
        return session.userId
    }
}
```

## The Senior Nuance

- **State that "should" be there is the classic `!!` trap.** `current!!.userId` crashes with an anonymous [`NullPointerException`]({{ "/en/glossary/null-pointer-exception/" | relative_url }}); `checkNotNull` crashes with a sentence that names the lifecycle rule that was violated. Same behaviour, far cheaper debugging.
- **If it is *always* initialised before use, model that.** `lateinit var` (throws `UninitializedPropertyAccessException` with the property name) or constructor injection remove the nullable altogether; `checkNotNull` is for the cases where null is a legitimate intermediate state.
- **Return value or smart cast — both work.** `val s = checkNotNull(current)` reads better in a chain; the smart cast on `current` itself only holds if it is a stable [`val`]({{ "/en/glossary/val/" | relative_url }}) — for a [`var`]({{ "/en/glossary/var/" | relative_url }}) property like the one above, keep the returned local.
- See [Smart Casts]({{ "/en/01-kotlin-core/smart-casts/" | relative_url }}) and [Null Safety]({{ "/en/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
