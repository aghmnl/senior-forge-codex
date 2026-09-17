# Notebook de estudio — Main-Safety

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.
> Capítulo II — Coroutines & Flow · Artículo: https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/main-safety/

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Qué significa que una suspend function sea "main-safe"? ¿De quién es la responsabilidad de garantizarlo: del que la llama o del que la escribe? ¿Por qué?
2. `suspend fun load(): String = File(path).readText()` — ¿es main-safe? ¿Qué pasa si la llamás desde `viewModelScope`? ¿Qué cambiarías?
3. ¿Hace falta envolver `dao.insert(x)` (método `suspend` de Room) o una llamada `suspend` de Retrofit en `withContext(Dispatchers.IO)`? ¿Por qué sí o por qué no?
4. Una función hace aritmética de fechas pesada (sin I/O) y otra lee un archivo. ¿A qué dispatcher mandás cada una y por qué? ¿"Main-safe" significa "rápido"?
5. Heredás un repositorio que bloquea Main. ¿Cómo lo arreglás y cómo lo probás en un test de forma determinista (qué inyectás, qué afirmás y en qué momento)?

### Rúbrica

| # | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | Se puede llamar desde el main thread sin bloquearlo: solo suspende, el trabajo bloqueante corre en otro dispatcher. Responsabilidad del *llamado*: el dispatcher se hereda, así que el `withContext` va adentro de la función que bloquea, una vez, y ningún llamador tiene que acordarse. Convención: toda suspend function es main-safe. | Sabe que "no debe bloquear el main thread" pero cree que el que llama tiene que poner `withContext(IO)`. | No conoce el término, o cree que `suspend` ya garantiza no bloquear. |
| 2 | No: `readText()` bloquea y no hay ningún suspension point. Desde `viewModelScope` (Main.immediate) bloquea Main durante la lectura → jank/ANR. Fix: `withContext(Dispatchers.IO) { File(path).readText() }` adentro de la función; idealmente con dispatcher inyectado. | Detecta que bloquea pero no explica por qué `suspend` no ayuda (sin suspension point), o propone el `withContext` en el llamador. | Cree que es main-safe porque es `suspend`. |
| 3 | No. Room ejecuta los métodos `suspend` del DAO en su propio executor y Retrofit en el pool de OkHttp; DataStore lee en IO. Envolverlos es un dispatch redundante y le dice al lector que no son main-safe. Solo se envuelve I/O crudo, CPU pesada o SDKs síncronos. | Sabe que Room "ya lo hace" pero no articula el costo de envolver dos veces, o duda con Retrofit/DataStore. | Cree que hay que envolver todo acceso a datos en `withContext(IO)`. |
| 4 | Fechas → `Dispatchers.Default` (CPU; pool = cores); archivo → `Dispatchers.IO` (bloquea un thread; pool grande). I/O en Default secuestra un core; CPU en IO desperdicia. Main-safe ≠ rápido: no congela la UI pero puede tardar igual; sigue haciendo falta progreso/caché. | Manda todo a IO, o distingue IO/Default pero no explica la consecuencia de equivocarse. Confunde main-safe con rápido. | Cree que basta con "sacarlo de Main" a cualquier dispatcher, o no distingue IO de Default. |
| 5 | Profiling para encontrar qué bloquea (SDKs síncronos escondidos tras callbacks). Envolver solo la parte bloqueante con el dispatcher correcto; no envolver Room/Retrofit/DataStore. Inyectar `@IoDispatcher`. Test: `runTest`, `StandardTestDispatcher(testScheduler)` inyectado, `launch { fn() }`, afirmar *antes* de avanzar que el job sigue activo (suspendió, no bloqueó), `advanceUntilIdle()`, afirmar resultado. | Envuelve en `withContext(IO)` hardcodeado y testea solo el resultado final, sin poder probar que suspendió. | No sabe cómo testearlo, o propone `Thread.sleep` / `runBlocking`. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior → Senior; 3+ intermedias o mezcla → Intermedio; 3+ junior o "no sé" → Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-09-17

| # | Nivel | Observación |
|---|---|---|
| 1 | Intermedia | Idea correcta ("no detiene el hilo principal"), pero imprecisa: lo que no se detiene es el main thread, no "todo el proceso". No sabe de quién es la responsabilidad (es del llamado, porque el dispatcher se hereda). |
| 2 | Intermedia | Detecta bien que no es main-safe y que `viewModelScope` corre en Main. La razón no es "no libera recursos": es que no hay ningún suspension point, así que `suspend` no ayuda. No propuso el fix (`withContext(Dispatchers.IO)` adentro de la función). |
| 3 | Senior | Correcto: Room y Retrofit ya manejan sus threads; no hace falta envolver. |
| 4 | Senior | Correcto: Default para CPU, IO para archivo; main-safe ≠ rápido. |
| 5 | Junior | No sé. |

**Nivel global: Intermedio** (2 Senior, 2 intermedias, 1 junior).

Texto "Nivel actual" entregado a Gemini:

```text
Nivel global: Intermedio.

Ya domina: sabe que Room y Retrofit ya ejecutan sus llamadas suspend fuera del main thread y que envolverlas en withContext(Dispatchers.IO) no es necesario; asigna correctamente Dispatchers.Default a la aritmética pesada y Dispatchers.IO a la lectura de archivos; tiene claro que main-safe no significa rápido sino no bloquear el main thread; sabe que viewModelScope corre en el main thread. Tratar la elección IO vs Default y la regla "no envolver Room/Retrofit" como repaso rápido.

Necesita explicación en profundidad: la definición precisa de main-safe (se puede llamar desde el main thread y solo suspende, el trabajo bloqueante corre en otro dispatcher); por qué la responsabilidad es del llamado — el dispatcher se hereda, así que el withContext va adentro de la función que bloquea, una sola vez; por qué suspend no garantiza nada: File(path).readText() no tiene ningún suspension point, así que bloquea aunque la función sea suspend; la forma canónica withContext(Dispatchers.IO) como cuerpo de la función; inyección del dispatcher con @IoDispatcher y cómo un test con runTest + StandardTestDispatcher puede afirmar que la función suspendió (job activo antes de advanceUntilIdle) en vez de bloquear.

Malentendidos a corregir: explica que readText() no es main-safe porque "no libera recursos hasta que termina" — la razón real es que no hay ningún suspension point: la coroutine nunca suspende, así que el main thread queda ocupado ejecutando la lectura. Y describió main-safe como "no detener todo el proceso": lo que se detiene es el main thread (frames e input), no el proceso; la consecuencia es jank y, a los 5 segundos, ANR.

Instrucción para el Audio Overview: explicá desde cero, con analogías, por qué el dispatcher se hereda y eso hace que la main-safety sea responsabilidad de la función que bloquea, por qué la palabra suspend no mueve nada a ningún lado, y cómo se prueba en un test que una función suspende en vez de bloquear; tratá IO vs Default y "Room ya es main-safe" como repaso de una frase.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Main-Safety

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/main-safety/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspend-functions/
https://aghmnl.github.io/senior-forge-codex/es/glosario/main-thread/
https://aghmnl.github.io/senior-forge-codex/es/glosario/blocking-call/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sdk/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatchers-main/
https://aghmnl.github.io/senior-forge-codex/es/glosario/with-context/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutines/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspension-point/
https://aghmnl.github.io/senior-forge-codex/es/glosario/looper/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread-pool/
https://aghmnl.github.io/senior-forge-codex/es/glosario/jank/
https://aghmnl.github.io/senior-forge-codex/es/glosario/anr/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dao/
https://aghmnl.github.io/senior-forge-codex/es/glosario/room/
https://aghmnl.github.io/senior-forge-codex/es/glosario/retrofit/
https://aghmnl.github.io/senior-forge-codex/es/glosario/okhttp/
https://aghmnl.github.io/senior-forge-codex/es/glosario/flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/datastore/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatchers-main-immediate/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatcher/
https://aghmnl.github.io/senior-forge-codex/es/glosario/test-dispatcher/
https://aghmnl.github.io/senior-forge-codex/es/glosario/strict-mode/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatchers-default/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatchers-io/
https://aghmnl.github.io/senior-forge-codex/es/glosario/run-blocking/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread/
https://aghmnl.github.io/senior-forge-codex/es/glosario/count-down-latch/
https://aghmnl.github.io/senior-forge-codex/es/glosario/callbacks/
https://aghmnl.github.io/senior-forge-codex/es/glosario/launched-effect/
https://aghmnl.github.io/senior-forge-codex/es/glosario/produce-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/composable/
https://aghmnl.github.io/senior-forge-codex/es/glosario/run-test/
https://aghmnl.github.io/senior-forge-codex/es/glosario/io-dispatcher/
https://aghmnl.github.io/senior-forge-codex/es/glosario/content-resolver/
https://aghmnl.github.io/senior-forge-codex/es/glosario/application-on-create/
https://aghmnl.github.io/senior-forge-codex/es/glosario/profiling/
https://aghmnl.github.io/senior-forge-codex/es/glosario/launch/
https://aghmnl.github.io/senior-forge-codex/es/glosario/advance-until-idle/

**Fuentes oficiales (agregar cada una como fuente web)**
https://developer.android.com/kotlin/coroutines
https://developer.android.com/kotlin/coroutines/coroutines-adv
https://developer.android.com/kotlin/coroutines/coroutines-best-practices
https://developer.android.com/kotlin/coroutines/test
https://developer.android.com/topic/performance/vitals/anr
https://developer.android.com/topic/performance/vitals/render
https://developer.android.com/training/data-storage/room/async-queries
https://developer.android.com/topic/libraries/architecture/datastore
https://developer.android.com/develop/ui/compose/side-effects
https://developer.android.com/reference/android/os/StrictMode
https://kotlinlang.org/docs/coroutine-context-and-dispatchers.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/with-context.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-dispatchers/

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Main-Safety
2. Agregá el artículo principal como fuente web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Intermedio.

Ya domina: sabe que Room y Retrofit ya ejecutan sus llamadas suspend fuera del main thread y que envolverlas en withContext(Dispatchers.IO) no es necesario; asigna correctamente Dispatchers.Default a la aritmética pesada y Dispatchers.IO a la lectura de archivos; tiene claro que main-safe no significa rápido sino no bloquear el main thread; sabe que viewModelScope corre en el main thread. Tratar la elección IO vs Default y la regla "no envolver Room/Retrofit" como repaso rápido.

Necesita explicación en profundidad: la definición precisa de main-safe (se puede llamar desde el main thread y solo suspende, el trabajo bloqueante corre en otro dispatcher); por qué la responsabilidad es del llamado — el dispatcher se hereda, así que el withContext va adentro de la función que bloquea, una sola vez; por qué suspend no garantiza nada: File(path).readText() no tiene ningún suspension point, así que bloquea aunque la función sea suspend; la forma canónica withContext(Dispatchers.IO) como cuerpo de la función; inyección del dispatcher con @IoDispatcher y cómo un test con runTest + StandardTestDispatcher puede afirmar que la función suspendió (job activo antes de advanceUntilIdle) en vez de bloquear.

Malentendidos a corregir: explica que readText() no es main-safe porque "no libera recursos hasta que termina" — la razón real es que no hay ningún suspension point: la coroutine nunca suspende, así que el main thread queda ocupado ejecutando la lectura. Y describió main-safe como "no detener todo el proceso": lo que se detiene es el main thread (frames e input), no el proceso; la consecuencia es jank y, a los 5 segundos, ANR.

Instrucción para el Audio Overview: explicá desde cero, con analogías, por qué el dispatcher se hereda y eso hace que la main-safety sea responsabilidad de la función que bloquea, por qué la palabra suspend no mueve nada a ningún lado, y cómo se prueba en un test que una función suspende en vez de bloquear; tratá IO vs Default y "Room ya es main-safe" como repaso de una frase.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Kotlin coroutines on Android | La definición oficial de main-safety y la convención "toda suspend function es main-safe". |
| Improve app performance with coroutines | El ejemplo canónico: `withContext(Dispatchers.IO)` adentro del repositorio, no en el ViewModel. |
| Best practices for coroutines | "Suspend functions should be main-safe", inyección de dispatchers, no envolver lo que ya es seguro. |
| Testing Kotlin coroutines on Android | `runTest`, `StandardTestDispatcher`, inyección de dispatchers para probar la suspensión. |
| ANRs | Qué es un ANR, el límite de 5 s sin procesar input, causas típicas en el main thread. |
| Slow rendering | El presupuesto de 16 ms por frame y el jank como consecuencia de bloquear Main. |
| Write asynchronous DAO queries | Cómo Room ejecuta los métodos `suspend` y los `Flow` fuera del main thread. |
| DataStore | Por qué las lecturas y escrituras de DataStore son main-safe por diseño. |
| Side-effects in Compose | `LaunchedEffect` y `produceState` corren en Main; dónde va el `withContext`. |
| `StrictMode` (referencia) | La herramienta para detectar disk/network en el main thread durante desarrollo. |
| Coroutine context and dispatchers | Herencia del dispatcher y semántica de `withContext`. |
| `withContext` (API) | Contrato exacto: suspende, corre el bloque en el dispatcher destino, vuelve al original. |
| `Dispatchers` (API) | Main, IO y Default: tamaño de cada pool y para qué trabajo está pensado. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Main-Safety", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Qué significa que una suspend function sea "main-safe"? ¿De quién es la responsabilidad de garantizarlo: del que la llama o del que la escribe? ¿Por qué?
2. `suspend fun load(): String = File(path).readText()` — ¿es main-safe? ¿Qué pasa si la llamás desde `viewModelScope`? ¿Qué cambiarías?
3. ¿Hace falta envolver `dao.insert(x)` (método `suspend` de Room) o una llamada `suspend` de Retrofit en `withContext(Dispatchers.IO)`? ¿Por qué sí o por qué no?
4. Una función hace aritmética de fechas pesada (sin I/O) y otra lee un archivo. ¿A qué dispatcher mandás cada una y por qué? ¿"Main-safe" significa "rápido"?
5. Heredás un repositorio que bloquea Main. ¿Cómo lo arreglás y cómo lo probás en un test de forma determinista (qué inyectás, qué afirmás y en qué momento)?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: llamable desde Main sin bloquear; responsabilidad del llamado porque el dispatcher se hereda; `withContext` adentro. Junior: cree que `suspend` ya lo garantiza.
- P2 Senior: no es main-safe (sin suspension point); bloquea Main desde `viewModelScope`; `withContext(IO)` adentro. Junior: cree que es main-safe por ser `suspend`.
- P3 Senior: no; Room/Retrofit/DataStore ya son main-safe; envolver es ruido. Junior: envuelve todo.
- P4 Senior: CPU → Default, I/O → IO, con consecuencias de equivocarse; main-safe ≠ rápido. Intermedio: todo a IO.
- P5 Senior: profiling, envolver solo lo bloqueante, inyectar dispatcher, `runTest` + `StandardTestDispatcher`, afirmar suspensión antes de avanzar. Junior: `Thread.sleep`/`runBlocking`.
```
