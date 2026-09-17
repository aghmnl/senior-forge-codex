---
layout: page
title: "Main-Safety"
lang: en
permalink: /en/02-coroutines-flow/main-safety/
order: 5
---

## The Theory (The What)

A [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) is **main-safe** when it can be called from the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) without blocking it. That is the whole definition, and it is a *contract about the callee*: the function itself is responsible for moving any [blocking call]({{ "/en/glossary/blocking-call/" | relative_url }}) — disk, network, a synchronous [SDK]({{ "/en/glossary/sdk/" | relative_url }}), heavy CPU — off Main, so that a caller on [`Dispatchers.Main`]({{ "/en/glossary/dispatchers-main/" | relative_url }}) only ever *suspends* while the work happens elsewhere.

The mechanism is [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}): the function wraps its blocking body in `withContext(Dispatchers.IO) { }` (for I/O) or `withContext(Dispatchers.Default) { }` (for CPU). The caller's [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) suspends at that [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}), the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) returns to its [`Looper`]({{ "/en/glossary/looper/" | relative_url }}) and keeps drawing frames and handling input, the block runs on a [thread pool]({{ "/en/glossary/thread-pool/" | relative_url }}), and when it returns the caller resumes on Main with the result.

Why the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) matters: Android draws at 60–120 Hz, so every frame has roughly 16 ms (or 8 ms) of budget, and *all* of it is spent on Main — measuring, laying out, drawing, and dispatching touch events. A [blocking call]({{ "/en/glossary/blocking-call/" | relative_url }}) of 50 ms on Main drops three frames ([jank]({{ "/en/glossary/jank/" | relative_url }})); one of 5 seconds without processing input triggers an **[ANR]({{ "/en/glossary/anr/" | relative_url }})** (Application Not Responding) dialog and the system kills the app. A [`suspend`]({{ "/en/glossary/suspend-functions/" | relative_url }}) keyword does *not* protect you from this: `suspend fun load() = File(path).readText()` is a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) that blocks Main for the whole read. Suspension only happens at real [suspension points]({{ "/en/glossary/suspension-point/" | relative_url }}).

The convention across the Android ecosystem, stated in the official guidance, is that **every [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) is main-safe**. [Room]({{ "/en/glossary/room/" | relative_url }})'s [`suspend`]({{ "/en/glossary/suspend-functions/" | relative_url }}) [DAO]({{ "/en/glossary/dao/" | relative_url }}) methods switch to their own query executor; [Retrofit]({{ "/en/glossary/retrofit/" | relative_url }})'s [`suspend`]({{ "/en/glossary/suspend-functions/" | relative_url }}) calls run on [OkHttp]({{ "/en/glossary/okhttp/" | relative_url }})'s pool; [DataStore]({{ "/en/glossary/datastore/" | relative_url }})'s `data` [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) reads on IO. Because of that, application code never has to guess: if a function is [`suspend`]({{ "/en/glossary/suspend-functions/" | relative_url }}), calling it from [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) (which is [`Main.immediate`]({{ "/en/glossary/dispatchers-main-immediate/" | relative_url }})) is safe. The only functions that can break the rule are the ones *you* write around raw files, sockets, JSON, cryptography, or a legacy synchronous [SDK]({{ "/en/glossary/sdk/" | relative_url }}) — and those are the ones this topic is about.

## The Senior Perspective (The Why)

- **Main-safety is a callee responsibility because the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) is inherited.** A [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) runs on whatever [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) its caller has. If the caller must remember to wrap `repository.export()` in [`withContext(Dispatchers.IO)`]({{ "/en/glossary/with-context/" | relative_url }}), then every caller must remember, forever — and the first one who forgets ships an [ANR]({{ "/en/glossary/anr/" | relative_url }}). Putting the [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}) *inside* `export()` makes the guarantee local, testable and impossible to opt out of. The rule of thumb: the layer that knows the work blocks is the layer that switches.
- **[`suspend`]({{ "/en/glossary/suspend-functions/" | relative_url }}) is a promise, not a mechanism.** Marking a function [`suspend`]({{ "/en/glossary/suspend-functions/" | relative_url }}) says "you may call me from a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }})"; it does not move anything anywhere. The trap is a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) that never actually suspends: it compiles, it works in tests on a [`TestDispatcher`]({{ "/en/glossary/test-dispatcher/" | relative_url }}), and it blocks Main in production. Reviewers should ask of every [`suspend fun`]({{ "/en/glossary/suspend-functions/" | relative_url }}) that touches a file, a socket or a big loop: *where is the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) switch?* In debug builds, [`StrictMode`]({{ "/en/glossary/strict-mode/" | relative_url }}) with `detectDiskReads()` and `detectNetwork()` makes the answer loud the first time the code runs on a device.
- **Do not wrap what is already safe.** `withContext(Dispatchers.IO) { dao.insert(x) }` around a [Room]({{ "/en/glossary/room/" | relative_url }}) [`suspend`]({{ "/en/glossary/suspend-functions/" | relative_url }}) method does nothing useful — [Room]({{ "/en/glossary/room/" | relative_url }}) already hops — and it costs a redundant dispatch plus a reader who now believes the [DAO]({{ "/en/glossary/dao/" | relative_url }}) is *not* main-safe. The same for [Retrofit]({{ "/en/glossary/retrofit/" | relative_url }}) [`suspend`]({{ "/en/glossary/suspend-functions/" | relative_url }}) calls and [DataStore]({{ "/en/glossary/datastore/" | relative_url }}). Double-wrapping is a signal that the author does not trust the contract, and it spreads.
- **The choice of [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) is part of main-safety, not an afterthought.** Blocking I/O on [`Default`]({{ "/en/glossary/dispatchers-default/" | relative_url }}) starves computation — [`Default`]({{ "/en/glossary/dispatchers-default/" | relative_url }}) has as many threads as cores, and a parked socket read holds one hostage. CPU loops on [`IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) are merely wasteful. Date math over months of recurrence rules, sorting thousands of rows, parsing a large JSON: [`Default`]({{ "/en/glossary/dispatchers-default/" | relative_url }}). Reading the JSON from disk: [`IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}). One function can legitimately do both, in two [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}) blocks.
- **Main-safe does not mean fast.** A main-safe function can still take ten seconds; it just does not freeze the UI while doing so. The user still sees a spinner for ten seconds. Main-safety removes [jank]({{ "/en/glossary/jank/" | relative_url }}) and [ANRs]({{ "/en/glossary/anr/" | relative_url }}) — it does not remove the need for caching, pagination, or a progress indicator. Conflating the two leads to "I added `withContext(IO)`, why is the screen still slow?".
- **Blocking *inside* a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) on Main is the modern [ANR]({{ "/en/glossary/anr/" | relative_url }}).** [`runBlocking`]({{ "/en/glossary/run-blocking/" | relative_url }}) on Main, [`Thread.sleep`]({{ "/en/glossary/thread/" | relative_url }}), a [`CountDownLatch.await()`]({{ "/en/glossary/count-down-latch/" | relative_url }}), a synchronous `Task.getResult()` from Play Services, [`MobileAds.initialize()`]({{ "/en/glossary/sdk/" | relative_url }}) — all of them park the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) *while inside a perfectly good [coroutine]({{ "/en/glossary/coroutines/" | relative_url }})*. Structured concurrency does not help here; only moving the call to a background [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) does. And because [SDK]({{ "/en/glossary/sdk/" | relative_url }}) bootstraps often hide 500 ms of synchronous work behind an async-looking [callback]({{ "/en/glossary/callbacks/" | relative_url }}) API, the senior move is to measure, not to trust the signature.
- **Compose has the same rule with different spelling.** [`LaunchedEffect`]({{ "/en/glossary/launched-effect/" | relative_url }}) and [`produceState`]({{ "/en/glossary/produce-state/" | relative_url }}) run on Main. A [blocking call]({{ "/en/glossary/blocking-call/" | relative_url }}) inside them blocks composition. `produceState { value = withContext(IO) { load() } }` is the [composable]({{ "/en/glossary/composable/" | relative_url }}) version of a main-safe repository call.
- **Injected [dispatchers]({{ "/en/glossary/dispatcher/" | relative_url }}) make main-safety testable.** Hard-coding [`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) ties the hop to a real [thread pool]({{ "/en/glossary/thread-pool/" | relative_url }}) that [`runTest`]({{ "/en/glossary/run-test/" | relative_url }}) cannot control. Injecting an [`@IoDispatcher`]({{ "/en/glossary/io-dispatcher/" | relative_url }}) lets the test substitute a [`TestDispatcher`]({{ "/en/glossary/test-dispatcher/" | relative_url }}) and drive the "background" work in virtual time — proving the function suspends where it claims to.

## Code in Action

### The canonical shape: `withContext` as the function body

`BackupManager` reads and writes files through the [`ContentResolver`]({{ "/en/glossary/content-resolver/" | relative_url }}). Every public [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) is main-safe because the switch to [`IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) *is* its body — no caller can forget it.

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

suspend fun importFrom(uri: Uri): Result<Unit> = withContext(Dispatchers.IO) { /* ... */ }
```

Note what is inside: `openOutputStream`, `stream.write` and JSON serialisation — all synchronous, all blocking. The `backupDao.getAll*()` calls are [Room]({{ "/en/glossary/room/" | relative_url }}) [`suspend`]({{ "/en/glossary/suspend-functions/" | relative_url }}) methods and would be main-safe on their own; wrapping them in the same [`IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) block is fine because the *rest* of the block genuinely needs it, and because [`IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) and [Room]({{ "/en/glossary/room/" | relative_url }})'s executor are both background threads anyway.

### Switching only around the part that blocks

`LegacyDataImporter` mixes three kinds of work: [DataStore]({{ "/en/glossary/datastore/" | relative_url }}) reads (already main-safe), [Room]({{ "/en/glossary/room/" | relative_url }}) inserts (already main-safe), and raw file operations (not). It wraps *only* the file operations.

```kotlin
// From FollowApp Suite — LegacyDataImporter.kt
suspend fun runIfNeeded() {
    if (preferences.isImportDoneOnce()) return          // DataStore: main-safe

    if (!reader.legacyDatabaseExists()) {
        preferences.markImportDone()
        return
    }

    runCatching {
        val legacyTasks = withContext(Dispatchers.IO) { reader.readLegacyTasks() }   // raw SQLite read
        if (legacyTasks.isNotEmpty()) {
            val now = System.currentTimeMillis()
            taskDao.insertTasks(                                                      // Room: main-safe
                legacyTasks.mapIndexed { index, task -> task.toTaskEntity(index, now) }
            )
        }
        preferences.markImportDone()
        withContext(Dispatchers.IO) { archiveLegacyFile() }                          // File.renameTo
        Log.d(TAG, "Legacy import complete: ${legacyTasks.size} task(s)")
    }.onFailure { e ->
        Log.e(TAG, "Legacy import failed; will retry next launch", e)
    }
}
```

This is main-safety applied with precision: two [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}) blocks around the two calls that park a thread, and nothing around the calls that already honour the contract. One thing a reviewer would flag: `reader.legacyDatabaseExists()` is a `File.exists()` — a disk stat — running on the caller's [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}). It is cheap, but it is a [blocking call]({{ "/en/glossary/blocking-call/" | relative_url }}) outside a switch, and the comment above it ("paid only once") is the author acknowledging the trade-off.

### CPU work is not exempt

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

No I/O here — pure date arithmetic — yet it hops, to [`Default`]({{ "/en/glossary/dispatchers-default/" | relative_url }}). The comment names the exact failure mode: input dispatching stalls, and a long enough stall while a popup is open is an [ANR]({{ "/en/glossary/anr/" | relative_url }}). Main-safety is about *time on Main*, not about what kind of work consumes it.

### Main-safety in Compose: `produceState`

```kotlin
// From FollowApp Suite — AboutScreen.kt
val licenses by produceState<List<License>?>(initialValue = null, key1 = context) {
    value = withContext(Dispatchers.IO) { loadLicenses(context) }
}
```

[`produceState`]({{ "/en/glossary/produce-state/" | relative_url }}) launches a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) on the composition's [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) — Main. `loadLicenses` reads a raw resource and parses it: blocking. The [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}) is what keeps the first frame of the About screen from waiting on disk. Without it the screen would still *eventually* render — but only after freezing on the way in.

### What "already main-safe" looks like

```kotlin
// From FollowApp Suite — LabelDao.kt
@Dao
interface LabelDao {
    @Query("SELECT * FROM labels ORDER BY name ASC")
    fun getLabelsStream(): Flow<List<LabelEntity>>

    @Query("SELECT * FROM labels WHERE name = :name LIMIT 1")
    suspend fun getLabelByName(name: String): LabelEntity?

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insertLabel(label: LabelEntity): Long
}
```

```kotlin
// From FollowApp Suite — LegacyImportPreferences.kt
fun isImportDone(): Flow<Boolean> = dataStore.data.map { it[importDoneKey] ?: false }
suspend fun isImportDoneOnce(): Boolean = isImportDone().first()
```

Neither file mentions a [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}), and neither needs to. [Room]({{ "/en/glossary/room/" | relative_url }}) runs every [`suspend`]({{ "/en/glossary/suspend-functions/" | relative_url }}) [DAO]({{ "/en/glossary/dao/" | relative_url }}) method on its query/transaction executor and every [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) query on a background observer; [DataStore]({{ "/en/glossary/datastore/" | relative_url }}) performs its reads on [`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) internally. These are the libraries honouring the contract so that the code above them can stay [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }})-free. Wrapping `insertLabel` in `withContext(IO)` would add nothing but noise.

### The blocking call that hides behind a callback

```kotlin
// From FollowApp Suite — ConsentManager.kt
// MobileAds.initialize does ~700 ms of synchronous SDK bootstrap on
// the caller thread even though it exposes an async callback.
CoroutineScope(SupervisorJob() + Dispatchers.IO).launch {
    MobileAds.initialize(app)
}
```

`MobileAds.initialize(context, listener)` *looks* asynchronous — it takes a completion listener. The measurement in the comment says otherwise: 700 ms of synchronous work on whatever thread calls it. Called from [`Application.onCreate()`]({{ "/en/glossary/application-on-create/" | relative_url }}) that is 700 ms added to cold start and, on a slow device, an [ANR]({{ "/en/glossary/anr/" | relative_url }}). The fix is the same as for any [blocking call]({{ "/en/glossary/blocking-call/" | relative_url }}): move it to [`IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}). The lesson is that main-safety is decided by [profiling]({{ "/en/glossary/profiling/" | relative_url }}), not by reading signatures.

### Making the hop testable — Not found in FAS

`BackupManager` hard-codes [`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}). Its tests therefore run the real pool. The injected form:

```kotlin
// Not found in FAS — standalone example
class BackupManager @Inject constructor(
    @IoDispatcher private val io: CoroutineDispatcher,
    /* ... */
) {
    suspend fun exportTo(uri: Uri): Result<Unit> = withContext(io) { /* ... */ }
}

@Test
fun `exportTo is main-safe`() = runTest {
    val io = StandardTestDispatcher(testScheduler)
    val manager = BackupManager(io = io, /* ... */)
    val job = launch { manager.exportTo(uri) }
    // the function has suspended at withContext(io); nothing ran on the caller yet
    assertTrue(job.isActive)
    advanceUntilIdle()
    assertTrue(job.isCompleted)
}
```

The test can *observe the suspension*: after [`launch`]({{ "/en/glossary/launch/" | relative_url }}), the body has not executed because the injected [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) has not been advanced. A function that blocked instead of switching would have completed synchronously — which is exactly the bug this test exists to catch.

## The Interview (The Hot Seat)

**Question**: What does "main-safe" mean, whose responsibility is it, and does marking a function [`suspend`]({{ "/en/glossary/suspend-functions/" | relative_url }}) make it main-safe?

**Senior Answer**: A [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) is main-safe when calling it from the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) never blocks that thread — it may take a long time, but it only ever *suspends*, so the UI keeps drawing and handling input while the work happens on a background [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}). It is the *callee's* responsibility, because the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) is inherited: a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) runs on whatever [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) its caller had, so if the caller is [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) on Main and the function reads a file without switching, Main blocks. Putting [`withContext(Dispatchers.IO)`]({{ "/en/glossary/with-context/" | relative_url }}) *inside* the function that does the blocking work — once — makes the guarantee local and means no caller has to remember it. The ecosystem convention is that every [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) is main-safe; [Room]({{ "/en/glossary/room/" | relative_url }}), [Retrofit]({{ "/en/glossary/retrofit/" | relative_url }}) and [DataStore]({{ "/en/glossary/datastore/" | relative_url }}) honour it, so I never wrap their calls, and I only write [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}) around raw I/O, heavy CPU, or a synchronous [SDK]({{ "/en/glossary/sdk/" | relative_url }}). And no, [`suspend`]({{ "/en/glossary/suspend-functions/" | relative_url }}) does not make anything main-safe: it is a promise about how the function may be *called*, not about where it runs. `suspend fun load() = File(p).readText()` compiles, passes tests on a [`TestDispatcher`]({{ "/en/glossary/test-dispatcher/" | relative_url }}), and blocks Main in production for the whole read — because there is no [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}) in it. The question I ask of every [`suspend fun`]({{ "/en/glossary/suspend-functions/" | relative_url }}) that touches disk, network or a big loop is "where is the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) switch?", and if it is not in the function, the function is not main-safe.

**Question**: You inherit a repository whose [suspend functions]({{ "/en/glossary/suspend-functions/" | relative_url }}) block the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}). Walk me through fixing it, and how you would prove the fix in a test.

**Senior Answer**: First I find *which* calls block, by [profiling]({{ "/en/glossary/profiling/" | relative_url }}) rather than by reading — a synchronous [SDK]({{ "/en/glossary/sdk/" | relative_url }}) bootstrap or a `File.exists()` can hide behind an innocent signature, and a method that takes a [callback]({{ "/en/glossary/callbacks/" | relative_url }}) can still do hundreds of milliseconds of synchronous work before returning. Then, for each [blocking call]({{ "/en/glossary/blocking-call/" | relative_url }}), I wrap the *blocking part* — not the whole function — in [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}) with the [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) that matches the work: [`IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) for anything that parks a thread on disk or network, [`Default`]({{ "/en/glossary/dispatchers-default/" | relative_url }}) for anything that burns CPU like parsing or date math. I leave [Room]({{ "/en/glossary/room/" | relative_url }}), [Retrofit]({{ "/en/glossary/retrofit/" | relative_url }}) and [DataStore]({{ "/en/glossary/datastore/" | relative_url }}) calls unwrapped, because they are already main-safe and double-wrapping is noise that misleads the next reader. I inject the [dispatchers]({{ "/en/glossary/dispatcher/" | relative_url }}) through a qualifier like [`@IoDispatcher`]({{ "/en/glossary/io-dispatcher/" | relative_url }}) instead of hard-coding [`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}), because that is what makes the fix provable. In the test I use [`runTest`]({{ "/en/glossary/run-test/" | relative_url }}), pass a `StandardTestDispatcher(testScheduler)` as the injected [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}), [`launch`]({{ "/en/glossary/launch/" | relative_url }}) a call to the function, and assert *before* advancing the scheduler that the job is still active and that the fake I/O has not been touched — that proves the function suspended at the switch instead of blocking through. Then [`advanceUntilIdle()`]({{ "/en/glossary/advance-until-idle/" | relative_url }}) and assert the result. A function that still blocked would have run to completion synchronously inside [`launch`]({{ "/en/glossary/launch/" | relative_url }}) on [`Main.immediate`]({{ "/en/glossary/dispatchers-main-immediate/" | relative_url }}), and the first assertion would fail. The last thing I would say is that main-safe is not the same as fast: after the fix the UI no longer freezes, but if the operation takes three seconds the user still needs a progress indicator, and that is a separate piece of work.

---

[Back to Chapters]({{ "/" | relative_url }})
