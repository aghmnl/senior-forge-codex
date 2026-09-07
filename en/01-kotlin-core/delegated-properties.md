---
layout: page
title: Delegated Properties (by lazy, by viewModels)
lang: en
permalink: /en/01-kotlin-core/delegated-properties/
order: 10
---

## The Theory (The What)

A delegated property is one whose `get` (and optionally `set`) logic is handled by a separate object — the **delegate** — rather than by a [backing field]({{ "/en/glossary/backing-field/" | relative_url }}). The `by` [keyword]({{ "/en/glossary/keyword/" | relative_url }}) is the syntactic bridge: `val x by SomeDelegate()` tells the compiler to route all access through the delegate's `operator fun getValue()` (and `operator fun setValue()` for `var`).

At the [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) level, the compiler generates a hidden field that holds the delegate instance and rewrites every property access into a call to `getValue(thisRef, property)`. The `property` parameter is a [`KProperty<*>`]({{ "/en/glossary/kproperty/" | relative_url }}) that carries [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) metadata about the delegated property (name, [type]({{ "/en/glossary/type-inference/" | relative_url }}), visibility).

Kotlin's [standard library]({{ "/en/glossary/standard-library/" | relative_url }}) ships several built-in delegates:

- **`lazy`** — computes a value on first access and caches it. Covered in depth in [Lateinit vs Lazy]({{ "/en/01-kotlin-core/lateinit-vs-lazy/" | relative_url }}).
- **`observable`** — fires a callback after every assignment.
- **`vetoable`** — fires a callback before assignment and can reject the new value.
- **`notNull`** — a non-nullable `var` that throws if read before being set (similar to `lateinit` but works with [primitives]({{ "/en/glossary/primitives/" | relative_url }})).
- **Map delegation** — reads property values from a `Map<String, Any?>` using the property name as the key.

Beyond the [standard library]({{ "/en/glossary/standard-library/" | relative_url }}), the Android ecosystem heavily uses the delegation pattern:

- **`by viewModels()`** / **`by activityViewModels()`** — [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) ViewModel scoping in Fragments.
- **`by hiltViewModel()`** — [Hilt]({{ "/en/glossary/hilt/" | relative_url }})-powered ViewModel injection in [Jetpack Compose]({{ "/en/glossary/jetpack-compose/" | relative_url }}).
- **`by remember { mutableStateOf() }`** — Compose's state delegation, where the delegate is a `MutableState<T>` and the `by` [keyword]({{ "/en/glossary/keyword/" | relative_url }}) unwraps `value` automatically.
- **`by mutableStateOf()`** — the same delegation but outside [`@Composable`]({{ "/en/glossary/composable/" | relative_url }}) functions, typically in [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}) classes that hold observable state for Compose's snapshot system.
- **`by collectAsStateWithLifecycle()`** — converts a [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}) into Compose `State<T>` that respects the [lifecycle]({{ "/en/glossary/lifecycle-event/" | relative_url }}).

## The Senior Perspective (The Why)

Delegated properties are one of Kotlin's most powerful abstractions because they extract **cross-cutting property logic** into reusable, composable units.

- **The `by` Contract**: Any object that provides `operator fun getValue(thisRef: T, property:` [`KProperty<*>`]({{ "/en/glossary/kproperty/" | relative_url }})`): R` can be a read [property delegate]({{ "/en/glossary/property-delegate/" | relative_url }}); adding `operator fun setValue(thisRef: T, property:` [`KProperty<*>`]({{ "/en/glossary/kproperty/" | relative_url }})`), value: R)` makes it a read-write [property delegate]({{ "/en/glossary/property-delegate/" | relative_url }}). The convention is purely structural — no interface is required (though `ReadOnlyProperty<T, R>` and `ReadWriteProperty<T, R>` exist for [type safety]({{ "/en/glossary/type-safety/" | relative_url }})). A Senior knows that this is [operator overloading]({{ "/en/glossary/operator-overloading/" | relative_url }}) at work — the compiler resolves `by` to these specific operators at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}).
- **`provideDelegate`**: When a [property delegate]({{ "/en/glossary/property-delegate/" | relative_url }}) class defines `operator fun provideDelegate(thisRef: T, property:` [`KProperty<*>`]({{ "/en/glossary/kproperty/" | relative_url }})`): D`, the compiler calls it at property initialization time instead of using the delegate directly. This allows validation or customization before the delegate is installed — for instance, checking that the property name matches a key in a configuration map.
- **Compose State as Delegation**: When you write `var count by remember { mutableStateOf(0) }`, the [`by`]({{ "/en/glossary/by-delegation/" | relative_url }}) keyword delegates reads and writes to the `MutableState<Int>` object. Without [`by`]({{ "/en/glossary/by-delegation/" | relative_url }}), you would need to write `count.value` everywhere. This is not just [syntax sugar]({{ "/en/glossary/syntax-sugar/" | relative_url }}) — it deeply integrates with Compose's [snapshot system]({{ "/en/glossary/snapshot-system/" | relative_url }}): every write triggers recomposition of readers.
- **`by mutableStateOf()` in [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}) Classes**: Outside [`@Composable`]({{ "/en/glossary/composable/" | relative_url }}) functions, a [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}) class can hold Compose-observable state by delegating to `mutableStateOf()`. This is the pattern for complex, multi-property [state holders]({{ "/en/glossary/state-holder/" | relative_url }}) (like drag-and-drop controllers) where snapshot-backed properties must trigger recomposition without wrapping everything in `State<T>.value` calls.
- **Allocation Awareness**: Every `by lazy` creates a `Lazy<T>` delegate object on the [heap]({{ "/en/glossary/heap/" | relative_url }}). Every `by mutableStateOf()` creates a `SnapshotMutableState` object. In [hot loops]({{ "/en/glossary/hot-loops/" | relative_url }}) or tight [allocations]({{ "/en/glossary/allocations/" | relative_url }}), a Senior considers whether the delegation [overhead]({{ "/en/glossary/overhead/" | relative_url }}) is justified or whether a direct [backing field]({{ "/en/glossary/backing-field/" | relative_url }}) is more appropriate.
- **viewModels() and Scoping**: `by viewModels()` is a `Lazy`-based delegate that scopes the ViewModel to the Fragment's [`ViewModelStore`]({{ "/en/glossary/viewmodel-store/" | relative_url }}). `by activityViewModels()` scopes it to the Activity. A Senior understands that these are not just convenience — they define the **survival scope** of the ViewModel across configuration changes and [back stack]({{ "/en/glossary/back-stack/" | relative_url }}) operations. In Compose with [Hilt]({{ "/en/glossary/hilt/" | relative_url }}), `hiltViewModel()` is a `@Composable` function (not property delegation) that uses the [navigation component]({{ "/en/glossary/navigation-component/" | relative_url }}) [back stack]({{ "/en/glossary/back-stack/" | relative_url }}) entry as the scope.

## Code in Action

### Compose state delegation with `by remember { mutableStateOf() }`

The `by` keyword unwraps `MutableState<T>` so that reads and writes look like plain variables, while Compose's [snapshot system]({{ "/en/glossary/snapshot-system/" | relative_url }}) tracks every change for recomposition.

```kotlin
// From FollowApp Suite — ScaleOptionChip.kt
@Composable
fun ScaleOptionChip(
    label: String,
    availableOptions: List<String>,
    onOptionSelect: (String) -> Unit,
    onRemove: () -> Unit,
    modifier: Modifier = Modifier
) {
    var isDropdownOpen by remember { mutableStateOf(false) }
    var chipHeightPx by remember { mutableStateOf(0) }
    var chipWidthPx by remember { mutableStateOf(0) }

    Box(modifier = modifier) {
        FilterChip(
            selected = true,
            onClick = { isDropdownOpen = !isDropdownOpen },
            modifier = Modifier.onSizeChanged {
                chipHeightPx = it.height
                chipWidthPx = it.width
            },
            label = { Text(label) }
        )
    }
}
```

### `by mutableStateOf()` in a [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}) class — snapshot-backed properties without `remember`

When state needs to be observable by Compose but lives in a class (not a [`@Composable`]({{ "/en/glossary/composable/" | relative_url }}) function), `by mutableStateOf()` delegates directly to the [snapshot system]({{ "/en/glossary/snapshot-system/" | relative_url }}). Every property write triggers recomposition of any composable that reads it.

```kotlin
// From FollowApp Suite — DragToReorder.kt
@Stable
class ReorderState<K : Any> internal constructor(
    private val onMove: (fromKey: K, toKey: K) -> Boolean,
    private val onDragEnd: () -> Unit,
    private val onLongPressOnly: (K) -> Unit
) {
    var draggingKey: K? by mutableStateOf(null)
        private set

    var pointerRootY by mutableFloatStateOf(0f)
        private set

    var autoScrollDirection by mutableStateOf(0)
        private set

    internal var draggedLayoutTop by mutableFloatStateOf(Float.NaN)
        private set
}
```

### Flow-to-Compose delegation with `by collectAsStateWithLifecycle()`

Converting a [StateFlow]({{ "/en/glossary/stateflow/" | relative_url }}) into Compose `State<T>` via `by` creates a [lifecycle-aware]({{ "/en/glossary/lifecycle-aware/" | relative_url }}) subscription that pauses collection when the UI is not visible and resumes automatically.

```kotlin
// From FollowApp Suite — TasksScreen.kt
@Composable
fun TasksRoute(
    viewModel: TasksViewModel = hiltViewModel(),
    settingsViewModel: SettingsViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
    val settingsState by settingsViewModel.uiState.collectAsStateWithLifecycle()
    val isTemplatePickerVisible by viewModel.isTemplatePickerVisible
        .collectAsStateWithLifecycle()
}
```

### Custom delegate — `Delegates.observable` and `Delegates.vetoable`

[Standard library]({{ "/en/glossary/standard-library/" | relative_url }}) delegates that fire callbacks on property changes. `observable` notifies after the change; `vetoable` can reject the new value before it's stored.

```kotlin
// Not found in FAS — standalone example
class UserProfile {
    var displayName: String by Delegates.observable("Guest") { _, old, new ->
        println("Name changed from $old to $new")
    }

    var age: Int by Delegates.vetoable(0) { _, _, newValue ->
        newValue >= 0
    }
}
```

### Map delegation — reading property values from a Map

Properties can delegate to a `Map`, using the property name as the lookup key. This is useful for parsing JSON-like structures or configuration maps.

```kotlin
// Not found in FAS — standalone example
class ServerConfig(properties: Map<String, Any?>) {
    val host: String by properties
    val port: Int by properties
    val debugMode: Boolean by properties
}

val config = ServerConfig(mapOf(
    "host" to "api.followapp.com",
    "port" to 8443,
    "debugMode" to false
))
```

## The Interview (The Hot Seat)

**Question**: How does Kotlin's `by` [keyword]({{ "/en/glossary/keyword/" | relative_url }}) work under the hood, and what makes `by mutableStateOf()` in a [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}) class different from `by remember { mutableStateOf() }` in a [`@Composable`]({{ "/en/glossary/composable/" | relative_url }}) function?

**Senior Answer**: The `by` [keyword]({{ "/en/glossary/keyword/" | relative_url }}) is resolved at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) through [operator overloading]({{ "/en/glossary/operator-overloading/" | relative_url }}): the compiler looks for `operator fun getValue` (and `setValue` for `var`) on the delegate object and rewrites property access into calls to those operators. A hidden field stores the delegate instance, and a [`KProperty<*>`]({{ "/en/glossary/kproperty/" | relative_url }}) metadata object is passed on every access. For `by remember { mutableStateOf(0) }` in a [`@Composable`]({{ "/en/glossary/composable/" | relative_url }}) function, the `remember` block preserves the `MutableState` across recompositions using the Compose [slot table]({{ "/en/glossary/slot-table/" | relative_url }}) — the delegate is scoped to that composable's [composition lifetime]({{ "/en/glossary/composition-lifetime/" | relative_url }}). For `by mutableStateOf(0)` in a [`@Stable`]({{ "/en/glossary/stable/" | relative_url }}) class, there is no `remember` — the `MutableState` is a regular instance field of the class. It still participates in Compose's [snapshot system]({{ "/en/glossary/snapshot-system/" | relative_url }}) (writes trigger recomposition of readers), but its [lifetime]({{ "/en/glossary/composition-lifetime/" | relative_url }}) is tied to the class instance, not to a composition slot. This makes it suitable for [state holders]({{ "/en/glossary/state-holder/" | relative_url }}) like drag-and-drop controllers that are created once and shared across multiple composables, whereas `remember`-based state is local to one composable's position in the tree.

---

[Back to Chapters]({{ "/" | relative_url }})
