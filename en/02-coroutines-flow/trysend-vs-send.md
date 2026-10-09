---
layout: page
title: "trySend() vs send()"
lang: en
permalink: /en/02-coroutines-flow/trysend-vs-send/
order: 14
---

## The Theory (The What)

There are two ways to put a value into a [`Channel`]({{ "/en/02-coroutines-flow/channel-hot-streams/" | relative_url }}), and the difference is what happens when the channel has no room.

- **[`send(value)`]({{ "/en/glossary/send/" | relative_url }})** is a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}). If there is room, it adds the value. If there is not (the buffer is full, or it is a [rendezvous]({{ "/en/glossary/channel-capacity/" | relative_url }}) channel and nobody is receiving), it **suspends** until a [receiver]({{ "/en/glossary/receive/" | relative_url }}) makes room. It never loses a value: it waits. Because it suspends, it can only be called from a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}).
- **[`trySend(value)`]({{ "/en/glossary/try-send/" | relative_url }})** is a regular function. It **never waits**: if there is room right now it adds the value, and if there is not, it gives up immediately. It returns a [`ChannelResult`]({{ "/en/glossary/channel-result/" | relative_url }}) that says what happened: [`isSuccess`]({{ "/en/glossary/channel-result/" | relative_url }}) when the value was added, [`isFailure`]({{ "/en/glossary/channel-result/" | relative_url }}) when it was not, and [`isClosed`]({{ "/en/glossary/channel-result/" | relative_url }}) when it failed because the channel is closed. Because it does not suspend, it can be called from anywhere, including code that is not a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}).

They also differ when the channel is **closed**. [`send`]({{ "/en/glossary/send/" | relative_url }}) throws an exception. [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) does not throw: it returns a closed result.

There is a third option for code that runs on a background [thread]({{ "/en/glossary/thread/" | relative_url }}) outside [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}): **[`trySendBlocking(value)`]({{ "/en/glossary/try-send-blocking/" | relative_url }})** blocks that [thread]({{ "/en/glossary/thread/" | relative_url }}) until there is room. It must never run on the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}).

[`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) replaced the older [`offer()`]({{ "/en/glossary/offer/" | relative_url }}), which threw an exception on a closed channel and is now deprecated.

## The Senior Perspective (The Why)

- **The real question is "can this code suspend?".** Inside a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}), [`send`]({{ "/en/glossary/send/" | relative_url }}) is the right default: it applies [backpressure]({{ "/en/glossary/backpressure/" | relative_url }}) (a fast [producer]({{ "/en/glossary/producer-consumer/" | relative_url }}) waits for a slow [consumer]({{ "/en/glossary/producer-consumer/" | relative_url }})) and never loses a value. [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) exists for code that **cannot** suspend: a click [listener]({{ "/en/glossary/listener/" | relative_url }}), a [callback]({{ "/en/glossary/callbacks/" | relative_url }}) from an [SDK]({{ "/en/glossary/sdk/" | relative_url }}), a system broadcast. It is not a "faster [`send`]({{ "/en/glossary/send/" | relative_url }})"; it is [`send`]({{ "/en/glossary/send/" | relative_url }}) for places where waiting is impossible.
- **[`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) can fail, and by default the failure is silent.** Calling `trySend(event)` and ignoring the result means that, when the buffer is full or the channel is closed, the event simply disappears, with no error and no log. Every [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) should answer the question "what happens when this fails?". Either the result is checked and handled (log it, count it, fall back), or the channel is configured so that failure is impossible except when it is closed.
- **Capacity decides whether [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) can fail.** On a [rendezvous]({{ "/en/glossary/channel-capacity/" | relative_url }}) channel with no [receiver]({{ "/en/glossary/receive/" | relative_url }}) suspended at that moment, [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) fails. On a full [`BUFFERED`]({{ "/en/glossary/channel-capacity/" | relative_url }}) channel it fails. On [`UNLIMITED`]({{ "/en/glossary/channel-capacity/" | relative_url }}), [`CONFLATED`]({{ "/en/glossary/channel-capacity/" | relative_url }}), or a buffer with a drop policy, it only fails when the channel is closed. So choosing [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) and choosing the capacity are one decision: if losing values is not acceptable, the channel needs room for them, or the [producer]({{ "/en/glossary/producer-consumer/" | relative_url }}) has to be able to wait.
- **"Drop" can be correct, but it has to be deliberate.** For location updates or a sensor, only the latest value matters, and losing intermediate ones is the right behavior: a [`CONFLATED`]({{ "/en/glossary/channel-capacity/" | relative_url }}) channel plus [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) says exactly that. For a payment confirmation, losing a value is a bug. The code should make clear which of the two it is.
- **[`trySendBlocking`]({{ "/en/glossary/try-send-blocking/" | relative_url }}) moves the waiting to a [thread]({{ "/en/glossary/thread/" | relative_url }}).** It is useful when a non-[coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) background [thread]({{ "/en/glossary/thread/" | relative_url }}) (a socket reader, a legacy library) produces values and must respect [backpressure]({{ "/en/glossary/backpressure/" | relative_url }}). On the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) it freezes the UI and can end in an [ANR]({{ "/en/glossary/anr/" | relative_url }}), so it does not belong there.
- **Sometimes the right answer is not a channel at all.** When a [callback]({{ "/en/glossary/callbacks/" | relative_url }}) only needs to publish "the latest value" (a connection status, a purchase verdict), assigning [`MutableStateFlow.value`]({{ "/en/glossary/mutable-state-flow/" | relative_url }}) is simpler: it never suspends, never fails and keeps the latest value for whoever collects. A channel with [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) makes sense when each value matters on its own and must be processed once.

## Code in Action

```kotlin
// Not found in FAS — standalone example
// Inside a coroutine: send waits for room and never loses a value
suspend fun enqueueUploads(queue: SendChannel<File>, files: List<File>) {
    files.forEach { queue.send(it) }      // suspends while the workers are busy
}

// Not found in FAS — standalone example
// From a callback: trySend cannot wait, so the failure is handled explicitly
private val scans = Channel<Barcode>(capacity = 16)

private val listener = BarcodeListener { barcode ->
    val result = scans.trySend(barcode)
    when {
        result.isClosed -> Log.w(TAG, "Scan dropped: scanner stopped")
        result.isFailure -> Log.w(TAG, "Scan dropped: queue full")
    }
}

// Not found in FAS — standalone example
// When only the latest value matters, CONFLATED makes trySend unable to fail
// (except on a closed channel): the new value replaces the pending one
private val positions = Channel<Location>(Channel.CONFLATED)

private val locationListener = LocationListener { location ->
    positions.trySend(location)
}

// From FollowApp Suite — BillingConnector.kt
// The same situation, a Play Billing callback that cannot suspend, solved
// without a channel: the result is state, so assigning value is enough.
// It never suspends, never fails, and keeps the latest verdict.
billingClient.queryPurchasesAsync(params) { result, purchases ->
    if (result.responseCode == BillingClient.BillingResponseCode.OK) {
        handlePurchases(purchases)
        if (purchases.none { it.isOwnedProduct() }) {
            _isOwned.value = false
        }
    }
}
```

## The Interview (The Hot Seat)

**Question**: What is the difference between [`send`]({{ "/en/glossary/send/" | relative_url }}) and [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) on a [`Channel`]({{ "/en/02-coroutines-flow/channel-hot-streams/" | relative_url }}), and how do you decide which one to use?

**Senior Answer**: Both put a value into a channel; the difference is what happens when there is no room. [`send`]({{ "/en/glossary/send/" | relative_url }}) is a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}): it waits until a [receiver]({{ "/en/glossary/receive/" | relative_url }}) makes room, so it never loses a value and it gives you [backpressure]({{ "/en/glossary/backpressure/" | relative_url }}) for free, because a fast [producer]({{ "/en/glossary/producer-consumer/" | relative_url }}) is slowed down by a slow [consumer]({{ "/en/glossary/producer-consumer/" | relative_url }}). On a closed channel it throws. [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) is a regular function that never waits: it either adds the value immediately or gives up, and it returns a [`ChannelResult`]({{ "/en/glossary/channel-result/" | relative_url }}) telling you whether it succeeded, failed or found the channel closed. It never throws. So the decision is really about where the code runs. Inside a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) I use [`send`]({{ "/en/glossary/send/" | relative_url }}). From code that cannot suspend, like a [listener]({{ "/en/glossary/listener/" | relative_url }}) or an [SDK]({{ "/en/glossary/sdk/" | relative_url }}) [callback]({{ "/en/glossary/callbacks/" | relative_url }}), I use [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}), and then I have to decide what a failure means: either I check the result and handle it, or I choose a capacity where failure is acceptable or impossible, such as [`CONFLATED`]({{ "/en/glossary/channel-capacity/" | relative_url }}) when only the latest value matters. What I avoid is treating [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) as a faster [`send`]({{ "/en/glossary/send/" | relative_url }}), because ignoring its result turns a full buffer into silently lost data.

**Question**: A [listener]({{ "/en/glossary/listener/" | relative_url }}) calls `channel.trySend(event)` and ignores the result. In production, some events never arrive. What could be happening, and how do you fix it?

**Senior Answer**: [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) only adds the value if there is room at that exact moment, and the code is throwing away the result that says whether it did. There are three typical causes. The channel is [rendezvous]({{ "/en/glossary/channel-capacity/" | relative_url }}), the default, and no [receiver]({{ "/en/glossary/receive/" | relative_url }}) was waiting at that moment, so every event sent while the [consumer]({{ "/en/glossary/producer-consumer/" | relative_url }}) is busy fails. Or it is buffered and the buffer was full because the [consumer]({{ "/en/glossary/producer-consumer/" | relative_url }}) is slower than the [producer]({{ "/en/glossary/producer-consumer/" | relative_url }}). Or the channel was already closed, for example because the screen that consumed it was gone. The fix starts with making the failure visible: check the result, at least log it, so you know which case it is. Then decide what the events are. If every event matters, the channel needs room for them, a larger or [`UNLIMITED`]({{ "/en/glossary/channel-capacity/" | relative_url }}) buffer when the volume is bounded, or the [producer]({{ "/en/glossary/producer-consumer/" | relative_url }}) has to move into a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) and use [`send`]({{ "/en/glossary/send/" | relative_url }}) so it can wait. If only the latest matters, [`CONFLATED`]({{ "/en/glossary/channel-capacity/" | relative_url }}) makes the loss intentional instead of accidental. And if the channel was closed, the bug is in the lifecycle: the [listener]({{ "/en/glossary/listener/" | relative_url }}) has to be unregistered when the [consumer]({{ "/en/glossary/producer-consumer/" | relative_url }}) goes away, which is exactly what [`callbackFlow`]({{ "/en/glossary/callback-flow/" | relative_url }}) with [`awaitClose`]({{ "/en/glossary/await-close/" | relative_url }}) does.

---

[Back to Chapters]({{ "/" | relative_url }})
