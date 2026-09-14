---
layout: page
title: "Context & Dispatchers (Main, IO, Default)"
lang: es
permalink: /es/02-coroutines-flow/context-dispatchers/
order: 2
---

## The Theory (El Qué)

Toda [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) corre dentro de un [`CoroutineContext`]({{ "/es/glosario/coroutine-context/" | relative_url }}): un conjunto inmutable e indexado de elementos que viaja con la coroutine y que hereda cada hijo que lanza. Los dos elementos que importan a diario son el [`Job`]({{ "/es/glosario/job/" | relative_url }}) — el handle de [lifecycle]({{ "/es/glosario/lifecycle/" | relative_url }}) de la coroutine, lo que se cancela — y el [`CoroutineDispatcher`]({{ "/es/glosario/dispatcher/" | relative_url }}) — el elemento que decide *qué [thread]({{ "/es/glosario/thread/" | relative_url }}) o [thread pool]({{ "/es/glosario/thread-pool/" | relative_url }})* ejecuta el código de la coroutine después de cada [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}). Los contextos se componen con `+`: `SupervisorJob() + Dispatchers.IO` es un contexto con dos elementos; agregar otro [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) reemplaza al primero, porque cada tipo de elemento tiene un único slot.

Android trae cuatro [dispatchers]({{ "/es/glosario/dispatcher/" | relative_url }}), y saber *para qué* sirve cada uno es todo el tema:

- **[`Dispatchers.Main`]({{ "/es/glosario/dispatchers-main/" | relative_url }})** — el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}). Todo lo que toca la UI, y el único lugar donde las mutaciones de Views y la mayoría de las escrituras de estado de Compose son legales. Hace post a la cola del [`Looper`]({{ "/es/glosario/looper/" | relative_url }}): una coroutine reanudada acá espera a que termine el trabajo del frame actual.
- **[`Dispatchers.Main.immediate`]({{ "/es/glosario/dispatchers-main-immediate/" | relative_url }})** — el mismo thread, pero si *ya* estás en Main corre de forma síncrona en vez de hacer post. [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) y `lifecycleScope` lo usan, así que un [`launch`]({{ "/es/glosario/launch/" | relative_url }}) desde un click handler se ejecuta hasta su primera suspensión antes de que el handler devuelva.
- **[`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }})** — un pool dimensionado para detener threads en [llamadas bloqueantes]({{ "/es/glosario/blocking-call/" | relative_url }}): I/O de archivos, sockets, SDKs síncronos legacy. Hasta 64 threads (o la cantidad de cores, lo que sea mayor).
- **[`Dispatchers.Default`]({{ "/es/glosario/dispatchers-default/" | relative_url }})** — un pool dimensionado según la cantidad de cores (mínimo 2), para cómputo: ordenar, parsear, aritmética de fechas, diffing. Bloquear acá deja sin recursos a toda otra coroutine que necesite un core.

[`IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) y [`Default`]({{ "/es/glosario/dispatchers-default/" | relative_url }}) son vistas sobre el *mismo* thread pool subyacente con distintos límites de paralelismo, así que saltar entre ellos es barato — el [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) muchas veces se saltea el cambio de thread por completo. También existe [`Dispatchers.Unconfined`]({{ "/es/glosario/dispatchers-unconfined/" | relative_url }}), y solo tiene lugar en tests y código de framework.

[`withContext(dispatcher) { }`]({{ "/es/glosario/with-context/" | relative_url }}) es la forma en que una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) cambia de [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) para un bloque: suspende, reanuda el bloque en el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) nuevo, y cuando el bloque devuelve reanuda al llamador de vuelta en el original — sin nueva coroutine, sin [`launch`]({{ "/es/glosario/launch/" | relative_url }}), y el resultado es el valor del bloque.

## The Senior Perspective (El Porqué)

- **El [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) se hereda, y eso hace que la main-safety sea responsabilidad del *callee*.** Una suspend function corre en el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) que tenía su llamador. Si [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) (Main) llama `repository.export()` y `export()` hace I/O de archivos sin cambiar de [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}), Main se bloquea. La convención en Android es que *toda* suspend function es segura de llamar desde Main — así que [`withContext(Dispatchers.IO)`]({{ "/es/glosario/with-context/" | relative_url }}) va *adentro* de la función que hace el trabajo bloqueante, una sola vez, no en cada call site. Room, Retrofit y DataStore ya la respetan; tu propio código de archivos y JSON tiene que hacerlo.
- **Elegí el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) por la naturaleza del trabajo, no por costumbre.** [`IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) para cualquier cosa que detenga un thread; [`Default`]({{ "/es/glosario/dispatchers-default/" | relative_url }}) para cualquier cosa que queme CPU. Hacerlo al revés no es fatal pero está mal en las dos direcciones: bloquear en [`Default`]({{ "/es/glosario/dispatchers-default/" | relative_url }}) le roba uno de los pocos cores a todo otro cómputo; los loops de CPU en [`IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) desperdician un pool diseñado para esperar. La aritmética de fechas, ordenar o hacer diff de una lista grande es cómputo y va en [`Default`]({{ "/es/glosario/dispatchers-default/" | relative_url }}) aunque sea "lento" — la lentitud no es el criterio, el bloqueo sí.
- **[`Main.immediate`]({{ "/es/glosario/dispatchers-main-immediate/" | relative_url }}) es una garantía de orden en la que podés apoyarte — y con la que podés tropezar.** Como un [`launch`]({{ "/es/glosario/launch/" | relative_url }}) desde Main corre de forma síncrona hasta su primera suspensión, el código *después* de la llamada a [`launch`]({{ "/es/glosario/launch/" | relative_url }}) ve los primeros efectos síncronos de la coroutine. Una trampa típica: un reset de estado puesto *después* de setear un flow disparador, cuando un collector de `combine` en [`Main.immediate`]({{ "/es/glosario/dispatchers-main-immediate/" | relative_url }}) corre de forma síncrona en el momento en que el disparador cambia y su resultado es borrado por el reset. Cuando ves un comentario explicando el orden de las sentencias alrededor de [`Main.immediate`]({{ "/es/glosario/dispatchers-main-immediate/" | relative_url }}), es un ingeniero senior que ya se lastimó una vez.
- **Un [`Job`]({{ "/es/glosario/job/" | relative_url }}) es un árbol de cancelación, y [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) cambia su semántica de fallo.** Con un [`Job`]({{ "/es/glosario/job/" | relative_url }}) común, un hijo que falla cancela a su padre y por lo tanto a sus hermanos. Con un [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}), el fallo de un hijo es problema suyo — los hermanos siguen corriendo. Por eso un [`CoroutineScope`]({{ "/es/glosario/coroutine-scope/" | relative_url }}) de larga vida, con scope de aplicación, se construye como `CoroutineScope(SupervisorJob() + Dispatchers.IO)`: un singleton suele ser dueño de varios collectors independientes, y que uno crashee no debe matar a los otros. [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) es un [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) por la misma razón.
- **Un scope custom es un leak hasta que se demuestre lo contrario.** `CoroutineScope(...)` en un campo de clase vive hasta que algo llama `cancel()`. Se justifica para objetos que genuinamente sobreviven a cualquier pantalla — un repositorio [`@Singleton`]({{ "/es/glosario/singleton-scope/" | relative_url }}), un manager a nivel `Application` — y debe documentarse como tal. `GlobalScope` es lo mismo sin dueño alguno; no hay razón para usarlo. `CoroutineScope(...).launch { }` creado inline para trabajo fire-and-forget — la inicialización única de un SDK, por ejemplo — es aceptable solo cuando el trabajo es acotado y no puede fallar de una forma que alguien necesite saber.
- **Hardcodear [`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) acopla tu clase a threads reales, y eso es un problema de testing.** [`runTest`]({{ "/es/glosario/run-test/" | relative_url }}) no puede controlar una coroutine que salta al pool real de IO: el test o tiene una race o tiene que dormir. El fix senior es inyectar el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) por dependencia ([`@IoDispatcher private val io: CoroutineDispatcher`]({{ "/es/glosario/io-dispatcher/" | relative_url }})) para que los tests sustituyan un [`TestDispatcher`]({{ "/es/glosario/test-dispatcher/" | relative_url }}). La media solución habitual es [`Dispatchers.setMain(testDispatcher)`]({{ "/es/glosario/set-main/" | relative_url }}), que controla solo Main: hace testeable el código en [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) y silenciosamente no hace nada por un [`withContext(Dispatchers.IO)`]({{ "/es/glosario/with-context/" | relative_url }}) más abajo.
- **Las excepciones no capturadas pertenecen al scope, no al [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}).** Una excepción que escapa de un [`launch`]({{ "/es/glosario/launch/" | relative_url }}) se propaga al [`Job`]({{ "/es/glosario/job/" | relative_url }}) padre; si nadie la maneja, la app crashea. Un [`CoroutineExceptionHandler`]({{ "/es/glosario/coroutine-exception-handler/" | relative_url }}) instalado en el contexto del scope es la última línea de defensa para trabajo fire-and-forget. Nunca aplica a `async` — ahí la excepción espera adentro del [`Deferred`]({{ "/es/glosario/deferred/" | relative_url }}) hasta el [`await()`]({{ "/es/glosario/await/" | relative_url }}).

## Code in Action

### La main-safety vive adentro de la suspend function

`BackupManager` se llama desde [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}), en Main. Cambia a [`IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) por su cuenta, así ningún llamador tiene que saber que toca el sistema de archivos.

```kotlin
// From FollowApp Suite — BackupManager.kt
suspend fun exportTo(uri: Uri): Result<Unit> = withContext(Dispatchers.IO) {
    runCatching {
        val bundle = BackupBundle(
            tasks = backupDao.getAllTasks(),
            labels = backupDao.getAllLabels(),
            labelOptions = backupDao.getAllLabelOptions(),
            presets = backupDao.getAllPresets()
        )
        val json = BackupSerializer.serialize(bundle)
        context.contentResolver.openOutputStream(uri, "wt").use { stream ->
            requireNotNull(stream) { "Cannot open destination" }
            stream.write(json.toByteArray(Charsets.UTF_8))
        }
    }.onSuccess {
        Log.d(TAG, "Backup exported")
    }.onFailure { Log.e(TAG, "Backup export failed", it) }
}
```

El [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}) *es* el cuerpo de la función, así que el llamador en Main suspende, el trabajo corre en un thread de IO, y el [`Result`]({{ "/es/glosario/result/" | relative_url }}) vuelve en Main.

### `Default` para cómputo, no `IO`

La aritmética de fechas de recurrencia es trabajo de CPU. Igual frenaría el input en Main, así que salta — al pool de CPU, no al de I/O.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
viewModelScope.launch {
    // Date math off the main thread: pattern scans over months/years
    // must never stall input dispatching (popup ANR)
    val suggested = withContext(Dispatchers.Default) {
        val settings = getRecurrenceSettingsUseCase().first()
        // ... RecurrenceCalculator.suggestPatternDueDate(...)
    }
    _uiState.update { it.copy(form = it.form.copy(dueDate = suggested)) }
}
```

Cuando [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}) devuelve, el `update` corre de vuelta en [`Main.immediate`]({{ "/es/glosario/dispatchers-main-immediate/" | relative_url }}) — el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) del llamador — sin ningún cambio explícito.

### Sobrescribir el dispatcher del scope al lanzar

[`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) usa [`Main.immediate`]({{ "/es/glosario/dispatchers-main-immediate/" | relative_url }}) por defecto. Acá ese default se sobrescribe deliberadamente, y el comentario registra la razón medida.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
// Dispatchers.IO because viewModelScope defaults to Main.immediate,
// and Main is saturated by Compose's first composition on cold start.
// The dataStore read is fast (~5 ms — hot cache after Application
// warmed it), but the resume-back-to-Main was getting queued behind
// Compose for hundreds of ms. IO bypasses that; MutableStateFlow
// updates are already thread-safe.
viewModelScope.launch(Dispatchers.IO) {
    val snapshot = runCatching { tasksViewPreferences.read() }
        .onFailure { Log.e(TAG, "Error restoring TasksView prefs — falling back to defaults", it) }
        .getOrNull()
    if (snapshot != null) {
        _uiState.update { it.copy(/* ... */) }
    }
}
```

Pasarle un contexto a [`launch`]({{ "/es/glosario/launch/" | relative_url }}) *suma* al contexto del scope: el [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) y la cancelación de [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) se conservan, solo se reemplaza el elemento [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}). La última línea del comentario es la precondición que hace esto seguro: [`MutableStateFlow.update`]({{ "/es/glosario/update/" | relative_url }}) es [atómico]({{ "/es/glosario/atomicity/" | relative_url }}), así que escribir estado desde un thread de IO está bien.

### `Main.immediate` como garantía de orden

```kotlin
// From FollowApp Suite — TasksViewModel.kt
fun onFabClicked() {
    subtasksJob?.cancel()
    subtasksJob = null
    // Reset the form FIRST, then trigger the suggestion recompute.
    // viewModelScope uses Main.immediate, so the combine collector may run
    // synchronously when a source flow is set — if the form reset came after,
    // it would wipe the freshly computed labelSearchResults.
    _uiState.update { it.copy(isFormVisible = true, editingTaskId = null, form = TaskFormState()) }
    _formLabelSearchQuery.value = ""
    _selectedLabels.value = emptyList()
    _formOpenTrigger.value = System.currentTimeMillis()
}
```

Setear `_formOpenTrigger` puede ejecutar un collector de `combine` *de forma síncrona*, dentro de esta misma llamada, porque el collector vive en una coroutine [`Main.immediate`]({{ "/es/glosario/dispatchers-main-immediate/" | relative_url }}) y ya está en Main. El orden de las sentencias, por lo tanto, sostiene la corrección.

### Un scope de larga vida: `SupervisorJob` + `IO`

Un repositorio [`@Singleton`]({{ "/es/glosario/singleton-scope/" | relative_url }}) sobrevive a toda pantalla, así que es dueño de su propio scope. Dos decisiones codificadas en una línea: [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) para que un listener que falla no cancele a los otros, [`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) porque el cliente de billing bloquea.

```kotlin
// From FollowApp Suite — PremiumRepositoryImpl.kt
@Singleton
class PremiumRepositoryImpl @Inject constructor(
    private val premiumPreferences: PremiumPreferences,
    private val billingConnector: BillingConnector
) : PremiumRepository {

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    init {
        billingConnector.connect()
        scope.launch {
            billingConnector.isOwned
                .filterNotNull()
                .collect { owned -> premiumPreferences.setAdsRemoved(owned) }
        }
    }
}
```

Lo que este scope *no* tiene es un [`CoroutineExceptionHandler`]({{ "/es/glosario/coroutine-exception-handler/" | relative_url }}) — una excepción que escape de [`collect`]({{ "/es/glosario/collect/" | relative_url }}) acá crashearía el proceso. Una versión más estricta: `CoroutineScope(SupervisorJob() + Dispatchers.IO + CoroutineExceptionHandler { _, e -> Log.e(TAG, "billing", e) })`.

### Fire-and-forget con un scope inline

```kotlin
// From FollowApp Suite — ConsentManager.kt
// MobileAds.initialize does ~700 ms of synchronous SDK bootstrap on
// the caller thread even though it exposes an async callback.
CoroutineScope(SupervisorJob() + Dispatchers.IO).launch {
    MobileAds.initialize(app)
}
```

Aceptable porque el trabajo es acotado, idempotente (protegido por un `compareAndSet` más arriba) y nadie necesita su resultado. Sigue siendo un scope sin dueño: nada puede cancelarlo. Ese es el trade-off que se está haciendo, y el comentario es lo que lo convierte en una decisión en vez de un accidente.

### Lo que revelan los tests

```kotlin
// From FollowApp Suite — SettingsViewModelTest.kt
@Before
fun setup() {
    Dispatchers.setMain(testDispatcher)
}

@After
fun tearDown() {
    Dispatchers.resetMain()
}
```

[`setMain`]({{ "/es/glosario/set-main/" | relative_url }}) reemplaza [`Dispatchers.Main`]({{ "/es/glosario/dispatchers-main/" | relative_url }}) para el test, así [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) se vuelve controlable. No hace nada por [`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}). La versión inyectada — la que FAS necesitaría para testear `BackupManager` de forma determinista:

```kotlin
// Not found in FAS — standalone example
class BackupManager @Inject constructor(
    @IoDispatcher private val io: CoroutineDispatcher,
    /* ... */
) {
    suspend fun exportTo(uri: Uri): Result<Unit> = withContext(io) { /* ... */ }
}

// Módulo de Hilt
@Provides @IoDispatcher fun provideIo(): CoroutineDispatcher = Dispatchers.IO

// Test
val manager = BackupManager(io = StandardTestDispatcher(testScheduler), /* ... */)
```

Un parámetro de constructor convierte un salto real de thread en tiempo virtual bajo [`runTest`]({{ "/es/glosario/run-test/" | relative_url }}).

## The Interview (En el banquillo)

**Pregunta**: ¿Qué es un `CoroutineContext`, y qué hace realmente [`withContext(Dispatchers.IO)`]({{ "/es/glosario/with-context/" | relative_url }})?

**Respuesta Senior**: Un [`CoroutineContext`]({{ "/es/glosario/coroutine-context/" | relative_url }}) es un conjunto inmutable de elementos indexados por tipo — el [`Job`]({{ "/es/glosario/job/" | relative_url }}) que representa el [lifecycle]({{ "/es/glosario/lifecycle/" | relative_url }}) de la coroutine, el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) que decide qué thread la corre, un [`CoroutineExceptionHandler`]({{ "/es/glosario/coroutine-exception-handler/" | relative_url }}) opcional y un nombre. Se hereda: un hijo lanzado desde un scope recibe el contexto del scope, y todo lo que le pasás a [`launch`]({{ "/es/glosario/launch/" | relative_url }}) o [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}) se *suma*, reemplazando solo los elementos del mismo tipo. Así, `viewModelScope.launch(Dispatchers.IO)` conserva el [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) y el atado de cancelación al ViewModel y cambia solo el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}). [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}) no es un cambio de thread en el sentido de `Thread`: suspende la coroutine actual, agenda la [continuation]({{ "/es/glosario/continuation/" | relative_url }}) del bloque en el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) destino, lo corre ahí, y cuando el bloque completa agenda la continuation del llamador de vuelta en el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) *original*, devolviendo el valor del bloque. No se crea ninguna coroutine nueva, la [cancelación]({{ "/es/glosario/cooperative-cancellation/" | relative_url }}) fluye a través, y como [`IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) y [`Default`]({{ "/es/glosario/dispatchers-default/" | relative_url }}) comparten pool, el [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) puede elidir el salto físico de thread cuando puede. La regla práctica que se desprende: poné [`withContext(Dispatchers.IO)`]({{ "/es/glosario/with-context/" | relative_url }}) *adentro* de la suspend function que bloquea, así la función es main-safe para todo llamador, e inyectá el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) para que los tests puedan reemplazarlo.

**Pregunta**: Un repositorio [`@Singleton`]({{ "/es/glosario/singleton-scope/" | relative_url }}) colecta un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) de billing para siempre. ¿Cómo scopeás esa coroutine, y qué pasa cuando el collector lanza una excepción?

**Respuesta Senior**: El repositorio sobrevive a toda pantalla, así que ni [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) ni `lifecycleScope` encajan — necesita su propio [`CoroutineScope`]({{ "/es/glosario/coroutine-scope/" | relative_url }}), y lo construiría como `CoroutineScope(SupervisorJob() + Dispatchers.IO + CoroutineExceptionHandler { ... })`. Cada elemento es una decisión. [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) porque un singleton típicamente es dueño de varios collectors independientes, y con un [`Job`]({{ "/es/glosario/job/" | relative_url }}) común un hijo que falla cancela al padre y por lo tanto a todos sus hermanos — que el listener de consentimiento muera porque el de billing lanzó una excepción es exactamente el acoplamiento a evitar. [`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) porque el cliente de billing bloquea. Y el handler porque con un [`SupervisorJob`]({{ "/es/glosario/supervisor-job/" | relative_url }}) la excepción de un hijo no se propaga a un padre que pudiera manejarla; va al handler del contexto, y si no hay ninguno, al handler de excepciones no capturadas del thread — que en Android crashea el proceso. Sin ese tercer elemento, una excepción en [`collect`]({{ "/es/glosario/collect/" | relative_url }}) es un crash de producción sin ningún [`try/catch`]({{ "/es/glosario/try-catch/" | relative_url }}) a la vista. Dos cosas más que plantearía: el scope nunca se cancela, lo cual es aceptable solo porque un [`@Singleton`]({{ "/es/glosario/singleton-scope/" | relative_url }}) vive genuinamente tanto como el proceso, e inyectaría el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) en vez de hardcodearlo para que el collector pueda manejarse con un [`TestDispatcher`]({{ "/es/glosario/test-dispatcher/" | relative_url }}) bajo [`runTest`]({{ "/es/glosario/run-test/" | relative_url }}).

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
