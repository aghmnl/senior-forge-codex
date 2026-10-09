---
layout: page
title: "Channel (Hot Streams)"
lang: en
permalink: /en/02-coroutines-flow/channel-hot-streams/
order: 13
---

## The Theory (The What)

A [`Channel<T>`]({{ "/en/glossary/channel/" | relative_url }}) is a **queue between [coroutines]({{ "/en/glossary/coroutines/" | relative_url }})**. One [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) puts values in with [`send`]({{ "/en/glossary/send/" | relative_url }}), another takes them out with [`receive`]({{ "/en/glossary/receive/" | relative_url }}), and **each value is delivered to exactly one receiver**. It works like a blocking queue, except that both operations **suspend** instead of blocking a [thread]({{ "/en/glossary/thread/" | relative_url }}): [`send`]({{ "/en/glossary/send/" | relative_url }}) suspends when there is no room, and [`receive`]({{ "/en/glossary/receive/" | relative_url }}) suspends when there is nothing to take.

A channel is a [hot stream]({{ "/en/glossary/hot-stream/" | relative_url }}). It exists independently of its consumers, and values sent into it wait there until someone takes them, whether or not anyone was listening when they were sent.

Its **capacity** decides when [`send`]({{ "/en/glossary/send/" | relative_url }}) suspends:

- **[`RENDEZVOUS`]({{ "/en/glossary/channel-capacity/" | relative_url }})** (the default, [`Channel<T>()`]({{ "/en/glossary/channel/" | relative_url }})): no buffer at all. [`send`]({{ "/en/glossary/send/" | relative_url }}) suspends until a receiver takes the value, so sender and receiver "meet".
- **[`BUFFERED`]({{ "/en/glossary/channel-capacity/" | relative_url }})**: a fixed buffer (64 by default). [`send`]({{ "/en/glossary/send/" | relative_url }}) only suspends when it is full.
- **[`UNLIMITED`]({{ "/en/glossary/channel-capacity/" | relative_url }})**: a buffer with no limit. [`send`]({{ "/en/glossary/send/" | relative_url }}) never suspends.
- **[`CONFLATED`]({{ "/en/glossary/channel-capacity/" | relative_url }})**: keeps only the latest value. A new one replaces the old one if it was not taken yet.

From code that cannot suspend, such as a callback, [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) adds a value only if there is room right now, and returns a result that says whether it worked. The difference between [`send`]({{ "/en/glossary/send/" | relative_url }}) and [`trySend`]({{ "/en/glossary/try-send/" | relative_url }}) [is a topic of its own]({{ "/en/02-coroutines-flow/trysend-vs-send/" | relative_url }}).

A channel has an **end**. The sender calls [`close()`]({{ "/en/glossary/close/" | relative_url }}) to say that no more values are coming. Receivers still get everything that was already in the buffer, and then a `for (value in channel)` loop finishes normally. Sending to a closed channel throws an exception, and so does calling [`receive()`]({{ "/en/glossary/receive/" | relative_url }}) on one that is closed and empty.

The usual way to create one is the [`produce { }`]({{ "/en/glossary/produce/" | relative_url }}) builder. It launches a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) that sends values, returns the receiving side, and **closes the channel automatically** when the [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) finishes or is cancelled. It is still marked as an experimental API, but it is the idiomatic way to build a producer.

## The Senior Perspective (The Why)

- **Queue, not broadcast: that is the whole difference from [SharedFlow]({{ "/en/02-coroutines-flow/sharedflow/" | relative_url }}).** A [SharedFlow]({{ "/en/02-coroutines-flow/sharedflow/" | relative_url }}) gives every value to *every* [collector]({{ "/en/glossary/collector/" | relative_url }}). A channel gives each value to *one* receiver. With two receivers on the same channel, values are split between them ([fan-out]({{ "/en/glossary/fan-out/" | relative_url }})). That makes a channel the tool for distributing work, and the wrong tool for notifying several listeners.
- **A channel is a resource that has to be closed.** A receiver in `for (value in channel)` waits forever if nobody calls [`close()`]({{ "/en/glossary/close/" | relative_url }}): the [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) never ends, the scope never completes, and whatever it holds leaks. Code that creates channels by hand has to decide who closes them. [`produce { }`]({{ "/en/glossary/produce/" | relative_url }}) solves this by tying the channel's life to a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}): when the producer ends or its scope is cancelled, the channel closes.
- **The default [rendezvous]({{ "/en/glossary/channel-capacity/" | relative_url }}) can hang code.** With no buffer, [`send`]({{ "/en/glossary/send/" | relative_url }}) waits for a receiver. A [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) that sends and then receives on the same [rendezvous]({{ "/en/glossary/channel-capacity/" | relative_url }}) channel, with nobody else around, suspends forever. Choosing the capacity is a design decision, not a detail.
- **[`UNLIMITED`]({{ "/en/glossary/channel-capacity/" | relative_url }}) moves the problem, it does not solve it.** A producer faster than its consumer keeps adding to an unbounded buffer until memory runs out. A bounded buffer ([`BUFFERED`]({{ "/en/glossary/channel-capacity/" | relative_url }}), or an explicit capacity) makes a fast producer wait, which is [backpressure]({{ "/en/glossary/backpressure/" | relative_url }}). Dropping values on purpose is [`CONFLATED`]({{ "/en/glossary/channel-capacity/" | relative_url }}) or a drop policy.
- **Order is preserved, and that is useful.** Values come out in the order they went in. A single [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) that processes commands from a channel handles them **one at a time, in order**, without any [lock]({{ "/en/glossary/lock/" | relative_url }}). That is a simple way to serialize work that must never run in parallel, such as writes to the same file.
- **For UI events, a buffered channel is the usual "event" answer, but not the first one.** Unlike a [SharedFlow]({{ "/en/02-coroutines-flow/sharedflow/" | relative_url }}) without replay, a buffered channel keeps an event sent while the screen is in the background, and delivers it when the UI collects again. It is still not bulletproof: an event already taken from the channel is lost if the [collector]({{ "/en/glossary/collector/" | relative_url }}) is cancelled before handling it. [Android]({{ "/en/glossary/android/" | relative_url }})'s guidance prefers modeling those events as UI state that the UI acknowledges, and using a channel only when something truly is a one-time event.
- **In app code, channels are mostly plumbing.** Flow operators such as [`buffer`]({{ "/en/glossary/buffer/" | relative_url }}), [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) and [`callbackFlow`]({{ "/en/02-coroutines-flow/callback-flow/" | relative_url }}) use channels internally, so most of the time you benefit from them without touching them. Reaching for a raw channel is justified for producer-consumer pipelines, work distribution and serialized processing; for everything else, a Flow or a [StateFlow]({{ "/en/02-coroutines-flow/stateflow/" | relative_url }}) is simpler.

## Code in Action

```kotlin
// Not found in FAS — standalone example
// produce {} creates the channel, runs the producer and closes it on completion.
// The for loop ends by itself when the channel is closed and drained.
fun CoroutineScope.pagesOf(api: TaskApi): ReceiveChannel<List<Task>> = produce {
    var page = 0
    while (true) {
        val tasks = api.fetchPage(page++)
        if (tasks.isEmpty()) break
        send(tasks)                    // suspends if the consumer is behind
    }
}                                      // leaving the block closes the channel

suspend fun importAll(scope: CoroutineScope, api: TaskApi, dao: TaskDao) {
    for (page in scope.pagesOf(api)) {
        dao.insertAll(page)
    }
}

// Not found in FAS — standalone example
// Fan-out: three workers share one queue. Each file is uploaded exactly once,
// by whichever worker is free, and at most three uploads run at the same time.
suspend fun uploadAll(files: List<File>) = coroutineScope {
    val queue = Channel<File>(Channel.UNLIMITED)
    files.forEach { queue.send(it) }
    queue.close()                      // no more work: workers stop when it drains

    repeat(3) {
        launch {
            for (file in queue) upload(file)
        }
    }
}

// Not found in FAS — standalone example
// Serialized processing: one consumer handles commands one at a time, in order,
// so two writes to the same file can never overlap. No lock needed.
class ExportWriter(scope: CoroutineScope, private val file: File) {
    private val commands = Channel<String>(Channel.BUFFERED)

    init {
        scope.launch {
            for (line in commands) file.appendText(line)
        }
    }

    suspend fun write(line: String) = commands.send(line)
}

// Not found in FAS — standalone example
// A buffered channel for one-shot events: an event sent while the screen is in
// the background waits in the buffer instead of being lost
private val _events = Channel<UiEvent>(Channel.BUFFERED)
val events: Flow<UiEvent> = _events.receiveAsFlow()
```

## The Interview (The Hot Seat)

**Question**: What is the difference between a [`Channel`]({{ "/en/glossary/channel/" | relative_url }}), a [`Flow`]({{ "/en/02-coroutines-flow/flow-cold-streams/" | relative_url }}) and a [`SharedFlow`]({{ "/en/02-coroutines-flow/sharedflow/" | relative_url }}), and when would you choose a channel?

**Senior Answer**: A [`Flow`]({{ "/en/02-coroutines-flow/flow-cold-streams/" | relative_url }}) is [cold]({{ "/en/glossary/cold-stream/" | relative_url }}): it is a description that runs its producer from scratch for each [collector]({{ "/en/glossary/collector/" | relative_url }}), so nothing is shared and nothing happens until someone collects. A [`SharedFlow`]({{ "/en/02-coroutines-flow/sharedflow/" | relative_url }}) and a [`Channel`]({{ "/en/glossary/channel/" | relative_url }}) are both [hot]({{ "/en/glossary/hot-stream/" | relative_url }}): they exist independently of their consumers. The difference between those two is how values are delivered. A [`SharedFlow`]({{ "/en/02-coroutines-flow/sharedflow/" | relative_url }}) broadcasts: every [collector]({{ "/en/glossary/collector/" | relative_url }}) receives every value. A [`Channel`]({{ "/en/glossary/channel/" | relative_url }}) is a queue: each value is delivered to exactly one receiver, so with several receivers the values are split between them. It also keeps values in its buffer until someone takes them, while a [`SharedFlow`]({{ "/en/02-coroutines-flow/sharedflow/" | relative_url }}) without replay drops values when nobody is subscribed. So I reach for a channel when each item must be handled exactly once: a producer-consumer pipeline, a pool of workers taking jobs from one queue, or a single consumer that serializes commands so they never run in parallel. For state I use a [`StateFlow`]({{ "/en/02-coroutines-flow/stateflow/" | relative_url }}), for notifying several listeners a [`SharedFlow`]({{ "/en/02-coroutines-flow/sharedflow/" | relative_url }}), and for UI events I first try to model them as state. I use a buffered channel only when something is truly a one-time event, knowing that an event already taken can still be lost if the [collector]({{ "/en/glossary/collector/" | relative_url }}) is cancelled before handling it.

**Question**: A [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) iterates `for (task in channel)` to process work, and QA notices that the screen's scope never completes and the [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) keeps running after the work is done. What is wrong, and how do you fix it?

**Senior Answer**: A `for` loop over a channel only ends when the channel is **closed** and its buffer is empty. If nobody calls [`close()`]({{ "/en/glossary/close/" | relative_url }}), the loop suspends on the next [`receive`]({{ "/en/glossary/receive/" | relative_url }}) forever, waiting for a value that will never come: the [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) never finishes, the scope that launched it never completes, and anything it references stays alive. The fix is to make closing someone's explicit responsibility. The producer calls [`close()`]({{ "/en/glossary/close/" | relative_url }}) when it has sent everything, ideally in a [`finally`]({{ "/en/glossary/finally/" | relative_url }}) block so that a failure also closes it. The better fix is not to manage it by hand at all and create the channel with [`produce { }`]({{ "/en/glossary/produce/" | relative_url }}): it ties the channel to the producer [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) and closes it automatically when that [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) finishes, fails or is cancelled with its scope. The same reasoning applies to the consumer side: if the consumer stops early, it should cancel the channel so the producer does not keep suspending on [`send`]({{ "/en/glossary/send/" | relative_url }}). In general, a raw [`Channel()`]({{ "/en/glossary/channel/" | relative_url }}) without a clear owner is a code smell. I prefer [`produce`]({{ "/en/glossary/produce/" | relative_url }}), or a [`Flow`]({{ "/en/02-coroutines-flow/flow-cold-streams/" | relative_url }}) when nothing needs to be queued at all.

---

[Back to Chapters]({{ "/" | relative_url }})
