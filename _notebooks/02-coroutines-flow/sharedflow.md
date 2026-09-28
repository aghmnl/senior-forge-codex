---
topic: "SharedFlow"
chapter: 02-coroutines-flow
slug: sharedflow
lang: es
article: /es/02-coroutines-flow/sharedflow/
diagnostic_date: 2026-09-28
---

# Notebook de estudio — SharedFlow

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Un `SharedFlow` tiene `.value` como un `StateFlow`? ¿Qué recibe un suscriptor que llega tarde si el flow se creó con `replay = 0`? ¿Y con `replay = 3`?
2. Tenés `val numbers = MutableSharedFlow<Int>()`. Llamás a `numbers.emit(1)` sin nadie suscripto, y después alguien empieza a colectar. ¿Qué recibe? Y si con el colector ya activo emitís `2` dos veces seguidas, ¿cuántas veces lo recibe?
3. Desde un callback que no puede suspender llamás a `tryEmit` sobre un `MutableSharedFlow<Event>()` que tiene un colector activo, y devuelve `false`. ¿Por qué? ¿Cómo configurarías el flow para que funcione?
4. Un `MutableSharedFlow` con la configuración por defecto tiene dos colectores, y uno de ellos tarda dos segundos en procesar cada valor. ¿Qué le pasa al que emite y al colector rápido? ¿Qué opciones tenés si el emisor nunca debería esperar?
5. Con dos colectores activos, ¿qué diferencia hay entre enviar un valor por un `SharedFlow` y enviarlo por un `Channel`? ¿Cuándo usarías cada uno?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | No: un `SharedFlow` **no tiene valor actual ni valor inicial**. Con `replay = 0` un suscriptor tardío no recibe nada del pasado, solo lo que se emita después de suscribirse. Con `replay = 3` recibe inmediatamente los últimos tres valores emitidos (el replay cache) y después los nuevos. Menciona que `StateFlow` es un `SharedFlow` con `replay = 1` más valor inicial y filtrado por igualdad. | Sabe que no tiene `.value` pero no explica bien el replay, o al revés. | Cree que se comporta igual que un `StateFlow`. |
| 2 | El `1` **se pierde**: sin suscriptores y sin replay, la emisión no va a ningún lado, sin error. El colector que llega después no recibe nada hasta la próxima emisión. El `2` emitido dos veces llega **dos veces**, porque `SharedFlow` no filtra por igualdad (a diferencia de `StateFlow`). | Acierta una de las dos mitades. | Cree que recibe el `1` o que el `2` llega una sola vez. |
| 3 | La configuración por defecto es un **rendezvous**: `replay = 0` y `extraBufferCapacity = 0`, así que no hay lugar donde dejar el valor sin suspender, y con un suscriptor presente `tryEmit` falla. Arreglo: `extraBufferCapacity` mayor que cero (y opcionalmente `onBufferOverflow = DROP_OLDEST` para que nunca falle), o emitir con `emit` desde una coroutine. | Intuye que "falta un buffer" pero no sabe qué parámetro configurar. | No sabe por qué falla. |
| 4 | Con `SUSPEND` el buffer se dimensiona según el **colector más lento**: cuando se atrasa y el buffer se llena, `emit` suspende y el colector rápido también espera, porque recibe al ritmo del emisor. Opciones: agregar buffer (`extraBufferCapacity`) para absorber picos, o una política de descarte (`DROP_OLDEST` / `DROP_LATEST`) que cambia completitud por fluidez, como decisión deliberada. | Sabe que el lento "frena" pero no conecta con las políticas de overflow. | Cree que cada colector va a su propio ritmo sin afectar al resto. |
| 5 | `SharedFlow` **difunde**: cada colector recibe cada valor. `Channel` **encola**: cada valor lo recibe un solo colector. `SharedFlow` para señales que varios consumidores tienen que ver (sesión expirada, invalidación de cachés, compartir un upstream con `shareIn`); `Channel` para trabajo o eventos que se procesan exactamente una vez, y además un `Channel` con buffer guarda los valores enviados mientras no hay colector. | Conoce la diferencia difusión/cola pero no sabe cuándo aplicar cada una. | No distingue entre los dos. |

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
| 1 | Junior | "No sé". No conoce la ausencia de valor actual ni la semántica de `replay`. |
| 2 | Junior | "No sé". No sabe que una emisión sin suscriptores se pierde ni que `SharedFlow` no filtra por igualdad. |
| 3 | Junior | "No sé". No conoce la configuración rendezvous por defecto ni `extraBufferCapacity`. |
| 4 | Junior | "No sé". No conoce el efecto del colector más lento ni las políticas de `BufferOverflow`. |
| 5 | Junior | "No sé". No distingue difusión (`SharedFlow`) de cola (`Channel`). |

**Nivel global: Junior** (0 Senior, 0 intermedias, 5 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: ningún punto de este tema todavía; el tema es nuevo. Acaba de ver StateFlow (valor actual, conflation, filtrado por equals y la idea de que StateFlow es para estado y no para eventos), así que conviene usarlo como punto de partida y explicar SharedFlow por contraste con él. Durante la lectura preguntó qué diferencia hay entre las coroutines y kotlinx.coroutines, así que vale una frase que recuerde que SharedFlow es una clase de la librería, no del lenguaje.

Necesita explicación en profundidad, desde cero: qué es un SharedFlow como hot stream que difunde cada emisión a todos los collectors, y que no tiene valor actual, ni valor inicial, ni filtrado por igualdad; los tres parámetros de MutableSharedFlow (replay, extraBufferCapacity y onBufferOverflow) y qué recibe un suscriptor tardío con replay 0 frente a replay 3; por qué una emisión sin suscriptores se pierde en silencio cuando replay es 0; por qué la configuración por defecto es un rendezvous sin buffer, de modo que emit suspende y tryEmit devuelve false cuando hay un collector; cómo el collector más lento marca el ritmo con BufferOverflow.SUSPEND y qué cambian DROP_OLDEST y DROP_LATEST; que StateFlow es un SharedFlow con replay 1, DROP_OLDEST, valor inicial y distinctUntilChanged; y la diferencia entre SharedFlow, que difunde, y Channel, que encola y entrega cada valor a un solo collector.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una radio que transmite frente a una fila de atención), qué es un SharedFlow comparándolo con el StateFlow que ya vio, después replay y la pérdida de emisiones sin suscriptores, después el buffer, tryEmit y el collector lento, y cerrá con cuándo usar SharedFlow, cuándo Channel y por qué los eventos de UI conviene modelarlos como estado.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
SharedFlow

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/sharedflow/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/stateflow/
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/flow-cold-streams/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/sharedflow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/hot-stream/
https://aghmnl.github.io/senior-forge-codex/es/glosario/kotlinx-coroutines/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collector/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cold-stream/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mutable-shared-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/as-shared-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/emit/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspend-functions/
https://aghmnl.github.io/senior-forge-codex/es/glosario/try-emit/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collect/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutines/
https://aghmnl.github.io/senior-forge-codex/es/glosario/distinct-until-changed/
https://aghmnl.github.io/senior-forge-codex/es/glosario/repeat-on-lifecycle/
https://aghmnl.github.io/senior-forge-codex/es/glosario/reset-replay-cache/
https://aghmnl.github.io/senior-forge-codex/es/glosario/singleton/
https://aghmnl.github.io/senior-forge-codex/es/glosario/upstream/
https://aghmnl.github.io/senior-forge-codex/es/glosario/share-in/
https://aghmnl.github.io/senior-forge-codex/es/glosario/channel/
https://aghmnl.github.io/senior-forge-codex/es/glosario/android/
https://aghmnl.github.io/senior-forge-codex/es/glosario/state-holder/
https://aghmnl.github.io/senior-forge-codex/es/glosario/receive-as-flow/

**Fuentes oficiales (agregar cada una como fuente web)**
https://developer.android.com/kotlin/flow/stateflow-and-sharedflow
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-shared-flow/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-mutable-shared-flow/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-mutable-shared-flow.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-buffer-overflow/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/as-shared-flow.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/share-in.html
https://kotlinlang.org/docs/flow.html
https://kotlinlang.org/docs/channels.html
https://developer.android.com/topic/architecture/ui-layer/events
https://developer.android.com/topic/libraries/architecture/coroutines

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: SharedFlow
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: ningún punto de este tema todavía; el tema es nuevo. Acaba de ver StateFlow (valor actual, conflation, filtrado por equals y la idea de que StateFlow es para estado y no para eventos), así que conviene usarlo como punto de partida y explicar SharedFlow por contraste con él. Durante la lectura preguntó qué diferencia hay entre las coroutines y kotlinx.coroutines, así que vale una frase que recuerde que SharedFlow es una clase de la librería, no del lenguaje.

Necesita explicación en profundidad, desde cero: qué es un SharedFlow como hot stream que difunde cada emisión a todos los collectors, y que no tiene valor actual, ni valor inicial, ni filtrado por igualdad; los tres parámetros de MutableSharedFlow (replay, extraBufferCapacity y onBufferOverflow) y qué recibe un suscriptor tardío con replay 0 frente a replay 3; por qué una emisión sin suscriptores se pierde en silencio cuando replay es 0; por qué la configuración por defecto es un rendezvous sin buffer, de modo que emit suspende y tryEmit devuelve false cuando hay un collector; cómo el collector más lento marca el ritmo con BufferOverflow.SUSPEND y qué cambian DROP_OLDEST y DROP_LATEST; que StateFlow es un SharedFlow con replay 1, DROP_OLDEST, valor inicial y distinctUntilChanged; y la diferencia entre SharedFlow, que difunde, y Channel, que encola y entrega cada valor a un solo collector.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una radio que transmite frente a una fila de atención), qué es un SharedFlow comparándolo con el StateFlow que ya vio, después replay y la pérdida de emisiones sin suscriptores, después el buffer, tryEmit y el collector lento, y cerrá con cuándo usar SharedFlow, cuándo Channel y por qué los eventos de UI conviene modelarlos como estado.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| StateFlow and SharedFlow | La guía de Android: cuándo usar cada uno y cómo exponerlos desde un ViewModel. |
| `SharedFlow` (API) | El contrato: difusión, replay cache, `collect` que nunca termina, y la relación con `StateFlow`. |
| `MutableSharedFlow` (API) | La mitad escribible: `emit`, `tryEmit`, `subscriptionCount` y `resetReplayCache`. |
| `MutableSharedFlow()` (función) | Los parámetros `replay`, `extraBufferCapacity` y `onBufferOverflow`, con sus valores por defecto. |
| `BufferOverflow` (API) | Las tres políticas: `SUSPEND`, `DROP_OLDEST` y `DROP_LATEST`. |
| `asSharedFlow` (API) | Cómo exponer una vista de solo lectura. |
| `shareIn` (API) | Cómo convertir un flow cold en un `SharedFlow` que comparte una sola colección del upstream. |
| Asynchronous Flow | La base de flows cold, para contrastar con el comportamiento hot. |
| Channels | La primitiva que encola en vez de difundir, para el contraste con `SharedFlow`. |
| UI events | Por qué la guía recomienda modelar los eventos de UI como estado en vez de emitirlos por un flow. |
| Coroutines with lifecycle-aware components | `repeatOnLifecycle` y por qué la pantalla tiene cero suscriptores mientras está en background. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "SharedFlow", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Un `SharedFlow` tiene `.value` como un `StateFlow`? ¿Qué recibe un suscriptor que llega tarde si el flow se creó con `replay = 0`? ¿Y con `replay = 3`?
2. Tenés `val numbers = MutableSharedFlow<Int>()`. Llamás a `numbers.emit(1)` sin nadie suscripto, y después alguien empieza a colectar. ¿Qué recibe? Y si con el colector ya activo emitís `2` dos veces seguidas, ¿cuántas veces lo recibe?
3. Desde un callback que no puede suspender llamás a `tryEmit` sobre un `MutableSharedFlow<Event>()` que tiene un colector activo, y devuelve `false`. ¿Por qué? ¿Cómo configurarías el flow para que funcione?
4. Un `MutableSharedFlow` con la configuración por defecto tiene dos colectores, y uno de ellos tarda dos segundos en procesar cada valor. ¿Qué le pasa al que emite y al colector rápido? ¿Qué opciones tenés si el emisor nunca debería esperar?
5. Con dos colectores activos, ¿qué diferencia hay entre enviar un valor por un `SharedFlow` y enviarlo por un `Channel`? ¿Cuándo usarías cada uno?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: SharedFlow no tiene valor actual ni inicial; con replay = 0 el suscriptor tardío no recibe nada del pasado; con replay = 3 recibe los últimos tres; StateFlow es un SharedFlow con replay = 1, valor inicial y filtrado por igualdad. Junior: cree que se comporta igual que StateFlow.
- P2 Senior: el 1 se pierde porque no había suscriptores ni replay; el 2 llega dos veces porque SharedFlow no filtra por igualdad. Junior: cree que recibe el 1 o que el 2 llega una vez.
- P3 Senior: la configuración por defecto es un rendezvous sin buffer, así que tryEmit falla con suscriptores presentes; se arregla con extraBufferCapacity (y opcionalmente DROP_OLDEST) o usando emit. Junior: no sabe por qué.
- P4 Senior: con SUSPEND el colector más lento marca el ritmo: emit suspende y el rápido espera; opciones: más buffer o una política de descarte como decisión deliberada. Junior: cree que cada colector va a su ritmo.
- P5 Senior: SharedFlow difunde (cada colector recibe todo), Channel encola (cada valor a un solo colector); SharedFlow para señales de difusión, Channel para eventos o trabajo que se procesan una sola vez. Junior: no los distingue.
```
