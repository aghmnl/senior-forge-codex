---
layout: post
title: "Event Handlers"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/event-handlers/
---

## The Theory (The What)

An **event handler** is a [callback]({{ "/en/glossary/callbacks/" | relative_url }}) that responds to a specific user interaction or system event — a button tap, a text change, a lifecycle transition, a gesture. In [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}), event handlers are [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) parameters (`onClick`, `onValueChange`, `onDismissRequest`) passed to composable functions. In the View system, they are listener interfaces (`OnClickListener`, `OnScrollListener`) set on widgets.

```kotlin
// From FollowApp Suite — ConfirmationDialog.kt
@Composable
fun ConfirmationDialog(
    title: String,
    message: String,
    confirmLabel: String,
    dismissLabel: String,
    onConfirm: (dontAskAgain: Boolean) -> Unit,
    onDismiss: () -> Unit,
    dontAskAgainLabel: String? = null,
) {
    // ...
    confirmButton = {
        TextButton(onClick = { onConfirm(dontAskAgain) }) { Text(confirmLabel) }
    }
    dismissButton = {
        TextButton(onClick = onDismiss) { Text(dismissLabel) }
    }
}
```

Each event handler has a [type-safe]({{ "/en/glossary/type-safety/" | relative_url }}) signature: `onConfirm` receives a `Boolean` (the "don't ask again" flag), while `onDismiss` takes no arguments.

## The Senior Nuance

- **Compose event flow**: Events flow **up** (child → parent) while state flows **down** (parent → child). This is the [unidirectional data flow]({{ "/en/glossary/unidirectional-data-flow/" | relative_url }}) pattern. Event handlers are the upward channel — they notify the parent (often a ViewModel) that something happened, and the parent updates the state.
- **Consolidation via callback classes**: When a composable needs many event handlers, grouping them into a dedicated class (like `TaskFormCallbacks`) avoids parameter-list explosion and makes the API easier to evolve. See [callbacks]({{ "/en/glossary/callbacks/" | relative_url }}).
- **Don't do heavy work inside event handlers**: An `onClick` runs on the main thread. If you need async work, launch a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) from the handler or dispatch an intent/event to the ViewModel. In [MVI]({{ "/en/glossary/mvi-pattern/" | relative_url }}), event handlers simply emit user intents.
- **Stability and recomposition**: In Compose, a lambda event handler captures its enclosing state. If those captures are unstable (reference a mutable non-`State` object), the composable is considered unstable and cannot be skipped during recomposition. Senior developers use `remember`, stable references, or move the handler to a stable holder to avoid this.
- **View system legacy**: In the View system, forgetting to remove an event handler (e.g., an `OnClickListener` on a view held by a long-lived adapter) is a [memory leak]({{ "/en/glossary/memory-leaks/" | relative_url }}) vector. Compose's declarative model eliminates this — handlers exist only while the composable is in the composition.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
