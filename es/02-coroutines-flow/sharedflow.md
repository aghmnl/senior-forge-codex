---
layout: page
title: "SharedFlow"
lang: es
permalink: /es/02-coroutines-flow/sharedflow/
order: 10
---

## The Theory (El Qué)

Un `SharedFlow<T>` es el [stream hot]({{ "/es/glosario/hot-stream/" | relative_url }}) general de [kotlinx.coroutines]({{ "/es/glosario/kotlinx-coroutines/" | relative_url }}). Tiene una sola fuente que **transmite cada emisión a todos los [collectors]({{ "/es/glosario/collector/" | relative_url }}) actuales**. Un [Flow]({{ "/es/02-coroutines-flow/flow-cold-streams/" | relative_url }}) [cold]({{ "/es/glosario/cold-stream/" | relative_url }}) ejecuta su productor una vez por cada [collector]({{ "/es/glosario/collector/" | relative_url }}). Un `SharedFlow`, en cambio, corre independientemente de sus [collectors]({{ "/es/glosario/collector/" | relative_url }}), y ellos se suscriben a lo que emita desde ese momento.

Se crea mutable, igual que un [StateFlow]({{ "/es/02-coroutines-flow/stateflow/" | relative_url }}): un [`MutableSharedFlow`]({{ "/es/glosario/mutable-shared-flow/" | relative_url }}) privado expuesto de solo lectura mediante [`asSharedFlow()`]({{ "/es/glosario/as-shared-flow/" | relative_url }}). Su constructor recibe tres parámetros, y definen todo su comportamiento:

- **`replay`** (por defecto `0`): cuántos valores pasados recibe un suscriptor nuevo en el momento en que se suscribe. Con `0`, un suscriptor que llega tarde solo ve lo que se emite después de que llegó.
- **`extraBufferCapacity`** (por defecto `0`): lugar extra, además de `replay`, para valores que los emisores rápidos ya enviaron y los suscriptores lentos todavía no tomaron.
- **`onBufferOverflow`** (por defecto `SUSPEND`): qué pasa cuando el buffer se llena. `SUSPEND` hace que [`emit`]({{ "/es/glosario/emit/" | relative_url }}) espere, `DROP_OLDEST` descarta el valor más viejo del buffer y `DROP_LATEST` descarta el nuevo. Las dos políticas de descarte requieren un buffer (`replay` o `extraBufferCapacity` mayor que cero).

Los valores entran con [`emit`]({{ "/es/glosario/emit/" | relative_url }}), una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) que espera cuando el buffer está lleno, o con [`tryEmit`]({{ "/es/glosario/try-emit/" | relative_url }}), que nunca suspende y devuelve `false` cuando el valor no entra. A diferencia de un [`StateFlow`]({{ "/es/02-coroutines-flow/stateflow/" | relative_url }}), un `SharedFlow` **no tiene valor actual, ni valor inicial, ni filtrado por igualdad**: emitir el mismo valor dos veces lo entrega dos veces. Su [`collect`]({{ "/es/glosario/collect/" | relative_url }}) **nunca termina**. El flow no tiene fin, así que la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) que colecta corre hasta que se cancela su scope.

[`StateFlow`]({{ "/es/02-coroutines-flow/stateflow/" | relative_url }}) es exactamente un `SharedFlow` con una configuración fija: `replay = 1`, `onBufferOverflow = DROP_OLDEST`, un valor inicial y [`distinctUntilChanged`]({{ "/es/glosario/distinct-until-changed/" | relative_url }}) incorporado. `SharedFlow` es lo que usás cuando esa configuración no es la que necesitás.

## The Senior Perspective (El Porqué)

- **La configuración por defecto es un rendezvous, y eso sorprende.** [`MutableSharedFlow<T>()`]({{ "/es/glosario/mutable-shared-flow/" | relative_url }}) no tiene buffer. Con suscriptores presentes, [`emit`]({{ "/es/glosario/emit/" | relative_url }}) suspende hasta que cada uno recibió el valor, y [`tryEmit`]({{ "/es/glosario/try-emit/" | relative_url }}) siempre devuelve `false`, porque no hay dónde dejar el valor sin suspender. Un [`tryEmit`]({{ "/es/glosario/try-emit/" | relative_url }}) que "no hace nada" casi siempre es esto. Llamar a [`tryEmit`]({{ "/es/glosario/try-emit/" | relative_url }}) desde código que no suspende necesita `extraBufferCapacity` o una política de descarte.
- **Sin suscriptores, las emisiones simplemente se pierden.** Con `replay = 0`, un valor emitido mientras nadie colecta no va a ningún lado: sin error y sin advertencia. Para una señal de difusión real, eso es exactamente lo correcto. Para un evento de UI es la trampa: una pantalla que colecta con [`repeatOnLifecycle(STARTED)`]({{ "/es/glosario/repeat-on-lifecycle/" | relative_url }}) tiene cero suscriptores mientras está en background, así que un evento de navegación emitido en ese momento desaparece.
- **Un suscriptor lento frena a todos.** Con `SUSPEND`, el buffer se dimensiona según el [collector]({{ "/es/glosario/collector/" | relative_url }}) más lento. Cuando se atrasa y el buffer se llena, [`emit`]({{ "/es/glosario/emit/" | relative_url }}) suspende para todos, y los [collectors]({{ "/es/glosario/collector/" | relative_url }}) rápidos esperan al lento. Cuando el productor nunca debe esperar, una política de descarte cambia completitud por fluidez, y ese intercambio tiene que ser una decisión deliberada.
- **El replay es una política, no un caché gratis.** `replay = 1` hace que un suscriptor tardío reciba el último valor, lo que se parece a un [`StateFlow`]({{ "/es/02-coroutines-flow/stateflow/" | relative_url }}) sin el filtro de igualdad. También significa que un evento de una sola vez se **reproduce** para cada suscriptor nuevo, por ejemplo después de una rotación, y ese es otra vez el bug de la doble navegación. [`resetReplayCache()`]({{ "/es/glosario/reset-replay-cache/" | relative_url }}) lo limpia, pero llamarlo en el momento justo es frágil.
- **El caso de uso correcto es la difusión.** Un `SharedFlow` brilla cuando varios consumidores independientes tienen que reaccionar cada uno a la misma señal, y perderla mientras nadie escucha es aceptable. Ejemplos son un "sesión expirada" para toda la app, una señal de "cambiaron los datos, invalidá tus cachés" desde un repositorio [singleton]({{ "/es/glosario/singleton/" | relative_url }}), o una única conexión [upstream]({{ "/es/glosario/upstream/" | relative_url }}) compartida entre varias pantallas mediante [`shareIn`]({{ "/es/glosario/share-in/" | relative_url }}). Cuando un valor tiene que manejarlo **exactamente una vez un único consumidor**, la primitiva es un [`Channel`]({{ "/es/glosario/channel/" | relative_url }}), que encola en vez de difundir.
- **Para eventos de UI, primero preguntate si realmente es un evento.** La guía de arquitectura de [Android]({{ "/es/glosario/android/" | relative_url }}) recomienda reducir los eventos de UI a estado: el ViewModel pone el mensaje pendiente en el estado de UI, y la UI avisa cuando ya lo mostró. Eso sobrevive a la rotación, al background y a la muerte del proceso, y es trivial de testear. Un `SharedFlow` de eventos de UI es el patrón del que la guía se alejó, porque le aplican todos los modos de falla de arriba.

## Code in Action

```kotlin
// Not found in FAS — standalone example
// Una señal de difusión: cada suscriptor tiene que reaccionar, y nadie
// necesita el valor si ocurrió mientras no estaba escuchando
class SessionManager {
    private val _sessionExpired = MutableSharedFlow<Unit>(
        extraBufferCapacity = 1,                        // permite que tryEmit tenga éxito
        onBufferOverflow = BufferOverflow.DROP_OLDEST   // nunca bloquea al que llama
    )
    val sessionExpired: SharedFlow<Unit> = _sessionExpired.asSharedFlow()

    // Se llama desde un interceptor de red que no suspende
    fun onUnauthorized() {
        _sessionExpired.tryEmit(Unit)
    }
}

// Not found in FAS — standalone example
// La configuración por defecto: sin buffer y sin replay
val events = MutableSharedFlow<String>()

events.tryEmit("lost")        // true, pero no hay nadie suscripto: el valor se pierde
scope.launch { events.collect { println(it) } }
events.tryEmit("rejected")    // false: hay un suscriptor y no hay buffer
events.emit("delivered")      // suspende hasta que el suscriptor lo recibió

// Not found in FAS — standalone example
// StateFlow es un SharedFlow con exactamente esta configuración
// (más un valor inicial y distinctUntilChanged)
val stateLike = MutableSharedFlow<Int>(
    replay = 1,
    onBufferOverflow = BufferOverflow.DROP_OLDEST
)

// De FollowApp Suite — TasksViewModel.kt
// El snackbar de "Deshacer" NO es un evento de SharedFlow. Es estado: los ids
// de las tareas pendientes viven en el estado de UI hasta que la UI avisa qué pasó.
fun onQuickDeleteTask(taskId: String) {
    viewModelScope.launch {
        // ...
        moveTaskToTrashUseCase(taskId)
        _uiState.update { it.copy(snackbarUndoTaskIds = listOf(taskId), snackbarIsArchiveUndo = false) }
    }
}

fun onSnackbarDismissed() {
    _uiState.update { it.copy(snackbarUndoTaskIds = emptyList()) }
}

// De FollowApp Suite — TasksScreen.kt
// La UI muestra el snackbar cuando el estado lo indica, y después lo confirma.
// Si la pantalla rota en el medio, el estado sigue ahí: no se pierde nada.
LaunchedEffect(uiState.snackbarUndoTaskIds) {
    if (uiState.snackbarUndoTaskIds.isEmpty()) return@LaunchedEffect
    val message = if (uiState.snackbarIsArchiveUndo) archiveMessage else deleteMessage
    val result = snackbarHostState.showSnackbar(
        message = message,
        actionLabel = undoLabel,
        duration = SnackbarDuration.Short
    )
    if (result == SnackbarResult.ActionPerformed) {
        onUndoDelete()
    } else {
        onSnackbarDismissed()
    }
}
```

## The Interview (En el banquillo)

**Pregunta**: ¿Qué diferencia hay entre `SharedFlow` y [`StateFlow`]({{ "/es/02-coroutines-flow/stateflow/" | relative_url }}), y cuándo elegirías un `SharedFlow`?

**Respuesta Senior**: Los dos son [streams hot]({{ "/es/glosario/hot-stream/" | relative_url }}) que difunden a cada [collector]({{ "/es/glosario/collector/" | relative_url }}), y de hecho [`StateFlow`]({{ "/es/02-coroutines-flow/stateflow/" | relative_url }}) es un `SharedFlow` con una configuración fija: replay de uno, overflow que descarta el más viejo, un valor inicial obligatorio y filtrado por igualdad incorporado. Esa configuración lo convierte en un **[state holder]({{ "/es/glosario/state-holder/" | relative_url }})**: siempre hay un valor actual legible con `.value`, un [collector]({{ "/es/glosario/collector/" | relative_url }}) nuevo lo recibe de inmediato, y escribir un valor igual no hace nada. Un `SharedFlow` no asume nada de eso. No tiene valor actual ni valor inicial, entrega los valores iguales cada vez, y el replay, el buffer y el comportamiento de overflow los configuro yo. Entonces elijo [`StateFlow`]({{ "/es/02-coroutines-flow/stateflow/" | relative_url }}) para "qué es verdad ahora", que es la mayor parte del estado de UI, y `SharedFlow` cuando necesito semántica de difusión sin la idea de "valor actual". Los casos típicos son una señal para toda la app a la que varios componentes tienen que reaccionar, como una sesión que expira, o compartir una conexión [upstream]({{ "/es/glosario/upstream/" | relative_url }}) entre varios consumidores con [`shareIn`]({{ "/es/glosario/share-in/" | relative_url }}). También tengo presente lo que `SharedFlow` no es. No es una cola, porque cada [collector]({{ "/es/glosario/collector/" | relative_url }}) recibe cada valor, y con la configuración por defecto ni siquiera es un buffer: los valores emitidos sin suscriptores se descartan y [`tryEmit`]({{ "/es/glosario/try-emit/" | relative_url }}) falla siempre que haya alguien suscripto. Cuando algo tiene que procesarlo exactamente una vez un solo consumidor, uso un [`Channel`]({{ "/es/glosario/channel/" | relative_url }}).

**Pregunta**: Un ViewModel expone eventos de navegación con [`MutableSharedFlow<NavEvent>()`]({{ "/es/glosario/mutable-shared-flow/" | relative_url }}), y la pantalla los colecta con [`repeatOnLifecycle(STARTED)`]({{ "/es/glosario/repeat-on-lifecycle/" | relative_url }}). QA reporta que a veces la navegación no ocurre cuando la app vuelve del background. ¿Por qué, y cómo lo arreglás?

**Respuesta Senior**: El [`MutableSharedFlow`]({{ "/es/glosario/mutable-shared-flow/" | relative_url }}) por defecto tiene `replay = 0` y no tiene buffer, así que una emisión solo llega a los [collectors]({{ "/es/glosario/collector/" | relative_url }}) que existen en ese momento exacto. [`repeatOnLifecycle(STARTED)`]({{ "/es/glosario/repeat-on-lifecycle/" | relative_url }}) cancela correctamente el [collector]({{ "/es/glosario/collector/" | relative_url }}) cuando la app pasa a background. Si el ViewModel emite el evento en ese momento, por ejemplo porque terminó una llamada de red, hay cero suscriptores y el evento se descarta en silencio. Cuando la pantalla vuelve, se suscribe de nuevo, pero ya no queda nada para recibir. Agregar `replay = 1` es el arreglo tentador, y es incorrecto: el evento se reproduciría en cada nueva suscripción, así que después de una rotación la app navegaría dos veces. Hay dos opciones sólidas. La primera, y la que prefiero, es dejar de tratarlo como evento: poner el destino de navegación en el estado de UI, dejar que la UI navegue cuando lo ve, y que la UI avise para limpiarlo. Eso sobrevive al background, a la rotación y a la muerte del proceso, y es fácil de testear. La segunda, cuando realmente tiene que seguir siendo un evento, es un [`Channel`]({{ "/es/glosario/channel/" | relative_url }}) con buffer expuesto con [`receiveAsFlow()`]({{ "/es/glosario/receive-as-flow/" | relative_url }}): un valor enviado sin [collector]({{ "/es/glosario/collector/" | relative_url }}) espera en el buffer hasta que la UI vuelve a colectar, y cada evento se entrega una sola vez a un solo [collector]({{ "/es/glosario/collector/" | relative_url }}). Incluso eso tiene un caso borde, porque un evento que ya salió del [channel]({{ "/es/glosario/channel/" | relative_url }}) se puede perder si el [collector]({{ "/es/glosario/collector/" | relative_url }}) se cancela a mitad del manejo. Es una razón más para ir primero al estado.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
