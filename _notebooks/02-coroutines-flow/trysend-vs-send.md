---
topic: "trySend() vs send()"
chapter: 02-coroutines-flow
slug: trysend-vs-send
lang: es
article: /es/02-coroutines-flow/trysend-vs-send/
diagnostic_date: 2026-10-02
---

# Notebook de estudio — trySend() vs send()

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Por qué no podés llamar a `channel.send(x)` directamente adentro de un `OnClickListener`? ¿Qué usarías en su lugar?
2. ¿Qué devuelve `trySend`? ¿Qué casos distintos te puede informar ese resultado?
3. Un channel creado con `Channel(capacity = 10)` ya tiene 10 valores sin leer. ¿Qué pasa si llamás a `send`? ¿Y si llamás a `trySend`?
4. El channel ya se cerró. ¿Qué pasa si llamás a `send`? ¿Y a `trySend`?
5. ¿Qué es `trySendBlocking` y por qué nunca lo llamarías desde el main thread?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | `send` es una **suspend function** y un listener no es una coroutine, así que no compila. Desde código que no puede suspender se usa **`trySend`**, que no espera: agrega el valor si hay lugar y si no, desiste. (Alternativa: lanzar una coroutine para hacer `send`, aceptando que el orden y el ciclo de vida pasan a depender de ese scope.) | Sabe que hay que usar `trySend` pero no explica por qué `send` no se puede llamar ahí. | No sabe la diferencia. |
| 2 | Devuelve un **`ChannelResult`**: `isSuccess` si el valor se agregó, `isFailure` si no se pudo (por ejemplo, buffer lleno o nadie recibiendo en un rendezvous) e `isClosed` si falló porque el channel está cerrado. No lanza excepciones, así que **ignorarlo pierde valores en silencio**. | Sabe que "devuelve si funcionó" pero no conoce el caso cerrado o no ve el riesgo de ignorarlo. | No sabe qué devuelve. |
| 3 | `send` **suspende** hasta que un receptor saque un valor y haga lugar; no pierde nada. `trySend` **falla de inmediato** y devuelve un resultado de falla; el valor no se agrega. | Acierta una de las dos. | Cree que se comportan igual. |
| 4 | `send` **lanza una excepción** (`ClosedSendChannelException`). `trySend` **no lanza**: devuelve un resultado con `isClosed`. | Acierta una de las dos. | No sabe qué pasa. |
| 5 | `trySendBlocking` **bloquea el thread** hasta que haya lugar. Sirve para un thread de background que no es una coroutine y tiene que respetar el backpressure. En el main thread congela la UI y puede producir un **ANR**. | Sabe que bloquea pero no conecta con el ANR o con para qué sirve. | No lo conoce. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior a Senior; 3+ intermedias o mezcla a Intermedio; 3+ junior o "no sé" a Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-10-02

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Junior | "No sé". No relaciona `send` con suspend functions ni conoce `trySend` como alternativa. |
| 2 | Junior | "No sé". No conoce `ChannelResult` ni sus casos. |
| 3 | Junior | "No sé". No distingue el comportamiento de `send` y `trySend` con el buffer lleno. |
| 4 | Junior | "No sé". No sabe qué pasa con cada uno sobre un channel cerrado. |
| 5 | Junior | "No sé". No conoce `trySendBlocking` ni el riesgo de ANR. |

**Nivel global: Junior** (0 Senior, 0 intermedias, 5 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de estudiar Channel (Hot Streams), donde vio que send suspende cuando no hay lugar y las capacidades del channel; conviene presentar trySend como la contraparte de send para el código que no puede suspender.

Necesita explicación en profundidad, desde cero: por qué send es una suspend function que espera lugar y nunca pierde valores, y por eso no se puede llamar desde un listener o un callback; qué hace trySend, que nunca espera y agrega el valor solo si hay lugar en ese momento; qué devuelve trySend (un ChannelResult con isSuccess, isFailure e isClosed) y por qué ignorarlo pierde valores en silencio; qué hacen send y trySend con el buffer lleno y con el channel cerrado (send suspende o lanza una excepción; trySend falla o devuelve isClosed, sin lanzar); cómo la capacidad del channel decide si trySend puede fallar, con CONFLATED como forma deliberada de quedarse con el último valor; y qué es trySendBlocking, que bloquea el thread y en el main thread provoca un ANR.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (dejar un paquete en un casillero: esperar a que se libere uno frente a irse si están todos ocupados), la diferencia entre send y trySend, después qué devuelve trySend y por qué hay que revisarlo, después el comportamiento con el buffer lleno y con el channel cerrado, y cerrá con trySendBlocking y el riesgo de ANR.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
trySend() vs send()

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/trysend-vs-send/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/channel-hot-streams/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/try-send/
https://aghmnl.github.io/senior-forge-codex/es/glosario/send/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspend-functions/
https://aghmnl.github.io/senior-forge-codex/es/glosario/channel-capacity/
https://aghmnl.github.io/senior-forge-codex/es/glosario/receive/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutines/
https://aghmnl.github.io/senior-forge-codex/es/glosario/channel-result/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread/
https://aghmnl.github.io/senior-forge-codex/es/glosario/try-send-blocking/
https://aghmnl.github.io/senior-forge-codex/es/glosario/main-thread/
https://aghmnl.github.io/senior-forge-codex/es/glosario/offer/
https://aghmnl.github.io/senior-forge-codex/es/glosario/backpressure/
https://aghmnl.github.io/senior-forge-codex/es/glosario/producer-consumer/
https://aghmnl.github.io/senior-forge-codex/es/glosario/listener/
https://aghmnl.github.io/senior-forge-codex/es/glosario/callbacks/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sdk/
https://aghmnl.github.io/senior-forge-codex/es/glosario/anr/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mutable-state-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/callback-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/await-close/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-send-channel/send.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-send-channel/try-send.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-channel-result/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/try-send-blocking.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-channel/
https://kotlinlang.org/docs/channels.html
https://developer.android.com/kotlin/flow
https://developer.android.com/topic/performance/vitals/anr

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: trySend() vs send()
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de estudiar Channel (Hot Streams), donde vio que send suspende cuando no hay lugar y las capacidades del channel; conviene presentar trySend como la contraparte de send para el código que no puede suspender.

Necesita explicación en profundidad, desde cero: por qué send es una suspend function que espera lugar y nunca pierde valores, y por eso no se puede llamar desde un listener o un callback; qué hace trySend, que nunca espera y agrega el valor solo si hay lugar en ese momento; qué devuelve trySend (un ChannelResult con isSuccess, isFailure e isClosed) y por qué ignorarlo pierde valores en silencio; qué hacen send y trySend con el buffer lleno y con el channel cerrado (send suspende o lanza una excepción; trySend falla o devuelve isClosed, sin lanzar); cómo la capacidad del channel decide si trySend puede fallar, con CONFLATED como forma deliberada de quedarse con el último valor; y qué es trySendBlocking, que bloquea el thread y en el main thread provoca un ANR.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (dejar un paquete en un casillero: esperar a que se libere uno frente a irse si están todos ocupados), la diferencia entre send y trySend, después qué devuelve trySend y por qué hay que revisarlo, después el comportamiento con el buffer lleno y con el channel cerrado, y cerrá con trySendBlocking y el riesgo de ANR.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| `send` (API) | El contrato: suspende cuando no hay lugar y lanza una excepción sobre un channel cerrado. |
| `trySend` (API) | El contrato: no suspende, agrega el valor solo si hay lugar y devuelve un `ChannelResult`. |
| `ChannelResult` (API) | `isSuccess`, `isFailure`, `isClosed` y los helpers para manejar cada caso. |
| `trySendBlocking` (API) | La variante que bloquea el thread, para productores que no son coroutines. |
| `Channel` (API) | Las capacidades, que deciden cuándo `send` suspende y cuándo `trySend` falla. |
| Channels | La guía oficial de channels, para el contexto de `send` y `receive`. |
| Kotlin flows on Android | Cómo se convierten APIs basadas en callbacks en flows, donde se usa `trySend`. |
| ANRs | Por qué bloquear el main thread (por ejemplo con `trySendBlocking`) termina en un ANR. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "trySend() vs send()", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Por qué no podés llamar a `channel.send(x)` directamente adentro de un `OnClickListener`? ¿Qué usarías en su lugar?
2. ¿Qué devuelve `trySend`? ¿Qué casos distintos te puede informar ese resultado?
3. Un channel creado con `Channel(capacity = 10)` ya tiene 10 valores sin leer. ¿Qué pasa si llamás a `send`? ¿Y si llamás a `trySend`?
4. El channel ya se cerró. ¿Qué pasa si llamás a `send`? ¿Y a `trySend`?
5. ¿Qué es `trySendBlocking` y por qué nunca lo llamarías desde el main thread?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: send es suspend y un listener no es coroutine; se usa trySend, que no espera. Junior: no sabe la diferencia.
- P2 Senior: devuelve un ChannelResult con isSuccess, isFailure e isClosed; no lanza, así que ignorarlo pierde valores en silencio. Junior: no sabe qué devuelve.
- P3 Senior: con el buffer lleno, send suspende hasta que haya lugar y trySend falla de inmediato. Junior: cree que son iguales.
- P4 Senior: con el channel cerrado, send lanza una excepción y trySend devuelve un resultado isClosed. Junior: no sabe.
- P5 Senior: trySendBlocking bloquea el thread; sirve fuera de coroutines en background; en el main thread provoca un ANR. Junior: no lo conoce.
```
