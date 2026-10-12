---
layout: page
title: "callbackFlow"
lang: es
permalink: /es/02-coroutines-flow/callback-flow/
order: 16
---

## The Theory (El Qué)

Muchas [APIs]({{ "/es/glosario/api/" | relative_url }}) de Android y de SDKs no devuelven valores: te llaman de vuelta. Registrás un [listener]({{ "/es/glosario/listener/" | relative_url }}), y la [API]({{ "/es/glosario/api/" | relative_url }}) lo invoca cada vez que pasa algo (una ubicación nueva, una lectura de un sensor, un cambio de red, el progreso de una descarga). `callbackFlow { }` es el builder que convierte ese tipo de [API]({{ "/es/glosario/api/" | relative_url }}) en un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}).

Adentro del bloque se hacen tres cosas:

1. **Registrar el [callback]({{ "/es/glosario/callbacks/" | relative_url }}).** Cada vez que se dispara, mete el valor en el [flow]({{ "/es/glosario/flow/" | relative_url }}) con [`trySend(value)`]({{ "/es/glosario/try-send/" | relative_url }}). El [callback]({{ "/es/glosario/callbacks/" | relative_url }}) no puede suspender, así que no puede llamar a [`send`]({{ "/es/glosario/send/" | relative_url }}) ni a [`emit`]({{ "/es/glosario/emit/" | relative_url }}); [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) es la forma de entrar sin suspender.
2. **Avisar el final, si la [API]({{ "/es/glosario/api/" | relative_url }}) tiene uno.** Cuando la [API]({{ "/es/glosario/api/" | relative_url }}) informa que terminó, el [callback]({{ "/es/glosario/callbacks/" | relative_url }}) llama a [`close()`]({{ "/es/glosario/close/" | relative_url }}); cuando informa un error, `close(exception)`, y el [collector]({{ "/es/glosario/collector/" | relative_url }}) recibe esa excepción.
3. **Terminar con `awaitClose { }`.** Suspende el bloque mientras el [flow]({{ "/es/glosario/flow/" | relative_url }}) se está colectando, y cuando la colección se detiene, por el motivo que sea, ejecuta su lambda: ahí es donde se **desregistra el [callback]({{ "/es/glosario/callbacks/" | relative_url }})**.

El bloque corre en un [`ProducerScope`]({{ "/es/glosario/producer-scope/" | relative_url }}), que es a la vez un [`CoroutineScope`]({{ "/es/glosario/coroutine-scope/" | relative_url }}) y un [`SendChannel`]({{ "/es/glosario/send-channel/" | relative_url }}). Por detrás hay un [`Channel`]({{ "/es/02-coroutines-flow/channel-hot-streams/" | relative_url }}) entre el [callback]({{ "/es/glosario/callbacks/" | relative_url }}) y el [collector]({{ "/es/glosario/collector/" | relative_url }}): el [callback]({{ "/es/glosario/callbacks/" | relative_url }}) envía y el [collector]({{ "/es/glosario/collector/" | relative_url }}) recibe. Ese [channel]({{ "/es/glosario/channel/" | relative_url }}) es lo que permite que los valores pasen de un [callback]({{ "/es/glosario/callbacks/" | relative_url }}), posiblemente en otro [thread]({{ "/es/glosario/thread/" | relative_url }}), a la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) que colecta. Por defecto tiene un buffer de 64 valores (`BUFFERED`), que se puede cambiar aplicando [`buffer(...)`]({{ "/es/glosario/buffer/" | relative_url }}) o [`conflate()`]({{ "/es/glosario/conflate/" | relative_url }}) al [flow]({{ "/es/glosario/flow/" | relative_url }}) resultante.

El [flow]({{ "/es/glosario/flow/" | relative_url }}) resultante es **cold**: no se registra nada hasta que alguien colecta, y cada [collector]({{ "/es/glosario/collector/" | relative_url }}) vuelve a ejecutar el bloque, así que cada uno registra su propio [callback]({{ "/es/glosario/callbacks/" | relative_url }}).

[`awaitClose`]({{ "/es/glosario/await-close/" | relative_url }}) no es opcional. Si el bloque termina sin él, el [flow]({{ "/es/glosario/flow/" | relative_url }}) falla con una [`IllegalStateException`]({{ "/es/glosario/illegal-state-exception/" | relative_url }}). Eso es lo que distingue a [`callbackFlow`]({{ "/es/glosario/callback-flow/" | relative_url }}) de su hermano más general, [`channelFlow`]({{ "/es/glosario/channel-flow/" | relative_url }}), que no lo exige.

## The Senior Perspective (El Porqué)

- **Uno o muchos valores decide la herramienta.** Si el [callback]({{ "/es/glosario/callbacks/" | relative_url }}) se dispara una sola vez (un request con [`onSuccess`]({{ "/es/glosario/on-success-on-failure/" | relative_url }})/[`onFailure`]({{ "/es/glosario/on-success-on-failure/" | relative_url }})), el puente correcto es [`suspendCancellableCoroutine`]({{ "/es/glosario/suspend-cancellable-coroutine/" | relative_url }}), que lo convierte en una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) que devuelve ese valor. [`callbackFlow`]({{ "/es/glosario/callback-flow/" | relative_url }}) es para [callbacks]({{ "/es/glosario/callbacks/" | relative_url }}) que se disparan repetidamente. Usar un [flow]({{ "/es/glosario/flow/" | relative_url }}) para un único resultado obliga a quien llama a colectar algo que en realidad es una llamada a una función.
- **[`awaitClose`]({{ "/es/glosario/await-close/" | relative_url }}) ata la vida del [listener]({{ "/es/glosario/listener/" | relative_url }}) a la colección.** Ese es el beneficio principal. Cuando el [collector]({{ "/es/glosario/collector/" | relative_url }}) se cancela (la pantalla pasa a background con [`repeatOnLifecycle`]({{ "/es/glosario/repeat-on-lifecycle/" | relative_url }}), el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) se limpia), [`awaitClose`]({{ "/es/glosario/await-close/" | relative_url }}) se ejecuta y el [listener]({{ "/es/glosario/listener/" | relative_url }}) se desregistra. Un [listener]({{ "/es/glosario/listener/" | relative_url }}) registrado a mano en un constructor o un bloque [`init`]({{ "/es/glosario/init/" | relative_url }}), en cambio, vive tanto como su dueño, y si nadie se acuerda de desregistrarlo, es un memory leak o trabajo que nadie está esperando (GPS, sensores, batería).
- **Cada [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) puede fallar, así que el buffer es una decisión de diseño.** Con la capacidad `BUFFERED` por defecto, un [callback]({{ "/es/glosario/callbacks/" | relative_url }}) que se dispara más rápido de lo que el [collector]({{ "/es/glosario/collector/" | relative_url }}) consume llena el buffer y [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) empieza a fallar en silencio. Para "solo importa el último" (ubicación, sensores), aplicar [`conflate()`]({{ "/es/glosario/conflate/" | relative_url }}) o [`buffer(Channel.CONFLATED)`]({{ "/es/glosario/buffer/" | relative_url }}). Si cada valor importa y el volumen es acotado, un buffer más grande o `UNLIMITED`. Como mínimo, revisar el resultado y loguear las fallas.
- **Cold significa un registro por [collector]({{ "/es/glosario/collector/" | relative_url }}).** Dos pantallas que colectan el mismo [`callbackFlow`]({{ "/es/glosario/callback-flow/" | relative_url }}) registran dos [listeners]({{ "/es/glosario/listener/" | relative_url }}) en el sistema. Si la fuente es cara, hay que compartirla: [`shareIn`]({{ "/es/glosario/share-in/" | relative_url }}) o [`stateIn`]({{ "/es/glosario/state-in/" | relative_url }}) con [`WhileSubscribed`]({{ "/es/glosario/while-subscribed/" | relative_url }}) mantiene un único registro mientras haya al menos un [suscriptor]({{ "/es/glosario/collector/" | relative_url }}) y lo desregistra cuando se va el último.
- **Los errores van por `close(cause)`, no por [`throw`]({{ "/es/glosario/throw/" | relative_url }}).** Una excepción lanzada adentro del [callback]({{ "/es/glosario/callbacks/" | relative_url }}) corre en el [thread]({{ "/es/glosario/thread/" | relative_url }}) de la [API]({{ "/es/glosario/api/" | relative_url }}), fuera del [flow]({{ "/es/glosario/flow/" | relative_url }}): rompe ese [thread]({{ "/es/glosario/thread/" | relative_url }}) o el [SDK]({{ "/es/glosario/sdk/" | relative_url }}) se la traga, y el [collector]({{ "/es/glosario/collector/" | relative_url }}) nunca la ve. Llamar a `close(exception)` hace que la colección falle con esa excepción, donde un [`catch`]({{ "/es/glosario/catch/" | relative_url }}) [downstream]({{ "/es/glosario/downstream/" | relative_url }}) la puede manejar.
- **¿Por qué no [`flow { }`]({{ "/es/glosario/flow-builder/" | relative_url }})?** [`flow { }`]({{ "/es/glosario/flow-builder/" | relative_url }}) exige que cada [`emit`]({{ "/es/glosario/emit/" | relative_url }}) ocurra desde la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) que colecta; emitir desde un [callback]({{ "/es/glosario/callbacks/" | relative_url }}) en otro [thread]({{ "/es/glosario/thread/" | relative_url }}) rompe esa regla y falla en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) ("[Flow]({{ "/es/glosario/flow/" | relative_url }}) invariant is violated"). [`callbackFlow`]({{ "/es/glosario/callback-flow/" | relative_url }}) existe justamente porque el [channel]({{ "/es/glosario/channel/" | relative_url }}) que tiene adentro hace que enviar desde otro [thread]({{ "/es/glosario/thread/" | relative_url }}) sea seguro.

## Code in Action

```kotlin
// From FollowApp Suite — InAppUpdateManager.kt
// A Play Core listener registered by hand in init and never unregistered.
// It works because the manager is a @Singleton that lives as long as the app
// and only needs the latest state, so a StateFlow is enough. The listener's
// lifetime is the app's lifetime, not the lifetime of whoever is observing.
private val installListener = InstallStateUpdatedListener { state ->
    if (state.installStatus() == InstallStatus.DOWNLOADED) {
        _flexibleUpdateDownloaded.value = true
    }
}

init {
    appUpdateManager.registerListener(installListener)
}

// Not found in FAS — standalone example
// The same listener as a callbackFlow: registered when someone collects,
// unregistered as soon as the collection stops.
fun AppUpdateManager.installStates(): Flow<InstallState> = callbackFlow {
    val listener = InstallStateUpdatedListener { state ->
        trySend(state)
        if (state.installStatus() == InstallStatus.INSTALLED) close()   // natural end
    }
    registerListener(listener)
    awaitClose { unregisterListener(listener) }
}

// Not found in FAS — standalone example
// A sensor fires very often and only the latest value matters: conflate()
// replaces the pending value, so trySend cannot fail for a full buffer.
fun SensorManager.readings(sensor: Sensor): Flow<SensorEvent> = callbackFlow {
    val listener = object : SensorEventListener {
        override fun onSensorChanged(event: SensorEvent) { trySend(event) }
        override fun onAccuracyChanged(sensor: Sensor, accuracy: Int) = Unit
    }
    registerListener(listener, sensor, SensorManager.SENSOR_DELAY_UI)
    awaitClose { unregisterListener(listener) }
}.conflate()

// Not found in FAS — standalone example
// Several screens, one registration: stateIn with WhileSubscribed keeps a
// single listener while anyone collects, and unregisters 5 s after the last one leaves.
val connectivity: StateFlow<Boolean> = connectivityManager.networkAvailability()
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), initialValue = false)
```

## The Interview (En el banquillo)

**Pregunta**: ¿Cómo convertís una [API]({{ "/es/glosario/api/" | relative_url }}) basada en [listeners]({{ "/es/glosario/listener/" | relative_url }}) en un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}), y para qué sirve [`awaitClose`]({{ "/es/glosario/await-close/" | relative_url }})?

**Respuesta Senior**: Con [`callbackFlow`]({{ "/es/glosario/callback-flow/" | relative_url }}). Adentro del bloque registro el [listener]({{ "/es/glosario/listener/" | relative_url }}), y cada vez que se dispara meto el valor en el [flow]({{ "/es/glosario/flow/" | relative_url }}) con [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}), porque el [listener]({{ "/es/glosario/listener/" | relative_url }}) no puede suspender. Si la [API]({{ "/es/glosario/api/" | relative_url }}) informa un final, llamo a [`close()`]({{ "/es/glosario/close/" | relative_url }}), y si informa un error, `close(exception)`, para que el [collector]({{ "/es/glosario/collector/" | relative_url }}) lo reciba. El bloque tiene que terminar con [`awaitClose`]({{ "/es/glosario/await-close/" | relative_url }}), que suspende mientras el [flow]({{ "/es/glosario/flow/" | relative_url }}) se está colectando y ejecuta su lambda cuando la colección se detiene, y en esa lambda desregistro el [listener]({{ "/es/glosario/listener/" | relative_url }}). Ese es el valor real de [`callbackFlow`]({{ "/es/glosario/callback-flow/" | relative_url }}): el [listener]({{ "/es/glosario/listener/" | relative_url }}) vive exactamente mientras alguien colecta. Cuando la pantalla pasa a background y [`repeatOnLifecycle`]({{ "/es/glosario/repeat-on-lifecycle/" | relative_url }}) cancela la colección, el [listener]({{ "/es/glosario/listener/" | relative_url }}) se desregistra solo, así que no hay leak ni trabajo que nadie espera. Si me olvido de [`awaitClose`]({{ "/es/glosario/await-close/" | relative_url }}), el [flow]({{ "/es/glosario/flow/" | relative_url }}) falla con una [`IllegalStateException`]({{ "/es/glosario/illegal-state-exception/" | relative_url }}). Por dentro hay un [channel]({{ "/es/glosario/channel/" | relative_url }}) entre el [callback]({{ "/es/glosario/callbacks/" | relative_url }}) y el [collector]({{ "/es/glosario/collector/" | relative_url }}), que es lo que hace seguro enviar desde el [thread]({{ "/es/glosario/thread/" | relative_url }}) de la [API]({{ "/es/glosario/api/" | relative_url }}). Y si la [API]({{ "/es/glosario/api/" | relative_url }}) llama de vuelta una sola vez, no uso [`callbackFlow`]({{ "/es/glosario/callback-flow/" | relative_url }}): [`suspendCancellableCoroutine`]({{ "/es/glosario/suspend-cancellable-coroutine/" | relative_url }}) la convierte en una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}).

**Pregunta**: Dos pantallas colectan el mismo [`callbackFlow`]({{ "/es/glosario/callback-flow/" | relative_url }}) de actualizaciones de ubicación. Ves dos registros de GPS, y bajo carga algunas actualizaciones nunca llegan. ¿Qué está pasando y cómo lo arreglás?

**Respuesta Senior**: Los dos síntomas vienen de cómo funciona [`callbackFlow`]({{ "/es/glosario/callback-flow/" | relative_url }}). Es cold: cada [collector]({{ "/es/glosario/collector/" | relative_url }}) vuelve a ejecutar el bloque, así que cada uno registra su propio [listener]({{ "/es/glosario/listener/" | relative_url }}), y dos pantallas son dos registros de GPS. La solución es compartirlo, con [`shareIn`]({{ "/es/glosario/share-in/" | relative_url }}) o [`stateIn`]({{ "/es/glosario/state-in/" | relative_url }}) y [`WhileSubscribed`]({{ "/es/glosario/while-subscribed/" | relative_url }}) en un scope que viva más que las pantallas, para que haya un único registro mientras al menos una pantalla colecta, y se desregistre cuando se va la última. Las actualizaciones perdidas vienen del [channel]({{ "/es/glosario/channel/" | relative_url }}) que tiene detrás. Su buffer por defecto guarda 64 valores, y el [listener]({{ "/es/glosario/listener/" | relative_url }}) usa [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}), que no espera: cuando el [collector]({{ "/es/glosario/collector/" | relative_url }}) es más lento que el GPS y el buffer está lleno, [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) falla y, si nadie revisa el resultado, la actualización desaparece en silencio. Para ubicación solo importa el último valor, así que la respuesta correcta es [`conflate()`]({{ "/es/glosario/conflate/" | relative_url }}): la posición más nueva reemplaza a la pendiente, y [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) deja de fallar por falta de lugar. Si cada valor importara, dimensionaría el buffer para eso, y en cualquier caso revisaría el resultado de [`trySend`]({{ "/es/glosario/try-send/" | relative_url }}) para que una falla sea visible en lugar de silenciosa.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
