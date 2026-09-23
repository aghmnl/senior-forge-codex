---
layout: page
title: "Flow (Cold Streams)"
lang: en
permalink: /en/02-coroutines-flow/flow-cold-streams/
order: 7
---

## The Theory (The What)

A [`Flow<T>`]({{ "/en/glossary/flow/" | relative_url }}) is an asynchronous stream of values that is **cold**: declaring it runs nothing. A flow is a *recipe* — a description of how values will be produced — and the recipe executes only when somebody applies a **terminal operator**. Until then, no query runs, no file is read, no [`emit`]({{ "/en/glossary/emit/" | relative_url }}) happens.

Three pieces make up the model:

- **Builders** produce the flow: `flow { emit(x) }` for arbitrary suspending work, `flowOf(a, b)` for fixed values, `asFlow()` over a collection, and `callbackFlow`/`channelFlow` to bridge a [callback]({{ "/en/glossary/callbacks/" | relative_url }})-based API.
- **Intermediate operators** — `map`, `filter`, `onEach`, [`combine`]({{ "/en/glossary/combine/" | relative_url }}), [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}) — are *declarative*. Each one returns a new `Flow` that wraps the previous one; none of them runs anything. They are as lazy as [`Sequence`]({{ "/en/glossary/sequences/" | relative_url }}) operators, and for the same reason.
- **[Terminal operators]({{ "/en/glossary/terminal-operations/" | relative_url }})** — [`collect`]({{ "/en/glossary/collect/" | relative_url }}), [`first`]({{ "/en/glossary/first/" | relative_url }}), `toList`, `single`, `fold` — are [suspend functions]({{ "/en/glossary/suspend-functions/" | relative_url }}). They start the producer, and they need a [coroutine scope]({{ "/en/glossary/coroutine-scope/" | relative_url }}) to run in.

Because the recipe restarts per collection, **each collector gets its own independent execution**: collect the same `Flow` twice and the producer runs twice. That is precisely what "cold" means, and it is the opposite of a hot stream like [`StateFlow`]({{ "/en/glossary/stateflow/" | relative_url }}), which exists and holds a value whether anyone is listening or not.

Emission is sequential and applies [backpressure]({{ "/en/glossary/backpressure/" | relative_url }}) by default: `emit` suspends until the collector has finished processing that value, so a slow consumer slows the producer instead of filling a queue.

## The Senior Perspective (The Why)

- **"Cold" is a cost model, not a trivia answer.** Two collectors on a [Room]({{ "/en/glossary/room/" | relative_url }})-backed flow means two live queries and two database observers, each re-running on every table change. A `Flow` exposed by a repository and collected from three screens is three times the work. The fix is not to collect less; it is to share one execution — which is what `stateIn`/`shareIn` exist for, and a later topic.
- **Nothing happens until collection, and that is a feature.** Calling `repository.getActiveTasks()` has no side effect: it allocates a description. That is why a repository can return a `Flow` without a scope, without threading decisions and without a lifecycle, and why flows are so testable. The corresponding bug is the mirror image: a flow nobody collects does *nothing*, silently — no error, no log, no warning. A `flow { }` whose logging never appears is almost always an uncollected flow.
- **Choosing the terminal operator is a design decision.** [`first()`]({{ "/en/glossary/first/" | relative_url }}) takes one value and **cancels the producer** — a one-shot read of a live source. `collect` observes forever and the coroutine never completes. Reaching for `first()` on a flow you meant to observe gives you data that silently goes stale; reaching for `collect` where you wanted a snapshot gives you a coroutine that never returns and a caller that hangs.
- **A cold flow's lifetime is the collecting coroutine's lifetime.** It has no lifecycle of its own: cancel the [scope]({{ "/en/glossary/coroutine-scope/" | relative_url }}) and the producer is cancelled at its next [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}). Collecting in [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) ties the stream to the ViewModel, which is usually right; collecting in an `Activity` without `repeatOnLifecycle` keeps the collector alive while the screen is in the background, which is usually a bug.
- **Sequential by default; concurrency is opt-in.** Values arrive in order and one at a time. If the producer should run ahead of the consumer you ask for it with [`buffer`]({{ "/en/glossary/buffer/" | relative_url }}); if it should run on another [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) you ask with [`flowOn`]({{ "/en/glossary/flow-on/" | relative_url }}). Nothing becomes concurrent behind your back, which makes flows far easier to reason about than callback pipelines.
- **The producer must stay exception-transparent.** A `flow { }` builder should not wrap its own emissions in `try/catch`; failures travel [downstream]({{ "/en/glossary/downstream/" | relative_url }}) to the collector, and [`catch`]({{ "/en/glossary/catch/" | relative_url }}) handles them there — only for its [upstream]({{ "/en/glossary/upstream/" | relative_url }}). That is a topic of its own.

## Code in Action

```kotlin
// From FollowApp Suite — LabelOptionDao.kt
// Room returns a cold Flow: the query runs per collector, and re-runs
// whenever the table changes
@Query("SELECT * FROM label_options ORDER BY sort_order ASC, label ASC")
fun getAllOptionsStream(): Flow<List<LabelOptionEntity>>

// From FollowApp Suite — TaskRepositoryImpl.kt
// map() is an intermediate operator: this line runs no query and touches
// no database. It only describes the mapping that will happen on collection.
override fun getActiveTasks(sort: ListSort): Flow<List<Task>> {
    return taskDao.getActiveTasksStream(sort.name).map { entities ->
        entities.map { it.toDomain() }
    }
}

// From FollowApp Suite — CleanUpPresetsUseCase.kt
// first() is terminal: it takes ONE emission and cancels the producer.
// A one-shot read of a live source, which is exactly what a cleanup needs.
suspend fun onLabelDeleted(labelName: String) {
    val presets = presetRepository.getAll().first()
    presets.forEach { preset ->
        if (preset.groupBy == labelName) {
            presetRepository.save(preset.copy(groupBy = null))
        }
    }
}

// From FollowApp Suite — PremiumUseCases.kt
// combine() is intermediate: it builds one cold Flow out of two cold Flows.
// Nothing runs until someone collects the result.
operator fun invoke(): Flow<Boolean> = combine(
    premiumLedgerRepository.getLedger(),
    authRepository.getSession()
) { ledger, session ->
    PremiumLifecycle.isPremium(
        now = System.currentTimeMillis(),
        premiumUntil = ledger.premiumUntil,
        isSignedIn = session != null
    )
}

// From FollowApp Suite — LabelsListViewModel.kt
// The terminal operator lives in the ViewModel, inside viewModelScope:
// that scope is the stream's lifetime.
private fun observeCatalog() {
    viewModelScope.launch {
        combine(
            getLabelsCatalogUseCase(),
            getActiveTasksUseCase(),
            _resyncTrigger
        ) { catalog, tasks, _ ->
            buildCatalogState(catalog, tasks)
        }
            .catch { e -> /* handled downstream, see Error Handling */ }
            .collect { (sortedLabels, scales) ->
                _uiState.update { /* ... */ }
            }
    }
}

// From FollowApp Suite — FakePresetRepository.kt (test fixtures)
// The flow builder: a fake that satisfies the same cold contract as Room
override fun getAll(): Flow<List<Preset>> = flow { emit(presets.toList()) }
```

## The Interview (The Hot Seat)

**Question**: What does it mean that a `Flow` is "cold", and what happens if two different screens collect the same repository flow?

**Senior Answer**: Cold means the flow is a description, not a running pipeline: building it and chaining intermediate operators executes nothing, and the producer only starts when a [terminal operator]({{ "/en/glossary/terminal-operations/" | relative_url }}) like [`collect`]({{ "/en/glossary/collect/" | relative_url }}) or [`first`]({{ "/en/glossary/first/" | relative_url }}) is applied. The consequence is that **each collector gets its own execution from scratch**. If two screens collect the same [Room]({{ "/en/glossary/room/" | relative_url }})-backed repository flow, you get two independent queries and two database observers, and every table change re-runs both — the work is duplicated, not shared. That is usually invisible in development and shows up as battery and CPU in production. The right fix is not to collect less but to share one upstream execution, which is what `shareIn` and `stateIn` are for, turning the cold flow into a hot one with a single producer and multiple subscribers. The other thing I would say is that coldness is also what makes flows safe to hand around: calling `repository.getActiveTasks()` has no side effect and needs no [scope]({{ "/en/glossary/coroutine-scope/" | relative_url }}), so the data layer can expose streams without owning a lifecycle — and it is the mirror-image bug too, because a flow nobody collects does absolutely nothing and never tells you.

**Question**: A repository exposes `getAll(): Flow<List<Preset>>`. When do you use `first()` and when `collect()`, and what breaks if you pick the wrong one?

**Senior Answer**: [`first()`]({{ "/en/glossary/first/" | relative_url }}) is for a snapshot: it suspends until the first emission, returns that value and **cancels the producer**, so the calling suspend function completes. That is what a cleanup [use case]({{ "/en/glossary/data-layer/" | relative_url }}) needs — read the current presets, act on them, finish. [`collect`]({{ "/en/glossary/collect/" | relative_url }}) is for observation: it never completes on its own, it keeps receiving every re-emission for as long as the [scope]({{ "/en/glossary/coroutine-scope/" | relative_url }}) lives, and it belongs in a ViewModel inside [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}). Picking the wrong one fails in two different ways. Using `first()` where you meant to observe compiles, runs, shows correct data once, and then silently goes stale — the screen never reflects a later change, and nothing errors, which makes it a genuinely hard bug to spot. Using `collect` where you wanted a snapshot suspends forever: the enclosing suspend function never returns, so whatever awaited it hangs, and if that is inside a `withContext` or a use case called from a click handler, the operation simply never finishes. My rule is that the terminal operator has to match the intent — one value and done, or a live subscription tied to a lifecycle — and if a function needs a snapshot of something that is genuinely a stream, I make that explicit in its name rather than leaving `first()` buried in the body.

---

[Back to Chapters]({{ "/" | relative_url }})
