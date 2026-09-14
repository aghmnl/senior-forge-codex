---
layout: page
title: "Context & Dispatchers (Main, IO, Default)"
lang: en
permalink: /en/02-coroutines-flow/context-dispatchers/
order: 2
---

## The Theory (The What)

Every [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) runs inside a [`CoroutineContext`]({{ "/en/glossary/coroutine-context/" | relative_url }}): an immutable, indexed set of elements that travels with the coroutine and is inherited by every child it launches. The two elements that matter daily are the [`Job`]({{ "/en/glossary/job/" | relative_url }}) — the coroutine's [lifecycle]({{ "/en/glossary/lifecycle/" | relative_url }}) handle, the thing you cancel — and the [`CoroutineDispatcher`]({{ "/en/glossary/dispatcher/" | relative_url }}) — the element that decides *which [thread]({{ "/en/glossary/thread/" | relative_url }}) or [thread pool]({{ "/en/glossary/thread-pool/" | relative_url }})* runs the coroutine's code after each [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}). Contexts compose with `+`: `SupervisorJob() + Dispatchers.IO` is a context with two elements; adding another [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) replaces the first, because each element type has one slot.

Android ships four [dispatchers]({{ "/en/glossary/dispatcher/" | relative_url }}), and knowing what each one is *for* is the whole topic:

- **[`Dispatchers.Main`]({{ "/en/glossary/dispatchers-main/" | relative_url }})** — the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}). Everything that touches the UI, and the only place View mutations and most Compose state writes are legal. Posts to the [`Looper`]({{ "/en/glossary/looper/" | relative_url }}) queue: a coroutine resumed here waits for the current frame work to finish.
- **[`Dispatchers.Main.immediate`]({{ "/en/glossary/dispatchers-main-immediate/" | relative_url }})** — same thread, but if you are *already* on Main it runs synchronously instead of posting. [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) and `lifecycleScope` use it, so a [`launch`]({{ "/en/glossary/launch/" | relative_url }}) from a click handler executes up to its first suspension before the handler returns.
- **[`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }})** — a pool sized to park threads in [blocking calls]({{ "/en/glossary/blocking-call/" | relative_url }}): file I/O, sockets, legacy synchronous SDKs. Up to 64 threads (or the core count, whichever is larger).
- **[`Dispatchers.Default`]({{ "/en/glossary/dispatchers-default/" | relative_url }})** — a pool sized to the CPU core count (minimum 2), for computation: sorting, parsing, date math, diffing. Blocking here starves every other coroutine that needs a core.

[`IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) and [`Default`]({{ "/en/glossary/dispatchers-default/" | relative_url }}) are views over the *same* underlying thread pool with different parallelism limits, so hopping between them is cheap — the [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) often skips the thread switch entirely. [`Dispatchers.Unconfined`]({{ "/en/glossary/dispatchers-unconfined/" | relative_url }}) exists too, and belongs only in tests and framework code.

[`withContext(dispatcher) { }`]({{ "/en/glossary/with-context/" | relative_url }}) is how a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) changes [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) for a block: it suspends, resumes the block on the new [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}), and resumes the caller back on the original one when the block returns — no new coroutine, no [`launch`]({{ "/en/glossary/launch/" | relative_url }}), and the result is the block's value.

## The Senior Perspective (The Why)

- **The [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) is inherited, which makes main-safety a *callee* responsibility.** A suspend function runs on whatever [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) its caller had. If [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) (Main) calls `repository.export()` and `export()` does file I/O without switching, Main blocks. The convention across Android is that *every* suspend function is safe to call from Main — so [`withContext(Dispatchers.IO)`]({{ "/en/glossary/with-context/" | relative_url }}) belongs *inside* the function that does the blocking work, once, not at every call site. Room, Retrofit and DataStore already honour this; your own file and JSON code must.
- **Pick the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) by the nature of the work, not by habit.** [`IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) for anything that parks a thread; [`Default`]({{ "/en/glossary/dispatchers-default/" | relative_url }}) for anything that burns CPU. Getting it backwards is not fatal but it is wrong in both directions: blocking on [`Default`]({{ "/en/glossary/dispatchers-default/" | relative_url }}) steals one of the few cores from every other computation; CPU loops on [`IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) waste a pool designed for waiting. Date arithmetic, sorting or diffing a large list is computation and belongs on [`Default`]({{ "/en/glossary/dispatchers-default/" | relative_url }}) even though it is "slow" — slowness is not the criterion, blocking is.
- **[`Main.immediate`]({{ "/en/glossary/dispatchers-main-immediate/" | relative_url }}) is an ordering guarantee you can rely on — and trip over.** Because a [`launch`]({{ "/en/glossary/launch/" | relative_url }}) from Main runs synchronously to its first suspension, code *after* the [`launch`]({{ "/en/glossary/launch/" | relative_url }}) call sees the coroutine's first synchronous effects. A typical trap: a state reset placed *after* setting a trigger flow, when a `combine` collector on [`Main.immediate`]({{ "/en/glossary/dispatchers-main-immediate/" | relative_url }}) runs synchronously the moment the trigger changes and its result is then wiped by the reset. When you see a comment explaining statement ordering around [`Main.immediate`]({{ "/en/glossary/dispatchers-main-immediate/" | relative_url }}), that is a senior engineer having been bitten once.
- **A [`Job`]({{ "/en/glossary/job/" | relative_url }}) is a cancellation tree, and [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) changes its failure semantics.** With a regular [`Job`]({{ "/en/glossary/job/" | relative_url }}), one failing child cancels its parent and therefore its siblings. With a [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}), a child's failure is its own problem — siblings keep running. That is why a long-lived, application-scoped [`CoroutineScope`]({{ "/en/glossary/coroutine-scope/" | relative_url }}) is built as `CoroutineScope(SupervisorJob() + Dispatchers.IO)`: a singleton usually owns several independent collectors, and one of them crashing must not kill the others. [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) is a [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) for the same reason.
- **A custom scope is a leak until proven otherwise.** `CoroutineScope(...)` in a class field lives until something calls `cancel()`. It is justified for objects that genuinely outlive any screen — a [`@Singleton`]({{ "/en/glossary/singleton-scope/" | relative_url }}) repository, an `Application`-level manager — and must be documented as such. `GlobalScope` is the same thing with no owner at all; there is no reason to use it. `CoroutineScope(...).launch { }` created inline for fire-and-forget work — a one-off SDK initialisation, say — is acceptable only when the work is bounded and cannot fail in a way anyone needs to know about.
- **Hard-coding [`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) couples your class to real threads, which is a testing problem.** [`runTest`]({{ "/en/glossary/run-test/" | relative_url }}) cannot control a coroutine that hops to the real IO pool: the test either races or has to sleep. The senior fix is dependency-injecting the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) ([`@IoDispatcher private val io: CoroutineDispatcher`]({{ "/en/glossary/io-dispatcher/" | relative_url }})) so tests substitute a [`TestDispatcher`]({{ "/en/glossary/test-dispatcher/" | relative_url }}). The common half-measure is [`Dispatchers.setMain(testDispatcher)`]({{ "/en/glossary/set-main/" | relative_url }}), which controls only Main: it makes [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) code testable and silently does nothing for a [`withContext(Dispatchers.IO)`]({{ "/en/glossary/with-context/" | relative_url }}) deeper down.
- **Uncaught exceptions belong to the scope, not the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}).** An exception escaping a [`launch`]({{ "/en/glossary/launch/" | relative_url }}) propagates to the parent [`Job`]({{ "/en/glossary/job/" | relative_url }}); if nothing handles it, the app crashes. A [`CoroutineExceptionHandler`]({{ "/en/glossary/coroutine-exception-handler/" | relative_url }}) installed in the scope's context is the last line of defence for fire-and-forget work. It never applies to `async` — there the exception waits inside the [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) until [`await()`]({{ "/en/glossary/await/" | relative_url }}).

## Code in Action

### Main-safety lives inside the suspend function

`BackupManager` is called from [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}), on Main. It switches to [`IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) itself, so no caller has to know it touches the file system.

```kotlin
// From FollowApp Suite — BackupManager.kt
suspend fun exportTo(uri: Uri): Result<Unit> = withContext(Dispatchers.IO) {
    runCatching {
        val bundle = BackupBundle(
            tasks = backupDao.getAllTasks(),
            labels = backupDao.getAllLabels(),
            labelOptions = backupDao.getAllLabelOptions(),
            presets = backupDao.getAllPresets()
        )
        val json = BackupSerializer.serialize(bundle)
        context.contentResolver.openOutputStream(uri, "wt").use { stream ->
            requireNotNull(stream) { "Cannot open destination" }
            stream.write(json.toByteArray(Charsets.UTF_8))
        }
    }.onSuccess {
        Log.d(TAG, "Backup exported")
    }.onFailure { Log.e(TAG, "Backup export failed", it) }
}
```

The [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}) is the *function body*, so the caller on Main suspends, the work runs on an IO thread, and the [`Result`]({{ "/en/glossary/result/" | relative_url }}) comes back on Main.

### `Default` for computation, not `IO`

Recurrence date math is CPU work. It would still stall input on Main, so it hops — to the CPU pool, not the I/O pool.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
viewModelScope.launch {
    // Date math off the main thread: pattern scans over months/years
    // must never stall input dispatching (popup ANR)
    val suggested = withContext(Dispatchers.Default) {
        val settings = getRecurrenceSettingsUseCase().first()
        // ... RecurrenceCalculator.suggestPatternDueDate(...)
    }
    _uiState.update { it.copy(form = it.form.copy(dueDate = suggested)) }
}
```

After [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}) returns, the `update` runs back on [`Main.immediate`]({{ "/en/glossary/dispatchers-main-immediate/" | relative_url }}) — the caller's [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) — with no explicit switch.

### Overriding the scope's dispatcher at launch

[`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) defaults to [`Main.immediate`]({{ "/en/glossary/dispatchers-main-immediate/" | relative_url }}). Here that default is deliberately overridden, and the comment records the measured reason.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Dispatchers.IO because viewModelScope defaults to Main.immediate,
// and Main is saturated by Compose's first composition on cold start.
// The dataStore read is fast (~5 ms — hot cache after Application
// warmed it), but the resume-back-to-Main was getting queued behind
// Compose for hundreds of ms. IO bypasses that; MutableStateFlow
// updates are already thread-safe.
viewModelScope.launch(Dispatchers.IO) {
    val snapshot = runCatching { tasksViewPreferences.read() }
        .onFailure { Log.e(TAG, "Error restoring TasksView prefs — falling back to defaults", it) }
        .getOrNull()
    if (snapshot != null) {
        _uiState.update { it.copy(/* ... */) }
    }
}
```

Passing a context to [`launch`]({{ "/en/glossary/launch/" | relative_url }}) *adds* to the scope's context: the [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) and cancellation from [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) are kept, only the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) element is replaced. The last line of the comment is the precondition that makes this safe: [`MutableStateFlow.update`]({{ "/en/glossary/update/" | relative_url }}) is [atomic]({{ "/en/glossary/atomicity/" | relative_url }}), so writing state from an IO thread is fine.

### `Main.immediate` as an ordering guarantee

```kotlin
// From FollowApp Suite — TasksViewModel.kt
fun onFabClicked() {
    subtasksJob?.cancel()
    subtasksJob = null
    // Reset the form FIRST, then trigger the suggestion recompute.
    // viewModelScope uses Main.immediate, so the combine collector may run
    // synchronously when a source flow is set — if the form reset came after,
    // it would wipe the freshly computed labelSearchResults.
    _uiState.update { it.copy(isFormVisible = true, editingTaskId = null, form = TaskFormState()) }
    _formLabelSearchQuery.value = ""
    _selectedLabels.value = emptyList()
    _formOpenTrigger.value = System.currentTimeMillis()
}
```

Setting `_formOpenTrigger` can run a `combine` collector *synchronously*, inside this very call, because the collector lives in a [`Main.immediate`]({{ "/en/glossary/dispatchers-main-immediate/" | relative_url }}) coroutine and is already on Main. The statement order is therefore load-bearing.

### A long-lived scope: `SupervisorJob` + `IO`

A [`@Singleton`]({{ "/en/glossary/singleton-scope/" | relative_url }}) repository outlives every screen, so it owns its own scope. Two decisions are encoded in one line: [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) so one listener failing does not cancel the others, [`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) because the billing client blocks.

```kotlin
// From FollowApp Suite — PremiumRepositoryImpl.kt
@Singleton
class PremiumRepositoryImpl @Inject constructor(
    private val premiumPreferences: PremiumPreferences,
    private val billingConnector: BillingConnector
) : PremiumRepository {

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    init {
        billingConnector.connect()
        scope.launch {
            billingConnector.isOwned
                .filterNotNull()
                .collect { owned -> premiumPreferences.setAdsRemoved(owned) }
        }
    }
}
```

What this scope does *not* have is a [`CoroutineExceptionHandler`]({{ "/en/glossary/coroutine-exception-handler/" | relative_url }}) — an exception escaping [`collect`]({{ "/en/glossary/collect/" | relative_url }}) here would crash the process. A stricter version: `CoroutineScope(SupervisorJob() + Dispatchers.IO + CoroutineExceptionHandler { _, e -> Log.e(TAG, "billing", e) })`.

### Fire-and-forget with an inline scope

```kotlin
// From FollowApp Suite — ConsentManager.kt
// MobileAds.initialize does ~700 ms of synchronous SDK bootstrap on
// the caller thread even though it exposes an async callback.
CoroutineScope(SupervisorJob() + Dispatchers.IO).launch {
    MobileAds.initialize(app)
}
```

Acceptable because the work is bounded, idempotent (guarded by a `compareAndSet` above it) and nobody needs its result. It is still an unowned scope: nothing can cancel it. That is the trade-off being made, and the comment is what makes it a decision rather than an accident.

### What the tests reveal

```kotlin
// From FollowApp Suite — SettingsViewModelTest.kt
@Before
fun setup() {
    Dispatchers.setMain(testDispatcher)
}

@After
fun tearDown() {
    Dispatchers.resetMain()
}
```

[`setMain`]({{ "/en/glossary/set-main/" | relative_url }}) replaces [`Dispatchers.Main`]({{ "/en/glossary/dispatchers-main/" | relative_url }}) for the test, so [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) becomes controllable. It does nothing for [`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}). The injected version — the one FAS would need to test `BackupManager` deterministically:

```kotlin
// Not found in FAS — standalone example
class BackupManager @Inject constructor(
    @IoDispatcher private val io: CoroutineDispatcher,
    /* ... */
) {
    suspend fun exportTo(uri: Uri): Result<Unit> = withContext(io) { /* ... */ }
}

// Hilt module
@Provides @IoDispatcher fun provideIo(): CoroutineDispatcher = Dispatchers.IO

// Test
val manager = BackupManager(io = StandardTestDispatcher(testScheduler), /* ... */)
```

One constructor parameter turns a real thread hop into virtual time under [`runTest`]({{ "/en/glossary/run-test/" | relative_url }}).

## The Interview (The Hot Seat)

**Question**: What is a `CoroutineContext`, and what does [`withContext(Dispatchers.IO)`]({{ "/en/glossary/with-context/" | relative_url }}) actually do?

**Senior Answer**: A [`CoroutineContext`]({{ "/en/glossary/coroutine-context/" | relative_url }}) is an immutable set of elements keyed by type — the [`Job`]({{ "/en/glossary/job/" | relative_url }}) that represents the coroutine's [lifecycle]({{ "/en/glossary/lifecycle/" | relative_url }}), the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) that decides which thread runs it, an optional [`CoroutineExceptionHandler`]({{ "/en/glossary/coroutine-exception-handler/" | relative_url }}) and a name. It is inherited: a child launched from a scope gets the scope's context, and anything you pass to [`launch`]({{ "/en/glossary/launch/" | relative_url }}) or [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}) is *added* to it, replacing only the elements of the same type. So `viewModelScope.launch(Dispatchers.IO)` keeps the [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) and the cancellation tie to the ViewModel and swaps only the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}). [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}) is not a thread switch in the `Thread` sense: it suspends the current coroutine, schedules the block's [continuation]({{ "/en/glossary/continuation/" | relative_url }}) on the target [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}), runs it there, and when the block completes schedules the caller's continuation back on the *original* [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}), returning the block's value. No new coroutine is created, [cancellation]({{ "/en/glossary/cooperative-cancellation/" | relative_url }}) flows through it, and because [`IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) and [`Default`]({{ "/en/glossary/dispatchers-default/" | relative_url }}) share a pool, the [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) may elide the physical thread hop when it can. The practical rule that follows: put [`withContext(Dispatchers.IO)`]({{ "/en/glossary/with-context/" | relative_url }}) *inside* the suspend function that blocks, so the function is main-safe for every caller, and inject the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) so tests can replace it.

**Question**: A [`@Singleton`]({{ "/en/glossary/singleton-scope/" | relative_url }}) repository collects a billing [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) forever. How do you scope that coroutine, and what happens when the collector throws?

**Senior Answer**: The repository outlives every screen, so neither [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) nor `lifecycleScope` fits — it needs its own [`CoroutineScope`]({{ "/en/glossary/coroutine-scope/" | relative_url }}), and I would build it as `CoroutineScope(SupervisorJob() + Dispatchers.IO + CoroutineExceptionHandler { ... })`. Each element is a decision. [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) because a singleton typically owns several independent collectors, and with a plain [`Job`]({{ "/en/glossary/job/" | relative_url }}) one failing child cancels the parent and therefore all its siblings — the consent listener dying because the billing listener threw is exactly the coupling to avoid. [`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) because the billing client blocks. And the handler because with a [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) a child's exception does not propagate to a parent that could handle it; it goes to the handler in the context, and if there is none, to the thread's uncaught-exception handler — which on Android crashes the process. Without that third element, an exception in [`collect`]({{ "/en/glossary/collect/" | relative_url }}) is a production crash with no [`try/catch`]({{ "/en/glossary/try-catch/" | relative_url }}) anywhere in sight. Two follow-ups I would raise: the scope is never cancelled, which is acceptable only because a [`@Singleton`]({{ "/en/glossary/singleton-scope/" | relative_url }}) genuinely lives as long as the process, and I would inject the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) rather than hard-code it so the collector can be driven by a [`TestDispatcher`]({{ "/en/glossary/test-dispatcher/" | relative_url }}) under [`runTest`]({{ "/en/glossary/run-test/" | relative_url }}).

---

[Back to Chapters]({{ "/" | relative_url }})
