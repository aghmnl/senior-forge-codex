---
layout: post
title: "Callback Hell"
date: 2026-09-10 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/callback-hell/
---

## The Theory (The What)

**Callback hell** is the shape asynchronous code takes when each [async operation]({{ "/en/glossary/async-operations/" | relative_url }}) reports its result through a [callback]({{ "/en/glossary/callbacks/" | relative_url }}) and the next operation must be started *inside* that callback: nesting grows rightward with every step, error handling is duplicated at every level, and cancellation has to be threaded through by hand.

```kotlin
// Not found in FAS — standalone example
api.getUser(id) { user ->
    api.getOrders(user.id) { orders ->
        api.getInvoice(orders.first().id) { invoice ->
            runOnUiThread { render(invoice) }   // error handling? cancellation?
        }
    }
}

// The same with suspend functions:
val invoice = api.getInvoice(api.getOrders(api.getUser(id).id).first().id)
render(invoice)
```

[Suspend functions]({{ "/en/glossary/suspend-functions/" | relative_url }}) are the compiler doing the nesting for you: the same [Continuation-Passing Style]({{ "/en/glossary/continuation-passing-style/" | relative_url }}) transformation, emitted automatically and hidden behind sequential syntax.

## The Senior Nuance

- **The problem was never the callbacks — it was composition.** Sequencing, branching, looping and `try/finally` are trivial in straight-line code and hostile inside callbacks. Coroutines restore the language's own control flow to async code.
- **Bridge once, at the edge.** [suspendCancellableCoroutine]({{ "/en/glossary/suspend-cancellable-coroutine/" | relative_url }}) converts a callback API to a suspend function in one place; everything above it is sequential. Modern Android has little callback hell left because Jetpack already did this.
- **`Flow` is the multi-shot answer.** A listener that fires repeatedly becomes `callbackFlow`, and its consumers get operators instead of nested handlers.
- See [Suspend Functions]({{ "/en/02-coroutines-flow/suspend-functions/" | relative_url }}).

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
