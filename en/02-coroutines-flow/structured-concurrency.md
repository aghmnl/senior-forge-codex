---
layout: page
title: "Structured Concurrency"
lang: en
permalink: /en/02-coroutines-flow/structured-concurrency/
order: 3
---

## The Theory (The What)

Structured concurrency is the rule that **every [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) has a parent, and a parent does not complete until all of its children have completed**. A coroutine is never a loose [thread]({{ "/en/glossary/thread/" | relative_url }}) you start and forget: it is a node in a tree whose root is a [`CoroutineScope`]({{ "/en/glossary/coroutine-scope/" | relative_url }}), and the tree is what the [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) uses to propagate three things — **completion, cancellation and failure**.

The tree is made of [`Job`]({{ "/en/glossary/job/" | relative_url }})s. When you call [`launch`]({{ "/en/glossary/launch/" | relative_url }}) or [`async`]({{ "/en/glossary/async/" | relative_url }}) on a scope, the new coroutine's [`Job`]({{ "/en/glossary/job/" | relative_url }}) is attached as a child of the [`Job`]({{ "/en/glossary/job/" | relative_url }}) found in the scope's [`CoroutineContext`]({{ "/en/glossary/coroutine-context/" | relative_url }}). From that link follow the four guarantees:

- **Waiting**: a parent [`Job`]({{ "/en/glossary/job/" | relative_url }}) stays in the *Completing* state until every child is done. [`coroutineScope { }`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) and [`supervisorScope { }`]({{ "/en/glossary/supervisor-scope/" | relative_url }}) make this visible: the [suspend function]({{ "/en/glossary/suspend-functions/" | relative_url }}) does not return until the block *and everything launched inside it* has finished.
- **Cancellation flows down**: cancelling a parent cancels all of its children, recursively. Cancelling [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) in [`onCleared()`]({{ "/en/glossary/on-cleared/" | relative_url }}) cancels every [collector]({{ "/en/glossary/collector/" | relative_url }}) and every one-shot write the ViewModel ever launched.
- **Failure flows up**: with a regular [`Job`]({{ "/en/glossary/job/" | relative_url }}), an uncaught exception in a child cancels the parent, which in turn cancels the *siblings*, and then the exception propagates further up. With a [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) — or inside [`supervisorScope { }`]({{ "/en/glossary/supervisor-scope/" | relative_url }}) — the failure stops at the child: siblings survive and the exception goes to a [`CoroutineExceptionHandler`]({{ "/en/glossary/coroutine-exception-handler/" | relative_url }}) instead.
- **No leaks**: because nothing can outlive its parent, work cannot silently keep running after the screen, ViewModel or request that started it is gone.

Two builders let you create a *sub-tree* inside sequential suspend code. [`coroutineScope { }`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) creates a child scope, runs the block, suspends until every child completes, and rethrows the first failure after cancelling the rest. [`supervisorScope { }`]({{ "/en/glossary/supervisor-scope/" | relative_url }}) is the same but with supervisor semantics: a failing child does not cancel its siblings. Neither creates a new [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}) or [thread]({{ "/en/glossary/thread/" | relative_url }}) — they inherit the context and only add a new [`Job`]({{ "/en/glossary/job/" | relative_url }}) node.

[`async`]({{ "/en/glossary/async/" | relative_url }}) is [`launch`]({{ "/en/glossary/launch/" | relative_url }}) with a result: it returns a [`Deferred<T>`]({{ "/en/glossary/deferred/" | relative_url }}) whose [`await()`]({{ "/en/glossary/await/" | relative_url }}) suspends until the value is ready. An exception inside [`async`]({{ "/en/glossary/async/" | relative_url }}) is stored in the [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}) and rethrown at [`await()`]({{ "/en/glossary/await/" | relative_url }}) — but it *also* fails the parent [`Job`]({{ "/en/glossary/job/" | relative_url }}) immediately, unless that parent is a supervisor.

Cancellation is [cooperative]({{ "/en/glossary/cooperative-cancellation/" | relative_url }}). Cancelling a [`Job`]({{ "/en/glossary/job/" | relative_url }}) sets a flag; the coroutine actually stops at its next [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}), where the [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) throws a [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}). Every `kotlinx.coroutines` suspend function checks the flag; a CPU loop with no suspension does not, and must call [`ensureActive()`]({{ "/en/glossary/ensure-active/" | relative_url }}) or check [`isActive`]({{ "/en/glossary/is-active/" | relative_url }}) itself. [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) is the one exception that structured concurrency treats as *normal completion*: it does not fail the parent and does not reach a [`CoroutineExceptionHandler`]({{ "/en/glossary/coroutine-exception-handler/" | relative_url }}).

## The Senior Perspective (The Why)

- **The tree is the contract that makes cancellation free.** Before structured concurrency, cancelling an operation meant threading a flag through every [callback]({{ "/en/glossary/callbacks/" | relative_url }}) and hoping every layer honoured it. With the [`Job`]({{ "/en/glossary/job/" | relative_url }}) tree, one `cancel()` at the root reaches every leaf, including coroutines launched three layers down in a repository you did not write. This is why [`GlobalScope`]({{ "/en/glossary/global-scope/" | relative_url }}) and unowned `CoroutineScope(...)` are a smell: they detach a sub-tree from every root that could cancel it, and any [memory leak]({{ "/en/glossary/memory-leaks/" | relative_url }}) they cause is invisible until production.
- **[`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) turns "fire N writes" into "fire N writes *and wait for all of them*".** Looping [`launch`]({{ "/en/glossary/launch/" | relative_url }}) directly on [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) starts N independent children and the calling function returns immediately. Wrapping the same loop in [`coroutineScope { }`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) makes the enclosing coroutine *suspend* until the last write lands. That single word is the difference between "I can run a [`finally`]({{ "/en/glossary/finally/" | relative_url }}) block after the batch" and "I have no idea when the batch is done".
- **Choose [`Job`]({{ "/en/glossary/job/" | relative_url }}) vs [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) by asking whether the children are one unit of work or independent units.** Fetching a screen's header, list and footer in parallel is one unit: if any part fails, the screen cannot render, so a plain [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) that cancels the siblings is right. A [`@Singleton`]({{ "/en/glossary/singleton-scope/" | relative_url }}) that runs a billing listener and a consent listener owns independent units: one dying must not take the other down, so it needs a [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}). [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) is a supervisor because each [`launch`]({{ "/en/glossary/launch/" | relative_url }}) from a UI event is independent of the others.
- **A `Job?` field is a hand-rolled scope, and it needs the same discipline.** Keeping `subtasksJob: Job?` to cancel a previous [collector]({{ "/en/glossary/collector/" | relative_url }}) before starting a new one is the correct tool for "only one of these at a time". The discipline is that *every* path that ends the owning state — dismiss, confirm, switch item — must cancel it, or the old [collector]({{ "/en/glossary/collector/" | relative_url }}) keeps writing stale data into state. The [`Job`]({{ "/en/glossary/job/" | relative_url }}) is still a child of [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}), so the worst case is a wasted [collector]({{ "/en/glossary/collector/" | relative_url }}) until [`onCleared()`]({{ "/en/glossary/on-cleared/" | relative_url }}), not a leak.
- **Swallowing [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) breaks the tree.** `catch (e: Exception)` around a suspend call catches [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) too. If you log it and continue, the coroutine is cancelled but keeps running, its parent waits for it, and the screen it belongs to cannot finish tearing down. The rule: rethrow it — `if (e is CancellationException) throw e` — or catch narrower types. The rare legitimate case for catching it is when the exception did *not* come from your own [`Job`]({{ "/en/glossary/job/" | relative_url }}) being cancelled, and then [`isActive`]({{ "/en/glossary/is-active/" | relative_url }}) is the check that tells the two apart.
- **[`async`]({{ "/en/glossary/async/" | relative_url }}) is for values, [`launch`]({{ "/en/glossary/launch/" | relative_url }}) is for effects — and the failure semantics differ.** A [`launch`]({{ "/en/glossary/launch/" | relative_url }}) failure is handled by the tree or the [`CoroutineExceptionHandler`]({{ "/en/glossary/coroutine-exception-handler/" | relative_url }}). An [`async`]({{ "/en/glossary/async/" | relative_url }}) failure is *also* stored in the [`Deferred`]({{ "/en/glossary/deferred/" | relative_url }}), so a `try/catch` around [`await()`]({{ "/en/glossary/await/" | relative_url }}) inside a plain [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) is not enough: the parent has already been cancelled by the time you catch. If you want to catch one [`async`]({{ "/en/glossary/async/" | relative_url }})'s failure and keep the others, the parent must be [`supervisorScope`]({{ "/en/glossary/supervisor-scope/" | relative_url }}).
- **Structured concurrency is what makes coroutines testable.** [`runTest`]({{ "/en/glossary/run-test/" | relative_url }}) is a [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}): it fails the test if a child is still running when the block ends, which is exactly the leaked-coroutine bug the tree is designed to expose. A test that needs [`advanceUntilIdle()`]({{ "/en/glossary/advance-until-idle/" | relative_url }}) and still hangs is telling you something is launched on a scope that [`runTest`]({{ "/en/glossary/run-test/" | relative_url }}) does not own.

## Code in Action

### `coroutineScope` — parallel writes that the caller waits for

Bulk-completing tasks runs one write per task in parallel. The enclosing coroutine needs to know when *all* of them are done so it can lift the `isBulkWriteInFlight` flag that suppresses intermediate emissions. [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) is what makes the [`finally`]({{ "/en/glossary/finally/" | relative_url }}) meaningful.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
updateSelectedTasksOptimistically { it.copy(isCompleted = isCompleted) }
isBulkWriteInFlight = true
try {
    kotlinx.coroutines.coroutineScope {
        ids.forEach { launch { quickCompleteTaskUseCase(taskId = it, isCompleted = isCompleted) } }
    }
} finally {
    isBulkWriteInFlight = false
}
```

Without the [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) wrapper, the `forEach` would launch N children directly on [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) and fall through to [`finally`]({{ "/en/glossary/finally/" | relative_url }}) immediately — the flag would drop while writes were still in flight. With it, the block suspends until the last [`launch`]({{ "/en/glossary/launch/" | relative_url }}) completes. If one write throws, the sibling writes are cancelled and the exception propagates out of the `try`, and [`finally`]({{ "/en/glossary/finally/" | relative_url }}) still runs: the flag is reset on every path.

The same shape appears twice more in the file, with the reasoning spelled out in the comment:

```kotlin
// From FollowApp Suite — TasksViewModel.kt
viewModelScope.launch {
    isBulkWriteInFlight = true
    try {
        // Writes run in parallel; coroutineScope waits for all of them
        // so emissions stay suppressed until the final state is persisted
        kotlinx.coroutines.coroutineScope {
            selected.forEach { task ->
                launch {
                    // ... compute updated tags for this task
                    if (updated.isEmpty()) {
                        removeLabelAssignmentUseCase(task.id, "labels")
                    } else {
                        applyLabelAssignmentUseCase(task.id, "labels", LabelValue.Tag(updated))
                    }
                }
            }
        }
    } finally {
        isBulkWriteInFlight = false
    }
}
```

### Where the wrapper is missing — and what changes

The confirmed-bulk-action path launches the same kind of writes *without* a [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}):

```kotlin
// From FollowApp Suite — TasksViewModel.kt
viewModelScope.launch {
    when (action) {
        is BulkAction.Complete -> {
            ids.forEach { launch { quickCompleteTaskUseCase(taskId = it, isCompleted = action.isCompleted, cascade = true) } }
        }
        is BulkAction.Archive -> {
            ids.forEach { launch { archiveTaskUseCase(it, cascade = true) } }
            onExitSelection()
        }
        is BulkAction.Delete -> {
            executeBulkDelete()
        }
    }
}
```

This is still structured: each inner [`launch`]({{ "/en/glossary/launch/" | relative_url }}) is a child of the outer one, which is a child of [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}). The outer coroutine will not complete until the children do, and clearing the ViewModel cancels all of them. What is *different* is that `onExitSelection()` runs before the archives have landed — the code after the loop does not wait. Here that is intentional: exiting selection mode should not wait for the database. The point is that [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) is not "the correct way"; it is the way to say *wait here*, and omitting it says *don't*.

### A `Job?` field for "one collector at a time"

Editing a task streams its direct children into the form. Only one such stream may exist, so the previous one is cancelled before the next starts — and on every path that closes the form.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Streams the direct children of the task being edited into the form.
// Cancelled whenever the form closes or switches task.
private var subtasksJob: Job? = null

fun startEditing(task: Task) {
    // ...
    subtasksJob?.cancel()
    subtasksJob = viewModelScope.launch {
        getSubtasksUseCase(task.id)
            .catch { error -> Log.e(TAG, "Error loading subtasks", error) }
            .collect { subtasks ->
                _uiState.update { it.copy(form = it.form.copy(subtasks = subtasks)) }
            }
    }
}

fun onFormDismissed() {
    subtasksJob?.cancel()
    subtasksJob = null
    // ...
}
```

`cancel()` on the [`Job`]({{ "/en/glossary/job/" | relative_url }}) cancels only that sub-tree: the [`collect`]({{ "/en/glossary/collect/" | relative_url }}) stops at its next [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}), the Room [`Flow`]({{ "/en/glossary/flow/" | relative_url }}) underneath unregisters its observer, and nothing else in [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) is affected. Note that `.catch` never sees the [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) — the [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) routes cancellation around it, so the log line is only for real errors.

### Rethrowing `CancellationException` — with a twist

Auto-scroll during drag-to-reorder runs inside a [`LaunchedEffect`]({{ "/en/glossary/launched-effect/" | relative_url }}), whose coroutine is a child of the composition. [`scrollBy`]({{ "/en/glossary/scroll-by/" | relative_url }}) can be cancelled by *another* scroll mutation on the same list, which throws a [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) even though the effect itself is still alive.

```kotlin
// From FollowApp Suite — TasksScreen.kt
LaunchedEffect(reorderState.autoScrollDirection) {
    val direction = reorderState.autoScrollDirection
    while (direction != 0) {
        if (direction > 0 && !lazyListState.canScrollForward) break
        if (direction < 0 && !lazyListState.canScrollBackward) break
        try {
            lazyListState.scrollBy(direction * autoScrollStep)
        } catch (e: CancellationException) {
            // Preempted by another scroll mutation (e.g. the
            // reorder re-anchor); keep scrolling unless the
            // effect itself was cancelled
            if (!isActive) throw e
        }
        reorderState.onAutoScrolled()
        withFrameNanos { }
    }
}
```

This is the one legitimate shape for catching [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}): the code distinguishes *"my [`Job`]({{ "/en/glossary/job/" | relative_url }}) was cancelled"* (`isActive == false` → rethrow, so the tree completes) from *"an inner operation was preempted"* (`isActive == true` → carry on). Swallowing it unconditionally would leave a cancelled coroutine looping until the next `withFrameNanos` happened to check the flag.

### The root of the tree: a scope that is never cancelled

```kotlin
// From FollowApp Suite — PremiumRepositoryImpl.kt
private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

init {
    scope.launch {
        billingConnector.isOwned
            .filterNotNull()
            .collect { owned -> premiumPreferences.setAdsRemoved(owned) }
    }
}
```

Every tree needs a root, and a [`@Singleton`]({{ "/en/glossary/singleton-scope/" | relative_url }}) is a legitimate one: its lifetime *is* the process. The [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) is the structured-concurrency decision here — the repository may grow a second [collector]({{ "/en/glossary/collector/" | relative_url }}), and the two are independent units of work.

### `async` — Not found in FAS

FAS never needs to *return* two values computed in parallel, so [`async`]({{ "/en/glossary/async/" | relative_url }}) does not appear. The canonical shape, and the failure semantics the interview will ask about:

```kotlin
// Not found in FAS — standalone example
suspend fun loadDashboard(): Dashboard = coroutineScope {
    val header = async { api.header() }
    val items = async { api.items() }
    Dashboard(header.await(), items.await())   // either failure cancels the other and rethrows
}

suspend fun loadDashboardLenient(): Dashboard = supervisorScope {
    val header = async { api.header() }
    val items = async { api.items() }
    Dashboard(
        header = runCatching { header.await() }.getOrNull(),   // one failing part does not cancel the other
        items = runCatching { items.await() }.getOrDefault(emptyList())
    )
}
```

In the first version a `try/catch` around `header.await()` would be useless: by the time [`await()`]({{ "/en/glossary/await/" | relative_url }}) rethrows, the [`async`]({{ "/en/glossary/async/" | relative_url }}) has already failed the [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) and `items` is cancelled. Only [`supervisorScope`]({{ "/en/glossary/supervisor-scope/" | relative_url }}) makes per-child recovery possible.

## The Interview (The Hot Seat)

**Question**: What is structured concurrency, and what concrete guarantees does it give you that a bare thread or [`GlobalScope.launch`]({{ "/en/glossary/global-scope/" | relative_url }}) does not?

**Senior Answer**: Structured concurrency is the rule that every [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) is a child of a [`Job`]({{ "/en/glossary/job/" | relative_url }}) in the scope that launched it, so all coroutines form a tree rooted in a [`CoroutineScope`]({{ "/en/glossary/coroutine-scope/" | relative_url }}). The tree gives four guarantees. A parent does not complete until its children complete — so [`coroutineScope { }`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) around a loop of [`launch`]({{ "/en/glossary/launch/" | relative_url }}) means "wait for all of them", and a [`finally`]({{ "/en/glossary/finally/" | relative_url }}) after it runs when the batch is really done. Cancellation propagates down — one `cancel()` on [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) reaches every [collector]({{ "/en/glossary/collector/" | relative_url }}), including ones launched by code I do not own. Failure propagates up — a child throwing cancels its parent and siblings under a plain [`Job`]({{ "/en/glossary/job/" | relative_url }}), or is isolated to that child under a [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) or [`supervisorScope`]({{ "/en/glossary/supervisor-scope/" | relative_url }}). And nothing can outlive its parent, which is what prevents leaks. [`GlobalScope.launch`]({{ "/en/glossary/global-scope/" | relative_url }}) and a bare [`Thread`]({{ "/en/glossary/thread/" | relative_url }}) give none of this: they detach the work from any root that could cancel or wait for it, an exception in them is invisible to the caller, and a test cannot know when they are finished. The trade-off I would mention is that cancellation is [cooperative]({{ "/en/glossary/cooperative-cancellation/" | relative_url }}): it only takes effect at a [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}), so a pure CPU loop must check [`isActive`]({{ "/en/glossary/is-active/" | relative_url }}) or call [`ensureActive()`]({{ "/en/glossary/ensure-active/" | relative_url }}), and catching [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}) without rethrowing it silently breaks the tree — the coroutine keeps running while its parent waits for it.

**Question**: You need to run N database writes in parallel and then update a flag when all of them have finished. Show me the shape, and tell me what happens if one write throws.

**Senior Answer**: Inside a coroutine on [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}), I set the flag, then wrap the loop in [`coroutineScope { ids.forEach { launch { write(it) } } }`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) inside a `try`, and reset the flag in [`finally`]({{ "/en/glossary/finally/" | relative_url }}). [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) creates a child [`Job`]({{ "/en/glossary/job/" | relative_url }}) that each [`launch`]({{ "/en/glossary/launch/" | relative_url }}) attaches to, and it suspends until every child completes — so the line after it, and the [`finally`]({{ "/en/glossary/finally/" | relative_url }}), run only when the last write has landed. Without the wrapper, the [`launch`]({{ "/en/glossary/launch/" | relative_url }}) calls attach directly to [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }}) and the `forEach` returns immediately: the flag would reset while writes were still in flight. If one write throws, [`coroutineScope`]({{ "/en/glossary/coroutine-scope-builder/" | relative_url }}) cancels the remaining siblings, waits for them to finish cancelling, and rethrows the original exception out of the block — the [`finally`]({{ "/en/glossary/finally/" | relative_url }}) still runs, so the flag is consistent, and the exception then propagates to the outer [`launch`]({{ "/en/glossary/launch/" | relative_url }}), where [`viewModelScope`]({{ "/en/glossary/viewmodel-scope/" | relative_url }})'s [`SupervisorJob`]({{ "/en/glossary/supervisor-job/" | relative_url }}) keeps it from cancelling the ViewModel's other coroutines but, with no [`CoroutineExceptionHandler`]({{ "/en/glossary/coroutine-exception-handler/" | relative_url }}), it crashes the app. If the requirement were instead "write as many as you can, report the failures", I would switch to [`supervisorScope`]({{ "/en/glossary/supervisor-scope/" | relative_url }}) so one failure does not cancel the others, and collect results with [`async`]({{ "/en/glossary/async/" | relative_url }}) plus `runCatching { await() }` per child. The one thing I would never do is `catch (e: Exception)` inside the child without rethrowing [`CancellationException`]({{ "/en/glossary/cancellation-exception/" | relative_url }}), because then cancelling the ViewModel would no longer stop the batch.

---

[Back to Chapters]({{ "/" | relative_url }})
