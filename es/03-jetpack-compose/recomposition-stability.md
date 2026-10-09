---
layout: page
title: "Recomposition & Stability"
lang: es
permalink: /es/03-jetpack-compose/recomposition-stability/
order: 1
---

## The Theory (El Qué)

En [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}), la UI es el resultado de llamar a funciones [`@Composable`]({{ "/es/glosario/composable/" | relative_url }}). La primera vez que corren, Compose construye la **[composition]({{ "/es/glosario/composition/" | relative_url }})** ([composición]({{ "/es/glosario/composition/" | relative_url }})): un árbol que registra qué emitió cada función y qué estado leyó. Cuando parte de ese estado cambia, Compose no reconstruye toda la pantalla. Vuelve a ejecutar **solo los composables que leyeron el estado que cambió**. Esa nueva ejecución es la **[recomposition]({{ "/es/glosario/recomposition/" | relative_url }})** (recomposición).

Dos mecanismos mantienen chica la [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}):

- **Invalidación precisa.** Compose registra las lecturas de estado a través del [snapshot system]({{ "/es/glosario/snapshot-system/" | relative_url }}). Cuando un [`MutableState`]({{ "/es/glosario/mutable-state/" | relative_url }}) cambia, solo se programan para recomponer los scopes que lo leyeron, no sus padres ni sus hermanos.
- **[Skipping]({{ "/es/glosario/skipping/" | relative_url }}) (salteo).** Cuando un composable se recompone, vuelve a llamar a sus hijos. Para cada hijo, Compose compara los argumentos nuevos con los de la llamada anterior. Si son todos iguales, el hijo **se saltea**: su cuerpo no corre y se reutiliza el resultado anterior.

Ahí entra la **[stability]({{ "/es/glosario/stability/" | relative_url }})** ([estabilidad]({{ "/es/glosario/stability/" | relative_url }})). Compose solo puede confiar en esa comparación si los tipos de los parámetros son **[stable]({{ "/es/glosario/stability/" | relative_url }})**. Un tipo es [stable]({{ "/es/glosario/stability/" | relative_url }}) cuando:

1. [`equals`]({{ "/es/glosario/equals/" | relative_url }}) siempre da el mismo resultado para las mismas dos instancias, y
2. si una propiedad pública puede cambiar, el cambio le avisa a la [composition]({{ "/es/glosario/composition/" | relative_url }}) (está respaldada por [`MutableState`]({{ "/es/glosario/mutable-state/" | relative_url }})), y
3. todas sus propiedades públicas también son [stable]({{ "/es/glosario/stability/" | relative_url }}).

Los [primitivos]({{ "/es/glosario/primitives/" | relative_url }}), [`String`]({{ "/es/glosario/string/" | relative_url }}), los tipos función ([lambdas]({{ "/es/glosario/lambdas/" | relative_url }})) y [`MutableState`]({{ "/es/glosario/mutable-state/" | relative_url }}) son [stable]({{ "/es/glosario/stability/" | relative_url }}). También lo es una clase cuyas propiedades son todas [`val`]({{ "/es/glosario/val/" | relative_url }}) de tipos [stable]({{ "/es/glosario/stability/" | relative_url }}), como la mayoría de las data classes. Los tipos son **[unstable]({{ "/es/glosario/stability/" | relative_url }})** cuando Compose no puede probar esas reglas: una clase con una propiedad [`var`]({{ "/es/glosario/var/" | relative_url }}), una clase de un módulo compilado sin el compilador de Compose y, sobre todo, [`List`]({{ "/es/glosario/list/" | relative_url }}), [`Set`]({{ "/es/glosario/sets/" | relative_url }}) y [`Map`]({{ "/es/glosario/maps/" | relative_url }}). Son interfaces, y la instancia detrás de un [`List`]({{ "/es/glosario/list/" | relative_url }}) podría ser un [`MutableList`]({{ "/es/glosario/mutable-list/" | relative_url }}) que cambia sin avisarle a nadie.

Desde [Kotlin]({{ "/es/glosario/kotlin/" | relative_url }}) 2.0.20, el **[strong skipping]({{ "/es/glosario/strong-skipping/" | relative_url }})** está activado por defecto y cambia la regla para los parámetros [unstable]({{ "/es/glosario/stability/" | relative_url }}). En lugar de hacer que el composable no se pueda saltear, Compose los compara por **instancia** ([`===`]({{ "/es/glosario/referential-equality/" | relative_url }})), y a los [stable]({{ "/es/glosario/stability/" | relative_url }}) por [`equals`]({{ "/es/glosario/equals/" | relative_url }}). Además recuerda las [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) automáticamente, así que pasar una [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) ya no rompe el [skipping]({{ "/es/glosario/skipping/" | relative_url }}). Los tipos [unstable]({{ "/es/glosario/stability/" | relative_url }}) dejaron de ser un bloqueo; se comparan de forma más estricta.

Compose también puede ejecutar los composables en cualquier orden, saltearlos, correrlos muchas veces, o cancelar y descartar una [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}). Por eso el cuerpo de un composable tiene que estar **libre de efectos secundarios**: describe la UI, no hace trabajo.

## The Senior Perspective (El Porqué)

- **Recomponer es normal; recomponer de más es el problema.** Un composable que se recompone porque cambiaron sus datos funciona como debe. Los bugs son los composables que se recomponen cuando nada de lo que muestran cambió, o que se recomponen en cada frame. Antes de optimizar, hay que medir: el [Layout Inspector]({{ "/es/glosario/layout-inspector/" | relative_url }}) muestra la cantidad de recomposiciones y de salteos por composable, y los [reportes del compilador de Compose]({{ "/es/glosario/compose-compiler-reports/" | relative_url }}) listan qué funciones se pueden saltear y qué parámetros son [unstable]({{ "/es/glosario/stability/" | relative_url }}).
- **Con [strong skipping]({{ "/es/glosario/strong-skipping/" | relative_url }}), la identidad importa más que la [stability]({{ "/es/glosario/stability/" | relative_url }}).** Un parámetro [`List`]({{ "/es/glosario/list/" | relative_url }}) [unstable]({{ "/es/glosario/stability/" | relative_url }}) ahora se compara con [`===`]({{ "/es/glosario/referential-equality/" | relative_url }}). Si el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) actualiza su estado con [`copy`]({{ "/es/glosario/copy/" | relative_url }}) y no toca la lista, la instancia es la misma y el hijo se saltea. Pero una lista creada **durante la [composition]({{ "/es/glosario/composition/" | relative_url }})** (`tasks.filter { ... }` en el cuerpo de un composable) es una instancia nueva en cada [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}), así que el hijo que la recibe nunca se saltea. La solución es calcularla fuera de la [composition]({{ "/es/glosario/composition/" | relative_url }}), en el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}), o hacer [`remember`]({{ "/es/glosario/remember/" | relative_url }}) con sus entradas como keys.
- **Leer el estado lo más tarde posible.** Cada lectura de estado decide qué scope se recompone. Leer un valor que cambia rápido (un [offset]({{ "/es/glosario/modifier-offset/" | relative_url }}) de scroll, una animación) arriba en el árbol recompone todo lo que está debajo. Pasar una [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) en lugar del valor (`{ offset }`), o leerlo adentro de un modifier basado en [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) ([`Modifier.offset { }`]({{ "/es/glosario/modifier-offset/" | relative_url }}), `drawBehind { }`), mueve la lectura a la fase de layout o de dibujo, y la [composition]({{ "/es/glosario/composition/" | relative_url }}) directamente no corre.
- **[`derivedStateOf`]({{ "/es/glosario/derived-state/" | relative_url }}) cuando la salida cambia menos que la entrada.** Una posición de scroll cambia en cada pixel, pero "mostrar el botón de volver arriba" cambia dos veces. [`derivedStateOf`]({{ "/es/glosario/derived-state/" | relative_url }}) recompone solo cuando cambia el resultado derivado.
- **[`@Immutable`]({{ "/es/glosario/immutable-annotation/" | relative_url }}) y [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}) son promesas, no verificaciones.** Le dicen al compilador que trate un tipo como [stable]({{ "/es/glosario/stability/" | relative_url }}), pero nada lo verifica. Anotar una clase con internos mutables hace que Compose saltee cuando no debería, y la UI muestra datos viejos. Mejor la inmutabilidad real: propiedades [`val`]({{ "/es/glosario/val/" | relative_url }}), colecciones inmutables, o un archivo de configuración de [stability]({{ "/es/glosario/stability/" | relative_url }}) para tipos de otros módulos que se sabe que son inmutables.
- **Los efectos secundarios en el cuerpo de un composable son bugs.** Loguear, mandar analytics, escribir en un [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) o lanzar trabajo directamente en el cuerpo corre una cantidad impredecible de veces. Los efectos van en [`LaunchedEffect`]({{ "/es/glosario/launched-effect/" | relative_url }}), [`SideEffect`]({{ "/es/glosario/side-effect/" | relative_url }}) o [`DisposableEffect`]({{ "/es/glosario/disposable-effect/" | relative_url }}), y en los callbacks de eventos.

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

## The Interview (En el banquillo)

**Pregunta**: ¿Qué es la [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}) en [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}), y qué decide si un composable se saltea?

**Respuesta Senior**: La [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}) es Compose volviendo a ejecutar un composable porque cambió un estado que leyó. Compose registra cada lectura de estado a través del [snapshot system]({{ "/es/glosario/snapshot-system/" | relative_url }}), así que cuando un [`MutableState`]({{ "/es/glosario/mutable-state/" | relative_url }}) cambia, solo se invalidan los scopes que lo leyeron, no toda la pantalla. Cuando un scope se recompone, vuelve a llamar a sus hijos, y para cada hijo Compose compara los argumentos nuevos con los anteriores: si son todos iguales, el hijo se saltea y se reutiliza su resultado anterior. Esa comparación depende de la [stability]({{ "/es/glosario/stability/" | relative_url }}). Un tipo [stable]({{ "/es/glosario/stability/" | relative_url }}) garantiza que [`equals`]({{ "/es/glosario/equals/" | relative_url }}) es confiable y que cualquier cambio le avisa a la [composition]({{ "/es/glosario/composition/" | relative_url }}), algo que se cumple para [primitivos]({{ "/es/glosario/primitives/" | relative_url }}), strings, [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}), [`MutableState`]({{ "/es/glosario/mutable-state/" | relative_url }}) y data classes inmutables. Interfaces como [`List`]({{ "/es/glosario/list/" | relative_url }}) son [unstable]({{ "/es/glosario/stability/" | relative_url }}) porque la instancia podría ser mutable. Antes de [Kotlin]({{ "/es/glosario/kotlin/" | relative_url }}) 2.0.20, un solo parámetro [unstable]({{ "/es/glosario/stability/" | relative_url }}) hacía que el composable no se pudiera saltear. Con [strong skipping]({{ "/es/glosario/strong-skipping/" | relative_url }}), que hoy viene por defecto, los parámetros [unstable]({{ "/es/glosario/stability/" | relative_url }}) se comparan por instancia y las [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) se recuerdan automáticamente, así que la regla práctica pasó a ser: pasar la misma instancia cuando nada cambió. Y como Compose puede volver a ejecutar, reordenar o cancelar composables, sus cuerpos tienen que estar libres de efectos secundarios.

**Pregunta**: Una lista de tareas se recompone con cada tecla en un campo de búsqueda, aunque las tareas no cambiaron. ¿Cómo lo diagnosticás y cómo lo arreglás?

**Respuesta Senior**: Primero lo confirmo, con los contadores de [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}) del [Layout Inspector]({{ "/es/glosario/layout-inspector/" | relative_url }}), para ver qué composable se recompone y si sus hijos se saltean o no. Después reviso qué recibe la lista. La causa típica es que un parámetro sea una instancia nueva en cada [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}): el padre lee el texto de búsqueda, así que se recompone con cada tecla, y si arma la lista durante la [composition]({{ "/es/glosario/composition/" | relative_url }}), con un [`filter`]({{ "/es/glosario/filter/" | relative_url }}) o un [`map`]({{ "/es/glosario/map-operator/" | relative_url }}) en su cuerpo, cada [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}) crea un [`List`]({{ "/es/glosario/list/" | relative_url }}) nuevo. Con [strong skipping]({{ "/es/glosario/strong-skipping/" | relative_url }}), un [`List`]({{ "/es/glosario/list/" | relative_url }}) [unstable]({{ "/es/glosario/stability/" | relative_url }}) se compara por identidad, así que una instancia nueva significa que el hijo nunca se saltea, aunque el contenido sea idéntico. La solución es dejar de crearla en la [composition]({{ "/es/glosario/composition/" | relative_url }}): o calcularla en el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) y exponerla en el estado, para que solo cambie cuando cambian las tareas, o hacer [`remember`]({{ "/es/glosario/remember/" | relative_url }}) con las tareas como key. Otras causas que reviso son un tipo que Compose considera [unstable]({{ "/es/glosario/stability/" | relative_url }}) y que comparo por valor (ahí ayuda una colección inmutable o una configuración de [stability]({{ "/es/glosario/stability/" | relative_url }})), y una lectura de estado ubicada demasiado arriba, que bajo al composable que realmente la necesita, o la difiero con una [lambda]({{ "/es/glosario/lambdas/" | relative_url }}).

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
