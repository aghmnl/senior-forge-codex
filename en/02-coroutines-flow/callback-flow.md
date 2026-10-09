---
layout: page
title: "callbackFlow"
lang: en
permalink: /en/02-coroutines-flow/callback-flow/
order: 16
---

## The Theory (The What)

Many Android and [SDK]({{ "/en/glossary/sdk/" | relative_url }}) [APIs]({{ "/en/glossary/api/" | relative_url }}) do not return values: they call you back. You register a [listener]({{ "/en/glossary/listener/" | relative_url }}), and the [API]({{ "/en/glossary/api/" | relative_url }}) invokes it every time something happens (a new location, a sensor reading, a network change, a download progress). `callbackFlow { }` is the builder that turns that kind of [API]({{ "/en/glossary/api/" | relative_url }}) into a [`Flow`]({{ "/en/glossary/flow/" | relative_url }}).

Inside the block you do three things:

1. **Register the [callback]({{ "/en/glossary/callbacks/" | relative_url }}).** Each time it fires, it puts the value into the [flow]({{ "/en/glossary/flow/" | relative_url }}) with [`trySend(value)`]({{ "/en/glossary/try-send/" | relative_url }}). The [callback]({{ "/en/glossary/callbacks/" | relative_url }}) cannot suspend, so it cannot call [`send`]({{ "/en/glossary/send/" | relative_url }}) or [`emit`]({{ "/en/glossary/emit/" | relative_url }}); [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) is the non-suspending way in.
2. **Signal the end, if the [API]({{ "/en/glossary/api/" | relative_url }}) has one.** When the [API]({{ "/en/glossary/api/" | relative_url }}) reports that it is done, the [callback]({{ "/en/glossary/callbacks/" | relative_url }}) calls [`close()`]({{ "/en/glossary/close/" | relative_url }}); when it reports an error, `close(exception)`, and the [collector]({{ "/en/glossary/collector/" | relative_url }}) receives that exception.
3. **End with `awaitClose { }`.** It suspends the block while the [flow]({{ "/en/glossary/flow/" | relative_url }}) is being collected, and when the collection stops, for any reason, it runs its lambda: that is where you **unregister the [callback]({{ "/en/glossary/callbacks/" | relative_url }})**.

The block runs in a [`ProducerScope`]({{ "/en/glossary/producer-scope/" | relative_url }}), which is both a [`CoroutineScope`]({{ "/en/glossary/coroutine-scope/" | relative_url }}) and a [`SendChannel`]({{ "/en/glossary/send-channel/" | relative_url }}). Behind the scenes there is a [`Channel`]({{ "/en/02-coroutines-flow/channel-hot-streams/" | relative_url }}) between the [callback]({{ "/en/glossary/callbacks/" | relative_url }}) and the [collector]({{ "/en/glossary/collector/" | relative_url }}): the [callback]({{ "/en/glossary/callbacks/" | relative_url }}) sends into it and the [collector]({{ "/en/glossary/collector/" | relative_url }}) receives from it. That [channel]({{ "/en/glossary/channel/" | relative_url }}) is what lets values cross from a [callback]({{ "/en/glossary/callbacks/" | relative_url }}), possibly on another [thread]({{ "/en/glossary/thread/" | relative_url }}), into the [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) that collects. By default it has a buffer of 64 values (`BUFFERED`), which can be changed by applying [`buffer(...)`]({{ "/en/glossary/buffer/" | relative_url }}) or [`conflate()`]({{ "/en/glossary/conflate/" | relative_url }}) to the resulting [flow]({{ "/en/glossary/flow/" | relative_url }}).

The resulting [flow]({{ "/en/glossary/flow/" | relative_url }}) is **[cold]({{ "/en/glossary/cold-stream/" | relative_url }})**: nothing is registered until someone collects, and each [collector]({{ "/en/glossary/collector/" | relative_url }}) runs the block again, so each one registers its own [callback]({{ "/en/glossary/callbacks/" | relative_url }}).

[`awaitClose`]({{ "/en/glossary/await-close/" | relative_url }}) is not optional. If the block finishes without it, the [flow]({{ "/en/glossary/flow/" | relative_url }}) fails with an [`IllegalStateException`]({{ "/en/glossary/illegal-state-exception/" | relative_url }}). This is what distinguishes [`callbackFlow`]({{ "/en/glossary/callback-flow/" | relative_url }}) from its more general sibling, [`channelFlow`]({{ "/en/glossary/channel-flow/" | relative_url }}), which does not require it.

## The Senior Perspective (The Why)

- **One value or many decides the tool.** If the [callback]({{ "/en/glossary/callbacks/" | relative_url }}) fires once (a single request with [`onSuccess`]({{ "/en/glossary/on-success-on-failure/" | relative_url }})/[`onFailure`]({{ "/en/glossary/on-success-on-failure/" | relative_url }})), the right bridge is [`suspendCancellableCoroutine`]({{ "/en/glossary/suspend-cancellable-coroutine/" | relative_url }}), which turns it into a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) that returns that value. [`callbackFlow`]({{ "/en/glossary/callback-flow/" | relative_url }}) is for [callbacks]({{ "/en/glossary/callbacks/" | relative_url }}) that fire repeatedly. Using a [flow]({{ "/en/glossary/flow/" | relative_url }}) for a single result forces the caller to [collect]({{ "/en/glossary/collect/" | relative_url }}) something that is really a function call.
- **[`awaitClose`]({{ "/en/glossary/await-close/" | relative_url }}) ties the [listener]({{ "/en/glossary/listener/" | relative_url }})'s lifetime to the collection.** That is the main benefit. When the [collector]({{ "/en/glossary/collector/" | relative_url }}) is cancelled (the screen goes to the background with [`repeatOnLifecycle`]({{ "/en/glossary/repeat-on-lifecycle/" | relative_url }}), the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) is cleared), [`awaitClose`]({{ "/en/glossary/await-close/" | relative_url }}) runs and the [listener]({{ "/en/glossary/listener/" | relative_url }}) is unregistered. A [listener]({{ "/en/glossary/listener/" | relative_url }}) registered by hand in a constructor or an [`init`]({{ "/en/glossary/init/" | relative_url }}) block, by contrast, lives as long as its owner, and if nobody remembers to unregister it, that is a memory leak or work nobody is waiting for (GPS, sensors, battery).
- **Every [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) can fail, so the buffer is a design decision.** With the default `BUFFERED` capacity, a [callback]({{ "/en/glossary/callbacks/" | relative_url }}) that fires faster than the [collector]({{ "/en/glossary/collector/" | relative_url }}) consumes fills the buffer and [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) starts failing silently. For "only the latest matters" (location, sensors), apply [`conflate()`]({{ "/en/glossary/conflate/" | relative_url }}) or [`buffer(Channel.CONFLATED)`]({{ "/en/glossary/buffer/" | relative_url }}). If every value matters and the volume is bounded, a larger or `UNLIMITED` buffer. At a minimum, check the result and log failures.
- **[Cold]({{ "/en/glossary/cold-stream/" | relative_url }}) means one registration per [collector]({{ "/en/glossary/collector/" | relative_url }}).** Two screens collecting the same [`callbackFlow`]({{ "/en/glossary/callback-flow/" | relative_url }}) register two [listeners]({{ "/en/glossary/listener/" | relative_url }}) on the system. If the source is expensive, share it: [`shareIn`]({{ "/en/glossary/share-in/" | relative_url }}) or [`stateIn`]({{ "/en/glossary/state-in/" | relative_url }}) with [`WhileSubscribed`]({{ "/en/glossary/while-subscribed/" | relative_url }}) keeps a single registration while there is at least one [subscriber]({{ "/en/glossary/collector/" | relative_url }}) and unregisters when the last one leaves.
- **Errors go through `close(cause)`, not [`throw`]({{ "/en/glossary/throw/" | relative_url }}).** An exception thrown inside the [callback]({{ "/en/glossary/callbacks/" | relative_url }}) runs on the [API]({{ "/en/glossary/api/" | relative_url }})'s [thread]({{ "/en/glossary/thread/" | relative_url }}), outside the [flow]({{ "/en/glossary/flow/" | relative_url }}): it crashes that [thread]({{ "/en/glossary/thread/" | relative_url }}) or is swallowed by the [SDK]({{ "/en/glossary/sdk/" | relative_url }}), and the [collector]({{ "/en/glossary/collector/" | relative_url }}) never sees it. Calling `close(exception)` makes the collection fail with that exception, where [`catch`]({{ "/en/glossary/catch/" | relative_url }}) [downstream]({{ "/en/glossary/downstream/" | relative_url }}) can handle it.
- **Why not [`flow { }`]({{ "/en/glossary/flow-builder/" | relative_url }})?** [`flow { }`]({{ "/en/glossary/flow-builder/" | relative_url }}) requires every [`emit`]({{ "/en/glossary/emit/" | relative_url }}) to happen from the [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) that collects; emitting from a [callback]({{ "/en/glossary/callbacks/" | relative_url }}) on another [thread]({{ "/en/glossary/thread/" | relative_url }}) breaks that rule and fails at [runtime]({{ "/en/glossary/runtime/" | relative_url }}) ("[Flow]({{ "/en/glossary/flow/" | relative_url }}) invariant is violated"). [`callbackFlow`]({{ "/en/glossary/callback-flow/" | relative_url }}) exists precisely because the [channel]({{ "/en/glossary/channel/" | relative_url }}) inside it makes cross-[thread]({{ "/en/glossary/thread/" | relative_url }}) sending safe.

## Code in Action

```kotlin
// From FollowApp Suite — InAppUpdateManager.kt
// A Play Core listener registered by hand in init and never unregistered.
// It works because the manager is a @Singleton that lives as long as the app
// and only needs the latest state, so a StateFlow is enough. The listener's
// lifetime is the app's lifetime, not the lifetime of whoever is observing.
private val installListener = InstallStateUpdatedListener { state ->
    if (state.installStatus() == InstallStatus.DOWNLOADED) {
        _flexibleUpdateDownloaded.value = true
    }
}

init {
    appUpdateManager.registerListener(installListener)
}

// Not found in FAS — standalone example
// The same listener as a callbackFlow: registered when someone collects,
// unregistered as soon as the collection stops.
fun AppUpdateManager.installStates(): Flow<InstallState> = callbackFlow {
    val listener = InstallStateUpdatedListener { state ->
        trySend(state)
        if (state.installStatus() == InstallStatus.INSTALLED) close()   // natural end
    }
    registerListener(listener)
    awaitClose { unregisterListener(listener) }
}

// Not found in FAS — standalone example
// A sensor fires very often and only the latest value matters: conflate()
// replaces the pending value, so trySend cannot fail for a full buffer.
fun SensorManager.readings(sensor: Sensor): Flow<SensorEvent> = callbackFlow {
    val listener = object : SensorEventListener {
        override fun onSensorChanged(event: SensorEvent) { trySend(event) }
        override fun onAccuracyChanged(sensor: Sensor, accuracy: Int) = Unit
    }
    registerListener(listener, sensor, SensorManager.SENSOR_DELAY_UI)
    awaitClose { unregisterListener(listener) }
}.conflate()

// Not found in FAS — standalone example
// Several screens, one registration: stateIn with WhileSubscribed keeps a
// single listener while anyone collects, and unregisters 5 s after the last one leaves.
val connectivity: StateFlow<Boolean> = connectivityManager.networkAvailability()
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), initialValue = false)
```

## The Interview (The Hot Seat)

**Question**: How do you convert a [listener]({{ "/en/glossary/listener/" | relative_url }})-based [API]({{ "/en/glossary/api/" | relative_url }}) into a [`Flow`]({{ "/en/glossary/flow/" | relative_url }}), and what is [`awaitClose`]({{ "/en/glossary/await-close/" | relative_url }}) for?

**Senior Answer**: With [`callbackFlow`]({{ "/en/glossary/callback-flow/" | relative_url }}). Inside the block I register the [listener]({{ "/en/glossary/listener/" | relative_url }}), and every time it fires I put the value into the [flow]({{ "/en/glossary/flow/" | relative_url }}) with [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}), because the [listener]({{ "/en/glossary/listener/" | relative_url }}) cannot suspend. If the [API]({{ "/en/glossary/api/" | relative_url }}) reports an end, I call [`close()`]({{ "/en/glossary/close/" | relative_url }}), and if it reports an error, `close(exception)`, so the [collector]({{ "/en/glossary/collector/" | relative_url }}) receives it. The block has to end with [`awaitClose`]({{ "/en/glossary/await-close/" | relative_url }}), which suspends while the [flow]({{ "/en/glossary/flow/" | relative_url }}) is being collected and runs its lambda when the collection stops, and that lambda is where I unregister the [listener]({{ "/en/glossary/listener/" | relative_url }}). That is the real value of [`callbackFlow`]({{ "/en/glossary/callback-flow/" | relative_url }}): the [listener]({{ "/en/glossary/listener/" | relative_url }}) lives exactly as long as someone collects. When the screen goes to the background and [`repeatOnLifecycle`]({{ "/en/glossary/repeat-on-lifecycle/" | relative_url }}) cancels the collection, the [listener]({{ "/en/glossary/listener/" | relative_url }}) is unregistered automatically, so there is no leak and no work nobody is waiting for. If I forget [`awaitClose`]({{ "/en/glossary/await-close/" | relative_url }}), the [flow]({{ "/en/glossary/flow/" | relative_url }}) fails with an [`IllegalStateException`]({{ "/en/glossary/illegal-state-exception/" | relative_url }}). Internally there is a [channel]({{ "/en/glossary/channel/" | relative_url }}) between the [callback]({{ "/en/glossary/callbacks/" | relative_url }}) and the [collector]({{ "/en/glossary/collector/" | relative_url }}), which is what makes it safe to [send]({{ "/en/glossary/send/" | relative_url }}) from the [API]({{ "/en/glossary/api/" | relative_url }})'s [thread]({{ "/en/glossary/thread/" | relative_url }}). And if the [API]({{ "/en/glossary/api/" | relative_url }}) calls back only once, I do not use [`callbackFlow`]({{ "/en/glossary/callback-flow/" | relative_url }}) at all: [`suspendCancellableCoroutine`]({{ "/en/glossary/suspend-cancellable-coroutine/" | relative_url }}) turns it into a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}).

**Question**: Two screens [collect]({{ "/en/glossary/collect/" | relative_url }}) the same [`callbackFlow`]({{ "/en/glossary/callback-flow/" | relative_url }}) of location updates. You see two GPS registrations, and under load some updates never arrive. What is going on, and how do you fix it?

**Senior Answer**: Both symptoms come from how [`callbackFlow`]({{ "/en/glossary/callback-flow/" | relative_url }}) works. It is [cold]({{ "/en/glossary/cold-stream/" | relative_url }}): each [collector]({{ "/en/glossary/collector/" | relative_url }}) runs the block again, so each one registers its own [listener]({{ "/en/glossary/listener/" | relative_url }}), and two screens mean two GPS registrations. The fix is to share it, with [`shareIn`]({{ "/en/glossary/share-in/" | relative_url }}) or [`stateIn`]({{ "/en/glossary/state-in/" | relative_url }}) and [`WhileSubscribed`]({{ "/en/glossary/while-subscribed/" | relative_url }}) in a scope that outlives the screens, so there is a single registration while at least one screen is collecting, and it is unregistered when the last one leaves. The lost updates come from the [channel]({{ "/en/glossary/channel/" | relative_url }}) behind it. Its default buffer holds 64 values, and the [listener]({{ "/en/glossary/listener/" | relative_url }}) uses [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}), which does not wait: when the [collector]({{ "/en/glossary/collector/" | relative_url }}) is slower than the GPS and the buffer is full, [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) fails and, if nobody checks the result, the update disappears silently. For location, only the latest value matters, so the right answer is [`conflate()`]({{ "/en/glossary/conflate/" | relative_url }}): the newest position replaces the pending one, and [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) no longer fails for lack of room. If every value mattered, I would size the buffer for it, and in any case I would check the result of [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) so a failure is visible instead of silent.

---

[Back to Chapters]({{ "/" | relative_url }})
