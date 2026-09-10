---
layout: page
title: Suspend Functions
lang: es
permalink: /es/02-coroutines-flow/suspend-functions/
order: 1
---

## The Theory (El Qué)

Una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) (función suspendible) es una función marcada con el [keyword]({{ "/es/glosario/keyword/" | relative_url }}) `suspend` que puede pausar su ejecución en un [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}) y reanudarla después — posiblemente en otro [thread]({{ "/es/glosario/thread/" | relative_url }}) — sin bloquear el thread en el que corría. Es la unidad de composición de las [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) de Kotlin: todo lo demás (`launch`, `async`, `Flow`, `withContext`) está construido encima.

- **`suspend` es un contrato de [compile time]({{ "/es/glosario/compile-time/" | relative_url }}), no un thread.** Marcar una función como `suspend` no la mueve a ningún lado. Corre en el thread que la llamó hasta que llega a un suspension point. Lo único que cambia el modificador es *quién puede llamarla*: otra suspend function o un coroutine builder. El compilador lo exige — llamar una suspend function desde código común es un error de compilación, y ese es justamente el punto.
- **El compilador la reescribe en [Continuation-Passing Style]({{ "/es/glosario/continuation-passing-style/" | relative_url }}).** `suspend fun load(id: String): Task` se convierte, en [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}), en `fun load(id: String, cont: Continuation<Task>): Any?`. El parámetro extra es la [continuation]({{ "/es/glosario/continuation/" | relative_url }}): un [callback]({{ "/es/glosario/callbacks/" | relative_url }}) que sabe cómo reanudar al llamador con un resultado o una excepción. El [return type]({{ "/es/glosario/return-type/" | relative_url }}) pasa a ser `Any?` porque la función devuelve o bien el valor real *o bien* un marcador centinela `COROUTINE_SUSPENDED` que significa "me pausé, voy a llamar a la continuation más tarde".
- **El cuerpo se convierte en una [state machine]({{ "/es/glosario/state-machine/" | relative_url }}).** Cada suspension point recibe una etiqueta; las variables locales que tienen que sobrevivir a una suspensión se suben a campos del objeto continuation (en el [heap]({{ "/es/glosario/heap/" | relative_url }}), no en el [stack]({{ "/es/glosario/stack-frame/" | relative_url }})). Cuando la función se reanuda, un `when(label)` salta directo al punto correcto. Por eso una coroutine suspendida cuesta unos cientos de bytes en lugar del megabyte de stack de un thread.
- **Suspender no es lo mismo que [bloquear]({{ "/es/glosario/blocking-call/" | relative_url }}).** Una llamada bloqueante — `Thread.sleep`, un `InputStream.read` síncrono, un `runBlocking` — detiene el *thread*. Una llamada suspendible devuelve el thread a su [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) para que pueda correr otras coroutines. Envolver una llamada bloqueante en una `suspend fun` no la hace suspender; solo lo hace una función que *realmente* suspende (`delay`, `withContext`, una llamada a un [DAO]({{ "/es/glosario/dao/" | relative_url }}) de Room, `suspendCancellableCoroutine`).
- **Secuencial por defecto.** Dentro de una suspend function, una línea corre después de la otra, exactamente como se lee. La concurrencia es opt-in — hay que pedirla con `async` o `launch` dentro de un [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}). Es el inverso de las APIs de [callbacks]({{ "/es/glosario/callbacks/" | relative_url }}), donde el secuenciamiento es lo que cuesta trabajo.

## The Senior Perspective (El Porqué)

- **El modificador es documentación que el compilador verifica.** Cuando un método de una interfaz de repositorio dice `suspend`, le dice a cada llamador "esto puede tardar y necesitás un scope para llamarme". Cuando *no* dice `suspend`, promete devolver de inmediato. Las interfaces de repositorio de FAS separan las dos cosas limpiamente: `Flow<T>` para streams, `suspend fun` para operaciones one-shot, `fun` común para nada que toque I/O. Un reviewer puede detectar una violación del main thread solo desde la firma — una `fun` común que internamente hace trabajo de disco es un bug que se ve sin leer el cuerpo.
- **Las suspend functions deberían ser main-safe.** La convención en Android es que una suspend function se puede llamar desde `Dispatchers.Main` sin pensarlo. Eso significa que la función misma es responsable de sacar el trabajo bloqueante del main thread — `withContext(Dispatchers.IO)` *adentro* de la función, no en cada call site. Room y Retrofit ya lo hacen por vos: sus métodos `suspend` de DAO/service saltan a su propio [thread pool]({{ "/es/glosario/thread-pool/" | relative_url }}) y te reanudan de vuelta. Tu propio código de archivos o JSON no, y por eso `BackupManager` envuelve su cuerpo en `withContext(Dispatchers.IO)`.
- **La cancelación es cooperativa, y la suspensión es donde ocurre.** Una coroutine se cancela solo cuando llega a un suspension point (o chequea `isActive`/`ensureActive()` explícitamente). Cada llamada suspendible real — `delay`, `withContext`, `Flow.collect`, una query de DAO — verifica cancelación antes y después de suspender y lanza [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}). Una suspend function que solo hace trabajo de CPU en un loop sin suspender nunca es incancelable; va a seguir corriendo después de que el [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) que la lanzó ya no exista. La [cooperative cancellation]({{ "/es/glosario/cooperative-cancellation/" | relative_url }}) es el precio de no ser matado a la fuerza en medio de una escritura.
- **Nunca tragarse `CancellationException`.** Tanto `runCatching { }` como `catch (e: Exception)` la atrapan, lo que convierte una coroutine cancelada en una que sigue silenciosamente más allá del punto donde debía morir. La regla: atrapá lo que podés manejar, relanzá `CancellationException`. El handler de gesto de drag de FAS hace exactamente eso — atrapa para resetear estado local, y relanza.
- **[`runBlocking`]({{ "/es/glosario/run-blocking/" | relative_url }}) es el puente, no el patrón.** Existe para llamar código suspendible desde un lugar que no tiene coroutine: `main()`, un test de JUnit, y — muy deliberadamente — `Application.onCreate` cuando *necesitás* un valor antes del primer frame. Cada uso en código de producción debería venir con un comentario que explique por qué bloquear al llamador es aceptable. FAS tiene dos, ambos con un párrafo de justificación y un número de issue.
- **Puentear callbacks es un costo de una sola vez.** [`suspendCancellableCoroutine`]({{ "/es/glosario/suspend-cancellable-coroutine/" | relative_url }}) convierte cualquier API basada en [callbacks]({{ "/es/glosario/callbacks/" | relative_url }}) en una suspend function una vez, en el borde; de ahí en adelante el resto del codebase es secuencial. Las librerías de Jetpack ya lo hicieron por vos (el `getCredential` de Credential Manager es suspend; `Task.await()` para Play Services), y por eso el código Android moderno casi no tiene [callback hell]({{ "/es/glosario/callback-hell/" | relative_url }}).
- **`suspend` en una lambda es un tipo, no solo un modificador.** `suspend () -> Unit` es un tipo de función distinto; una [higher-order function]({{ "/es/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) que lo acepta puede llamar código suspendible dentro de la lambda. `withContext`, `coroutineScope`, `withTransaction` y `launch` reciben suspend lambdas — así es como te dejan suspender dentro de su bloque.

## Code in Action

### La firma es el contrato

El [DAO]({{ "/es/glosario/dao/" | relative_url }}) separa lo que es un stream de lo que es una operación one-shot. `getLabelsStream` devuelve un `Flow` y *no* es suspend — suscribirse no cuesta nada. Cada escritura y lectura puntual es `suspend`, y [Room]({{ "/es/glosario/room/" | relative_url }}) genera la implementación que corre la query en su propio executor y reanuda al llamador.

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

    @Query("UPDATE labels SET name = :name, updated_at = :updatedAt WHERE id = :labelId")
    suspend fun renameLabel(labelId: String, name: String, updatedAt: String)

    @Query("DELETE FROM labels WHERE id = :labelId")
    suspend fun deleteLabel(labelId: String)
}
```

Como son main-safe, el [ViewModel]({{ "/es/glosario/viewmodel-store/" | relative_url }}) puede llamarlos desde [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) (que por defecto usa `Dispatchers.Main.immediate`) sin cambiar de dispatcher.

### Código secuencial que se lee como una historia

Un use case compone varias llamadas suspendibles en orden. No hay callbacks anidados, no hay `then`, no hay thread explícito — y si el scope que lo contiene se cancela entre el paso uno y el dos, el paso dos simplemente nunca corre.

```kotlin
// From FollowApp Suite — QuickCompleteTaskUseCase.kt
suspend operator fun invoke(taskId: String, isCompleted: Boolean, cascade: Boolean = false) {
    taskRepository.updateTaskCompletion(taskId = taskId, isCompleted = isCompleted)
    if (cascade) {
        taskRepository.updateDescendantsCompletion(taskId = taskId, isCompleted = isCompleted)
    }
    if (isCompleted) {
        spawnNextOccurrence(taskId)
    }
}
```

Cada línea es un [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}). El compilador genera una [state machine]({{ "/es/glosario/state-machine/" | relative_url }}) con tres etiquetas; `taskId`, `isCompleted` y `cascade` se guardan en la [continuation]({{ "/es/glosario/continuation/" | relative_url }}) para sobrevivir a cada suspensión.

### Hacer main-safe una suspend function

Escribir un archivo es I/O [bloqueante]({{ "/es/glosario/blocking-call/" | relative_url }}). `BackupManager` asume esa responsabilidad dentro de la función, así los llamadores en Main no tienen que saberlo.

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

`LegacyDataImporter` es más quirúrgico: solo se envuelven las dos llamadas genuinamente bloqueantes, y el insert del DAO — que ya es main-safe — se queda en el dispatcher del llamador.

```kotlin
// From FollowApp Suite — LegacyDataImporter.kt
suspend fun runIfNeeded() {
    if (preferences.isImportDoneOnce()) return
    // ...
    runCatching {
        val legacyTasks = withContext(Dispatchers.IO) { reader.readLegacyTasks() }
        if (legacyTasks.isNotEmpty()) {
            val now = System.currentTimeMillis()
            taskDao.insertTasks(
                legacyTasks.mapIndexed { index, task -> task.toTaskEntity(index, now) }
            )
        }
        preferences.markImportDone()
        withContext(Dispatchers.IO) { archiveLegacyFile() }
    }.onFailure { e ->
        Log.e(TAG, "Legacy import failed; will retry next launch", e)
    }
}
```

Lo mismo aplica al trabajo pesado de CPU. La aritmética de fechas sobre meses de patrones de recurrencia no es I/O, pero igual frenaría el input en Main, así que el [ViewModel]({{ "/es/glosario/viewmodel-store/" | relative_url }}) salta a `Dispatchers.Default`:

```kotlin
// From FollowApp Suite — TasksViewModel.kt
viewModelScope.launch {
    // Date math off the main thread: pattern scans over months/years
    // must never stall input dispatching (popup ANR)
    val suggested = withContext(Dispatchers.Default) {
        val settings = getRecurrenceSettingsUseCase().first()
        // ... RecurrenceCalculator.suggestPatternDueDate(...)
    }
    // de vuelta en Main acá
}
```

### Suspend no significa secuencial cuando pedís concurrencia

Completar veinte tareas seleccionadas una detrás de otra serían veinte round-trips. [`coroutineScope`]({{ "/es/glosario/coroutine-scope-builder/" | relative_url }}) es en sí una suspend function: lanza los hijos, suspende hasta que *todos* terminan, y relanza si alguno falla. El `finally` corre exactamente una vez, después de que cada escritura terminó.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
isBulkWriteInFlight = true
try {
    coroutineScope {
        ids.forEach { launch { quickCompleteTaskUseCase(taskId = it, isCompleted = isCompleted) } }
    }
} finally {
    isBulkWriteInFlight = false
}
```

### Relanzar la cancelación

Una coroutine de pointer input se descarta cada vez que el composable sale de la composición. El handler atrapa [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}) solo para limpiar el estado local del drag, y luego relanza para que la maquinaria de coroutines siga viendo la cancelación.

```kotlin
// From FollowApp Suite — DragToReorder.kt
} catch (e: CancellationException) {
    // Gesture coroutine disposed mid-drag (e.g. composition change)
    state.endDrag(cancelled = true)
    throw e
}
```

Compará con el flujo de sign-in, que atrapa una cancelación de *dominio* (el usuario cerró el selector) y deliberadamente la trata como no-error — otro tipo de excepción, otra decisión:

```kotlin
// From FollowApp Suite — SettingsViewModel.kt
viewModelScope.launch {
    try {
        val session = googleAuthClient.signIn(activityContext)
        saveUserSessionUseCase(session)
    } catch (e: GetCredentialCancellationException) {
        Log.d(TAG, "Google sign-in cancelled by user")
    } catch (e: GetCredentialException) {
        _uiState.update { it.copy(messageRes = R.string.error_sign_in) }
    }
}
```

### `runBlocking` — la excepción justificada

`Application.onCreate` no tiene coroutine y *necesita* conocer el locale y el tema antes de que la primera Activity se infle, o el usuario ve un flash. Es el único lugar donde FAS bloquea el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) con código suspendible, y el comentario explica por qué.

```kotlin
// From FollowApp Suite — MyTasksApplication.kt
// All three values live in the same "settings" DataStore — reading
// them in a single runBlocking triggers exactly one cold file open.
val (language, themeMode, contrastLevel) = runBlocking {
    Triple(
        languagePreferences.getLanguage().first(),
        themePreferences.getThemeMode().first(),
        themePreferences.getContrastLevel().first()
    )
}
```

### Puentear una API de callbacks

FAS consume APIs que Jetpack ya envolvió (`CredentialManager.getCredential` es suspend). Cuando el envoltorio es tuyo, esta es la forma:

```kotlin
// Not found in FAS — standalone example
suspend fun LocationClient.awaitLastLocation(): Location? =
    suspendCancellableCoroutine { cont ->
        val listener = object : LocationListener {
            override fun onSuccess(loc: Location?) = cont.resume(loc)
            override fun onFailure(e: Exception) = cont.resumeWithException(e)
        }
        requestLastLocation(listener)
        cont.invokeOnCancellation { removeListener(listener) }
    }
```

Tres obligaciones: reanudar exactamente una vez, propagar el fallo, y desregistrar en la cancelación. Si te olvidás la tercera, una coroutine cancelada filtra el listener; si te olvidás la primera, el llamador se cuelga para siempre.

### Lo que genera el compilador

```kotlin
// Not found in FAS — standalone example (simplified decompilation)
suspend fun load(id: String): Task {
    val raw = fetch(id)        // suspension point 1
    val parsed = parse(raw)    // suspension point 2
    return parsed
}

// se convierte, aproximadamente, en:
fun load(id: String, cont: Continuation<Task>): Any? {
    val sm = cont as? LoadSM ?: LoadSM(cont)
    when (sm.label) {
        0 -> { sm.label = 1; val r = fetch(id, sm); if (r == COROUTINE_SUSPENDED) return r; sm.raw = r }
        1 -> { sm.raw = sm.result }
    }
    when (sm.label) {
        1 -> { sm.label = 2; val p = parse(sm.raw, sm); if (p == COROUTINE_SUSPENDED) return p; return p }
        2 -> return sm.result
    }
}
```

Sin threads, sin magia: una función que devuelve temprano con un marcador, y un objeto que recuerda dónde retomar. Todo lo que una coroutine "hace" se reduce a esto.

## The Interview (En el banquillo)

**Pregunta**: ¿Qué hace realmente el keyword `suspend`?

**Respuesta Senior**: Cambia la firma de la función en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}) y nada sobre dónde corre. El compilador reescribe la función en [Continuation-Passing Style]({{ "/es/glosario/continuation-passing-style/" | relative_url }}): gana un parámetro oculto `Continuation<T>` y su return type pasa a ser `Any?`, para poder devolver o bien el resultado real o bien el marcador `COROUTINE_SUSPENDED`. El cuerpo se compila a una [state machine]({{ "/es/glosario/state-machine/" | relative_url }}) cuyas etiquetas son los [suspension points]({{ "/es/glosario/suspension-point/" | relative_url }}); las locales que cruzan una suspensión se suben al objeto [continuation]({{ "/es/glosario/continuation/" | relative_url }}) en el [heap]({{ "/es/glosario/heap/" | relative_url }}). Cuando una llamada realmente suspende, la función devuelve el marcador, el [thread]({{ "/es/glosario/thread/" | relative_url }}) vuelve a su [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}), y más tarde algo llama `continuation.resume(value)`, que reentra a la función y salta a la etiqueta correcta. Por eso una suspend function necesita ser llamada desde una coroutine — necesita una continuation que entregar. Dos consecuencias importan en la práctica: `suspend` no hace no-bloqueante a una [llamada bloqueante]({{ "/es/glosario/blocking-call/" | relative_url }}), solo lo hacen los suspension points reales; y una suspend function que nunca llega a un suspension point nunca puede ser cancelada, porque la [cancelación]({{ "/es/glosario/cooperative-cancellation/" | relative_url }}) se verifica en esos puntos.

**Pregunta**: Un compañero envuelve `File.readText()` en una `suspend fun` y la llama desde `viewModelScope.launch`. La UI se sigue congelando. ¿Por qué, y qué cambiás?

**Respuesta Senior**: Porque `suspend` es un contrato sobre *quién puede llamarte*, no un cambio de thread. [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) corre en `Dispatchers.Main.immediate`, la función corre en ese thread hasta llegar a un suspension point real, y `readText()` es una [llamada bloqueante]({{ "/es/glosario/blocking-call/" | relative_url }}) — nunca suspende, así que detiene el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) durante toda la lectura. El fix es hacer la función *main-safe*: envolver el cuerpo bloqueante en `withContext(Dispatchers.IO)` dentro de la propia suspend function, como hace `BackupManager`, para que cada llamador — el ViewModel, un test, un worker de WorkManager — obtenga el comportamiento correcto sin saber nada de I/O. No pondría el `withContext` en el call site, porque el próximo llamador se lo olvida. Y verificaría que el código de alrededor no haga `runCatching` de todo, porque eso se traga la [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}) y convierte una pantalla cancelada en una coroutine que sigue escribiendo a disco después de que el ViewModel fue limpiado.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
