---
layout: page
title: "UI State Modeling: Sealed vs Flat Data Class"
lang: es
permalink: /es/05-architecture/ui-state-modeling/
order: 1
---

## The Theory (El Qué)

El UI state (estado de UI) de una pantalla es todo lo que la UI necesita para dibujarse en un momento dado. En un [unidirectional data flow]({{ "/es/glosario/unidirectional-data-flow/" | relative_url }}), el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) lo expone como un único [`StateFlow`]({{ "/es/glosario/stateflow/" | relative_url }}), y la UI dibuja el valor que recibe. Hay dos formas dominantes de modelar ese valor:

- **[Sealed state]({{ "/es/glosario/sealed-state/" | relative_url }})**: una [`sealed interface`]({{ "/es/glosario/sealed-interface/" | relative_url }}) (o [`sealed class`]({{ "/es/glosario/sealed-class/" | relative_url }})) donde cada subtipo es un estado mutuamente excluyente de la pantalla, como [`Loading`]({{ "/es/glosario/loading-state/" | relative_url }}), [`Success`]({{ "/es/glosario/success-state/" | relative_url }}) y [`Error`]({{ "/es/glosario/error-state/" | relative_url }}). Cada subtipo lleva solo los datos que tienen sentido en ese estado, y un [`when`]({{ "/es/glosario/when-expression/" | relative_url }}) sobre el estado tiene que manejar todos los subtipos: si se agrega uno nuevo, cada [`when`]({{ "/es/glosario/when-expression/" | relative_url }}) sin `else` deja de compilar hasta que se lo maneje.
- **[Flat data class]({{ "/es/glosario/flat-data-class/" | relative_url }})** (data class plana): una única [`data class`]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}) con todas las propiedades de la pantalla una al lado de la otra: flags como `isLoading`, campos nullables como `errorMessage`, y los datos en sí. Cada cambio produce una instancia nueva con [`copy()`]({{ "/es/glosario/copy/" | relative_url }}), normalmente adentro de [`MutableStateFlow.update { }`]({{ "/es/02-coroutines-flow/mutablestateflow-update/" | relative_url }}) para que no se pierdan actualizaciones concurrentes.

La diferencia es lo que el tipo permite. Un [sealed state]({{ "/es/glosario/sealed-state/" | relative_url }}) solo puede ser uno de sus subtipos a la vez, así que **no puede representar combinaciones imposibles**: no hay forma de estar en [`Loading`]({{ "/es/glosario/loading-state/" | relative_url }}) y en [`Error`]({{ "/es/glosario/error-state/" | relative_url }}) al mismo tiempo. Una [flat data class]({{ "/es/glosario/flat-data-class/" | relative_url }}) puede representar cualquier combinación de sus campos, incluidas las que no tienen sentido, como `isLoading = true` con un mensaje de error y una lista de resultados, y el compilador no se queja.

Las dos no son excluyentes. Un modelo **híbrido** usa una adentro de la otra: una [flat data class]({{ "/es/glosario/flat-data-class/" | relative_url }}) para las partes de la pantalla que conviven, con una propiedad sealed (muchas veces nullable) para una parte que tiene variantes mutuamente excluyentes, o un [sealed state]({{ "/es/glosario/sealed-state/" | relative_url }}) de nivel superior cuyo subtipo principal es una [flat data class]({{ "/es/glosario/flat-data-class/" | relative_url }}).

## The Senior Perspective (El Porqué)

- **La pregunta es si los estados realmente se excluyen.** Una pantalla de detalle que está cargando, mostrando un ítem o mostrando un error es el caso de libro de un [sealed state]({{ "/es/glosario/sealed-state/" | relative_url }}). Una pantalla de lista con búsqueda, filtros, modo selección, un formulario y un refresco en background no lo es: el usuario puede escribir una búsqueda mientras la lista está cargada, seleccionar ítems con un filtro activo, y ver un error no bloqueante mientras los datos siguen en pantalla. Forzar eso en `Loading / Loaded / Error` obliga a copiar las propiedades compartidas en cada subtipo, o a perderlas cuando cambia el estado (la búsqueda desaparece cuando un refresco pasa a [`Loading`]({{ "/es/glosario/loading-state/" | relative_url }})).
- **Sealed compra seguridad del compilador; flat compra flexibilidad a costa de disciplina.** Con una [flat data class]({{ "/es/glosario/flat-data-class/" | relative_url }}) nada impide una combinación imposible, así que lo tiene que impedir el código: propiedades derivadas (`val isEmpty get() = !isLoading && items.isEmpty()`) en lugar de flags independientes que se pueden contradecir, un único lugar que cambia juntos los campos relacionados, y tests de las transiciones. Con un [sealed state]({{ "/es/glosario/sealed-state/" | relative_url }}) las transiciones son explícitas y el compilador verifica el manejo, pero cada campo compartido se duplica o se saca afuera.
- **Lo híbrido suele ser la respuesta real.** Las partes que conviven van planas; cada parte con variantes excluyentes tiene su propio tipo sealed. Una confirmación pendiente, por ejemplo, es "borrar" o "archivar" o nada, que es una propiedad sealed nullable adentro de un estado plano. Eso mantiene la seguridad donde los estados de verdad se excluyen, sin pagarla en todos lados.
- **Modelar la UI de una sola vez como estado, y después limpiarla.** Un diálogo de confirmación, o una navegación que pide el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}), puede ser un campo del estado que la UI muestra y después le pide al [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) que limpie. Sobrevive a la rotación y a la [muerte del proceso]({{ "/es/glosario/process-death/" | relative_url }}) y es fácil de testear, y por eso muchas veces se prefiere a un [channel]({{ "/es/glosario/channel/" | relative_url }}) de [eventos]({{ "/es/glosario/one-shot-event/" | relative_url }}).
- **Actualizar de forma [atómica]({{ "/es/glosario/atomicity/" | relative_url }}).** Un estado plano se actualiza copiando el valor actual. `_state.value = _state.value.copy(...)` lee y escribe en dos pasos, así que dos actualizaciones concurrentes se pueden pisar. [`update { it.copy(...) }`]({{ "/es/02-coroutines-flow/mutablestateflow-update/" | relative_url }}) reintenta hasta que el cambio se aplica sobre el último valor.
- **El modelo también afecta a Compose.** Cada [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}) compara los parámetros que recibe. Pasarle el estado plano entero a cada composable hace que todos dependan de todo; pasar solo los campos que cada uno necesita, y conservar como las mismas instancias las colecciones que no cambian al copiar, deja que Compose se saltee el resto.

### Regla de decisión

| Pantalla | Modelo recomendado |
|----------|--------------------|
| Flujo simple (cargar → mostrar → error) | [Sealed interface]({{ "/es/glosario/sealed-interface/" | relative_url }}) |
| Pantalla compleja (búsqueda + filtros + selección + formularios) | [Flat data class]({{ "/es/glosario/flat-data-class/" | relative_url }}) |
| Partes compartidas más algunas variantes excluyentes | Híbrido: [flat data class]({{ "/es/glosario/flat-data-class/" | relative_url }}) con propiedades sealed |

## Code in Action

```kotlin
// Not found in FAS — standalone example
// Sealed state for a screen whose states truly exclude each other.
sealed interface DetailState {
    data object Loading : DetailState
    data class Success(val task: Task) : DetailState
    data class Error(val message: String) : DetailState
}

@Composable
fun DetailScreen(state: DetailState) {
    when (state) {                       // no else: a new subtype will not compile until handled
        DetailState.Loading -> Loader()
        is DetailState.Success -> TaskDetail(state.task)
        is DetailState.Error -> ErrorMessage(state.message)
    }
}

// From FollowApp Suite — TasksUiState.kt
// Flat data class for a screen whose concerns overlap: loading, search,
// selection and the form coexist. Derived properties replace flags that could
// contradict each other.
data class TasksUiState(
    val isLoading: Boolean = true,
    val activeTasks: List<Task> = emptyList(),
    @StringRes val errorMessageRes: Int? = null,
    val isFormVisible: Boolean = false,
    val searchQuery: String = "",
    val isSearchActive: Boolean = false,
    // ... 30+ properties that coexist
    val pendingCascadeAction: CascadeAction? = null,
    val selectedTaskIds: Set<String> = emptySet(),
) {
    val isSelectionMode: Boolean get() = selectedTaskIds.isNotEmpty()
}

// From FollowApp Suite — TasksUiState.kt
// The hybrid part: a confirmation is either Complete, Archive or Delete, never
// two at once, so it is a sealed type. It lives in the flat state as a nullable
// property: null means no dialog.
sealed class CascadeAction {
    abstract val taskId: String
    abstract val childCount: Int

    data class Complete(override val taskId: String, val isCompleted: Boolean, override val childCount: Int) : CascadeAction()
    data class Archive(override val taskId: String, override val childCount: Int) : CascadeAction()
    data class Delete(override val taskId: String, override val childCount: Int) : CascadeAction()
}

// From FollowApp Suite — TasksViewModel.kt
// The dialog is state: setting the property shows it, clearing it hides it.
// The when over the sealed type must handle every action.
fun onCascadeConfirmed() {
    val action = _uiState.value.pendingCascadeAction ?: return
    _uiState.update { it.copy(pendingCascadeAction = null) }
    viewModelScope.launch {
        when (action) {
            is CascadeAction.Complete -> {
                quickCompleteTaskUseCase(taskId = action.taskId, isCompleted = action.isCompleted, cascade = true)
            }
            is CascadeAction.Archive -> {
                archiveTaskUseCase(action.taskId, cascade = true)
                onFormDismissed()
            }
            is CascadeAction.Delete -> {
                moveTaskToTrashUseCase(action.taskId, cascade = true)
                onFormDismissed()
            }
        }
    }
}

fun onCascadeDismissed() {
    _uiState.update { it.copy(pendingCascadeAction = null) }
}
```

## The Interview (En el banquillo)

**Pregunta**: Tu equipo está construyendo una pantalla de gestión de tareas con búsqueda, filtros, selección múltiple, edición en línea y un indicador de carga. Un compañero propone modelar el UI state como `sealed interface TasksState { Loading, Loaded, Error }`. ¿Qué recomendás y por qué?

**Respuesta Senior**: Usaría una [flat data class]({{ "/es/glosario/flat-data-class/" | relative_url }}) para esta pantalla, con tipos sealed solo para las partes que de verdad son excluyentes. Un [sealed state]({{ "/es/glosario/sealed-state/" | relative_url }}) supone que la pantalla está en exactamente un estado a la vez, pero acá las preocupaciones se superponen: el usuario puede buscar mientras los datos están cargados, seleccionar tareas con un filtro activo, y ver un error no bloqueante mientras la lista sigue visible. Con `Loading / Loaded / Error`, la búsqueda, la selección y los filtros tendrían que copiarse en cada subtipo, o se perderían en cada transición: un refresco que pasa a [`Loading`]({{ "/es/glosario/loading-state/" | relative_url }}) borraría la búsqueda. Una [flat data class]({{ "/es/glosario/flat-data-class/" | relative_url }}) deja que cada preocupación cambie de forma independiente con [`copy()`]({{ "/es/glosario/copy/" | relative_url }}) adentro de [`update { }`]({{ "/es/02-coroutines-flow/mutablestateflow-update/" | relative_url }}). El precio es que el compilador ya no impide las combinaciones imposibles, así que evito flags independientes que se puedan contradecir, prefiero propiedades derivadas, y testeo las transiciones. Donde la pantalla sí tiene variantes excluyentes, como una confirmación pendiente que es borrar o archivar, modelo esa parte como un tipo sealed adentro del estado plano. Un [sealed state]({{ "/es/glosario/sealed-state/" | relative_url }}) para toda la pantalla es la opción correcta para pantallas más simples con un flujo claro de carga, contenido o error, como una página de detalle.

**Pregunta**: El [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) necesita que el usuario confirme una acción destructiva antes de ejecutarla. ¿Cómo lo modelás en el UI state?

**Respuesta Senior**: Como estado, con una propiedad nullable que guarda lo que está pendiente: `pendingAction: ConfirmAction? = null`. Si hay varios tipos de acción, `ConfirmAction` es un tipo sealed, porque una confirmación pendiente es exactamente uno de ellos. Cuando el usuario inicia la acción, el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) setea la propiedad y la UI muestra el diálogo porque el valor no es [null]({{ "/es/glosario/null/" | relative_url }}). Confirmar llama al [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}), que limpia la propiedad y ejecuta la acción con un [`when`]({{ "/es/glosario/when-expression/" | relative_url }}) sobre el tipo sealed, así que no se puede agregar un tipo de acción nuevo sin manejarlo. Cancelar solo la limpia. Modelarlo como estado en lugar de un [evento]({{ "/es/glosario/one-shot-event/" | relative_url }}) de una sola vez significa que el diálogo sobrevive a una rotación, y con [estado guardado]({{ "/es/glosario/saved-instance-state/" | relative_url }}) incluso a la [muerte del proceso]({{ "/es/glosario/process-death/" | relative_url }}); no se puede entregar dos veces ni perderse mientras la pantalla está en background; y un test solo tiene que revisar el estado después de cada llamada. La UI sigue siendo una función del estado, que es justamente el sentido de un único estado con [unidirectional data flow]({{ "/es/glosario/unidirectional-data-flow/" | relative_url }}).

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
