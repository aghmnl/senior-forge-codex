---
layout: page
title: Inmutabilidad y Estado Atómico para UI
lang: es
permalink: /es/01-kotlin-core/immutability-atomic-state/
order: 13
---

## The Theory (El Qué)

La [Inmutabilidad]({{ "/es/glosario/immutability/" | relative_url }}) significa que un valor nunca cambia después de construirse; para "cambiarlo" producís un valor nuevo. El **estado atómico** significa que cada una de esas transiciones se publica como un único paso indivisible, así ningún observador ve nunca un cambio a medio aplicar. En un [State Holder]({{ "/es/glosario/state-holder/" | relative_url }}) de Android, las dos cosas son un solo mecanismo: una clase de estado inmutable más una operación de publicación atómica.

- **La clase de estado es un valor, no un objeto.** Una [`data class`]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}) donde toda propiedad es un `val` de un tipo de solo lectura tiene [Value Semantics]({{ "/es/glosario/value-semantics/" | relative_url }}): su identidad *es* su contenido. Eso es lo que hace significativo a [`equals`]({{ "/es/glosario/equals/" | relative_url }}), y sobre [`equals`]({{ "/es/glosario/equals/" | relative_url }}) están construidos tanto [Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) como [`StateFlow`]({{ "/es/glosario/stateflow/" | relative_url }}).
- **[`copy`]({{ "/es/glosario/copy/" | relative_url }}) es cómo se expresan las transiciones.** Asigna un objeto chico y reutiliza cada referencia sin cambios — [Structural Sharing]({{ "/es/glosario/structural-sharing/" | relative_url }}) — así que una clase de estado con treinta campos cuesta unos cientos de bytes por transición, sin importar qué tan grandes sean las listas que contiene.
- **`value =` no es [atómico]({{ "/es/glosario/atomicity/" | relative_url }}) cuando el valor nuevo depende del viejo.** `_uiState.value = _uiState.value.copy(...)` es leer, calcular, escribir: tres pasos con los que otro escritor puede intercalarse. El resultado es un update perdido — una [Race Condition]({{ "/es/glosario/race-condition/" | relative_url }}) que nunca crashea, simplemente descarta en silencio una de las acciones del usuario.
- **[`update {}`]({{ "/es/glosario/update/" | relative_url }}) cierra ese hueco.** Es un retry loop de [Compare-and-Set]({{ "/es/glosario/compare-and-set/" | relative_url }}): leer el valor actual, ejecutar la lambda, publicar solo si el valor no cambió, y si cambió recalcular a partir del fresco. Lock-free, y todo el read-modify-write se vuelve una transición indivisible.
- **CAS compara referencias, así que la inmutabilidad es la precondición.** Si el objeto de estado se pudiera mutar in-place, su identidad sobreviviría al cambio y la comparación tendría éxito sobre data vieja. La [Inmutabilidad]({{ "/es/glosario/immutability/" | relative_url }}) no es decoración alrededor de `update` — es lo que hace correcto a `update`.
- **El extremo de escritura tiene que ser privado.** `private val _uiState = MutableStateFlow(...)` más `val uiState = _uiState.`[`asStateFlow()`]({{ "/es/glosario/as-state-flow/" | relative_url }}) es el par: un escritor, muchos lectores, y una [Read-Only View]({{ "/es/glosario/read-only-view/" | relative_url }}) a la que no se le puede hacer Cast de vuelta.
- **[`StateFlow`]({{ "/es/glosario/stateflow/" | relative_url }}) es [conflated]({{ "/es/glosario/conflation/" | relative_url }}) y deduplicado.** Guarda exactamente un valor, descarta los intermedios para un collector lento, y no emite nada cuando el valor nuevo es [igual]({{ "/es/glosario/equals/" | relative_url }}) al actual. Eso es correcto para estado y equivocado para eventos one-shot.

## The Senior Perspective (El Porqué)

- **"Todo corre en el main thread" es la suposición que produce el bug.** No es así: `viewModelScope.launch(Dispatchers.IO)`, `flowOn`, un callback de repositorio y un `collect` en un dispatcher de background escriben estado fuera de Main. Y aun en `Main.immediate`, una llamada `suspend` entre la lectura y la escritura es un punto de suspensión donde otra coroutine toma el control. `update` no es programación defensiva para un caso exótico; es el caso ordinario.
- **La lambda que recibe [`update`]({{ "/es/glosario/update/" | relative_url }}) debe ser pura.** Puede correr varias veces por el reintento de CAS, así que logging, analytics, navegación y llamadas a repositorios adentro se van a disparar dos veces bajo contención. Es el hallazgo de code review más común una vez que un equipo adopta `update` — la corrección es calcular el estado siguiente adentro y hacer los side effects después.
- **Leé el valor viejo *dentro* del bloque, nunca afuera.** `val current = _uiState.value; _uiState.update { it.copy(x = current.x + 1) }` reintroduce exactamente la race que `update` existe para eliminar. Una vez que la transición se expresa como función pura de `it`, la atomicidad es estructural y no una cuestión de disciplina.
- **La mutabilidad dentro de la clase de estado derrota todo lo anterior en una línea.** `val tasks: MutableList<Task>` es un `val` con semántica de referencia: dos objetos de estado comparten un buffer, [`equals`]({{ "/es/glosario/equals/" | relative_url }}) reporta "sin cambios" mientras el contenido difiere, CAS no puede detectar el cambio, y la clase no es [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}) así que [Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) la recompone defensivamente en cada pasada del padre. La falla es silenciosa en las dos direcciones — una pantalla que no se actualiza, o una que se actualiza todo el tiempo.
- **Derivá en vez de almacenar.** El [Derived State]({{ "/es/glosario/derived-state/" | relative_url }}) — una propiedad con getter y sin [Backing Field]({{ "/es/glosario/backing-field/" | relative_url }}) — no puede desincronizarse de su fuente, lo que hace irrepresentable a la combinación inconsistente. Almacenar `selectedTaskIds` y `isSelectionMode` a la vez crea una obligación de sincronización en cada lugar donde se hace [`copy`]({{ "/es/glosario/copy/" | relative_url }}); derivar uno del otro elimina la obligación y con ella la clase entera de bugs. Es [Single Source of Truth]({{ "/es/glosario/single-source-of-truth/" | relative_url }}) aplicado dentro de una sola clase.
- **Un objeto de estado le gana a cinco flows.** Cinco `MutableStateFlow` separados se pueden actualizar de forma independiente, lo que significa que se pueden observar en una combinación que no es un estado real — loading en `true` con resultados ya presentes, selection mode activo con la selección vacía. Un único objeto de estado inmutable hace que cada transición sea todo-o-nada y le da a la pantalla exactamente una cosa que renderizar.
- **La conflación hace a `StateFlow` incorrecto para eventos.** "El set de filtros actual" solo necesita su último valor; "mostrar este snackbar" tiene que pasar una vez por ocurrencia. Modelar un evento one-shot como campo de estado hace que se pierda en un frame lento, o que se repita tras un cambio de configuración — el toast que vuelve a aparecer al rotar es este bug.
- **La inmutabilidad es cómo se consigue [Thread Safety]({{ "/es/glosario/thread-safety/" | relative_url }}) sin un [Synchronized Block]({{ "/es/glosario/synchronized-block/" | relative_url }}).** Un valor que nadie puede escribir no necesita lock para compartirse entre [Coroutines]({{ "/es/glosario/coroutines/" | relative_url }}). La única celda mutable genuinamente compartida que queda es la referencia del `MutableStateFlow`, y esa celda está protegida por CAS. Ese es todo el diseño de concurrencia de un [ViewModel]({{ "/es/glosario/viewmodel-store/" | relative_url }}) moderno.

## Code in Action

### El par que define el límite

```kotlin
// De FollowApp Suite — TasksViewModel.kt
private val _uiState = MutableStateFlow(TasksUiState())
val uiState: StateFlow<TasksUiState> = _uiState.asStateFlow()
```

Un escritor privado, una [Read-Only View]({{ "/es/glosario/read-only-view/" | relative_url }}) pública. [`asStateFlow()`]({{ "/es/glosario/as-state-flow/" | relative_url }}) devuelve un objeto genuinamente distinto en vez de la misma instancia bajo un tipo más angosto, así que un caller no puede hacer [Cast]({{ "/es/glosario/cast/" | relative_url }}) de vuelta a `MutableStateFlow` y emitir. Eso es el "uni" del [Unidirectional Data Flow]({{ "/es/glosario/unidirectional-data-flow/" | relative_url }}).

### La clase de estado: toda propiedad un `val`

```kotlin
// De FollowApp Suite — TasksUiState.kt
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

Prestá atención a las dos propiedades del cuerpo. Son [Derived State]({{ "/es/glosario/derived-state/" | relative_url }}): calculadas al leer, invisibles para el [`equals`]({{ "/es/glosario/equals/" | relative_url }}) y el [`copy`]({{ "/es/glosario/copy/" | relative_url }}) generados (que solo cubren las propiedades del constructor primario), y por lo tanto incapaces de desincronizarse. `isSelectionMode = true` con la selección vacía no es un estado que esta clase pueda expresar.

Fijate también en `Map<String, Set<String>>` para `collapsedGroupsByPreset` — un map de solo lectura de sets de solo lectura. La inmutabilidad se sostiene hasta el fondo, que es lo que la garantía realmente exige.

### La transición: `update`, no `value =`

```kotlin
// De FollowApp Suite — TasksViewModel.kt
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

Los dos son read-modify-write, y los dos leen a través del parámetro `it`/`state` de la lambda y no de `_uiState.value`. Si dos de estos corren concurrentemente, el loop de [Compare-and-Set]({{ "/es/glosario/compare-and-set/" | relative_url }}) hace que el perdedor recalcule sobre el resultado del ganador en vez de sobrescribirlo. Notá la aritmética de [`Set`]({{ "/es/glosario/sets/" | relative_url }}): `- taskId` y `+ taskId` devuelven cada uno un set nuevo, así que la transición es una función pura y el reintento no tiene side effects. `mapTo(mutableSetOf())` construye localmente y se publica como un [`Set`]({{ "/es/glosario/sets/" | relative_url }}) de solo lectura — mutar localmente, publicar inmutable, como en [Collections y Mutabilidad]({{ "/es/01-kotlin-core/collections-mutability/" | relative_url }}).

### Atomicidad en una transición de múltiples campos

```kotlin
// De FollowApp Suite — TasksViewModel.kt
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

Siete propiedades restauradas desde disco en una sola publicación. Esto corre en `Dispatchers.IO` — el comentario del código fuente lo dice explícitamente, y agrega que "los updates de `MutableStateFlow` ya son thread-safe". Con siete flows separados, o siete asignaciones `value =`, la UI podría observar un estado con el sort order restaurado pero los filtros anteriores. Acá la pantalla ve el estado viejo o el nuevo, nunca una mezcla.

### Estado anidado sin perder atomicidad

```kotlin
// De FollowApp Suite — TasksViewModel.kt
_uiState.update { it.copy(form = it.form.copy(title = title)) }
_uiState.update { it.copy(form = it.form.copy(labelSearchResults = results)) }
```

`TaskFormState` es a su vez una [`data class`]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}) inmutable, así que un cambio anidado es un [`copy`]({{ "/es/glosario/copy/" | relative_url }}) anidado. El detalle crucial es que `it.form` se lee **dentro** del bloque. Sacarlo afuera — `val form = _uiState.value.form` — restauraría la race para el objeto anidado mientras el `update` externo se ve perfectamente seguro.

### Leer el estado una vez, y después transicionar

```kotlin
// De FollowApp Suite — TasksViewModel.kt
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

Este es el uso legítimo de `.value`: tomar un snapshot consistente para *leer* — validación, derivar el payload para una llamada al repositorio — mientras cada *escritura* sigue pasando por [`update`]({{ "/es/glosario/update/" | relative_url }}). El valor leído es un objeto inmutable, así que no puede cambiar mientras la función lo inspecciona, y la escritura no depende de él.

### Deduplicación con una proyección angosta

```kotlin
// De FollowApp Suite — TasksViewModel.kt
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
    .collect { key -> /* escribir a preferencias */ }
```

`TasksUiState` cambia con cada tecla; solo siete de sus propiedades vale la pena persistir. Proyectar a un `PersistKey` inmutable y aplicar [`distinctUntilChanged`]({{ "/es/glosario/distinct-until-changed/" | relative_url }}) convierte "el estado cambió" en "cambió algo persistible" — y funciona *solo* porque `PersistKey` tiene [Value Semantics]({{ "/es/glosario/value-semantics/" | relative_url }}). Un map mutable ahí adentro y el operador compararía igual mientras el contenido difiere, tragándose la escritura en silencio.

### El bug que todo esto previene

```kotlin
// No encontrado en FAS — ejemplo standalone
// Dos coroutines activando filtros distintos al mismo tiempo.
fun onFilterToggled(filter: String) {
    // Thread A lee {}, calcula {dueToday}
    // Thread B lee {}, calcula {starred}
    // A escribe {dueToday}; B escribe {starred}. El filtro de A desapareció.
    _uiState.value = _uiState.value.copy(filters = _uiState.value.filters + filter)
}

// Versión atómica: la lambda de B se vuelve a ejecutar sobre el resultado publicado por A.
fun onFilterToggled(filter: String) {
    _uiState.update { it.copy(filters = it.filters + filter) }
}
```

Sin crash, sin log, sin stack trace — solo un filtro que "a veces no queda", irreproducible en el dispositivo rápido del reviewer.

## The Interview (En el banquillo)

**Pregunta**: `_uiState.value = _uiState.value.copy(isLoading = false)` — ¿qué tiene de malo esta línea?

**Respuesta Senior**: Es un read-modify-write tratado como si fuera un solo paso. `MutableStateFlow.value` está respaldado por `@Volatile`, así que el get individual y el set individual son cada uno [atómicos]({{ "/es/glosario/atomicity/" | relative_url }}) y visibles entre threads — que es justamente por qué la línea parece segura. Pero entre la lectura y la escritura otro escritor puede publicar, y esta línea va a hacer [copy]({{ "/es/glosario/copy/" | relative_url }}) de un valor viejo y sobrescribir ese update. Es una [Race Condition]({{ "/es/glosario/race-condition/" | relative_url }}) de update perdido, y no crashea: la pantalla renderiza un estado plausible que simplemente omite una de las acciones del usuario, así que se reporta como "a veces el filtro no me queda" y nunca se reproduce en un dispositivo rápido. La objeción que espero es "pero si todo corre en el main thread" — no es así. `viewModelScope.launch(Dispatchers.IO)`, `flowOn`, un callback de repositorio, un `collect` en un dispatcher de background escriben desde otro lado, y aun en `Main.immediate` una llamada `suspend` entre la lectura y la escritura es un punto de suspensión donde otra coroutine se intercala. La solución es [`update {}`]({{ "/es/glosario/update/" | relative_url }}), que es un retry loop de [Compare-and-Set]({{ "/es/glosario/compare-and-set/" | relative_url }}): publica solo si el valor que leyó sigue vigente, y si no, recalcula sobre el fresco. Vienen dos advertencias con eso — la lambda puede correr más de una vez, así que tiene que ser pura, sin logging ni navegación adentro; y el valor viejo hay que leerlo por el parámetro de la lambda, no desde `_uiState.value` afuera del bloque, o la race vuelve al toque. La regla que aplico es mecánica: si el valor nuevo menciona al viejo, usá `update`; un `value =` simple está bien solo para una publicación incondicional, como resetear a un objeto de estado fresco.

**Pregunta**: ¿Por qué el estado atómico requiere que la clase de estado sea inmutable? ¿No alcanza con `update`?

**Respuesta Senior**: No, porque [Compare-and-Set]({{ "/es/glosario/compare-and-set/" | relative_url }}) compara *referencias*, no contenido. Si el objeto de estado se puede mutar in-place, su identidad sobrevive a la mutación: `update` lee el objeto, alguien edita el contenido de ese mismo objeto, el CAS compara la referencia consigo misma, tiene éxito, y publica un valor calculado sobre data que ya cambió. La protección no hace nada, en silencio. El mismo problema de identidad rompe todo lo que viene después — [`StateFlow`]({{ "/es/glosario/stateflow/" | relative_url }}) deduplica por [`equals`]({{ "/es/glosario/equals/" | relative_url }}), así que mutar una lista dentro del estado y re-emitir la misma instancia no emite nada y la pantalla nunca se actualiza; [Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) saltea la [Recomposition]({{ "/es/glosario/recomposition/" | relative_url }}) con la misma comparación, y una `data class` que contiene un `MutableList` no es [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}), así que en cambio recompone defensivamente en cada pasada del padre. Los dos modos de falla son silenciosos y opuestos. Y el `val` en la propiedad es solo la mitad del trabajo — el *tipo* de la propiedad tiene que ser de solo lectura hasta el fondo, y por eso una clase de estado declara `Set<String>` y `Map<String, Set<String>>` en vez de sus contrapartes mutables. La ventaja es que la inmutabilidad es lo que compra la seguridad de concurrencia en primer lugar: un valor que nadie puede escribir no necesita un [Synchronized Block]({{ "/es/glosario/synchronized-block/" | relative_url }}) para compartirse entre [Coroutines]({{ "/es/glosario/coroutines/" | relative_url }}), así que la única celda mutable compartida de todo el [ViewModel]({{ "/es/glosario/viewmodel-store/" | relative_url }}) es la referencia del `MutableStateFlow` — y esa está protegida por CAS. La objeción del costo ("copiar en cada tecla") la responde el [Structural Sharing]({{ "/es/glosario/structural-sharing/" | relative_url }}): [`copy`]({{ "/es/glosario/copy/" | relative_url }}) asigna un objeto chico con referencias a las partes sin cambios, no una copia profunda de las listas.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
