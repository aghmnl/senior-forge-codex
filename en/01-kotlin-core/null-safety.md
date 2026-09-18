---
layout: page
title: "Null Safety: Elvis & Safe Calls"
lang: en
permalink: /en/01-kotlin-core/null-safety-elvis-safe-calls/
order: 1
---

## The Theory (The What)

Kotlin's type system distinguishes between nullable ([`String?`]({{ "/en/glossary/string/" | relative_url }})) and non-nullable ([`String`]({{ "/en/glossary/string/" | relative_url }})) types at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}). This eliminates the majority of [NullPointerException]({{ "/en/glossary/null-pointer-exception/" | relative_url }}) crashes that plague Java codebases. The key operators are:

- **[Safe call]({{ "/en/glossary/safe-call/" | relative_url }}) (`?.`)**: Accesses a member only if the receiver is non-null; returns [`null`]({{ "/en/glossary/null/" | relative_url }}) otherwise.
- **[Elvis operator]({{ "/en/glossary/elvis-operator/" | relative_url }}) ([`?:`]({{ "/en/glossary/elvis-operator/" | relative_url }}))**: Provides a fallback value when the left-hand side is [`null`]({{ "/en/glossary/null/" | relative_url }}).
- **Non-null [assertion]({{ "/en/glossary/assertion/" | relative_url }}) ([`!!`]({{ "/en/glossary/non-null-assertion/" | relative_url }}))**: Forces a nullable type to non-null, throwing [NullPointerException]({{ "/en/glossary/null-pointer-exception/" | relative_url }}) if it is [`null`]({{ "/en/glossary/null/" | relative_url }}). **Should never be used in production code.**
- **Safe [cast]({{ "/en/glossary/cast/" | relative_url }}) ([`as?`]({{ "/en/glossary/as-safe-cast/" | relative_url }}))**: Attempts a cast and returns [`null`]({{ "/en/glossary/null/" | relative_url }}) on failure instead of throwing [ClassCastException]({{ "/en/glossary/class-cast-exception/" | relative_url }}).

## The Senior Perspective (The Why)

For a Senior Developer, null safety is not [syntax sugar]({{ "/en/glossary/syntax-sugar/" | relative_url }}) — it's a design tool that encodes domain invariants into the type system.

- **Null Means Something**: A [`String?`]({{ "/en/glossary/string/" | relative_url }}) return type is a contract: "this value might legitimately be absent." A Senior uses nullable types to express optionality (a user's photo URL) and non-nullable types to express guarantees (a user's email). Choosing the wrong nullability leaks domain ambiguity into every consumer.
- **[`!!`]({{ "/en/glossary/non-null-assertion/" | relative_url }}) Should Never Be Used**: Every [`!!`]({{ "/en/glossary/non-null-assertion/" | relative_url }}) is a claim that the developer knows more than the compiler — and it's almost always wrong or lazy. It produces a generic [NullPointerException]({{ "/en/glossary/null-pointer-exception/" | relative_url }}) with no context, making the [stack trace]({{ "/en/glossary/stack-trace/" | relative_url }}) useless for debugging. There is always a better alternative (see strategies below).
- **[Platform Types]({{ "/en/glossary/platform-types/" | relative_url }})**: Values from Java APIs arrive as [platform types]({{ "/en/glossary/platform-types/" | relative_url }}) (`String!`) — neither nullable nor non-nullable. A Senior annotates Java interop boundaries with [`@Nullable`]({{ "/en/glossary/nullable-annotation/" | relative_url }})/[`@NonNull`]({{ "/en/glossary/non-null-annotation/" | relative_url }}) or wraps them in Kotlin functions that declare explicit nullability, preventing silent [NullPointerException]({{ "/en/glossary/null-pointer-exception/" | relative_url }}) propagation.
- **Early Return with Elvis**: The [`?: return`]({{ "/en/glossary/elvis-return/" | relative_url }}) pattern is the idiomatic [guard clause]({{ "/en/glossary/guard-clause/" | relative_url }}) that eliminates nullability from the rest of the function [scope]({{ "/en/glossary/scope/" | relative_url }}), keeping the happy path flat and readable.

### Strategies to eliminate `!!`

1. **Redesign the data flow** so the value is non-nullable from the start — use constructor injection instead of late assignment, or move the null check to the caller.
2. **Use Elvis with an explicit exception** (`?: `[`throw`]({{ "/en/glossary/throw/" | relative_url }}) [`IllegalStateException`]({{ "/en/glossary/illegal-state-exception/" | relative_url }})`("reason")`) so the [stack trace]({{ "/en/glossary/stack-trace/" | relative_url }}) explains which invariant was violated.
3. **Use [safe calls]({{ "/en/glossary/safe-call/" | relative_url }}) with [`let`]({{ "/en/glossary/let/" | relative_url }}), [`run`]({{ "/en/glossary/run/" | relative_url }}), or [early return]({{ "/en/glossary/elvis-return/" | relative_url }})** ([`?: return`]({{ "/en/glossary/elvis-return/" | relative_url }})) to handle the null case explicitly in the control flow.

The goal is to make nullability decisions visible in the type system, not hidden behind [assertions]({{ "/en/glossary/assertion/" | relative_url }}).

## Code in Action

```kotlin
// From FollowApp Suite — BillingConnector
// Guard clause with Elvis: eliminates null from the rest of the scope
fun launchPurchase(activity: Activity): Boolean {
    val details = productDetails ?: return false
    val params = BillingFlowParams.newBuilder()
        .setProductDetailsParamsList(
            listOf(
                BillingFlowParams.ProductDetailsParams.newBuilder()
                    .setProductDetails(details)
                    .build()
            )
        )
        .build()
    return billingClient.launchBillingFlow(activity, params)
        .responseCode == BillingClient.BillingResponseCode.OK
}

// From FollowApp Suite — AuthPreferences
// Safe call + let + Elvis: save when present, remove when absent
fun saveSession(session: UserSession, prefs: MutablePreferences) {
    session.photoUrl?.let { prefs[photoUrlKey] = it }
        ?: prefs.remove(photoUrlKey)
}

// From FollowApp Suite — PresetRepositoryImpl
// Elvis for defaults: production-safe fallback
fun resolvePosition(existing: Preset?): Int {
    return existing?.position ?: dao.nextPosition()
}

// From FollowApp Suite — TasksViewModel
// Guard clause + smart cast in sealed hierarchy
fun onCascadeConfirmed() {
    val action = _uiState.value.pendingCascadeAction ?: return
    _uiState.update { it.copy(pendingCascadeAction = null) }
    viewModelScope.launch {
        when (action) {
            is CascadeAction.Complete -> {
                quickCompleteTaskUseCase(
                    taskId = action.taskId,
                    isCompleted = action.isCompleted,
                    cascade = true
                )
            }
            is CascadeAction.Archive -> {
                archiveTaskUseCase(action.taskId, cascade = true)
            }
            is CascadeAction.Delete -> {
                moveTaskToTrashUseCase(action.taskId, cascade = true)
            }
        }
    }
}
```

## The Interview (The Hot Seat)

**Question**: Why should [`!!`]({{ "/en/glossary/non-null-assertion/" | relative_url }}) never appear in production code, and what does a Senior do instead?

**Senior Answer**: The [`!!`]({{ "/en/glossary/non-null-assertion/" | relative_url }}) operator trades a [compile-time]({{ "/en/glossary/compile-time/" | relative_url }}) safety guarantee for a [runtime]({{ "/en/glossary/runtime/" | relative_url }}) crash with no context. It produces a generic [NullPointerException]({{ "/en/glossary/null-pointer-exception/" | relative_url }}) whose [stack trace]({{ "/en/glossary/stack-trace/" | relative_url }}) tells you WHERE the crash happened but not WHY the value was null. In every case, a Senior eliminates [`!!`]({{ "/en/glossary/non-null-assertion/" | relative_url }}) through three strategies:

   1. Redesign the data flow so the value is non-nullable from the start — for example, using constructor injection instead of late assignment.
   2. Use the [Elvis operator]({{ "/en/glossary/elvis-operator/" | relative_url }}) with an explicit exception (`?: `[`throw`]({{ "/en/glossary/throw/" | relative_url }}) [`IllegalStateException`]({{ "/en/glossary/illegal-state-exception/" | relative_url }})`("reason")`) so the [stack trace]({{ "/en/glossary/stack-trace/" | relative_url }}) explains the invariant that was violated.
   3. Use [safe calls]({{ "/en/glossary/safe-call/" | relative_url }}) with [`let`]({{ "/en/glossary/let/" | relative_url }}), [`run`]({{ "/en/glossary/run/" | relative_url }}), or [early return]({{ "/en/glossary/elvis-return/" | relative_url }}) ([`?: return`]({{ "/en/glossary/elvis-return/" | relative_url }})) to handle the null case explicitly.

   The goal is to make nullability decisions visible in the type system, not hidden behind [assertions]({{ "/en/glossary/assertion/" | relative_url }}).

---

[Back to Chapters]({{ "/" | relative_url }})
