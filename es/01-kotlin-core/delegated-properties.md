---
layout: page
title: Delegated Properties (by lazy, by viewModels)
lang: es
permalink: /es/01-kotlin-core/delegated-properties/
order: 10
---

## The Theory (El Qué)

Una propiedad delegada es aquella cuya lógica de `get` (y opcionalmente `set`) es manejada por un objeto separado — el **delegate** (delegado) — en lugar de un [backing field]({{ "/es/glosario/backing-field/" | relative_url }}). La [keyword]({{ "/es/glosario/keyword/" | relative_url }}) `by` es el puente sintáctico: `val x by SomeDelegate()` le indica al compilador que enrute todos los accesos a través del `operator fun getValue()` del delegado (y `operator fun setValue()` para `var`).

A nivel de [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}), el compilador genera un campo oculto que almacena la instancia del delegado y reescribe cada acceso a la propiedad como una llamada a `getValue(thisRef, property)`. El parámetro `property` es un [`KProperty<*>`]({{ "/es/glosario/kproperty/" | relative_url }}) que transporta metadata de [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) sobre la propiedad delegada (nombre, [tipo]({{ "/es/glosario/type-inference/" | relative_url }}), visibilidad).

La [standard library]({{ "/es/glosario/standard-library/" | relative_url }}) de Kotlin incluye varios delegates incorporados:

- **`lazy`** — calcula un valor en el primer acceso y lo cachea. Cubierto en detalle en [Lateinit vs Lazy]({{ "/es/01-kotlin-core/lateinit-vs-lazy/" | relative_url }}).
- **`observable`** — ejecuta un callback después de cada asignación.
- **`vetoable`** — ejecuta un callback antes de la asignación y puede rechazar el nuevo valor.
- **`notNull`** — un `var` no nulable que lanza excepción si se lee antes de ser asignado (similar a `lateinit` pero funciona con [primitivos]({{ "/es/glosario/primitives/" | relative_url }})).
- **Map delegation** — lee valores de propiedades desde un `Map<String, Any?>` usando el nombre de la propiedad como clave.

Más allá de la [standard library]({{ "/es/glosario/standard-library/" | relative_url }}), el ecosistema Android usa extensivamente el patrón de delegación:

- **`by viewModels()`** / **`by activityViewModels()`** — scoping de ViewModel [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}) en Fragments.
- **`by hiltViewModel()`** — inyección de ViewModel powered by [Hilt]({{ "/es/glosario/hilt/" | relative_url }}) en [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}).
- **`by remember { mutableStateOf() }`** — delegación de estado en Compose, donde el delegado es un `MutableState<T>` y la [keyword]({{ "/es/glosario/keyword/" | relative_url }}) `by` desenvuelve `value` automáticamente.
- **`by mutableStateOf()`** — la misma delegación pero fuera de funciones [`@Composable`]({{ "/es/glosario/composable/" | relative_url }}), típicamente en clases [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}) que mantienen [estado observable]({{ "/es/glosario/observable-state/" | relative_url }}) para el [sistema de snapshots]({{ "/es/glosario/snapshot-system/" | relative_url }}) de Compose.
- **`by collectAsStateWithLifecycle()`** — convierte un [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) en `State<T>` de Compose que respeta el [lifecycle]({{ "/es/glosario/lifecycle-event/" | relative_url }}).

## The Senior Perspective (El Porqué)

Las propiedades delegadas son una de las abstracciones más poderosas de Kotlin porque extraen **lógica transversal de propiedades** en unidades reutilizables y componibles.

- **El Contrato de `by`**: Cualquier objeto que provea `operator fun getValue(thisRef: T, property:` [`KProperty<*>`]({{ "/es/glosario/kproperty/" | relative_url }})`): R` puede ser un [property delegate]({{ "/es/glosario/property-delegate/" | relative_url }}) de lectura; agregar `operator fun setValue(thisRef: T, property:` [`KProperty<*>`]({{ "/es/glosario/kproperty/" | relative_url }})`), value: R)` lo convierte en un [property delegate]({{ "/es/glosario/property-delegate/" | relative_url }}) de lectura-escritura. La convención es puramente estructural — no se requiere ninguna interfaz (aunque `ReadOnlyProperty<T, R>` y `ReadWriteProperty<T, R>` existen para [type safety]({{ "/es/glosario/type-safety/" | relative_url }})). Un Senior sabe que esto es [operator overloading]({{ "/es/glosario/operator-overloading/" | relative_url }}) en acción — el compilador resuelve `by` a estos operadores específicos en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}).
- **`provideDelegate`**: Cuando un [property delegate]({{ "/es/glosario/property-delegate/" | relative_url }}) define `operator fun provideDelegate(thisRef: T, property:` [`KProperty<*>`]({{ "/es/glosario/kproperty/" | relative_url }})`): D`, el compilador la llama en el momento de inicialización de la propiedad en lugar de usar el delegado directamente. Esto permite validación o personalización antes de que el delegado sea instalado — por ejemplo, verificar que el nombre de la propiedad coincida con una clave en un mapa de configuración.
- **Compose State como Delegación**: Cuando escribís `var count by remember { mutableStateOf(0) }`, la keyword [`by`]({{ "/es/glosario/by-delegation/" | relative_url }}) delega lecturas y escrituras al objeto `MutableState<Int>`. Sin [`by`]({{ "/es/glosario/by-delegation/" | relative_url }}), necesitarías escribir `count.value` en todos lados. Esto no es solo [syntax sugar]({{ "/es/glosario/syntax-sugar/" | relative_url }}) — se integra profundamente con el [sistema de snapshots]({{ "/es/glosario/snapshot-system/" | relative_url }}) de Compose: cada escritura dispara la recomposición de los lectores.
- **`by mutableStateOf()` en Clases [`@Stable`]({{ "/es/glosario/stable/" | relative_url }})**: Fuera de funciones [`@Composable`]({{ "/es/glosario/composable/" | relative_url }}), una clase [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}) puede mantener estado observable por Compose delegando a `mutableStateOf()`. Este es el patrón para [state holders]({{ "/es/glosario/state-holder/" | relative_url }}) complejos con múltiples propiedades (como controladores de drag-and-drop) donde las propiedades respaldadas por [snapshots]({{ "/es/glosario/snapshot-system/" | relative_url }}) deben disparar recomposición sin envolver todo en llamadas a `State<T>.value`.
- **Awareness de Allocations**: Cada `by lazy` crea un objeto `Lazy<T>` en el [heap]({{ "/es/glosario/heap/" | relative_url }}). Cada `by mutableStateOf()` crea un objeto `SnapshotMutableState`. En [hot loops]({{ "/es/glosario/hot-loops/" | relative_url }}) o [allocations]({{ "/es/glosario/allocations/" | relative_url }}) críticas, un Senior considera si el [overhead]({{ "/es/glosario/overhead/" | relative_url }}) de la delegación está justificado o si un [backing field]({{ "/es/glosario/backing-field/" | relative_url }}) directo es más apropiado.
- **viewModels() y Scoping**: `by viewModels()` es un delegate basado en `Lazy` que scopea el ViewModel al [`ViewModelStore`]({{ "/es/glosario/viewmodel-store/" | relative_url }}) del Fragment. `by activityViewModels()` lo scopea a la Activity. Un Senior entiende que estos no son solo conveniencia — definen el **scope de supervivencia** del ViewModel a través de cambios de configuración y operaciones del [back stack]({{ "/es/glosario/back-stack/" | relative_url }}). En Compose con [Hilt]({{ "/es/glosario/hilt/" | relative_url }}), `hiltViewModel()` es una función `@Composable` (no delegación de propiedad) que usa el entry del [back stack]({{ "/es/glosario/back-stack/" | relative_url }}) del [navigation component]({{ "/es/glosario/navigation-component/" | relative_url }}) como scope.

## Code in Action

### Delegación de estado Compose con `by remember { mutableStateOf() }`

La keyword `by` desenvuelve `MutableState<T>` para que las lecturas y escrituras parezcan variables comunes, mientras el [sistema de snapshots]({{ "/es/glosario/snapshot-system/" | relative_url }}) de Compose trackea cada cambio para la recomposición.

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

### `by mutableStateOf()` en una clase [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}) — propiedades snapshot-backed sin `remember`

Cuando el estado necesita ser observable por Compose pero vive en una clase (no en una función [`@Composable`]({{ "/es/glosario/composable/" | relative_url }})), `by mutableStateOf()` delega directamente al [sistema de snapshots]({{ "/es/glosario/snapshot-system/" | relative_url }}). Cada escritura de propiedad dispara la recomposición de cualquier composable que la lea.

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

### Delegación Flow-to-Compose con `by collectAsStateWithLifecycle()`

Convertir un [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) en `State<T>` de Compose vía `by` crea una suscripción [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}) que pausa la colección cuando la UI no es visible y se reanuda automáticamente.

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

### Delegate custom — `Delegates.observable` y `Delegates.vetoable`

Delegates de la [standard library]({{ "/es/glosario/standard-library/" | relative_url }}) que ejecutan callbacks en cambios de propiedades. `observable` notifica después del cambio; `vetoable` puede rechazar el nuevo valor antes de que se almacene.

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

### Map delegation — leyendo valores de propiedades desde un Map

Las propiedades pueden delegar a un `Map`, usando el nombre de la propiedad como clave de búsqueda. Esto es útil para parsear estructuras tipo JSON o mapas de configuración.

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

## The Interview (En el banquillo)

**Pregunta**: ¿Cómo funciona la [keyword]({{ "/es/glosario/keyword/" | relative_url }}) `by` de Kotlin internamente, y qué diferencia hay entre `by mutableStateOf()` en una clase [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}) y `by remember { mutableStateOf() }` en una función [`@Composable`]({{ "/es/glosario/composable/" | relative_url }})?

**Respuesta Senior**: La [keyword]({{ "/es/glosario/keyword/" | relative_url }}) `by` se resuelve en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}) a través de [operator overloading]({{ "/es/glosario/operator-overloading/" | relative_url }}): el compilador busca `operator fun getValue` (y `setValue` para `var`) en el objeto delegado y reescribe los accesos a la propiedad como llamadas a esos operadores. Un campo oculto almacena la instancia del delegado, y un objeto [`KProperty<*>`]({{ "/es/glosario/kproperty/" | relative_url }}) con metadata se pasa en cada acceso. Para `by remember { mutableStateOf(0) }` en una función [`@Composable`]({{ "/es/glosario/composable/" | relative_url }}), el bloque `remember` preserva el `MutableState` a través de recomposiciones usando la [slot table]({{ "/es/glosario/slot-table/" | relative_url }}) de Compose — el delegado tiene su scope en el [lifetime de la composición]({{ "/es/glosario/composition-lifetime/" | relative_url }}) de ese composable. Para `by mutableStateOf(0)` en una clase [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}), no hay `remember` — el `MutableState` es un campo de instancia regular de la clase. Sigue participando en el [sistema de snapshots]({{ "/es/glosario/snapshot-system/" | relative_url }}) de Compose (las escrituras disparan recomposición de los lectores), pero su [lifetime]({{ "/es/glosario/composition-lifetime/" | relative_url }}) está atado a la instancia de la clase, no a un slot de composición. Esto lo hace adecuado para [state holders]({{ "/es/glosario/state-holder/" | relative_url }}) como controladores de drag-and-drop que se crean una vez y se comparten entre múltiples composables, mientras que el estado basado en `remember` es local a la posición de un composable en el árbol.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
