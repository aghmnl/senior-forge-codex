---
layout: page
title: Immutability & Atomic State for UI
lang: en
permalink: /en/01-kotlin-core/immutability-atomic-state/
order: 13
---

## The Theory (The What)

[Immutability]({{ "/en/glossary/immutability/" | relative_url }}) means a value never changes after construction; to "change" it you produce a new value. **Atomic state** means each of those transitions is published as one indivisible step, so no observer ever sees a half-applied change. In an Android [state holder]({{ "/en/glossary/state-holder/" | relative_url }}), the two are one mechanism: an immutable state class plus an atomic publish operation.

- **The state class is a value, not an object.** A [`data class`]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}) where every property is a `val` of a read-only type has [value semantics]({{ "/en/glossary/value-semantics/" | relative_url }}): its identity *is* its contents. That is what makes [`equals`]({{ "/en/glossary/equals/" | relative_url }}) meaningful, and [`equals`]({{ "/en/glossary/equals/" | relative_url }}) is what [Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) and [`StateFlow`]({{ "/en/glossary/stateflow/" | relative_url }}) both build on.
- **[`copy`]({{ "/en/glossary/copy/" | relative_url }}) is how transitions are expressed.** It allocates one small object and reuses every unchanged reference — [structural sharing]({{ "/en/glossary/structural-sharing/" | relative_url }}) — so a thirty-field state class costs a few hundred bytes per transition, independent of how large the lists inside it are.
- **`value =` is not [atomic]({{ "/en/glossary/atomicity/" | relative_url }}) when the new value depends on the old.** `_uiState.value = _uiState.value.copy(...)` is read, compute, write: three steps another writer can interleave with. The result is a lost update — a [race condition]({{ "/en/glossary/race-condition/" | relative_url }}) that never crashes, it just silently discards one of the user's actions.
- **[`update {}`]({{ "/en/glossary/update/" | relative_url }}) closes the gap.** It is a [compare-and-set]({{ "/en/glossary/compare-and-set/" | relative_url }}) retry loop: read the current value, run the lambda, publish only if the value has not changed, otherwise recompute from the fresh one. Lock-free, and the whole read-modify-write becomes one indivisible transition.
- **CAS compares references, so immutability is the precondition.** If the state object could be mutated in place, its identity would survive the change and the compare would succeed on stale data. [Immutability]({{ "/en/glossary/immutability/" | relative_url }}) is not decoration around `update` — it is what makes `update` correct.
- **The write end must be private.** `private val _uiState = MutableStateFlow(...)` plus `val uiState = _uiState.`[`asStateFlow()`]({{ "/en/glossary/as-state-flow/" | relative_url }}) is the pair: one writer, many readers, and a [read-only view]({{ "/en/glossary/read-only-view/" | relative_url }}) that cannot be cast back.
- **[`StateFlow`]({{ "/en/glossary/stateflow/" | relative_url }}) is [conflated]({{ "/en/glossary/conflation/" | relative_url }}) and deduplicated.** It holds exactly one value, drops intermediate ones for a slow collector, and emits nothing at all when the new value is [equal]({{ "/en/glossary/equals/" | relative_url }}) to the current one. That is correct for state and wrong for one-shot events.

## The Senior Perspective (The Why)

- **"It all runs on the main thread" is the assumption that produces the bug.** It does not: `viewModelScope.launch(Dispatchers.IO)`, `flowOn`, a repository callback and a `collect` on a background dispatcher all write state off-Main. And even on `Main.immediate`, a `suspend` call between the read and the write is a suspension point where another coroutine takes over. `update` is not defensive programming for an exotic case; it is the ordinary case.
- **The lambda passed to [`update`]({{ "/en/glossary/update/" | relative_url }}) must be pure.** It can run several times because of the CAS retry, so logging, analytics, navigation and repository calls inside it will fire twice under contention. This is the single most common review finding once a team adopts `update` — the fix is to compute the next state inside and do side effects after.
- **Read the old value *inside* the block, never outside.** `val current = _uiState.value; _uiState.update { it.copy(x = current.x + 1) }` reintroduces exactly the race `update` exists to remove. Once the transition is expressed as a pure function of `it`, the atomicity is structural rather than a matter of discipline.
- **Mutability inside the state class defeats everything above in one line.** `val tasks: MutableList<Task>` is a `val` with reference semantics: two state objects alias one buffer, [`equals`]({{ "/en/glossary/equals/" | relative_url }}) reports "unchanged" while the contents differ, CAS cannot detect the change, and the class is not [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}) so [Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) recomposes it defensively on every parent pass. The failure is silent in both directions — a screen that does not update, or one that updates constantly.
- **Derive rather than store.** [Derived state]({{ "/en/glossary/derived-state/" | relative_url }}) — a property with a getter and no [backing field]({{ "/en/glossary/backing-field/" | relative_url }}) — cannot desynchronise from its source, which makes the inconsistent combination unrepresentable. Storing both `selectedTaskIds` and `isSelectionMode` creates a synchronisation obligation at every [`copy`]({{ "/en/glossary/copy/" | relative_url }}) site; deriving one from the other removes the obligation and the bug class with it. This is [Single Source of Truth]({{ "/en/glossary/single-source-of-truth/" | relative_url }}) applied inside a single class.
- **One state object beats five flows.** Five separate `MutableStateFlow`s can be updated independently, which means they can be observed in a combination that is not a real state — loading `true` with results already present, selection mode active with an empty selection. A single immutable state object makes every transition all-or-nothing and gives the screen exactly one thing to render.
- **Conflation makes `StateFlow` wrong for events.** "The current filter set" only needs its latest value; "show this snackbar" needs to happen once per occurrence. Modelling a one-shot event as a state field means it gets swallowed on a slow frame, or replayed after a configuration change — the toast that fires again on rotation is this bug.
- **Immutability is how you get [thread safety]({{ "/en/glossary/thread-safety/" | relative_url }}) without a [synchronized block]({{ "/en/glossary/synchronized-block/" | relative_url }}).** A value nobody can write needs no lock to be shared across [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}). The only genuinely shared mutable cell left is the `MutableStateFlow` reference itself, and that one cell is protected by CAS. That is the whole concurrency design of a modern [ViewModel]({{ "/en/glossary/viewmodel-store/" | relative_url }}).

## Code in Action

### The pair that defines the boundary

```kotlin
// From FollowApp Suite — TasksViewModel.kt
private val _uiState = MutableStateFlow(TasksUiState())
val uiState: StateFlow<TasksUiState> = _uiState.asStateFlow()
```

One private writer, one public [read-only view]({{ "/en/glossary/read-only-view/" | relative_url }}). [`asStateFlow()`]({{ "/en/glossary/as-state-flow/" | relative_url }}) returns a genuinely different object rather than the same instance under a narrower type, so a caller cannot [cast]({{ "/en/glossary/cast/" | relative_url }}) back to `MutableStateFlow` and emit. That is the "uni" in [Unidirectional Data Flow]({{ "/en/glossary/unidirectional-data-flow/" | relative_url }}).

### The state class: every property a `val`

```kotlin
// From FollowApp Suite — TasksUiState.kt
data class TasksUiState(
    val isLoading: Boolean = true,
    val activeTasks: List<Task> = emptyList(),
    val form: TaskFormState = TaskFormState(),
    val labelFilters: Map<String, LabelFilterState> = emptyMap(),
    val collapsedGroupsByPreset: Map<String, Set<String>> = emptyMap(),
    val selectedTaskIds: Set<String> = emptySet(),
    // ...
) {
    val isSelectionMode: Boolean get() = selectedTaskIds.isNotEmpty()
    val selectedTasks: List<Task> get() = activeTasks.filter { it.id in selectedTaskIds }
}
```

Note the two properties in the body. They are [derived state]({{ "/en/glossary/derived-state/" | relative_url }}): computed on read, invisible to the generated [`equals`]({{ "/en/glossary/equals/" | relative_url }}) and [`copy`]({{ "/en/glossary/copy/" | relative_url }}) (which only cover primary-constructor properties), and therefore incapable of drifting out of sync. `isSelectionMode = true` with an empty selection is not a state this class can express.

Note also `Map<String, Set<String>>` for `collapsedGroupsByPreset` — a read-only map of read-only sets. The immutability holds all the way down, which is what the guarantee actually requires.

### The transition: `update`, not `value =`

```kotlin
// From FollowApp Suite — TasksViewModel.kt
fun onTaskSelectionToggled(taskId: String) {
    _uiState.update {
        val updated = if (taskId in it.selectedTaskIds) {
            it.selectedTaskIds - taskId
        } else {
            it.selectedTaskIds + taskId
        }
        it.copy(selectedTaskIds = updated)
    }
}

fun onSelectAll() {
    _uiState.update { state ->
        val allIds = state.activeTasks.mapTo(mutableSetOf()) { it.id }
        val allSelected = state.selectedTaskIds.containsAll(allIds)
        state.copy(selectedTaskIds = if (allSelected) emptySet() else allIds)
    }
}
```

Both are read-modify-write, and both do the reading through the lambda's `it`/`state` parameter rather than through `_uiState.value`. If two of these run concurrently, the [compare-and-set]({{ "/en/glossary/compare-and-set/" | relative_url }}) loop makes the loser recompute against the winner's result instead of overwriting it. Note the [`Set`]({{ "/en/glossary/sets/" | relative_url }}) arithmetic: `- taskId` and `+ taskId` each return a new set, so the transition is a pure function and the retry is free of side effects. `mapTo(mutableSetOf())` builds locally and is published as a read-only [`Set`]({{ "/en/glossary/sets/" | relative_url }}) — mutate locally, publish immutably, as in [Collections & Mutability]({{ "/en/01-kotlin-core/collections-mutability/" | relative_url }}).

### Atomicity across a multi-field transition

```kotlin
// From FollowApp Suite — TasksViewModel.kt
_uiState.update {
    it.copy(
        sortOrder = snapshot.sortOrder,
        groupBy = snapshot.groupBy,
        doneFilter = snapshot.doneFilter,
        labelFilters = snapshot.labelFilters,
        scaleFilters = snapshot.scaleFilters,
        chipsExpanded = snapshot.chipsExpanded,
        collapsedGroupsByPreset = snapshot.collapsedGroupsByPreset
    )
}
```

Seven properties restored from disk in one publish. This runs on `Dispatchers.IO` — the comment in the source says so explicitly, and adds that "`MutableStateFlow` updates are already thread-safe". With seven separate flows, or seven `value =` assignments, the UI could observe a state with the restored sort order but the previous filters. Here the screen sees the old state or the new one, never a blend.

### Nested state without losing atomicity

```kotlin
// From FollowApp Suite — TasksViewModel.kt
_uiState.update { it.copy(form = it.form.copy(title = title)) }
_uiState.update { it.copy(form = it.form.copy(labelSearchResults = results)) }
```

`TaskFormState` is itself an immutable [`data class`]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}), so a nested change is a nested [`copy`]({{ "/en/glossary/copy/" | relative_url }}). The crucial detail is that `it.form` is read **inside** the block. Hoisting it out — `val form = _uiState.value.form` — would restore the race for the nested object while the outer `update` looks perfectly safe.

### Reading state once, then transitioning

```kotlin
// From FollowApp Suite — TasksViewModel.kt
fun onFormConfirmed() {
    val state = _uiState.value
    val title = state.form.title.trim()
    if (state.editingTaskId == null && title.isNotBlank()) {
        val duplicate = state.activeTasks.any { it.title.equals(title, ignoreCase = true) }
        if (duplicate) {
            _uiState.update { it.copy(toastMessageRes = R.string.error_duplicate_task) }
            return
        }
    }
    // ...
}
```

This is the legitimate use of `.value`: taking one consistent snapshot to *read* from — validation, deriving the payload for a repository call — while every *write* still goes through [`update`]({{ "/en/glossary/update/" | relative_url }}). The value read is an immutable object, so it cannot change while the function inspects it, and the write does not depend on it.

### Deduplication with a narrow projection

```kotlin
// From FollowApp Suite — TasksViewModel.kt
data class PersistKey(
    val sortOrder: ListSort,
    val groupBy: String?,
    val doneFilter: LabelFilterState?,
    val labelFilters: Map<String, LabelFilterState>,
    val scaleFilters: Map<String, ScaleFilterState>,
    val chipsExpanded: Boolean,
    val collapsedGroupsByPreset: Map<String, Set<String>>
)

_uiState
    .map { s -> PersistKey(s.sortOrder, s.groupBy, s.doneFilter, s.labelFilters,
                           s.scaleFilters, s.chipsExpanded, s.collapsedGroupsByPreset) }
    .distinctUntilChanged()
    .drop(1)
    .debounce(200L)
    .collect { key -> /* write to preferences */ }
```

`TasksUiState` changes on every keystroke; only seven of its properties are worth persisting. Projecting to an immutable `PersistKey` and applying [`distinctUntilChanged`]({{ "/en/glossary/distinct-until-changed/" | relative_url }}) turns "the state changed" into "something persistable changed" — and it works *only* because `PersistKey` has [value semantics]({{ "/en/glossary/value-semantics/" | relative_url }}). A mutable map in there and the operator would compare equal while the contents differ, silently swallowing the write.

### The bug this all prevents

```kotlin
// Not found in FAS — standalone example
// Two coroutines toggling different filters at the same time.
fun onFilterToggled(filter: String) {
    // Thread A reads {}, computes {dueToday}
    // Thread B reads {}, computes {starred}
    // A writes {dueToday}; B writes {starred}. A's filter is gone.
    _uiState.value = _uiState.value.copy(filters = _uiState.value.filters + filter)
}

// Atomic version: B's lambda re-runs against A's published result.
fun onFilterToggled(filter: String) {
    _uiState.update { it.copy(filters = it.filters + filter) }
}
```

No crash, no log, no stack trace — just a filter that "sometimes doesn't stick", unreproducible on the reviewer's fast device.

## The Interview (The Hot Seat)

**Question**: `_uiState.value = _uiState.value.copy(isLoading = false)` — what is wrong with this line?

**Senior Answer**: It is a read-modify-write treated as if it were one step. `MutableStateFlow.value` is `@Volatile`-backed, so the individual get and the individual set are each [atomic]({{ "/en/glossary/atomicity/" | relative_url }}) and visible across threads — which is exactly why the line reads safe. But between the read and the write another writer can publish, and this line will then [copy]({{ "/en/glossary/copy/" | relative_url }}) from a stale value and overwrite that update. It is a lost-update [race condition]({{ "/en/glossary/race-condition/" | relative_url }}), and it does not crash: the screen renders a plausible state that simply omits one of the user's actions, so it gets reported as "sometimes my filter doesn't stick" and never reproduces on a fast device. The objection I expect is "but it's all on the main thread" — it isn't. `viewModelScope.launch(Dispatchers.IO)`, `flowOn`, a repository callback, a `collect` on a background dispatcher all write from elsewhere, and even on `Main.immediate` a `suspend` call between the read and the write is a suspension point where another coroutine interleaves. The fix is [`update {}`]({{ "/en/glossary/update/" | relative_url }}), which is a [compare-and-set]({{ "/en/glossary/compare-and-set/" | relative_url }}) retry loop: it publishes only if the value it read is still current, and otherwise recomputes against the fresh one. Two caveats come with it — the lambda can run more than once, so it must be pure with no logging or navigation inside; and the old value must be read through the lambda parameter, not from `_uiState.value` outside the block, or the race comes straight back. The rule I apply is mechanical: if the new value mentions the old value, use `update`; a plain `value =` is fine only for an unconditional publish like resetting to a fresh state object.

**Question**: Why does atomic state require the state class to be immutable? Isn't `update` enough on its own?

**Senior Answer**: No, because [compare-and-set]({{ "/en/glossary/compare-and-set/" | relative_url }}) compares *references*, not contents. If the state object can be mutated in place, its identity survives the mutation: `update` reads the object, someone edits that same object's contents, the CAS compares the reference to itself, succeeds, and publishes a value computed from data that has already changed. The guard silently does nothing. The same identity problem breaks everything downstream — [`StateFlow`]({{ "/en/glossary/stateflow/" | relative_url }}) deduplicates on [`equals`]({{ "/en/glossary/equals/" | relative_url }}), so mutating a list inside the state and re-emitting the same instance emits nothing and the screen never updates; [Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) skips [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}) on the same comparison, and a `data class` holding a `MutableList` is not [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}), so it recomposes defensively on every parent pass instead. Both failure modes are silent and opposite. And `val` on the property is only half the job — the property's *type* has to be read-only all the way down, which is why a state class declares `Set<String>` and `Map<String, Set<String>>` rather than their mutable counterparts. The upside is that immutability is what buys the concurrency safety in the first place: a value nobody can write needs no [synchronized block]({{ "/en/glossary/synchronized-block/" | relative_url }}) to be shared across [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}), so the only shared mutable cell in the whole [ViewModel]({{ "/en/glossary/viewmodel-store/" | relative_url }}) is the `MutableStateFlow` reference — and that one is protected by CAS. The cost objection ("copying on every keystroke") is answered by [structural sharing]({{ "/en/glossary/structural-sharing/" | relative_url }}): [`copy`]({{ "/en/glossary/copy/" | relative_url }}) allocates one small object holding references to the unchanged parts, not a deep copy of the lists.

---

[Back to Chapters]({{ "/" | relative_url }})
