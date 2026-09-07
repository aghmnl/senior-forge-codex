---
layout: page
title: Generics, Variance & Reification
lang: en
permalink: /en/01-kotlin-core/generics-variance-reification/
order: 11
---

## The Theory (The What)

Generics let a class or function work with many types while keeping [type safety]({{ "/en/glossary/type-safety/" | relative_url }}). Instead of writing one `List` per element type, you declare [generic type parameters]({{ "/en/glossary/generic-type-parameters/" | relative_url }}) — `List<T>` — and the compiler checks every [call site]({{ "/en/glossary/call-site/" | relative_url }}).

On the [JVM]({{ "/en/glossary/jvm/" | relative_url }}) this guarantee is a [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) one only. Because of [Type Erasure]({{ "/en/glossary/type-erasure/" | relative_url }}), the generic argument is stripped from the [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}): at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) a `List<String>` and a `List<Task>` are the same class. Three [keywords]({{ "/en/glossary/keyword/" | relative_url }}) shape how you work inside that constraint:

- **[Invariance]({{ "/en/glossary/invariance/" | relative_url }}) (default)** — `Box<String>` is *not* a subtype of `Box<Any>`, and not a supertype either. This is the safe default: the type is both produced and consumed, so neither direction of substitution is sound.
- **[Covariance]({{ "/en/glossary/covariance/" | relative_url }}) (`out T`)** — the type parameter appears only in *out* positions ([return types]({{ "/en/glossary/return-type/" | relative_url }})). `Producer<String>` becomes a subtype of `Producer<Any>`. This is why `List<out E>` is [covariant]({{ "/en/glossary/covariance/" | relative_url }}) in Kotlin and `MutableList<E>` is not.
- **[Contravariance]({{ "/en/glossary/contravariance/" | relative_url }}) (`in T`)** — the type parameter appears only in *in* positions (parameters). `Consumer<Any>` becomes a subtype of `Consumer<String>`. `Comparable<in T>` is the canonical example.
- **[Reification]({{ "/en/glossary/reified/" | relative_url }}) ([`reified`]({{ "/en/glossary/reified/" | relative_url }}))** — combined with [inline functions]({{ "/en/glossary/inline-functions/" | relative_url }}), the compiler copies the function body into every [call site]({{ "/en/glossary/call-site/" | relative_url }}) and substitutes the real class for `T`, which defeats [Type Erasure]({{ "/en/glossary/type-erasure/" | relative_url }}) locally and makes `T::class` and `is T` legal.

Two more tools complete the picture:

- **[Upper bounds]({{ "/en/glossary/upper-bound/" | relative_url }})** — `<K : Any>` constrains what may be substituted. Without a bound, `T` is implicitly `Any?`, so nullable types are allowed.
- **[Star projection]({{ "/en/glossary/star-projection/" | relative_url }}) (`<*>`)** — `ReorderState<*>` says "some concrete type I do not know". Reads come back as the [upper bound]({{ "/en/glossary/upper-bound/" | relative_url }}) (`Any?`), writes are forbidden. It is the safe replacement for Java [raw types]({{ "/en/glossary/raw-types/" | relative_url }}).

## The Senior Perspective (The Why)

Generics are where a Senior stops thinking about "what type is inside" and starts thinking about **who owns the type**.

- **[Variance]({{ "/en/glossary/variance/" | relative_url }}) is an API decision, not a syntax detail**: Declaring `out` on an interface is a promise to callers that the type will never be consumed. That promise is what lets a caller pass a `Producer<Task>` where a `Producer<Any>` is expected without an unchecked [cast]({{ "/en/glossary/cast/" | relative_url }}). Declaration-site [variance]({{ "/en/glossary/variance/" | relative_url }}) (Kotlin) states the promise once at the class; use-site [variance]({{ "/en/glossary/variance/" | relative_url }}) (Java's wildcards, `List<? extends T>`) forces every caller to restate it. This is why Kotlin's [collections]({{ "/en/glossary/collections/" | relative_url }}) split read-only (`List<out E>`) from mutable (`MutableList<E>`) — [immutability]({{ "/en/glossary/immutability/" | relative_url }}) is exactly what makes [covariance]({{ "/en/glossary/covariance/" | relative_url }}) sound.
- **PECS, restated**: Java's "Producer-Extends, Consumer-Super" is the same rule. Kotlin encodes it as `out` for producers and `in` for consumers. The mnemonic that actually survives an interview is the *position* rule: if `T` appears in a [return type]({{ "/en/glossary/return-type/" | relative_url }}) it must be `out`; if it appears in a parameter it must be `in`; if it appears in both, it must stay [invariant]({{ "/en/glossary/invariance/" | relative_url }}).
- **[Invariance]({{ "/en/glossary/invariance/" | relative_url }}) is a signal, not a failure**: When a generic [state holder]({{ "/en/glossary/state-holder/" | relative_url }}) both stores and hands back `K`, [invariance]({{ "/en/glossary/invariance/" | relative_url }}) is correct. Reaching for `out` there and then patching the holes with unchecked casts trades a compile error for a [`ClassCastException`]({{ "/en/glossary/class-cast-exception/" | relative_url }}) in production.
- **Function types are already variant**: `(T) -> R` compiles to `Function1<in P1, out R>`. Every callback parameter in a generic API — `itemKey: (T) -> String`, `onMove: (K, K) -> Boolean` — inherits that [variance]({{ "/en/glossary/variance/" | relative_url }}) for free. A Senior reads a signature and knows immediately which side of the boundary each type sits on.
- **[Reification]({{ "/en/glossary/reified/" | relative_url }}) has a cost**: [`reified`]({{ "/en/glossary/reified/" | relative_url }}) requires [`inline`]({{ "/en/glossary/inline-functions/" | relative_url }}), and [`inline`]({{ "/en/glossary/inline-functions/" | relative_url }}) means the body is duplicated at every [call site]({{ "/en/glossary/call-site/" | relative_url }}) — real [code bloat]({{ "/en/glossary/code-bloat/" | relative_url }}) and real [overhead]({{ "/en/glossary/overhead/" | relative_url }}) in APK size when the function is large or widely used. It is also why a [`reified`]({{ "/en/glossary/reified/" | relative_url }}) [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) parameter cannot be stored for later. Use it to *avoid passing a `Class<T>` token*, not as a default.
- **Erasure is what libraries fight**: [Moshi]({{ "/en/glossary/moshi/" | relative_url }}) and [Room]({{ "/en/glossary/room/" | relative_url }}) exist on the wrong side of [Type Erasure]({{ "/en/glossary/type-erasure/" | relative_url }}) and solve it in opposite ways — Moshi at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) with `Types.newParameterizedType` and [runtime reflection]({{ "/en/glossary/runtime-reflection/" | relative_url }}), Room at [compile time]({{ "/en/glossary/compile-time/" | relative_url }}) by generating code. [`reified`]({{ "/en/glossary/reified/" | relative_url }}) is the third option: solve it at the [call site]({{ "/en/glossary/call-site/" | relative_url }}).
- **Generics keep layers honest**: A shared UI component that is generic over its row type cannot name a domain entity, which enforces the [Single Responsibility Principle]({{ "/en/glossary/single-responsibility-principle/" | relative_url }}) structurally rather than by convention. The compiler, not a code review, is what stops the [data layer]({{ "/en/glossary/data-layer/" | relative_url }}) leaking into the design system.

## Code in Action

### Unbounded `T` — a generic component that cannot name a domain type

`SelectableListScaffold` is shared by the Trash and Archive screens. It is generic over the row type so the design system module never depends on `TaskEntity`. Note that `T` appears in a parameter (`items: List<T>`) *and* inside [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) types (`itemKey: (T) -> String`) — a function, unlike a class, needs no [variance]({{ "/en/glossary/variance/" | relative_url }}) annotation, because its type parameter is fixed per call.

```kotlin
// From FollowApp Suite — SelectableListScaffold.kt
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun <T> SelectableListScaffold(
    title: String,
    backContentDescription: String,
    emptyContent: @Composable () -> Unit,
    @StringRes searchPlaceholderRes: Int,
    items: List<T>,
    itemKey: (T) -> String,
    selectedIds: Set<String>,
    isSelectionMode: Boolean,
    // ...
    itemContent: @Composable (
        item: T,
        isSelected: Boolean,
        onClick: () -> Unit,
        onLongClick: () -> Unit
    ) -> Unit,
    snackbarHost: @Composable () -> Unit = {},
) {
```

At the [call site]({{ "/en/glossary/call-site/" | relative_url }}) `T` is inferred — no type argument is written anywhere. [Type inference]({{ "/en/glossary/type-inference/" | relative_url }}) picks it up from `items`, and then `itemKey` and `itemContent` are checked against it:

```kotlin
// From FollowApp Suite — TrashScreen.kt
SelectableListScaffold(
    title = stringResource(R.string.trash_screen_title),
    backContentDescription = stringResource(R.string.trash_back_content_description),
    emptyContent = { /* ... */ },
    searchPlaceholderRes = R.string.trash_search_placeholder,
    items = uiState.visibleTasks,   // T is inferred here
    itemKey = { it.id },            // ...and checked here
    selectedIds = uiState.selectedTaskIds,
    isSelectionMode = uiState.isSelectionMode,
    // ...
)
```

Because `items` is `List<T>` and `List<out E>` is [covariant]({{ "/en/glossary/covariance/" | relative_url }}), a caller can legally pass a `List<CompletedTask>` where the surrounding code reasons about a supertype. Had the parameter been `MutableList<T>`, that substitution would be rejected — writing into a [covariant]({{ "/en/glossary/covariance/" | relative_url }}) [collection]({{ "/en/glossary/collections/" | relative_url }}) is exactly the unsound operation the [invariance]({{ "/en/glossary/invariance/" | relative_url }}) of `MutableList` prevents.

### Bounded `K : Any` — and why the class stays invariant

`ReorderState` is the [state holder]({{ "/en/glossary/state-holder/" | relative_url }}) behind drag-to-reorder. Its key type is bounded by `Any` because the keys are used as map keys and must be non-null; and the class is **[invariant]({{ "/en/glossary/invariance/" | relative_url }})** because `K` appears on both sides of the boundary.

```kotlin
// From FollowApp Suite — DragToReorder.kt
@Stable
class ReorderState<K : Any> internal constructor(
    private val onMove: (fromKey: K, toKey: K) -> Boolean,   // K consumed
    private val onDragEnd: () -> Unit,
    private val onLongPressOnly: (K) -> Unit                 // K consumed
) {
    /** Key currently being dragged, or null. Observable from composition. */
    var draggingKey: K? by mutableStateOf(null)              // K produced
        private set

    private val itemCoords = mutableMapOf<K, LayoutCoordinates>()

    internal var liveKeys: List<K> = emptyList()             // K produced

    fun isDragging(key: K): Boolean = key == draggingKey     // K consumed

    internal fun updateBounds(key: K, coords: LayoutCoordinates) {
        itemCoords.entries.removeAll { it.key != key && it.value === coords }
        itemCoords[key] = coords
        // ...
    }
}
```

Marking this `class ReorderState<out K : Any>` would not compile: `isDragging(key: K)` and `updateBounds(key: K, ...)` put `K` in an *in* position. Marking it `<in K : Any>` would fail too, because `draggingKey: K?` and `liveKeys: List<K>` are *out* positions. [Invariance]({{ "/en/glossary/invariance/" | relative_url }}) here is not a limitation — it is the type system correctly reporting that this object owns the key in both directions.

The [extension functions]({{ "/en/01-kotlin-core/extension-functions/" | relative_url }}) that wire the state into Compose repeat the same bound, so `K` stays a single consistent type across the whole gesture API:

```kotlin
// From FollowApp Suite — DragToReorder.kt
@Composable
fun <K : Any> rememberReorderState(
    keys: List<K>,
    onMove: (fromKey: K, toKey: K) -> Boolean,
    onDragEnd: () -> Unit,
    onLongPressOnly: (K) -> Unit = {}
): ReorderState<K>

fun <K : Any> Modifier.reorderTarget(state: ReorderState<K>, key: K): Modifier =
    this.onGloballyPositioned { state.updateContainerBounds(key, it) }

fun <K : Any> Modifier.reorderViewport(state: ReorderState<K>): Modifier =
    this.onGloballyPositioned { state.updateViewport(it) }
```

### A pure producer — generics over parsing

`mapObjects` is generic over its *result*. `T` appears only in the return of the `transform` [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) and in `List<T>`: a textbook producer, and a [mapper function]({{ "/en/glossary/mapper-function/" | relative_url }}) that one generic [extension function]({{ "/en/01-kotlin-core/extension-functions/" | relative_url }}) reuses across four different entity types.

```kotlin
// From FollowApp Suite — BackupSerializer.kt
private fun <T> JSONArray.mapObjects(transform: (JSONObject) -> T): List<T> =
    (0 until length()).map { transform(getJSONObject(it)) }

fun parse(json: String): BackupBundle {
    // ...
    return try {
        BackupBundle(
            tasks = root.getJSONArray("tasks").mapObjects(::taskFromJson),
            labels = root.getJSONArray("labels").mapObjects(::labelFromJson),
            labelOptions = root.getJSONArray("labelOptions").mapObjects(::optionFromJson),
            presets = root.getJSONArray("presets").mapObjects(::presetFromJson)
        )
    } catch (e: JSONException) {
        throw IllegalArgumentException("Corrupted backup content", e)
    }
}
```

Notice what this design *avoids*: `mapObjects` never inspects `T`. It does not need [`reified`]({{ "/en/glossary/reified/" | relative_url }}), a `Class<T>` token, or [runtime reflection]({{ "/en/glossary/runtime-reflection/" | relative_url }}) — the caller supplies the constructor as a function reference, so [Type Erasure]({{ "/en/glossary/type-erasure/" | relative_url }}) is simply never a problem. Reaching for [`reified`]({{ "/en/glossary/reified/" | relative_url }}) before checking whether the type can be passed as a [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) is the most common junior mistake in generic code.

### Reification — when the type really must survive to Runtime

FollowApp Suite has no [`reified`]({{ "/en/glossary/reified/" | relative_url }}) usage, precisely because the patterns above cover its needs. The canonical case is an API where the type is the *only* input, and passing a `Class<T>` token would be noise.

```kotlin
// Not found in FAS — standalone example
// Without reified: the caller must hand over a Class token.
fun <T> Bundle.getEntity(key: String, type: Class<T>): T? =
    getSerializable(key)?.takeIf { type.isInstance(it) }?.let { type.cast(it) }

// With reified: the type argument survives inlining and is checked directly.
inline fun <reified T> Bundle.getEntity(key: String): T? =
    getSerializable(key) as? T

// Call site — no token, and the smart cast is real.
val task: TaskEntity? = bundle.getEntity("task")
```

The compiler copies the body into the [call site]({{ "/en/glossary/call-site/" | relative_url }}) and replaces `T` with `TaskEntity`, so `as? T` becomes a genuine `instanceof` check in the [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}). The trade-off is duplication: every [call site]({{ "/en/glossary/call-site/" | relative_url }}) carries its own copy, which is [code bloat]({{ "/en/glossary/code-bloat/" | relative_url }}) if the body is large. Keep [`reified`]({{ "/en/glossary/reified/" | relative_url }}) helpers small.

### Star projection — when the type does not matter

```kotlin
// Not found in FAS — standalone example
// Accepts any ReorderState regardless of key type.
fun logDragActivity(state: ReorderState<*>) {
    // Reads are typed as the upper bound: K? becomes Any?
    val key: Any? = state.draggingKey
    println("dragging: $key")

    // state.isDragging(someKey)  // does not compile: K is unknown for writes
}
```

`ReorderState<*>` is not a [raw type]({{ "/en/glossary/raw-types/" | relative_url }}). The compiler still tracks that *some* concrete `K : Any` exists — it just refuses any operation that would require knowing which one, preserving [type safety]({{ "/en/glossary/type-safety/" | relative_url }}) where Java's [raw types]({{ "/en/glossary/raw-types/" | relative_url }}) abandon it.

## The Interview (The Hot Seat)

**Question**: Why can't we use [`reified`]({{ "/en/glossary/reified/" | relative_url }}) types in regular functions, and what happens to them at the [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}) level?

**Senior Answer**: Because of [Type Erasure]({{ "/en/glossary/type-erasure/" | relative_url }}), a regular generic function compiles to a single method whose type parameter is erased to `Object`, so at [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) there is nothing left to check `T` against — `is T` and `T::class` have no referent. [`reified`]({{ "/en/glossary/reified/" | relative_url }}) requires [`inline`]({{ "/en/glossary/inline-functions/" | relative_url }}) because inlining is what removes the problem: instead of one shared method, the compiler copies the body into each [call site]({{ "/en/glossary/call-site/" | relative_url }}) and substitutes the concrete type argument known at that site. In the [bytecode]({{ "/en/glossary/bytecode/" | relative_url }}), `value is T` at a call that passes `TaskEntity` becomes a literal `instanceof TaskEntity`, and `T::class` becomes a constant class reference. That is also the cost: the body is duplicated per [call site]({{ "/en/glossary/call-site/" | relative_url }}), which is [code bloat]({{ "/en/glossary/code-bloat/" | relative_url }}), and a [`reified`]({{ "/en/glossary/reified/" | relative_url }}) type cannot escape the inlined frame — you cannot store it in a field or capture it in a non-inline [lambda]({{ "/en/glossary/lambdas/" | relative_url }}) for later. The practical rule is to use [`reified`]({{ "/en/glossary/reified/" | relative_url }}) for small helpers that would otherwise force callers to pass a `Class<T>` token, and to prefer passing behaviour as a function reference when the type itself is never inspected.

**Question**: You have a generic [state holder]({{ "/en/glossary/state-holder/" | relative_url }}) and the compiler rejects `out` on its type parameter. What does that tell you?

**Senior Answer**: That the class both produces and consumes the type, so [covariance]({{ "/en/glossary/covariance/" | relative_url }}) would be unsound. In a drag-to-reorder holder, the key is returned (`draggingKey: K?`, `liveKeys: List<K>`) and accepted (`isDragging(key: K)`, `updateBounds(key: K, ...)`). If `out` were allowed, a `ReorderState<Any>` reference could be bound to a `ReorderState<String>` and then handed a non-`String` key, which would only fail later as a [`ClassCastException`]({{ "/en/glossary/class-cast-exception/" | relative_url }}). [Invariance]({{ "/en/glossary/invariance/" | relative_url }}) is the correct answer, and the position rule is what proves it: `out` requires `T` only in return positions, `in` requires it only in parameter positions, and appearing in both means the class must stay [invariant]({{ "/en/glossary/invariance/" | relative_url }}). If callers genuinely need a type-agnostic view, the right tool is a [star projection]({{ "/en/glossary/star-projection/" | relative_url }}) — `ReorderState<*>` — which keeps reads (widened to the [upper bound]({{ "/en/glossary/upper-bound/" | relative_url }})) and forbids writes, rather than an unchecked [cast]({{ "/en/glossary/cast/" | relative_url }}) that trades a compile error for a [Runtime]({{ "/en/glossary/runtime/" | relative_url }}) crash.

---

[Back to Chapters]({{ "/" | relative_url }})
