---
layout: page
title: "Error Handling: try-catch & .catch"
lang: es
permalink: /es/02-coroutines-flow/error-handling/
order: 8
---

## The Theory (El Qué)

Las [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) no inventan un mecanismo de errores nuevo: una excepción lanzada dentro de una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) se propaga por el [call stack]({{ "/es/glosario/call-stack/" | relative_url }}) como cualquier otra, y un [`try/catch`]({{ "/es/glosario/try-catch/" | relative_url }}) común alrededor de una llamada suspendible funciona exactamente como esperarías. Lo que cambia es la forma del código que estás protegiendo.

Para **código suspendible imperativo** — una llamada, un resultado — la herramienta es `try/catch`, y [`runCatching`]({{ "/es/glosario/run-catching/" | relative_url }}) es la versión funcional que empaqueta el éxito o la falla en un [`Result`]({{ "/es/glosario/result/" | relative_url }}).

Para un **[`Flow`]({{ "/es/glosario/flow/" | relative_url }})** la herramienta es el operador [`catch`]({{ "/es/glosario/catch/" | relative_url }}), y obedece una regla: **solo ve las excepciones de su [upstream]({{ "/es/glosario/upstream/" | relative_url }})**. Una excepción lanzada en el bloque [`collect`]({{ "/es/glosario/collect/" | relative_url }}), que está [downstream]({{ "/es/glosario/downstream/" | relative_url }}), no la atrapa un `catch` escrito más arriba. Adentro del operador podés loguear, actualizar estado, o [`emitir`]({{ "/es/glosario/emit/" | relative_url }}) un valor de respaldo, convirtiendo una falla en una emisión normal.

Esa regla es consecuencia de la **[transparencia a las excepciones]({{ "/es/glosario/exception-transparency/" | relative_url }})**: el productor de un flow tiene que dejar que las excepciones viajen hasta el colector en vez de tragárselas. Envolver tu propio [`emit`]({{ "/es/glosario/emit/" | relative_url }}) en un `try/catch` adentro de un builder `flow { }` la viola, y el [runtime]({{ "/es/glosario/runtime/" | relative_url }}) te lo va a decir.

La cancelación es la excepción a todo esto. [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}) no es un error: es la señal de que el [job]({{ "/es/glosario/job/" | relative_url }}) de una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) fue cancelado. Tragársela rompe la [cancelación cooperativa]({{ "/es/glosario/cooperative-cancellation/" | relative_url }}) — la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) sigue corriendo después de que su scope ya no existe. Siempre hay que relanzarla.

## The Senior Perspective (El Porqué)

- **`catch { }` para el upstream, `try { }` para el downstream — y la diferencia muerde.** Un `.catch` arriba del `.collect` protege al productor y a cada operador intermedio; **no** protege el cuerpo del propio colector. Si el código que escribe el estado de UI puede lanzar, eso necesita su propio `try/catch` adentro del bloque `collect`, o el trabajo se sube a un [`onEach`]({{ "/es/glosario/on-each/" | relative_url }}) por encima del `catch`. Los equipos descubren esto por las malas cuando un crash en una función de mapeo adentro del `collect` voltea la app a pesar de tener un `.catch` justo arriba.
- **`catch (e: Exception)` se traga la cancelación.** En la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}) es una [`RuntimeException`]({{ "/es/glosario/runtime-exception/" | relative_url }}), así que un `catch (e: Exception)` amplio alrededor de código suspendible atrapa la señal de cancelación y sigue como si nada. La [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) sobrevive a su propia cancelación, el [scope]({{ "/es/glosario/coroutine-scope/" | relative_url }}) nunca termina, y una pantalla que se cerró sigue trabajando. Atrapá tipos estrechos, o atrapá amplio y relanzá la cancelación explícitamente.
- **[`runCatching`]({{ "/es/glosario/run-catching/" | relative_url }}) tiene la misma trampa, y es peor porque parece segura.** Atrapa [`Throwable`]({{ "/es/glosario/throwable/" | relative_url }}), que incluye a [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}). En código de [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) habría que evitarlo o seguirlo inmediatamente de un relanzamiento de la cancelación. Su lugar legítimo es un borde genuinamente puntual que nunca se cancela a mitad de camino — una exportación, un parseo, un puente hacia una API de callbacks — donde devolverle un `Result` al llamador es más lindo que lanzar.
- **Atrapá la cancelación solo para limpiar, y después relanzá.** Hay una razón válida para atrapar una [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}): liberar algo que la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) posee — terminar un drag, cerrar un stream, restaurar un estado visual. El patrón es siempre el mismo: hacés la limpieza y después `throw e`. [`finally`]({{ "/es/glosario/finally/" | relative_url }}) cubre la mayoría de los casos; el catch explícito es para cuando la limpieza depende de *por qué* terminó la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}).
- **Traducí las excepciones a mensajes de usuario en el borde de la UI, no en la capa de datos.** Un repositorio que convierte una [`SQLiteConstraintException`]({{ "/es/glosario/sqlite-constraint-exception/" | relative_url }}) en "Algo salió mal" destruyó la única información sobre la que alguien podía actuar. Dejá viajar las excepciones técnicas; traducilas una vez, en la capa de UI, donde conocés la pantalla, el texto y el idioma.
- **Un error es un estado, no solo una línea de log.** Un `.catch { }` que solo llama a `Log.e` deja la UI trabada en un spinner para siempre. Si una falla significa que la pantalla no puede mostrar datos, el bloque catch tiene que mover el [state holder]({{ "/es/glosario/state-holder/" | relative_url }}) a un estado de error — que es también por qué un estado de UI sellado con un miembro [`Error`]({{ "/es/glosario/error-state/" | relative_url }}) rinde acá.

## Code in Action

```kotlin
// De FollowApp Suite — TasksViewModel.kt
// .catch protege al flow upstream: si el use case del catálogo falla,
// el colector nunca corre y la app no crashea
private fun observeLabels() {
    viewModelScope.launch {
        getLabelsCatalogUseCase()
            .catch { error ->
                Log.e(TAG, "Error loading labels", error)
            }
            .collect { allLabels ->
                _labelsWithOptions.value = allLabels
            }
    }
}

// De FollowApp Suite — LabelsListViewModel.kt
// La versión madura: la falla se convierte en estado de UI, no solo en un log
combine(getLabelsCatalogUseCase(), getActiveTasksUseCase(), _resyncTrigger) { catalog, tasks, _ ->
    buildCatalogState(catalog, tasks)
}
    .catch { e ->
        Log.e(TAG, "Error loading labels", e)
        _uiState.update {
            it.copy(isLoading = false, errorMessageRes = e.toUserMessage())
        }
    }
    .collect { (sortedLabels, scales) -> /* ... */ }

// De FollowApp Suite — ErrorMapping.kt
// La traducción ocurre una sola vez, en el borde de la UI — la capa de datos
// sigue lanzando excepciones técnicas que llevan información real
fun Throwable.toUserMessage(): Int = when {
    this is SQLiteConstraintException && message.orEmpty().contains("UNIQUE") ->
        R.string.error_duplicate_tag
    else -> R.string.error_generic
}

// De FollowApp Suite — DragToReorder.kt
// La única forma correcta de atrapar la cancelación: limpiar y después RELANZAR.
// Sin el throw, la coroutine del gesto sobreviviría a su propia cancelación.
try {
    // ... loop del gesto de drag
} catch (e: CancellationException) {
    // Gesture coroutine disposed mid-drag (e.g. composition change)
    state.endDrag(cancelled = true)
    throw e
}

// De FollowApp Suite — SettingsViewModel.kt
// Catches estrechos, y un login cancelado no es un error que valga mostrar
viewModelScope.launch {
    try {
        val session = googleAuthClient.signIn(activityContext)
        saveUserSessionUseCase(session)
    } catch (e: GetCredentialCancellationException) {
        Log.d(TAG, "Google sign-in cancelled by user")
    } catch (e: GetCredentialException) {
        Log.e(TAG, "Google sign-in failed", e)
        _uiState.update { it.copy(messageRes = R.string.error_sign_in) }
    }
}

// De FollowApp Suite — BackupManager.kt
// runCatching en un borde genuinamente puntual, devolviéndole Result al llamador
suspend fun exportTo(uri: Uri): Result<Unit> = withContext(Dispatchers.IO) {
    runCatching {
        val json = jsonOf(content)
        context.contentResolver.openOutputStream(uri, "wt").use { stream ->
            requireNotNull(stream) { "Cannot open destination" }
            stream.write(json.toByteArray(Charsets.UTF_8))
        }
    }.onFailure { Log.e(TAG, "Backup export failed", it) }
}
```

## The Interview (En el banquillo)

**Pregunta**: Tenés `flow.catch { }.collect { }` y la app igual crashea. El stack trace apunta adentro del bloque `collect`. ¿Por qué no ayudó el `.catch`, y cómo lo arreglás?

**Respuesta Senior**: Porque [`catch`]({{ "/es/glosario/catch/" | relative_url }}) solo maneja las excepciones que vienen de su [upstream]({{ "/es/glosario/upstream/" | relative_url }}) — el builder y cada operador declarado **arriba** de él. El bloque [`collect`]({{ "/es/glosario/collect/" | relative_url }}) está [downstream]({{ "/es/glosario/downstream/" | relative_url }}), así que una excepción lanzada mientras se procesa un valor queda fuera del alcance del operador y se propaga a la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) que lo contiene. Esa asimetría no es un accidente: es la [transparencia a las excepciones]({{ "/es/glosario/exception-transparency/" | relative_url }}), la misma regla que le prohíbe a un builder `flow { }` envolver su propio [`emit`]({{ "/es/glosario/emit/" | relative_url }}) en un `try/catch`. Hay dos arreglos según la intención. Si el trabajo que falla es realmente parte del pipeline — un mapeo, una conversión — lo muevo a un [`onEach`]({{ "/es/glosario/on-each/" | relative_url }}) o un `map` ubicado *arriba* del `catch`, y ahí sí queda cubierto. Si es genuinamente trabajo del consumidor, como escribir un [state holder]({{ "/es/glosario/state-holder/" | relative_url }}), lleva su propio [`try/catch`]({{ "/es/glosario/try-catch/" | relative_url }}) adentro del bloque `collect`. Lo que no haría es envolver toda la llamada a `collect` en un `try/catch` y darlo por resuelto: eso atrapa también la cancelación, y esconde cuál de las dos mitades del pipeline falló realmente.

**Pregunta**: Un compañero envuelve el cuerpo de cada [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) en `try { ... } catch (e: Exception) { log(e) }` para que "nada pueda crashear". ¿Qué le decís?

**Respuesta Senior**: Que eso no hace la app más segura, hace que la cancelación quede rota. En la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}) es una [`RuntimeException`]({{ "/es/glosario/runtime-exception/" | relative_url }}), así que `catch (e: Exception)` atrapa la señal de cancelación junto con las fallas reales. La [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) entonces se traga su propia cancelación y sigue corriendo: el [scope]({{ "/es/glosario/coroutine-scope/" | relative_url }}) nunca completa, una pantalla cerrada sigue haciendo queries, y la concurrencia estructurada deja de significar algo — el padre espera a un hijo que se niega a morir. Lo mismo aplica a [`runCatching`]({{ "/es/glosario/run-catching/" | relative_url }}), que atrapa [`Throwable`]({{ "/es/glosario/throwable/" | relative_url }}) y es más peligroso justamente porque se lee como la opción segura e idiomática. Lo que pido en cambio son catches estrechos de las excepciones que esa llamada realmente puede producir — que es lo que hacemos en el login con Google, donde una credencial cancelada por el usuario se loguea en debug y una falla real se convierte en mensaje de error — y, cuando un catch amplio hace falta de verdad, un `if (e is [CancellationException]({{ "/es/glosario/cancellation-exception/" | relative_url }})) throw e` explícito al principio. La única razón legítima para atrapar la cancelación es limpiar, y entonces el bloque tiene que terminar en `throw e`; es exactamente lo que hace nuestro gesto de drag cuando la composición lo descarta a mitad del arrastre. Por último, señalaría que "loguear y seguir" normalmente no es manejar el error: si la falla significa que la pantalla no tiene datos, el usuario necesita un estado de error, no una línea en Logcat.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
