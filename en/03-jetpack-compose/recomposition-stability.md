---
layout: page
title: "Recomposition & Stability"
lang: en
permalink: /en/03-jetpack-compose/recomposition-stability/
order: 1
---

## The Theory (The What)

In [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}), the UI is the result of calling [`@Composable`]({{ "/en/glossary/composable/" | relative_url }}) functions. The first time they run, Compose builds the **[composition]({{ "/en/glossary/composition/" | relative_url }})**: a tree that records what each function emitted and which state it read. When some of that state changes, Compose does not rebuild the whole screen. It runs again **only the composables that read the state that changed**. That re-execution is **[recomposition]({{ "/en/glossary/recomposition/" | relative_url }})**.

Two mechanisms keep [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}) small:

- **Precise invalidation.** Compose tracks state reads through the [snapshot system]({{ "/en/glossary/snapshot-system/" | relative_url }}). When a [`MutableState`]({{ "/en/glossary/mutable-state/" | relative_url }}) changes, only the scopes that read it are scheduled to recompose, not their parents or siblings.
- **[Skipping]({{ "/en/glossary/skipping/" | relative_url }}).** When a composable recomposes, it calls its children again. For each child, Compose compares the new arguments with the ones from the previous call. If all of them are equal, the child is **skipped**: its body does not run, and the previous result is reused.

[Skipping]({{ "/en/glossary/skipping/" | relative_url }}) is where **[stability]({{ "/en/glossary/stability/" | relative_url }})** comes in. Compose can only trust that comparison if the parameter types are **[stable]({{ "/en/glossary/stability/" | relative_url }})**. A type is [stable]({{ "/en/glossary/stability/" | relative_url }}) when:

1. [`equals`]({{ "/en/glossary/equals/" | relative_url }}) always gives the same result for the same two instances, and
2. if a public property can change, the change notifies the [composition]({{ "/en/glossary/composition/" | relative_url }}) (it is backed by [`MutableState`]({{ "/en/glossary/mutable-state/" | relative_url }})), and
3. all its public properties are [stable]({{ "/en/glossary/stability/" | relative_url }}) too.

[Primitives]({{ "/en/glossary/primitives/" | relative_url }}), [`String`]({{ "/en/glossary/string/" | relative_url }}), function types ([lambdas]({{ "/en/glossary/lambdas/" | relative_url }})) and [`MutableState`]({{ "/en/glossary/mutable-state/" | relative_url }}) are [stable]({{ "/en/glossary/stability/" | relative_url }}). So is a class whose properties are all [`val`]({{ "/en/glossary/val/" | relative_url }})s of [stable]({{ "/en/glossary/stability/" | relative_url }}) types, such as most data classes. Types are **[unstable]({{ "/en/glossary/stability/" | relative_url }})** when Compose cannot prove those rules: a class with a [`var`]({{ "/en/glossary/var/" | relative_url }}) property, a class from a module compiled without the Compose compiler, and, notably, [`List`]({{ "/en/glossary/list/" | relative_url }}), [`Set`]({{ "/en/glossary/sets/" | relative_url }}) and [`Map`]({{ "/en/glossary/maps/" | relative_url }}). These are interfaces, and the instance behind a [`List`]({{ "/en/glossary/list/" | relative_url }}) could be a [`MutableList`]({{ "/en/glossary/mutable-list/" | relative_url }}) that changes without telling anyone.

Since [Kotlin]({{ "/en/glossary/kotlin/" | relative_url }}) 2.0.20, **[strong skipping]({{ "/en/glossary/strong-skipping/" | relative_url }})** is enabled by default and changes the rule for [unstable]({{ "/en/glossary/stability/" | relative_url }}) parameters. Instead of making the composable impossible to skip, Compose compares them by **instance** ([`===`]({{ "/en/glossary/referential-equality/" | relative_url }})), and [stable]({{ "/en/glossary/stability/" | relative_url }}) ones by [`equals`]({{ "/en/glossary/equals/" | relative_url }}). It also remembers [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}) automatically, so passing a [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) no longer breaks [skipping]({{ "/en/glossary/skipping/" | relative_url }}). [Unstable]({{ "/en/glossary/stability/" | relative_url }}) types are no longer a blocker; they are compared more strictly.

Compose may also run composables in any order, skip them, run them many times, or cancel and discard a [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}). That is why the body of a composable must be **free of side effects**: it describes the UI, it does not do work.

## The Senior Perspective (The Why)

- **Recomposing is normal; recomposing too much is the problem.** A composable that recomposes because its data changed is working as designed. The bugs are composables that recompose when nothing they show changed, or that recompose on every frame. Before optimizing, measure: the [Layout Inspector]({{ "/en/glossary/layout-inspector/" | relative_url }}) shows [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}) and skip counts per composable, and the [Compose compiler reports]({{ "/en/glossary/compose-compiler-reports/" | relative_url }}) [list]({{ "/en/glossary/list/" | relative_url }}) which functions are skippable and which parameters are [unstable]({{ "/en/glossary/stability/" | relative_url }}).
- **With [strong skipping]({{ "/en/glossary/strong-skipping/" | relative_url }}), identity matters more than [stability]({{ "/en/glossary/stability/" | relative_url }}).** An [unstable]({{ "/en/glossary/stability/" | relative_url }}) [`List`]({{ "/en/glossary/list/" | relative_url }}) parameter is now compared with [`===`]({{ "/en/glossary/referential-equality/" | relative_url }}). If the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) updates its state with [`copy`]({{ "/en/glossary/copy/" | relative_url }}) and leaves the [list]({{ "/en/glossary/list/" | relative_url }}) untouched, the instance is the same and the child is skipped. But a [list]({{ "/en/glossary/list/" | relative_url }}) created **during [composition]({{ "/en/glossary/composition/" | relative_url }})** (`tasks.filter { ... }` in the body of a composable) is a new instance on every [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}), so the child that receives it never skips. The fix is to compute it outside [composition]({{ "/en/glossary/composition/" | relative_url }}), in the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}), or to [`remember`]({{ "/en/glossary/remember/" | relative_url }}) it with its inputs as keys.
- **Read state as late as possible.** Every state read decides which scope recomposes. Reading a fast-changing value (a scroll [offset]({{ "/en/glossary/modifier-offset/" | relative_url }}), an animation) high in the tree recomposes everything below it. Passing a [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) instead of the value (`{ offset }`), or reading it inside a [lambda]({{ "/en/glossary/lambdas/" | relative_url }})-based modifier ([`Modifier.offset { }`]({{ "/en/glossary/modifier-offset/" | relative_url }}), `drawBehind { }`), moves the read to the layout or draw phase, and [composition]({{ "/en/glossary/composition/" | relative_url }}) does not run at all.
- **[`derivedStateOf`]({{ "/en/glossary/derived-state/" | relative_url }}) when the output changes less often than the input.** A scroll position changes on every pixel, but "show the back-to-top button" changes twice. [`derivedStateOf`]({{ "/en/glossary/derived-state/" | relative_url }}) recomposes only when the derived result changes.
- **[`@Immutable`]({{ "/en/glossary/immutable-annotation/" | relative_url }}) and [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}) are promises, not checks.** They tell the compiler to treat a type as [stable]({{ "/en/glossary/stability/" | relative_url }}), but nothing verifies it. Annotating a class with mutable internals makes Compose skip when it should not, and the UI shows stale data. Prefer real [immutability]({{ "/en/glossary/immutability/" | relative_url }}): [`val`]({{ "/en/glossary/val/" | relative_url }}) properties, immutable collections, or a [stability]({{ "/en/glossary/stability/" | relative_url }}) configuration file for types from other modules that you know are immutable.
- **Side effects in a composable body are bugs.** Logging, analytics, writing to a [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) or launching work directly in the body runs an unpredictable number of times. Effects belong in [`LaunchedEffect`]({{ "/en/glossary/launched-effect/" | relative_url }}), [`SideEffect`]({{ "/en/glossary/side-effect/" | relative_url }}) or [`DisposableEffect`]({{ "/en/glossary/disposable-effect/" | relative_url }}), and event callbacks.

## Code in Action

```kotlin
// From FollowApp Suite — DragToReorder.kt
// A state holder that Compose cannot prove stable on its own (it is a regular
// class with private mutable fields), annotated @Stable as a promise: every
// value the UI reads is backed by snapshot state, so changes notify the
// composition, and the same instance is reused across recompositions.
@Stable
class ReorderState<K : Any> internal constructor(
    private val onMove: (fromKey: K, toKey: K) -> Boolean,
    private val onDragEnd: () -> Unit,
    private val onLongPressOnly: (K) -> Unit
) {
    /** Key currently being dragged, or null. Observable from composition. */
    var draggingKey: K? by mutableStateOf(null)
        private set

    var pointerRootY by mutableFloatStateOf(0f)
        private set
    // ...
}

// From FollowApp Suite — TaskFormSheet.kt
// offsetPx changes on every frame of the drag gesture, but these values only
// matter when their result changes: derivedStateOf limits recomposition to that.
val scrimAlpha by remember {
    derivedStateOf { ((1f - offsetPx.value / maxOffsetPx) * 0.5f).coerceIn(0f, 0.5f) }
}
val isFullscreen by remember {
    derivedStateOf { offsetPx.value < maxOffsetPx * 0.5f }
}

// From FollowApp Suite — TasksUiState.kt
// List and Map are unstable types. FAS uses Kotlin 2.0.21, so strong skipping
// is on: they are compared by instance. Updating the state with copy() keeps the
// same list instance when the tasks did not change, so children can still skip.
data class TasksUiState(
    val isLoading: Boolean = true,
    val activeTasks: List<Task> = emptyList(),
    val searchQuery: String = "",
    val labelFilters: Map<String, LabelFilterState> = emptyMap(),
    // ...
)

// Not found in FAS — standalone example
// The identity trap: filter creates a new list on every recomposition of
// TaskScreen (for example, on every keystroke in the search field), so
// TaskList never skips. remember with the right keys keeps the same instance.
@Composable
fun TaskScreen(state: TasksUiState, onQueryChange: (String) -> Unit) {
    SearchField(state.searchQuery, onQueryChange)
    // TaskList(state.activeTasks.filter { !it.isCompleted })      // always recomposes
    val pending = remember(state.activeTasks) { state.activeTasks.filter { !it.isCompleted } }
    TaskList(pending)                                              // skipped while tasks are unchanged
}
```

## The Interview (The Hot Seat)

**Question**: What is [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}) in [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}), and what decides whether a composable is skipped?

**Senior Answer**: [Recomposition]({{ "/en/glossary/recomposition/" | relative_url }}) is Compose running a composable again because state it read has changed. Compose tracks every state read through the [snapshot system]({{ "/en/glossary/snapshot-system/" | relative_url }}), so when a [`MutableState`]({{ "/en/glossary/mutable-state/" | relative_url }}) changes, only the scopes that read it are invalidated, not the whole screen. When a scope recomposes, it calls its children again, and for each child Compose compares the new arguments with the previous ones: if they are all equal, the child is skipped and its previous output is reused. That comparison depends on [stability]({{ "/en/glossary/stability/" | relative_url }}). A [stable]({{ "/en/glossary/stability/" | relative_url }}) type guarantees that [`equals`]({{ "/en/glossary/equals/" | relative_url }}) is reliable and that any change to it notifies the [composition]({{ "/en/glossary/composition/" | relative_url }}), which is true for [primitives]({{ "/en/glossary/primitives/" | relative_url }}), strings, [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}), [`MutableState`]({{ "/en/glossary/mutable-state/" | relative_url }}) and immutable data classes. Interfaces like [`List`]({{ "/en/glossary/list/" | relative_url }}) are [unstable]({{ "/en/glossary/stability/" | relative_url }}) because the instance could be mutable. Before [Kotlin]({{ "/en/glossary/kotlin/" | relative_url }}) 2.0.20, a single [unstable]({{ "/en/glossary/stability/" | relative_url }}) parameter made the composable non-skippable. With [strong skipping]({{ "/en/glossary/strong-skipping/" | relative_url }}), which is now the default, [unstable]({{ "/en/glossary/stability/" | relative_url }}) parameters are compared by instance and [lambdas]({{ "/en/glossary/lambdas/" | relative_url }}) are remembered automatically, so the practical rule became: pass the same instance when nothing changed. And because Compose can rerun, reorder or cancel composables, their bodies must be free of side effects.

**Question**: A [list]({{ "/en/glossary/list/" | relative_url }}) of tasks recomposes on every keystroke in a search field, even though the tasks did not change. How do you diagnose it and fix it?

**Senior Answer**: First I confirm it, with the [Layout Inspector]({{ "/en/glossary/layout-inspector/" | relative_url }})'s [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}) counts, to see which composable recomposes and whether its children are skipped or not. Then I check what the [list]({{ "/en/glossary/list/" | relative_url }}) receives. The typical cause is that a parameter is a new instance on every [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}): the parent reads the search query, so it recomposes on every keystroke, and if it builds the [list]({{ "/en/glossary/list/" | relative_url }}) during [composition]({{ "/en/glossary/composition/" | relative_url }}), with a [`filter`]({{ "/en/glossary/filter/" | relative_url }}) or [`map`]({{ "/en/glossary/map-operator/" | relative_url }}) in its body, each [recomposition]({{ "/en/glossary/recomposition/" | relative_url }}) creates a new [`List`]({{ "/en/glossary/list/" | relative_url }}). With [strong skipping]({{ "/en/glossary/strong-skipping/" | relative_url }}), an [unstable]({{ "/en/glossary/stability/" | relative_url }}) [`List`]({{ "/en/glossary/list/" | relative_url }}) is compared by identity, so a new instance means the child never skips, even if the content is identical. The fix is to stop creating it in [composition]({{ "/en/glossary/composition/" | relative_url }}): either compute it in the [ViewModel]({{ "/en/glossary/viewmodel/" | relative_url }}) and expose it in the state, so it only changes when the tasks change, or [`remember`]({{ "/en/glossary/remember/" | relative_url }}) it with the tasks as the key. Other causes I check are a type Compose considers [unstable]({{ "/en/glossary/stability/" | relative_url }}) that I compare by value (where an immutable collection or a [stability]({{ "/en/glossary/stability/" | relative_url }}) configuration helps), and a state read placed too high, which I move down into the composable that actually needs it, or defer with a [lambda]({{ "/en/glossary/lambdas/" | relative_url }}).

---

[Back to Chapters]({{ "/" | relative_url }})
