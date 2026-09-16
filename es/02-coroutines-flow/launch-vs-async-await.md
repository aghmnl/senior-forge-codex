---
layout: page
title: "Launch vs Async/Await"
lang: es
permalink: /es/02-coroutines-flow/launch-vs-async-await/
order: 4
---

## The Theory (El Qué)

[`launch`]({{ "/es/glosario/launch/" | relative_url }}) y [`async`]({{ "/es/glosario/async/" | relative_url }}) son los dos coroutine builders que llamás sobre un [`CoroutineScope`]({{ "/es/glosario/coroutine-scope/" | relative_url }}). Los dos arrancan una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) hija colgada del [`Job`]({{ "/es/glosario/job/" | relative_url }}) del scope, los dos heredan el [`CoroutineContext`]({{ "/es/glosario/coroutine-context/" | relative_url }}) del scope, los dos aceptan un contexto adicional y un [`CoroutineStart`]({{ "/es/glosario/coroutine-start/" | relative_url }}). Difieren en exactamente una cosa: **qué te devuelven**.

- **[`launch`]({{ "/es/glosario/launch/" | relative_url }})** devuelve un [`Job`]({{ "/es/glosario/job/" | relative_url }}). La coroutine es un *efecto*: corre, y lo único que podés hacer con el handle es [`cancel()`]({{ "/es/glosario/cancel/" | relative_url }}), [`join()`]({{ "/es/glosario/join/" | relative_url }}) o ignorarlo. Su bloque devuelve `Unit`. Si el bloque lanza una excepción, es un *fallo no capturado* de la coroutine: se propaga al [`Job`]({{ "/es/glosario/job/" | relative_url }}) padre de inmediato, y si nada en el árbol lo maneja, al [`CoroutineExceptionHandler`]({{ "/es/glosario/coroutine-exception-handler/" | relative_url }}) — o el proceso crashea.
- **[`async`]({{ "/es/glosario/async/" | relative_url }})** devuelve un [`Deferred<T>`]({{ "/es/glosario/deferred/" | relative_url }}). La coroutine es un *cómputo*: su bloque devuelve `T`, y [`await()`]({{ "/es/glosario/await/" | relative_url }}) suspende al llamador hasta que ese valor existe. [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) extiende [`Job`]({{ "/es/glosario/job/" | relative_url }}), así que todo lo que te da [`launch`]({{ "/es/glosario/launch/" | relative_url }}) sigue ahí. Si el bloque lanza, la excepción queda *guardada* en el [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) y se relanza a quien llame a [`await()`]({{ "/es/glosario/await/" | relative_url }}) — **y**, salvo que el padre sea un supervisor, también hace fallar al [`Job`]({{ "/es/glosario/job/" | relative_url }}) padre en el momento en que ocurre, no en el momento del [`await()`]({{ "/es/glosario/await/" | relative_url }}).

[`await()`]({{ "/es/glosario/await/" | relative_url }}) es un [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}). No bloquea un [thread]({{ "/es/glosario/thread/" | relative_url }}); estaciona la coroutine que llama hasta que el [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) completa, y participa de la [cancelación]({{ "/es/glosario/cooperative-cancellation/" | relative_url }}) — cancelar la coroutine que espera lanza [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}) desde [`await()`]({{ "/es/glosario/await/" | relative_url }}). [`awaitAll()`]({{ "/es/glosario/await-all/" | relative_url }}) sobre una lista de [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) los espera a todos y devuelve los valores en orden; falla apenas falla *cualquiera*.

La decisión, entonces, no es "cuál es más rápido" — son la misma maquinaria — sino **¿necesito el valor?** Una secuencia de [suspend functions]({{ "/es/glosario/suspend-functions/" | relative_url }}) llamadas una tras otra no necesita ningún builder: `val a = fetchA(); val b = fetchB(a)` ya es secuencial y ya es estructurado. [`async`]({{ "/es/glosario/async/" | relative_url }}) existe para el caso en que dos cómputos son *independientes* y querés que se solapen: arrancá los dos, después esperá los dos.

[`CoroutineStart.LAZY`]({{ "/es/glosario/coroutine-start/" | relative_url }}) es la tercera variable: un `async(start = LAZY)` no corre hasta que alguien llama a [`await()`]({{ "/es/glosario/await/" | relative_url }}) o [`start()`]({{ "/es/glosario/start/" | relative_url }}). Convierte un [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) en un cómputo memoizado, cancelable y bajo demanda — útil, raro, y fácil de olvidar cuando un hijo lazy nunca se arranca y el padre espera para siempre.

## The Senior Perspective (El Porqué)

- **Elegí el builder por la pregunta del llamador, no por el trabajo del llamado.** "¿Pasó?" es [`launch`]({{ "/es/glosario/launch/" | relative_url }}). "¿Cuál es la respuesta?" es [`async`]({{ "/es/glosario/async/" | relative_url }}). Un ViewModel que reacciona a un click lanza — nadie espera un click. Una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) que arma una pantalla desde tres fuentes usa async — la función *es* su valor de retorno. Mezclarlos produce los dos olores clásicos: un [`async`]({{ "/es/glosario/async/" | relative_url }}) cuyo [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) se descarta (un [`launch`]({{ "/es/glosario/launch/" | relative_url }}) cuyo fallo ahora es invisible), y un [`launch`]({{ "/es/glosario/launch/" | relative_url }}) que escribe su resultado en una variable compartida para que alguien la lea (un [`async`]({{ "/es/glosario/async/" | relative_url }}) con un `await` artesanal y con race).
- **Nunca `async { }.await()` en la misma línea.** `async { fetch() }.await()` es `fetch()` con más allocations y peores stack traces. No agrega concurrencia, y confunde al lector haciéndole pensar que algo corre en paralelo. Lo mismo vale para [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}): cambiar de [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) es trabajo de [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}), no de [`async`]({{ "/es/glosario/async/" | relative_url }}).
- **[`async`]({{ "/es/glosario/async/" | relative_url }}) es siempre un hijo; un [`async`]({{ "/es/glosario/async/" | relative_url }}) suelto es un bug.** Como necesita un scope, [`async`]({{ "/es/glosario/async/" | relative_url }}) se llama casi siempre dentro de [`coroutineScope { }`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) o [`supervisorScope { }`]({{ "/es/glosario/supervisor-scope/" | relative_url }}). Llamar a `viewModelScope.async { }` desde una función común y devolver el [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) filtra un handle de coroutine fuera del ViewModel — el llamador ahora posee un pedazo del árbol del ViewModel. Encerrá el paralelismo dentro de una suspend function y devolvé el valor plano.
- **El camino de la excepción es adonde van las entrevistas.** Con [`launch`]({{ "/es/glosario/launch/" | relative_url }}), un fallo es un evento del árbol: padre cancelado (o no, bajo un [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }})), después handler, después crash. Con [`async`]({{ "/es/glosario/async/" | relative_url }}), un fallo es *a la vez* un evento del árbol y un valor guardado. Dentro de un [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) común, gana el evento del árbol: el [`async`]({{ "/es/glosario/async/" | relative_url }}) que falla cancela a sus hermanos antes de que llegues al [`try/catch`]({{ "/es/glosario/try-catch/" | relative_url }}) alrededor de [`await()`]({{ "/es/glosario/await/" | relative_url }}). Para que [`await()`]({{ "/es/glosario/await/" | relative_url }}) sea el *único* lugar donde aflora el fallo — y conservar vivos a los hermanos — el padre tiene que ser [`supervisorScope`]({{ "/es/glosario/supervisor-scope/" | relative_url }}). Un [`try/catch`]({{ "/es/glosario/try-catch/" | relative_url }}) alrededor de [`await()`]({{ "/es/glosario/await/" | relative_url }}) dentro de [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) no está mal, solo que no hace lo que su autor cree.
- **Paralelismo sin resultado sigue siendo [`launch`]({{ "/es/glosario/launch/" | relative_url }}).** N escrituras independientes que no devuelven nada son `coroutineScope { items.forEach { launch { write(it) } } }`. Agarrar [`async`]({{ "/es/glosario/async/" | relative_url }}) ahí porque "es paralelo" es el mismo error de categoría al revés: estarías creando N `Deferred<Unit>` y llamando a [`awaitAll()`]({{ "/es/glosario/await-all/" | relative_url }}) por valores que nunca usás. [`launch`]({{ "/es/glosario/launch/" | relative_url }}) dentro de [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) ya los espera a todos.
- **Un [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) es una promesa de un solo disparo, y eso tiene usos más allá de [`async`]({{ "/es/glosario/async/" | relative_url }}).** [`CompletableDeferred<T>`]({{ "/es/glosario/completable-deferred/" | relative_url }}) es un [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) que completás a mano. Es la forma idiomática de frenar una coroutine hasta un evento externo — un test que quiere mantener un repositorio "en vuelo" hasta que él lo diga, un puente desde un [callback]({{ "/es/glosario/callbacks/" | relative_url }}) de un solo disparo hacia código suspend. Es el [`CountDownLatch(1)`]({{ "/es/glosario/count-down-latch/" | relative_url }}) nativo de coroutines, con valor.
- **En los tests es donde aparece la diferencia.** Bajo [`runTest`]({{ "/es/glosario/run-test/" | relative_url }}), un [`launch`]({{ "/es/glosario/launch/" | relative_url }}) que falla hace fallar el test al final del bloque; un [`async`]({{ "/es/glosario/async/" | relative_url }}) que falla y nunca se espera *también* hace fallar el test — la excepción no se pierde, llega al padre. Si alguna vez ves un [`async`]({{ "/es/glosario/async/" | relative_url }}) cuyo resultado "no importaba", preguntá por qué no era un [`launch`]({{ "/es/glosario/launch/" | relative_url }}), y qué pasa con su error.

## Code in Action

### `launch` para un evento de UI: nadie espera un click

Confirmar el formulario de tarea dispara una cadena de escrituras. El llamador es un click handler en Main; no puede suspender y no necesita un resultado. Este es el [`launch`]({{ "/es/glosario/launch/" | relative_url }}) canónico.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
fun onFormConfirmed() {
    val state = _uiState.value
    // ... validation
    viewModelScope.launch {
        val taskId = if (state.editingTaskId == null) {
            createTaskUseCase(
                title = state.form.title,
                description = state.form.description,
                isCompleted = state.form.isCompleted,
                dueDate = state.form.dueDate
            ) // returns the new task ID
        } else {
            editTaskUseCase(/* ... */)
            state.editingTaskId
        }

        if (selectedLabels.isNotEmpty()) {
            applyLabelAssignmentUseCase(taskId = taskId, labelName = "labels", value = LabelValue.Tag(selectedLabels))
        }
    }
}
```

Notá que *dentro* del [`launch`]({{ "/es/glosario/launch/" | relative_url }}) el código es secuencial: `applyLabelAssignmentUseCase` necesita `taskId`, que devuelve `createTaskUseCase`. No hace falta [`async`]({{ "/es/glosario/async/" | relative_url }}) para una cadena de dependencias — las llamadas suspend planas, una tras otra, ya son correctas. El resultado de toda la operación no es un valor sino un efecto: el [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) de [Room]({{ "/es/glosario/room/" | relative_url }}) emite la tarea nueva y la UI se actualiza.

### `launch` devuelve un `Job`, y el `Job` es el handle

```kotlin
// From FollowApp Suite — TasksViewModel.kt
private var subtasksJob: Job? = null

subtasksJob?.cancel()
subtasksJob = viewModelScope.launch {
    getSubtasksUseCase(task.id)
        .catch { error -> Log.e(TAG, "Error loading subtasks", error) }
        .collect { subtasks -> _uiState.update { it.copy(form = it.form.copy(subtasks = subtasks)) } }
}
```

El valor de [`launch`]({{ "/es/glosario/launch/" | relative_url }}) no es el resultado de la coroutine — no hay ninguno — sino su [`Job`]({{ "/es/glosario/job/" | relative_url }}). Lo único que este código hace con él es [`cancel()`]({{ "/es/glosario/cancel/" | relative_url }}). Esa es toda la superficie de API para la que [`launch`]({{ "/es/glosario/launch/" | relative_url }}) está diseñado.

### Paralelo sin resultado: sigue siendo `launch`

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Writes run in parallel; coroutineScope waits for all of them
// so emissions stay suppressed until the final state is persisted
kotlinx.coroutines.coroutineScope {
    selected.forEach { task ->
        launch {
            applyLabelAssignmentUseCase(task.id, scaleName, LabelValue.Scale(value))
        }
    }
}
```

Son N coroutines corriendo concurrentemente, y *no* es un caso de [`async`]({{ "/es/glosario/async/" | relative_url }}): nadie necesita N valores de retorno. [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) ya espera a cada hijo. La versión con [`async`]({{ "/es/glosario/async/" | relative_url }}) + [`awaitAll()`]({{ "/es/glosario/await-all/" | relative_url }}) sería estrictamente más código para el mismo comportamiento.

### Donde encajaría `async` — Not found in FAS

FAS nunca devuelve dos valores calculados independientemente desde una suspend function, así que [`async`]({{ "/es/glosario/async/" | relative_url }}) no aparece en código de producción. El call site más cercano es esta comprobación secuencial, que hoy es correcta y se volvería candidata a [`async`]({{ "/es/glosario/async/" | relative_url }}) solo si los conteos fueran caros:

```kotlin
// From FollowApp Suite — TasksViewModel.kt
viewModelScope.launch {
    val anyChildren = ids.any { countActiveSubtasksUseCase(it) > 0 }
    // ...
}
```

`any` corta en el primer acierto, así que corre las queries del DAO de a una y se detiene en el primer hit. La forma paralela — y la forma estándar de [`async`]({{ "/es/glosario/async/" | relative_url }}) que van a pedir en la entrevista — es:

```kotlin
// Not found in FAS — standalone example
suspend fun anyHasChildren(ids: List<String>): Boolean = coroutineScope {
    ids.map { id -> async { countActiveSubtasksUseCase(id) > 0 } }
        .awaitAll()
        .any { it }
}
```

Trade-off dicho sin vueltas: la versión secuencial hace *menos* trabajo cuando la primera tarea tiene hijos; la paralela tiene *menor latencia* cuando la mayoría no. Ninguna es "correcta" sin medir — y para un puñado de queries indexadas de [Room]({{ "/es/glosario/room/" | relative_url }}) la diferencia es invisible.

### `Deferred` a mano: frenar una coroutine en un test

[`CompletableDeferred`]({{ "/es/glosario/completable-deferred/" | relative_url }}) es un [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) sin ningún [`async`]({{ "/es/glosario/async/" | relative_url }}) detrás. El fixture de test lo usa para congelar una lectura del repositorio hasta que el test decide dejarla pasar.

```kotlin
// From FollowApp Suite — FakeLabelRepository.kt
/** When set, getLabelsWithOptions suspends until completed — lets tests observe in-flight reloads. */
var loadGate: CompletableDeferred<Unit>? = null

override fun getLabelsWithOptions(): Flow<Map<Label, List<LabelOption>>> =
    flow.map {
        loadGate?.await()
        labels.associateWith { label -> options.filter { it.labelId == label.id }.sortedBy { it.sortOrder } }
    }
```

```kotlin
// From FollowApp Suite — LabelsListViewModelTest.kt
// Block the next catalog read so the reload stays in flight
labelRepo.loadGate = CompletableDeferred()

vm.onConfirmScaleOptionRename(option.id)
advanceUntilIdle()

// While the reload is suspended, the screen must NOT show the loading state
assertFalse(vm.uiState.value.isLoading)

// Release the reload and verify it still completes with fresh data
labelRepo.loadGate!!.complete(Unit)
advanceUntilIdle()
```

[`await()`]({{ "/es/glosario/await/" | relative_url }}) suspende al [collector]({{ "/es/glosario/collector/" | relative_url }}) exactamente como lo haría sobre un [`async`]({{ "/es/glosario/async/" | relative_url }}); `complete(Unit)` lo reanuda. El primer [`advanceUntilIdle()`]({{ "/es/glosario/advance-until-idle/" | relative_url }}) corre todo *hasta* la compuerta, que es lo que le permite al test afirmar un estado intermedio que de otro modo sería una race.

## The Interview (En el banquillo)

**Pregunta**: ¿Cuándo usás [`launch`]({{ "/es/glosario/launch/" | relative_url }}) y cuándo [`async`]({{ "/es/glosario/async/" | relative_url }})? ¿Cuál es la diferencia real, si los dos arrancan una coroutine?

**Respuesta Senior**: Son la misma maquinaria con una diferencia: qué devuelven. [`launch`]({{ "/es/glosario/launch/" | relative_url }}) devuelve un [`Job`]({{ "/es/glosario/job/" | relative_url }}) — un handle para cancelar o hacer join — y su bloque no produce valor; es para efectos, y los llamadores son típicamente puntos de entrada no suspendibles como un click handler en un ViewModel. [`async`]({{ "/es/glosario/async/" | relative_url }}) devuelve un [`Deferred<T>`]({{ "/es/glosario/deferred/" | relative_url }}), un [`Job`]({{ "/es/glosario/job/" | relative_url }}) que además lleva un resultado, y [`await()`]({{ "/es/glosario/await/" | relative_url }}) suspende hasta que ese resultado está listo; es para la única situación en que dos cómputos son independientes y quiero que se solapen — arrancar los dos, después esperar los dos, dentro de un [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) para que la función devuelva un valor plano y el paralelismo nunca se escape. La regla es "¿necesito el valor?", no "¿es paralelo?": N escrituras independientes sin resultado son [`launch`]({{ "/es/glosario/launch/" | relative_url }}) dentro de [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}), que ya las espera a todas, y una cadena de dependencias son llamadas suspend secuenciales sin ningún builder. Los dos olores son un [`async`]({{ "/es/glosario/async/" | relative_url }}) cuyo [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) nunca se espera — debió ser un [`launch`]({{ "/es/glosario/launch/" | relative_url }}) — y `async { }.await()` en una línea, que es una llamada a función con allocations extra. Donde esperaría la repregunta es en el fallo: un fallo de [`launch`]({{ "/es/glosario/launch/" | relative_url }}) se propaga por el árbol de inmediato; un fallo de [`async`]({{ "/es/glosario/async/" | relative_url }}) queda *a la vez* guardado en el [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) para [`await()`]({{ "/es/glosario/await/" | relative_url }}) *y* propagado al padre en el momento en que ocurre. Dentro de un [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) común gana la propagación — el hermano se cancela antes de que pueda atrapar nada en [`await()`]({{ "/es/glosario/await/" | relative_url }}) — así que el manejo de errores por hijo necesita [`supervisorScope`]({{ "/es/glosario/supervisor-scope/" | relative_url }}).

**Pregunta**: Tenés tres llamadas de red que producen tres partes de una pantalla. Dos son independientes; la tercera necesita el resultado de la primera. Escribí la forma, y decime qué pasa si falla la segunda.

**Respuesta Senior**: Una suspend function que devuelve el modelo armado, con un [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) como cuerpo. Adentro, `val a = async { fetchA() }` y `val b = async { fetchB() }` arrancan las dos llamadas independientes concurrentemente; después `val c = fetchC(a.await())` — una llamada secuencial plana, porque depende de `a`; después `Screen(a.await(), b.await(), c)`. Sin [`async`]({{ "/es/glosario/async/" | relative_url }}) para `c`: envolver una llamada dependiente en [`async`]({{ "/es/glosario/async/" | relative_url }}) y esperarla de inmediato no agrega nada. Si `fetchB` lanza, el [`async`]({{ "/es/glosario/async/" | relative_url }}) hace fallar a su [`Job`]({{ "/es/glosario/job/" | relative_url }}) padre — el [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) — de inmediato, lo que cancela a `a` si todavía corre y cancela a la coroutine que está en `fetchC`, y después relanza la excepción de `fetchB` fuera de la función una vez que los hijos terminaron de cancelarse. El llamador ve una sola excepción y ninguna pantalla a medio armar, que para "la pantalla no puede renderizar sin las tres" es el comportamiento que quiero. Si en cambio la parte `b` fuera opcional — un carrusel de recomendaciones que puede estar vacío — cambiaría el cuerpo a [`supervisorScope`]({{ "/es/glosario/supervisor-scope/" | relative_url }}) y envolvería solo `b.await()` en [`runCatching`]({{ "/es/glosario/run-catching/" | relative_url }}), así su fallo queda dentro de su [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) y `a` y `c` completan normalmente. En cualquier caso el manejo del fallo vive en [`await()`]({{ "/es/glosario/await/" | relative_url }}), no alrededor del bloque `async { }`, y la elección entre los dos scopes es una decisión de producto sobre si las partes son una sola unidad o unidades independientes — la misma pregunta que decide [`Job`]({{ "/es/glosario/job/" | relative_url }}) versus [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) en todos lados.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
