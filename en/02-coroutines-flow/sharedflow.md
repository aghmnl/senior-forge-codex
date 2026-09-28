---
layout: page
title: "SharedFlow"
lang: en
permalink: /en/02-coroutines-flow/sharedflow/
order: 10
---

## The Theory (The What)

A `SharedFlow<T>` is the general [hot stream]({{ "/en/glossary/hot-stream/" | relative_url }}) of [kotlinx.coroutines]({{ "/en/glossary/kotlinx-coroutines/" | relative_url }}). It has a single source that **broadcasts every emission to every current [collector]({{ "/en/glossary/collector/" | relative_url }})**. Where a [cold]({{ "/en/glossary/cold-stream/" | relative_url }}) [Flow]({{ "/en/02-coroutines-flow/flow-cold-streams/" | relative_url }}) runs its producer once per [collector]({{ "/en/glossary/collector/" | relative_url }}), a `SharedFlow` runs independently of its [collectors]({{ "/en/glossary/collector/" | relative_url }}), and they subscribe to whatever it emits from that moment on.

It is created mutable, the same way as a [StateFlow]({{ "/en/02-coroutines-flow/stateflow/" | relative_url }}): a private [`MutableSharedFlow`]({{ "/en/glossary/mutable-shared-flow/" | relative_url }}) exposed read-only through [`asSharedFlow()`]({{ "/en/glossary/as-shared-flow/" | relative_url }}). Its constructor takes three parameters, and they define its whole behavior:

- **`replay`** (default `0`): how many past values a new subscriber receives the moment it subscribes. With `0`, a late subscriber only sees what is emitted after it arrives.
- **`extraBufferCapacity`** (default `0`): extra room, on top of `replay`, for values that fast emitters have sent and slow subscribers have not taken yet.
- **`onBufferOverflow`** (default `SUSPEND`): what happens when the buffer is full. `SUSPEND` makes [`emit`]({{ "/en/glossary/emit/" | relative_url }}) wait, `DROP_OLDEST` throws away the oldest buffered value, and `DROP_LATEST` throws away the new one. The two drop policies require a buffer (`replay` or `extraBufferCapacity` above zero).

Values go in with [`emit`]({{ "/en/glossary/emit/" | relative_url }}), a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) that waits when the buffer is full, or with [`tryEmit`]({{ "/en/glossary/try-emit/" | relative_url }}), which never suspends and returns `false` when the value does not fit. Unlike a [`StateFlow`]({{ "/en/02-coroutines-flow/stateflow/" | relative_url }}), a `SharedFlow` has **no current value, no initial value and no equality filtering**: emitting the same value twice delivers it twice. Its [`collect`]({{ "/en/glossary/collect/" | relative_url }}) **never completes**. The flow has no end, so the collecting [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) runs until its scope is cancelled.

[`StateFlow`]({{ "/en/02-coroutines-flow/stateflow/" | relative_url }}) is exactly a `SharedFlow` with a fixed configuration: `replay = 1`, `onBufferOverflow = DROP_OLDEST`, an initial value, and [`distinctUntilChanged`]({{ "/en/glossary/distinct-until-changed/" | relative_url }}) built in. `SharedFlow` is what you use when that configuration is not the one you need.

## The Senior Perspective (The Why)

- **The default configuration is a rendezvous, and that surprises people.** [`MutableSharedFlow<T>()`]({{ "/en/glossary/mutable-shared-flow/" | relative_url }}) has no buffer at all. With subscribers present, [`emit`]({{ "/en/glossary/emit/" | relative_url }}) suspends until every one of them has received the value, and [`tryEmit`]({{ "/en/glossary/try-emit/" | relative_url }}) always returns `false`, because there is nowhere to put the value without suspending. A [`tryEmit`]({{ "/en/glossary/try-emit/" | relative_url }}) that "does nothing" is almost always this. Calling [`tryEmit`]({{ "/en/glossary/try-emit/" | relative_url }}) from non-suspending code needs `extraBufferCapacity` or a drop policy.
- **With no subscribers, emissions are simply lost.** With `replay = 0`, a value emitted while nobody is collecting goes nowhere: no error, no warning. For a real broadcast signal that is exactly right. For a UI event it is the trap: a screen collecting with [`repeatOnLifecycle(STARTED)`]({{ "/en/glossary/repeat-on-lifecycle/" | relative_url }}) has zero subscribers while it is in the background, so a navigation event emitted then disappears.
- **One slow subscriber slows everyone.** Under `SUSPEND` the buffer is sized for the slowest [collector]({{ "/en/glossary/collector/" | relative_url }}). When it falls behind and the buffer fills, [`emit`]({{ "/en/glossary/emit/" | relative_url }}) suspends for all of them, and fast [collectors]({{ "/en/glossary/collector/" | relative_url }}) wait for the slow one. When the producer must never wait, a drop policy trades completeness for liveness, and that trade has to be a deliberate decision.
- **Replay is a policy, not a cache you get for free.** `replay = 1` makes a late subscriber receive the latest value, which looks like a [`StateFlow`]({{ "/en/02-coroutines-flow/stateflow/" | relative_url }}) without the equality filter. It also means a one-shot event is **replayed** to every new subscriber, after a rotation for example, which is the double-navigation bug again. [`resetReplayCache()`]({{ "/en/glossary/reset-replay-cache/" | relative_url }}) clears it, but calling it at the right moment is fragile.
- **The right use case is broadcast.** A `SharedFlow` shines when several independent consumers must each react to the same signal and missing it while nobody listens is acceptable. Examples are an app-wide "session expired", a "data changed, invalidate your caches" signal from a [singleton]({{ "/en/glossary/singleton/" | relative_url }}) repository, or a single [upstream]({{ "/en/glossary/upstream/" | relative_url }}) connection shared by several screens through [`shareIn`]({{ "/en/glossary/share-in/" | relative_url }}). When a value must be handled **exactly once by exactly one consumer**, the primitive is a [`Channel`]({{ "/en/glossary/channel/" | relative_url }}), which queues instead of broadcasting.
- **For UI events, first ask whether it is an event at all.** [Android]({{ "/en/glossary/android/" | relative_url }})'s architecture guidance recommends reducing UI events to state: the ViewModel puts the pending message into the UI state, and the UI reports back when it has shown it. That survives rotation, background and process death, and it is trivial to test. A `SharedFlow` of UI events is the pattern the guidance moved away from, because every one of the failure modes above applies to it.

## Code in Action

```kotlin
// Not found in FAS — standalone example
// A broadcast signal: every subscriber must react, and nobody needs
// the value if it happened while they were not listening
class SessionManager {
    private val _sessionExpired = MutableSharedFlow<Unit>(
        extraBufferCapacity = 1,                        // lets tryEmit succeed
        onBufferOverflow = BufferOverflow.DROP_OLDEST   // never blocks the caller
    )
    val sessionExpired: SharedFlow<Unit> = _sessionExpired.asSharedFlow()

    // Called from a non-suspending network interceptor
    fun onUnauthorized() {
        _sessionExpired.tryEmit(Unit)
    }
}

// Not found in FAS — standalone example
// The default configuration: no buffer, no replay
val events = MutableSharedFlow<String>()

events.tryEmit("lost")        // true, but nobody is subscribed: the value is gone
scope.launch { events.collect { println(it) } }
events.tryEmit("rejected")    // false: a subscriber exists and there is no buffer
events.emit("delivered")      // suspends until the subscriber has received it

// Not found in FAS — standalone example
// StateFlow is a SharedFlow with this exact configuration
// (plus an initial value and distinctUntilChanged)
val stateLike = MutableSharedFlow<Int>(
    replay = 1,
    onBufferOverflow = BufferOverflow.DROP_OLDEST
)

// From FollowApp Suite — TasksViewModel.kt
// The "Undo" snackbar is NOT a SharedFlow event. It is state: the pending
// task ids live in the UI state until the UI reports what happened.
fun onQuickDeleteTask(taskId: String) {
    viewModelScope.launch {
        // ...
        moveTaskToTrashUseCase(taskId)
        _uiState.update { it.copy(snackbarUndoTaskIds = listOf(taskId), snackbarIsArchiveUndo = false) }
    }
}

fun onSnackbarDismissed() {
    _uiState.update { it.copy(snackbarUndoTaskIds = emptyList()) }
}

// From FollowApp Suite — TasksScreen.kt
// The UI shows the snackbar when the state says so, then acknowledges it.
// If the screen rotates in between, the state is still there: nothing is lost.
LaunchedEffect(uiState.snackbarUndoTaskIds) {
    if (uiState.snackbarUndoTaskIds.isEmpty()) return@LaunchedEffect
    val message = if (uiState.snackbarIsArchiveUndo) archiveMessage else deleteMessage
    val result = snackbarHostState.showSnackbar(
        message = message,
        actionLabel = undoLabel,
        duration = SnackbarDuration.Short
    )
    if (result == SnackbarResult.ActionPerformed) {
        onUndoDelete()
    } else {
        onSnackbarDismissed()
    }
}
```

## The Interview (The Hot Seat)

**Question**: What is the difference between `SharedFlow` and [`StateFlow`]({{ "/en/02-coroutines-flow/stateflow/" | relative_url }}), and when would you choose a `SharedFlow`?

**Senior Answer**: Both are [hot streams]({{ "/en/glossary/hot-stream/" | relative_url }}) that broadcast to every [collector]({{ "/en/glossary/collector/" | relative_url }}), and in fact [`StateFlow`]({{ "/en/02-coroutines-flow/stateflow/" | relative_url }}) is a `SharedFlow` with a fixed configuration: replay of one, drop-oldest overflow, a mandatory initial value, and equality filtering built in. That configuration makes it a **[state holder]({{ "/en/glossary/state-holder/" | relative_url }})**: there is always a current value readable through `.value`, a new [collector]({{ "/en/glossary/collector/" | relative_url }}) gets it immediately, and writing an equal value does nothing. A `SharedFlow` makes none of those assumptions. It has no current value and no initial value, it delivers equal values every time, and replay, buffer and overflow behavior are all mine to configure. So I choose [`StateFlow`]({{ "/en/02-coroutines-flow/stateflow/" | relative_url }}) for "what is true now", which is most UI state, and `SharedFlow` when I need broadcast semantics without the "current value" idea. Typical cases are an app-wide signal several components must react to, like a session expiring, or sharing one [upstream]({{ "/en/glossary/upstream/" | relative_url }}) connection among several consumers with [`shareIn`]({{ "/en/glossary/share-in/" | relative_url }}). I also keep in mind what `SharedFlow` is not. It is not a queue, because every [collector]({{ "/en/glossary/collector/" | relative_url }}) gets every value, and with the default configuration it is not even a buffer: values emitted with no subscribers are dropped and [`tryEmit`]({{ "/en/glossary/try-emit/" | relative_url }}) fails whenever someone is subscribed. When something must be processed exactly once by one consumer, I use a [`Channel`]({{ "/en/glossary/channel/" | relative_url }}) instead.

**Question**: A ViewModel exposes navigation events through [`MutableSharedFlow<NavEvent>()`]({{ "/en/glossary/mutable-shared-flow/" | relative_url }}), and the screen collects them with [`repeatOnLifecycle(STARTED)`]({{ "/en/glossary/repeat-on-lifecycle/" | relative_url }}). QA reports that navigation sometimes does not happen after the app comes back from the background. Why, and how do you fix it?

**Senior Answer**: The default [`MutableSharedFlow`]({{ "/en/glossary/mutable-shared-flow/" | relative_url }}) has `replay = 0` and no buffer, so an emission only reaches the [collectors]({{ "/en/glossary/collector/" | relative_url }}) that exist at that exact moment. [`repeatOnLifecycle(STARTED)`]({{ "/en/glossary/repeat-on-lifecycle/" | relative_url }}) correctly cancels the [collector]({{ "/en/glossary/collector/" | relative_url }}) when the app goes to the background. If the ViewModel emits the event then, for example because a network call finished, there are zero subscribers and the event is dropped silently. When the screen comes back it resubscribes, but there is nothing left to receive. Adding `replay = 1` is the tempting fix, and it is wrong: the event would be replayed on every resubscription, so after a rotation the app would navigate twice. There are two sound options. The first, and the one I prefer, is to stop treating it as an event: put the navigation target in the UI state, let the UI navigate when it sees it, and have the UI call back to clear it. That survives the background, rotation and process death, and it is easy to test. The second, when it really must stay an event, is a buffered [`Channel`]({{ "/en/glossary/channel/" | relative_url }}) exposed with [`receiveAsFlow()`]({{ "/en/glossary/receive-as-flow/" | relative_url }}): a value sent with no [collector]({{ "/en/glossary/collector/" | relative_url }}) waits in the buffer until the UI collects again, and each event is delivered to one [collector]({{ "/en/glossary/collector/" | relative_url }}) only once. Even that has an edge case, because an event already taken from the [channel]({{ "/en/glossary/channel/" | relative_url }}) can be lost if the [collector]({{ "/en/glossary/collector/" | relative_url }}) is cancelled mid-handling. That is one more reason I reach for state first.

---

[Back to Chapters]({{ "/" | relative_url }})
