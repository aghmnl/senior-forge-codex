---
layout: page
title: "receiveAsFlow()"
lang: en
permalink: /en/02-coroutines-flow/receive-as-flow/
order: 15
---

## The Theory (The What)

`receiveAsFlow()` turns a [`Channel`]({{ "/en/02-coroutines-flow/channel-hot-streams/" | relative_url }}) (more precisely, any [`ReceiveChannel`]({{ "/en/glossary/receive-channel/" | relative_url }})) into a [`Flow`]({{ "/en/glossary/flow/" | relative_url }}). It does not copy or buffer anything: every time someone calls [`collect`]({{ "/en/glossary/collect/" | relative_url }}) on that [`Flow`]({{ "/en/glossary/flow/" | relative_url }}), the [collector]({{ "/en/glossary/collector/" | relative_url }}) runs a loop of [`receive`]({{ "/en/glossary/receive/" | relative_url }}) on the [channel]({{ "/en/glossary/channel/" | relative_url }}) and emits each value it gets.

That means the result **looks like a [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) but behaves like a [channel]({{ "/en/glossary/channel/" | relative_url }})**:

- **It is hot.** The values live in the [channel]({{ "/en/glossary/channel/" | relative_url }}), not in the [`Flow`]({{ "/en/glossary/flow/" | relative_url }}). Values sent before anyone collects wait in the [channel]({{ "/en/glossary/channel/" | relative_url }})'s buffer (if the capacity allows it), and collecting again later does not start anything from the beginning.
- **Each value is delivered once.** A value taken by one [collector]({{ "/en/glossary/collector/" | relative_url }}) is gone from the [channel]({{ "/en/glossary/channel/" | relative_url }}). With two [collectors]({{ "/en/glossary/collector/" | relative_url }}) at the same time, the values are split between them ([fan-out]({{ "/en/glossary/fan-out/" | relative_url }})); they are not copied to both.
- **Cancelling a [collector]({{ "/en/glossary/collector/" | relative_url }}) does not [close]({{ "/en/glossary/close/" | relative_url }}) the [channel]({{ "/en/glossary/channel/" | relative_url }}).** The collection stops, the [channel]({{ "/en/glossary/channel/" | relative_url }}) stays open, and a new [collector]({{ "/en/glossary/collector/" | relative_url }}) can continue where the previous one left off.
- **The [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) ends when the [channel]({{ "/en/glossary/channel/" | relative_url }}) closes.** If the [channel]({{ "/en/glossary/channel/" | relative_url }}) is closed normally with [`close()`]({{ "/en/glossary/close/" | relative_url }}), the collection completes. If it is closed with an exception, [`collect`]({{ "/en/glossary/collect/" | relative_url }}) throws that exception.

Its sibling is **`consumeAsFlow()`**. It does the same, with two differences: it can be collected **only once** (a second [`collect`]({{ "/en/glossary/collect/" | relative_url }}) throws an [`IllegalStateException`]({{ "/en/glossary/illegal-state-exception/" | relative_url }})), and when that collection ends, for whatever reason, it **cancels the [channel]({{ "/en/glossary/channel/" | relative_url }})**. In other words, [`consumeAsFlow`]({{ "/en/glossary/consume-as-flow/" | relative_url }}) gives ownership of the [channel]({{ "/en/glossary/channel/" | relative_url }}) to the [collector]({{ "/en/glossary/collector/" | relative_url }}); [`receiveAsFlow`]({{ "/en/glossary/receive-as-flow/" | relative_url }}) only lends it.

The opposite direction also exists: `produceIn(scope)` turns a [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) into a [`ReceiveChannel`]({{ "/en/glossary/receive-channel/" | relative_url }}).

## The Senior Perspective (The Why)

- **Its main job in Android: one-shot [events]({{ "/en/glossary/one-shot-event/" | relative_url }}) from a [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}).** The usual pattern is a private [`Channel`]({{ "/en/glossary/channel/" | relative_url }}) with a buffer and a public [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) built with `receiveAsFlow()`. The UI can [collect]({{ "/en/glossary/collect/" | relative_url }}), but it cannot [`send`]({{ "/en/glossary/send/" | relative_url }}), so only the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) produces [events]({{ "/en/glossary/one-shot-event/" | relative_url }}). This is the [channel]({{ "/en/glossary/channel/" | relative_url }}) equivalent of exposing a [`MutableStateFlow`]({{ "/en/glossary/mutable-state-flow/" | relative_url }}) through `asStateFlow()`.
- **Why a [channel]({{ "/en/glossary/channel/" | relative_url }}) and not a [`SharedFlow`]({{ "/en/glossary/sharedflow/" | relative_url }}) for those [events]({{ "/en/glossary/one-shot-event/" | relative_url }}).** A [`SharedFlow`]({{ "/en/02-coroutines-flow/sharedflow/" | relative_url }}) with `replay = 0` delivers each value only to the [collectors]({{ "/en/glossary/collector/" | relative_url }}) that exist at that moment. If the screen is in the background, with [`repeatOnLifecycle`]({{ "/en/glossary/repeat-on-lifecycle/" | relative_url }}) its [collector]({{ "/en/glossary/collector/" | relative_url }}) is cancelled, and an [event]({{ "/en/glossary/one-shot-event/" | relative_url }}) emitted then is lost. A buffered [channel]({{ "/en/glossary/channel/" | relative_url }}) keeps the [event]({{ "/en/glossary/one-shot-event/" | relative_url }}) until someone collects again, and [`receiveAsFlow`]({{ "/en/glossary/receive-as-flow/" | relative_url }}) delivers it to that [collector]({{ "/en/glossary/collector/" | relative_url }}) once. That is exactly the "deliver later, but only once" behavior a navigation or a snackbar needs.
- **The type hides the semantics.** A public `Flow<UiEvent>` looks [cold]({{ "/en/glossary/cold-stream/" | relative_url }}), but it is not: two [collectors]({{ "/en/glossary/collector/" | relative_url }}) do not each get all the [events]({{ "/en/glossary/one-shot-event/" | relative_url }}), and collecting again does not replay anything. That is easy to break without noticing: a second composable that collects the same [`events`]({{ "/en/glossary/one-shot-event/" | relative_url }}) takes half of them. A senior makes sure there is **exactly one [collector]({{ "/en/glossary/collector/" | relative_url }})** for that [flow]({{ "/en/glossary/flow/" | relative_url }}) and documents it.
- **A value received is a value gone, even if it is never handled.** The [channel]({{ "/en/glossary/channel/" | relative_url }}) delivers the [event]({{ "/en/glossary/one-shot-event/" | relative_url }}) when the [collector]({{ "/en/glossary/collector/" | relative_url }}) receives it, not when the [collector]({{ "/en/glossary/collector/" | relative_url }}) finishes handling it. If the [collector]({{ "/en/glossary/collector/" | relative_url }}) is cancelled in between, for example during a configuration change, the [event]({{ "/en/glossary/one-shot-event/" | relative_url }}) is lost. Collecting on [`Dispatchers.Main.immediate`]({{ "/en/glossary/dispatchers-main-immediate/" | relative_url }}) (which [`repeatOnLifecycle`]({{ "/en/glossary/repeat-on-lifecycle/" | relative_url }}) already uses) makes that window very small, but does not eliminate it. That is why Google's guidance prefers modeling these [events]({{ "/en/glossary/one-shot-event/" | relative_url }}) as **UI state** that the UI consumes and clears: it survives rotation and process death. [`receiveAsFlow`]({{ "/en/glossary/receive-as-flow/" | relative_url }}) is the pragmatic option when the [event]({{ "/en/glossary/one-shot-event/" | relative_url }}) really has to be an [event]({{ "/en/glossary/one-shot-event/" | relative_url }}).
- **[`receiveAsFlow`]({{ "/en/glossary/receive-as-flow/" | relative_url }}) vs [`consumeAsFlow`]({{ "/en/glossary/consume-as-flow/" | relative_url }}) is a [lifecycle]({{ "/en/glossary/lifecycle/" | relative_url }}) decision.** If the [channel]({{ "/en/glossary/channel/" | relative_url }}) outlives its [collectors]({{ "/en/glossary/collector/" | relative_url }}) (a [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) [channel]({{ "/en/glossary/channel/" | relative_url }}) collected by a screen that comes and goes), it has to be [`receiveAsFlow`]({{ "/en/glossary/receive-as-flow/" | relative_url }}): with [`consumeAsFlow`]({{ "/en/glossary/consume-as-flow/" | relative_url }}), the first time the screen goes to the background the [channel]({{ "/en/glossary/channel/" | relative_url }}) would be cancelled, and the next collection would throw. [`consumeAsFlow`]({{ "/en/glossary/consume-as-flow/" | relative_url }}) fits when the [channel]({{ "/en/glossary/channel/" | relative_url }}) exists only to feed one collection, and closing it when that collection ends is exactly what you want.
- **Prefer it over `for (value in channel)` when the [consumer]({{ "/en/glossary/producer-consumer/" | relative_url }}) speaks [`Flow`]({{ "/en/glossary/flow/" | relative_url }}).** Once the [channel]({{ "/en/glossary/channel/" | relative_url }}) is a [`Flow`]({{ "/en/glossary/flow/" | relative_url }}), all the operators ([`map`]({{ "/en/glossary/map-operator/" | relative_url }}), [`filter`]({{ "/en/glossary/filter/" | relative_url }}), [`debounce`]({{ "/en/glossary/debounce/" | relative_url }}), [`catch`]({{ "/en/glossary/catch/" | relative_url }})) and the [lifecycle]({{ "/en/glossary/lifecycle/" | relative_url }})-aware collection APIs work on it with no extra code.

## Code in Action

```kotlin
// Not found in FAS — standalone example
// The ViewModel owns the channel; the UI only sees a Flow it can collect.
class CheckoutViewModel : ViewModel() {

    private val _events = Channel<CheckoutEvent>(Channel.BUFFERED)
    val events: Flow<CheckoutEvent> = _events.receiveAsFlow()   // exactly one collector

    fun onPayClicked() {
        viewModelScope.launch {
            val result = repository.pay()
            _events.send(
                if (result.isSuccess) CheckoutEvent.GoToReceipt
                else CheckoutEvent.ShowError(result.message)
            )
        }
    }
}

// Not found in FAS — standalone example
// One collector, tied to the lifecycle. If the payment finishes while the app is
// in the background, the event waits in the buffer and is delivered on return.
@Composable
fun CheckoutScreen(viewModel: CheckoutViewModel, onReceipt: () -> Unit) {
    val lifecycleOwner = LocalLifecycleOwner.current
    LaunchedEffect(viewModel, lifecycleOwner) {
        lifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
            viewModel.events.collect { event ->
                when (event) {
                    CheckoutEvent.GoToReceipt -> onReceipt()
                    is CheckoutEvent.ShowError -> snackbarHost.showSnackbar(event.message)
                }
            }
        }
    }
}

// Not found in FAS — standalone example
// The fan-out trap: two collectors on the same receiveAsFlow split the events.
// The banner and the logger each see only some of them.
launch { viewModel.events.collect { showBanner(it) } }
launch { viewModel.events.collect { analytics.log(it) } }   // steals events from the banner

// Not found in FAS — standalone example
// consumeAsFlow: the channel lives only for this collection. When it ends,
// the channel is cancelled; collecting the same flow again throws.
val progress = Channel<Int>(Channel.CONFLATED)
progress.consumeAsFlow()
    .map { "$it%" }
    .collect { label.text = it }
```

## The Interview (The Hot Seat)

**Question**: What does `receiveAsFlow()` do, and why is it the usual way to expose one-shot [events]({{ "/en/glossary/one-shot-event/" | relative_url }}) from a [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) instead of a [`SharedFlow`]({{ "/en/glossary/sharedflow/" | relative_url }})?

**Senior Answer**: It wraps a [channel]({{ "/en/glossary/channel/" | relative_url }}) in a [`Flow`]({{ "/en/glossary/flow/" | relative_url }}): each collection runs a [`receive`]({{ "/en/glossary/receive/" | relative_url }}) loop on the [channel]({{ "/en/glossary/channel/" | relative_url }}) and emits what it gets. So the result keeps the [channel]({{ "/en/glossary/channel/" | relative_url }})'s semantics. It is hot, a value is delivered to exactly one [collector]({{ "/en/glossary/collector/" | relative_url }}), cancelling the [collector]({{ "/en/glossary/collector/" | relative_url }}) leaves the [channel]({{ "/en/glossary/channel/" | relative_url }}) open, and the [flow]({{ "/en/glossary/flow/" | relative_url }}) completes when the [channel]({{ "/en/glossary/channel/" | relative_url }}) is closed. For one-shot [events]({{ "/en/glossary/one-shot-event/" | relative_url }}), like a navigation or a snackbar, that is what you want. With a private buffered [channel]({{ "/en/glossary/channel/" | relative_url }}) and a public `receiveAsFlow()`, the UI can only [collect]({{ "/en/glossary/collect/" | relative_url }}), and an [event]({{ "/en/glossary/one-shot-event/" | relative_url }}) sent while the screen is in the background, with its [collector]({{ "/en/glossary/collector/" | relative_url }}) cancelled by [`repeatOnLifecycle`]({{ "/en/glossary/repeat-on-lifecycle/" | relative_url }}), waits in the buffer and is delivered once when the screen comes back. A [`SharedFlow`]({{ "/en/glossary/sharedflow/" | relative_url }}) with no replay would have dropped it, because there was nobody subscribed, and adding replay would deliver it again after every rotation. Two caveats I keep in mind: it must have a single [collector]({{ "/en/glossary/collector/" | relative_url }}), because two [collectors]({{ "/en/glossary/collector/" | relative_url }}) split the [events]({{ "/en/glossary/one-shot-event/" | relative_url }}) instead of both receiving them; and an [event]({{ "/en/glossary/one-shot-event/" | relative_url }}) already received can still be lost if the [collector]({{ "/en/glossary/collector/" | relative_url }}) is cancelled before handling it. That is why, when I can, I model the [event]({{ "/en/glossary/one-shot-event/" | relative_url }}) as UI state that the UI consumes and clears, and keep [`receiveAsFlow`]({{ "/en/glossary/receive-as-flow/" | relative_url }}) for the cases that really are [events]({{ "/en/glossary/one-shot-event/" | relative_url }}).

**Question**: What is the difference between `receiveAsFlow()` and `consumeAsFlow()`, and what goes wrong if you use `consumeAsFlow()` for a [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }})'s [event]({{ "/en/glossary/one-shot-event/" | relative_url }}) [channel]({{ "/en/glossary/channel/" | relative_url }})?

**Senior Answer**: Both turn a [channel]({{ "/en/glossary/channel/" | relative_url }}) into a [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) with the same per-value behavior. The difference is ownership. [`receiveAsFlow`]({{ "/en/glossary/receive-as-flow/" | relative_url }}) only borrows the [channel]({{ "/en/glossary/channel/" | relative_url }}): it can be collected many times, one after another or even concurrently, and when a collection ends the [channel]({{ "/en/glossary/channel/" | relative_url }}) stays open. [`consumeAsFlow`]({{ "/en/glossary/consume-as-flow/" | relative_url }}) takes ownership: it can be collected only once, a second collection throws an [`IllegalStateException`]({{ "/en/glossary/illegal-state-exception/" | relative_url }}), and when that collection ends, normally or by cancellation, it cancels the [channel]({{ "/en/glossary/channel/" | relative_url }}). In a [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) the screen collects with [`repeatOnLifecycle`]({{ "/en/glossary/repeat-on-lifecycle/" | relative_url }}), so the collection is cancelled every time the app goes to the background. With [`consumeAsFlow`]({{ "/en/glossary/consume-as-flow/" | relative_url }}), that first cancellation would [cancel]({{ "/en/glossary/cancel/" | relative_url }}) the [channel]({{ "/en/glossary/channel/" | relative_url }}): from then on the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }})'s [`send`]({{ "/en/glossary/send/" | relative_url }}) would fail and the next collection, when the user returns, would throw. The [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }})'s [channel]({{ "/en/glossary/channel/" | relative_url }}) outlives each collection, so it needs [`receiveAsFlow`]({{ "/en/glossary/receive-as-flow/" | relative_url }}). I use [`consumeAsFlow`]({{ "/en/glossary/consume-as-flow/" | relative_url }}) only when the [channel]({{ "/en/glossary/channel/" | relative_url }}) exists just to feed one collection, and closing it when that collection ends is the behavior I want.

---

[Back to Chapters]({{ "/" | relative_url }})
