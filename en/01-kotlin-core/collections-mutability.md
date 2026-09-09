---
layout: page
title: Collections & Mutability
lang: en
permalink: /en/01-kotlin-core/collections-mutability/
order: 12
---

## The Theory (The What)

Kotlin's [collections]({{ "/en/glossary/collections/" | relative_url }}) are split into two interface hierarchies. [`List<out E>`]({{ "/en/glossary/list/" | relative_url }}), [`Set<out E>`]({{ "/en/glossary/sets/" | relative_url }}) and [`Map<K, out V>`]({{ "/en/glossary/maps/" | relative_url }}) expose only read operations. [`MutableList<E>`]({{ "/en/glossary/mutable-list/" | relative_url }}), [`MutableSet<E>`]({{ "/en/glossary/mutable-set/" | relative_url }}) and [`MutableMap<K, V>`]({{ "/en/glossary/mutable-map/" | relative_url }}) extend them with [`add`]({{ "/en/glossary/add/" | relative_url }}), [`remove`]({{ "/en/glossary/remove/" | relative_url }}), [`put`]({{ "/en/glossary/put/" | relative_url }}) and [`clear`]({{ "/en/glossary/clear/" | relative_url }}). There is no third "immutable" hierarchy in the [standard library]({{ "/en/glossary/standard-library/" | relative_url }}) — which is the single most important fact about them.

- **Read-only is not immutable.** A [`List<String>`]({{ "/en/glossary/list/" | relative_url }}) is a [read-only view]({{ "/en/glossary/read-only-view/" | relative_url }}): the *reference* forbids [mutation]({{ "/en/glossary/mutation/" | relative_url }}), the *object* behind it may still be an [`ArrayList`]({{ "/en/glossary/arraylist/" | relative_url }}) that somebody else is writing to. [`listOf()`]({{ "/en/glossary/list-of/" | relative_url }}) happens to return an unmodifiable instance; `myMutableList as List<String>` does not.
- **[Variance]({{ "/en/glossary/variance/" | relative_url }}) follows from that split.** [`List<out E>`]({{ "/en/glossary/list/" | relative_url }}) is [covariant]({{ "/en/glossary/covariance/" | relative_url }}) precisely because it cannot be written to, so `List<Task>` is a `List<Any>`. [`MutableList<E>`]({{ "/en/glossary/mutable-list/" | relative_url }}) must stay [invariant]({{ "/en/glossary/invariance/" | relative_url }}) — see [Generics, Variance & Reification]({{ "/en/01-kotlin-core/generics-variance-reification/" | relative_url }}).
- **Three families, three cost profiles.** [`List`]({{ "/en/glossary/list/" | relative_url }}) gives ordered, indexed access with `O(n)` [`contains`]({{ "/en/glossary/contains/" | relative_url }}). [`Set`]({{ "/en/glossary/sets/" | relative_url }}) gives `O(1)` membership through hashing and drops duplicates. [`Map`]({{ "/en/glossary/maps/" | relative_url }}) gives `O(1)` keyed lookup. [`setOf`]({{ "/en/glossary/set-of/" | relative_url }}) and [`mapOf`]({{ "/en/glossary/map-of/" | relative_url }}) are backed by `LinkedHashSet`/`LinkedHashMap`, so iteration order is insertion order — Kotlin quietly gives you determinism Java does not.
- **Builders and conversions.** [`toList()`]({{ "/en/glossary/to-list/" | relative_url }}), [`toSet()`]({{ "/en/glossary/to-set/" | relative_url }}) and [`toMutableList()`]({{ "/en/glossary/to-mutable-list/" | relative_url }}) produce a [defensive copy]({{ "/en/glossary/defensive-copy/" | relative_url }}). [`buildList {}`]({{ "/en/glossary/build-list/" | relative_url }}) and [`buildMap {}`]({{ "/en/glossary/build-map/" | relative_url }}) ([builder functions]({{ "/en/glossary/builder-functions/" | relative_url }})) let you mutate locally and hand back a read-only result, without exposing the mutable receiver.
- **Eager vs lazy.** Every [collection operator]({{ "/en/glossary/collection-operators/" | relative_url }}) — [`map`]({{ "/en/glossary/map-operator/" | relative_url }}), [`filter`]({{ "/en/glossary/filter/" | relative_url }}), [`groupBy`]({{ "/en/glossary/group-by/" | relative_url }}), [`sorted`]({{ "/en/glossary/sorted/" | relative_url }}) — allocates a new list per step. [Sequences]({{ "/en/glossary/sequences/" | relative_url }}) ([`asSequence()`]({{ "/en/glossary/as-sequence/" | relative_url }})) evaluate lazily, one element through the whole chain until a [terminal operation]({{ "/en/glossary/terminal-operations/" | relative_url }}) pulls it, trading [allocations]({{ "/en/glossary/allocations/" | relative_url }}) for per-element [overhead]({{ "/en/glossary/overhead/" | relative_url }}).

## The Senior Perspective (The Why)

- **Mutability is a [concurrency]({{ "/en/glossary/concurrency/" | relative_url }}) and ownership question, not a style question.** The moment a [`MutableList`]({{ "/en/glossary/mutable-list/" | relative_url }}) crosses a boundary — returned from a repository, stored in a [ViewModel]({{ "/en/glossary/viewmodel-store/" | relative_url }}) state object, captured by a [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) — two callers can write to it and neither owns it. [Immutability]({{ "/en/glossary/immutability/" | relative_url }}) is what makes state safe to share across [coroutines]({{ "/en/glossary/coroutines/" | relative_url }}) without a [synchronized block]({{ "/en/glossary/synchronized-block/" | relative_url }}); it is [thread safety]({{ "/en/glossary/thread-safety/" | relative_url }}) obtained by construction rather than by locking.
- **Mutate locally, publish immutably.** The pattern that survives review is: build with a [`MutableList`]({{ "/en/glossary/mutable-list/" | relative_url }})/[`MutableMap`]({{ "/en/glossary/mutable-map/" | relative_url }}) inside a function, return the read-only supertype. The mutation is confined to one [stack frame]({{ "/en/glossary/stack-frame/" | relative_url }}) where no other thread can observe it, and the [call site]({{ "/en/glossary/call-site/" | relative_url }}) gets something it cannot corrupt. This is the imperative core inside a [functional-style]({{ "/en/glossary/functional-style/" | relative_url }}) API, and it is usually faster than a chain of operators that allocates four intermediate lists.
- **The leaky-view trap.** `private val _items = mutableListOf<T>()` plus `val items: List<T> get() = _items` is *not* [protected state]({{ "/en/glossary/protected-state/" | relative_url }}) — it is a [backing field]({{ "/en/glossary/backing-field/" | relative_url }}) exposed through a read-only *type*. Callers cannot write through the interface, but they hold a live reference: the contents can change under them mid-iteration, and a `ConcurrentModificationException` is the friendly outcome. A [`StateFlow`]({{ "/en/glossary/stateflow/" | relative_url }}) of a genuinely new list, or a [defensive copy]({{ "/en/glossary/defensive-copy/" | relative_url }}) via [`toList()`]({{ "/en/glossary/to-list/" | relative_url }}), is the honest version.
- **[`data class`]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}) equality depends on the collection's semantics.** Two [data classes]({{ "/en/01-kotlin-core/data-classes/" | relative_url }}) holding `List<String>` are [equal]({{ "/en/glossary/equals/" | relative_url }}) only if the elements match *in order*; with `Set<String>` order is irrelevant. Getting this wrong is how a Compose screen recomposes on every emission, or fails to recompose when it should — Compose compares the previous and next state with [`equals`]({{ "/en/glossary/equals/" | relative_url }}). A mutable collection inside a state class is worse still: it is not [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}), so the [snapshot system]({{ "/en/glossary/snapshot-system/" | relative_url }}) cannot reason about it.
- **Pick the structure for the access pattern, not the declaration.** `if (id in list)` inside a [`filter`]({{ "/en/glossary/filter/" | relative_url }}) over `n` tasks is `O(n·m)`. Hoisting [`list.toSet()`]({{ "/en/glossary/to-set/" | relative_url }}) out of the loop makes it `O(n + m)`. This is the single most common performance finding in a real Android codebase, and the fix is one call.
- **[Sequences]({{ "/en/glossary/sequences/" | relative_url }}) are not a free win.** Below roughly a thousand elements the iterator machinery costs more than the intermediate lists it saves. Reach for [`asSequence()`]({{ "/en/glossary/as-sequence/" | relative_url }}) when the chain is long, the source is large, or the pipeline short-circuits on a [terminal operation]({{ "/en/glossary/terminal-operations/" | relative_url }}) (`first`, `any`, `take`) — not by default, and never when the chain ends in [`sorted`]({{ "/en/glossary/sorted/" | relative_url }}).
- **Compose has its own mutable collection.** [`mutableStateListOf()`]({{ "/en/glossary/mutable-state-list-of/" | relative_url }}) is an [observable]({{ "/en/glossary/observable-state/" | relative_url }}) [snapshot state list]({{ "/en/glossary/snapshot-state-list/" | relative_url }}): mutating it triggers recomposition of exactly the readers that touched it. It is the one place where a mutable collection in UI code is correct — as local, optimistic state, never as the source of truth.

## Code in Action

### Mutate locally, return read-only

`GetLabelReferenceCounts` builds its result with a [`MutableMap`]({{ "/en/glossary/mutable-map/" | relative_url }}) because counting requires repeated in-place updates, then returns [`Map<String, Int>`]({{ "/en/glossary/maps/" | relative_url }}). The mutable type never escapes the function.

```kotlin
// From FollowApp Suite — GetLabelReferenceCounts.kt
class GetLabelReferenceCounts @Inject constructor() {
    operator fun invoke(tasks: List<Task>, scaleName: String): Map<String, Int> {
        val refCounts = mutableMapOf<String, Int>()

        tasks.forEach { task ->
            when (val labelValue = task.customLabels[scaleName]) {
                is LabelValue.Tag -> labelValue.values.forEach { label ->
                    refCounts[label] = (refCounts[label] ?: 0) + 1
                }
                is LabelValue.Scale -> {
                    val value = labelValue.value
                    refCounts[value] = (refCounts[value] ?: 0) + 1
                }
                null -> {}
            }
        }

        return refCounts
    }
}
```

The declared [return type]({{ "/en/glossary/return-type/" | relative_url }}) is what carries the guarantee. `refCounts` *is* a `LinkedHashMap` at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) — nothing was copied — but no caller has a reference typed to allow writing, and the local reference dies with the [stack frame]({{ "/en/glossary/stack-frame/" | relative_url }}). The same shape appears in `StringListTypeConverter`, where a `mutableListOf<String>` is filled from a `JSONArray` and handed back as [`List<String>`]({{ "/en/glossary/list/" | relative_url }}):

```kotlin
// From FollowApp Suite — StringListTypeConverter.kt
@TypeConverter
fun toStringList(value: String?): List<String> {
    if (value == null) return emptyList()
    val list = mutableListOf<String>()
    val jsonArray = JSONArray(value)
    for (i in 0 until jsonArray.length()) {
        list.add(jsonArray.getString(i))
    }
    return list
}
```

### Choosing the structure for the lookup

`computeTaskGroups` splits tasks by scale option. The membership test runs once per task, so the option labels are converted to a [`Set`]({{ "/en/glossary/sets/" | relative_url }}) *before* the loop — turning an `O(n·m)` scan into `O(n)` hashed lookups.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
val assignedValues = options.toSet()
val unassigned = tasks.filter { task ->
    val value = (task.customLabels[groupBy] as? LabelValue.Scale)?.value
    value == null || value !in assignedValues
}
groups.add(TaskGroup(chipLabel = groupBy, isAssigned = false, tasks = unassigned, chipShape = Chip.Shape.Scale))
```

Note the accumulator: `val groups = mutableListOf<TaskGroup>()` inside the function, while the function's [return type]({{ "/en/glossary/return-type/" | relative_url }}) is `List<TaskGroup>`. The same rule, applied to a builder loop that an operator chain would express less clearly.

`mapTo(mutableSetOf())` is the same idea fused into one pass — it [maps]({{ "/en/glossary/map-operator/" | relative_url }}) and collects directly into the target [collection]({{ "/en/glossary/collections/" | relative_url }}), with no intermediate list:

```kotlin
// From FollowApp Suite — TasksViewModel.kt
val parentIds = if (hasSubtasksFilter != null) {
    tasks.mapNotNullTo(mutableSetOf()) { it.parentTaskId }
} else emptySet()
```

### Set algebra instead of manual mutation

Toggling a group's selection is expressed as [`Set`]({{ "/en/glossary/sets/" | relative_url }}) arithmetic. `selectedTaskIds - groupSet` and `+ groupSet` each return a **new** `Set`; nothing is mutated, so the result can be published straight into [immutable]({{ "/en/glossary/immutability/" | relative_url }}) UI state.

```kotlin
// From FollowApp Suite — BulkSelection.kt
internal fun toggleGroupSelection(
    selectedTaskIds: Set<String>,
    groupTaskIds: List<String>
): Set<String> {
    val groupSet = groupTaskIds.toSet()
    return if (groupSet.all { it in selectedTaskIds }) {
        selectedTaskIds - groupSet
    } else {
        selectedTaskIds + groupSet
    }
}
```

This is why the UI state object declares `val selectedTaskIds: Set<String> = emptySet()` rather than a [`MutableSet`]({{ "/en/glossary/mutable-set/" | relative_url }}): every transition produces a new value, so [equality]({{ "/en/glossary/equals/" | relative_url }}) comparison is meaningful and [Unidirectional Data Flow]({{ "/en/glossary/unidirectional-data-flow/" | relative_url }}) holds.

### The one place a mutable collection belongs in the UI

Drag-to-reorder needs the list to move *during* the gesture, before the [ViewModel]({{ "/en/glossary/viewmodel-store/" | relative_url }}) has confirmed anything. That is a [snapshot state list]({{ "/en/glossary/snapshot-state-list/" | relative_url }}): mutating it is observed by [Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}) and recomposes the list immediately.

```kotlin
// From FollowApp Suite — TasksScreen.kt
// Local optimistic copy: drag moves mutate this list synchronously
// (no ViewModel round-trip per move, which caused visible jumps);
// the ViewModel is notified once on drop.
val localTasks = remember { mutableStateListOf<Task>() }
LaunchedEffect(uiState.activeTasks) {
    val localIds = localTasks.map { it.id }
    val remoteIds = uiState.activeTasks.map { it.id }
    if (localIds != remoteIds) {
        localTasks.clear()
        localTasks.addAll(uiState.activeTasks)
    } else {
        uiState.activeTasks.forEachIndexed { i, task ->
            if (localTasks[i] != task) localTasks[i] = task
        }
    }
}
```

Two details make this correct rather than a leak. The mutable list is *derived* — it is re-synchronised from `uiState.activeTasks`, which stays the source of truth — and it never leaves the composable. On drop, the result is published as an ordinary read-only [`List<String>`]({{ "/en/glossary/list/" | relative_url }}): `onDragEnd = { onReorderComplete(localTasks.map { it.id }) }`.

For cross-group moves the code takes an explicit [defensive copy]({{ "/en/glossary/defensive-copy/" | relative_url }}) before mutating, because the group's `tasks` is a read-only [`List`]({{ "/en/glossary/list/" | relative_url }}) owned by the state object:

```kotlin
// From FollowApp Suite — TasksScreen.kt
val source = localGroups[originIdx].tasks.toMutableList()
val target = localGroups[targetIdx].tasks.toMutableList()
```

### The leak this all prevents

```kotlin
// Not found in FAS — standalone example
class TaskCache {
    private val _tasks = mutableListOf<Task>()
    val tasks: List<Task> get() = _tasks   // read-only *type*, live *object*
}

val snapshot = cache.tasks       // caller believes this is a stable value
for (t in snapshot) { /* another thread calls cache.add(...) */ }
// -> ConcurrentModificationException, or silently stale rendering

// Honest version: hand back a copy the caller owns.
val tasks: List<Task> get() = _tasks.toList()
```

[`toList()`]({{ "/en/glossary/to-list/" | relative_url }}) costs one array copy. A `ConcurrentModificationException` in production costs considerably more.

## The Interview (The Hot Seat)

**Question**: In Kotlin, is [`List`]({{ "/en/glossary/list/" | relative_url }}) immutable?

**Senior Answer**: No — `List` is *read-only*, which is a property of the interface, not of the object. `List<out E>` simply omits the mutating methods, so a reference typed `List` cannot [add]({{ "/en/glossary/add/" | relative_url }}) or [remove]({{ "/en/glossary/remove/" | relative_url }}). The instance behind it can still be an [`ArrayList`]({{ "/en/glossary/arraylist/" | relative_url }}) that someone else holds as a [`MutableList`]({{ "/en/glossary/mutable-list/" | relative_url }}) and writes to; [`listOf()`]({{ "/en/glossary/list-of/" | relative_url }}) returns an unmodifiable instance, but an upcast `MutableList` does not. The practical consequence is the classic [backing field]({{ "/en/glossary/backing-field/" | relative_url }}) leak: exposing `val items: List<T> get() = _items` over a private `MutableList` gives callers a live [view]({{ "/en/glossary/read-only-view/" | relative_url }}) that can change mid-iteration — a `ConcurrentModificationException`, or a Compose screen comparing a list to itself and skipping recomposition because the reference never changed. Real [immutability]({{ "/en/glossary/immutability/" | relative_url }}) requires either a [defensive copy]({{ "/en/glossary/defensive-copy/" | relative_url }}) ([`toList()`]({{ "/en/glossary/to-list/" | relative_url }})) at the boundary, or a [persistent collection]({{ "/en/glossary/persistent-collections/" | relative_url }}) from `kotlinx.collections.immutable`. The rule I apply is: mutate locally inside a function, publish the read-only supertype — and if the value escapes into shared state, copy it.

**Question**: A screen filters ten thousand tasks and, for each one, checks whether its id is in a list of selected ids. It janks. What do you change?

**Senior Answer**: First the data structure, then maybe the evaluation strategy. `id in selectedList` is a linear scan, so the [filter]({{ "/en/glossary/filter/" | relative_url }}) is `O(n·m)`; hoisting [`selectedList.toSet()`]({{ "/en/glossary/to-set/" | relative_url }}) out of the loop makes each membership test an `O(1)` hash lookup and the whole pass `O(n + m)` — one line, and it is almost always the entire fix. Only after that would I look at the operator chain: each of [`map`]({{ "/en/glossary/map-operator/" | relative_url }})/`filter`/[`sortedBy`]({{ "/en/glossary/sorted/" | relative_url }}) allocates a full intermediate list, so a four-step chain over ten thousand items allocates forty thousand entries and gives the [Garbage Collector]({{ "/en/glossary/garbage-collector/" | relative_url }}) work on the main thread. Switching to [`asSequence()`]({{ "/en/glossary/as-sequence/" | relative_url }}) evaluates one element through the whole chain and short-circuits on [terminal operations]({{ "/en/glossary/terminal-operations/" | relative_url }}) like `first` or `any`; if the pipeline ends in [`sorted`]({{ "/en/glossary/sorted/" | relative_url }}) it buys nothing, since sorting is inherently eager. And I would check where the work runs at all — filtering ten thousand rows belongs in the [ViewModel]({{ "/en/glossary/viewmodel-store/" | relative_url }}) off the main thread, cached against its inputs, not recomputed inside a composable on every recomposition.

---

[Back to Chapters]({{ "/" | relative_url }})
