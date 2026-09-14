# Notebook de estudio — Context & Dispatchers (Main, IO, Default)

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.
> Capítulo II — Coroutines & Flow · Artículo: https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/context-dispatchers/

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Qué es un `CoroutineContext` y qué elementos contiene? Si hacés `viewModelScope.launch(Dispatchers.IO) { }`, ¿qué pasa con el resto del contexto que tenía `viewModelScope`?
2. ¿Para qué sirve cada uno de `Dispatchers.Main`, `Dispatchers.Main.immediate`, `Dispatchers.IO` y `Dispatchers.Default`? ¿Cómo decidís cuál usar para un trabajo dado?
3. ¿Qué hace exactamente `withContext(Dispatchers.IO) { ... }`? ¿Crea una coroutine nueva? Cuando termina el bloque, ¿en qué dispatcher sigue corriendo el código que viene después?
4. Un repositorio `@Singleton` necesita colectar un `Flow` de billing durante toda la vida de la app. ¿Con qué scope lanzás esa coroutine, y por qué elegirías `SupervisorJob` en vez de un `Job` común?
5. ¿Qué problema aparece al testear una clase que tiene `Dispatchers.IO` hardcodeado adentro de un `withContext`, y cómo lo resolverías?

### Rúbrica

| # | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | Conjunto inmutable de elementos indexados por tipo: `Job`, dispatcher, `CoroutineExceptionHandler`, nombre. Se compone con `+`; se hereda del scope; lo pasado a `launch` reemplaza solo el elemento del mismo tipo. `launch(Dispatchers.IO)` conserva el `SupervisorJob` y la cancelación de `viewModelScope`. | Sabe que "el contexto define dónde corre" y que el hijo hereda, pero no enumera los elementos ni explica qué se conserva al pasar un dispatcher. | No conoce `CoroutineContext`, o cree que `launch(Dispatchers.IO)` desprende la coroutine del ViewModel. |
| 2 | Main = main thread / UI; `Main.immediate` = igual pero síncrono si ya está en Main (lo usan `viewModelScope` y `lifecycleScope`); IO = pool para llamadas bloqueantes (hasta 64 threads); Default = pool de tamaño = cores para CPU. Criterio: ¿bloquea un thread o quema CPU? IO y Default comparten pool. | Clasifica Main/IO/Default bien pero no conoce `Main.immediate` ni formula el criterio bloqueo-vs-cómputo. | Confunde IO con "cosas lentas" y Default con "lo que no es UI", o cree que IO crea threads a demanda sin límite. |
| 3 | Suspende la coroutine actual, agenda el bloque en el dispatcher destino, y al terminar reanuda al llamador en el dispatcher *original*. No crea coroutine ni thread; usa el pool. Devuelve el valor del bloque; la cancelación fluye a través. | Sabe que "corre el bloque en IO y después vuelve", pero cree que vuelve "a Main" (en vez de al dispatcher del llamador) o no sabe si crea una coroutine. | Cree que crea un thread nuevo o una coroutine nueva, o lo confunde con `launch`. |
| 4 | Scope propio `CoroutineScope(SupervisorJob() + Dispatchers.IO + CoroutineExceptionHandler)` porque el singleton sobrevive a toda pantalla. `SupervisorJob` para que el fallo de un collector no cancele a sus hermanos; con `Job` común un hijo que falla cancela al padre y a todos. Sin handler, la excepción crashea el proceso. | Elige un scope propio pero no justifica `SupervisorJob`, o lo justifica sin mencionar qué pasa con la excepción no capturada. | Propone `viewModelScope`, `GlobalScope` sin justificar, o no sabe. |
| 5 | El test no puede controlar el thread real de IO: races o sleeps. Fix: inyectar `CoroutineDispatcher` (qualifier `@IoDispatcher`) y pasar `StandardTestDispatcher(testScheduler)` bajo `runTest`. `Dispatchers.setMain` solo cubre Main. | Identifica el problema de timing pero propone esperar/dormir, o menciona `setMain` como solución completa. | No ve el problema, o propone `runBlocking`/`Thread.sleep`. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior → Senior; 3+ intermedias o mezcla → Intermedio; 3+ junior o "no sé" → Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-09-14

| # | Nivel | Observación |
|---|---|---|
| 1 | Junior | No conoce `CoroutineContext`. La intuición "adentro en IO, después vuelve" es correcta pero describe `withContext`, no lo que pasa con el contexto en `launch(Dispatchers.IO)` (se conserva el `SupervisorJob` y la cancelación; solo cambia el dispatcher). |
| 2 | Intermedia | Main, IO y Default bien caracterizados. Falta `Main.immediate` y el criterio explícito: bloquea un thread → IO; quema CPU → Default. |
| 3 | Junior | Malentendido: `withContext` no crea ni un thread ni una coroutine — reutiliza el pool y suspende la coroutine actual. "Después sigue en el principal" es correcto solo porque el llamador estaba en Main: vuelve al dispatcher original. |
| 4 | Junior | No sé. |
| 5 | Intermedia | Identifica bien el problema (el test no puede esperar/controlar un thread real). La solución no: no es "esperar con un return", es inyectar el dispatcher y sustituirlo por un `TestDispatcher` bajo `runTest`. |

**Nivel global: Junior con base intermedia** (2 intermedias, 3 junior).

Texto "Nivel actual" entregado a Gemini:

```text
Nivel global: Junior con base intermedia.

Ya domina: distingue correctamente Dispatchers.Main (UI), Dispatchers.IO (entrada/salida bloqueante) y Dispatchers.Default (cómputo intensivo); sabe que el código dentro de withContext(Dispatchers.IO) corre en IO y que después el flujo vuelve a Main; percibe que un Dispatchers.IO hardcodeado hace que un test no pueda controlar el timing. Tratar la clasificación de los tres dispatchers como repaso rápido.

Necesita explicación en profundidad: qué es un CoroutineContext y sus elementos (Job, dispatcher, CoroutineExceptionHandler), cómo se compone con + y cómo se hereda; qué conserva viewModelScope.launch(Dispatchers.IO) del contexto original; Dispatchers.Main.immediate y su garantía de orden; qué hace realmente withContext (suspende la coroutine actual, no crea thread ni coroutine, vuelve al dispatcher original); Job y SupervisorJob como árbol de cancelación y por qué un scope de un @Singleton se construye con SupervisorJob + Dispatchers.IO; CoroutineExceptionHandler; inyección de dispatchers y TestDispatcher / runTest para testear.

Malentendidos a corregir: cree que withContext(Dispatchers.IO) crea un hilo nuevo (usa un thread pool existente y no crea ninguna coroutine); cree que después de withContext se vuelve "al hilo principal" (se vuelve al dispatcher del llamador, que puede no ser Main); cree que el problema de testing se resuelve esperando el resultado (se resuelve inyectando el dispatcher).

Instrucción para el Audio Overview: explicá desde cero, con analogías, el CoroutineContext como conjunto de elementos heredado, el árbol de Jobs con y sin SupervisorJob, y qué hace withContext por dentro; tratá la clasificación Main/IO/Default como repaso de una frase y dedicá tiempo a Main.immediate y a la inyección de dispatchers para tests.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en NotebookLM para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Context & Dispatchers (Main, IO, Default)

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/context-dispatchers/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutines/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutine-context/
https://aghmnl.github.io/senior-forge-codex/es/glosario/job/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lifecycle/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatcher/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread-pool/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspension-point/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatchers-main/
https://aghmnl.github.io/senior-forge-codex/es/glosario/main-thread/
https://aghmnl.github.io/senior-forge-codex/es/glosario/looper/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatchers-main-immediate/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/launch/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatchers-io/
https://aghmnl.github.io/senior-forge-codex/es/glosario/blocking-call/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatchers-default/
https://aghmnl.github.io/senior-forge-codex/es/glosario/runtime/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatchers-unconfined/
https://aghmnl.github.io/senior-forge-codex/es/glosario/with-context/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspend-functions/
https://aghmnl.github.io/senior-forge-codex/es/glosario/supervisor-job/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutine-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/singleton-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/run-test/
https://aghmnl.github.io/senior-forge-codex/es/glosario/io-dispatcher/
https://aghmnl.github.io/senior-forge-codex/es/glosario/test-dispatcher/
https://aghmnl.github.io/senior-forge-codex/es/glosario/set-main/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutine-exception-handler/
https://aghmnl.github.io/senior-forge-codex/es/glosario/deferred/
https://aghmnl.github.io/senior-forge-codex/es/glosario/await/
https://aghmnl.github.io/senior-forge-codex/es/glosario/result/
https://aghmnl.github.io/senior-forge-codex/es/glosario/update/
https://aghmnl.github.io/senior-forge-codex/es/glosario/atomicity/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collect/
https://aghmnl.github.io/senior-forge-codex/es/glosario/continuation/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cooperative-cancellation/
https://aghmnl.github.io/senior-forge-codex/es/glosario/flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/try-catch/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/coroutine-context-and-dispatchers.html
https://kotlinlang.org/docs/coroutines-basics.html
https://kotlinlang.org/docs/composing-suspending-functions.html
https://kotlinlang.org/docs/cancellation-and-timeouts.html
https://kotlinlang.org/docs/exception-handling.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/with-context.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-supervisor-job.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-exception-handler/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-test/
https://developer.android.com/kotlin/coroutines
https://developer.android.com/kotlin/coroutines/coroutines-adv
https://developer.android.com/kotlin/coroutines/coroutines-best-practices
https://developer.android.com/kotlin/coroutines/test
https://developer.android.com/topic/libraries/architecture/coroutines
https://developer.android.com/training/dependency-injection/hilt-android
https://developer.android.com/reference/android/os/Looper

**Pasos de ejecución**
1. Creá un notebook nuevo en NotebookLM llamado exactamente: Context & Dispatchers (Main, IO, Default)
2. Agregá el artículo principal como fuente web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior con base intermedia.

Ya domina: distingue correctamente Dispatchers.Main (UI), Dispatchers.IO (entrada/salida bloqueante) y Dispatchers.Default (cómputo intensivo); sabe que el código dentro de withContext(Dispatchers.IO) corre en IO y que después el flujo vuelve a Main; percibe que un Dispatchers.IO hardcodeado hace que un test no pueda controlar el timing. Tratar la clasificación de los tres dispatchers como repaso rápido.

Necesita explicación en profundidad: qué es un CoroutineContext y sus elementos (Job, dispatcher, CoroutineExceptionHandler), cómo se compone con + y cómo se hereda; qué conserva viewModelScope.launch(Dispatchers.IO) del contexto original; Dispatchers.Main.immediate y su garantía de orden; qué hace realmente withContext (suspende la coroutine actual, no crea thread ni coroutine, vuelve al dispatcher original); Job y SupervisorJob como árbol de cancelación y por qué un scope de un @Singleton se construye con SupervisorJob + Dispatchers.IO; CoroutineExceptionHandler; inyección de dispatchers y TestDispatcher / runTest para testear.

Malentendidos a corregir: cree que withContext(Dispatchers.IO) crea un hilo nuevo (usa un thread pool existente y no crea ninguna coroutine); cree que después de withContext se vuelve "al hilo principal" (se vuelve al dispatcher del llamador, que puede no ser Main); cree que el problema de testing se resuelve esperando el resultado (se resuelve inyectando el dispatcher).

Instrucción para el Audio Overview: explicá desde cero, con analogías, el CoroutineContext como conjunto de elementos heredado, el árbol de Jobs con y sin SupervisorJob, y qué hace withContext por dentro; tratá la clasificación Main/IO/Default como repaso de una frase y dedicá tiempo a Main.immediate y a la inyección de dispatchers para tests.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Coroutine context and dispatchers | La guía central: elementos del contexto, `Dispatchers.*`, `withContext`, herencia, `Job` padre/hijo, `CoroutineName`. |
| Coroutines basics | Scope, `launch`, structured concurrency como base. |
| Composing suspending functions | `async`/`await`, `Deferred`, descomposición paralela. |
| Cancellation and timeouts | Árbol de cancelación, `isActive`, `finally`, `NonCancellable`. |
| Exception handling | `CoroutineExceptionHandler`, `SupervisorJob` vs `Job`, por qué `async` no usa el handler. |
| `Dispatchers` (API) | Contrato exacto de `Main`, `Main.immediate`, `IO`, `Default`, `Unconfined` y `limitedParallelism`. |
| `withContext` (API) | Semántica precisa: mismo Job, vuelve al contexto original, elide el dispatch si no cambia. |
| `SupervisorJob` (API) | Semántica de fallo independiente de los hijos. |
| `CoroutineExceptionHandler` (API) | Cuándo se invoca y cuándo no. |
| `kotlinx-coroutines-test` (API) | `runTest`, `TestDispatcher`, `setMain`. |
| Kotlin coroutines on Android | Main-safety, `viewModelScope`, dispatchers en Android. |
| Improve app performance with coroutines | El ejemplo canónico de `withContext(Dispatchers.IO)` adentro de la suspend fun. |
| Best practices for coroutines | Inyectar dispatchers, no exponer scopes, `@Singleton` con scope propio. |
| Testing Kotlin coroutines on Android | `setMain`, `StandardTestDispatcher` vs `Unconfined`, inyección para tests. |
| Coroutines with lifecycle-aware components | `viewModelScope`, `lifecycleScope`, `repeatOnLifecycle`. |
| Dependency injection with Hilt | `@Singleton`, componentes y qualifiers (`@IoDispatcher`). |
| `Looper` (referencia) | Qué hay debajo de `Dispatchers.Main`. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Context & Dispatchers (Main, IO, Default)", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Qué es un `CoroutineContext` y qué elementos contiene? Si hacés `viewModelScope.launch(Dispatchers.IO) { }`, ¿qué pasa con el resto del contexto que tenía `viewModelScope`?
2. ¿Para qué sirve cada uno de `Dispatchers.Main`, `Dispatchers.Main.immediate`, `Dispatchers.IO` y `Dispatchers.Default`? ¿Cómo decidís cuál usar para un trabajo dado?
3. ¿Qué hace exactamente `withContext(Dispatchers.IO) { ... }`? ¿Crea una coroutine nueva? Cuando termina el bloque, ¿en qué dispatcher sigue corriendo el código que viene después?
4. Un repositorio `@Singleton` necesita colectar un `Flow` de billing durante toda la vida de la app. ¿Con qué scope lanzás esa coroutine, y por qué elegirías `SupervisorJob` en vez de un `Job` común?
5. ¿Qué problema aparece al testear una clase que tiene `Dispatchers.IO` hardcodeado adentro de un `withContext`, y cómo lo resolverías?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: conjunto de elementos (Job, dispatcher, handler) compuesto con +, heredado; launch(IO) conserva SupervisorJob y cancelación. Junior: no conoce CoroutineContext.
- P2 Senior: Main/Main.immediate/IO/Default con el criterio bloqueo-vs-CPU; IO y Default comparten pool. Intermedio: no conoce Main.immediate.
- P3 Senior: suspende, corre el bloque en el dispatcher destino, vuelve al dispatcher original; sin coroutine ni thread nuevos. Junior: cree que crea un thread.
- P4 Senior: scope propio con SupervisorJob + IO + CoroutineExceptionHandler; sin supervisor un hijo cancela a todos; sin handler crashea. Junior: viewModelScope/GlobalScope o no sabe.
- P5 Senior: inyectar CoroutineDispatcher (@IoDispatcher) y usar StandardTestDispatcher bajo runTest; setMain solo cubre Main. Intermedio: propone esperar o dormir.
```
