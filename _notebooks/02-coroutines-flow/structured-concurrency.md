# Notebook de estudio — Structured Concurrency

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.
> Capítulo II — Coroutines & Flow · Artículo: https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/structured-concurrency/

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Qué significa que las coroutines sean "estructuradas"? ¿Qué relación hay entre una coroutine lanzada con `launch` y el scope desde el que se lanzó, y qué garantías salen de esa relación?
2. Tenés una lista de IDs y lanzás una escritura por cada uno con `ids.forEach { launch { write(it) } }` dentro de `viewModelScope.launch { }`. ¿Qué cambia si envolvés ese loop en `coroutineScope { }`? ¿Cuándo corre la línea que viene después del loop en cada caso?
3. Un hijo lanza una excepción no capturada. ¿Qué pasa con sus hermanos y con el padre si el padre es un `Job` común? ¿Y si es un `SupervisorJob` o estás dentro de `supervisorScope`?
4. ¿Cómo se cancela realmente una coroutine? ¿En qué momento se detiene, qué es `CancellationException`, y qué problema aparece si la atrapás con un `catch (e: Exception)` y no la relanzás?
5. ¿Qué diferencia hay entre `launch` y `async` en cuanto a resultado y en cuanto a qué pasa cuando fallan? Si dos `async` corren dentro de un `coroutineScope` y uno falla, ¿alcanza con un `try/catch` alrededor de su `await()` para conservar el otro?

### Rúbrica

| # | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | Toda coroutine tiene un `Job` padre en el scope que la lanzó; forman un árbol con raíz en un `CoroutineScope`. Garantías: el padre espera a los hijos, la cancelación fluye hacia abajo, el fallo fluye hacia arriba, nada sobrevive a su padre (sin leaks). `GlobalScope` rompe esto. | Sabe que "las coroutines se cancelan con el scope" pero no describe el árbol de `Job`s ni enumera las garantías. | Cree que `launch` arranca un thread independiente, o no distingue scope de dispatcher. |
| 2 | Sin wrapper: los `launch` se cuelgan de `viewModelScope`, el `forEach` retorna al instante y la línea siguiente corre con escrituras en vuelo. Con `coroutineScope`: crea un `Job` hijo, suspende hasta que terminan todos, y la línea siguiente corre cuando aterrizó la última; si una falla, cancela a las hermanas y relanza. | Sabe que `coroutineScope` "espera", pero no explica que sin él el código sigue de inmediato, o no menciona qué pasa ante un fallo. | No conoce `coroutineScope { }` como builder, o cree que `launch` bloquea. |
| 3 | `Job` común: el hijo que falla cancela al padre, que cancela a los hermanos, y la excepción sigue subiendo. `SupervisorJob` / `supervisorScope`: el fallo queda en el hijo, los hermanos siguen, la excepción va al `CoroutineExceptionHandler` (o crashea si no hay). `viewModelScope` es supervisor. | Sabe que `SupervisorJob` "aísla fallos" pero no describe el camino completo (padre → hermanos) ni adónde va la excepción. | Cree que una excepción en un hijo solo afecta a ese hijo siempre, o no conoce `SupervisorJob`. |
| 4 | `cancel()` marca el `Job`; la coroutine se detiene en su próximo suspension point, donde el Runtime lanza `CancellationException`. Es cooperativa: un loop de CPU necesita `ensureActive()` / `isActive`. `CancellationException` es terminación normal, no fallo. Tragarla deja la coroutine corriendo cancelada y el padre esperándola; hay que relanzarla. | Sabe que la cancelación es "cooperativa" o que hay que relanzar `CancellationException`, pero no ambas cosas ni por qué. | Cree que `cancel()` detiene la coroutine de inmediato, o no conoce `CancellationException`. |
| 5 | `launch` → `Job`, para efectos; `async` → `Deferred<T>`, para valores, con `await()`. Fallo en `async`: se guarda en el `Deferred` y se relanza en `await()`, pero *también* falla al padre de inmediato. Dentro de `coroutineScope`, el `try/catch` en `await()` no alcanza: el otro `async` ya fue cancelado. Hace falta `supervisorScope`. | Distingue `launch`/`async` por el resultado, pero cree que el `try/catch` en `await()` alcanza para aislar el fallo. | No distingue `launch` de `async`, o cree que `async` es "launch en otro thread". |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior → Senior; 3+ intermedias o mezcla → Intermedio; 3+ junior o "no sé" → Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-09-15

| # | Nivel | Observación |
|---|---|---|
| 1 | Junior | No sé. |
| 2 | Junior | No sé. |
| 3 | Intermedia | La idea central es correcta: `Job` común → padre y hermanos se cancelan; `SupervisorJob` → solo el hijo. Falta el camino completo (hijo → padre → hermanos → sigue subiendo) y adónde va la excepción con supervisor (`CoroutineExceptionHandler`, o crash si no hay). |
| 4 | Intermedia | Correcto que se detiene en un punto de suspensión y que hay que relanzar. Falta: la cancelación es cooperativa (`ensureActive()` / `isActive` en loops de CPU) y `CancellationException` es terminación normal. Malentendido: el problema de tragarla no es que "nadie se entere" — es que la coroutine sigue corriendo cancelada y el padre la espera sin poder completar. |
| 5 | Junior | No sé. |

**Nivel global: Junior con base intermedia** (2 intermedias, 3 junior).

Texto "Nivel actual" entregado a Gemini:

```text
Nivel global: Junior con base intermedia.

Ya domina: sabe que con un Job común el fallo de un hijo termina al padre y a los hermanos, y que con SupervisorJob el fallo queda en el hijo; sabe que una coroutine se cancela cuando llega a un punto de suspensión y que una CancellationException atrapada con catch (e: Exception) debe relanzarse. Tratar la diferencia Job vs SupervisorJob como repaso, profundizando solo en adónde va la excepción.

Necesita explicación en profundidad: qué es Structured Concurrency como árbol de Jobs con raíz en un CoroutineScope y sus cuatro garantías (el padre espera a los hijos, la cancelación fluye hacia abajo, el fallo fluye hacia arriba, nada sobrevive a su padre); el builder coroutineScope { } y qué cambia respecto de lanzar launch directo sobre viewModelScope (suspender hasta que terminan todos vs. seguir de inmediato); supervisorScope y CoroutineExceptionHandler como destino de la excepción; cancelación cooperativa, ensureActive() e isActive en loops de CPU; por qué CancellationException es terminación normal y no un fallo; launch vs async, Deferred y await(), y por qué dentro de coroutineScope un try/catch alrededor de await() no aísla el fallo de un async (hace falta supervisorScope).

Malentendidos a corregir: cree que tragarse una CancellationException hace que "la app siga como si nada" — el problema real es el inverso: la coroutine queda cancelada pero sigue ejecutándose, y su padre la espera sin poder completar.

Instrucción para el Audio Overview: explicá desde cero, con analogías, el árbol de Jobs y sus cuatro garantías, qué hace coroutineScope { } frente a un loop de launch suelto, y la diferencia launch/async con su semántica de fallo; tratá Job vs SupervisorJob como repaso de una frase y dedicá tiempo a por qué CancellationException es terminación normal y hay que relanzarla.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en NotebookLM para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Structured Concurrency

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/structured-concurrency/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutines/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutine-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/runtime/
https://aghmnl.github.io/senior-forge-codex/es/glosario/job/
https://aghmnl.github.io/senior-forge-codex/es/glosario/launch/
https://aghmnl.github.io/senior-forge-codex/es/glosario/async/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutine-context/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutine-scope-builder/
https://aghmnl.github.io/senior-forge-codex/es/glosario/supervisor-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspend-functions/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/on-cleared/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collector/
https://aghmnl.github.io/senior-forge-codex/es/glosario/supervisor-job/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutine-exception-handler/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatcher/
https://aghmnl.github.io/senior-forge-codex/es/glosario/deferred/
https://aghmnl.github.io/senior-forge-codex/es/glosario/await/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cooperative-cancellation/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspension-point/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cancellation-exception/
https://aghmnl.github.io/senior-forge-codex/es/glosario/ensure-active/
https://aghmnl.github.io/senior-forge-codex/es/glosario/is-active/
https://aghmnl.github.io/senior-forge-codex/es/glosario/callbacks/
https://aghmnl.github.io/senior-forge-codex/es/glosario/global-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/memory-leaks/
https://aghmnl.github.io/senior-forge-codex/es/glosario/finally/
https://aghmnl.github.io/senior-forge-codex/es/glosario/singleton-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/run-test/
https://aghmnl.github.io/senior-forge-codex/es/glosario/advance-until-idle/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collect/
https://aghmnl.github.io/senior-forge-codex/es/glosario/flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/launched-effect/
https://aghmnl.github.io/senior-forge-codex/es/glosario/scroll-by/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/coroutines-basics.html
https://kotlinlang.org/docs/composing-suspending-functions.html
https://kotlinlang.org/docs/cancellation-and-timeouts.html
https://kotlinlang.org/docs/exception-handling.html
https://kotlinlang.org/docs/coroutine-context-and-dispatchers.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/coroutine-scope.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/supervisor-scope.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/async.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-job/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/ensure-active.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-cancellation-exception/
https://developer.android.com/kotlin/coroutines
https://developer.android.com/kotlin/coroutines/coroutines-adv
https://developer.android.com/kotlin/coroutines/coroutines-best-practices
https://developer.android.com/kotlin/coroutines/test
https://developer.android.com/topic/libraries/architecture/coroutines
https://developer.android.com/develop/ui/compose/side-effects

**Pasos de ejecución**
1. Creá un notebook nuevo en NotebookLM llamado exactamente: Structured Concurrency
2. Agregá el artículo principal como fuente web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior con base intermedia.

Ya domina: sabe que con un Job común el fallo de un hijo termina al padre y a los hermanos, y que con SupervisorJob el fallo queda en el hijo; sabe que una coroutine se cancela cuando llega a un punto de suspensión y que una CancellationException atrapada con catch (e: Exception) debe relanzarse. Tratar la diferencia Job vs SupervisorJob como repaso, profundizando solo en adónde va la excepción.

Necesita explicación en profundidad: qué es Structured Concurrency como árbol de Jobs con raíz en un CoroutineScope y sus cuatro garantías (el padre espera a los hijos, la cancelación fluye hacia abajo, el fallo fluye hacia arriba, nada sobrevive a su padre); el builder coroutineScope { } y qué cambia respecto de lanzar launch directo sobre viewModelScope (suspender hasta que terminan todos vs. seguir de inmediato); supervisorScope y CoroutineExceptionHandler como destino de la excepción; cancelación cooperativa, ensureActive() e isActive en loops de CPU; por qué CancellationException es terminación normal y no un fallo; launch vs async, Deferred y await(), y por qué dentro de coroutineScope un try/catch alrededor de await() no aísla el fallo de un async (hace falta supervisorScope).

Malentendidos a corregir: cree que tragarse una CancellationException hace que "la app siga como si nada" — el problema real es el inverso: la coroutine queda cancelada pero sigue ejecutándose, y su padre la espera sin poder completar.

Instrucción para el Audio Overview: explicá desde cero, con analogías, el árbol de Jobs y sus cuatro garantías, qué hace coroutineScope { } frente a un loop de launch suelto, y la diferencia launch/async con su semántica de fallo; tratá Job vs SupervisorJob como repaso de una frase y dedicá tiempo a por qué CancellationException es terminación normal y hay que relanzarla.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Coroutines basics | La definición oficial de structured concurrency: scope, `launch`, el padre espera a los hijos. |
| Composing suspending functions | `async`/`await`, descomposición paralela, y por qué `async` dentro de `coroutineScope` cancela al hermano si falla. |
| Cancellation and timeouts | Cancelación cooperativa, `isActive`, `ensureActive()`, `finally`, `NonCancellable`, `withTimeout`. |
| Exception handling | Propagación de fallos por el árbol, `CoroutineExceptionHandler`, `SupervisorJob` y `supervisorScope`, excepciones en `async`. |
| Coroutine context and dispatchers | El `Job` como elemento del contexto y la relación padre-hijo entre `Job`s. |
| `coroutineScope` (API) | Contrato exacto: espera a los hijos, cancela hermanos ante un fallo y relanza. |
| `supervisorScope` (API) | Contrato exacto de la variante supervisor. |
| `async` (API) | `Deferred`, cuándo falla al padre y cuándo se relanza en `await()`. |
| `Job` (API) | Estados del `Job` (Active, Completing, Cancelling, Completed), `cancel()`, `join()`, jerarquía padre-hijo. |
| `ensureActive` (API) | La comprobación explícita para loops de CPU sin suspension points. |
| `CancellationException` (API) | Por qué es terminación normal y no fallo. |
| Kotlin coroutines on Android | `viewModelScope`, `lifecycleScope` y por qué no usar `GlobalScope`. |
| Improve app performance with coroutines | Ejemplos de `coroutineScope` con `async` en paralelo. |
| Best practices for coroutines | No exponer scopes, no usar `GlobalScope`, cómo crear scopes propios cuando corresponde. |
| Testing Kotlin coroutines on Android | `runTest` como scope estructurado y cómo detecta coroutines filtradas. |
| Coroutines with lifecycle-aware components | `viewModelScope` (supervisor), `lifecycleScope`, `repeatOnLifecycle`. |
| Side-effects in Compose | `LaunchedEffect` y `rememberCoroutineScope` como scopes atados a la composición. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Structured Concurrency", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Qué significa que las coroutines sean "estructuradas"? ¿Qué relación hay entre una coroutine lanzada con `launch` y el scope desde el que se lanzó, y qué garantías salen de esa relación?
2. Tenés una lista de IDs y lanzás una escritura por cada uno con `ids.forEach { launch { write(it) } }` dentro de `viewModelScope.launch { }`. ¿Qué cambia si envolvés ese loop en `coroutineScope { }`? ¿Cuándo corre la línea que viene después del loop en cada caso?
3. Un hijo lanza una excepción no capturada. ¿Qué pasa con sus hermanos y con el padre si el padre es un `Job` común? ¿Y si es un `SupervisorJob` o estás dentro de `supervisorScope`?
4. ¿Cómo se cancela realmente una coroutine? ¿En qué momento se detiene, qué es `CancellationException`, y qué problema aparece si la atrapás con un `catch (e: Exception)` y no la relanzás?
5. ¿Qué diferencia hay entre `launch` y `async` en cuanto a resultado y en cuanto a qué pasa cuando fallan? Si dos `async` corren dentro de un `coroutineScope` y uno falla, ¿alcanza con un `try/catch` alrededor de su `await()` para conservar el otro?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: árbol de `Job`s con raíz en un scope; el padre espera, cancelación hacia abajo, fallo hacia arriba, sin leaks. Junior: cree que `launch` es un thread suelto.
- P2 Senior: sin `coroutineScope` la línea siguiente corre de inmediato; con él suspende hasta que terminan todos y ante un fallo cancela hermanos y relanza. Junior: no conoce el builder.
- P3 Senior: `Job` común → hijo cancela padre y hermanos; `SupervisorJob`/`supervisorScope` → aislado, va al handler o crashea. Junior: no conoce `SupervisorJob`.
- P4 Senior: cooperativa, se detiene en el suspension point con `CancellationException`, que es terminación normal y debe relanzarse; `ensureActive()` en loops de CPU. Junior: cree que `cancel()` es inmediato.
- P5 Senior: `async` devuelve `Deferred`, su fallo también cancela al padre; en `coroutineScope` el `try/catch` en `await()` no aísla, hace falta `supervisorScope`. Intermedio: cree que el `try/catch` alcanza.
```
