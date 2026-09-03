---
layout: post
title: "Event Wiring"
date: 2026-09-02 12:00:00 +0000
categories: [en, glossary]
lang: en
permalink: /en/glossary/event-wiring/
---

## The Theory (The What)

**Event wiring** is the practice of connecting UI components to the logic that handles their interactions — plugging [event handlers]({{ "/en/glossary/event-handlers/" | relative_url }}) into the composables, views, or framework components that produce events. In [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}), event wiring means passing [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) [callbacks]({{ "/en/glossary/callbacks/" | relative_url }}) from a screen-level composable (which holds the ViewModel reference) down to leaf composables. In the View system, it means calling `setOnClickListener`, `addTextChangedListener`, or registering observer interfaces.

```kotlin
// From FollowApp Suite — TasksCallbacks.kt
class TaskFormCallbacks(
    val onFormTitleChange: (String) -> Unit,
    val onFormDescriptionChange: (String) -> Unit,
    val onFormCompletedChange: (Boolean) -> Unit,
    val onFormDueDateChange: (Long?) -> Unit,
    val onFormConfirmed: () -> Unit,
    val onFormDismissed: () -> Unit,
    val onFormRecurrenceChange: (RecurrenceRule?) -> Unit,
    val onAddSubtask: (String) -> Unit,
)
```

This class is the wiring contract: the screen composable creates an instance (each [callback]({{ "/en/glossary/callbacks/" | relative_url }}) calling the corresponding ViewModel method) and passes it to the form composable, which invokes the right handler on each user interaction.

## The Senior Nuance

- **Compose makes wiring explicit**: Every event path is visible in the function signature — no hidden `findViewById` + `setListener` chains. This makes it easier to trace what happens when a user taps, types, or swipes, because the [callback]({{ "/en/glossary/callbacks/" | relative_url }}) is right there in the parameter list.
- **Callback consolidation is a wiring pattern**: When a form has 10+ events, passing them individually creates noisy signatures and fragile call sites. Grouping them into a class (like `TaskFormCallbacks`) is a wiring strategy that keeps the connection clean and [type-safe]({{ "/en/glossary/type-safety/" | relative_url }}).
- **In [MVI]({{ "/en/glossary/mvi-pattern/" | relative_url }})**, event wiring routes UI events to a single `onEvent(UiEvent)` function on the ViewModel. The wiring becomes a mapping from user action → sealed class variant, keeping the composable layer thin and the event routing centralized.
- **View system wiring pitfalls**: Forgetting to unwire (unregister a listener) when a view is recycled (RecyclerView) or a fragment is destroyed is a classic [memory leak]({{ "/en/glossary/memory-leaks/" | relative_url }}) source. Compose's declarative model removes this problem — wiring exists only while the composable is in the composition tree.
- **[Broadcast receivers]({{ "/en/glossary/broadcast-receiver/" | relative_url }})** represent system-level event wiring: registering a receiver wires your component to system or app events (connectivity changes, battery low). Senior developers prefer [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) registration to avoid leaking receivers.

---

[Back to Glossary]({{ "/en/glossary/" | relative_url }})
