---
layout: page
title: "StateFlow"
lang: es
permalink: /es/02-coroutines-flow/stateflow/
order: 9
---

## The Theory (El Qué)

Un `StateFlow<T>` es un flow **[hot]({{ "/es/glosario/hot-stream/" | relative_url }})** (caliente) que siempre contiene exactamente un valor. Un [Flow]({{ "/es/02-coroutines-flow/flow-cold-streams/" | relative_url }}) [cold]({{ "/es/glosario/cold-stream/" | relative_url }}) es una receta que se ejecuta una vez por cada [collector]({{ "/es/glosario/collector/" | relative_url }}). Un `StateFlow` es un *contenedor*: existe y tiene un valor actual, lo colecte alguien o no.

Su contrato entra en cuatro reglas:

- **Siempre tiene un valor.** [`MutableStateFlow(initial)`]({{ "/es/glosario/mutable-state-flow/" | relative_url }}) exige un valor inicial, y `.value` lee el actual de forma sincrónica, desde cualquier [thread]({{ "/es/glosario/thread/" | relative_url }}), sin suspender y sin colectar.
- **Un [collector]({{ "/es/glosario/collector/" | relative_url }}) nuevo recibe el valor actual de inmediato**, y después cada cambio. Un [collector]({{ "/es/glosario/collector/" | relative_url }}) que llega tarde ve el presente, no la historia. Nunca se pierde "la primera emisión", porque siempre hay un valor actual para entregar.
- **Es conflated** (aplica [conflation]({{ "/es/glosario/conflation/" | relative_url }})). Solo importa el último valor. Si el valor cambia tres veces mientras un [collector]({{ "/es/glosario/collector/" | relative_url }}) lento está ocupado, el [collector]({{ "/es/glosario/collector/" | relative_url }}) recibe el último y se saltea los del medio. Escribir nunca suspende al que escribe: no hay [backpressure]({{ "/es/glosario/backpressure/" | relative_url }}).
- **Es distinto por igualdad.** Asignar un valor que es [`equals()`]({{ "/es/glosario/equals/" | relative_url }}) al actual no hace nada: no hay emisión y ningún [collector]({{ "/es/glosario/collector/" | relative_url }}) se despierta. [`distinctUntilChanged`]({{ "/es/glosario/distinct-until-changed/" | relative_url }}) viene incorporado.

La separación entre el tipo mutable y el de solo lectura sostiene la arquitectura. [`MutableStateFlow`]({{ "/es/glosario/mutable-state-flow/" | relative_url }}) expone un `value` escribible (más [`update`]({{ "/es/glosario/update/" | relative_url }}) y [`compareAndSet`]({{ "/es/glosario/compare-and-set/" | relative_url }})), y `StateFlow` es de solo lectura. La forma estándar es un [`MutableStateFlow`]({{ "/es/glosario/mutable-state-flow/" | relative_url }}) privado llamado `_uiState` dentro del [state holder]({{ "/es/glosario/state-holder/" | relative_url }}), expuesto como un `StateFlow` llamado `uiState` mediante [`asStateFlow()`]({{ "/es/glosario/as-state-flow/" | relative_url }}).

Dos propiedades más importan en la práctica:

- [`collect`]({{ "/es/glosario/collect/" | relative_url }}) sobre un `StateFlow` **nunca termina**. El stream no tiene fin, así que la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) que colecta corre hasta que se cancela su scope.
- Todos sus métodos son **[thread-safe]({{ "/es/glosario/thread-safety/" | relative_url }})**. Las escrituras desde cualquier [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) no necesitan sincronización extra. Aun así, un leer-modificar-escribir escrito como `value = value.copy(...)` sigue siendo dos operaciones y no una, y ese hueco es el que cierra [`update {}`]({{ "/es/glosario/update/" | relative_url }}). Tiene su propio tema.

Por dentro, un `StateFlow` es un [`SharedFlow`]({{ "/es/glosario/sharedflow/" | relative_url }}) especializado: reproduce un valor, aplica conflation y filtra los valores iguales. El [stream hot]({{ "/es/glosario/hot-stream/" | relative_url }}) general ([`SharedFlow`]({{ "/es/glosario/sharedflow/" | relative_url }})) y la conversión de un flow [cold]({{ "/es/glosario/cold-stream/" | relative_url }}) en un `StateFlow` ([`stateIn`]({{ "/es/glosario/state-in/" | relative_url }})) son temas de más adelante.

## The Senior Perspective (El Porqué)

- **StateFlow es para estado, no para eventos.** La [conflation]({{ "/es/glosario/conflation/" | relative_url }}) y el filtrado por igualdad son exactamente lo correcto para "qué tiene que mostrar la pantalla ahora". Son exactamente lo incorrecto para "mostrá este snackbar una vez" o "navegá". Dos mensajes de error idénticos seguidos colapsan en uno. Un evento de navegación guardado como estado se le entrega de nuevo a cada [collector]({{ "/es/glosario/collector/" | relative_url }}) nuevo, después de una rotación o de volver del background, así que se dispara dos veces salvo que alguien lo limpie. La solución idiomática es modelar el evento como estado que la UI confirma: el ítem pendiente vive en el estado de UI, y la UI avisa cuando ya lo manejó. Empujar eventos de "disparar y olvidar" a través de un contenedor diseñado para recordar no funciona.
- **La igualdad es la regla de emisión, así que el tipo del estado decide si es correcto.** Con una [`data class`]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}) inmutable, [`copy()`]({{ "/es/glosario/copy/" | relative_url }}) crea un valor nuevo y el [`equals()`]({{ "/es/glosario/equals/" | relative_url }}) generado compara contenido: los cambios reales emiten, los que no cambian nada no. Con un objeto mutable, mutarlo en el lugar y reasignar la *misma* referencia se compara igual a sí mismo, y la UI nunca se actualiza. Con una clase que no sobrescribe [`equals()`]({{ "/es/glosario/equals/" | relative_url }}), la comparación cae en la [igualdad referencial]({{ "/es/glosario/referential-equality/" | relative_url }}), así que cada instancia nueva emite aunque no haya cambiado nada. `StateFlow` asume en silencio [value semantics]({{ "/es/glosario/value-semantics/" | relative_url }}), y la [immutability]({{ "/es/glosario/immutability/" | relative_url }}) es lo que hace verdadera esa suposición. La misma regla protege el trabajo downstream: un `StateFlow` de parámetros de búsqueda que alimenta un [`flatMapLatest`]({{ "/es/glosario/flat-map-latest/" | relative_url }}) solo cancela y reinicia la query cuando los parámetros cambian de verdad.
- **El filtrado por igualdad también es una trampa para los triggers.** Un [`MutableStateFlow(true)`]({{ "/es/glosario/mutable-state-flow/" | relative_url }}) usado como señal de "refrescar" se dispara una vez y nunca más, porque cada escritura posterior es igual al valor actual. Un contador o un [timestamp]({{ "/es/glosario/timestamp/" | relative_url }}) lo esquivan haciendo que cada escritura sea distinta. Es un patrón legítimo, pero también es una señal para preguntarse si el trigger es realmente estado.
- **El valor inicial es una decisión de diseño, no boilerplate.** `StateFlow` te obliga a decidir qué muestra la pantalla antes de que llegue cualquier dato. Elegir [`emptyList()`]({{ "/es/glosario/empty-list/" | relative_url }}) hace indistinguibles "todavía cargando" y "realmente vacío", y así es como un mensaje de estado vacío parpadea en cada arranque en frío. Las opciones honestas son un flag `isLoading` explícito, un miembro `Loading` en un estado sellado, o un valor nullable donde `null` significa "todavía desconocido". Cada una convierte la ausencia de datos en un estado en vez de una mentira.
- **[Hot]({{ "/es/glosario/hot-stream/" | relative_url }}) significa que sobrevive a sus collectors, así que el [lifecycle]({{ "/es/glosario/lifecycle/" | relative_url }}) es trabajo del [collector]({{ "/es/glosario/collector/" | relative_url }}).** Un `StateFlow` conserva su valor con cero suscriptores, y eso es lo que permite que una pantalla rotada se redibuje al instante. El [collector]({{ "/es/glosario/collector/" | relative_url }}), en cambio, tiene que frenar cuando la UI no está visible. En [Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}), `collectAsState()` sigue colectando mientras la app está en background. [`collectAsStateWithLifecycle()`]({{ "/es/glosario/collect-as-state-with-lifecycle/" | relative_url }}) frena por debajo de `STARTED` y retoma el valor actual al volver. Para un [`MutableStateFlow`]({{ "/es/glosario/mutable-state-flow/" | relative_url }}) simple el costo es chico. Para un `StateFlow` alimentado por un [upstream]({{ "/es/glosario/upstream/" | relative_url }}) mediante [`stateIn`]({{ "/es/glosario/state-in/" | relative_url }}) con [`WhileSubscribed`]({{ "/es/glosario/while-subscribed/" | relative_url }}), el [collector]({{ "/es/glosario/collector/" | relative_url }}) [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}) es lo único que le permite a ese [upstream]({{ "/es/glosario/upstream/" | relative_url }}) detenerse.
- **El `.value` sincrónico es poderoso y fácil de usar mal.** Leer `.value` dentro del [state holder]({{ "/es/glosario/state-holder/" | relative_url }}) para tomar una decisión está bien. Leerlo desde la UI en vez de colectar significa que la UI nunca se entera de los cambios posteriores. Escribir `value = value.copy(...)` desde dos [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) a la vez es una [race condition]({{ "/es/glosario/race-condition/" | relative_url }}) que pierde una de las escrituras en silencio.
- **StateFlow vs [LiveData]({{ "/es/glosario/livedata/" | relative_url }}).** Los dos son contenedores observables, y las diferencias deciden la elección. `StateFlow` exige un valor inicial, filtra por igualdad, es [Kotlin]({{ "/es/glosario/kotlin/" | relative_url }}) puro (se puede testear sin [Android]({{ "/es/glosario/android/" | relative_url }}) y usar en cualquier capa) y funciona con todos los operadores de Flow. [LiveData]({{ "/es/glosario/livedata/" | relative_url }}) es [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}) por sí mismo y notifica en cada `setValue`, incluso con un valor igual. En código nuevo, la conciencia del [lifecycle]({{ "/es/glosario/lifecycle/" | relative_url }}) pasa al [collector]({{ "/es/glosario/collector/" | relative_url }}) ([`collectAsStateWithLifecycle`]({{ "/es/glosario/collect-as-state-with-lifecycle/" | relative_url }}), [`repeatOnLifecycle`]({{ "/es/glosario/repeat-on-lifecycle/" | relative_url }})), y `StateFlow` encaja mejor en todo lo demás.

## Code in Action

```kotlin
// De FollowApp Suite — TasksViewModel.kt
// El par canónico: mutable y privado adentro, de solo lectura afuera
private val _uiState = MutableStateFlow(TasksUiState())
val uiState: StateFlow<TasksUiState> = _uiState.asStateFlow()

// Los parámetros de la query también son estado. QueryParams es una data
// class, así que una escritura que no cambia nada (misma query, mismo orden)
// se descarta por igualdad y NO vuelve a ejecutar la query de abajo.
private val _queryParams = MutableStateFlow(
    QueryParams(
        query = "",
        filters = setOf(TaskStatus.ACTIVE),
        sort = ListSort.TITLE_ASC
    )
)

// Un StateFlow<Boolean> usado como compuerta: no se consulta nada hasta
// que se restauró la configuración de vista persistida
private val _restored = MutableStateFlow(false)

private fun observeTasks() {
    viewModelScope.launch {
        _restored
            .filter { it }
            .flatMapLatest { _queryParams }   // cada QueryParams distinto re-consulta
            .flatMapLatest { params -> /* getActiveTasksUseCase(params.sort) ... */ }
            .collect { /* ... */ }
    }
}

// De FollowApp Suite — TasksViewModel.kt
// Escribir desde Dispatchers.IO es seguro: MutableStateFlow es thread-safe.
// El comentario original lo dice explícitamente.
private fun restoreViewPreferences() {
    // ... IO bypasses that; MutableStateFlow
    // updates are already thread-safe.
    viewModelScope.launch(Dispatchers.IO) {
        val snapshot = runCatching { tasksViewPreferences.read() }.getOrNull()
        if (snapshot != null) {
            _queryParams.update { it.copy(sort = snapshot.sortOrder /* ... */) }
        }
        _restored.value = true   // abre la compuerta
    }
}

// De FollowApp Suite — TasksViewModel.kt
// Un trigger que tiene que dispararse en CADA apertura del formulario.
// Escribir `true` dos veces se descartaría por igualdad, así que cada
// escritura usa un timestamp nuevo para ser distinta.
private val _formOpenTrigger = MutableStateFlow(0L)

fun onFabClicked() {
    // ...
    _formOpenTrigger.value = System.currentTimeMillis()
}

// De FollowApp Suite — LabelsListViewModel.kt
// La misma idea con un contador: incrementarlo obliga a combine() a
// recalcular con el último catálogo y las últimas tareas tras una escritura fallida
private val _resyncTrigger = MutableStateFlow(0)

private fun resync() {
    _resyncTrigger.value++
}

// De FollowApp Suite — BillingConnector.kt
// El valor inicial es una decisión: null significa "Play todavía no respondió",
// y quien lo consume lo puede distinguir de un false real
private val _isOwned = MutableStateFlow<Boolean?>(null)
val isOwned: StateFlow<Boolean?> = _isOwned.asStateFlow()

// De FollowApp Suite — TasksScreen.kt
// Colección lifecycle-aware: frena por debajo de STARTED y retoma con el valor actual
val uiState by viewModel.uiState.collectAsStateWithLifecycle()

// De FollowApp Suite — SettingsScreen.kt
// El mismo codebase con collectAsState(): sigue colectando mientras la app
// está en background. Cuando consentManager es null, el fallback además crea
// un MutableStateFlow NUEVO en cada recomposición, lo que reinicia la colección.
val uiState by viewModel.uiState.collectAsState()
val privacyOptionsRequired by (consentManager?.privacyOptionsRequired ?: MutableStateFlow(false))
    .collectAsState()
```

## The Interview (En el banquillo)

**Pregunta**: ¿Por qué `StateFlow` es una mala opción para eventos de una sola vez, como una navegación o un snackbar, y qué hacés en su lugar?

**Respuesta Senior**: `StateFlow` está hecho para responder "qué es verdad ahora mismo", y sus dos comportamientos definitorios rompen los eventos. Primero, aplica [conflation]({{ "/es/glosario/conflation/" | relative_url }}) y filtra por igualdad: dos mensajes de snackbar idénticos seguidos colapsan en uno, y una ráfaga de eventos se puede saltear porque un [collector]({{ "/es/glosario/collector/" | relative_url }}) lento solo ve el último valor. Segundo, recuerda: el valor actual se le entrega a cada [collector]({{ "/es/glosario/collector/" | relative_url }}) nuevo, así que un evento de navegación que sigue guardado en el estado se vuelve a disparar después de una rotación o cuando la pantalla vuelve del background. El parche habitual, limpiar el valor después de leerlo, tiene condiciones de carrera y desparrama lógica de "consumir" por toda la UI. El enfoque que prefiero es dejar de tratarlo como evento y modelarlo como estado: el mensaje o el destino de navegación pendiente vive en el estado de UI, la UI lo muestra o navega, y después le avisa al ViewModel que lo confirmó, lo que lo saca del estado. Eso sobrevive a la rotación y a la muerte del proceso, y es trivial de testear. Cuando algo realmente es de "disparar y olvidar" y no se tiene que reproducir de nuevo, pertenece a otra primitiva (un [`Channel`]({{ "/es/glosario/channel/" | relative_url }}) o un [`SharedFlow`]({{ "/es/glosario/sharedflow/" | relative_url }}) sin replay), no a un contenedor diseñado para recordar.

**Pregunta**: Un ViewModel hace `_uiState.value = _uiState.value.also { it.tasks.add(newTask) }` y la lista en pantalla nunca se actualiza. ¿Qué está mal y cómo lo arreglás?

**Respuesta Senior**: `StateFlow` solo emite cuando el valor nuevo no es [`equals()`]({{ "/es/glosario/equals/" | relative_url }}) al actual. Acá `tasks` es una lista mutable que se muta en el lugar, y se vuelve a asignar el mismo objeto de estado, así que la comparación es entre un objeto y sí mismo y la escritura se descarta. Ningún [collector]({{ "/es/glosario/collector/" | relative_url }}) se despierta y [Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) nunca recompone. Encima, el "valor actual" del flow se cambió a sus espaldas, así que cualquier código que lea `.value` ve datos que nunca se emitieron. El arreglo es hacer el estado inmutable: una [`data class`]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}) con una `List` de solo lectura, actualizada con `copy(tasks = tasks + newTask)`. Eso produce una instancia nueva con contenido distinto, la igualdad detecta el cambio y la emisión ocurre. También reemplazaría el leer-y-asignar por `_uiState.update { it.copy(...) }`, porque `value = value.copy(...)` son dos operaciones separadas, y dos [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) haciéndolo a la vez pueden perder una escritura. La lección general es que `StateFlow` asume [value semantics]({{ "/es/glosario/value-semantics/" | relative_url }}): no puede detectar un cambio que no produce un valor nuevo y distinto.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
