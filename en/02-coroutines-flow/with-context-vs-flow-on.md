---
layout: page
title: "withContext vs flowOn"
lang: en
permalink: /en/02-coroutines-flow/with-context-vs-flow-on/
order: 6
---

## The Theory (The What)

Both [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}) and [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) move work to a different [`Dispatcher`]({{ "/en/glossary/dispatcher/" | relative_url }}). They are not interchangeable, because they operate on different things: `withContext` on **one suspending call**, [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) on **a stream**.

[`withContext(context) { }`]({{ "/en/glossary/with-context/" | relative_url }}) is a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}). It suspends the calling [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}), runs the block on [`context`]({{ "/en/glossary/coroutine-context/" | relative_url }}), and resumes the caller — on its original context — with the single value the block returned. It is imperative and it happens *now*: the [context]({{ "/en/glossary/coroutine-context/" | relative_url }}) is changed for the duration of that block and restored afterwards. This is the mechanism behind [Main-Safety]({{ "/en/02-coroutines-flow/main-safety/" | relative_url }}) for one-shot work.

[`flowOn(context)`]({{ "/en/glossary/flow-on/" | relative_url }}) is a [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) operator. It changes the context of everything [upstream]({{ "/en/glossary/upstream/" | relative_url }}) of it — the builder and the operators declared above — and leaves everything [downstream]({{ "/en/glossary/downstream/" | relative_url }}) running in the collector's context. It is declarative: writing it changes nothing until somebody [collects]({{ "/en/glossary/collect/" | relative_url }}) the flow, and it applies to *every* value the flow will ever emit, not to a single call.

The reason [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) has to exist at all is [context preservation]({{ "/en/glossary/context-preservation/" | relative_url }}): a flow must [emit]({{ "/en/glossary/emit/" | relative_url }}) from the same context in which it is collected. So the obvious move — wrapping the emission — is illegal:

```kotlin
// Throws IllegalStateException: "Flow invariant is violated"
flow { withContext(Dispatchers.IO) { emit(readFile()) } }
```

[`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) is the sanctioned alternative. It does not wrap an emission; it re-hosts the whole upstream in another coroutine and hands the values across a channel — which is also why it [buffers]({{ "/en/glossary/buffer/" | relative_url }}) as a side effect.

## The Senior Perspective (The Why)

- **The decision is made by the return type, not by taste.** A [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) returning `T` uses [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}); a function returning `Flow<T>` uses [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}). Reaching for `withContext` inside a `flow { }` builder is not a style choice — it is a runtime crash waiting for the first emission, and it compiles perfectly.
- **[`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) is upstream-only, and position is the API.** Operators written after it run wherever the collector runs. That asymmetry is a feature: put the expensive parsing and the I/O above the [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}), leave the cheap mapping that feeds UI state below it, and you have described a two-thread pipeline in one line. Writing [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) at the end of a chain in a ViewModel — a common habit — moves the *whole* chain off Main, including the mapping that was meant to run there.
- **[`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) changes concurrency, not just threading.** [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}) is a hand-off: the caller waits. [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) inserts a channel, so the producer can run ahead of the collector — the same behaviour as [`buffer`]({{ "/en/glossary/buffer/" | relative_url }}). That makes pipelines faster and makes emission timing in tests less predictable. If a test starts failing after you add a [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}), this is usually why, and the fix is a deterministic [`TestDispatcher`]({{ "/en/glossary/test-dispatcher/" | relative_url }}), not a [`delay`]({{ "/en/glossary/delay/" | relative_url }}).
- **Most Android flows need neither.** A [Room]({{ "/en/glossary/room/" | relative_url }}) [DAO]({{ "/en/glossary/dao/" | relative_url }}) `Flow` already emits on Room's own executor, [DataStore]({{ "/en/glossary/datastore/" | relative_url }}) reads on IO, and a [Retrofit]({{ "/en/glossary/retrofit/" | relative_url }}) call suspends on [OkHttp]({{ "/en/glossary/okhttp/" | relative_url }})'s pool. Adding [`flowOn(Dispatchers.IO)`]({{ "/en/glossary/flow-on/" | relative_url }}) on top of them buys nothing, costs a channel, and tells the next reader that the source was not [main-safe]({{ "/en/02-coroutines-flow/main-safety/" | relative_url }}) — which is false. Add it only when *you* wrote the blocking producer.
- **Both belong in the data layer.** The rule from [Main-Safety]({{ "/en/02-coroutines-flow/main-safety/" | relative_url }}) does not change for streams: the function that does the blocking work declares where it runs. A ViewModel that has to remember [`.flowOn(IO)`]({{ "/en/glossary/flow-on/" | relative_url }}) on every repository call is a repository that broke its contract.
- **[`flowOn(Dispatchers.Main)`]({{ "/en/glossary/flow-on/" | relative_url }}) almost never means what people think.** It does not force collection onto Main — the collector's [scope]({{ "/en/glossary/coroutine-scope/" | relative_url }}) decides that. It forces the *producer* onto Main, which is the opposite of what anyone wants.

## Code in Action

```kotlin
// From FollowApp Suite — BackupManager.kt
// One-shot, returns a single value → withContext. The blocking stream write
// lives inside the function, so no caller has to remember the dispatcher.
suspend fun exportTo(uri: Uri): Result<Unit> = withContext(Dispatchers.IO) {
    runCatching {
        val json = jsonOf(content)
        context.contentResolver.openOutputStream(uri, "wt").use { stream ->
            requireNotNull(stream) { "Cannot open destination" }
            stream.write(json.toByteArray(Charsets.UTF_8))
        }
    }.onFailure { Log.e(TAG, "Backup export failed", it) }
}

// From FollowApp Suite — TasksViewModel.kt
// CPU-bound date math inside a launch → withContext(Default), not IO
viewModelScope.launch {
    // Date math off the main thread: pattern scans over months/years
    // must never stall input dispatching (popup ANR)
    val suggested = withContext(Dispatchers.Default) {
        val settings = getRecurrenceSettingsUseCase().first()
        RecurrenceCalculator.suggestPatternDueDate(rule, now, zone, settings.holidays)
    }
    _uiState.update { it.copy(form = it.form.copy(dueDate = suggested)) }
}

// From FollowApp Suite — TaskRepositoryImpl.kt
// A stream — and deliberately NO flowOn: Room already emits off the main
// thread, and the mapping is cheap enough to run wherever the collector runs.
override fun getActiveTasks(sort: ListSort): Flow<List<Task>> {
    return taskDao.getActiveTasksStream(sort.name).map { entities ->
        entities.map { it.toDomain() }
    }
}

// Not found in FAS — standalone example
// A producer we wrote ourselves, doing blocking I/O: this is where flowOn earns its place.
fun importedFiles(dir: File): Flow<Backup> = flow {
    dir.listFiles().orEmpty().forEach { file ->
        emit(parseBackup(file.readText()))   // blocking read + parse
    }
}.flowOn(ioDispatcher)                       // upstream (read + parse) runs on IO

// Collected from the ViewModel: the mapping below stays on Main by design
viewModelScope.launch {
    importedFiles(dir)
        .map { it.toUiModel() }              // downstream: Main
        .collect { _uiState.value = it }     // downstream: Main
}
```

## The Interview (The Hot Seat)

**Question**: When do you use `withContext` and when [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}), and what happens if you use `withContext` inside a `flow { }` builder?

**Senior Answer**: [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}) is for a single suspending computation that returns one value: it suspends the caller, runs the block on the target [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}), and resumes the caller on its original context. [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) is for a stream: it is a declarative operator that changes the context of everything [upstream]({{ "/en/glossary/upstream/" | relative_url }}) of it and leaves the [downstream]({{ "/en/glossary/downstream/" | relative_url }}) running wherever the collector runs. So the signature decides — `suspend fun T` takes `withContext`, `fun Flow<T>` takes [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}). Using `withContext` around an [`emit`]({{ "/en/glossary/emit/" | relative_url }}) inside a `flow { }` compiles and then throws [`IllegalStateException: Flow invariant is violated`]({{ "/en/glossary/illegal-state-exception/" | relative_url }}) on the first emission, because of [context preservation]({{ "/en/glossary/context-preservation/" | relative_url }}): a flow has to emit from the same context it is collected in, so that emissions stay sequential and exceptions stay attributable. [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) is the sanctioned way to cross that boundary — it re-hosts the upstream in its own coroutine and passes values over a channel. Two consequences I would mention: position matters, because [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) only affects what is written above it, so I put it immediately after the blocking producer and keep the cheap UI mapping below it; and [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) implies a [buffer]({{ "/en/glossary/buffer/" | relative_url }}), so it changes concurrency too — the producer can run ahead of the collector, which is usually a win but makes emission timing in tests less predictable.

**Question**: A teammate adds [`.flowOn(Dispatchers.IO)`]({{ "/en/glossary/flow-on/" | relative_url }}) to every repository function that returns a `Flow`, including the ones backed by Room. What do you tell them?

**Senior Answer**: That most of those are redundant and one of them may be in the wrong place. A [Room]({{ "/en/glossary/room/" | relative_url }}) [DAO]({{ "/en/glossary/dao/" | relative_url }}) `Flow` already emits on Room's own query executor, and [DataStore]({{ "/en/glossary/datastore/" | relative_url }}) already reads on IO — they are [main-safe]({{ "/en/02-coroutines-flow/main-safety/" | relative_url }}) by contract. Wrapping them adds a channel hop and, worse, signals to the next reader that the source was unsafe, which sends them looking for a bug that does not exist. In our own `TaskRepositoryImpl` the mapping from entity to domain model has no [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) on purpose: Room is already off Main and the mapping is cheap. Where [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) *is* right is a producer we wrote ourselves that blocks — reading files, parsing JSON, a synchronous [SDK]({{ "/en/glossary/sdk/" | relative_url }}) — and there it goes immediately after that producer, in the data layer, not in the ViewModel. I would also check the position: [`.flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) at the very end of a chain in a ViewModel moves the *entire* chain off Main, including mapping that was meant to feed UI state, and [`flowOn(Dispatchers.Main)`]({{ "/en/glossary/flow-on/" | relative_url }}) does not do what its name suggests to a reader — it pins the producer to Main instead of the collector. Finally, I would inject the dispatcher with an [`@IoDispatcher`]({{ "/en/glossary/io-dispatcher/" | relative_url }}) qualifier rather than hardcoding [`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}), so a test can swap in a [`TestDispatcher`]({{ "/en/glossary/test-dispatcher/" | relative_url }}) and assert the behaviour deterministically.

---

[Back to Chapters]({{ "/" | relative_url }})
