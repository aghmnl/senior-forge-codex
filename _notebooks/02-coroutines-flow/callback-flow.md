---
topic: "callbackFlow"
chapter: 02-coroutines-flow
slug: callback-flow
lang: es
article: /es/02-coroutines-flow/callback-flow/
diagnostic_date: 2026-10-09
---

# Notebook de estudio — callbackFlow

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. Una API te avisa con un listener cada vez que cambia el estado de la red, desde un thread propio. ¿Por qué no podés armar el Flow con `flow { }` y llamar a `emit` adentro del listener?
2. Adentro de un `callbackFlow`, ¿qué hace `awaitClose { }`? ¿Qué pasa si lo omitís?
3. Una API te llama de vuelta **una sola vez**, con `onSuccess(result)` o `onFailure(error)`. ¿Usarías `callbackFlow` para convertirla a coroutines? Si no, ¿qué usarías?
4. Adentro de un `callbackFlow`, la API te informa un error a través del callback. ¿Cómo hacés para que ese error le llegue al collector?
5. ¿Qué tamaño de buffer tiene `callbackFlow` por defecto, y qué le pasa a `trySend` cuando ese buffer se llena?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | `emit` es una **suspend function** y el listener no puede suspender; además `flow { }` exige que cada `emit` ocurra en la coroutine que colecta, y emitir desde otro thread falla en Runtime ("Flow invariant is violated"). Por eso existe **`callbackFlow`**, que tiene un channel adentro y se alimenta con `trySend`. | Sabe que hay que usar `callbackFlow` pero no explica por qué `flow { }` falla. | No sabe la diferencia. |
| 2 | Suspende el bloque mientras el flow se colecta y, cuando la colección se detiene, ejecuta su lambda, donde se **desregistra el listener**. Sin él, el flow falla con una **`IllegalStateException`**; sin la lambda de limpieza, el listener queda registrado (leak). | Sabe que sirve para limpiar pero no qué pasa si se omite. | No lo conoce. |
| 3 | No: para un callback de **un solo valor** se usa **`suspendCancellableCoroutine`**, que lo convierte en una suspend function que devuelve el resultado o lanza el error. `callbackFlow` es para callbacks que se disparan muchas veces. | Intuye que un flow no encaja pero no conoce la alternativa. | Usaría `callbackFlow` igual. |
| 4 | Llamando a **`close(exception)`**: la colección falla con esa excepción y un `catch` downstream la puede manejar. Hacer `throw` adentro del callback corre en el thread de la API y el collector nunca lo ve. | Sabe que hay que cerrar el flow pero no que se pasa la excepción. | Haría `throw` en el callback. |
| 5 | **64 valores** (`BUFFERED`, con overflow que suspende). Cuando se llena, **`trySend` falla** sin esperar y, si no se revisa el resultado, el valor se pierde en silencio. Para "solo el último", `conflate()`; si cada valor importa, un buffer mayor. | Sabe que hay un buffer y que se pierden valores pero no el tamaño o la solución. | No sabe qué pasa. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior a Senior; 3+ intermedias o mezcla a Intermedio; 3+ junior o "no sé" a Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-10-09

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Junior | "No sé". No conoce por qué `flow { }` no sirve para emitir desde un callback. |
| 2 | Junior | "No sé". No conoce `awaitClose` ni su rol en el desregistro del listener. |
| 3 | Junior | "No sé". No conoce `suspendCancellableCoroutine` para callbacks de un solo valor. |
| 4 | Junior | "No sé". No sabe propagar un error con `close(exception)`. |
| 5 | Junior | "No sé". No conoce el buffer por defecto ni la falla de `trySend` al llenarse. |

**Nivel global: Junior** (0 Senior, 0 intermedias, 5 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de estudiar Channel (Hot Streams), trySend() vs send() y receiveAsFlow(), así que conoce los channels y el papel de trySend; conviene presentar callbackFlow como un Flow con un channel adentro, alimentado con trySend desde un callback.

Necesita explicación en profundidad, desde cero: por qué no se puede usar flow { } con emit adentro de un listener (emit es una suspend function y emitir desde otro thread rompe el invariante de Flow); qué hace awaitClose, que mantiene vivo el flow mientras se colecta y desregistra el listener cuando la colección se detiene, y por qué omitirlo provoca una IllegalStateException; por qué un callback de un solo valor se convierte con suspendCancellableCoroutine y no con callbackFlow; cómo se propaga un error con close(exception) para que lo reciba el collector; y el buffer por defecto de 64 valores, por qué trySend falla en silencio cuando se llena y cuándo usar conflate().

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una suscripción a un diario: te llega cada mañana mientras estás suscrito, y al darte de baja dejan de mandarlo), qué es callbackFlow y por qué no sirve flow { }, después awaitClose y el desregistro del listener, después la diferencia con suspendCancellableCoroutine, y cerrá con close(exception) y el buffer de trySend.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
callbackFlow

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/callback-flow/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/channel-hot-streams/
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/trysend-vs-send/
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/sharein-statein/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/api/
https://aghmnl.github.io/senior-forge-codex/es/glosario/listener/
https://aghmnl.github.io/senior-forge-codex/es/glosario/flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/callbacks/
https://aghmnl.github.io/senior-forge-codex/es/glosario/try-send/
https://aghmnl.github.io/senior-forge-codex/es/glosario/send/
https://aghmnl.github.io/senior-forge-codex/es/glosario/emit/
https://aghmnl.github.io/senior-forge-codex/es/glosario/close/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collector/
https://aghmnl.github.io/senior-forge-codex/es/glosario/producer-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutine-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/send-channel/
https://aghmnl.github.io/senior-forge-codex/es/glosario/channel/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutines/
https://aghmnl.github.io/senior-forge-codex/es/glosario/buffer/
https://aghmnl.github.io/senior-forge-codex/es/glosario/conflate/
https://aghmnl.github.io/senior-forge-codex/es/glosario/await-close/
https://aghmnl.github.io/senior-forge-codex/es/glosario/illegal-state-exception/
https://aghmnl.github.io/senior-forge-codex/es/glosario/callback-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/channel-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/on-success-on-failure/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspend-cancellable-coroutine/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspend-functions/
https://aghmnl.github.io/senior-forge-codex/es/glosario/repeat-on-lifecycle/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel/
https://aghmnl.github.io/senior-forge-codex/es/glosario/init/
https://aghmnl.github.io/senior-forge-codex/es/glosario/share-in/
https://aghmnl.github.io/senior-forge-codex/es/glosario/state-in/
https://aghmnl.github.io/senior-forge-codex/es/glosario/while-subscribed/
https://aghmnl.github.io/senior-forge-codex/es/glosario/throw/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sdk/
https://aghmnl.github.io/senior-forge-codex/es/glosario/catch/
https://aghmnl.github.io/senior-forge-codex/es/glosario/downstream/
https://aghmnl.github.io/senior-forge-codex/es/glosario/flow-builder/
https://aghmnl.github.io/senior-forge-codex/es/glosario/runtime/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/callback-flow.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/await-close.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/channel-flow.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-producer-scope/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/suspend-cancellable-coroutine.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/conflate.html
https://kotlinlang.org/docs/flow.html
https://developer.android.com/kotlin/flow

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: callbackFlow
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de estudiar Channel (Hot Streams), trySend() vs send() y receiveAsFlow(), así que conoce los channels y el papel de trySend; conviene presentar callbackFlow como un Flow con un channel adentro, alimentado con trySend desde un callback.

Necesita explicación en profundidad, desde cero: por qué no se puede usar flow { } con emit adentro de un listener (emit es una suspend function y emitir desde otro thread rompe el invariante de Flow); qué hace awaitClose, que mantiene vivo el flow mientras se colecta y desregistra el listener cuando la colección se detiene, y por qué omitirlo provoca una IllegalStateException; por qué un callback de un solo valor se convierte con suspendCancellableCoroutine y no con callbackFlow; cómo se propaga un error con close(exception) para que lo reciba el collector; y el buffer por defecto de 64 valores, por qué trySend falla en silencio cuando se llena y cuándo usar conflate().

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una suscripción a un diario: te llega cada mañana mientras estás suscrito, y al darte de baja dejan de mandarlo), qué es callbackFlow y por qué no sirve flow { }, después awaitClose y el desregistro del listener, después la diferencia con suspendCancellableCoroutine, y cerrá con close(exception) y el buffer de trySend.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| `callbackFlow` (API) | El contrato: el bloque corre en un `ProducerScope`, se alimenta con `trySend` y tiene que terminar con `awaitClose`. |
| `awaitClose` (API) | Suspende hasta que el flow se cancela o se cierra y ejecuta la limpieza. |
| `channelFlow` (API) | El builder general del que `callbackFlow` es un caso particular; buffer por defecto y ejemplos. |
| `ProducerScope` (API) | El receptor del bloque: un `CoroutineScope` que además es un `SendChannel`. |
| `suspendCancellableCoroutine` (API) | El puente para callbacks de un solo valor. |
| `conflate` (API) | Cómo quedarse solo con el último valor cuando el collector es lento. |
| Asynchronous Flow | La guía oficial de Flow, con el invariante de contexto que `flow { }` exige. |
| Kotlin flows on Android | La sección sobre convertir APIs basadas en callbacks en flows con `callbackFlow`. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "callbackFlow", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. Una API te avisa con un listener cada vez que cambia el estado de la red, desde un thread propio. ¿Por qué no podés armar el Flow con `flow { }` y llamar a `emit` adentro del listener?
2. Adentro de un `callbackFlow`, ¿qué hace `awaitClose { }`? ¿Qué pasa si lo omitís?
3. Una API te llama de vuelta **una sola vez**, con `onSuccess(result)` o `onFailure(error)`. ¿Usarías `callbackFlow` para convertirla a coroutines? Si no, ¿qué usarías?
4. Adentro de un `callbackFlow`, la API te informa un error a través del callback. ¿Cómo hacés para que ese error le llegue al collector?
5. ¿Qué tamaño de buffer tiene `callbackFlow` por defecto, y qué le pasa a `trySend` cuando ese buffer se llena?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: emit es suspend y el listener no puede suspender; flow { } exige emitir desde la coroutine que colecta y emitir desde otro thread rompe el invariante; por eso existe callbackFlow con trySend. Junior: no sabe la diferencia.
- P2 Senior: awaitClose suspende mientras se colecta y al detenerse la colección desregistra el listener; sin él el flow falla con IllegalStateException. Junior: no lo conoce.
- P3 Senior: para un solo valor se usa suspendCancellableCoroutine, no callbackFlow. Junior: usaría callbackFlow igual.
- P4 Senior: close(exception) hace que la colección falle con esa excepción; un throw en el callback no llega al collector. Junior: haría throw.
- P5 Senior: buffer de 64 (BUFFERED); cuando se llena trySend falla y el valor se pierde en silencio; conflate() si solo importa el último. Junior: no sabe.
```
