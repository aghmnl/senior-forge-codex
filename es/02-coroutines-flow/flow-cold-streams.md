---
layout: page
title: "Flow (Cold Streams)"
lang: es
permalink: /es/02-coroutines-flow/flow-cold-streams/
order: 7
---

## The Theory (El Qué)

Un [`Flow<T>`]({{ "/es/glosario/flow/" | relative_url }}) es un stream asincrónico de valores que es **cold** (frío): declararlo no ejecuta nada. Un flow es una *receta* — la descripción de cómo se van a producir los valores — y la receta se ejecuta recién cuando alguien aplica un **operador terminal**. Hasta entonces no corre ninguna query, no se lee ningún archivo, no ocurre ningún [`emit`]({{ "/es/glosario/emit/" | relative_url }}).

El modelo tiene tres piezas:

- **Los builders** producen el flow: `flow { emit(x) }` para trabajo suspendible arbitrario, `flowOf(a, b)` para valores fijos, `asFlow()` sobre una colección, y `callbackFlow`/`channelFlow` para tender un puente hacia una API basada en [callbacks]({{ "/es/glosario/callbacks/" | relative_url }}).
- **Los operadores intermedios** — `map`, `filter`, `onEach`, [`combine`]({{ "/es/glosario/combine/" | relative_url }}), [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}) — son *declarativos*. Cada uno devuelve un `Flow` nuevo que envuelve al anterior; ninguno ejecuta nada. Son tan lazy como los operadores de [`Sequence`]({{ "/es/glosario/sequences/" | relative_url }}), y por la misma razón.
- **Los [operadores terminales]({{ "/es/glosario/terminal-operations/" | relative_url }})** — [`collect`]({{ "/es/glosario/collect/" | relative_url }}), [`first`]({{ "/es/glosario/first/" | relative_url }}), `toList`, `single`, `fold` — son [suspend functions]({{ "/es/glosario/suspend-functions/" | relative_url }}). Arrancan el productor, y necesitan un [coroutine scope]({{ "/es/glosario/coroutine-scope/" | relative_url }}) donde correr.

Como la receta se reinicia en cada colección, **cada colector obtiene su propia ejecución independiente**: colectá el mismo `Flow` dos veces y el productor corre dos veces. Eso es exactamente lo que significa "cold", y es lo opuesto a un stream caliente como [`StateFlow`]({{ "/es/glosario/stateflow/" | relative_url }}), que existe y mantiene un valor haya o no alguien escuchando.

La emisión es secuencial y aplica [backpressure]({{ "/es/glosario/backpressure/" | relative_url }}) por defecto: `emit` suspende hasta que el colector terminó de procesar ese valor, así que un consumidor lento frena al productor en vez de llenar una cola.

## The Senior Perspective (El Porqué)

- **"Cold" es un modelo de costos, no un dato de trivia.** Dos colectores sobre un flow respaldado por [Room]({{ "/es/glosario/room/" | relative_url }}) significan dos queries vivas y dos observadores de base de datos, cada uno re-ejecutándose ante cada cambio de tabla. Un `Flow` que expone un repositorio y colectan tres pantallas es tres veces el trabajo. La solución no es colectar menos, sino compartir una sola ejecución — que es para lo que existen `stateIn`/`shareIn`, tema de más adelante.
- **No pasa nada hasta que se colecta, y eso es una feature.** Llamar a `repository.getActiveTasks()` no tiene efectos secundarios: aloca una descripción. Por eso un repositorio puede devolver un `Flow` sin scope, sin decisiones de threading y sin ciclo de vida, y por eso los flows son tan testeables. El bug correspondiente es la imagen espejo: un flow que nadie colecta *no hace nada*, en silencio — sin error, sin log, sin warning. Un `flow { }` cuyo logging nunca aparece es, casi siempre, un flow sin colectar.
- **Elegir el operador terminal es una decisión de diseño.** [`first()`]({{ "/es/glosario/first/" | relative_url }}) toma un valor y **cancela el productor** — una lectura puntual de una fuente viva. `collect` observa para siempre y la coroutine nunca completa. Usar `first()` sobre un flow que querías observar te da datos que quedan obsoletos en silencio; usar `collect` donde querías una foto te da una coroutine que nunca retorna y un llamador colgado.
- **La vida de un flow cold es la vida de la coroutine que lo colecta.** No tiene ciclo de vida propio: cancelás el [scope]({{ "/es/glosario/coroutine-scope/" | relative_url }}) y el productor se cancela en su próximo [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}). Colectar en [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) ata el stream al ViewModel, que normalmente es lo correcto; colectar en una `Activity` sin `repeatOnLifecycle` mantiene vivo al colector mientras la pantalla está en background, que normalmente es un bug.
- **Secuencial por defecto; la concurrencia se pide.** Los valores llegan en orden y de a uno. Si el productor tiene que adelantarse al consumidor, lo pedís con [`buffer`]({{ "/es/glosario/buffer/" | relative_url }}); si tiene que correr en otro [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}), lo pedís con [`flowOn`]({{ "/es/glosario/flow-on/" | relative_url }}). Nada se vuelve concurrente a tus espaldas, y eso hace a los flows mucho más fáciles de razonar que un pipeline de callbacks.
- **El productor tiene que mantenerse transparente a las excepciones.** Un builder `flow { }` no debería envolver sus propias emisiones en `try/catch`; las fallas viajan [downstream]({{ "/es/glosario/downstream/" | relative_url }}) hasta el colector, y [`catch`]({{ "/es/glosario/catch/" | relative_url }}) las maneja ahí — solo las de su [upstream]({{ "/es/glosario/upstream/" | relative_url }}). Ese es un tema aparte.

## Code in Action

```kotlin
// De FollowApp Suite — LabelOptionDao.kt
// Room devuelve un Flow cold: la query corre por colector, y vuelve a correr
// cada vez que cambia la tabla
@Query("SELECT * FROM label_options ORDER BY sort_order ASC, label ASC")
fun getAllOptionsStream(): Flow<List<LabelOptionEntity>>

// De FollowApp Suite — TaskRepositoryImpl.kt
// map() es un operador intermedio: esta línea no corre ninguna query ni toca
// la base de datos. Solo describe el mapeo que va a ocurrir en la colección.
override fun getActiveTasks(sort: ListSort): Flow<List<Task>> {
    return taskDao.getActiveTasksStream(sort.name).map { entities ->
        entities.map { it.toDomain() }
    }
}

// De FollowApp Suite — CleanUpPresetsUseCase.kt
// first() es terminal: toma UNA emisión y cancela el productor.
// Una lectura puntual de una fuente viva, que es justo lo que un cleanup necesita.
suspend fun onLabelDeleted(labelName: String) {
    val presets = presetRepository.getAll().first()
    presets.forEach { preset ->
        if (preset.groupBy == labelName) {
            presetRepository.save(preset.copy(groupBy = null))
        }
    }
}

// De FollowApp Suite — PremiumUseCases.kt
// combine() es intermedio: arma un Flow cold a partir de dos Flows cold.
// Nada corre hasta que alguien colecta el resultado.
operator fun invoke(): Flow<Boolean> = combine(
    premiumLedgerRepository.getLedger(),
    authRepository.getSession()
) { ledger, session ->
    PremiumLifecycle.isPremium(
        now = System.currentTimeMillis(),
        premiumUntil = ledger.premiumUntil,
        isSignedIn = session != null
    )
}

// De FollowApp Suite — LabelsListViewModel.kt
// El operador terminal vive en el ViewModel, adentro de viewModelScope:
// ese scope es la vida del stream.
private fun observeCatalog() {
    viewModelScope.launch {
        combine(
            getLabelsCatalogUseCase(),
            getActiveTasksUseCase(),
            _resyncTrigger
        ) { catalog, tasks, _ ->
            buildCatalogState(catalog, tasks)
        }
            .catch { e -> /* manejado downstream, ver Error Handling */ }
            .collect { (sortedLabels, scales) ->
                _uiState.update { /* ... */ }
            }
    }
}

// De FollowApp Suite — FakePresetRepository.kt (test fixtures)
// El builder flow: un fake que cumple el mismo contrato cold que Room
override fun getAll(): Flow<List<Preset>> = flow { emit(presets.toList()) }
```

## The Interview (En el banquillo)

**Pregunta**: ¿Qué significa que un `Flow` sea "cold", y qué pasa si dos pantallas distintas colectan el mismo flow de un repositorio?

**Respuesta Senior**: Cold significa que el flow es una descripción, no un pipeline corriendo: construirlo y encadenarle operadores intermedios no ejecuta nada, y el productor arranca recién cuando se aplica un [operador terminal]({{ "/es/glosario/terminal-operations/" | relative_url }}) como [`collect`]({{ "/es/glosario/collect/" | relative_url }}) o [`first`]({{ "/es/glosario/first/" | relative_url }}). La consecuencia es que **cada colector obtiene su propia ejecución desde cero**. Si dos pantallas colectan el mismo flow de repositorio respaldado por [Room]({{ "/es/glosario/room/" | relative_url }}), tenés dos queries independientes y dos observadores de base de datos, y cada cambio de tabla vuelve a correr los dos — el trabajo se duplica, no se comparte. Eso normalmente es invisible en desarrollo y aparece como batería y CPU en producción. El arreglo correcto no es colectar menos sino compartir una sola ejecución upstream, que es para lo que están `shareIn` y `stateIn`, convirtiendo el flow cold en uno hot con un productor único y varios suscriptores. Lo otro que agregaría es que ser cold es también lo que hace seguro pasarlos de mano en mano: llamar a `repository.getActiveTasks()` no tiene efectos secundarios y no necesita [scope]({{ "/es/glosario/coroutine-scope/" | relative_url }}), así que la capa de datos puede exponer streams sin ser dueña de un ciclo de vida — y es también el bug espejo, porque un flow que nadie colecta no hace absolutamente nada y nunca te avisa.

**Pregunta**: Un repositorio expone `getAll(): Flow<List<Preset>>`. ¿Cuándo usás `first()` y cuándo `collect()`, y qué se rompe si elegís mal?

**Respuesta Senior**: [`first()`]({{ "/es/glosario/first/" | relative_url }}) es para una foto: suspende hasta la primera emisión, devuelve ese valor y **cancela el productor**, así que la suspend function llamadora completa. Eso es lo que necesita un use case de limpieza — leer los presets actuales, actuar sobre ellos, terminar. [`collect`]({{ "/es/glosario/collect/" | relative_url }}) es para observar: nunca completa por sí solo, sigue recibiendo cada re-emisión mientras viva el [scope]({{ "/es/glosario/coroutine-scope/" | relative_url }}), y va en un ViewModel adentro de [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}). Elegir mal falla de dos formas distintas. Usar `first()` donde querías observar compila, corre, muestra los datos correctos una vez, y después queda obsoleto en silencio — la pantalla nunca refleja un cambio posterior, y nada lanza error, lo que lo vuelve un bug genuinamente difícil de detectar. Usar `collect` donde querías una foto suspende para siempre: la suspend function que lo contiene nunca retorna, así que lo que la esperaba queda colgado, y si eso está adentro de un `withContext` o de un use case llamado desde un click handler, la operación simplemente nunca termina. Mi regla es que el operador terminal tiene que coincidir con la intención — un valor y listo, o una suscripción viva atada a un ciclo de vida — y si una función necesita una foto de algo que genuinamente es un stream, lo hago explícito en el nombre en vez de dejar un `first()` enterrado en el cuerpo.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
