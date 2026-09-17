---
layout: page
title: "Main-Safety"
lang: es
permalink: /es/02-coroutines-flow/main-safety/
order: 5
---

## The Theory (El Qué)

Una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) es **main-safe** cuando se la puede llamar desde el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) sin bloquearlo. Esa es toda la definición, y es un *contrato sobre el llamado*: la función misma es responsable de mover cualquier [blocking call]({{ "/es/glosario/blocking-call/" | relative_url }}) — disco, red, un [SDK]({{ "/es/glosario/sdk/" | relative_url }}) síncrono, CPU pesada — fuera de Main, para que un llamador en [`Dispatchers.Main`]({{ "/es/glosario/dispatchers-main/" | relative_url }}) solo *suspenda* mientras el trabajo ocurre en otro lado.

El mecanismo es [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}): la función envuelve su cuerpo bloqueante en `withContext(Dispatchers.IO) { }` (para I/O) o `withContext(Dispatchers.Default) { }` (para CPU). La [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) del llamador suspende en ese [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}), el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) vuelve a su [`Looper`]({{ "/es/glosario/looper/" | relative_url }}) y sigue dibujando frames y manejando input, el bloque corre en un [thread pool]({{ "/es/glosario/thread-pool/" | relative_url }}), y cuando retorna el llamador se reanuda en Main con el resultado.

Por qué importa el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}): Android dibuja a 60–120 Hz, así que cada frame tiene aproximadamente 16 ms (u 8 ms) de presupuesto, y *todo* se gasta en Main — medir, ubicar, dibujar y despachar eventos táctiles. Una [blocking call]({{ "/es/glosario/blocking-call/" | relative_url }}) de 50 ms en Main pierde tres frames ([jank]({{ "/es/glosario/jank/" | relative_url }})); una de 5 segundos sin procesar input dispara un diálogo de **[ANR]({{ "/es/glosario/anr/" | relative_url }})** (Application Not Responding) y el sistema mata la app. La palabra [`suspend`]({{ "/es/glosario/suspend-functions/" | relative_url }}) *no* te protege de esto: `suspend fun load() = File(path).readText()` es una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) que bloquea Main durante toda la lectura. La suspensión solo ocurre en [suspension points]({{ "/es/glosario/suspension-point/" | relative_url }}) reales.

La convención en todo el ecosistema Android, enunciada en la guía oficial, es que **toda [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) es main-safe**. Los métodos [`suspend`]({{ "/es/glosario/suspend-functions/" | relative_url }}) de un [DAO]({{ "/es/glosario/dao/" | relative_url }}) de [Room]({{ "/es/glosario/room/" | relative_url }}) cambian a su propio executor de queries; las llamadas [`suspend`]({{ "/es/glosario/suspend-functions/" | relative_url }}) de [Retrofit]({{ "/es/glosario/retrofit/" | relative_url }}) corren en el pool de [OkHttp]({{ "/es/glosario/okhttp/" | relative_url }}); el [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) `data` de [DataStore]({{ "/es/glosario/datastore/" | relative_url }}) lee en IO. Gracias a eso, el código de aplicación nunca tiene que adivinar: si una función es [`suspend`]({{ "/es/glosario/suspend-functions/" | relative_url }}), llamarla desde [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) (que es [`Main.immediate`]({{ "/es/glosario/dispatchers-main-immediate/" | relative_url }})) es seguro. Las únicas funciones que pueden romper la regla son las que escribís *vos* alrededor de archivos crudos, sockets, JSON, criptografía o un [SDK]({{ "/es/glosario/sdk/" | relative_url }}) síncrono legacy — y de esas trata este tema.

## The Senior Perspective (El Porqué)

- **Main-safety es responsabilidad del llamado porque el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) se hereda.** Una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) corre en el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) que tenga su llamador. Si el llamador tiene que acordarse de envolver `repository.export()` en [`withContext(Dispatchers.IO)`]({{ "/es/glosario/with-context/" | relative_url }}), entonces todos los llamadores tienen que acordarse, para siempre — y el primero que se olvida manda un [ANR]({{ "/es/glosario/anr/" | relative_url }}) a producción. Poner el [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}) *adentro* de `export()` hace la garantía local, testeable e imposible de esquivar. Regla práctica: la capa que sabe que el trabajo bloquea es la capa que cambia de [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}).
- **[`suspend`]({{ "/es/glosario/suspend-functions/" | relative_url }}) es una promesa, no un mecanismo.** Marcar una función [`suspend`]({{ "/es/glosario/suspend-functions/" | relative_url }}) dice "podés llamarme desde una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }})"; no mueve nada a ningún lado. La trampa es una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) que nunca suspende de verdad: compila, funciona en tests sobre un [`TestDispatcher`]({{ "/es/glosario/test-dispatcher/" | relative_url }}), y bloquea Main en producción. Quien revisa debería preguntar de cada [`suspend fun`]({{ "/es/glosario/suspend-functions/" | relative_url }}) que toca un archivo, un socket o un loop grande: *¿dónde está el cambio de [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }})?* En builds de debug, [`StrictMode`]({{ "/es/glosario/strict-mode/" | relative_url }}) con `detectDiskReads()` y `detectNetwork()` hace ruidosa la respuesta la primera vez que el código corre en un dispositivo.
- **No envuelvas lo que ya es seguro.** `withContext(Dispatchers.IO) { dao.insert(x) }` alrededor de un método [`suspend`]({{ "/es/glosario/suspend-functions/" | relative_url }}) de [Room]({{ "/es/glosario/room/" | relative_url }}) no hace nada útil — [Room]({{ "/es/glosario/room/" | relative_url }}) ya salta — y cuesta un dispatch redundante más un lector que ahora cree que el [DAO]({{ "/es/glosario/dao/" | relative_url }}) *no* es main-safe. Lo mismo para las llamadas [`suspend`]({{ "/es/glosario/suspend-functions/" | relative_url }}) de [Retrofit]({{ "/es/glosario/retrofit/" | relative_url }}) y [DataStore]({{ "/es/glosario/datastore/" | relative_url }}). Envolver dos veces es señal de que el autor no confía en el contrato, y se contagia.
- **La elección del [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) es parte de main-safety, no un detalle posterior.** I/O bloqueante en [`Default`]({{ "/es/glosario/dispatchers-default/" | relative_url }}) deja sin recursos al cómputo — [`Default`]({{ "/es/glosario/dispatchers-default/" | relative_url }}) tiene tantos threads como cores, y una lectura de socket estacionada secuestra uno. Loops de CPU en [`IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) son solo desperdicio. Aritmética de fechas sobre meses de reglas de recurrencia, ordenar miles de filas, parsear un JSON grande: [`Default`]({{ "/es/glosario/dispatchers-default/" | relative_url }}). Leer ese JSON del disco: [`IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}). Una misma función puede hacer las dos cosas legítimamente, en dos bloques [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}).
- **Main-safe no significa rápido.** Una función main-safe puede tardar igual diez segundos; solo que no congela la UI mientras tanto. El usuario sigue viendo un spinner diez segundos. Main-safety elimina el [jank]({{ "/es/glosario/jank/" | relative_url }}) y los [ANR]({{ "/es/glosario/anr/" | relative_url }}) — no elimina la necesidad de caché, paginación o un indicador de progreso. Confundir las dos cosas lleva a "agregué `withContext(IO)`, ¿por qué la pantalla sigue lenta?".
- **Bloquear *dentro* de una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) en Main es el [ANR]({{ "/es/glosario/anr/" | relative_url }}) moderno.** [`runBlocking`]({{ "/es/glosario/run-blocking/" | relative_url }}) en Main, [`Thread.sleep`]({{ "/es/glosario/thread/" | relative_url }}), un [`CountDownLatch.await()`]({{ "/es/glosario/count-down-latch/" | relative_url }}), un `Task.getResult()` síncrono de Play Services, [`MobileAds.initialize()`]({{ "/es/glosario/sdk/" | relative_url }}) — todos estacionan el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) *desde adentro de una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) perfectamente válida*. Structured Concurrency no ayuda acá; solo mover la llamada a un [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) de fondo ayuda. Y como los bootstraps de [SDK]({{ "/es/glosario/sdk/" | relative_url }}) suelen esconder 500 ms de trabajo síncrono detrás de una API con [callback]({{ "/es/glosario/callbacks/" | relative_url }}) que parece asíncrona, la jugada senior es medir, no confiar en la firma.
- **Compose tiene la misma regla con otra ortografía.** [`LaunchedEffect`]({{ "/es/glosario/launched-effect/" | relative_url }}) y [`produceState`]({{ "/es/glosario/produce-state/" | relative_url }}) corren en Main. Una [blocking call]({{ "/es/glosario/blocking-call/" | relative_url }}) adentro bloquea la composición. `produceState { value = withContext(IO) { load() } }` es la versión [composable]({{ "/es/glosario/composable/" | relative_url }}) de una llamada main-safe a un repositorio.
- **Los [dispatchers]({{ "/es/glosario/dispatcher/" | relative_url }}) inyectados hacen testeable la main-safety.** Hardcodear [`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) ata el salto a un [thread pool]({{ "/es/glosario/thread-pool/" | relative_url }}) real que [`runTest`]({{ "/es/glosario/run-test/" | relative_url }}) no puede controlar. Inyectar un [`@IoDispatcher`]({{ "/es/glosario/io-dispatcher/" | relative_url }}) deja que el test sustituya un [`TestDispatcher`]({{ "/es/glosario/test-dispatcher/" | relative_url }}) y maneje el trabajo "de fondo" en tiempo virtual — probando que la función suspende donde dice que suspende.

## Code in Action

### La forma canónica: `withContext` como cuerpo de la función

`BackupManager` lee y escribe archivos a través del [`ContentResolver`]({{ "/es/glosario/content-resolver/" | relative_url }}). Cada [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) pública es main-safe porque el cambio a [`IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) *es* su cuerpo — ningún llamador puede olvidarlo.

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

suspend fun importFrom(uri: Uri): Result<Unit> = withContext(Dispatchers.IO) { /* ... */ }
```

Fijate qué hay adentro: `openOutputStream`, `stream.write` y la serialización JSON — todo síncrono, todo bloqueante. Las llamadas `backupDao.getAll*()` son métodos [`suspend`]({{ "/es/glosario/suspend-functions/" | relative_url }}) de [Room]({{ "/es/glosario/room/" | relative_url }}) y serían main-safe por sí solas; envolverlas en el mismo bloque [`IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) está bien porque el *resto* del bloque realmente lo necesita, y porque [`IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) y el executor de [Room]({{ "/es/glosario/room/" | relative_url }}) son threads de fondo de todos modos.

### Cambiar solo alrededor de la parte que bloquea

`LegacyDataImporter` mezcla tres tipos de trabajo: lecturas de [DataStore]({{ "/es/glosario/datastore/" | relative_url }}) (ya main-safe), inserts de [Room]({{ "/es/glosario/room/" | relative_url }}) (ya main-safe), y operaciones crudas sobre archivos (no). Envuelve *solo* las operaciones sobre archivos.

```kotlin
// From FollowApp Suite — LegacyDataImporter.kt
suspend fun runIfNeeded() {
    if (preferences.isImportDoneOnce()) return          // DataStore: main-safe

    if (!reader.legacyDatabaseExists()) {
        preferences.markImportDone()
        return
    }

    runCatching {
        val legacyTasks = withContext(Dispatchers.IO) { reader.readLegacyTasks() }   // raw SQLite read
        if (legacyTasks.isNotEmpty()) {
            val now = System.currentTimeMillis()
            taskDao.insertTasks(                                                      // Room: main-safe
                legacyTasks.mapIndexed { index, task -> task.toTaskEntity(index, now) }
            )
        }
        preferences.markImportDone()
        withContext(Dispatchers.IO) { archiveLegacyFile() }                          // File.renameTo
        Log.d(TAG, "Legacy import complete: ${legacyTasks.size} task(s)")
    }.onFailure { e ->
        Log.e(TAG, "Legacy import failed; will retry next launch", e)
    }
}
```

Esto es main-safety aplicada con precisión: dos bloques [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}) alrededor de las dos llamadas que estacionan un thread, y nada alrededor de las llamadas que ya cumplen el contrato. Algo que un revisor marcaría: `reader.legacyDatabaseExists()` es un `File.exists()` — un stat de disco — corriendo en el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) del llamador. Es barato, pero es una [blocking call]({{ "/es/glosario/blocking-call/" | relative_url }}) fuera de un cambio de [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}), y el comentario de arriba ("paid only once") es el autor reconociendo el trade-off.

### El trabajo de CPU no está exento

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

Acá no hay I/O — pura aritmética de fechas — y aun así salta, a [`Default`]({{ "/es/glosario/dispatchers-default/" | relative_url }}). El comentario nombra el modo de fallo exacto: el despacho de input se traba, y una traba lo bastante larga con un popup abierto es un [ANR]({{ "/es/glosario/anr/" | relative_url }}). Main-safety trata del *tiempo en Main*, no del tipo de trabajo que lo consume.

### Main-safety en Compose: `produceState`

```kotlin
// From FollowApp Suite — AboutScreen.kt
val licenses by produceState<List<License>?>(initialValue = null, key1 = context) {
    value = withContext(Dispatchers.IO) { loadLicenses(context) }
}
```

[`produceState`]({{ "/es/glosario/produce-state/" | relative_url }}) lanza una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) en el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) de la composición — Main. `loadLicenses` lee un raw resource y lo parsea: bloqueante. El [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}) es lo que evita que el primer frame de la pantalla About espere al disco. Sin él la pantalla igual *terminaría* renderizando — pero solo después de congelarse al entrar.

### Cómo se ve "ya main-safe"

```kotlin
// From FollowApp Suite — LabelDao.kt
@Dao
interface LabelDao {
    @Query("SELECT * FROM labels ORDER BY name ASC")
    fun getLabelsStream(): Flow<List<LabelEntity>>

    @Query("SELECT * FROM labels WHERE name = :name LIMIT 1")
    suspend fun getLabelByName(name: String): LabelEntity?

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insertLabel(label: LabelEntity): Long
}
```

```kotlin
// From FollowApp Suite — LegacyImportPreferences.kt
fun isImportDone(): Flow<Boolean> = dataStore.data.map { it[importDoneKey] ?: false }
suspend fun isImportDoneOnce(): Boolean = isImportDone().first()
```

Ninguno de los dos archivos menciona un [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}), y ninguno lo necesita. [Room]({{ "/es/glosario/room/" | relative_url }}) corre cada método [`suspend`]({{ "/es/glosario/suspend-functions/" | relative_url }}) del [DAO]({{ "/es/glosario/dao/" | relative_url }}) en su executor de queries/transacciones y cada query [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) en un observer de fondo; [DataStore]({{ "/es/glosario/datastore/" | relative_url }}) hace sus lecturas en [`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) internamente. Son las librerías cumpliendo el contrato para que el código de arriba pueda quedar libre de [dispatchers]({{ "/es/glosario/dispatcher/" | relative_url }}). Envolver `insertLabel` en `withContext(IO)` no agregaría nada más que ruido.

### La blocking call que se esconde detrás de un callback

```kotlin
// From FollowApp Suite — ConsentManager.kt
// MobileAds.initialize does ~700 ms of synchronous SDK bootstrap on
// the caller thread even though it exposes an async callback.
CoroutineScope(SupervisorJob() + Dispatchers.IO).launch {
    MobileAds.initialize(app)
}
```

`MobileAds.initialize(context, listener)` *parece* asíncrono — recibe un listener de completitud. La medición del comentario dice otra cosa: 700 ms de trabajo síncrono en el thread que lo llame. Llamado desde [`Application.onCreate()`]({{ "/es/glosario/application-on-create/" | relative_url }}) son 700 ms sumados al cold start y, en un dispositivo lento, un [ANR]({{ "/es/glosario/anr/" | relative_url }}). El arreglo es el mismo que para cualquier [blocking call]({{ "/es/glosario/blocking-call/" | relative_url }}): moverlo a [`IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}). La lección es que main-safety se decide con [profiling]({{ "/es/glosario/profiling/" | relative_url }}), no leyendo firmas.

### Hacer testeable el salto — Not found in FAS

`BackupManager` hardcodea [`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}). Sus tests, por lo tanto, corren el pool real. La forma inyectada:

```kotlin
// Not found in FAS — standalone example
class BackupManager @Inject constructor(
    @IoDispatcher private val io: CoroutineDispatcher,
    /* ... */
) {
    suspend fun exportTo(uri: Uri): Result<Unit> = withContext(io) { /* ... */ }
}

@Test
fun `exportTo is main-safe`() = runTest {
    val io = StandardTestDispatcher(testScheduler)
    val manager = BackupManager(io = io, /* ... */)
    val job = launch { manager.exportTo(uri) }
    // the function has suspended at withContext(io); nothing ran on the caller yet
    assertTrue(job.isActive)
    advanceUntilIdle()
    assertTrue(job.isCompleted)
}
```

El test puede *observar la suspensión*: después del [`launch`]({{ "/es/glosario/launch/" | relative_url }}), el cuerpo no se ejecutó porque el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) inyectado no fue avanzado. Una función que bloqueara en vez de cambiar de [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) habría completado sincrónicamente — que es exactamente el bug que este test existe para atrapar.

## The Interview (En el banquillo)

**Pregunta**: ¿Qué significa "main-safe", de quién es la responsabilidad, y marcar una función como [`suspend`]({{ "/es/glosario/suspend-functions/" | relative_url }}) la hace main-safe?

**Respuesta Senior**: Una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) es main-safe cuando llamarla desde el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) nunca bloquea ese thread — puede tardar mucho, pero solo *suspende*, así que la UI sigue dibujando y manejando input mientras el trabajo ocurre en un [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) de fondo. Es responsabilidad del *llamado*, porque el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) se hereda: una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) corre en el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) que tenía su llamador, así que si el llamador es [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) en Main y la función lee un archivo sin cambiar de [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}), Main se bloquea. Poner [`withContext(Dispatchers.IO)`]({{ "/es/glosario/with-context/" | relative_url }}) *adentro* de la función que hace el trabajo bloqueante — una sola vez — hace la garantía local y significa que ningún llamador tiene que acordarse. La convención del ecosistema es que toda [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) es main-safe; [Room]({{ "/es/glosario/room/" | relative_url }}), [Retrofit]({{ "/es/glosario/retrofit/" | relative_url }}) y [DataStore]({{ "/es/glosario/datastore/" | relative_url }}) la cumplen, así que nunca envuelvo sus llamadas, y solo escribo [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}) alrededor de I/O crudo, CPU pesada o un [SDK]({{ "/es/glosario/sdk/" | relative_url }}) síncrono. Y no, [`suspend`]({{ "/es/glosario/suspend-functions/" | relative_url }}) no hace main-safe a nada: es una promesa sobre cómo se puede *llamar* la función, no sobre dónde corre. `suspend fun load() = File(p).readText()` compila, pasa los tests sobre un [`TestDispatcher`]({{ "/es/glosario/test-dispatcher/" | relative_url }}), y bloquea Main en producción durante toda la lectura — porque no hay ningún [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}) adentro. La pregunta que le hago a cada [`suspend fun`]({{ "/es/glosario/suspend-functions/" | relative_url }}) que toca disco, red o un loop grande es "¿dónde está el cambio de [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }})?", y si no está en la función, la función no es main-safe.

**Pregunta**: Heredás un repositorio cuyas [suspend functions]({{ "/es/glosario/suspend-functions/" | relative_url }}) bloquean el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}). Contame cómo lo arreglás, y cómo probarías el arreglo en un test.

**Respuesta Senior**: Primero encuentro *qué* llamadas bloquean, con [profiling]({{ "/es/glosario/profiling/" | relative_url }}) y no leyendo — un bootstrap síncrono de [SDK]({{ "/es/glosario/sdk/" | relative_url }}) o un `File.exists()` pueden esconderse detrás de una firma inocente, y un método que recibe un [callback]({{ "/es/glosario/callbacks/" | relative_url }}) igual puede hacer cientos de milisegundos de trabajo síncrono antes de retornar. Después, para cada [blocking call]({{ "/es/glosario/blocking-call/" | relative_url }}), envuelvo la *parte bloqueante* — no toda la función — en [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}) con el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) que corresponde al trabajo: [`IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) para todo lo que estaciona un thread en disco o red, [`Default`]({{ "/es/glosario/dispatchers-default/" | relative_url }}) para todo lo que quema CPU como parsear o hacer aritmética de fechas. Dejo sin envolver las llamadas a [Room]({{ "/es/glosario/room/" | relative_url }}), [Retrofit]({{ "/es/glosario/retrofit/" | relative_url }}) y [DataStore]({{ "/es/glosario/datastore/" | relative_url }}), porque ya son main-safe y envolver dos veces es ruido que confunde al próximo lector. Inyecto los [dispatchers]({{ "/es/glosario/dispatcher/" | relative_url }}) con un qualifier como [`@IoDispatcher`]({{ "/es/glosario/io-dispatcher/" | relative_url }}) en vez de hardcodear [`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}), porque eso es lo que hace demostrable el arreglo. En el test uso [`runTest`]({{ "/es/glosario/run-test/" | relative_url }}), paso un `StandardTestDispatcher(testScheduler)` como [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) inyectado, hago [`launch`]({{ "/es/glosario/launch/" | relative_url }}) de una llamada a la función, y afirmo *antes* de avanzar el scheduler que el job sigue activo y que el I/O falso no fue tocado — eso prueba que la función suspendió en el cambio de [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) en vez de bloquear de largo. Después [`advanceUntilIdle()`]({{ "/es/glosario/advance-until-idle/" | relative_url }}) y afirmo el resultado. Una función que siguiera bloqueando habría corrido hasta completar sincrónicamente dentro del [`launch`]({{ "/es/glosario/launch/" | relative_url }}) en [`Main.immediate`]({{ "/es/glosario/dispatchers-main-immediate/" | relative_url }}), y la primera aserción fallaría. Lo último que diría es que main-safe no es lo mismo que rápido: después del arreglo la UI ya no se congela, pero si la operación tarda tres segundos el usuario sigue necesitando un indicador de progreso, y eso es un trabajo aparte.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
