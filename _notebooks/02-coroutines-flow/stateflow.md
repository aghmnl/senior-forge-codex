---
topic: "StateFlow"
chapter: 02-coroutines-flow
slug: stateflow
lang: es
article: /es/02-coroutines-flow/stateflow/
diagnostic_date: 2026-09-25
---

# Notebook de estudio — StateFlow

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. Un repositorio expone un `Flow` de Room y un ViewModel expone un `StateFlow`. Tres pantallas colectan cada uno. ¿Qué diferencia hay en lo que pasa por debajo? Y un colector que llega tarde, ¿qué recibe de cada uno?
2. Un `MutableStateFlow<Int>` recibe `1`, `2` y `3` en rápida sucesión mientras su único colector está ocupado procesando lento. ¿Qué valores ve el colector? ¿Y qué pasa si después escribís `5` dos veces seguidas?
3. El `TasksUiState` inicial tiene `tasks = emptyList()`, y en cada arranque la pantalla muestra "No tenés tareas" durante medio segundo antes de mostrar la lista. ¿Por qué pasa y cómo diseñarías el estado para evitarlo?
4. En Compose, ¿qué diferencia hay entre `collectAsState()` y `collectAsStateWithLifecycle()` al colectar un `StateFlow`? ¿Cuándo importa de verdad?
5. Un ViewModel tiene `private val _refresh = MutableStateFlow(true)` y un `combine` que recalcula la lista cada vez que `_refresh` emite. Para pedir un refresco hace `_refresh.value = true`. Funciona la primera vez y después nunca más. ¿Por qué? ¿Cómo lo arreglarías?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | El `Flow` de Room es **cold**: cada colector ejecuta su propia query y su propio observer, así que tres pantallas son tres ejecuciones independientes, y un colector que llega tarde arranca la suya desde cero. El `StateFlow` es **hot**: existe una sola vez, tiene un valor actual con o sin colectores, y los tres comparten ese mismo valor. Un colector que llega tarde recibe **el valor actual inmediatamente** y después solo los cambios, no la historia. | Sabe que uno es cold y el otro hot, pero no explica el costo duplicado del cold o no sabe qué recibe un colector tardío. | No distingue entre los dos o cree que se comportan igual. |
| 2 | `StateFlow` aplica **conflation**: el colector lento ve el último valor disponible cuando termina (probablemente `1` y después `3`, salteando `2`), nunca una cola de pendientes, y el que escribe nunca se suspende. Escribir `5` dos veces produce **una sola emisión**: la segunda escritura es `equals()` al valor actual y se descarta. Menciona que por eso sirve para estado y no para eventos. | Conoce una de las dos cosas (conflation o el filtrado por igualdad) pero no la otra. | Cree que el colector ve 1, 2, 3, 5, 5. |
| 3 | `StateFlow` exige un valor inicial, y `emptyList()` hace indistinguibles "todavía cargando" y "realmente vacío": la UI dibuja el estado vacío hasta que llega la primera emisión real. Soluciones: un flag `isLoading` que arranca en `true`, un miembro `Loading` en un estado sellado, o un valor nullable donde `null` significa "todavía desconocido". Presenta el valor inicial como una **decisión de diseño**. | Identifica que el valor inicial es el problema, pero propone un parche (un delay, esconder el mensaje) en vez de modelar el estado de carga. | No sabe por qué pasa. |
| 4 | `collectAsState()` colecta mientras el composable está en la composición, **incluso con la app en background**. `collectAsStateWithLifecycle()` frena la colección por debajo de `STARTED` y la retoma con el valor actual al volver. Para un `MutableStateFlow` simple la diferencia es menor; importa de verdad cuando el `StateFlow` está alimentado por un upstream (`stateIn` con `WhileSubscribed`, una query, la ubicación, etc.), porque solo un colector lifecycle-aware permite que ese upstream se detenga. | Sabe que uno "respeta el lifecycle", pero no explica qué pasa en background o cuándo importa. | No conoce la diferencia. |
| 5 | Como `StateFlow` filtra por igualdad, escribir `true` cuando el valor ya es `true` **no emite**: el `combine` nunca se entera. Arreglos: hacer que cada escritura sea distinta (un contador que se incrementa o un timestamp), o replantear si el trigger es realmente estado, y si es un evento de verdad usar otra primitiva (`SharedFlow` sin replay o `Channel`). | Intuye que "no cambia el valor" pero no nombra el filtrado por igualdad o no propone un arreglo. | No sabe por qué deja de funcionar. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior a Senior; 3+ intermedias o mezcla a Intermedio; 3+ junior o "no sé" a Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-09-25

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Junior | "No me acuerdo". No distingue cold de hot ni sabe qué recibe un colector tardío. |
| 2 | Junior | "No sé". No conoce la conflation ni el filtrado por igualdad. |
| 3 | Intermedia | Identifica que los datos llegan de forma asíncrona y propone un estado de loading, que es modelar la carga y no parcharla. No nombra que el problema es el valor inicial obligatorio del `StateFlow` ni que `emptyList()` confunde "cargando" con "vacío". |
| 4 | Junior | "No recuerdo". No conoce la diferencia entre `collectAsState` y `collectAsStateWithLifecycle`. |
| 5 | Junior | "No sé". No conecta el trigger con el filtrado por igualdad. |

**Nivel global: Junior** (0 Senior, 1 intermedia, 4 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: ningún punto a nivel Senior todavía. Sí tiene la intuición correcta de que los datos de una lista llegan de forma asíncrona desde una coroutine, y que la pantalla necesita un estado de carga explícito mientras tanto; eso se puede usar como punto de partida.

Necesita explicación en profundidad: la diferencia entre un Flow cold, que ejecuta su productor una vez por cada collector, y un StateFlow hot, que existe una sola vez, siempre tiene un valor y le entrega el valor actual a cualquier collector que llegue tarde; la conflation, por la que un collector lento solo ve el último valor y se saltea los intermedios, sin backpressure; el filtrado por equals(), por el que escribir un valor igual al actual no emite, y cómo eso depende de value semantics e immutability en una data class; por qué el valor inicial de un StateFlow es una decisión de diseño, ya que emptyList() confunde "cargando" con "vacío"; la diferencia entre collectAsState y collectAsStateWithLifecycle, y por qué el collector tiene que ser lifecycle-aware; y por qué un trigger con un valor fijo deja de emitir después de la primera vez.

Malentendidos a corregir: ninguno explícito. En la respuesta sobre la lista vacía, la causa no es solo que la carga sea asíncrona, sino que el StateFlow obliga a tener un valor inicial y emptyList() no distingue "todavía no hay datos" de "no hay tareas".

Instrucción para el Audio Overview: explicá desde cero, con analogías, qué significa hot frente a cold y qué recibe un collector que llega tarde, después la conflation y el filtrado por igualdad como las dos reglas que definen cuándo emite un StateFlow, con la trampa del trigger que escribe siempre el mismo valor, y por último collectAsStateWithLifecycle; tratá el estado de carga como repaso breve apoyado en lo que ya intuye.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
StateFlow

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/stateflow/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/flow-cold-streams/
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/data-classes/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/stateflow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/hot-stream/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cold-stream/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collector/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mutable-state-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread/
https://aghmnl.github.io/senior-forge-codex/es/glosario/conflation/
https://aghmnl.github.io/senior-forge-codex/es/glosario/backpressure/
https://aghmnl.github.io/senior-forge-codex/es/glosario/equals/
https://aghmnl.github.io/senior-forge-codex/es/glosario/distinct-until-changed/
https://aghmnl.github.io/senior-forge-codex/es/glosario/update/
https://aghmnl.github.io/senior-forge-codex/es/glosario/compare-and-set/
https://aghmnl.github.io/senior-forge-codex/es/glosario/state-holder/
https://aghmnl.github.io/senior-forge-codex/es/glosario/as-state-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collect/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutines/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread-safety/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatcher/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sharedflow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/state-in/
https://aghmnl.github.io/senior-forge-codex/es/glosario/copy/
https://aghmnl.github.io/senior-forge-codex/es/glosario/referential-equality/
https://aghmnl.github.io/senior-forge-codex/es/glosario/value-semantics/
https://aghmnl.github.io/senior-forge-codex/es/glosario/immutability/
https://aghmnl.github.io/senior-forge-codex/es/glosario/flat-map-latest/
https://aghmnl.github.io/senior-forge-codex/es/glosario/timestamp/
https://aghmnl.github.io/senior-forge-codex/es/glosario/empty-list/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lifecycle/
https://aghmnl.github.io/senior-forge-codex/es/glosario/jetpack-compose/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collect-as-state-with-lifecycle/
https://aghmnl.github.io/senior-forge-codex/es/glosario/upstream/
https://aghmnl.github.io/senior-forge-codex/es/glosario/while-subscribed/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lifecycle-aware/
https://aghmnl.github.io/senior-forge-codex/es/glosario/race-condition/
https://aghmnl.github.io/senior-forge-codex/es/glosario/livedata/
https://aghmnl.github.io/senior-forge-codex/es/glosario/kotlin/
https://aghmnl.github.io/senior-forge-codex/es/glosario/android/
https://aghmnl.github.io/senior-forge-codex/es/glosario/repeat-on-lifecycle/
https://aghmnl.github.io/senior-forge-codex/es/glosario/channel/

**Fuentes oficiales (agregar cada una como fuente web)**
https://developer.android.com/kotlin/flow/stateflow-and-sharedflow
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-state-flow/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-mutable-state-flow/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/as-state-flow.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/update.html
https://kotlinlang.org/docs/flow.html
https://developer.android.com/topic/architecture/ui-layer
https://developer.android.com/topic/architecture/ui-layer/state-production
https://developer.android.com/topic/architecture/ui-layer/events
https://developer.android.com/develop/ui/compose/state
https://developer.android.com/topic/libraries/architecture/coroutines

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: StateFlow
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: ningún punto a nivel Senior todavía. Sí tiene la intuición correcta de que los datos de una lista llegan de forma asíncrona desde una coroutine, y que la pantalla necesita un estado de carga explícito mientras tanto; eso se puede usar como punto de partida.

Necesita explicación en profundidad: la diferencia entre un Flow cold, que ejecuta su productor una vez por cada collector, y un StateFlow hot, que existe una sola vez, siempre tiene un valor y le entrega el valor actual a cualquier collector que llegue tarde; la conflation, por la que un collector lento solo ve el último valor y se saltea los intermedios, sin backpressure; el filtrado por equals(), por el que escribir un valor igual al actual no emite, y cómo eso depende de value semantics e immutability en una data class; por qué el valor inicial de un StateFlow es una decisión de diseño, ya que emptyList() confunde "cargando" con "vacío"; la diferencia entre collectAsState y collectAsStateWithLifecycle, y por qué el collector tiene que ser lifecycle-aware; y por qué un trigger con un valor fijo deja de emitir después de la primera vez.

Malentendidos a corregir: ninguno explícito. En la respuesta sobre la lista vacía, la causa no es solo que la carga sea asíncrona, sino que el StateFlow obliga a tener un valor inicial y emptyList() no distingue "todavía no hay datos" de "no hay tareas".

Instrucción para el Audio Overview: explicá desde cero, con analogías, qué significa hot frente a cold y qué recibe un collector que llega tarde, después la conflation y el filtrado por igualdad como las dos reglas que definen cuándo emite un StateFlow, con la trampa del trigger que escribe siempre el mismo valor, y por último collectAsStateWithLifecycle; tratá el estado de carga como repaso breve apoyado en lo que ya intuye.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| StateFlow and SharedFlow | La guía de Android: el patrón `_uiState`/`uiState`, la diferencia con LiveData y por qué colectar con `repeatOnLifecycle`. |
| `StateFlow` (API) | El contrato exacto: siempre tiene valor, conflation, filtrado por `equals()`, `collect` nunca termina y thread-safety. |
| `MutableStateFlow` (API) | La mitad escribible: `value`, `compareAndSet` y la relación con `SharedFlow`. |
| `asStateFlow` (API) | Cómo exponer una vista de solo lectura sin que la UI pueda castear de vuelta al tipo mutable. |
| `update` (API) | Por qué `value = value.copy(...)` no es atómico y cómo `update {}` resuelve el leer-modificar-escribir. |
| Asynchronous Flow | La base de flows cold, para contrastar con el comportamiento hot de `StateFlow`. |
| UI layer | Cómo se modela el estado de UI y por qué se expone como un stream observable e inmutable. |
| State production | Cómo producir estado a partir de fuentes cold y hot, y la elección del valor inicial. |
| UI events | Por qué los eventos de una sola vez se modelan como estado que la UI confirma. |
| State and Jetpack Compose | Cómo Compose lee estado y cuándo recompone. |
| Coroutines with lifecycle-aware components | `repeatOnLifecycle` y la colección que respeta el lifecycle, la base de `collectAsStateWithLifecycle`. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "StateFlow", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. Un repositorio expone un `Flow` de Room y un ViewModel expone un `StateFlow`. Tres pantallas colectan cada uno. ¿Qué diferencia hay en lo que pasa por debajo? Y un colector que llega tarde, ¿qué recibe de cada uno?
2. Un `MutableStateFlow<Int>` recibe `1`, `2` y `3` en rápida sucesión mientras su único colector está ocupado procesando lento. ¿Qué valores ve el colector? ¿Y qué pasa si después escribís `5` dos veces seguidas?
3. El `TasksUiState` inicial tiene `tasks = emptyList()`, y en cada arranque la pantalla muestra "No tenés tareas" durante medio segundo antes de mostrar la lista. ¿Por qué pasa y cómo diseñarías el estado para evitarlo?
4. En Compose, ¿qué diferencia hay entre `collectAsState()` y `collectAsStateWithLifecycle()` al colectar un `StateFlow`? ¿Cuándo importa de verdad?
5. Un ViewModel tiene `private val _refresh = MutableStateFlow(true)` y un `combine` que recalcula la lista cada vez que `_refresh` emite. Para pedir un refresco hace `_refresh.value = true`. Funciona la primera vez y después nunca más. ¿Por qué? ¿Cómo lo arreglarías?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: el Flow de Room es cold y cada colector ejecuta su propia query; el StateFlow es hot, existe una vez y un colector tardío recibe el valor actual inmediatamente. Junior: no distingue los dos.
- P2 Senior: conflation (el colector lento ve el último valor, se saltea los intermedios) y filtrado por igualdad (escribir 5 dos veces emite una sola vez). Junior: cree que ve 1, 2, 3, 5, 5.
- P3 Senior: el valor inicial emptyList() confunde "cargando" con "vacío"; se modela con isLoading, un miembro Loading sellado o null como "desconocido". Intermedio: parchea en vez de modelar la carga.
- P4 Senior: collectAsState sigue colectando en background; collectAsStateWithLifecycle frena por debajo de STARTED; importa cuando el StateFlow tiene un upstream (stateIn con WhileSubscribed). Junior: no conoce la diferencia.
- P5 Senior: escribir true sobre true no emite por el filtrado por igualdad; se arregla con contador/timestamp o replanteando si es un evento (SharedFlow/Channel). Junior: no sabe por qué.
```
