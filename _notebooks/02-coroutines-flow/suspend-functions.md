# Notebook de estudio — Suspend Functions

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.
> Capítulo II — Coroutines & Flow · Artículo: https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/suspend-functions/

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Qué cambia exactamente cuando marcás una función con `suspend`? ¿En qué thread corre?
2. Un compañero envuelve `File.readText()` en una `suspend fun` y la llama desde `viewModelScope.launch`. La UI se congela igual. ¿Por qué, y qué cambiarías?
3. ¿Qué pasa con una coroutine cuando se cancela el scope que la lanzó? ¿Se detiene en cualquier punto o en puntos específicos?
4. ¿Qué problema tiene envolver una llamada suspendible en `runCatching { }` o en `catch (e: Exception)`?
5. ¿Cuándo es aceptable usar `runBlocking` en una app Android, y cuándo no?

### Rúbrica

| # | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | Es un contrato de compile time: solo puede llamarse desde una coroutine u otra suspend fun. El compilador la reescribe en CPS: parámetro `Continuation` oculto, retorno `Any?`, cuerpo como state machine. Corre en el thread del llamador hasta el primer suspension point; `suspend` no cambia de thread por sí solo. | Sabe que "puede pausarse sin bloquear" y que necesita una coroutine, pero no puede explicar el mecanismo (continuation / state machine) ni afirma con claridad que no cambia de thread. | Cree que `suspend` mueve el trabajo a background o que es equivalente a `async`. |
| 2 | `suspend` no hace no-bloqueante a una llamada bloqueante; solo un suspension point real libera el thread. `viewModelScope` corre en `Main.immediate`, así que `readText()` bloquea Main. Fix: hacer la función *main-safe* con `withContext(Dispatchers.IO)` **adentro** de la suspend fun, no en cada call site. | Identifica que falta `withContext(Dispatchers.IO)` pero lo pondría en el `launch` (call site) o no explica por qué `suspend` solo no alcanza. | Propone `Thread`, `AsyncTask`, `GlobalScope` o cree que el problema es el ViewModel. |
| 3 | Cancelación cooperativa: la coroutine se cancela solo cuando alcanza un suspension point (o chequea `isActive`/`ensureActive()`), donde se lanza `CancellationException`. Un loop de CPU sin suspender es incancelable. Los `finally` corren; `NonCancellable` para cleanup. | Sabe que "se cancela sola" al limpiar el ViewModel, pero no que es cooperativa ni que el código sin suspension points sigue corriendo. | Cree que la cancelación es inmediata/preemptiva, o que hay que cancelar a mano cada coroutine. |
| 4 | Ambos atrapan `CancellationException` (extiende `IllegalStateException`), así la coroutine sigue ejecutando después de haber sido cancelada (p. ej. escribiendo a disco con el ViewModel ya limpiado). Regla: atrapar lo manejable y relanzar `CancellationException`, o `ensureActive()` después del catch. | Sabe que "hay excepciones que no conviene tragarse" pero no nombra `CancellationException` ni el efecto concreto. | No ve problema alguno; considera `runCatching` una buena práctica universal. |
| 5 | Es el puente desde código sin coroutine: `main()`, tests (mejor `runTest`), y excepcionalmente `Application.onCreate` cuando un valor se necesita antes del primer frame — siempre con comentario que justifique. Nunca en ViewModel, Composable o repositorio; en Main puede deadlockear. | Sabe que bloquea y que "no se usa en producción", pero no puede dar el caso legítimo ni el riesgo de deadlock. | Lo usa como forma general de llamar suspend funs desde código normal. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior → Senior; 3+ intermedias o mezcla → Intermedio; 3+ junior o "no sé" → Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario (continuation, state machine, main-safety, cancelación cooperativa, `CancellationException`, `runBlocking`).
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-09-14

| # | Nivel | Observación |
|---|---|---|
| 1 | Intermedia | Correcto que corre en el thread del llamador. Falta el mecanismo (continuation, state machine, contrato de compile time). Malentendido: cree que la intención de `suspend` es sacar el trabajo del main thread. |
| 2 | Intermedia | Identifica que hay que cambiar el thread y que `viewModelScope` corre en Main. Falta el por qué (`suspend` no hace no-bloqueante a `readText()`) y que `withContext(Dispatchers.IO)` va adentro de la suspend fun. |
| 3 | Junior | "Se detiene en el punto en que esté": modelo preemptivo; la cancelación es cooperativa, solo en suspension points. |
| 4 | Junior | No sé. |
| 5 | Junior | No sé. |

**Nivel global: Junior con base intermedia** (2 intermedias, 3 junior).

Texto "Nivel actual" entregado a Gemini:

```text
Nivel global: Junior con base intermedia.

Ya domina: sabe que una suspend function corre en el thread del llamador y que ese thread lo define la coroutine; sabe que viewModelScope corre en el main thread y que trabajo de disco/red ahí congela la UI. Estos dos puntos pueden tratarse como repaso rápido.

Necesita explicación en profundidad: el mecanismo de suspend (continuation, continuation-passing style, state machine, suspension point) y por qué es un contrato de compile time; main-safety y por qué withContext(Dispatchers.IO) va adentro de la suspend function y no en el call site; cancelación cooperativa, suspension points como únicos puntos de cancelación y CancellationException; el problema de runCatching / catch (e: Exception) tragándose la cancelación; runBlocking, sus usos legítimos (tests con runTest, Application.onCreate justificado) y sus riesgos (deadlock en Main).

Malentendidos a corregir: cree que la intención de suspend es sacar el trabajo del main thread (suspend no cambia de thread por sí solo); cree que una coroutine cancelada se detiene en cualquier punto (es cooperativa: solo en suspension points).

Instrucción para el Audio Overview: explicá desde cero, con analogías, qué hace realmente el compilador con suspend, la cancelación cooperativa y el peligro de tragarse CancellationException; tratá "corre en el thread del llamador" y "viewModelScope es Main" como repaso de una frase.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en NotebookLM para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Suspend Functions

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/suspend-functions/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspend-functions/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutines/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspension-point/
https://aghmnl.github.io/senior-forge-codex/es/glosario/continuation/
https://aghmnl.github.io/senior-forge-codex/es/glosario/continuation-passing-style/
https://aghmnl.github.io/senior-forge-codex/es/glosario/state-machine/
https://aghmnl.github.io/senior-forge-codex/es/glosario/blocking-call/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatcher/
https://aghmnl.github.io/senior-forge-codex/es/glosario/main-thread/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread-pool/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cooperative-cancellation/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cancellation-exception/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutine-scope-builder/
https://aghmnl.github.io/senior-forge-codex/es/glosario/run-blocking/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspend-cancellable-coroutine/
https://aghmnl.github.io/senior-forge-codex/es/glosario/callbacks/
https://aghmnl.github.io/senior-forge-codex/es/glosario/callback-hell/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dao/
https://aghmnl.github.io/senior-forge-codex/es/glosario/room/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel-store/
https://aghmnl.github.io/senior-forge-codex/es/glosario/compile-time/
https://aghmnl.github.io/senior-forge-codex/es/glosario/bytecode/
https://aghmnl.github.io/senior-forge-codex/es/glosario/keyword/
https://aghmnl.github.io/senior-forge-codex/es/glosario/return-type/
https://aghmnl.github.io/senior-forge-codex/es/glosario/heap/
https://aghmnl.github.io/senior-forge-codex/es/glosario/stack-frame/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/coroutines-basics.html
https://kotlinlang.org/docs/composing-suspending-functions.html
https://kotlinlang.org/docs/cancellation-and-timeouts.html
https://kotlinlang.org/docs/coroutine-context-and-dispatchers.html
https://kotlinlang.org/docs/exception-handling.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/run-blocking.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/suspend-cancellable-coroutine.html
https://developer.android.com/kotlin/coroutines
https://developer.android.com/kotlin/coroutines/coroutines-adv
https://developer.android.com/kotlin/coroutines/coroutines-best-practices
https://developer.android.com/topic/libraries/architecture/coroutines
https://developer.android.com/training/data-storage/room/async-queries

**Pasos de ejecución**
1. Creá un notebook nuevo en NotebookLM llamado exactamente: Suspend Functions
2. Agregá el artículo principal como fuente web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior con base intermedia.

Ya domina: sabe que una suspend function corre en el thread del llamador y que ese thread lo define la coroutine; sabe que viewModelScope corre en el main thread y que trabajo de disco/red ahí congela la UI. Estos dos puntos pueden tratarse como repaso rápido.

Necesita explicación en profundidad: el mecanismo de suspend (continuation, continuation-passing style, state machine, suspension point) y por qué es un contrato de compile time; main-safety y por qué withContext(Dispatchers.IO) va adentro de la suspend function y no en el call site; cancelación cooperativa, suspension points como únicos puntos de cancelación y CancellationException; el problema de runCatching / catch (e: Exception) tragándose la cancelación; runBlocking, sus usos legítimos (tests con runTest, Application.onCreate justificado) y sus riesgos (deadlock en Main).

Malentendidos a corregir: cree que la intención de suspend es sacar el trabajo del main thread (suspend no cambia de thread por sí solo); cree que una coroutine cancelada se detiene en cualquier punto (es cooperativa: solo en suspension points).

Instrucción para el Audio Overview: explicá desde cero, con analogías, qué hace realmente el compilador con suspend, la cancelación cooperativa y el peligro de tragarse CancellationException; tratá "corre en el thread del llamador" y "viewModelScope es Main" como repaso de una frase.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Coroutines basics | Qué es una coroutine, `launch`, scope, el primer contacto con `suspend`. |
| Composing suspending functions | Secuencial por defecto, `async` para concurrencia — la parte "Sequential by default" del artículo. |
| Cancellation and timeouts | Cancelación cooperativa, `isActive`/`ensureActive`, `finally`, `NonCancellable`. |
| Coroutine context and dispatchers | `Dispatchers.Main/IO/Default`, `withContext`, herencia del dispatcher. |
| Exception handling | Por qué `CancellationException` es especial y cómo se propagan las excepciones. |
| `runBlocking` (API) | Contrato exacto del builder que bloquea el thread. |
| `suspendCancellableCoroutine` (API) | Contrato del puente callback → suspend, `invokeOnCancellation`. |
| Kotlin coroutines on Android | Visión Android: main-safety, `viewModelScope`, patrones de uso. |
| Improve app performance with coroutines | El ejemplo canónico de `withContext(Dispatchers.IO)` dentro de la suspend fun. |
| Best practices for coroutines | Inyectar dispatchers, suspend funs main-safe, no exponer scopes. |
| Coroutines with lifecycle-aware components | `viewModelScope`, `lifecycleScope`, `repeatOnLifecycle`. |
| Room: async queries | DAOs con `suspend` y `Flow`; por qué Room ya es main-safe. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Suspend Functions", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Qué cambia exactamente cuando marcás una función con `suspend`? ¿En qué thread corre?
2. Un compañero envuelve `File.readText()` en una `suspend fun` y la llama desde `viewModelScope.launch`. La UI se congela igual. ¿Por qué, y qué cambiarías?
3. ¿Qué pasa con una coroutine cuando se cancela el scope que la lanzó? ¿Se detiene en cualquier punto o en puntos específicos?
4. ¿Qué problema tiene envolver una llamada suspendible en `runCatching { }` o en `catch (e: Exception)`?
5. ¿Cuándo es aceptable usar `runBlocking` en una app Android, y cuándo no?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: contrato de compile time, CPS con Continuation oculta y state machine, corre en el thread del llamador hasta el primer suspension point. Junior: cree que `suspend` mueve el trabajo a background.
- P2 Senior: `suspend` no hace no-bloqueante a una llamada bloqueante; `viewModelScope` corre en Main.immediate; fix con `withContext(Dispatchers.IO)` adentro de la suspend fun (main-safety). Intermedio: pone el withContext en el call site.
- P3 Senior: cancelación cooperativa en suspension points, `CancellationException`, un loop de CPU sin suspender es incancelable, `NonCancellable` para cleanup. Junior: cree que es preemptiva.
- P4 Senior: ambos atrapan `CancellationException` y la coroutine sigue tras ser cancelada; relanzarla o `ensureActive()`. Junior: no ve problema.
- P5 Senior: puente desde código sin coroutine (`main`, tests → `runTest`, `Application.onCreate` justificado); nunca en ViewModel/Composable/repositorio; deadlock en Main. Junior: lo usa como forma general de llamar suspend funs.
```
