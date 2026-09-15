---
layout: page
title: "Structured Concurrency"
lang: es
permalink: /es/02-coroutines-flow/structured-concurrency/
order: 3
---

## The Theory (El Qué)

Structured Concurrency (concurrencia estructurada) es la regla de que **toda [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) tiene un padre, y un padre no termina hasta que terminaron todos sus hijos**. Una coroutine nunca es un [thread]({{ "/es/glosario/thread/" | relative_url }}) suelto que arrancás y olvidás: es un nodo de un árbol cuya raíz es un [`CoroutineScope`]({{ "/es/glosario/coroutine-scope/" | relative_url }}), y ese árbol es lo que el [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) usa para propagar tres cosas — **completitud, cancelación y fallo**.

El árbol está hecho de [`Job`]({{ "/es/glosario/job/" | relative_url }})s. Cuando llamás a [`launch`]({{ "/es/glosario/launch/" | relative_url }}) o [`async`]({{ "/es/glosario/async/" | relative_url }}) sobre un scope, el [`Job`]({{ "/es/glosario/job/" | relative_url }}) de la coroutine nueva se cuelga como hijo del [`Job`]({{ "/es/glosario/job/" | relative_url }}) que está en el [`CoroutineContext`]({{ "/es/glosario/coroutine-context/" | relative_url }}) del scope. De ese enlace salen las cuatro garantías:

- **Espera**: un [`Job`]({{ "/es/glosario/job/" | relative_url }}) padre queda en estado *Completing* hasta que todos sus hijos terminan. [`coroutineScope { }`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) y [`supervisorScope { }`]({{ "/es/glosario/supervisor-scope/" | relative_url }}) lo hacen visible: la [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) no retorna hasta que terminó el bloque *y todo lo que se lanzó adentro*.
- **La cancelación fluye hacia abajo**: cancelar un padre cancela a todos sus hijos, recursivamente. Cancelar [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) en [`onCleared()`]({{ "/es/glosario/on-cleared/" | relative_url }}) cancela cada [collector]({{ "/es/glosario/collector/" | relative_url }}) y cada escritura puntual que el ViewModel haya lanzado.
- **El fallo fluye hacia arriba**: con un [`Job`]({{ "/es/glosario/job/" | relative_url }}) común, una excepción no capturada en un hijo cancela al padre, que a su vez cancela a los *hermanos*, y después la excepción sigue subiendo. Con un [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) — o dentro de [`supervisorScope { }`]({{ "/es/glosario/supervisor-scope/" | relative_url }}) — el fallo se detiene en el hijo: los hermanos sobreviven y la excepción va a un [`CoroutineExceptionHandler`]({{ "/es/glosario/coroutine-exception-handler/" | relative_url }}).
- **Sin leaks**: como nada puede sobrevivir a su padre, ningún trabajo puede seguir corriendo en silencio después de que desapareció la pantalla, el ViewModel o el request que lo inició.

Dos builders permiten crear un *subárbol* dentro de código suspend secuencial. [`coroutineScope { }`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) crea un scope hijo, corre el bloque, suspende hasta que todos los hijos terminan, y relanza el primer fallo después de cancelar al resto. [`supervisorScope { }`]({{ "/es/glosario/supervisor-scope/" | relative_url }}) es lo mismo pero con semántica de supervisor: un hijo que falla no cancela a sus hermanos. Ninguno de los dos crea un [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) ni un [thread]({{ "/es/glosario/thread/" | relative_url }}) nuevo — heredan el contexto y solo agregan un nodo [`Job`]({{ "/es/glosario/job/" | relative_url }}).

[`async`]({{ "/es/glosario/async/" | relative_url }}) es [`launch`]({{ "/es/glosario/launch/" | relative_url }}) con resultado: devuelve un [`Deferred<T>`]({{ "/es/glosario/deferred/" | relative_url }}) cuyo [`await()`]({{ "/es/glosario/await/" | relative_url }}) suspende hasta que el valor está listo. Una excepción dentro de [`async`]({{ "/es/glosario/async/" | relative_url }}) queda guardada en el [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) y se relanza en [`await()`]({{ "/es/glosario/await/" | relative_url }}) — pero *también* hace fallar al [`Job`]({{ "/es/glosario/job/" | relative_url }}) padre de inmediato, salvo que ese padre sea un supervisor.

La cancelación es [cooperativa]({{ "/es/glosario/cooperative-cancellation/" | relative_url }}). Cancelar un [`Job`]({{ "/es/glosario/job/" | relative_url }}) levanta una bandera; la coroutine realmente se detiene en su próximo [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}), donde el [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) lanza una [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}). Toda suspend function de `kotlinx.coroutines` revisa esa bandera; un loop de CPU sin suspensión no lo hace, y tiene que llamar a [`ensureActive()`]({{ "/es/glosario/ensure-active/" | relative_url }}) o revisar [`isActive`]({{ "/es/glosario/is-active/" | relative_url }}) por su cuenta. [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}) es la única excepción que Structured Concurrency trata como *terminación normal*: no hace fallar al padre y no llega a un [`CoroutineExceptionHandler`]({{ "/es/glosario/coroutine-exception-handler/" | relative_url }}).

## The Senior Perspective (El Porqué)

- **El árbol es el contrato que hace que cancelar sea gratis.** Antes de Structured Concurrency, cancelar una operación implicaba pasar una bandera por cada [callback]({{ "/es/glosario/callbacks/" | relative_url }}) y confiar en que cada capa la respetara. Con el árbol de [`Job`]({{ "/es/glosario/job/" | relative_url }})s, un solo `cancel()` en la raíz llega a cada hoja, incluidas las coroutines lanzadas tres capas más abajo en un repositorio que no escribiste vos. Por eso [`GlobalScope`]({{ "/es/glosario/global-scope/" | relative_url }}) y un `CoroutineScope(...)` sin dueño son un olor: desprenden un subárbol de toda raíz que pudiera cancelarlo, y cualquier [memory leak]({{ "/es/glosario/memory-leaks/" | relative_url }}) que causen es invisible hasta producción.
- **[`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) convierte "disparar N escrituras" en "disparar N escrituras *y esperarlas a todas*".** Hacer un loop de [`launch`]({{ "/es/glosario/launch/" | relative_url }}) directo sobre [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) arranca N hijos independientes y la función que llama retorna al instante. Envolver el mismo loop en [`coroutineScope { }`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) hace que la coroutine que lo contiene *suspenda* hasta que aterriza la última escritura. Esa única palabra es la diferencia entre "puedo correr un [`finally`]({{ "/es/glosario/finally/" | relative_url }}) después del batch" y "no tengo idea de cuándo terminó el batch".
- **Elegí [`Job`]({{ "/es/glosario/job/" | relative_url }}) vs [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) preguntándote si los hijos son una sola unidad de trabajo o unidades independientes.** Traer en paralelo el header, la lista y el footer de una pantalla es una sola unidad: si falla cualquier parte, la pantalla no puede renderizar, así que un [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) común que cancele a los hermanos es lo correcto. Un [`@Singleton`]({{ "/es/glosario/singleton-scope/" | relative_url }}) que corre un listener de billing y otro de consentimiento tiene unidades independientes: que muera uno no debe tirar al otro, así que necesita un [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}). [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) es supervisor porque cada [`launch`]({{ "/es/glosario/launch/" | relative_url }}) desde un evento de UI es independiente de los demás.
- **Un campo `Job?` es un scope hecho a mano, y necesita la misma disciplina.** Guardar `subtasksJob: Job?` para cancelar el [collector]({{ "/es/glosario/collector/" | relative_url }}) anterior antes de arrancar el siguiente es la herramienta correcta para "solo uno de estos a la vez". La disciplina es que *todo* camino que termina el estado dueño — cerrar, confirmar, cambiar de item — tiene que cancelarlo, o el [collector]({{ "/es/glosario/collector/" | relative_url }}) viejo sigue escribiendo datos obsoletos en el estado. El [`Job`]({{ "/es/glosario/job/" | relative_url }}) sigue siendo hijo de [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}), así que el peor caso es un [collector]({{ "/es/glosario/collector/" | relative_url }}) desperdiciado hasta [`onCleared()`]({{ "/es/glosario/on-cleared/" | relative_url }}), no un leak.
- **Tragarse una [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}) rompe el árbol.** Un `catch (e: Exception)` alrededor de una llamada suspend atrapa también la [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}). Si la logueás y seguís, la coroutine está cancelada pero sigue corriendo, su padre la espera, y la pantalla a la que pertenece no puede terminar de desmontarse. La regla: relanzala — `if (e is CancellationException) throw e` — o atrapá tipos más específicos. El caso raro y legítimo para atraparla es cuando la excepción *no* vino de la cancelación de tu propio [`Job`]({{ "/es/glosario/job/" | relative_url }}), y ahí [`isActive`]({{ "/es/glosario/is-active/" | relative_url }}) es la comprobación que distingue los dos casos.
- **[`async`]({{ "/es/glosario/async/" | relative_url }}) es para valores, [`launch`]({{ "/es/glosario/launch/" | relative_url }}) es para efectos — y la semántica de fallo difiere.** Un fallo en [`launch`]({{ "/es/glosario/launch/" | relative_url }}) lo maneja el árbol o el [`CoroutineExceptionHandler`]({{ "/es/glosario/coroutine-exception-handler/" | relative_url }}). Un fallo en [`async`]({{ "/es/glosario/async/" | relative_url }}) *además* queda guardado en el [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}), así que un `try/catch` alrededor de [`await()`]({{ "/es/glosario/await/" | relative_url }}) dentro de un [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) común no alcanza: para cuando lo atrapás, el padre ya fue cancelado. Si querés atrapar el fallo de un [`async`]({{ "/es/glosario/async/" | relative_url }}) y conservar los otros, el padre tiene que ser [`supervisorScope`]({{ "/es/glosario/supervisor-scope/" | relative_url }}).
- **Structured Concurrency es lo que hace testeables a las coroutines.** [`runTest`]({{ "/es/glosario/run-test/" | relative_url }}) es un [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}): hace fallar el test si un hijo sigue corriendo cuando termina el bloque, que es exactamente el bug de coroutine filtrada que el árbol está diseñado para exponer. Un test que necesita [`advanceUntilIdle()`]({{ "/es/glosario/advance-until-idle/" | relative_url }}) y aun así se cuelga te está diciendo que algo se lanzó en un scope que [`runTest`]({{ "/es/glosario/run-test/" | relative_url }}) no controla.

## Code in Action

### `coroutineScope` — escrituras paralelas que el llamador espera

Completar tareas en bloque corre una escritura por tarea en paralelo. La coroutine que lo contiene necesita saber cuándo terminaron *todas* para bajar la bandera `isBulkWriteInFlight` que suprime las emisiones intermedias. [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) es lo que le da sentido al [`finally`]({{ "/es/glosario/finally/" | relative_url }}).

```kotlin
// From FollowApp Suite — TasksViewModel.kt
updateSelectedTasksOptimistically { it.copy(isCompleted = isCompleted) }
isBulkWriteInFlight = true
try {
    kotlinx.coroutines.coroutineScope {
        ids.forEach { launch { quickCompleteTaskUseCase(taskId = it, isCompleted = isCompleted) } }
    }
} finally {
    isBulkWriteInFlight = false
}
```

Sin el wrapper [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}), el `forEach` lanzaría N hijos directo sobre [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) y caería al [`finally`]({{ "/es/glosario/finally/" | relative_url }}) de inmediato — la bandera bajaría con escrituras todavía en vuelo. Con él, el bloque suspende hasta que termina el último [`launch`]({{ "/es/glosario/launch/" | relative_url }}). Si una escritura lanza una excepción, las escrituras hermanas se cancelan y la excepción sale del `try`, y el [`finally`]({{ "/es/glosario/finally/" | relative_url }}) corre igual: la bandera se resetea en todos los caminos.

La misma forma aparece dos veces más en el archivo, con el razonamiento explícito en el comentario:

```kotlin
// From FollowApp Suite — TasksViewModel.kt
viewModelScope.launch {
    isBulkWriteInFlight = true
    try {
        // Writes run in parallel; coroutineScope waits for all of them
        // so emissions stay suppressed until the final state is persisted
        kotlinx.coroutines.coroutineScope {
            selected.forEach { task ->
                launch {
                    // ... compute updated tags for this task
                    if (updated.isEmpty()) {
                        removeLabelAssignmentUseCase(task.id, "labels")
                    } else {
                        applyLabelAssignmentUseCase(task.id, "labels", LabelValue.Tag(updated))
                    }
                }
            }
        }
    } finally {
        isBulkWriteInFlight = false
    }
}
```

### Donde falta el wrapper — y qué cambia

El camino de la acción en bloque confirmada lanza el mismo tipo de escrituras *sin* [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}):

```kotlin
// From FollowApp Suite — TasksViewModel.kt
viewModelScope.launch {
    when (action) {
        is BulkAction.Complete -> {
            ids.forEach { launch { quickCompleteTaskUseCase(taskId = it, isCompleted = action.isCompleted, cascade = true) } }
        }
        is BulkAction.Archive -> {
            ids.forEach { launch { archiveTaskUseCase(it, cascade = true) } }
            onExitSelection()
        }
        is BulkAction.Delete -> {
            executeBulkDelete()
        }
    }
}
```

Esto sigue siendo estructurado: cada [`launch`]({{ "/es/glosario/launch/" | relative_url }}) interno es hijo del externo, que es hijo de [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}). La coroutine externa no termina hasta que terminan los hijos, y limpiar el ViewModel los cancela a todos. Lo *distinto* es que `onExitSelection()` corre antes de que aterricen los archivados — el código después del loop no espera. Acá eso es intencional: salir del modo selección no debería esperar a la base de datos. El punto es que [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) no es "la forma correcta"; es la forma de decir *esperá acá*, y omitirlo dice *no esperes*.

### Un campo `Job?` para "un solo collector a la vez"

Editar una tarea transmite sus hijos directos al formulario. Solo puede existir un stream de estos, así que el anterior se cancela antes de arrancar el siguiente — y en cada camino que cierra el formulario.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Streams the direct children of the task being edited into the form.
// Cancelled whenever the form closes or switches task.
private var subtasksJob: Job? = null

fun startEditing(task: Task) {
    // ...
    subtasksJob?.cancel()
    subtasksJob = viewModelScope.launch {
        getSubtasksUseCase(task.id)
            .catch { error -> Log.e(TAG, "Error loading subtasks", error) }
            .collect { subtasks ->
                _uiState.update { it.copy(form = it.form.copy(subtasks = subtasks)) }
            }
    }
}

fun onFormDismissed() {
    subtasksJob?.cancel()
    subtasksJob = null
    // ...
}
```

`cancel()` sobre el [`Job`]({{ "/es/glosario/job/" | relative_url }}) cancela solo ese subárbol: el [`collect`]({{ "/es/glosario/collect/" | relative_url }}) se detiene en su próximo [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}), el [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) de Room de abajo desregistra su observer, y nada más en [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) se ve afectado. Notá que `.catch` nunca ve la [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}) — el [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) enruta la cancelación por fuera de él, así que la línea de log es solo para errores reales.

### Relanzar `CancellationException` — con un giro

El auto-scroll durante el drag-to-reorder corre dentro de un [`LaunchedEffect`]({{ "/es/glosario/launched-effect/" | relative_url }}), cuya coroutine es hija de la composición. [`scrollBy`]({{ "/es/glosario/scroll-by/" | relative_url }}) puede ser cancelado por *otra* mutación de scroll sobre la misma lista, lo que lanza una [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}) aunque el efecto en sí siga vivo.

```kotlin
// From FollowApp Suite — TasksScreen.kt
LaunchedEffect(reorderState.autoScrollDirection) {
    val direction = reorderState.autoScrollDirection
    while (direction != 0) {
        if (direction > 0 && !lazyListState.canScrollForward) break
        if (direction < 0 && !lazyListState.canScrollBackward) break
        try {
            lazyListState.scrollBy(direction * autoScrollStep)
        } catch (e: CancellationException) {
            // Preempted by another scroll mutation (e.g. the
            // reorder re-anchor); keep scrolling unless the
            // effect itself was cancelled
            if (!isActive) throw e
        }
        reorderState.onAutoScrolled()
        withFrameNanos { }
    }
}
```

Esta es la única forma legítima de atrapar una [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}): el código distingue *"mi [`Job`]({{ "/es/glosario/job/" | relative_url }}) fue cancelado"* (`isActive == false` → relanzar, para que el árbol complete) de *"una operación interna fue interrumpida"* (`isActive == true` → seguir). Tragársela incondicionalmente dejaría una coroutine cancelada loopeando hasta que el próximo `withFrameNanos` revisara la bandera por casualidad.

### La raíz del árbol: un scope que nunca se cancela

```kotlin
// From FollowApp Suite — PremiumRepositoryImpl.kt
private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

init {
    scope.launch {
        billingConnector.isOwned
            .filterNotNull()
            .collect { owned -> premiumPreferences.setAdsRemoved(owned) }
    }
}
```

Todo árbol necesita una raíz, y un [`@Singleton`]({{ "/es/glosario/singleton-scope/" | relative_url }}) es una raíz legítima: su vida *es* el proceso. El [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) es la decisión de Structured Concurrency acá — el repositorio puede sumar un segundo [collector]({{ "/es/glosario/collector/" | relative_url }}), y los dos son unidades de trabajo independientes.

### `async` — Not found in FAS

FAS nunca necesita *devolver* dos valores calculados en paralelo, así que [`async`]({{ "/es/glosario/async/" | relative_url }}) no aparece. La forma canónica, y la semántica de fallo que van a preguntar en la entrevista:

```kotlin
// Not found in FAS — standalone example
suspend fun loadDashboard(): Dashboard = coroutineScope {
    val header = async { api.header() }
    val items = async { api.items() }
    Dashboard(header.await(), items.await())   // either failure cancels the other and rethrows
}

suspend fun loadDashboardLenient(): Dashboard = supervisorScope {
    val header = async { api.header() }
    val items = async { api.items() }
    Dashboard(
        header = runCatching { header.await() }.getOrNull(),   // one failing part does not cancel the other
        items = runCatching { items.await() }.getOrDefault(emptyList())
    )
}
```

En la primera versión un `try/catch` alrededor de `header.await()` sería inútil: para cuando [`await()`]({{ "/es/glosario/await/" | relative_url }}) relanza, el [`async`]({{ "/es/glosario/async/" | relative_url }}) ya hizo fallar al [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) e `items` está cancelado. Solo [`supervisorScope`]({{ "/es/glosario/supervisor-scope/" | relative_url }}) hace posible la recuperación por hijo.

## The Interview (En el banquillo)

**Pregunta**: ¿Qué es Structured Concurrency, y qué garantías concretas te da que un thread suelto o un [`GlobalScope.launch`]({{ "/es/glosario/global-scope/" | relative_url }}) no te dan?

**Respuesta Senior**: Structured Concurrency es la regla de que toda [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) es hija de un [`Job`]({{ "/es/glosario/job/" | relative_url }}) del scope que la lanzó, así que todas las coroutines forman un árbol con raíz en un [`CoroutineScope`]({{ "/es/glosario/coroutine-scope/" | relative_url }}). El árbol da cuatro garantías. Un padre no termina hasta que terminan sus hijos — así que un [`coroutineScope { }`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) alrededor de un loop de [`launch`]({{ "/es/glosario/launch/" | relative_url }}) significa "esperalos a todos", y un [`finally`]({{ "/es/glosario/finally/" | relative_url }}) después corre cuando el batch realmente terminó. La cancelación se propaga hacia abajo — un `cancel()` sobre [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) llega a cada [collector]({{ "/es/glosario/collector/" | relative_url }}), incluidos los lanzados por código que no es mío. El fallo se propaga hacia arriba — un hijo que lanza cancela a su padre y hermanos bajo un [`Job`]({{ "/es/glosario/job/" | relative_url }}) común, o queda aislado en ese hijo bajo un [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) o [`supervisorScope`]({{ "/es/glosario/supervisor-scope/" | relative_url }}). Y nada puede sobrevivir a su padre, que es lo que previene los leaks. [`GlobalScope.launch`]({{ "/es/glosario/global-scope/" | relative_url }}) y un [`Thread`]({{ "/es/glosario/thread/" | relative_url }}) suelto no dan nada de esto: desprenden el trabajo de cualquier raíz que pudiera cancelarlo o esperarlo, una excepción adentro es invisible para el llamador, y un test no puede saber cuándo terminaron. El trade-off que mencionaría es que la cancelación es [cooperativa]({{ "/es/glosario/cooperative-cancellation/" | relative_url }}): solo tiene efecto en un [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}), así que un loop de CPU puro tiene que revisar [`isActive`]({{ "/es/glosario/is-active/" | relative_url }}) o llamar a [`ensureActive()`]({{ "/es/glosario/ensure-active/" | relative_url }}), y atrapar una [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}) sin relanzarla rompe el árbol en silencio — la coroutine sigue corriendo mientras su padre la espera.

**Pregunta**: Necesitás correr N escrituras a la base de datos en paralelo y después actualizar una bandera cuando terminaron todas. Mostrame la forma, y decime qué pasa si una escritura lanza una excepción.

**Respuesta Senior**: Dentro de una coroutine sobre [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}), levanto la bandera, envuelvo el loop en [`coroutineScope { ids.forEach { launch { write(it) } } }`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) dentro de un `try`, y bajo la bandera en el [`finally`]({{ "/es/glosario/finally/" | relative_url }}). [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) crea un [`Job`]({{ "/es/glosario/job/" | relative_url }}) hijo al que se cuelga cada [`launch`]({{ "/es/glosario/launch/" | relative_url }}), y suspende hasta que todos los hijos terminan — así que la línea que sigue, y el [`finally`]({{ "/es/glosario/finally/" | relative_url }}), corren solo cuando aterrizó la última escritura. Sin el wrapper, los [`launch`]({{ "/es/glosario/launch/" | relative_url }}) se cuelgan directo de [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) y el `forEach` retorna al instante: la bandera bajaría con escrituras todavía en vuelo. Si una escritura lanza, [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) cancela a los hermanos restantes, espera a que terminen de cancelarse, y relanza la excepción original fuera del bloque — el [`finally`]({{ "/es/glosario/finally/" | relative_url }}) corre igual, así que la bandera queda consistente, y la excepción sigue hasta el [`launch`]({{ "/es/glosario/launch/" | relative_url }}) externo, donde el [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) de [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) evita que cancele las otras coroutines del ViewModel pero, sin [`CoroutineExceptionHandler`]({{ "/es/glosario/coroutine-exception-handler/" | relative_url }}), crashea la app. Si el requisito fuera en cambio "escribí las que puedas y reportá los fallos", cambiaría a [`supervisorScope`]({{ "/es/glosario/supervisor-scope/" | relative_url }}) para que un fallo no cancele a los otros, y juntaría los resultados con [`async`]({{ "/es/glosario/async/" | relative_url }}) más `runCatching { await() }` por hijo. Lo único que nunca haría es un `catch (e: Exception)` dentro del hijo sin relanzar la [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}), porque entonces cancelar el ViewModel ya no detendría el batch.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
