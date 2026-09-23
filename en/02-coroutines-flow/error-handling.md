---
layout: page
title: "Error Handling: try-catch & .catch"
lang: en
permalink: /en/02-coroutines-flow/error-handling/
order: 8
---

## The Theory (The What)

Coroutines do not invent a new error mechanism: an exception thrown inside a [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) propagates up the [call stack]({{ "/en/glossary/call-stack/" | relative_url }}) like any other, and an ordinary [`try/catch`]({{ "/en/glossary/try-catch/" | relative_url }}) around a suspending call works exactly as you would expect. What changes is the shape of the code you are protecting.

For **imperative suspending code** — one call, one result — `try/catch` is the tool, and [`runCatching`]({{ "/en/glossary/run-catching/" | relative_url }}) is the functional version that packages success or failure into a [`Result`]({{ "/en/glossary/result/" | relative_url }}).

For a **[`Flow`]({{ "/en/glossary/flow/" | relative_url }})** the tool is the [`catch`]({{ "/en/glossary/catch/" | relative_url }}) operator, and it obeys one rule: **it only sees exceptions from its [upstream]({{ "/en/glossary/upstream/" | relative_url }})**. An exception thrown in the [`collect`]({{ "/en/glossary/collect/" | relative_url }}) block, which is [downstream]({{ "/en/glossary/downstream/" | relative_url }}), is not caught by a `catch` written above it. Inside the operator you can log, update state, or [`emit`]({{ "/en/glossary/emit/" | relative_url }}) a fallback value, turning a failure into a normal emission.

That rule is the consequence of **[exception transparency]({{ "/en/glossary/exception-transparency/" | relative_url }})**: a flow's producer must let exceptions travel to the collector instead of swallowing them. Wrapping your own [`emit`]({{ "/en/glossary/emit/" | relative_url }}) in a `try/catch` inside a `flow { }` builder violates it, and the [runtime]({{ "/en/glossary/runtime/" | relative_url }}) will tell you so.

Cancellation is the exception to all of this. [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) is not an error: it is the signal that a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }})'s [job]({{ "/en/glossary/job/" | relative_url }}) was cancelled. Swallowing it breaks [cooperative cancellation]({{ "/en/glossary/cooperative-cancellation/" | relative_url }}) — the [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) keeps running after its scope is gone. It must always be rethrown.

## The Senior Perspective (The Why)

- **`catch { }` upstream, `try { }` downstream — and the difference bites.** A `.catch` above `.collect` protects the producer and every operator between them; it does **not** protect the collector's own body. If the code that writes to UI state can throw, that needs its own `try/catch` inside the `collect` block, or the work moves up into an [`onEach`]({{ "/en/glossary/on-each/" | relative_url }}) above the `catch`. Teams discover this the hard way when a crash in a mapping function inside `collect` takes down the app despite a `.catch` sitting right above it.
- **`catch (e: Exception)` swallows cancellation.** On the [JVM]({{ "/en/glossary/jvm/" | relative_url }}) [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) is a [`RuntimeException`]({{ "/en/glossary/runtime-exception/" | relative_url }}), so a broad `catch (e: Exception)` around suspending code catches the cancellation signal and quietly keeps going. The [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) survives its own cancellation, the [scope]({{ "/en/glossary/coroutine-scope/" | relative_url }}) never finishes, and a screen that was closed keeps doing work. Catch narrow types, or catch broadly and rethrow cancellation explicitly.
- **[`runCatching`]({{ "/en/glossary/run-catching/" | relative_url }}) has the same trap, and it is worse because it looks safe.** It catches [`Throwable`]({{ "/en/glossary/throwable/" | relative_url }}), which includes [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}). In [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) code it should either be avoided or immediately followed by a rethrow of cancellation. Its legitimate home is a boundary that is genuinely one-shot and never cancelled mid-flight — an export, a parse, a bridge to a callback API — where returning a `Result` to the caller is nicer than throwing.
- **Catch cancellation only to clean up, then rethrow.** There is one valid reason to catch a [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}): releasing something the [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) owns — ending a drag, closing a stream, restoring a visual state. The pattern is always the same: do the cleanup, then `throw e`. [`finally`]({{ "/en/glossary/finally/" | relative_url }}) covers most cases; the explicit catch is for when cleanup depends on *why* the [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) ended.
- **Map exceptions to user messages at the UI boundary, not in the data layer.** A repository that turns a [`SQLiteConstraintException`]({{ "/en/glossary/sqlite-constraint-exception/" | relative_url }}) into "Something went wrong" has destroyed the only information anyone could act on. Let technical exceptions travel; translate them once, in the UI layer, where you know the screen, the copy and the locale.
- **An error is a state, not just a log line.** `.catch { }` that only calls `Log.e` leaves the UI stuck on a spinner forever. If a failure means the screen cannot show data, the catch block has to move the [state holder]({{ "/en/glossary/state-holder/" | relative_url }}) into an error state — which is also why sealed UI state with an [`Error`]({{ "/en/glossary/error-state/" | relative_url }}) member pays off here.

## Code in Action

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// .catch protects the upstream flow: if the catalog use case fails,
// the collector never runs and the app does not crash
private fun observeLabels() {
    viewModelScope.launch {
        getLabelsCatalogUseCase()
            .catch { error ->
                Log.e(TAG, "Error loading labels", error)
            }
            .collect { allLabels ->
                _labelsWithOptions.value = allLabels
            }
    }
}

// From FollowApp Suite — LabelsListViewModel.kt
// The mature version: the failure becomes UI state, not only a log line
combine(getLabelsCatalogUseCase(), getActiveTasksUseCase(), _resyncTrigger) { catalog, tasks, _ ->
    buildCatalogState(catalog, tasks)
}
    .catch { e ->
        Log.e(TAG, "Error loading labels", e)
        _uiState.update {
            it.copy(isLoading = false, errorMessageRes = e.toUserMessage())
        }
    }
    .collect { (sortedLabels, scales) -> /* ... */ }

// From FollowApp Suite — ErrorMapping.kt
// Translation happens once, at the UI boundary — the data layer keeps
// throwing technical exceptions that carry real information
fun Throwable.toUserMessage(): Int = when {
    this is SQLiteConstraintException && message.orEmpty().contains("UNIQUE") ->
        R.string.error_duplicate_tag
    else -> R.string.error_generic
}

// From FollowApp Suite — DragToReorder.kt
// The only correct way to catch cancellation: clean up, then RETHROW.
// Without the throw, the gesture coroutine would survive its own cancellation.
try {
    // ... drag gesture loop
} catch (e: CancellationException) {
    // Gesture coroutine disposed mid-drag (e.g. composition change)
    state.endDrag(cancelled = true)
    throw e
}

// From FollowApp Suite — SettingsViewModel.kt
// Narrow catches, and a cancelled sign-in is not an error worth showing
viewModelScope.launch {
    try {
        val session = googleAuthClient.signIn(activityContext)
        saveUserSessionUseCase(session)
    } catch (e: GetCredentialCancellationException) {
        Log.d(TAG, "Google sign-in cancelled by user")
    } catch (e: GetCredentialException) {
        Log.e(TAG, "Google sign-in failed", e)
        _uiState.update { it.copy(messageRes = R.string.error_sign_in) }
    }
}

// From FollowApp Suite — BackupManager.kt
// runCatching at a genuine one-shot boundary, returning Result to the caller
suspend fun exportTo(uri: Uri): Result<Unit> = withContext(Dispatchers.IO) {
    runCatching {
        val json = jsonOf(content)
        context.contentResolver.openOutputStream(uri, "wt").use { stream ->
            requireNotNull(stream) { "Cannot open destination" }
            stream.write(json.toByteArray(Charsets.UTF_8))
        }
    }.onFailure { Log.e(TAG, "Backup export failed", it) }
}
```

## The Interview (The Hot Seat)

**Question**: You have `flow.catch { }.collect { }` and the app still crashes. The stack trace points inside the `collect` block. Why did `.catch` not help, and how do you fix it?

**Senior Answer**: Because [`catch`]({{ "/en/glossary/catch/" | relative_url }}) only handles exceptions coming from its [upstream]({{ "/en/glossary/upstream/" | relative_url }}) — the builder and every operator declared **above** it. The [`collect`]({{ "/en/glossary/collect/" | relative_url }}) block is [downstream]({{ "/en/glossary/downstream/" | relative_url }}), so an exception thrown while handling a value is outside the operator's reach and propagates to the enclosing [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}). That asymmetry is not an accident: it is [exception transparency]({{ "/en/glossary/exception-transparency/" | relative_url }}), the same rule that forbids a `flow { }` builder from wrapping its own [`emit`]({{ "/en/glossary/emit/" | relative_url }}) in a `try/catch`. There are two fixes depending on intent. If the failing work is really part of the pipeline — a mapping, a conversion — I move it into an [`onEach`]({{ "/en/glossary/on-each/" | relative_url }}) or `map` placed *above* the `catch`, and then the operator does cover it. If it is genuinely consumer-side work, like writing to a [state holder]({{ "/en/glossary/state-holder/" | relative_url }}), it gets its own [`try/catch`]({{ "/en/glossary/try-catch/" | relative_url }}) inside the `collect` block. What I would not do is wrap the whole `collect` call in a `try/catch` and call it handled: that catches cancellation too, and it hides which half of the pipeline actually failed.

**Question**: A teammate wraps every [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) body in `try { ... } catch (e: Exception) { log(e) }` so "nothing can crash". What do you tell them?

**Senior Answer**: That it does not make the app safer, it makes cancellation broken. On the [JVM]({{ "/en/glossary/jvm/" | relative_url }}) [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) is a [`RuntimeException`]({{ "/en/glossary/runtime-exception/" | relative_url }}), so `catch (e: Exception)` catches the cancellation signal along with real failures. The [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) then swallows its own cancellation and keeps running: the [scope]({{ "/en/glossary/coroutine-scope/" | relative_url }}) never completes, a closed screen keeps querying, and structured concurrency stops meaning anything — the parent waits for a child that refuses to die. The same applies to [`runCatching`]({{ "/en/glossary/run-catching/" | relative_url }}), which catches [`Throwable`]({{ "/en/glossary/throwable/" | relative_url }}) and is more dangerous precisely because it reads as the safe, idiomatic option. What I ask for instead is narrow catches of the exceptions that a call can actually produce — that is what we do for Google sign-in, where a user-cancelled credential request is logged at debug and a real failure becomes an error message — and, when a broad catch is genuinely needed, an explicit `if (e is [CancellationException]({{ "/en/glossary/cancellation-exception/" | relative_url }})) throw e` first. The one legitimate reason to catch cancellation is cleanup, and then the block must end in `throw e`; that is exactly what our drag gesture does when the composition disposes it mid-drag. Finally, I would point out that "log it and continue" is usually not [error handling]({{ "/en/glossary/state-holder/" | relative_url }}) at all: if the failure means the screen has no data, the user needs an error state, not a line in Logcat.

---

[Back to Chapters]({{ "/" | relative_url }})
