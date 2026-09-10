---
layout: page
title: Suspend Functions
lang: en
permalink: /en/02-coroutines-flow/suspend-functions/
order: 1
---

## The Theory (The What)

A [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) is a function marked with the `suspend` [keyword]({{ "/en/glossary/keyword/" | relative_url }}) that can pause its execution at a [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}) and resume later — possibly on a different [thread]({{ "/en/glossary/thread/" | relative_url }}) — without blocking the thread it was running on. It is the unit of composition in Kotlin [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}): everything else (`launch`, `async`, `Flow`, `withContext`) is built on top of it.

- **`suspend` is a [compile-time]({{ "/en/glossary/compile-time/" | relative_url }}) contract, not a thread.** Marking a function `suspend` does not move it anywhere. It runs on whatever thread called it, until it hits a suspension point. The only thing the modifier changes is *who may call it*: another suspend function, or a coroutine builder. The compiler enforces this — calling a suspend function from plain code is a compile error, which is the whole point.
- **The compiler rewrites it in [Continuation-Passing Style]({{ "/en/glossary/continuation-passing-style/" | relative_url }}).** `suspend fun load(id: String): Task` becomes, in [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}), `fun load(id: String, cont: Continuation<Task>): Any?`. The extra parameter is the [continuation]({{ "/en/glossary/continuation/" | relative_url }}): a [callback]({{ "/en/glossary/callbacks/" | relative_url }}) that knows how to resume the caller with a result or an exception. The [return type]({{ "/en/glossary/return-type/" | relative_url }}) becomes `Any?` because the function returns either the real value *or* a sentinel `COROUTINE_SUSPENDED` marker meaning "I paused, I will call the continuation later".
- **The body becomes a [state machine]({{ "/en/glossary/state-machine/" | relative_url }}).** Every suspension point gets a label; local variables that must survive a suspension are hoisted into fields of the continuation object (on the [heap]({{ "/en/glossary/heap/" | relative_url }}), not the [stack]({{ "/en/glossary/stack-frame/" | relative_url }})). When the function resumes, a `when(label)` jumps straight to the right point. This is why a suspended coroutine costs a few hundred bytes instead of a thread's megabyte of stack.
- **Suspending is not the same as [blocking]({{ "/en/glossary/blocking-call/" | relative_url }}).** A blocking call — `Thread.sleep`, a synchronous `InputStream.read`, a `runBlocking` — parks the *thread*. A suspending call returns the thread to its [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) so it can run other coroutines. Wrapping a blocking call in a `suspend fun` does not make it suspend; only a function that *actually* suspends (`delay`, `withContext`, a Room [DAO]({{ "/en/glossary/dao/" | relative_url }}) call, `suspendCancellableCoroutine`) does.
- **Sequential by default.** Inside a suspend function, one line runs after the other, exactly as it reads. Concurrency is opt-in — you have to ask for it with `async` or `launch` inside a [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}). This is the inverse of [callback]({{ "/en/glossary/callbacks/" | relative_url }}) APIs, where sequencing is the thing you have to work for.

## The Senior Perspective (The Why)

- **The modifier is documentation the compiler checks.** When a method on a repository interface says `suspend`, it tells every caller "this may take a while and you need a scope to call me". When it does *not* say `suspend`, it promises to return immediately. FAS repository interfaces separate the two cleanly: `Flow<T>` for streams, `suspend fun` for one-shot operations, plain `fun` for nothing that touches I/O. Reviewers can spot a main-thread violation from the signature alone — a plain `fun` that internally does disk work is a bug you can see without reading the body.
- **Suspend functions should be main-safe.** The convention across Android is that a suspend function can be called from `Dispatchers.Main` without thinking. That means the function itself is responsible for moving blocking work off the main thread — `withContext(Dispatchers.IO)` *inside* the function, not at every call site. Room and Retrofit already do this for you: their `suspend` DAO/service methods hop to their own [thread pool]({{ "/en/glossary/thread-pool/" | relative_url }}) and resume you back. Your own file or JSON code does not, which is why `BackupManager` wraps its body in `withContext(Dispatchers.IO)`.
- **Cancellation is cooperative, and suspension is where it happens.** A coroutine is cancelled only when it reaches a suspension point (or checks `isActive`/`ensureActive()` explicitly). Every real suspend call — `delay`, `withContext`, `Flow.collect`, a DAO query — checks for cancellation before and after suspending and throws [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}). A suspend function that only does CPU work in a loop without ever suspending is uncancellable; it will keep running after the [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) that launched it is gone. [Cooperative cancellation]({{ "/en/glossary/cooperative-cancellation/" | relative_url }}) is the price of not being preemptively killed mid-write.
- **Never swallow `CancellationException`.** `runCatching { }` and `catch (e: Exception)` both catch it, which turns a cancelled coroutine into one that quietly continues past the point where it should have died. The rule: catch what you can handle, rethrow `CancellationException`. FAS's drag gesture handler does exactly this — it catches to reset local state, then rethrows.
- **[`runBlocking`]({{ "/en/glossary/run-blocking/" | relative_url }}) is the bridge, not the pattern.** It exists to call suspend code from a place that has no coroutine: `main()`, a JUnit test, and — very deliberately — `Application.onCreate` when you *must* have a value before the first frame. Every use in production code should come with a comment explaining why blocking the caller is acceptable. FAS has two, both with a paragraph of justification and an issue number.
- **Bridging callbacks is a one-time cost.** [`suspendCancellableCoroutine`]({{ "/en/glossary/suspend-cancellable-coroutine/" | relative_url }}) turns any [callback]({{ "/en/glossary/callbacks/" | relative_url }})-based API into a suspend function once, at the edge; from there on the rest of the codebase is sequential. The Jetpack libraries have already done this for you (Credential Manager's `getCredential` is suspend; `Task.await()` for Play Services), which is why modern Android code has almost no [callback hell]({{ "/en/glossary/callback-hell/" | relative_url }}) left.
- **`suspend` on a lambda is a type, not just a modifier.** `suspend () -> Unit` is a distinct function type; a [higher-order function]({{ "/en/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) that accepts it can call suspend code inside the lambda. `withContext`, `coroutineScope`, `withTransaction` and `launch` all take suspend lambdas — that is how they let you suspend inside their block.

## Code in Action

### The signature is the contract

The [DAO]({{ "/en/glossary/dao/" | relative_url }}) separates what is a stream from what is a one-shot operation. `getLabelsStream` returns a `Flow` and is *not* suspend — subscribing costs nothing. Every write and point-read is `suspend`, and [Room]({{ "/en/glossary/room/" | relative_url }}) generates the implementation that runs the query on its own executor and resumes the caller.

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

    @Query("UPDATE labels SET name = :name, updated_at = :updatedAt WHERE id = :labelId")
    suspend fun renameLabel(labelId: String, name: String, updatedAt: String)

    @Query("DELETE FROM labels WHERE id = :labelId")
    suspend fun deleteLabel(labelId: String)
}
```

Because these are main-safe, the [ViewModel]({{ "/en/glossary/viewmodel-store/" | relative_url }}) can call them from [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) (which defaults to `Dispatchers.Main.immediate`) without a dispatcher switch.

### Sequential code that reads like a story

A use case composes several suspend calls in order. There is no callback nesting, no `then`, no explicit thread — and if the enclosing scope is cancelled between step one and step two, step two simply never runs.

```kotlin
// From FollowApp Suite — QuickCompleteTaskUseCase.kt
suspend operator fun invoke(taskId: String, isCompleted: Boolean, cascade: Boolean = false) {
    taskRepository.updateTaskCompletion(taskId = taskId, isCompleted = isCompleted)
    if (cascade) {
        taskRepository.updateDescendantsCompletion(taskId = taskId, isCompleted = isCompleted)
    }
    if (isCompleted) {
        spawnNextOccurrence(taskId)
    }
}
```

Each line is a [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}). The compiler generates a [state machine]({{ "/en/glossary/state-machine/" | relative_url }}) with three labels; `taskId`, `isCompleted` and `cascade` are stored in the [continuation]({{ "/en/glossary/continuation/" | relative_url }}) so they survive each suspension.

### Making a suspend function main-safe

Writing a file is [blocking]({{ "/en/glossary/blocking-call/" | relative_url }}) I/O. `BackupManager` takes responsibility for that inside the function, so callers on Main do not have to know.

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

`LegacyDataImporter` is more surgical: only the two genuinely blocking calls are wrapped, and the DAO insert — already main-safe — stays on the caller's dispatcher.

```kotlin
// From FollowApp Suite — LegacyDataImporter.kt
suspend fun runIfNeeded() {
    if (preferences.isImportDoneOnce()) return
    // ...
    runCatching {
        val legacyTasks = withContext(Dispatchers.IO) { reader.readLegacyTasks() }
        if (legacyTasks.isNotEmpty()) {
            val now = System.currentTimeMillis()
            taskDao.insertTasks(
                legacyTasks.mapIndexed { index, task -> task.toTaskEntity(index, now) }
            )
        }
        preferences.markImportDone()
        withContext(Dispatchers.IO) { archiveLegacyFile() }
    }.onFailure { e ->
        Log.e(TAG, "Legacy import failed; will retry next launch", e)
    }
}
```

The same applies to CPU-heavy work. Date math over months of recurrence patterns is not I/O, but it would still stall input on Main, so the [ViewModel]({{ "/en/glossary/viewmodel-store/" | relative_url }}) hops to `Dispatchers.Default`:

```kotlin
// From FollowApp Suite — TasksViewModel.kt
viewModelScope.launch {
    // Date math off the main thread: pattern scans over months/years
    // must never stall input dispatching (popup ANR)
    val suggested = withContext(Dispatchers.Default) {
        val settings = getRecurrenceSettingsUseCase().first()
        // ... RecurrenceCalculator.suggestPatternDueDate(...)
    }
    // back on Main here
}
```

### Suspend does not mean sequential when you ask for concurrency

Completing twenty selected tasks one after the other would be twenty round-trips. [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) is itself a suspend function: it launches the children, suspends until *all* of them finish, and rethrows if any fails. The `finally` runs exactly once, after every write is done.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
isBulkWriteInFlight = true
try {
    coroutineScope {
        ids.forEach { launch { quickCompleteTaskUseCase(taskId = it, isCompleted = isCompleted) } }
    }
} finally {
    isBulkWriteInFlight = false
}
```

### Rethrow cancellation

A pointer-input coroutine is disposed whenever the composable leaves composition. The handler catches [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) only to clean up local drag state, then rethrows so the coroutine machinery still sees the cancellation.

```kotlin
// From FollowApp Suite — DragToReorder.kt
} catch (e: CancellationException) {
    // Gesture coroutine disposed mid-drag (e.g. composition change)
    state.endDrag(cancelled = true)
    throw e
}
```

Compare with the sign-in flow, which catches a *domain* cancellation (the user dismissed the picker) and deliberately treats it as a non-error — a different exception type, a different decision:

```kotlin
// From FollowApp Suite — SettingsViewModel.kt
viewModelScope.launch {
    try {
        val session = googleAuthClient.signIn(activityContext)
        saveUserSessionUseCase(session)
    } catch (e: GetCredentialCancellationException) {
        Log.d(TAG, "Google sign-in cancelled by user")
    } catch (e: GetCredentialException) {
        _uiState.update { it.copy(messageRes = R.string.error_sign_in) }
    }
}
```

### `runBlocking` — the justified exception

`Application.onCreate` has no coroutine and *must* know the locale and theme before the first Activity inflates, or the user sees a flash. This is the one place FAS blocks the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) on suspend code, and the comment says why.

```kotlin
// From FollowApp Suite — MyTasksApplication.kt
// All three values live in the same "settings" DataStore — reading
// them in a single runBlocking triggers exactly one cold file open.
val (language, themeMode, contrastLevel) = runBlocking {
    Triple(
        languagePreferences.getLanguage().first(),
        themePreferences.getThemeMode().first(),
        themePreferences.getContrastLevel().first()
    )
}
```

### Bridging a callback API

FAS consumes APIs that Jetpack has already wrapped (`CredentialManager.getCredential` is suspend). When you own the wrapping, this is the shape:

```kotlin
// Not found in FAS — standalone example
suspend fun LocationClient.awaitLastLocation(): Location? =
    suspendCancellableCoroutine { cont ->
        val listener = object : LocationListener {
            override fun onSuccess(loc: Location?) = cont.resume(loc)
            override fun onFailure(e: Exception) = cont.resumeWithException(e)
        }
        requestLastLocation(listener)
        cont.invokeOnCancellation { removeListener(listener) }
    }
```

Three obligations: resume exactly once, propagate the failure, and unregister on cancellation. Miss the third and a cancelled coroutine leaks the listener; miss the first and the caller hangs forever.

### What the compiler generates

```kotlin
// Not found in FAS — standalone example (simplified decompilation)
suspend fun load(id: String): Task {
    val raw = fetch(id)        // suspension point 1
    val parsed = parse(raw)    // suspension point 2
    return parsed
}

// becomes, roughly:
fun load(id: String, cont: Continuation<Task>): Any? {
    val sm = cont as? LoadSM ?: LoadSM(cont)
    when (sm.label) {
        0 -> { sm.label = 1; val r = fetch(id, sm); if (r == COROUTINE_SUSPENDED) return r; sm.raw = r }
        1 -> { sm.raw = sm.result }
    }
    when (sm.label) {
        1 -> { sm.label = 2; val p = parse(sm.raw, sm); if (p == COROUTINE_SUSPENDED) return p; return p }
        2 -> return sm.result
    }
}
```

No threads, no magic: a function that returns early with a marker, and an object that remembers where to pick up. Everything a coroutine "does" reduces to this.

## The Interview (The Hot Seat)

**Question**: What does the `suspend` keyword actually do?

**Senior Answer**: It changes the function's [compile-time]({{ "/en/glossary/compile-time/" | relative_url }}) signature and nothing about where it runs. The compiler rewrites the function in [Continuation-Passing Style]({{ "/en/glossary/continuation-passing-style/" | relative_url }}): it gains a hidden `Continuation<T>` parameter and its return type becomes `Any?`, so it can return either the real result or the `COROUTINE_SUSPENDED` marker. The body is compiled into a [state machine]({{ "/en/glossary/state-machine/" | relative_url }}) whose labels are the [suspension points]({{ "/en/glossary/suspension-point/" | relative_url }}); locals that cross a suspension are hoisted into the [continuation]({{ "/en/glossary/continuation/" | relative_url }}) object on the [heap]({{ "/en/glossary/heap/" | relative_url }}). When a call actually suspends, the function returns the marker, the [thread]({{ "/en/glossary/thread/" | relative_url }}) goes back to its [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}), and later something calls `continuation.resume(value)`, which re-enters the function and jumps to the right label. That is why a suspend function needs a coroutine to be called from — it needs a continuation to hand over. Two consequences matter in practice: `suspend` does not make a [blocking]({{ "/en/glossary/blocking-call/" | relative_url }}) call non-blocking, only real suspension points do; and a suspend function that never reaches a suspension point can never be cancelled, because [cancellation]({{ "/en/glossary/cooperative-cancellation/" | relative_url }}) is checked at those points.

**Question**: A teammate wraps `File.readText()` in a `suspend fun` and calls it from `viewModelScope.launch`. The UI still freezes. Why, and what do you change?

**Senior Answer**: Because `suspend` is a contract about *who can call you*, not a thread switch. [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) runs on `Dispatchers.Main.immediate`, the function runs on that thread until it hits a real suspension point, and `readText()` is a [blocking call]({{ "/en/glossary/blocking-call/" | relative_url }}) — it never suspends, so it parks the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) for the duration of the read. The fix is to make the function *main-safe*: wrap the blocking body in `withContext(Dispatchers.IO)` inside the suspend function itself, the way `BackupManager` does, so every caller — the ViewModel, a test, a WorkManager worker — gets correct behaviour without knowing about I/O. I would not put the `withContext` at the call site, because then the next caller forgets it. And I would check that the surrounding code doesn't `runCatching` the whole thing, because that swallows [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) and turns a cancelled screen into a coroutine that keeps writing to disk after the ViewModel is cleared.

---

[Back to Chapters]({{ "/" | relative_url }})
