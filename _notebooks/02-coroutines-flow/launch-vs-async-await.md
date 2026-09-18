---
topic: "Launch vs Async/Await"
chapter: 02-coroutines-flow
slug: launch-vs-async-await
lang: es
article: /es/02-coroutines-flow/launch-vs-async-await/
diagnostic_date: 2026-09-16
---

# Notebook de estudio — Launch vs Async/Await

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Qué devuelve `launch` y qué devuelve `async`? ¿Qué podés hacer con cada cosa que devuelven, y cómo decidís cuál usar en un caso dado?
2. Tenés dos llamadas de red independientes y una tercera que necesita el resultado de la primera. Escribí (o describí) la forma con coroutines para que las independientes se solapen. ¿Dónde va `async` y dónde no?
3. Un bloque `async` lanza una excepción. ¿Dónde y cuándo aflora esa excepción? Si el `async` vive dentro de un `coroutineScope` junto a otro `async`, ¿qué le pasa al otro, y alcanza con un `try/catch` alrededor de `await()` para salvarlo?
4. ¿Qué hace `async { fetch() }.await()` escrito en una sola línea? ¿Y qué problema tiene un `async` cuyo `Deferred` nunca se espera?
5. Tenés N escrituras independientes a la base de datos que no devuelven nada y querés que corran en paralelo y esperar a que terminen todas. ¿Usás `launch` o `async`? ¿Qué es un `CompletableDeferred` y para qué lo usarías?

### Rúbrica

| #   | Respuesta Senior (incluye)                                                                                                                                                                                                                                                                   | Respuesta intermedia (le falta)                                                                                                                   | Señal junior                                                                                |
| --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 1   | `launch` → `Job` (cancel/join, sin valor; para efectos). `async` → `Deferred<T>` (extiende `Job`, `await()` suspende hasta el valor; para cómputos). Criterio: ¿necesito el valor? — no "¿es paralelo?".                                                                                     | Sabe que `async` "devuelve algo" y `launch` no, pero no nombra `Job`/`Deferred` ni formula el criterio.                                           | Cree que `async` es "launch en otro thread" o que uno es más rápido que el otro.            |
| 2   | Suspend fun con `coroutineScope` como cuerpo; `val a = async { }`, `val b = async { }`; `val c = fetchC(a.await())` como llamada secuencial plana; devuelve el valor armado. Sin `async` para la dependiente.                                                                                | Usa `async` para las dos independientes pero también envuelve la dependiente en `async` y la espera de inmediato, o no menciona `coroutineScope`. | No sabe cómo solapar, o propone threads / callbacks.                                        |
| 3   | Se guarda en el `Deferred` y se relanza en `await()`, _y además_ hace fallar al padre en el momento en que ocurre. Dentro de `coroutineScope` el otro `async` se cancela antes de llegar al `try/catch`; hace falta `supervisorScope` para aislar.                                           | Sabe que aflora en `await()` pero cree que el `try/catch` alrededor de `await()` alcanza para conservar al hermano.                               | No sabe dónde aflora, o cree que se pierde si nadie hace `await()`.                         |
| 4   | Es `fetch()` con allocations extra: no agrega concurrencia. Un `Deferred` sin `await` esconde su fallo — aunque bajo structured concurrency igual llega al padre; debió ser un `launch`.                                                                                                     | Identifica que `async().await()` en línea "no sirve" pero no explica por qué, o no ve el problema del `Deferred` sin esperar.                     | Cree que `async { }.await()` corre en paralelo con lo que sigue.                            |
| 5   | `launch` dentro de `coroutineScope { forEach { launch { } } }` — sin resultados no hay `Deferred` que esperar; `coroutineScope` ya espera a todos. `CompletableDeferred` es un `Deferred` que se completa a mano: compuerta para tests o puente de un callback de un solo disparo a suspend. | Elige `launch` pero no sabe que `coroutineScope` espera, o no conoce `CompletableDeferred`.                                                       | Elige `async` + `awaitAll()` para escrituras sin resultado "porque es paralelo", o no sabe. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior → Senior; 3+ intermedias o mezcla → Intermedio; 3+ junior o "no sé" → Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-09-16

| #   | Nivel      | Observación                                                                                                                                                                                                                                                                                                                                                                                    |
| --- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Junior     | No sé.                                                                                                                                                                                                                                                                                                                                                                                         |
| 2   | Junior     | No sé.                                                                                                                                                                                                                                                                                                                                                                                         |
| 3   | Intermedia | Correcto: la excepción aflora en `await()`. Falta la segunda vía: también hace fallar al padre en el momento en que ocurre, y por eso dentro de `coroutineScope` el otro `async` se cancela antes de que el `try/catch` pueda hacer nada. Malentendido: el problema del `try/catch` no es que "silencie" — es que no alcanza para salvar al hermano; para aislar hace falta `supervisorScope`. |
| 4   | Junior     | No sé.                                                                                                                                                                                                                                                                                                                                                                                         |
| 5   | Intermedia | `launch` es la elección correcta. Falta que `coroutineScope` ya espera a todos los hijos, y no conoce `CompletableDeferred`.                                                                                                                                                                                                                                                                   |

**Nivel global: Junior con base intermedia** (2 intermedias, 3 junior).

Texto "Nivel actual" entregado a Gemini:

```text
Nivel global: Junior con base intermedia.

Ya domina: intuye que la excepción de un async aflora en await(); elige launch (y no async) para N escrituras paralelas sin resultado. Tratar "launch para efectos sin valor" como repaso rápido.

Necesita explicación en profundidad: qué devuelve cada builder — launch devuelve un Job (cancel/join, sin valor) y async devuelve un Deferred<T> que extiende Job y cuyo await() suspende hasta el valor — y el criterio "¿necesito el valor?" para elegir; la forma canónica de paralelismo: suspend function con coroutineScope como cuerpo, dos async independientes y la llamada dependiente como suspend call plana; la doble vía del fallo de async (guardado en el Deferred para await() y a la vez propagado al Job padre en el momento), por qué dentro de coroutineScope el otro async se cancela antes del try/catch y por qué hace falta supervisorScope para aislar; por qué async { }.await() en una línea es una llamada normal con overhead y por qué un Deferred que nadie espera debió ser un launch; que coroutineScope ya espera a todos los launch hijos; CompletableDeferred como Deferred completado a mano (compuerta en tests, puente desde un callback de un solo disparo).

Malentendidos a corregir: cree que un try/catch alrededor de await() "silencia" el fallo del otro async — en realidad no lo alcanza: dentro de coroutineScope el hermano ya fue cancelado por la propagación al padre antes de llegar al catch; el problema no es silenciar sino que el catch no puede salvar al hermano.

Instrucción para el Audio Overview: explicá desde cero, con analogías, Job vs Deferred como "recibo sin valor" vs "promesa con valor", la forma coroutineScope + async + await para solapar llamadas independientes, y la doble vía del fallo de async con coroutineScope vs supervisorScope; tratá "launch para efectos" como repaso de una frase y dedicá tiempo a CompletableDeferred y a los dos olores (async().await() en línea y Deferred sin esperar).
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Launch vs Async/Await

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/launch-vs-async-await/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/launch/
https://aghmnl.github.io/senior-forge-codex/es/glosario/async/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutine-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutines/
https://aghmnl.github.io/senior-forge-codex/es/glosario/job/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutine-context/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutine-start/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cancel/
https://aghmnl.github.io/senior-forge-codex/es/glosario/join/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutine-exception-handler/
https://aghmnl.github.io/senior-forge-codex/es/glosario/deferred/
https://aghmnl.github.io/senior-forge-codex/es/glosario/await/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspension-point/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cooperative-cancellation/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cancellation-exception/
https://aghmnl.github.io/senior-forge-codex/es/glosario/await-all/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspend-functions/
https://aghmnl.github.io/senior-forge-codex/es/glosario/start/
https://aghmnl.github.io/senior-forge-codex/es/glosario/with-context/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatcher/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutine-scope-builder/
https://aghmnl.github.io/senior-forge-codex/es/glosario/supervisor-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/supervisor-job/
https://aghmnl.github.io/senior-forge-codex/es/glosario/try-catch/
https://aghmnl.github.io/senior-forge-codex/es/glosario/completable-deferred/
https://aghmnl.github.io/senior-forge-codex/es/glosario/callbacks/
https://aghmnl.github.io/senior-forge-codex/es/glosario/count-down-latch/
https://aghmnl.github.io/senior-forge-codex/es/glosario/run-test/
https://aghmnl.github.io/senior-forge-codex/es/glosario/flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/room/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collector/
https://aghmnl.github.io/senior-forge-codex/es/glosario/advance-until-idle/
https://aghmnl.github.io/senior-forge-codex/es/glosario/run-catching/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/coroutines-basics.html
https://kotlinlang.org/docs/composing-suspending-functions.html
https://kotlinlang.org/docs/exception-handling.html
https://kotlinlang.org/docs/cancellation-and-timeouts.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/launch.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/async.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-deferred/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/await-all.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-completable-deferred/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-coroutine-start/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/coroutine-scope.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/supervisor-scope.html
https://developer.android.com/kotlin/coroutines
https://developer.android.com/kotlin/coroutines/coroutines-adv
https://developer.android.com/kotlin/coroutines/coroutines-best-practices
https://developer.android.com/kotlin/coroutines/test

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Launch vs Async/Await
2. Agregá el artículo principal como fuente web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior con base intermedia.

Ya domina: intuye que la excepción de un async aflora en await(); elige launch (y no async) para N escrituras paralelas sin resultado. Tratar "launch para efectos sin valor" como repaso rápido.

Necesita explicación en profundidad: qué devuelve cada builder — launch devuelve un Job (cancel/join, sin valor) y async devuelve un Deferred<T> que extiende Job y cuyo await() suspende hasta el valor — y el criterio "¿necesito el valor?" para elegir; la forma canónica de paralelismo: suspend function con coroutineScope como cuerpo, dos async independientes y la llamada dependiente como suspend call plana; la doble vía del fallo de async (guardado en el Deferred para await() y a la vez propagado al Job padre en el momento), por qué dentro de coroutineScope el otro async se cancela antes del try/catch y por qué hace falta supervisorScope para aislar; por qué async { }.await() en una línea es una llamada normal con overhead y por qué un Deferred que nadie espera debió ser un launch; que coroutineScope ya espera a todos los launch hijos; CompletableDeferred como Deferred completado a mano (compuerta en tests, puente desde un callback de un solo disparo).

Malentendidos a corregir: cree que un try/catch alrededor de await() "silencia" el fallo del otro async — en realidad no lo alcanza: dentro de coroutineScope el hermano ya fue cancelado por la propagación al padre antes de llegar al catch; el problema no es silenciar sino que el catch no puede salvar al hermano.

Instrucción para el Audio Overview: explicá desde cero, con analogías, Job vs Deferred como "recibo sin valor" vs "promesa con valor", la forma coroutineScope + async + await para solapar llamadas independientes, y la doble vía del fallo de async con coroutineScope vs supervisorScope; tratá "launch para efectos" como repaso de una frase y dedicá tiempo a CompletableDeferred y a los dos olores (async().await() en línea y Deferred sin esperar).

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente                                  | Aporta                                                                                                                                |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Coroutines basics                       | `launch`, scope, `Job` y `join()`; la base de structured concurrency.                                                                 |
| Composing suspending functions          | El capítulo central: secuencial por defecto, `async` para concurrencia, `awaitAll`, lazy `async`, structured concurrency con `async`. |
| Exception handling                      | Por qué `launch` y `async` tratan las excepciones distinto; `supervisorScope`; el `CoroutineExceptionHandler` no aplica a `async`.    |
| Cancellation and timeouts               | Cómo `await()` participa de la cancelación.                                                                                           |
| `launch` (API)                          | Contrato exacto: devuelve `Job`, `CoroutineStart`, contexto.                                                                          |
| `async` (API)                           | Contrato exacto: devuelve `Deferred`, semántica de fallo, `start = LAZY`.                                                             |
| `Deferred` (API)                        | `await()`, `getCompleted()`, relación con `Job`.                                                                                      |
| `awaitAll` (API)                        | Espera de una lista de `Deferred` y fallo ante el primero que falla.                                                                  |
| `CompletableDeferred` (API)             | `Deferred` completado a mano: `complete()`, `completeExceptionally()`.                                                                |
| `CoroutineStart` (API)                  | `DEFAULT`, `LAZY`, `ATOMIC`, `UNDISPATCHED`.                                                                                          |
| `coroutineScope` (API)                  | El contenedor habitual de `async`: espera a los hijos, cancela hermanos ante un fallo.                                                |
| `supervisorScope` (API)                 | La variante que aísla el fallo de un `async` a su `Deferred`.                                                                         |
| Kotlin coroutines on Android            | `viewModelScope.launch` como punto de entrada desde eventos de UI.                                                                    |
| Improve app performance with coroutines | Ejemplos oficiales de `async` en paralelo dentro de `coroutineScope`.                                                                 |
| Best practices for coroutines           | No exponer `Deferred` ni scopes; encapsular el paralelismo en suspend functions.                                                      |
| Testing Kotlin coroutines on Android    | `runTest`, `advanceUntilIdle`, y cómo un fallo de `async` llega al test.                                                              |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Launch vs Async/Await", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Qué devuelve `launch` y qué devuelve `async`? ¿Qué podés hacer con cada cosa que devuelven, y cómo decidís cuál usar en un caso dado?
2. Tenés dos llamadas de red independientes y una tercera que necesita el resultado de la primera. Escribí (o describí) la forma con coroutines para que las independientes se solapen. ¿Dónde va `async` y dónde no?
3. Un bloque `async` lanza una excepción. ¿Dónde y cuándo aflora esa excepción? Si el `async` vive dentro de un `coroutineScope` junto a otro `async`, ¿qué le pasa al otro, y alcanza con un `try/catch` alrededor de `await()` para salvarlo?
4. ¿Qué hace `async { fetch() }.await()` escrito en una sola línea? ¿Y qué problema tiene un `async` cuyo `Deferred` nunca se espera?
5. Tenés N escrituras independientes a la base de datos que no devuelven nada y querés que corran en paralelo y esperar a que terminen todas. ¿Usás `launch` o `async`? ¿Qué es un `CompletableDeferred` y para qué lo usarías?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: `launch`→`Job`, `async`→`Deferred<T>` con `await()`; criterio "¿necesito el valor?". Junior: cree que `async` es más rápido o corre en otro thread.
- P2 Senior: `coroutineScope` + dos `async` independientes + la dependiente como llamada plana. Intermedio: envuelve la dependiente en `async` y la espera de inmediato.
- P3 Senior: se guarda en el `Deferred` y falla al padre en el momento; en `coroutineScope` el hermano se cancela, `supervisorScope` para aislar. Intermedio: cree que el `try/catch` en `await()` alcanza.
- P4 Senior: `async{}.await()` en línea es una llamada normal con overhead; `Deferred` sin `await` debió ser `launch`. Junior: cree que corre en paralelo con lo que sigue.
- P5 Senior: `launch` dentro de `coroutineScope`; `CompletableDeferred` como compuerta manual. Junior: `async`+`awaitAll` para escrituras sin resultado.
```
