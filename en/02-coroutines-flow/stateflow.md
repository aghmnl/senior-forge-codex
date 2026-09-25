---
layout: page
title: "StateFlow"
lang: en
permalink: /en/02-coroutines-flow/stateflow/
order: 9
---

## The Theory (The What)

A `StateFlow<T>` is a **[hot]({{ "/en/glossary/hot-stream/" | relative_url }})** flow that always holds exactly one value. A [cold]({{ "/en/glossary/cold-stream/" | relative_url }}) [Flow]({{ "/en/02-coroutines-flow/flow-cold-streams/" | relative_url }}) is a recipe that runs once per [collector]({{ "/en/glossary/collector/" | relative_url }}). A `StateFlow` is a *container*: it exists and has a current value whether anyone collects it or not.

Its contract fits in four rules:

- **It always has a value.** [`MutableStateFlow(initial)`]({{ "/en/glossary/mutable-state-flow/" | relative_url }}) requires an initial value, and `.value` reads the current one synchronously, from any [thread]({{ "/en/glossary/thread/" | relative_url }}), without suspending and without collecting.
- **A new [collector]({{ "/en/glossary/collector/" | relative_url }}) gets the current value immediately**, then every later change. A [collector]({{ "/en/glossary/collector/" | relative_url }}) that arrives late sees the present, not the history. It never misses "the first emission", because there is always a current value to deliver.
- **It is conflated.** Only the latest value matters. If the value changes three times while a slow [collector]({{ "/en/glossary/collector/" | relative_url }}) is busy, the [collector]({{ "/en/glossary/collector/" | relative_url }}) receives the last one and skips the ones in between. Writing never suspends the writer: there is no [backpressure]({{ "/en/glossary/backpressure/" | relative_url }}).
- **It is distinct by equality.** Assigning a value that [`equals()`]({{ "/en/glossary/equals/" | relative_url }}) the current one does nothing: no emission, and no [collector]({{ "/en/glossary/collector/" | relative_url }}) wakes up. [`distinctUntilChanged`]({{ "/en/glossary/distinct-until-changed/" | relative_url }}) is built in.

The split between the mutable and the read-only type carries the architecture. [`MutableStateFlow`]({{ "/en/glossary/mutable-state-flow/" | relative_url }}) exposes a writable `value` (plus [`update`]({{ "/en/glossary/update/" | relative_url }}) and [`compareAndSet`]({{ "/en/glossary/compare-and-set/" | relative_url }})), and `StateFlow` is read-only. The standard shape is a private [`MutableStateFlow`]({{ "/en/glossary/mutable-state-flow/" | relative_url }}) called `_uiState` inside the [state holder]({{ "/en/glossary/state-holder/" | relative_url }}), exposed as a `StateFlow` called `uiState` through [`asStateFlow()`]({{ "/en/glossary/as-state-flow/" | relative_url }}).

Two more properties matter in practice:

- [`collect`]({{ "/en/glossary/collect/" | relative_url }}) on a `StateFlow` **never completes**. The stream has no end, so the collecting [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) runs until its scope is cancelled.
- All its methods are **[thread-safe]({{ "/en/glossary/thread-safety/" | relative_url }})**. Writes from any [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) need no extra synchronization. A read-modify-write written as `value = value.copy(...)` is still two operations and not one, though, and that gap is what [`update {}`]({{ "/en/glossary/update/" | relative_url }}) closes. It gets its own topic.

Under the hood a `StateFlow` is a specialized [`SharedFlow`]({{ "/en/glossary/sharedflow/" | relative_url }}): it replays one value, conflates, and filters out equal values. The general [hot stream]({{ "/en/glossary/hot-stream/" | relative_url }}) ([`SharedFlow`]({{ "/en/glossary/sharedflow/" | relative_url }})) and turning a [cold]({{ "/en/glossary/cold-stream/" | relative_url }}) flow into a `StateFlow` ([`stateIn`]({{ "/en/glossary/state-in/" | relative_url }})) are later topics.

## The Senior Perspective (The Why)

- **StateFlow is for state, not events.** [Conflation]({{ "/en/glossary/conflation/" | relative_url }}) and equality filtering are exactly right for "what should the screen show now". They are exactly wrong for "show this snackbar once" or "navigate". Two identical error messages in a row collapse into one. A navigation event stored as state is delivered again to every new [collector]({{ "/en/glossary/collector/" | relative_url }}), after a rotation or a return from the background, so it fires twice unless someone clears it. The idiomatic fix is to model the event as state that the UI acknowledges: the pending item lives in the UI state, and the UI reports back when it has handled it. Pushing fire-and-forget events through a container designed to remember does not work.
- **Equality is the emission rule, so the state type decides correctness.** With an immutable [`data class`]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}), [`copy()`]({{ "/en/glossary/copy/" | relative_url }}) creates a new value and the generated [`equals()`]({{ "/en/glossary/equals/" | relative_url }}) compares content: real changes [emit]({{ "/en/glossary/emit/" | relative_url }}), no-ops do not. With a mutable object, mutating it in place and reassigning the *same* reference compares equal to itself, and the UI never updates. With a class that does not override [`equals()`]({{ "/en/glossary/equals/" | relative_url }}), the check falls back to [referential equality]({{ "/en/glossary/referential-equality/" | relative_url }}), so every new instance emits even when nothing changed. `StateFlow` quietly assumes [value semantics]({{ "/en/glossary/value-semantics/" | relative_url }}), and [immutability]({{ "/en/glossary/immutability/" | relative_url }}) is what makes that assumption true. The same rule protects work downstream: a `StateFlow` of query parameters feeding [`flatMapLatest`]({{ "/en/glossary/flat-map-latest/" | relative_url }}) only cancels and restarts the query when the parameters actually change.
- **Equality filtering is also a trap for triggers.** A [`MutableStateFlow(true)`]({{ "/en/glossary/mutable-state-flow/" | relative_url }}) used as a "refresh" signal fires once and then never again, because every later write equals the current value. A counter or a [timestamp]({{ "/en/glossary/timestamp/" | relative_url }}) works around it by making every write distinct. That is a legitimate pattern, but it is also a sign to ask whether the trigger is really state.
- **The initial value is a design decision, not boilerplate.** `StateFlow` forces you to decide what the screen shows before any data arrives. Choosing [`emptyList()`]({{ "/en/glossary/empty-list/" | relative_url }}) makes "still loading" and "genuinely empty" indistinguishable, and that is how an empty-state message flashes on every cold start. Honest options are an explicit `isLoading` flag, a `Loading` member in a sealed state, or a nullable value where `null` means "unknown yet". Each one makes the absence of data a state instead of a lie.
- **[Hot]({{ "/en/glossary/hot-stream/" | relative_url }}) means it outlives its collectors, so [lifecycle]({{ "/en/glossary/lifecycle/" | relative_url }}) is the [collector]({{ "/en/glossary/collector/" | relative_url }})'s job.** A `StateFlow` keeps its value with zero subscribers, and that is what lets a rotated screen redraw instantly. The [collector]({{ "/en/glossary/collector/" | relative_url }}), however, must stop when the UI is not visible. In [Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}), `collectAsState()` keeps collecting while the app sits in the background. [`collectAsStateWithLifecycle()`]({{ "/en/glossary/collect-as-state-with-lifecycle/" | relative_url }}) stops below `STARTED` and picks up the current value on return. For a plain [`MutableStateFlow`]({{ "/en/glossary/mutable-state-flow/" | relative_url }}) the cost is small. For a `StateFlow` fed by an [upstream]({{ "/en/glossary/upstream/" | relative_url }}) through [`stateIn`]({{ "/en/glossary/state-in/" | relative_url }}) with [`WhileSubscribed`]({{ "/en/glossary/while-subscribed/" | relative_url }}), the [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) [collector]({{ "/en/glossary/collector/" | relative_url }}) is the only thing that lets that [upstream]({{ "/en/glossary/upstream/" | relative_url }}) stop at all.
- **Synchronous `.value` is powerful and easy to misuse.** Reading `.value` inside the [state holder]({{ "/en/glossary/state-holder/" | relative_url }}) to make a decision is fine. Reading it from the UI instead of collecting means the UI never hears about later changes. Writing `value = value.copy(...)` from two [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}) at once is a [race condition]({{ "/en/glossary/race-condition/" | relative_url }}) that silently loses one of the writes.
- **StateFlow vs [LiveData]({{ "/en/glossary/livedata/" | relative_url }}).** Both are observable holders, and the differences decide the choice. `StateFlow` requires an initial value, filters by equality, is plain [Kotlin]({{ "/en/glossary/kotlin/" | relative_url }}) (so it is testable without [Android]({{ "/en/glossary/android/" | relative_url }}) and usable in any layer), and works with every Flow operator. [LiveData]({{ "/en/glossary/livedata/" | relative_url }}) is [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) on its own and notifies on every `setValue`, even with an equal value. In new code, [lifecycle]({{ "/en/glossary/lifecycle/" | relative_url }}) awareness moves to the [collector]({{ "/en/glossary/collector/" | relative_url }}) ([`collectAsStateWithLifecycle`]({{ "/en/glossary/collect-as-state-with-lifecycle/" | relative_url }}), [`repeatOnLifecycle`]({{ "/en/glossary/repeat-on-lifecycle/" | relative_url }})), and `StateFlow` is the better fit everywhere else.

## Code in Action

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// The canonical pair: mutable and private inside, read-only outside
private val _uiState = MutableStateFlow(TasksUiState())
val uiState: StateFlow<TasksUiState> = _uiState.asStateFlow()

// The query parameters are state too. QueryParams is a data class, so a
// write that changes nothing (same query, same sort) is dropped by equality
// and does NOT re-run the database query below.
private val _queryParams = MutableStateFlow(
    QueryParams(
        query = "",
        filters = setOf(TaskStatus.ACTIVE),
        sort = ListSort.TITLE_ASC
    )
)

// A StateFlow<Boolean> used as a gate: nothing is queried until the
// persisted view configuration has been restored
private val _restored = MutableStateFlow(false)

private fun observeTasks() {
    viewModelScope.launch {
        _restored
            .filter { it }
            .flatMapLatest { _queryParams }   // every distinct QueryParams re-queries
            .flatMapLatest { params -> /* getActiveTasksUseCase(params.sort) ... */ }
            .collect { /* ... */ }
    }
}

// From FollowApp Suite — TasksViewModel.kt
// Writing from Dispatchers.IO is safe: MutableStateFlow is thread-safe.
// The original comment says it explicitly.
private fun restoreViewPreferences() {
    // ... IO bypasses that; MutableStateFlow
    // updates are already thread-safe.
    viewModelScope.launch(Dispatchers.IO) {
        val snapshot = runCatching { tasksViewPreferences.read() }.getOrNull()
        if (snapshot != null) {
            _queryParams.update { it.copy(sort = snapshot.sortOrder /* ... */) }
        }
        _restored.value = true   // opens the gate
    }
}

// From FollowApp Suite — TasksViewModel.kt
// A trigger that must fire on EVERY form open. Writing `true` twice would
// be dropped by equality, so each write uses a new timestamp to stay distinct.
private val _formOpenTrigger = MutableStateFlow(0L)

fun onFabClicked() {
    // ...
    _formOpenTrigger.value = System.currentTimeMillis()
}

// From FollowApp Suite — LabelsListViewModel.kt
// The same idea with a counter: bumping it forces combine() to recompute
// from the latest catalog and tasks after a failed write
private val _resyncTrigger = MutableStateFlow(0)

private fun resync() {
    _resyncTrigger.value++
}

// From FollowApp Suite — BillingConnector.kt
// The initial value is a decision: null means "Play has not answered yet",
// which callers can tell apart from a real false
private val _isOwned = MutableStateFlow<Boolean?>(null)
val isOwned: StateFlow<Boolean?> = _isOwned.asStateFlow()

// From FollowApp Suite — TasksScreen.kt
// Lifecycle-aware collection: stops below STARTED, resumes with the current value
val uiState by viewModel.uiState.collectAsStateWithLifecycle()

// From FollowApp Suite — SettingsScreen.kt
// The same codebase with collectAsState(): it keeps collecting while the app
// is in the background. When consentManager is null, the fallback also builds
// a NEW MutableStateFlow on every recomposition, which restarts the collection.
val uiState by viewModel.uiState.collectAsState()
val privacyOptionsRequired by (consentManager?.privacyOptionsRequired ?: MutableStateFlow(false))
    .collectAsState()
```

## The Interview (The Hot Seat)

**Question**: Why is `StateFlow` a poor fit for one-shot events such as navigation or a snackbar, and what do you do instead?

**Senior Answer**: `StateFlow` is built to answer "what is true right now", and its two defining behaviors both break events. First, it is conflated and filters by equality: two identical snackbar messages in a row collapse into one, and a burst of events can be skipped because a slow [collector]({{ "/en/glossary/collector/" | relative_url }}) only sees the latest value. Second, it remembers: the current value is delivered to every new [collector]({{ "/en/glossary/collector/" | relative_url }}), so a navigation event that is still sitting in the state fires again after a rotation or when the screen comes back from the background. The usual patch, clearing the value after reading it, is racy and spreads "consume" logic across the UI. The approach I prefer is to stop treating it as an event and model it as state: the pending message or navigation target lives in the UI state, the UI shows it or navigates, and then calls back to the ViewModel to acknowledge it, which removes it from the state. That survives rotation and process death and is trivial to test. When something truly is fire-and-forget and must not be replayed, it belongs in a different primitive (a [`Channel`]({{ "/en/glossary/channel/" | relative_url }}) or a [`SharedFlow`]({{ "/en/glossary/sharedflow/" | relative_url }}) without replay), not in a container designed to remember.

**Question**: A ViewModel does `_uiState.value = _uiState.value.also { it.tasks.add(newTask) }` and the list on screen never updates. What is wrong, and how do you fix it?

**Senior Answer**: `StateFlow` only emits when the new value is not [`equals()`]({{ "/en/glossary/equals/" | relative_url }}) to the current one. Here `tasks` is a mutable list mutated in place, and the same state object is assigned back, so the comparison is between an object and itself and the write is dropped. No [collector]({{ "/en/glossary/collector/" | relative_url }}) wakes up and [Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) never recomposes. On top of that, the flow's "current value" was changed behind its back, so any code that reads `.value` sees data that was never emitted. The fix is to make the state immutable: a [`data class`]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}) with a read-only `List`, updated with `copy(tasks = tasks + newTask)`. That produces a new instance with different content, equality detects the change, and the emission happens. I would also replace the read-then-assign with `_uiState.update { it.copy(...) }`, because `value = value.copy(...)` is two separate operations, and two [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}) doing it concurrently can lose a write. The general lesson is that `StateFlow` assumes [value semantics]({{ "/en/glossary/value-semantics/" | relative_url }}): it cannot detect a change that doesn't produce a new, unequal value.

---

[Back to Chapters]({{ "/" | relative_url }})
