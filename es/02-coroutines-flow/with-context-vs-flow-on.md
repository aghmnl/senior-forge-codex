---
layout: page
title: "withContext vs flowOn"
lang: es
permalink: /es/02-coroutines-flow/with-context-vs-flow-on/
order: 6
---

## The Theory (El Qué)

Tanto [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}) como [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) mueven trabajo a un [`Dispatcher`]({{ "/es/glosario/dispatcher/" | relative_url }}) distinto. No son intercambiables, porque operan sobre cosas distintas: `withContext` sobre **una llamada suspendible**, [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) sobre **un stream**.

[`withContext(context) { }`]({{ "/es/glosario/with-context/" | relative_url }}) es una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}). Suspende la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) llamadora, corre el bloque en [`context`]({{ "/es/glosario/coroutine-context/" | relative_url }}), y reanuda al llamador — en su contexto original — con el único valor que devolvió el bloque. Es imperativo y ocurre *ahora*: el [contexto]({{ "/es/glosario/coroutine-context/" | relative_url }}) se cambia por la duración de ese bloque y se restaura después. Este es el mecanismo detrás de [Main-Safety]({{ "/es/02-coroutines-flow/main-safety/" | relative_url }}) para trabajo de una sola vez.

[`flowOn(context)`]({{ "/es/glosario/flow-on/" | relative_url }}) es un operador de [`Flow`]({{ "/es/glosario/flow/" | relative_url }}). Cambia el contexto de todo lo que está [upstream]({{ "/es/glosario/upstream/" | relative_url }}) de él — el builder y los operadores declarados más arriba — y deja todo lo [downstream]({{ "/es/glosario/downstream/" | relative_url }}) corriendo en el contexto del colector. Es declarativo: escribirlo no cambia nada hasta que alguien [colecta]({{ "/es/glosario/collect/" | relative_url }}) el flow, y aplica a *todos* los valores que el flow vaya a emitir, no a una llamada puntual.

La razón por la que [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) tiene que existir es la [preservación del contexto]({{ "/es/glosario/context-preservation/" | relative_url }}): un flow tiene que [emitir]({{ "/es/glosario/emit/" | relative_url }}) desde el mismo contexto en el que es colectado. Así que el movimiento obvio — envolver la emisión — es ilegal:

```kotlin
// Lanza IllegalStateException: "Flow invariant is violated"
flow { withContext(Dispatchers.IO) { emit(readFile()) } }
```

[`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) es la alternativa autorizada. No envuelve una emisión; re-aloja todo el upstream en otra coroutine y pasa los valores a través de un channel — que es también la razón por la que [bufferea]({{ "/es/glosario/buffer/" | relative_url }}) como efecto secundario.

## The Senior Perspective (El Porqué)

- **La decisión la toma el tipo de retorno, no el gusto.** Una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) que devuelve `T` usa [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}); una función que devuelve `Flow<T>` usa [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}). Meter `withContext` adentro de un builder `flow { }` no es una elección de estilo — es un crash en runtime esperando la primera emisión, y compila perfecto.
- **[`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) es solo upstream, y la posición es la API.** Los operadores escritos después corren donde corra el colector. Esa asimetría es una feature: poné el parseo caro y el I/O arriba del [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}), dejá abajo el mapeo barato que alimenta el estado de UI, y describiste un pipeline de dos threads en una línea. Escribir [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) al final de una cadena en un ViewModel — costumbre común — mueve la cadena *entera* fuera de Main, incluido el mapeo que debía correr ahí.
- **[`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) cambia la concurrencia, no solo el threading.** [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}) es una entrega en mano: el llamador espera. [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) inserta un channel, así que el productor puede adelantarse al colector — el mismo comportamiento que [`buffer`]({{ "/es/glosario/buffer/" | relative_url }}). Eso hace los pipelines más rápidos y hace el timing de las emisiones menos predecible en los tests. Si un test empieza a fallar después de agregar un [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}), normalmente es por esto, y el arreglo es un [`TestDispatcher`]({{ "/es/glosario/test-dispatcher/" | relative_url }}) determinista, no un [`delay`]({{ "/es/glosario/delay/" | relative_url }}).
- **La mayoría de los flows en Android no necesitan ninguno de los dos.** Un `Flow` de un [DAO]({{ "/es/glosario/dao/" | relative_url }}) de [Room]({{ "/es/glosario/room/" | relative_url }}) ya emite en el executor propio de Room, [DataStore]({{ "/es/glosario/datastore/" | relative_url }}) lee en IO, y una llamada de [Retrofit]({{ "/es/glosario/retrofit/" | relative_url }}) suspende en el pool de [OkHttp]({{ "/es/glosario/okhttp/" | relative_url }}). Agregarles [`flowOn(Dispatchers.IO)`]({{ "/es/glosario/flow-on/" | relative_url }}) encima no compra nada, cuesta un channel, y le dice al próximo lector que la fuente no era [main-safe]({{ "/es/02-coroutines-flow/main-safety/" | relative_url }}) — lo cual es falso. Agregalo solo cuando el productor bloqueante lo escribiste *vos*.
- **Los dos van en la capa de datos.** La regla de [Main-Safety]({{ "/es/02-coroutines-flow/main-safety/" | relative_url }}) no cambia para los streams: la función que hace el trabajo bloqueante declara dónde corre. Un ViewModel que tiene que acordarse de [`.flowOn(IO)`]({{ "/es/glosario/flow-on/" | relative_url }}) en cada llamada al repositorio es un repositorio que rompió su contrato.
- **[`flowOn(Dispatchers.Main)`]({{ "/es/glosario/flow-on/" | relative_url }}) casi nunca significa lo que la gente cree.** No fuerza la colección a Main — eso lo decide el [scope]({{ "/es/glosario/coroutine-scope/" | relative_url }}) del colector. Fuerza al *productor* a Main, que es lo opuesto a lo que quiere cualquiera.

## Code in Action

```kotlin
// De FollowApp Suite — BackupManager.kt
// Una sola vez, devuelve un valor único → withContext. La escritura bloqueante
// vive adentro de la función, así que ningún llamador se acuerda del dispatcher.
suspend fun exportTo(uri: Uri): Result<Unit> = withContext(Dispatchers.IO) {
    runCatching {
        val json = jsonOf(content)
        context.contentResolver.openOutputStream(uri, "wt").use { stream ->
            requireNotNull(stream) { "Cannot open destination" }
            stream.write(json.toByteArray(Charsets.UTF_8))
        }
    }.onFailure { Log.e(TAG, "Backup export failed", it) }
}

// De FollowApp Suite — TasksViewModel.kt
// Aritmética de fechas (CPU) adentro de un launch → withContext(Default), no IO
viewModelScope.launch {
    // Date math off the main thread: pattern scans over months/years
    // must never stall input dispatching (popup ANR)
    val suggested = withContext(Dispatchers.Default) {
        val settings = getRecurrenceSettingsUseCase().first()
        RecurrenceCalculator.suggestPatternDueDate(rule, now, zone, settings.holidays)
    }
    _uiState.update { it.copy(form = it.form.copy(dueDate = suggested)) }
}

// De FollowApp Suite — TaskRepositoryImpl.kt
// Un stream — y deliberadamente SIN flowOn: Room ya emite fuera del main
// thread, y el mapeo es barato como para correr donde corra el colector.
override fun getActiveTasks(sort: ListSort): Flow<List<Task>> {
    return taskDao.getActiveTasksStream(sort.name).map { entities ->
        entities.map { it.toDomain() }
    }
}

// Not found in FAS — standalone example
// Un productor escrito por nosotros que hace I/O bloqueante: acá flowOn se gana su lugar.
fun importedFiles(dir: File): Flow<Backup> = flow {
    dir.listFiles().orEmpty().forEach { file ->
        emit(parseBackup(file.readText()))   // lectura bloqueante + parseo
    }
}.flowOn(ioDispatcher)                       // el upstream (leer + parsear) corre en IO

// Colectado desde el ViewModel: el mapeo de abajo queda en Main por diseño
viewModelScope.launch {
    importedFiles(dir)
        .map { it.toUiModel() }              // downstream: Main
        .collect { _uiState.value = it }     // downstream: Main
}
```

## The Interview (En el banquillo)

**Pregunta**: ¿Cuándo usás `withContext` y cuándo [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}), y qué pasa si usás `withContext` adentro de un builder `flow { }`?

**Respuesta Senior**: [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}) es para un cómputo suspendible único que devuelve un valor: suspende al llamador, corre el bloque en el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) destino, y reanuda al llamador en su contexto original. [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) es para un stream: es un operador declarativo que cambia el contexto de todo lo que está [upstream]({{ "/es/glosario/upstream/" | relative_url }}) de él y deja el [downstream]({{ "/es/glosario/downstream/" | relative_url }}) corriendo donde corra el colector. Así que la firma decide — `suspend fun T` lleva `withContext`, `fun Flow<T>` lleva [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}). Usar `withContext` alrededor de un [`emit`]({{ "/es/glosario/emit/" | relative_url }}) adentro de un `flow { }` compila y después lanza [`IllegalStateException: Flow invariant is violated`]({{ "/es/glosario/illegal-state-exception/" | relative_url }}) en la primera emisión, por la [preservación del contexto]({{ "/es/glosario/context-preservation/" | relative_url }}): un flow tiene que emitir desde el mismo contexto en el que es colectado, para que las emisiones sigan siendo secuenciales y las excepciones sigan siendo atribuibles. [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) es la forma autorizada de cruzar ese límite — re-aloja el upstream en su propia coroutine y pasa los valores por un channel. Dos consecuencias que mencionaría: la posición importa, porque [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) solo afecta lo que está escrito arriba, así que lo pongo inmediatamente después del productor bloqueante y dejo abajo el mapeo barato para la UI; y [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) implica un [buffer]({{ "/es/glosario/buffer/" | relative_url }}), así que también cambia la concurrencia — el productor puede adelantarse al colector, lo que normalmente es una ganancia pero hace el timing de las emisiones menos predecible en los tests.

**Pregunta**: Un compañero agrega [`.flowOn(Dispatchers.IO)`]({{ "/es/glosario/flow-on/" | relative_url }}) a todas las funciones del repositorio que devuelven `Flow`, incluidas las que vienen de Room. ¿Qué le decís?

**Respuesta Senior**: Que la mayoría son redundantes y que alguna puede estar en el lugar equivocado. Un `Flow` de un [DAO]({{ "/es/glosario/dao/" | relative_url }}) de [Room]({{ "/es/glosario/room/" | relative_url }}) ya emite en el query executor propio de Room, y [DataStore]({{ "/es/glosario/datastore/" | relative_url }}) ya lee en IO — son [main-safe]({{ "/es/02-coroutines-flow/main-safety/" | relative_url }}) por contrato. Envolverlos agrega un salto por channel y, peor, le señala al próximo lector que la fuente era insegura, lo que lo manda a buscar un bug que no existe. En nuestro propio `TaskRepositoryImpl` el mapeo de entidad a modelo de dominio no tiene [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) a propósito: Room ya está fuera de Main y el mapeo es barato. Donde [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) *sí* corresponde es en un productor escrito por nosotros que bloquea — leer archivos, parsear JSON, un [SDK]({{ "/es/glosario/sdk/" | relative_url }}) síncrono — y ahí va inmediatamente después de ese productor, en la capa de datos, no en el ViewModel. También revisaría la posición: un [`.flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) al final de una cadena en un ViewModel mueve la cadena *entera* fuera de Main, incluido el mapeo que debía alimentar el estado de UI, y [`flowOn(Dispatchers.Main)`]({{ "/es/glosario/flow-on/" | relative_url }}) no hace lo que su nombre le sugiere a quien lee — fija el productor a Main, no al colector. Por último, inyectaría el dispatcher con un qualifier [`@IoDispatcher`]({{ "/es/glosario/io-dispatcher/" | relative_url }}) en vez de hardcodear [`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}), para que un test pueda pasar un [`TestDispatcher`]({{ "/es/glosario/test-dispatcher/" | relative_url }}) y afirmar el comportamiento de forma determinista.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
