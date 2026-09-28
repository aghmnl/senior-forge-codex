---
topic: "shareIn & stateIn"
chapter: 02-coroutines-flow
slug: sharein-statein
lang: es
article: /es/02-coroutines-flow/sharein-statein/
diagnostic_date: 2026-09-28
---

# Notebook de estudio — shareIn & stateIn

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. Tres pantallas colectan el mismo `repository.observeTasks()`, que devuelve un `Flow` de Room. ¿Cuántas queries corren? ¿Cómo harías para que corra una sola?
2. ¿Qué diferencia hay entre `stateIn` y `shareIn`? ¿Cuándo usarías cada uno?
3. Un ViewModel expone `fun uiState() = repository.observe().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), UiState.Loading)`, y un composable llama a `viewModel.uiState()` para colectarlo. ¿Qué problema tiene?
4. El upstream de un `stateIn` en `viewModelScope` lanza una excepción. ¿Qué pasa? ¿Dónde pondrías el `catch`?
5. En un test hacés `assertEquals(expected, viewModel.uiState.value)` sobre un `StateFlow` creado con `stateIn(..., SharingStarted.WhileSubscribed(5_000), ...)`, y siempre ves el valor inicial. ¿Por qué? ¿Cómo lo arreglás?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | Como el flow de Room es **cold**, cada collector ejecuta su propia query: tres pantallas son tres queries y tres observers. Para que corra una sola, se comparte la ejecución con `shareIn` o `stateIn`, que lanzan **una** colección del upstream y difunden el resultado; `stateIn` si hay un valor actual con sentido (lo típico para estado), `shareIn` si no. | Sabe que hay trabajo duplicado pero no conoce `shareIn`/`stateIn` como solución. | Cree que corre una sola query. |
| 2 | `stateIn` devuelve un `StateFlow`: valor actual en `.value`, **valor inicial obligatorio**, conflation y filtrado por igualdad; sirve para estado. `shareIn` devuelve un `SharedFlow`: sin valor actual, con `replay` configurable, entrega valores iguales; sirve para streams sin semántica de "valor actual" o para difundir. | Sabe que uno da `StateFlow` y el otro `SharedFlow` pero no sabe cuándo elegir cada uno. | No distingue los dos. |
| 3 | Cada llamada a `stateIn` crea una **colección compartida nueva**: llamado desde un composable, se ejecuta en cada recomposición y lanza una colección nueva cada vez, así que no se comparte nada y se acumulan colecciones en `viewModelScope`. El `stateIn` va en una **propiedad** que se inicializa una sola vez. | Intuye que "se crea muchas veces" pero no explica la consecuencia. | No ve problema. |
| 4 | La excepción **no les llega a los collectors**: hace fallar a la coroutine que comparte adentro del scope, y en `viewModelScope` una excepción no atrapada crashea la app. El `catch` (mapeado a un estado de error) y el `retry` van **antes** de `stateIn`, sobre el upstream. | Sabe que hay que poner un `catch` pero lo pondría después de `stateIn` o en el collector. | No sabe qué pasa. |
| 5 | Con `WhileSubscribed`, el upstream **no se colecta hasta que alguien se suscribe**, así que sin collector `.value` queda en el valor inicial para siempre. En el test hay que colectar el estado, normalmente en `backgroundScope` dentro de `runTest`, antes de verificar. | Intuye que "el flow no arrancó" pero no conecta con `WhileSubscribed` ni sabe cómo arreglarlo en el test. | No sabe por qué. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior a Senior; 3+ intermedias o mezcla a Intermedio; 3+ junior o "no sé" a Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-09-28

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Junior | "No sé". No conecta el flow cold con una query por collector ni conoce la solución de compartir. |
| 2 | Junior | "No sé". No distingue `stateIn` de `shareIn`. |
| 3 | Junior | "No sé". No sabe que cada llamada crea una colección compartida nueva. |
| 4 | Junior | "No sé". No conoce el efecto de una excepción del upstream compartido ni dónde va el `catch`. |
| 5 | Junior | "No sé". No conecta `WhileSubscribed` con la necesidad de un suscriptor en el test. |

**Nivel global: Junior** (0 Senior, 0 intermedias, 5 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de estudiar StateFlow y SharedFlow, y en el tema de Flow (Cold Streams) vio que un flow cold ejecuta su productor una vez por cada collector; conviene apoyarse en esas tres ideas y presentar shareIn y stateIn como el puente entre cold y hot.

Necesita explicación en profundidad, desde cero: por qué tres pantallas colectando el mismo flow de Room ejecutan tres queries, y cómo stateIn y shareIn lanzan una sola colección del upstream y la comparten; la diferencia entre stateIn, que da un StateFlow con valor inicial obligatorio, y shareIn, que da un SharedFlow con replay configurable, y cuándo usar cada uno; los parámetros scope y started, y las tres estrategias Eagerly, Lazily y WhileSubscribed, con el porqué de WhileSubscribed(5_000) y su dependencia de un collector lifecycle-aware; por qué stateIn va en una propiedad creada una sola vez y nunca en una función o getter; por qué una excepción del upstream no llega a los collectors y crashea la app en viewModelScope, y por qué catch y retry van antes de stateIn; y por qué un test sobre un StateFlow con WhileSubscribed necesita colectarlo en backgroundScope.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una sola transmisión de radio para muchos oyentes en vez de un llamado telefónico por oyente), por qué compartir un flow cold, después stateIn frente a shareIn, después las estrategias de started con WhileSubscribed(5_000) como caso central, y cerrá con las tres trampas prácticas: crearlo en una función, el catch después de stateIn y el test sin suscriptor.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
shareIn & stateIn

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/sharein-statein/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/stateflow/
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/sharedflow/
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/flow-cold-streams/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/state-in/
https://aghmnl.github.io/senior-forge-codex/es/glosario/share-in/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cold-stream/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collector/
https://aghmnl.github.io/senior-forge-codex/es/glosario/hot-stream/
https://aghmnl.github.io/senior-forge-codex/es/glosario/upstream/
https://aghmnl.github.io/senior-forge-codex/es/glosario/conflation/
https://aghmnl.github.io/senior-forge-codex/es/glosario/distinct-until-changed/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sharing-started/
https://aghmnl.github.io/senior-forge-codex/es/glosario/while-subscribed/
https://aghmnl.github.io/senior-forge-codex/es/glosario/init/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutines/
https://aghmnl.github.io/senior-forge-codex/es/glosario/eager/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lifecycle-aware/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collect-as-state-with-lifecycle/
https://aghmnl.github.io/senior-forge-codex/es/glosario/repeat-on-lifecycle/
https://aghmnl.github.io/senior-forge-codex/es/glosario/catch/
https://aghmnl.github.io/senior-forge-codex/es/glosario/retry/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mutable-state-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/combine/
https://aghmnl.github.io/senior-forge-codex/es/glosario/test-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/run-test/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collect/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/state-in.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/share-in.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-sharing-started/
https://developer.android.com/kotlin/flow/stateflow-and-sharedflow
https://developer.android.com/topic/architecture/ui-layer/state-production
https://developer.android.com/topic/libraries/architecture/coroutines
https://developer.android.com/kotlin/flow/test
https://developer.android.com/kotlin/coroutines/coroutines-best-practices
https://kotlinlang.org/docs/flow.html

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: shareIn & stateIn
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de estudiar StateFlow y SharedFlow, y en el tema de Flow (Cold Streams) vio que un flow cold ejecuta su productor una vez por cada collector; conviene apoyarse en esas tres ideas y presentar shareIn y stateIn como el puente entre cold y hot.

Necesita explicación en profundidad, desde cero: por qué tres pantallas colectando el mismo flow de Room ejecutan tres queries, y cómo stateIn y shareIn lanzan una sola colección del upstream y la comparten; la diferencia entre stateIn, que da un StateFlow con valor inicial obligatorio, y shareIn, que da un SharedFlow con replay configurable, y cuándo usar cada uno; los parámetros scope y started, y las tres estrategias Eagerly, Lazily y WhileSubscribed, con el porqué de WhileSubscribed(5_000) y su dependencia de un collector lifecycle-aware; por qué stateIn va en una propiedad creada una sola vez y nunca en una función o getter; por qué una excepción del upstream no llega a los collectors y crashea la app en viewModelScope, y por qué catch y retry van antes de stateIn; y por qué un test sobre un StateFlow con WhileSubscribed necesita colectarlo en backgroundScope.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una sola transmisión de radio para muchos oyentes en vez de un llamado telefónico por oyente), por qué compartir un flow cold, después stateIn frente a shareIn, después las estrategias de started con WhileSubscribed(5_000) como caso central, y cerrá con las tres trampas prácticas: crearlo en una función, el catch después de stateIn y el test sin suscriptor.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| `stateIn` (API) | El contrato: valor inicial, la sobrecarga suspendible y la colección compartida en el scope. |
| `shareIn` (API) | El contrato: `replay`, el manejo de errores del upstream y por qué no se llama adentro de una función. |
| `SharingStarted` (API) | `Eagerly`, `Lazily` y `WhileSubscribed`, con sus parámetros de timeout y expiración del replay. |
| StateFlow and SharedFlow | La guía de Android, incluida la sección sobre convertir flows cold en hot con `stateIn` y `shareIn`. |
| State production | Cómo producir estado de UI declarándolo desde sus fuentes, y la elección del valor inicial. |
| Coroutines with lifecycle-aware components | `repeatOnLifecycle` y por qué el collector tiene que irse para que `WhileSubscribed` detenga el upstream. |
| Testing Kotlin flows | Cómo testear un `StateFlow` que necesita un suscriptor, con `backgroundScope`. |
| Best practices for coroutines | Dónde crear y exponer los flows compartidos desde la capa de datos y el ViewModel. |
| Asynchronous Flow | La base de flows cold, para entender qué se está compartiendo. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "shareIn & stateIn", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. Tres pantallas colectan el mismo `repository.observeTasks()`, que devuelve un `Flow` de Room. ¿Cuántas queries corren? ¿Cómo harías para que corra una sola?
2. ¿Qué diferencia hay entre `stateIn` y `shareIn`? ¿Cuándo usarías cada uno?
3. Un ViewModel expone `fun uiState() = repository.observe().stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), UiState.Loading)`, y un composable llama a `viewModel.uiState()` para colectarlo. ¿Qué problema tiene?
4. El upstream de un `stateIn` en `viewModelScope` lanza una excepción. ¿Qué pasa? ¿Dónde pondrías el `catch`?
5. En un test hacés `assertEquals(expected, viewModel.uiState.value)` sobre un `StateFlow` creado con `stateIn(..., SharingStarted.WhileSubscribed(5_000), ...)`, y siempre ves el valor inicial. ¿Por qué? ¿Cómo lo arreglás?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: el flow de Room es cold y cada collector ejecuta su propia query; shareIn/stateIn lanzan una sola colección y la comparten. Junior: cree que corre una sola query.
- P2 Senior: stateIn da un StateFlow (valor actual, valor inicial obligatorio, filtrado por igualdad) para estado; shareIn da un SharedFlow (sin valor actual, replay configurable) para difundir. Junior: no los distingue.
- P3 Senior: cada llamada crea una colección compartida nueva; desde un composable se crea una en cada recomposición; va en una propiedad creada una vez. Junior: no ve problema.
- P4 Senior: la excepción no llega a los collectors, hace fallar la coroutine que comparte y en viewModelScope crashea la app; catch y retry van antes de stateIn. Junior: no sabe qué pasa.
- P5 Senior: con WhileSubscribed el upstream no corre sin suscriptores; el test tiene que colectar el estado en backgroundScope dentro de runTest. Junior: no sabe por qué.
```
