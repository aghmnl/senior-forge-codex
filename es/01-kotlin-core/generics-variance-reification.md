---
layout: page
title: Generics, Varianza y Reificación
lang: es
permalink: /es/01-kotlin-core/generics-variance-reification/
order: 11
---

## The Theory (El Qué)

Los Generics permiten que una clase o función trabaje con muchos tipos manteniendo el [Type Safety]({{ "/es/glosario/type-safety/" | relative_url }}). En lugar de escribir un `List` por cada tipo de elemento, declarás [Generic Type Parameters]({{ "/es/glosario/generic-type-parameters/" | relative_url }}) — `List<T>` — y el compilador verifica cada [call site]({{ "/es/glosario/call-site/" | relative_url }}).

En la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) esa garantía existe únicamente en [Compile Time]({{ "/es/glosario/compile-time/" | relative_url }}). Por el [Type Erasure]({{ "/es/glosario/type-erasure/" | relative_url }}) (borrado de tipos), el argumento genérico se elimina del [Bytecode]({{ "/es/glosario/bytecode/" | relative_url }}): en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}), un `List<String>` y un `List<Task>` son la misma clase. Tres [Keywords]({{ "/es/glosario/keyword/" | relative_url }}) definen cómo trabajás dentro de esa restricción:

- **[Invarianza]({{ "/es/glosario/invariance/" | relative_url }}) (por defecto)** — `Box<String>` *no* es subtipo de `Box<Any>`, ni tampoco supertipo. Es el default seguro: el tipo se produce y se consume, así que ninguna dirección de sustitución es válida.
- **[Covarianza]({{ "/es/glosario/covariance/" | relative_url }}) (`out T`)** — el type parameter aparece solo en posiciones *out* ([tipos de retorno]({{ "/es/glosario/return-type/" | relative_url }})). `Producer<String>` pasa a ser subtipo de `Producer<Any>`. Por eso en Kotlin `List<out E>` es [covariante]({{ "/es/glosario/covariance/" | relative_url }}) y `MutableList<E>` no lo es.
- **[Contravarianza]({{ "/es/glosario/contravariance/" | relative_url }}) (`in T`)** — el type parameter aparece solo en posiciones *in* (parámetros). `Consumer<Any>` pasa a ser subtipo de `Consumer<String>`. `Comparable<in T>` es el ejemplo canónico.
- **[Reificación]({{ "/es/glosario/reified/" | relative_url }}) ([`reified`]({{ "/es/glosario/reified/" | relative_url }}))** — combinada con [Inline Functions]({{ "/es/glosario/inline-functions/" | relative_url }}), el compilador copia el cuerpo de la función en cada [call site]({{ "/es/glosario/call-site/" | relative_url }}) y sustituye `T` por la clase real, lo que derrota localmente al [Type Erasure]({{ "/es/glosario/type-erasure/" | relative_url }}) y vuelve legales `T::class` e `is T`.

Dos herramientas más completan el cuadro:

- **[Upper bounds]({{ "/es/glosario/upper-bound/" | relative_url }})** — `<K : Any>` restringe qué puede sustituirse. Sin bound, `T` es implícitamente `Any?`, así que se admiten tipos nullable.
- **[Star projection]({{ "/es/glosario/star-projection/" | relative_url }}) (`<*>`)** — `ReorderState<*>` significa "algún tipo concreto que no conozco". Las lecturas vuelven como el [upper bound]({{ "/es/glosario/upper-bound/" | relative_url }}) (`Any?`) y las escrituras quedan prohibidas. Es el reemplazo seguro de los [raw types]({{ "/es/glosario/raw-types/" | relative_url }}) de Java.

## The Senior Perspective (El Porqué)

Los Generics son el punto donde un Senior deja de pensar "qué tipo hay adentro" y empieza a pensar **quién es dueño del tipo**.

- **La [varianza]({{ "/es/glosario/variance/" | relative_url }}) es una decisión de API, no un detalle de sintaxis**: Declarar `out` en una interfaz es una promesa al caller de que el tipo nunca será consumido. Esa promesa es lo que permite pasar un `Producer<Task>` donde se espera un `Producer<Any>` sin un [Cast]({{ "/es/glosario/cast/" | relative_url }}) inseguro. La [varianza]({{ "/es/glosario/variance/" | relative_url }}) en el sitio de declaración (Kotlin) enuncia la promesa una sola vez en la clase; la [varianza]({{ "/es/glosario/variance/" | relative_url }}) en el sitio de uso (los wildcards de Java, `List<? extends T>`) obliga a cada caller a repetirla. Por eso las [Collections]({{ "/es/glosario/collections/" | relative_url }}) de Kotlin separan lectura (`List<out E>`) de mutación (`MutableList<E>`) — la [Immutability]({{ "/es/glosario/immutability/" | relative_url }}) es justamente lo que hace válida la [covarianza]({{ "/es/glosario/covariance/" | relative_url }}).
- **PECS, reformulado**: El "Producer-Extends, Consumer-Super" de Java es la misma regla. Kotlin la codifica como `out` para productores e `in` para consumidores. El mnemónico que realmente sobrevive a una entrevista es la regla de *posición*: si `T` aparece en un [tipo de retorno]({{ "/es/glosario/return-type/" | relative_url }}) debe ser `out`; si aparece en un parámetro debe ser `in`; si aparece en ambos, tiene que quedar [invariante]({{ "/es/glosario/invariance/" | relative_url }}).
- **La [invarianza]({{ "/es/glosario/invariance/" | relative_url }}) es una señal, no un fracaso**: Cuando un [State Holder]({{ "/es/glosario/state-holder/" | relative_url }}) genérico almacena y además devuelve `K`, la [invarianza]({{ "/es/glosario/invariance/" | relative_url }}) es lo correcto. Forzar `out` ahí y después tapar los agujeros con casts inseguros cambia un error de compilación por una [`ClassCastException`]({{ "/es/glosario/class-cast-exception/" | relative_url }}) en producción.
- **Los function types ya son variantes**: `(T) -> R` compila a `Function1<in P1, out R>`. Cada parámetro de callback en una API genérica — `itemKey: (T) -> String`, `onMove: (K, K) -> Boolean` — hereda esa [varianza]({{ "/es/glosario/variance/" | relative_url }}) gratis. Un Senior lee una firma y sabe de inmediato de qué lado de la frontera está cada tipo.
- **La [reificación]({{ "/es/glosario/reified/" | relative_url }}) tiene un costo**: [`reified`]({{ "/es/glosario/reified/" | relative_url }}) exige [`inline`]({{ "/es/glosario/inline-functions/" | relative_url }}), e [`inline`]({{ "/es/glosario/inline-functions/" | relative_url }}) significa que el cuerpo se duplica en cada [call site]({{ "/es/glosario/call-site/" | relative_url }}) — [Code Bloat]({{ "/es/glosario/code-bloat/" | relative_url }}) real y [Overhead]({{ "/es/glosario/overhead/" | relative_url }}) real en el tamaño del APK cuando la función es grande o muy usada. Es también la razón por la que un tipo [`reified`]({{ "/es/glosario/reified/" | relative_url }}) no puede guardarse para después dentro de una [Lambda]({{ "/es/glosario/lambdas/" | relative_url }}) no inline. Usalo para *evitar pasar un token `Class<T>`*, no como default.
- **El erasure es contra lo que pelean las librerías**: [Moshi]({{ "/es/glosario/moshi/" | relative_url }}) y [Room]({{ "/es/glosario/room/" | relative_url }}) viven del lado equivocado del [Type Erasure]({{ "/es/glosario/type-erasure/" | relative_url }}) y lo resuelven de formas opuestas — Moshi en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) con `Types.newParameterizedType` y [Runtime Reflection]({{ "/es/glosario/runtime-reflection/" | relative_url }}), Room en [Compile Time]({{ "/es/glosario/compile-time/" | relative_url }}) generando código. [`reified`]({{ "/es/glosario/reified/" | relative_url }}) es la tercera opción: resolverlo en el [call site]({{ "/es/glosario/call-site/" | relative_url }}).
- **Los Generics mantienen honestas a las capas**: Un componente de UI compartido que es genérico sobre su tipo de fila no puede nombrar una entidad de dominio, lo que impone el [Single Responsibility Principle]({{ "/es/glosario/single-responsibility-principle/" | relative_url }}) de forma estructural y no por convención. Es el compilador, y no un code review, lo que evita que la [Data Layer]({{ "/es/glosario/data-layer/" | relative_url }}) se filtre en el design system.

## Code in Action

### `T` sin bound — un componente genérico que no puede nombrar un tipo de dominio

`SelectableListScaffold` es compartido por las pantallas de Papelera y Archivo. Es genérico sobre el tipo de fila para que el módulo de design system nunca dependa de `TaskEntity`. Notá que `T` aparece en un parámetro (`items: List<T>`) *y* dentro de tipos [Lambda]({{ "/es/glosario/lambdas/" | relative_url }}) (`itemKey: (T) -> String`) — una función, a diferencia de una clase, no necesita anotación de [varianza]({{ "/es/glosario/variance/" | relative_url }}), porque su type parameter queda fijo en cada llamada.

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

En el [call site]({{ "/es/glosario/call-site/" | relative_url }}) `T` se infiere — no se escribe ningún type argument. El [Type Inference]({{ "/es/glosario/type-inference/" | relative_url }}) lo toma de `items`, y a partir de ahí verifica `itemKey` e `itemContent`:

```kotlin
// From FollowApp Suite — TrashScreen.kt
SelectableListScaffold(
    title = stringResource(R.string.trash_screen_title),
    backContentDescription = stringResource(R.string.trash_back_content_description),
    emptyContent = { /* ... */ },
    searchPlaceholderRes = R.string.trash_search_placeholder,
    items = uiState.visibleTasks,   // acá se infiere T
    itemKey = { it.id },            // ...y acá se verifica
    selectedIds = uiState.selectedTaskIds,
    isSelectionMode = uiState.isSelectionMode,
    // ...
)
```

Como `items` es `List<T>` y `List<out E>` es [covariante]({{ "/es/glosario/covariance/" | relative_url }}), un caller puede pasar legalmente un `List<CompletedTask>` donde el código circundante razona sobre un supertipo. Si el parámetro fuera `MutableList<T>`, esa sustitución sería rechazada: escribir dentro de una [Collection]({{ "/es/glosario/collections/" | relative_url }}) [covariante]({{ "/es/glosario/covariance/" | relative_url }}) es exactamente la operación insegura que la [invarianza]({{ "/es/glosario/invariance/" | relative_url }}) de `MutableList` previene.

### `K : Any` con bound — y por qué la clase queda invariante

`ReorderState` es el [State Holder]({{ "/es/glosario/state-holder/" | relative_url }}) detrás del drag-to-reorder. Su tipo de key está acotado por `Any` porque las keys se usan como claves de mapa y deben ser non-null; y la clase es **[invariante]({{ "/es/glosario/invariance/" | relative_url }})** porque `K` aparece a ambos lados de la frontera.

```kotlin
// From FollowApp Suite — DragToReorder.kt
@Stable
class ReorderState<K : Any> internal constructor(
    private val onMove: (fromKey: K, toKey: K) -> Boolean,   // K consumido
    private val onDragEnd: () -> Unit,
    private val onLongPressOnly: (K) -> Unit                 // K consumido
) {
    /** Key currently being dragged, or null. Observable from composition. */
    var draggingKey: K? by mutableStateOf(null)              // K producido
        private set

    private val itemCoords = mutableMapOf<K, LayoutCoordinates>()

    internal var liveKeys: List<K> = emptyList()             // K producido

    fun isDragging(key: K): Boolean = key == draggingKey     // K consumido

    internal fun updateBounds(key: K, coords: LayoutCoordinates) {
        itemCoords.entries.removeAll { it.key != key && it.value === coords }
        itemCoords[key] = coords
        // ...
    }
}
```

Escribir `class ReorderState<out K : Any>` no compilaría: `isDragging(key: K)` y `updateBounds(key: K, ...)` ponen `K` en posición *in*. Marcarla `<in K : Any>` también fallaría, porque `draggingKey: K?` y `liveKeys: List<K>` son posiciones *out*. La [invarianza]({{ "/es/glosario/invariance/" | relative_url }}) acá no es una limitación — es el sistema de tipos reportando correctamente que este objeto es dueño de la key en ambas direcciones.

Las [Extension Functions]({{ "/es/01-kotlin-core/extension-functions/" | relative_url }}) que conectan el state con Compose repiten el mismo bound, así `K` se mantiene como un único tipo consistente en toda la API del gesto:

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

### Un productor puro — Generics sobre el parseo

`mapObjects` es genérico sobre su *resultado*. `T` aparece solo en el retorno de la [Lambda]({{ "/es/glosario/lambdas/" | relative_url }}) `transform` y en `List<T>`: un productor de manual, y una [Mapper Function]({{ "/es/glosario/mapper-function/" | relative_url }}) que una sola [Extension Function]({{ "/es/01-kotlin-core/extension-functions/" | relative_url }}) genérica reutiliza para cuatro tipos de entidad distintos.

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

Fijate en lo que este diseño *evita*: `mapObjects` nunca inspecciona `T`. No necesita [`reified`]({{ "/es/glosario/reified/" | relative_url }}), ni un token `Class<T>`, ni [Runtime Reflection]({{ "/es/glosario/runtime-reflection/" | relative_url }}) — el caller aporta el constructor como referencia a función, así que el [Type Erasure]({{ "/es/glosario/type-erasure/" | relative_url }}) simplemente nunca es un problema. Recurrir a [`reified`]({{ "/es/glosario/reified/" | relative_url }}) antes de verificar si el tipo puede pasarse como [Lambda]({{ "/es/glosario/lambdas/" | relative_url }}) es el error junior más común en código genérico.

### Reificación — cuando el tipo realmente debe sobrevivir hasta Runtime

FollowApp Suite no tiene usos de [`reified`]({{ "/es/glosario/reified/" | relative_url }}), precisamente porque los patrones anteriores cubren sus necesidades. El caso canónico es una API donde el tipo es la *única* entrada, y pasar un token `Class<T>` sería puro ruido.

```kotlin
// Not found in FAS — standalone example
// Sin reified: el caller tiene que entregar un token Class.
fun <T> Bundle.getEntity(key: String, type: Class<T>): T? =
    getSerializable(key)?.takeIf { type.isInstance(it) }?.let { type.cast(it) }

// Con reified: el type argument sobrevive al inlining y se verifica directo.
inline fun <reified T> Bundle.getEntity(key: String): T? =
    getSerializable(key) as? T

// Call site — sin token, y el cast es real.
val task: TaskEntity? = bundle.getEntity("task")
```

El compilador copia el cuerpo dentro del [call site]({{ "/es/glosario/call-site/" | relative_url }}) y reemplaza `T` por `TaskEntity`, de modo que `as? T` se convierte en un `instanceof` genuino en el [Bytecode]({{ "/es/glosario/bytecode/" | relative_url }}). El trade-off es la duplicación: cada [call site]({{ "/es/glosario/call-site/" | relative_url }}) carga su propia copia, lo que es [Code Bloat]({{ "/es/glosario/code-bloat/" | relative_url }}) si el cuerpo es grande. Mantené chicos los helpers [`reified`]({{ "/es/glosario/reified/" | relative_url }}).

### Star projection — cuando el tipo no importa

```kotlin
// Not found in FAS — standalone example
// Acepta cualquier ReorderState sin importar el tipo de key.
fun logDragActivity(state: ReorderState<*>) {
    // Las lecturas se tipan como el upper bound: K? pasa a ser Any?
    val key: Any? = state.draggingKey
    println("dragging: $key")

    // state.isDragging(someKey)  // no compila: K es desconocido para escribir
}
```

`ReorderState<*>` no es un [raw type]({{ "/es/glosario/raw-types/" | relative_url }}). El compilador sigue sabiendo que existe *algún* `K : Any` concreto — simplemente rechaza cualquier operación que requiera saber cuál, preservando el [Type Safety]({{ "/es/glosario/type-safety/" | relative_url }}) justo donde los [raw types]({{ "/es/glosario/raw-types/" | relative_url }}) de Java lo abandonan.

## The Interview (En el banquillo)

**Pregunta**: ¿Por qué no podemos usar tipos [`reified`]({{ "/es/glosario/reified/" | relative_url }}) en funciones normales y qué sucede con ellos a nivel de [Bytecode]({{ "/es/glosario/bytecode/" | relative_url }})?

**Respuesta Senior**: Por el [Type Erasure]({{ "/es/glosario/type-erasure/" | relative_url }}), una función genérica normal compila a un único método cuyo type parameter se borra a `Object`, así que en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) no queda nada contra lo cual verificar `T` — `is T` y `T::class` no tienen referente. [`reified`]({{ "/es/glosario/reified/" | relative_url }}) exige [`inline`]({{ "/es/glosario/inline-functions/" | relative_url }}) porque el inlining es lo que elimina el problema: en lugar de un método compartido, el compilador copia el cuerpo en cada [call site]({{ "/es/glosario/call-site/" | relative_url }}) y sustituye el tipo concreto conocido en ese punto. En el [Bytecode]({{ "/es/glosario/bytecode/" | relative_url }}), `value is T` en una llamada que pasa `TaskEntity` se vuelve un `instanceof TaskEntity` literal, y `T::class` se vuelve una referencia constante de clase. Ese es también el costo: el cuerpo se duplica por [call site]({{ "/es/glosario/call-site/" | relative_url }}), lo que es [Code Bloat]({{ "/es/glosario/code-bloat/" | relative_url }}), y un tipo [`reified`]({{ "/es/glosario/reified/" | relative_url }}) no puede escapar del frame inlineado — no podés guardarlo en un campo ni capturarlo en una [Lambda]({{ "/es/glosario/lambdas/" | relative_url }}) no inline para después. La regla práctica es usar [`reified`]({{ "/es/glosario/reified/" | relative_url }}) para helpers chicos que de otro modo obligarían al caller a pasar un token `Class<T>`, y preferir pasar comportamiento como referencia a función cuando el tipo nunca se inspecciona.

**Pregunta**: Tenés un [State Holder]({{ "/es/glosario/state-holder/" | relative_url }}) genérico y el compilador rechaza `out` en su type parameter. ¿Qué te está diciendo eso?

**Respuesta Senior**: Que la clase produce y consume el tipo, así que la [covarianza]({{ "/es/glosario/covariance/" | relative_url }}) sería insegura. En un holder de drag-to-reorder, la key se devuelve (`draggingKey: K?`, `liveKeys: List<K>`) y se acepta (`isDragging(key: K)`, `updateBounds(key: K, ...)`). Si `out` estuviera permitido, una referencia `ReorderState<Any>` podría apuntar a un `ReorderState<String>` y recibir una key que no es `String`, lo que solo fallaría más tarde como [`ClassCastException`]({{ "/es/glosario/class-cast-exception/" | relative_url }}). La [invarianza]({{ "/es/glosario/invariance/" | relative_url }}) es la respuesta correcta, y la regla de posición es lo que lo demuestra: `out` requiere `T` solo en posiciones de retorno, `in` solo en posiciones de parámetro, y aparecer en ambas significa que la clase debe quedar [invariante]({{ "/es/glosario/invariance/" | relative_url }}). Si los callers realmente necesitan una vista agnóstica del tipo, la herramienta adecuada es una [star projection]({{ "/es/glosario/star-projection/" | relative_url }}) — `ReorderState<*>` — que conserva las lecturas (ampliadas al [upper bound]({{ "/es/glosario/upper-bound/" | relative_url }})) y prohíbe las escrituras, en vez de un [Cast]({{ "/es/glosario/cast/" | relative_url }}) inseguro que cambia un error de compilación por un crash en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}).

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
