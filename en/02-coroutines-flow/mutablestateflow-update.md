---
layout: page
title: "MutableStateFlow.update {}"
lang: en
permalink: /en/02-coroutines-flow/mutablestateflow-update/
order: 12
---

## The Theory (The What)

A [`MutableStateFlow`]({{ "/en/glossary/mutable-state-flow/" | relative_url }}) can be changed in two ways. Assigning `value` **overwrites** the state with a new value. Most changes, though, are **read-modify-write**: take the current state, derive a new one from it, and store it. Written as `_uiState.value = _uiState.value.copy(isLoading = false)`, that is two separate operations, a read and then a write. If another [thread]({{ "/en/glossary/thread/" | relative_url }}) writes in between, the second write is computed from a stale value and **silently erases** the other one. That is a [race condition]({{ "/en/glossary/race-condition/" | relative_url }}), and the lost change never produces an error.

[`update {}`]({{ "/en/glossary/update/" | relative_url }}) makes the read-modify-write **[atomic]({{ "/en/glossary/atomicity/" | relative_url }})**. It is an extension on [`MutableStateFlow`]({{ "/en/glossary/mutable-state-flow/" | relative_url }}), and its implementation fits in a few lines:

```kotlin
// kotlinx.coroutines — MutableStateFlow.update
inline fun <T> MutableStateFlow<T>.update(function: (T) -> T) {
    while (true) {
        val prevValue = value
        val nextValue = function(prevValue)
        if (compareAndSet(prevValue, nextValue)) return
    }
}
```

It reads the current value, computes the next one with your [lambda]({{ "/en/glossary/lambdas/" | relative_url }}), and then calls [`compareAndSet`]({{ "/en/glossary/compare-and-set/" | relative_url }}): "store `nextValue` only if the state is still `prevValue`". If another writer got in first, the comparison fails and the loop **tries again** with the fresh value. There is no [lock]({{ "/en/glossary/lock/" | relative_url }}): nobody waits, the loser just recomputes. This technique is called [compare-and-set]({{ "/en/glossary/compare-and-set/" | relative_url }}).

There are two variants for when the caller needs a value back:

- **[`getAndUpdate { }`]({{ "/en/glossary/get-and-update/" | relative_url }})** applies the change and returns the value **before** it.
- **[`updateAndGet { }`]({{ "/en/glossary/update-and-get/" | relative_url }})** applies the change and returns the value **after** it.

## The Senior Perspective (The Why)

- **The race needs real parallelism.** `value = value.copy(...)` has no [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}) between the read and the write, so on a single [thread]({{ "/en/glossary/thread/" | relative_url }}) (the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}), or a test inside [`runTest`]({{ "/en/glossary/run-test/" | relative_url }})) nothing can get in between. It breaks when writers run on **several [threads]({{ "/en/glossary/thread/" | relative_url }})**, for example a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) on [`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) updating state while the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) also does. The bug is rare, timing-dependent and impossible to reproduce on demand: the worst kind to debug. [`update {}`]({{ "/en/glossary/update/" | relative_url }}) removes it by construction, and it costs nothing when there is no contention.
- **It is the default because it survives refactors.** A [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) that only writes from the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) is safe today with plain assignment. The day someone moves one of those writes to [`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}), the code is still correct if every read-modify-write already goes through [`update {}`]({{ "/en/glossary/update/" | relative_url }}). The rule "every change derived from the current state uses [`update`]({{ "/en/glossary/update/" | relative_url }})" is easy to review; "this is safe because all writers happen to share a [thread]({{ "/en/glossary/thread/" | relative_url }})" is not.
- **The [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) can run more than once, so it must be [pure]({{ "/en/glossary/pure-function/" | relative_url }}).** Under contention [`update`]({{ "/en/glossary/update/" | relative_url }}) calls the function again with the new value. A log line, an analytics event, a network call or a counter increment inside the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) can happen twice. The [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) should only compute the next state from [`it`]({{ "/en/glossary/it/" | relative_url }}); side effects go before or after.
- **Only what is computed from [`it`]({{ "/en/glossary/it/" | relative_url }}) is protected.** [`update {}`]({{ "/en/glossary/update/" | relative_url }}) guarantees [atomicity]({{ "/en/glossary/atomicity/" | relative_url }}) for the [lambda]({{ "/en/glossary/lambdas/" | relative_url }})'s input and output, nothing else. Reading `_uiState.value.items` outside, computing a new list, and then writing `update { it.copy(items = newList) }` looks [atomic]({{ "/en/glossary/atomicity/" | relative_url }}) but is not: `newList` was derived from a snapshot that may be stale by the time the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) runs. Anything that depends on the current state has to be derived inside the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}), from [`it`]({{ "/en/glossary/it/" | relative_url }}).
- **Keep it short.** A long computation inside [`update`]({{ "/en/glossary/update/" | relative_url }}) widens the window in which another writer can win, and every retry repeats it. Slow work (a [query]({{ "/en/glossary/query/" | relative_url }}), a sort over thousands of items) that does not depend on the current state belongs outside, with only the final combine happening inside.
- **Plain assignment is still correct for a pure overwrite.** When the new value does not depend on the old one (`_isLoading.value = true`, `_query.value = ""`), there is nothing to read, so there is nothing to race: `value =` is clear and correct. [`update`]({{ "/en/glossary/update/" | relative_url }}) is for derivation, not for every write.

## Code in Action

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// The case update {} exists for: this coroutine writes from Dispatchers.IO
// while the main thread keeps updating the same _uiState
private fun restoreViewPreferences() {
    viewModelScope.launch(Dispatchers.IO) {
        val snapshot = runCatching { tasksViewPreferences.read() }.getOrNull()
        if (snapshot != null) {
            _uiState.update {
                it.copy(
                    sortOrder = snapshot.sortOrder,
                    groupBy = snapshot.groupBy,
                    // ...
                )
            }
        }
        _restored.value = true   // pure overwrite: plain assignment is fine
    }
}

// From FollowApp Suite — TasksViewModel.kt
// The update only protects what is computed from `it`. Here `reordered` is
// derived from a snapshot read OUTSIDE the lambda, so the write is not
// atomic with respect to that read. It is safe only because every writer
// of activeTasks runs on the main thread.
fun onReorderComplete(orderedIds: List<String>) {
    val tasksById = _uiState.value.activeTasks.associateBy { it.id }
    val reordered = orderedIds.mapNotNull { tasksById[it] }
    if (reordered.size == _uiState.value.activeTasks.size) {
        _uiState.update { it.copy(activeTasks = reordered) }
    }
    // ...
}

// Not found in FAS — standalone example
// The same change derived entirely inside the lambda: atomic end to end
_uiState.update { state ->
    val byId = state.activeTasks.associateBy { it.id }
    val reordered = orderedIds.mapNotNull { byId[it] }
    if (reordered.size == state.activeTasks.size) state.copy(activeTasks = reordered) else state
}

// From FollowApp Suite — LabelsListViewModel.kt
// value++ is a read-modify-write too: read value, add one, write it back.
// Safe here because resync() only runs on the main thread.
private fun resync() {
    _resyncTrigger.value++
}

// Not found in FAS — standalone example
// The atomic version, correct from any thread
private fun resync() {
    _resyncTrigger.update { it + 1 }
}

// Not found in FAS — standalone example
// The lambda may run again under contention: side effects stay outside
_uiState.update { it.copy(isSaving = true) }
analytics.log("save_started")   // once, after the state change
```

## The Interview (The Hot Seat)

**Question**: Why write `_uiState.update { it.copy(isLoading = false) }` instead of `_uiState.value = _uiState.value.copy(isLoading = false)`? Is the second one ever a real problem?

**Senior Answer**: The second form is a read-modify-write split into two operations: it reads the current state, builds a copy, and writes it back. If another [thread]({{ "/en/glossary/thread/" | relative_url }}) writes the state between that read and that write, the copy is built from a stale value and the other [thread]({{ "/en/glossary/thread/" | relative_url }})'s change is silently overwritten. It is a [race condition]({{ "/en/glossary/race-condition/" | relative_url }}) that produces no error, just a lost update. [`update {}`]({{ "/en/glossary/update/" | relative_url }}) closes that gap with [compare-and-set]({{ "/en/glossary/compare-and-set/" | relative_url }}): it reads the value, computes the new one, and only stores it if the state is still the one it read; otherwise it retries with the fresh value. Whether the second form is a real problem depends on threading. With no [suspension point]({{ "/en/glossary/suspension-point/" | relative_url }}) between the read and the write, a single [thread]({{ "/en/glossary/thread/" | relative_url }}) cannot interleave, so if every writer runs on the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) it happens to be safe. It becomes a real bug as soon as writers run in parallel, for example a [coroutine]({{ "/en/glossary/coroutines/" | relative_url }}) on [`Dispatchers.IO`]({{ "/en/glossary/dispatchers-io/" | relative_url }}) updating state while the [main thread]({{ "/en/glossary/main-thread/" | relative_url }}) does too, and then it is intermittent and nearly impossible to reproduce. That is why I use [`update`]({{ "/en/glossary/update/" | relative_url }}) for every change derived from the current state: it is correct regardless of threading, it costs nothing without contention, and it stays correct when someone later moves a write to another [dispatcher]({{ "/en/glossary/dispatcher/" | relative_url }}). For a pure overwrite that does not depend on the old value, plain assignment is fine.

**Question**: In a code review you see `_uiState.update { analytics.log("state_changed"); it.copy(count = it.count + 1) }`. What would you flag?

**Senior Answer**: Two things. The first is the side effect inside the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}). [`update`]({{ "/en/glossary/update/" | relative_url }}) is a [compare-and-set]({{ "/en/glossary/compare-and-set/" | relative_url }}) loop: when another writer changes the state first, [`compareAndSet`]({{ "/en/glossary/compare-and-set/" | relative_url }}) fails and the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) runs again with the new value. Under contention, that analytics event is logged twice, or more, for a single logical change. The [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) has to be a [pure function]({{ "/en/glossary/pure-function/" | relative_url }}) from the current state to the next one, so the log goes after the [`update`]({{ "/en/glossary/update/" | relative_url }}) call, where it runs exactly once. The second is a subtler rule that this particular line gets right, but which is worth checking in the rest of the change: only what is computed from [`it`]({{ "/en/glossary/it/" | relative_url }}) is [atomic]({{ "/en/glossary/atomicity/" | relative_url }}). Here `count + 1` is derived from [`it`]({{ "/en/glossary/it/" | relative_url }}), so the increment is safe. If the code had read `_uiState.value.count` outside the [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) and written `update { it.copy(count = savedCount + 1) }`, the [atomicity]({{ "/en/glossary/atomicity/" | relative_url }}) would be gone, because the input was taken from a snapshot that may already be stale. So my rule for review is: inside [`update`]({{ "/en/glossary/update/" | relative_url }}), derive everything from [`it`]({{ "/en/glossary/it/" | relative_url }}), keep it short, and keep side effects out.

---

[Back to Chapters]({{ "/" | relative_url }})
