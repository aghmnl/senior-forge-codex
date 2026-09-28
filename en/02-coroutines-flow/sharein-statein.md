---
layout: page
title: "shareIn & stateIn"
lang: en
permalink: /en/02-coroutines-flow/sharein-statein/
order: 11
---

## The Theory (The What)

A [cold]({{ "/en/glossary/cold-stream/" | relative_url }}) [Flow]({{ "/en/02-coroutines-flow/flow-cold-streams/" | relative_url }}) runs its producer once per [collector]({{ "/en/glossary/collector/" | relative_url }}): three screens collecting the same repository flow mean three queries. [`shareIn`]({{ "/en/glossary/share-in/" | relative_url }}) and [`stateIn`]({{ "/en/glossary/state-in/" | relative_url }}) fix that. They take a [cold flow]({{ "/en/glossary/cold-stream/" | relative_url }}), launch **one** collection of it, and share the result with every [subscriber]({{ "/en/glossary/collector/" | relative_url }}). They are the bridge from [cold]({{ "/en/glossary/cold-stream/" | relative_url }}) to [hot]({{ "/en/glossary/hot-stream/" | relative_url }}).

- **[`stateIn(scope, started, initialValue)`]({{ "/en/glossary/state-in/" | relative_url }})** returns a [StateFlow]({{ "/en/02-coroutines-flow/stateflow/" | relative_url }}): a current value readable through `.value`, the initial value until the [upstream]({{ "/en/glossary/upstream/" | relative_url }}) emits, [conflation]({{ "/en/glossary/conflation/" | relative_url }}) and [equality filtering]({{ "/en/glossary/distinct-until-changed/" | relative_url }}).
- **[`shareIn(scope, started, replay)`]({{ "/en/glossary/share-in/" | relative_url }})** returns a [SharedFlow]({{ "/en/02-coroutines-flow/sharedflow/" | relative_url }}): no current value, and `replay` decides how many past values a new [subscriber]({{ "/en/glossary/collector/" | relative_url }}) receives.

Both take the same two decisions as parameters:

- **`scope`** is where the shared collection runs, and therefore its maximum lifetime. In a [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) it is [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}); for something shared across the whole app, an application-level scope.
- **`started`** is *when* that collection runs:
  - [`SharingStarted.Eagerly`]({{ "/en/glossary/sharing-started/" | relative_url }}) starts immediately and never stops until the scope is cancelled.
  - [`SharingStarted.Lazily`]({{ "/en/glossary/sharing-started/" | relative_url }}) starts with the first [subscriber]({{ "/en/glossary/collector/" | relative_url }}) and never stops after that.
  - [`SharingStarted.WhileSubscribed(stopTimeoutMillis)`]({{ "/en/glossary/while-subscribed/" | relative_url }}) runs only while there is at least one [subscriber]({{ "/en/glossary/collector/" | relative_url }}), stops after the timeout when the last one leaves, and starts again when a new one arrives.

A suspending overload, [`stateIn(scope)`]({{ "/en/glossary/state-in/" | relative_url }}), takes no initial value: it suspends until the [upstream]({{ "/en/glossary/upstream/" | relative_url }}) emits its first value and returns a [`StateFlow`]({{ "/en/02-coroutines-flow/stateflow/" | relative_url }}) that already holds it.

## The Senior Perspective (The Why)

- **It replaces the "launch and copy" pattern.** The common way to build UI state is an [`init`]({{ "/en/glossary/init/" | relative_url }}) block with a `launch { flow.collect { _uiState.update { ... } } }` per source. It works, but the state is *pushed* from side [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}) instead of being *declared* from its sources, and every one of those collections runs [eagerly]({{ "/en/glossary/eager/" | relative_url }}) for the whole life of the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}), visible screen or not. `combine(...).map { ... }.stateIn(...)` declares the state as a function of its inputs, in one place, and it only runs while someone is looking.
- **[`WhileSubscribed(5_000)`]({{ "/en/glossary/while-subscribed/" | relative_url }}) is the default for UI state, and the number is not arbitrary.** A rotation removes the [subscriber]({{ "/en/glossary/collector/" | relative_url }}) for about a second and adds it back. With a timeout of `0`, every rotation would stop and restart the [upstream]({{ "/en/glossary/upstream/" | relative_url }}), re-running queries. With `5_000`, a rotation survives, but a user who leaves the app for longer stops the work. It only works with a [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) [collector]({{ "/en/glossary/collector/" | relative_url }}) ([`collectAsStateWithLifecycle`]({{ "/en/glossary/collect-as-state-with-lifecycle/" | relative_url }}), [`repeatOnLifecycle`]({{ "/en/glossary/repeat-on-lifecycle/" | relative_url }})): a [collector]({{ "/en/glossary/collector/" | relative_url }}) that never leaves means [`WhileSubscribed`]({{ "/en/glossary/while-subscribed/" | relative_url }}) never sees zero [subscribers]({{ "/en/glossary/collector/" | relative_url }}).
- **[`Eagerly`]({{ "/en/glossary/sharing-started/" | relative_url }}) and [`Lazily`]({{ "/en/glossary/sharing-started/" | relative_url }}) mean "forever in this scope".** In [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) that is acceptable for cheap sources. In an application scope it means the [upstream]({{ "/en/glossary/upstream/" | relative_url }}) never stops for as long as the process lives: right for something the whole app needs, a leak for anything else.
- **Create it once, as a property.** Each call to [`stateIn`]({{ "/en/glossary/state-in/" | relative_url }}) or [`shareIn`]({{ "/en/glossary/share-in/" | relative_url }}) starts a new shared collection. Writing it inside a function, or in a getter (`val state get() = flow.stateIn(...)`), creates a new one per call, and the sharing silently disappears. The operator belongs in a property initialized once.
- **The initial value is still a design decision.** It is what the UI shows until the [upstream]({{ "/en/glossary/upstream/" | relative_url }}) emits. `UiState(isLoading = true)` is honest; an empty list is not, because it makes "still loading" look exactly like "nothing there".
- **[Upstream]({{ "/en/glossary/upstream/" | relative_url }}) errors do not reach the [collectors]({{ "/en/glossary/collector/" | relative_url }}).** An exception in the shared [upstream]({{ "/en/glossary/upstream/" | relative_url }}) is not delivered to [subscribers]({{ "/en/glossary/collector/" | relative_url }}). It fails the sharing [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) inside `scope`, and in [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) an uncaught exception crashes the app. [`catch`]({{ "/en/glossary/catch/" | relative_url }}) (usually mapped to an error state) and [`retry`]({{ "/en/glossary/retry/" | relative_url }}) belong **before** [`stateIn`]({{ "/en/glossary/state-in/" | relative_url }}) or [`shareIn`]({{ "/en/glossary/share-in/" | relative_url }}).
- **When to keep [`MutableStateFlow`]({{ "/en/glossary/mutable-state-flow/" | relative_url }}).** State that also changes through user actions (a search query, a selected tab, a form field) still needs a writable source. The idiomatic shape is to keep that input in a small [`MutableStateFlow`]({{ "/en/glossary/mutable-state-flow/" | relative_url }}), [`combine`]({{ "/en/glossary/combine/" | relative_url }}) it with the data sources, and [`stateIn`]({{ "/en/glossary/state-in/" | relative_url }}) the result, so there is still a single declared state instead of two competing writers.
- **Testing needs a [subscriber]({{ "/en/glossary/collector/" | relative_url }}).** A [`StateFlow`]({{ "/en/02-coroutines-flow/stateflow/" | relative_url }}) built with [`WhileSubscribed`]({{ "/en/glossary/while-subscribed/" | relative_url }}) does not collect its [upstream]({{ "/en/glossary/upstream/" | relative_url }}) until someone subscribes, so a test that only reads `.value` sees the initial value forever. The test has to collect it, typically in [`backgroundScope`]({{ "/en/glossary/test-scope/" | relative_url }}) inside [`runTest`]({{ "/en/glossary/run-test/" | relative_url }}).

## Code in Action

```kotlin
// From FollowApp Suite — SettingsViewModel.kt
// The "launch and copy" pattern: one eager collection per source, each one
// pushing a slice into _uiState for as long as the ViewModel lives
init {
    viewModelScope.launch {
        getPremiumStatusUseCase()
            .catch { error -> Log.e(TAG, "Error loading premium status", error) }
            .collect { premium -> _uiState.update { it.copy(isPremium = premium) } }
    }
    viewModelScope.launch {
        getRemoveAdsPriceUseCase()
            .catch { error -> Log.e(TAG, "Error loading product price", error) }
            .collect { price -> _uiState.update { it.copy(removeAdsPrice = price) } }
    }
    viewModelScope.launch {
        getUserSessionUseCase()
            .catch { error -> Log.e(TAG, "Error loading session", error) }
            .collect { session -> _uiState.update { it.copy(userSession = session) } }
    }
    // ... two more collections with the same shape
}

// Not found in FAS — standalone example
// The same state declared with stateIn: one expression, derived from its
// sources, running only while the screen is subscribed
val uiState: StateFlow<SettingsUiState> = combine(
    getPremiumStatusUseCase(),
    getRemoveAdsPriceUseCase(),
    getUserSessionUseCase()
) { premium, price, session ->
    SettingsUiState(isPremium = premium, removeAdsPrice = price, userSession = session)
}
    .catch { error -> Log.e(TAG, "Error loading settings", error) }   // before stateIn
    .stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = SettingsUiState()
    )

// From FollowApp Suite — TasksViewModel.kt
// The same ViewModel collects the active-tasks stream in two places:
// once in observeTasks() (for the list) and once here (for preset counts).
// Two cold collections mean two independent Room queries on the same table.
private fun observePresetTaskCounts() {
    viewModelScope.launch {
        combine(
            getActiveTasksUseCase(),
            getPresetsUseCase()
        ) { allTasks, presets -> /* count tasks per preset */ }
            .catch { error -> Log.e(TAG, "Error computing preset counts", error) }
            .collect { counts -> _uiState.update { it.copy(presetTaskCounts = counts) } }
    }
}

// Not found in FAS — standalone example
// shareIn turns one cold query into a single shared collection
private val activeTasks: SharedFlow<List<Task>> = getActiveTasksUseCase()
    .shareIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), replay = 1)

// From FollowApp Suite — PremiumRepositoryImpl.kt
// An application-level scope in a @Singleton: the place where sharing
// across the whole app lives, and why Eagerly here means "for the whole process"
@Singleton
class PremiumRepositoryImpl @Inject constructor(/* ... */) : PremiumRepository {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    // ...
}
```

## The Interview (The Hot Seat)

**Question**: What is the difference between [`SharingStarted.Eagerly`]({{ "/en/glossary/sharing-started/" | relative_url }}), [`Lazily`]({{ "/en/glossary/sharing-started/" | relative_url }}) and [`WhileSubscribed`]({{ "/en/glossary/while-subscribed/" | relative_url }}), and which one would you use for a screen's UI state?

**Senior Answer**: The three strategies answer *when* the shared [upstream]({{ "/en/glossary/upstream/" | relative_url }}) collection runs. [`Eagerly`]({{ "/en/glossary/sharing-started/" | relative_url }}) starts it immediately and keeps it running until the scope is cancelled, whether or not anyone is subscribed. [`Lazily`]({{ "/en/glossary/sharing-started/" | relative_url }}) waits for the first [subscriber]({{ "/en/glossary/collector/" | relative_url }}) and then also keeps it running until the scope ends. [`WhileSubscribed`]({{ "/en/glossary/while-subscribed/" | relative_url }}) ties it to the [subscribers]({{ "/en/glossary/collector/" | relative_url }}): it runs while at least one is collecting, and after the last one leaves it waits `stopTimeoutMillis` and cancels the [upstream]({{ "/en/glossary/upstream/" | relative_url }}), restarting it when someone subscribes again. For UI state I use [`WhileSubscribed(5_000)`]({{ "/en/glossary/while-subscribed/" | relative_url }}). The timeout is what makes it work in practice: a configuration change drops the [subscriber]({{ "/en/glossary/collector/" | relative_url }}) for about a second, so a zero timeout would restart queries on every rotation, while five seconds survives the rotation but still stops the work when the user really leaves the app. Two conditions make it effective. The UI has to collect with something [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}), [`collectAsStateWithLifecycle`]({{ "/en/glossary/collect-as-state-with-lifecycle/" | relative_url }}) or [`repeatOnLifecycle`]({{ "/en/glossary/repeat-on-lifecycle/" | relative_url }}), or the [subscriber]({{ "/en/glossary/collector/" | relative_url }}) never leaves. And the [`stateIn`]({{ "/en/glossary/state-in/" | relative_url }}) call has to live in a property created once, because every call starts a new shared collection. I reserve [`Eagerly`]({{ "/en/glossary/sharing-started/" | relative_url }}) for something that must be warm before anyone asks, usually in an application scope, knowing that it means the [upstream]({{ "/en/glossary/upstream/" | relative_url }}) lives as long as the process.

**Question**: A [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) builds its state with `init { viewModelScope.launch { repository.observe().collect { _uiState.value = it } } }`. What would you change, and why?

**Senior Answer**: That pattern works, but it has three costs. The collection starts [eagerly]({{ "/en/glossary/eager/" | relative_url }}) and runs for the whole life of the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}), even while the screen is in the background, because [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) knows nothing about visibility. The state is pushed from a side [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) instead of being declared, so as more sources are added you end up with several [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}) writing slices of the same [`MutableStateFlow`]({{ "/en/glossary/mutable-state-flow/" | relative_url }}). And it is easy to forget error handling, because each [`collect`]({{ "/en/glossary/collect/" | relative_url }}) needs its own. I would declare the state instead: `val uiState = repository.observe().map { it.toUiState() }.catch { emit(UiState.Error) }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), UiState.Loading)`. That gives one expression that says exactly what the state is derived from, an honest initial value, error handling placed before the sharing where it can actually [catch]({{ "/en/glossary/catch/" | relative_url }}) [upstream]({{ "/en/glossary/upstream/" | relative_url }}) failures, and an [upstream]({{ "/en/glossary/upstream/" | relative_url }}) that stops when nobody is looking. If part of the state also changes through user actions, like a search query, I keep only that input in a small [`MutableStateFlow`]({{ "/en/glossary/mutable-state-flow/" | relative_url }}) and [`combine`]({{ "/en/glossary/combine/" | relative_url }}) it with the repository flow before [`stateIn`]({{ "/en/glossary/state-in/" | relative_url }}), so there is still a single source for the screen. The one thing I watch for in tests is that [`WhileSubscribed`]({{ "/en/glossary/while-subscribed/" | relative_url }}) needs a [subscriber]({{ "/en/glossary/collector/" | relative_url }}), so the test collects the state in [`backgroundScope`]({{ "/en/glossary/test-scope/" | relative_url }}) before asserting on it.

---

[Back to Chapters]({{ "/" | relative_url }})
