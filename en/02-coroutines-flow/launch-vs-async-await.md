---
layout: page
title: "Launch vs Async/Await"
lang: en
permalink: /en/02-coroutines-flow/launch-vs-async-await/
order: 4
---

## The Theory (The What)

[`launch`]({{ "/en/glossary/launch/" | relative_url }}) and [`async`]({{ "/en/glossary/async/" | relative_url }}) are the two coroutine builders you call on a [`CoroutineScope`]({{ "/en/glossary/coroutine-scope/" | relative_url }}). Both start a child [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) attached to the scope's [`Job`]({{ "/en/glossary/job/" | relative_url }}), both inherit the scope's [`CoroutineContext`]({{ "/en/glossary/coroutine-context/" | relative_url }}), both accept a context override and a [`CoroutineStart`]({{ "/en/glossary/coroutine-start/" | relative_url }}). They differ in exactly one thing: **what they hand back**.

- **[`launch`]({{ "/en/glossary/launch/" | relative_url }})** returns a [`Job`]({{ "/en/glossary/job/" | relative_url }}). The coroutine is a *side effect*: it runs, and the only things you can do with the handle are [`cancel()`]({{ "/en/glossary/cancel/" | relative_url }}) it, [`join()`]({{ "/en/glossary/join/" | relative_url }}) it, or ignore it. Its block returns `Unit`. If the block throws, the exception is an *uncaught failure* of the coroutine: it propagates to the parent [`Job`]({{ "/en/glossary/job/" | relative_url }}) immediately, and if nothing in the tree handles it, to the [`CoroutineExceptionHandler`]({{ "/en/glossary/coroutine-exception-handler/" | relative_url }}) — or the process crashes.
- **[`async`]({{ "/en/glossary/async/" | relative_url }})** returns a [`Deferred<T>`]({{ "/en/glossary/deferred/" | relative_url }}). The coroutine is a *computation*: its block returns `T`, and [`await()`]({{ "/en/glossary/await/" | relative_url }}) suspends the caller until that value exists. [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) extends [`Job`]({{ "/en/glossary/job/" | relative_url }}), so everything [`launch`]({{ "/en/glossary/launch/" | relative_url }}) gives you is still there. If the block throws, the exception is *stored* in the [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) and rethrown to whoever calls [`await()`]({{ "/en/glossary/await/" | relative_url }}) — **and**, unless the parent is a supervisor, it also fails the parent [`Job`]({{ "/en/glossary/job/" | relative_url }}) at the moment it happens, not at the moment of [`await()`]({{ "/en/glossary/await/" | relative_url }}).

[`await()`]({{ "/en/glossary/await/" | relative_url }}) is a [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}). It does not block a [thread]({{ "/en/glossary/thread/" | relative_url }}); it parks the calling coroutine until the [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) completes, and participates in [cancellation]({{ "/en/glossary/cooperative-cancellation/" | relative_url }}) — cancelling the awaiting coroutine throws [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) out of [`await()`]({{ "/en/glossary/await/" | relative_url }}). [`awaitAll()`]({{ "/en/glossary/await-all/" | relative_url }}) on a list of [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) awaits them all and returns the values in order; it fails as soon as *any* of them fails.

The decision, then, is not "which is faster" — they are the same machinery — but **do I need the value?** A sequence of [suspend functions]({{ "/en/glossary/suspend-functions/" | relative_url }}) called one after another needs neither builder: `val a = fetchA(); val b = fetchB(a)` is already sequential and already structured. [`async`]({{ "/en/glossary/async/" | relative_url }}) exists for the case where two computations are *independent* and you want them to overlap: start both, then await both.

[`CoroutineStart.LAZY`]({{ "/en/glossary/coroutine-start/" | relative_url }}) is the third variable: an `async(start = LAZY)` does not run until someone calls [`await()`]({{ "/en/glossary/await/" | relative_url }}) or [`start()`]({{ "/en/glossary/start/" | relative_url }}). It turns a [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) into a memoised, cancellable, on-demand computation — useful, rare, and easy to forget about when a lazy child is never started and the parent waits forever.

## The Senior Perspective (The Why)

- **Pick the builder by the caller's question, not by the callee's work.** "Did it happen?" is [`launch`]({{ "/en/glossary/launch/" | relative_url }}). "What is the answer?" is [`async`]({{ "/en/glossary/async/" | relative_url }}). A ViewModel reacting to a click launches — nobody awaits a click. A [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) assembling a screen from three sources asyncs — the function *is* its return value. Mixing them up produces the two classic smells: an [`async`]({{ "/en/glossary/async/" | relative_url }}) whose [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) is dropped (a [`launch`]({{ "/en/glossary/launch/" | relative_url }}) whose failure is now invisible), and a [`launch`]({{ "/en/glossary/launch/" | relative_url }}) that writes its result into a shared variable for someone to poll (an [`async`]({{ "/en/glossary/async/" | relative_url }}) with a hand-rolled, racy `await`).
- **Never `async { }.await()` on the same line.** `async { fetch() }.await()` is `fetch()` with more allocations and worse stack traces. It does not add concurrency, and it confuses readers into thinking something runs in parallel. The same goes for [`withContext`]({{ "/en/glossary/with-context/" | relative_url }}): switching [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) is [`withContext`]({{ "/en/glossary/with-context/" | relative_url }})'s job, not [`async`]({{ "/en/glossary/async/" | relative_url }})'s.
- **[`async`]({{ "/en/glossary/async/" | relative_url }}) is always a child; a lone [`async`]({{ "/en/glossary/async/" | relative_url }}) is a bug.** Because it needs a scope, [`async`]({{ "/en/glossary/async/" | relative_url }}) is almost always called inside [`coroutineScope { }`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) or [`supervisorScope { }`]({{ "/en/glossary/supervisor-scope/" | relative_url }}). Calling `viewModelScope.async { }` from a plain function and returning the [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) leaks a coroutine handle out of the ViewModel — the caller now owns a piece of the ViewModel's tree. Wrap the parallelism inside a suspend function and return the plain value.
- **The exception path is where interviews go.** With [`launch`]({{ "/en/glossary/launch/" | relative_url }}), a failure is a tree event: parent cancelled (or not, under a [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }})), then handler, then crash. With [`async`]({{ "/en/glossary/async/" | relative_url }}), a failure is *both* a tree event and a stored value. Inside a plain [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}), the tree event wins: the failing [`async`]({{ "/en/glossary/async/" | relative_url }}) cancels its siblings before you reach the [`try/catch`]({{ "/en/glossary/try-catch/" | relative_url }}) around [`await()`]({{ "/en/glossary/await/" | relative_url }}). To make [`await()`]({{ "/en/glossary/await/" | relative_url }}) the *only* place the failure surfaces — and keep the siblings alive — the parent must be [`supervisorScope`]({{ "/en/glossary/supervisor-scope/" | relative_url }}). A [`try/catch`]({{ "/en/glossary/try-catch/" | relative_url }}) around [`await()`]({{ "/en/glossary/await/" | relative_url }}) inside [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) is not wrong, it is just not doing what its author thinks.
- **Parallelism with no result is still [`launch`]({{ "/en/glossary/launch/" | relative_url }}).** N independent writes that return nothing are `coroutineScope { items.forEach { launch { write(it) } } }`. Reaching for [`async`]({{ "/en/glossary/async/" | relative_url }}) there because "it's parallel" is the same category error in reverse: you would be creating N `Deferred<Unit>` and calling [`awaitAll()`]({{ "/en/glossary/await-all/" | relative_url }}) for values you never use. [`launch`]({{ "/en/glossary/launch/" | relative_url }}) inside [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) already waits for all of them.
- **A [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) is a one-shot promise, and that has uses beyond [`async`]({{ "/en/glossary/async/" | relative_url }}).** [`CompletableDeferred<T>`]({{ "/en/glossary/completable-deferred/" | relative_url }}) is a [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) you complete by hand. It is the idiomatic way to gate a coroutine on an external event — a test that wants to hold a repository "in flight" until it says so, a bridge from a one-shot [callback]({{ "/en/glossary/callbacks/" | relative_url }}) into suspend code. It is the coroutine-native [`CountDownLatch(1)`]({{ "/en/glossary/count-down-latch/" | relative_url }}) with a value.
- **Testing is where the difference shows up.** Under [`runTest`]({{ "/en/glossary/run-test/" | relative_url }}), a [`launch`]({{ "/en/glossary/launch/" | relative_url }}) that fails fails the test at the end of the block; an [`async`]({{ "/en/glossary/async/" | relative_url }}) that fails and is never awaited *also* fails the test — the exception is not lost, it reaches the parent. If you ever see an [`async`]({{ "/en/glossary/async/" | relative_url }}) whose result "didn't matter", ask why it was not a [`launch`]({{ "/en/glossary/launch/" | relative_url }}), and what happens to its error.

## Code in Action

### `launch` for a UI event: nobody awaits a click

Confirming the task form kicks off a chain of writes. The caller is a click handler on Main; it cannot suspend and does not need a result. This is the canonical [`launch`]({{ "/en/glossary/launch/" | relative_url }}).

```kotlin
// From FollowApp Suite — TasksViewModel.kt
fun onFormConfirmed() {
    val state = _uiState.value
    // ... validation
    viewModelScope.launch {
        val taskId = if (state.editingTaskId == null) {
            createTaskUseCase(
                title = state.form.title,
                description = state.form.description,
                isCompleted = state.form.isCompleted,
                dueDate = state.form.dueDate
            ) // returns the new task ID
        } else {
            editTaskUseCase(/* ... */)
            state.editingTaskId
        }

        if (selectedLabels.isNotEmpty()) {
            applyLabelAssignmentUseCase(taskId = taskId, labelName = "labels", value = LabelValue.Tag(selectedLabels))
        }
    }
}
```

Notice that *inside* the [`launch`]({{ "/en/glossary/launch/" | relative_url }}) the code is sequential: `applyLabelAssignmentUseCase` needs `taskId`, which `createTaskUseCase` returns. No [`async`]({{ "/en/glossary/async/" | relative_url }}) is needed for a dependency chain — plain suspend calls, one after another, are already correct. The result of the whole operation is not a value but an effect: the [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) from [Room]({{ "/en/glossary/room/" | relative_url }}) emits the new task and the UI updates.

### `launch` returns a `Job`, and the `Job` is the handle

```kotlin
// From FollowApp Suite — TasksViewModel.kt
private var subtasksJob: Job? = null

subtasksJob?.cancel()
subtasksJob = viewModelScope.launch {
    getSubtasksUseCase(task.id)
        .catch { error -> Log.e(TAG, "Error loading subtasks", error) }
        .collect { subtasks -> _uiState.update { it.copy(form = it.form.copy(subtasks = subtasks)) } }
}
```

The value of [`launch`]({{ "/en/glossary/launch/" | relative_url }}) is not the coroutine's result — there is none — but its [`Job`]({{ "/en/glossary/job/" | relative_url }}). The only thing this code ever does with it is [`cancel()`]({{ "/en/glossary/cancel/" | relative_url }}). That is the whole API surface [`launch`]({{ "/en/glossary/launch/" | relative_url }}) is designed around.

### Parallel with no result: still `launch`

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Writes run in parallel; coroutineScope waits for all of them
// so emissions stay suppressed until the final state is persisted
kotlinx.coroutines.coroutineScope {
    selected.forEach { task ->
        launch {
            applyLabelAssignmentUseCase(task.id, scaleName, LabelValue.Scale(value))
        }
    }
}
```

This is N coroutines running concurrently, and it is *not* an [`async`]({{ "/en/glossary/async/" | relative_url }}) use case: nobody needs N return values. [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) already waits for every child. The [`async`]({{ "/en/glossary/async/" | relative_url }}) + [`awaitAll()`]({{ "/en/glossary/await-all/" | relative_url }}) version would be strictly more code for the same behaviour.

### Where `async` would fit — Not found in FAS

FAS never returns two independently computed values from one suspend function, so [`async`]({{ "/en/glossary/async/" | relative_url }}) does not appear in production code. The closest call site is this sequential check, which is correct today and would become an [`async`]({{ "/en/glossary/async/" | relative_url }}) candidate only if the counts were expensive:

```kotlin
// From FollowApp Suite — TasksViewModel.kt
viewModelScope.launch {
    val anyChildren = ids.any { countActiveSubtasksUseCase(it) > 0 }
    // ...
}
```

`any` short-circuits, so this runs the DAO queries one at a time and stops at the first hit. The parallel form — and the standard [`async`]({{ "/en/glossary/async/" | relative_url }}) shape the interview will ask for — is:

```kotlin
// Not found in FAS — standalone example
suspend fun anyHasChildren(ids: List<String>): Boolean = coroutineScope {
    ids.map { id -> async { countActiveSubtasksUseCase(id) > 0 } }
        .awaitAll()
        .any { it }
}
```

Trade-off stated plainly: the sequential version does *less* work when the first task has children; the parallel one has *lower latency* when most do not. Neither is "right" without measuring — and for a handful of indexed [Room]({{ "/en/glossary/room/" | relative_url }}) queries the difference is invisible.

### `Deferred` by hand: gating a coroutine in a test

[`CompletableDeferred`]({{ "/en/glossary/completable-deferred/" | relative_url }}) is a [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) with no [`async`]({{ "/en/glossary/async/" | relative_url }}) behind it. The test fixture uses it to freeze a repository read until the test decides to let it through.

```kotlin
// From FollowApp Suite — FakeLabelRepository.kt
/** When set, getLabelsWithOptions suspends until completed — lets tests observe in-flight reloads. */
var loadGate: CompletableDeferred<Unit>? = null

override fun getLabelsWithOptions(): Flow<Map<Label, List<LabelOption>>> =
    flow.map {
        loadGate?.await()
        labels.associateWith { label -> options.filter { it.labelId == label.id }.sortedBy { it.sortOrder } }
    }
```

```kotlin
// From FollowApp Suite — LabelsListViewModelTest.kt
// Block the next catalog read so the reload stays in flight
labelRepo.loadGate = CompletableDeferred()

vm.onConfirmScaleOptionRename(option.id)
advanceUntilIdle()

// While the reload is suspended, the screen must NOT show the loading state
assertFalse(vm.uiState.value.isLoading)

// Release the reload and verify it still completes with fresh data
labelRepo.loadGate!!.complete(Unit)
advanceUntilIdle()
```

[`await()`]({{ "/en/glossary/await/" | relative_url }}) suspends the [collector]({{ "/en/glossary/collector/" | relative_url }}) exactly as it would on an [`async`]({{ "/en/glossary/async/" | relative_url }}); `complete(Unit)` resumes it. The first [`advanceUntilIdle()`]({{ "/en/glossary/advance-until-idle/" | relative_url }}) runs everything *up to* the gate, which is what lets the test assert an intermediate state that would otherwise be a race.

## The Interview (The Hot Seat)

**Question**: When do you use [`launch`]({{ "/en/glossary/launch/" | relative_url }}) and when [`async`]({{ "/en/glossary/async/" | relative_url }})? What is the actual difference, given that both start a coroutine?

**Senior Answer**: They are the same machinery with one difference: what they return. [`launch`]({{ "/en/glossary/launch/" | relative_url }}) returns a [`Job`]({{ "/en/glossary/job/" | relative_url }}) — a handle to cancel or join — and its block produces no value; it is for side effects, and the callers are typically non-suspending entry points like a click handler on a ViewModel. [`async`]({{ "/en/glossary/async/" | relative_url }}) returns a [`Deferred<T>`]({{ "/en/glossary/deferred/" | relative_url }}), a [`Job`]({{ "/en/glossary/job/" | relative_url }}) that also carries a result, and [`await()`]({{ "/en/glossary/await/" | relative_url }}) suspends until that result is ready; it is for the one situation where two computations are independent and I want them to overlap — start both, then await both, inside a [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) so the function returns a plain value and the parallelism never leaks out. The rule is "do I need the value?", not "is it parallel?": N independent writes with no result are [`launch`]({{ "/en/glossary/launch/" | relative_url }}) inside [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}), which already waits for all of them, and a dependency chain is plain sequential suspend calls with no builder at all. The two smells are an [`async`]({{ "/en/glossary/async/" | relative_url }}) whose [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) is never awaited — that should have been a [`launch`]({{ "/en/glossary/launch/" | relative_url }}) — and `async { }.await()` on one line, which is just a function call with extra allocations. The place I would expect a follow-up is failure: a [`launch`]({{ "/en/glossary/launch/" | relative_url }}) failure propagates up the tree immediately; an [`async`]({{ "/en/glossary/async/" | relative_url }}) failure is *both* stored in the [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) for [`await()`]({{ "/en/glossary/await/" | relative_url }}) *and* propagated to the parent at the moment it happens. Inside a plain [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) the propagation wins — the sibling is cancelled before I can catch anything at [`await()`]({{ "/en/glossary/await/" | relative_url }}) — so per-child error handling needs [`supervisorScope`]({{ "/en/glossary/supervisor-scope/" | relative_url }}).

**Question**: You have three network calls that produce three parts of a screen. Two are independent; the third needs the result of the first. Write the shape, and tell me what happens if the second one fails.

**Senior Answer**: A suspend function returning the assembled model, with a [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) as its body. Inside it, `val a = async { fetchA() }` and `val b = async { fetchB() }` start the two independent calls concurrently; then `val c = fetchC(a.await())` — a plain sequential call, because it depends on `a`; then `Screen(a.await(), b.await(), c)`. No [`async`]({{ "/en/glossary/async/" | relative_url }}) for `c`: wrapping a dependent call in [`async`]({{ "/en/glossary/async/" | relative_url }}) and immediately awaiting it adds nothing. If `fetchB` throws, the [`async`]({{ "/en/glossary/async/" | relative_url }}) fails its parent [`Job`]({{ "/en/glossary/job/" | relative_url }}) — the [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) — immediately, which cancels `a` if it is still running and cancels the coroutine sitting in `fetchC`, and then rethrows `fetchB`'s exception out of the function once the children have finished cancelling. The caller sees one exception and no half-built screen, which for "the screen cannot render without all three" is the behaviour I want. If instead part `b` were optional — a recommendations rail that can be empty — I would switch the body to [`supervisorScope`]({{ "/en/glossary/supervisor-scope/" | relative_url }}) and wrap only `b.await()` in [`runCatching`]({{ "/en/glossary/run-catching/" | relative_url }}), so its failure stays inside its [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) and `a` and `c` complete normally. Either way the failure handling lives at [`await()`]({{ "/en/glossary/await/" | relative_url }}), not around the `async { }` block, and the choice between the two scopes is a product decision about whether the parts are one unit or independent units — the same question that decides [`Job`]({{ "/en/glossary/job/" | relative_url }}) versus [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) everywhere else.

---

[Back to Chapters]({{ "/" | relative_url }})
