---
layout: page
title: Collections y Mutabilidad
lang: es
permalink: /es/01-kotlin-core/collections-mutability/
order: 12
---

## The Theory (El Qué)

Las [Collections]({{ "/es/glosario/collections/" | relative_url }}) de Kotlin están divididas en dos jerarquías de interfaces. [`List<out E>`]({{ "/es/glosario/list/" | relative_url }}), [`Set<out E>`]({{ "/es/glosario/sets/" | relative_url }}) y [`Map<K, out V>`]({{ "/es/glosario/maps/" | relative_url }}) exponen solo operaciones de lectura. [`MutableList<E>`]({{ "/es/glosario/mutable-list/" | relative_url }}), [`MutableSet<E>`]({{ "/es/glosario/mutable-set/" | relative_url }}) y [`MutableMap<K, V>`]({{ "/es/glosario/mutable-map/" | relative_url }}) las extienden con [`add`]({{ "/es/glosario/add/" | relative_url }}), [`remove`]({{ "/es/glosario/remove/" | relative_url }}), [`put`]({{ "/es/glosario/put/" | relative_url }}) y [`clear`]({{ "/es/glosario/clear/" | relative_url }}). No existe una tercera jerarquía "inmutable" en la [Standard Library]({{ "/es/glosario/standard-library/" | relative_url }}) — y ese es el dato más importante de todos.

- **Read-only no es inmutable.** Un [`List<String>`]({{ "/es/glosario/list/" | relative_url }}) es una [Read-Only View]({{ "/es/glosario/read-only-view/" | relative_url }}): la *referencia* prohíbe la [mutación]({{ "/es/glosario/mutation/" | relative_url }}), pero el *objeto* detrás puede seguir siendo un [`ArrayList`]({{ "/es/glosario/arraylist/" | relative_url }}) que otro está escribiendo. [`listOf()`]({{ "/es/glosario/list-of/" | relative_url }}) devuelve una instancia no modificable; `myMutableList as List<String>` no.
- **La [Varianza]({{ "/es/glosario/variance/" | relative_url }}) se desprende de esa división.** [`List<out E>`]({{ "/es/glosario/list/" | relative_url }}) es [covariante]({{ "/es/glosario/covariance/" | relative_url }}) precisamente porque no se puede escribir en ella, así que `List<Task>` es un `List<Any>`. [`MutableList<E>`]({{ "/es/glosario/mutable-list/" | relative_url }}) debe quedar [invariante]({{ "/es/glosario/invariance/" | relative_url }}) — ver [Generics, Varianza y Reificación]({{ "/es/01-kotlin-core/generics-variance-reification/" | relative_url }}).
- **Tres familias, tres perfiles de costo.** [`List`]({{ "/es/glosario/list/" | relative_url }}) da acceso ordenado e indexado con [`contains`]({{ "/es/glosario/contains/" | relative_url }}) en `O(n)`. [`Set`]({{ "/es/glosario/sets/" | relative_url }}) da pertenencia en `O(1)` mediante hashing y descarta duplicados. [`Map`]({{ "/es/glosario/maps/" | relative_url }}) da búsqueda por clave en `O(1)`. [`setOf`]({{ "/es/glosario/set-of/" | relative_url }}) y [`mapOf`]({{ "/es/glosario/map-of/" | relative_url }}) están respaldados por `LinkedHashSet`/`LinkedHashMap`, así que el orden de iteración es el de inserción — Kotlin te da en silencio un determinismo que Java no.
- **Builders y conversiones.** [`toList()`]({{ "/es/glosario/to-list/" | relative_url }}), [`toSet()`]({{ "/es/glosario/to-set/" | relative_url }}) y [`toMutableList()`]({{ "/es/glosario/to-mutable-list/" | relative_url }}) producen una [Defensive Copy]({{ "/es/glosario/defensive-copy/" | relative_url }}). [`buildList {}`]({{ "/es/glosario/build-list/" | relative_url }}) y [`buildMap {}`]({{ "/es/glosario/build-map/" | relative_url }}) ([Builder Functions]({{ "/es/glosario/builder-functions/" | relative_url }})) permiten mutar localmente y devolver un resultado de solo lectura, sin exponer el receiver mutable.
- **Eager vs lazy.** Cada [Collection Operator]({{ "/es/glosario/collection-operators/" | relative_url }}) — [`map`]({{ "/es/glosario/map-operator/" | relative_url }}), [`filter`]({{ "/es/glosario/filter/" | relative_url }}), [`groupBy`]({{ "/es/glosario/group-by/" | relative_url }}), [`sorted`]({{ "/es/glosario/sorted/" | relative_url }}) — asigna una lista nueva por paso. Las [Sequences]({{ "/es/glosario/sequences/" | relative_url }}) ([`asSequence()`]({{ "/es/glosario/as-sequence/" | relative_url }})) evalúan de forma perezosa, un elemento a través de toda la cadena hasta que una [Terminal Operation]({{ "/es/glosario/terminal-operations/" | relative_url }}) tira de él, cambiando [Allocations]({{ "/es/glosario/allocations/" | relative_url }}) por [Overhead]({{ "/es/glosario/overhead/" | relative_url }}) por elemento.

## The Senior Perspective (El Porqué)

- **La mutabilidad es una cuestión de [Concurrencia]({{ "/es/glosario/concurrency/" | relative_url }}) y propiedad, no de estilo.** En el momento en que un [`MutableList`]({{ "/es/glosario/mutable-list/" | relative_url }}) cruza un límite — devuelto por un repositorio, guardado en el estado de un [ViewModel]({{ "/es/glosario/viewmodel-store/" | relative_url }}), capturado por una [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) — dos callers pueden escribirlo y ninguno lo posee. La [Inmutabilidad]({{ "/es/glosario/immutability/" | relative_url }}) es lo que hace seguro compartir estado entre [Coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) sin un [Synchronized Block]({{ "/es/glosario/synchronized-block/" | relative_url }}); es [Thread Safety]({{ "/es/glosario/thread-safety/" | relative_url }}) obtenida por construcción y no por locking.
- **Mutá localmente, publicá inmutable.** El patrón que sobrevive a un code review es: construir con un [`MutableList`]({{ "/es/glosario/mutable-list/" | relative_url }})/[`MutableMap`]({{ "/es/glosario/mutable-map/" | relative_url }}) dentro de una función y devolver el supertipo de solo lectura. La mutación queda confinada a un [Stack Frame]({{ "/es/glosario/stack-frame/" | relative_url }}) donde ningún otro thread puede observarla, y el [Call Site]({{ "/es/glosario/call-site/" | relative_url }}) recibe algo que no puede corromper. Es el núcleo imperativo dentro de una API [Functional-Style]({{ "/es/glosario/functional-style/" | relative_url }}), y suele ser más rápido que una cadena de operadores que asigna cuatro listas intermedias.
- **La trampa de la vista filtrada.** `private val _items = mutableListOf<T>()` más `val items: List<T> get() = _items` *no* es [Protected State]({{ "/es/glosario/protected-state/" | relative_url }}) — es un [Backing Field]({{ "/es/glosario/backing-field/" | relative_url }}) expuesto a través de un *tipo* de solo lectura. Los callers no pueden escribir a través de la interfaz, pero tienen una referencia viva: el contenido puede cambiar bajo sus pies en medio de una iteración, y una `ConcurrentModificationException` es el resultado amable. Un [`StateFlow`]({{ "/es/glosario/stateflow/" | relative_url }}) de una lista genuinamente nueva, o una [Defensive Copy]({{ "/es/glosario/defensive-copy/" | relative_url }}) con [`toList()`]({{ "/es/glosario/to-list/" | relative_url }}), es la versión honesta.
- **La igualdad de una [`data class`]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}) depende de la semántica de la colección.** Dos [Data Classes]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}) con `List<String>` son [iguales]({{ "/es/glosario/equals/" | relative_url }}) solo si los elementos coinciden *en orden*; con `Set<String>` el orden es irrelevante. Equivocarse acá es cómo una pantalla de Compose recompone en cada emisión, o no recompone cuando debería — Compose compara el estado previo y el siguiente con [`equals`]({{ "/es/glosario/equals/" | relative_url }}). Una colección mutable dentro de una clase de estado es peor todavía: no es [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}), así que el [Snapshot System]({{ "/es/glosario/snapshot-system/" | relative_url }}) no puede razonar sobre ella.
- **Elegí la estructura por el patrón de acceso, no por la declaración.** `if (id in list)` dentro de un [`filter`]({{ "/es/glosario/filter/" | relative_url }}) sobre `n` tasks es `O(n·m)`. Sacar [`list.toSet()`]({{ "/es/glosario/to-set/" | relative_url }}) fuera del loop lo convierte en `O(n + m)`. Es el hallazgo de performance más común en un codebase Android real, y la corrección es una sola llamada.
- **Las [Sequences]({{ "/es/glosario/sequences/" | relative_url }}) no son gratis.** Por debajo de unos mil elementos, la maquinaria de iteradores cuesta más que las listas intermedias que ahorra. Usá [`asSequence()`]({{ "/es/glosario/as-sequence/" | relative_url }}) cuando la cadena es larga, la fuente es grande, o el pipeline corta temprano en una [Terminal Operation]({{ "/es/glosario/terminal-operations/" | relative_url }}) (`first`, `any`, `take`) — no por defecto, y nunca cuando la cadena termina en [`sorted`]({{ "/es/glosario/sorted/" | relative_url }}).
- **Compose tiene su propia colección mutable.** [`mutableStateListOf()`]({{ "/es/glosario/mutable-state-list-of/" | relative_url }}) es una [Snapshot State List]({{ "/es/glosario/snapshot-state-list/" | relative_url }}) [observable]({{ "/es/glosario/observable-state/" | relative_url }}): mutarla dispara la recomposición exactamente de los lectores que la tocaron. Es el único lugar donde una colección mutable en código de UI es correcta — como estado local y optimista, nunca como source of truth.

## Code in Action

### Mutar localmente, devolver read-only

`GetLabelReferenceCounts` construye su resultado con un [`MutableMap`]({{ "/es/glosario/mutable-map/" | relative_url }}) porque contar requiere actualizaciones repetidas in-place, y luego devuelve [`Map<String, Int>`]({{ "/es/glosario/maps/" | relative_url }}). El tipo mutable nunca escapa de la función.

```kotlin
// De FollowApp Suite — GetLabelReferenceCounts.kt
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

El [Return Type]({{ "/es/glosario/return-type/" | relative_url }}) declarado es lo que carga la garantía. `refCounts` *es* un `LinkedHashMap` en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) — no se copió nada — pero ningún caller tiene una referencia tipada que permita escribir, y la referencia local muere con el [Stack Frame]({{ "/es/glosario/stack-frame/" | relative_url }}). La misma forma aparece en `StringListTypeConverter`, donde un `mutableListOf<String>` se llena desde un `JSONArray` y se devuelve como [`List<String>`]({{ "/es/glosario/list/" | relative_url }}):

```kotlin
// De FollowApp Suite — StringListTypeConverter.kt
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

### Elegir la estructura por la búsqueda

`computeTaskGroups` divide las tasks por opción de escala. El test de pertenencia corre una vez por task, así que las opciones se convierten a [`Set`]({{ "/es/glosario/sets/" | relative_url }}) *antes* del loop — convirtiendo un escaneo `O(n·m)` en búsquedas hasheadas `O(n)`.

```kotlin
// De FollowApp Suite — TasksViewModel.kt
val assignedValues = options.toSet()
val unassigned = tasks.filter { task ->
    val value = (task.customLabels[groupBy] as? LabelValue.Scale)?.value
    value == null || value !in assignedValues
}
groups.add(TaskGroup(chipLabel = groupBy, isAssigned = false, tasks = unassigned, chipShape = Chip.Shape.Scale))
```

Notá el acumulador: `val groups = mutableListOf<TaskGroup>()` dentro de la función, mientras que el [Return Type]({{ "/es/glosario/return-type/" | relative_url }}) es `List<TaskGroup>`. La misma regla, aplicada a un loop constructor que una cadena de operadores expresaría con menos claridad.

`mapTo(mutableSetOf())` es la misma idea fusionada en una sola pasada — [mapea]({{ "/es/glosario/map-operator/" | relative_url }}) y recolecta directo en la [Collection]({{ "/es/glosario/collections/" | relative_url }}) destino, sin lista intermedia:

```kotlin
// De FollowApp Suite — TasksViewModel.kt
val parentIds = if (hasSubtasksFilter != null) {
    tasks.mapNotNullTo(mutableSetOf()) { it.parentTaskId }
} else emptySet()
```

### Álgebra de Sets en vez de mutación manual

Alternar la selección de un grupo se expresa como aritmética de [`Set`]({{ "/es/glosario/sets/" | relative_url }}). `selectedTaskIds - groupSet` y `+ groupSet` devuelven cada uno un `Set` **nuevo**; nada se muta, así que el resultado puede publicarse directo en estado de UI [inmutable]({{ "/es/glosario/immutability/" | relative_url }}).

```kotlin
// De FollowApp Suite — BulkSelection.kt
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

Por eso el objeto de estado de UI declara `val selectedTaskIds: Set<String> = emptySet()` y no un [`MutableSet`]({{ "/es/glosario/mutable-set/" | relative_url }}): cada transición produce un valor nuevo, así que la comparación por [igualdad]({{ "/es/glosario/equals/" | relative_url }}) tiene sentido y se sostiene el [Unidirectional Data Flow]({{ "/es/glosario/unidirectional-data-flow/" | relative_url }}).

### El único lugar donde una colección mutable pertenece a la UI

El drag-to-reorder necesita que la lista se mueva *durante* el gesto, antes de que el [ViewModel]({{ "/es/glosario/viewmodel-store/" | relative_url }}) haya confirmado nada. Eso es una [Snapshot State List]({{ "/es/glosario/snapshot-state-list/" | relative_url }}): mutarla es observado por [Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) y recompone la lista inmediatamente.

```kotlin
// De FollowApp Suite — TasksScreen.kt
// Copia local optimista: los movimientos del drag mutan esta lista de forma
// sincrónica (sin round-trip al ViewModel por movimiento, que causaba saltos
// visibles); al ViewModel se le notifica una sola vez en el drop.
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

Dos detalles hacen que esto sea correcto y no una fuga. La lista mutable es *derivada* — se re-sincroniza desde `uiState.activeTasks`, que sigue siendo el source of truth — y nunca sale del composable. En el drop, el resultado se publica como un [`List<String>`]({{ "/es/glosario/list/" | relative_url }}) de solo lectura común: `onDragEnd = { onReorderComplete(localTasks.map { it.id }) }`.

Para movimientos entre grupos, el código toma una [Defensive Copy]({{ "/es/glosario/defensive-copy/" | relative_url }}) explícita antes de mutar, porque el `tasks` del grupo es un [`List`]({{ "/es/glosario/list/" | relative_url }}) de solo lectura propiedad del objeto de estado:

```kotlin
// De FollowApp Suite — TasksScreen.kt
val source = localGroups[originIdx].tasks.toMutableList()
val target = localGroups[targetIdx].tasks.toMutableList()
```

### La fuga que todo esto previene

```kotlin
// No encontrado en FAS — ejemplo standalone
class TaskCache {
    private val _tasks = mutableListOf<Task>()
    val tasks: List<Task> get() = _tasks   // *tipo* read-only, *objeto* vivo
}

val snapshot = cache.tasks       // el caller cree que es un valor estable
for (t in snapshot) { /* otro thread llama a cache.add(...) */ }
// -> ConcurrentModificationException, o renderizado silenciosamente obsoleto

// Versión honesta: devolver una copia que el caller posee.
val tasks: List<Task> get() = _tasks.toList()
```

[`toList()`]({{ "/es/glosario/to-list/" | relative_url }}) cuesta una copia de array. Una `ConcurrentModificationException` en producción cuesta bastante más.

## The Interview (En el banquillo)

**Pregunta**: En Kotlin, ¿[`List`]({{ "/es/glosario/list/" | relative_url }}) es inmutable?

**Respuesta Senior**: No — `List` es *de solo lectura*, que es una propiedad de la interfaz y no del objeto. `List<out E>` simplemente omite los métodos que mutan, así que una referencia tipada `List` no puede [agregar]({{ "/es/glosario/add/" | relative_url }}) ni [quitar]({{ "/es/glosario/remove/" | relative_url }}). La instancia detrás puede seguir siendo un [`ArrayList`]({{ "/es/glosario/arraylist/" | relative_url }}) que otro tiene como [`MutableList`]({{ "/es/glosario/mutable-list/" | relative_url }}) y escribe; [`listOf()`]({{ "/es/glosario/list-of/" | relative_url }}) devuelve una instancia no modificable, pero un `MutableList` upcasteado no. La consecuencia práctica es la fuga clásica del [Backing Field]({{ "/es/glosario/backing-field/" | relative_url }}): exponer `val items: List<T> get() = _items` sobre un `MutableList` privado le da a los callers una [vista]({{ "/es/glosario/read-only-view/" | relative_url }}) viva que puede cambiar en medio de una iteración — una `ConcurrentModificationException`, o una pantalla de Compose comparando una lista consigo misma y salteando la recomposición porque la referencia nunca cambió. La [Inmutabilidad]({{ "/es/glosario/immutability/" | relative_url }}) real requiere o una [Defensive Copy]({{ "/es/glosario/defensive-copy/" | relative_url }}) ([`toList()`]({{ "/es/glosario/to-list/" | relative_url }})) en el límite, o una [Persistent Collection]({{ "/es/glosario/persistent-collections/" | relative_url }}) de `kotlinx.collections.immutable`. La regla que aplico es: mutar localmente dentro de una función, publicar el supertipo de solo lectura — y si el valor escapa a estado compartido, copiarlo.

**Pregunta**: Una pantalla filtra diez mil tasks y, por cada una, verifica si su id está en una lista de ids seleccionados. Hace jank. ¿Qué cambiás?

**Respuesta Senior**: Primero la estructura de datos, después quizás la estrategia de evaluación. `id in selectedList` es un escaneo lineal, así que el [filtro]({{ "/es/glosario/filter/" | relative_url }}) es `O(n·m)`; sacar [`selectedList.toSet()`]({{ "/es/glosario/to-set/" | relative_url }}) fuera del loop convierte cada test de pertenencia en una búsqueda hash `O(1)` y toda la pasada en `O(n + m)` — una línea, y casi siempre es la corrección completa. Recién después miraría la cadena de operadores: cada [`map`]({{ "/es/glosario/map-operator/" | relative_url }})/`filter`/[`sortedBy`]({{ "/es/glosario/sorted/" | relative_url }}) asigna una lista intermedia completa, así que una cadena de cuatro pasos sobre diez mil ítems asigna cuarenta mil entradas y le da trabajo al [Garbage Collector]({{ "/es/glosario/garbage-collector/" | relative_url }}) en el main thread. Pasar a [`asSequence()`]({{ "/es/glosario/as-sequence/" | relative_url }}) evalúa un elemento a través de toda la cadena y corta temprano en [Terminal Operations]({{ "/es/glosario/terminal-operations/" | relative_url }}) como `first` o `any`; si el pipeline termina en [`sorted`]({{ "/es/glosario/sorted/" | relative_url }}) no gana nada, porque ordenar es inherentemente eager. Y verificaría dónde corre el trabajo: filtrar diez mil filas pertenece al [ViewModel]({{ "/es/glosario/viewmodel-store/" | relative_url }}) fuera del main thread, cacheado contra sus inputs, no recalculado dentro de un composable en cada recomposición.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
