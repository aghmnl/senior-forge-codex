---
topic: "Channel (Hot Streams)"
chapter: 02-coroutines-flow
slug: channel-hot-streams
lang: es
article: /es/02-coroutines-flow/channel-hot-streams/
diagnostic_date: 2026-10-02
---

# Notebook de estudio — Channel (Hot Streams)

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Por qué se dice que un `Channel` es un stream "hot"? Si enviás valores a un channel con buffer antes de que alguien empiece a recibir, ¿qué pasa con esos valores?
2. Creás `val channel = Channel<Int>()` sin argumentos. Una coroutine hace `channel.send(1)` y nadie está recibiendo. ¿Qué pasa? ¿Qué otras capacidades de channel conocés?
3. Varias coroutines necesitan escribir líneas en un mismo archivo, y dos escrituras nunca se pueden superponer. ¿Cómo lo resolverías con un channel?
4. ¿Cómo armarías un productor que va leyendo páginas de una API y un consumidor que las guarda en la base de datos a medida que llegan?
5. ¿Qué riesgo tiene usar `Channel(Channel.UNLIMITED)` cuando el productor es más rápido que el consumidor?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | Es **hot** porque existe independientemente de sus consumidores: no espera a que alguien lo colecte para aceptar valores, a diferencia de un `Flow` cold. Los valores enviados antes de que haya un receptor **quedan en el buffer** (hasta llenarlo) y se entregan, en orden, cuando alguien empieza a recibir. | Sabe que "guarda" los valores pero no explica qué lo hace hot. | Cree que los valores se pierden o que el channel no hace nada hasta que alguien recibe. |
| 2 | `Channel<Int>()` es **rendezvous**: sin buffer, así que `send(1)` **suspende** hasta que alguien llame a `receive`. Capacidades: `RENDEZVOUS`, `BUFFERED`, `UNLIMITED` y `CONFLATED`, que deciden cuándo suspende `send`. | Sabe que "espera" pero no conoce las capacidades. | Cree que el valor queda guardado o se pierde. |
| 3 | Un solo consumidor lee de un channel y hace las escrituras **de a una, en orden**; las coroutines que quieren escribir hacen `send` con la línea. Como el channel conserva el orden y hay un único consumidor, las escrituras nunca se superponen, **sin necesidad de un lock**. | Propone un lock o un `Mutex`, correcto pero sin ver la alternativa con channel. | No sabe cómo resolverlo. |
| 4 | Con `produce { }`: crea el channel, lanza la coroutine productora que hace `send`, devuelve el lado que recibe y lo **cierra automáticamente** al terminar o cancelarse. El consumidor recorre el resultado con `for`. El productor suspende si el consumidor va atrasado. | Arma el pipeline a mano con un `Channel` y `launch`, sin pensar en quién lo cierra. | No sabe cómo armarlo. |
| 5 | Con un productor más rápido que el consumidor, un buffer **sin límite** crece hasta agotar la memoria. Un buffer acotado hace esperar al productor (backpressure); descartar valores a propósito es `CONFLATED` o una política de descarte. | Intuye que "puede crecer mucho" pero no propone alternativa. | No ve ningún riesgo. |

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
| 1 | Junior | "No sé". No sabe qué hace hot a un channel ni que guarda en el buffer lo enviado sin receptor. |
| 2 | Junior | "No sé". No conoce el rendezvous por defecto ni las capacidades. |
| 3 | Junior | "No sé". No conoce el patrón de un único consumidor para serializar trabajo. |
| 4 | Junior | "No sé". No conoce `produce` ni el pipeline productor-consumidor. |
| 5 | Junior | "No sé". No ve el riesgo de memoria de un buffer sin límite. |

**Nivel global: Junior** (0 Senior, 0 intermedias, 5 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de estudiar SharedFlow, donde Channel apareció como contraste (cola frente a difusión), y Flow (Cold Streams); conviene presentar el Channel por comparación con esas dos piezas.

Necesita explicación en profundidad, desde cero: qué es un Channel como cola entre coroutines con send y receive que suspenden, y por qué es un hot stream que guarda en su buffer lo enviado antes de que haya receptor; que cada valor lo recibe un solo receptor, a diferencia del SharedFlow, que difunde; las capacidades RENDEZVOUS (la de por defecto, donde send suspende hasta que alguien recibe), BUFFERED, UNLIMITED y CONFLATED; cómo se cierra un channel con close, por qué un for sobre un channel sin cerrar nunca termina, y cómo produce lo crea y lo cierra solo; cómo se arma un pipeline productor-consumidor y un reparto de trabajo entre varios workers; cómo un único consumidor serializa trabajo en orden sin lock; y por qué UNLIMITED puede agotar la memoria con un productor rápido, frente a un buffer acotado que aplica backpressure.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una cinta transportadora entre un cocinero y varios mozos, donde cada plato lo lleva un solo mozo), qué es un Channel y en qué se diferencia de SharedFlow, después las capacidades y cuándo suspende send, después cerrar el channel y produce, y cerrá con los usos prácticos: pipeline, reparto de trabajo, serializar escrituras y por qué UNLIMITED es riesgoso.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Channel (Hot Streams)

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/channel-hot-streams/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/sharedflow/
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/flow-cold-streams/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/channel/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutines/
https://aghmnl.github.io/senior-forge-codex/es/glosario/send/
https://aghmnl.github.io/senior-forge-codex/es/glosario/receive/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread/
https://aghmnl.github.io/senior-forge-codex/es/glosario/hot-stream/
https://aghmnl.github.io/senior-forge-codex/es/glosario/conflation/
https://aghmnl.github.io/senior-forge-codex/es/glosario/try-send/
https://aghmnl.github.io/senior-forge-codex/es/glosario/close/
https://aghmnl.github.io/senior-forge-codex/es/glosario/produce/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collector/
https://aghmnl.github.io/senior-forge-codex/es/glosario/fan-out/
https://aghmnl.github.io/senior-forge-codex/es/glosario/backpressure/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lock/
https://aghmnl.github.io/senior-forge-codex/es/glosario/android/
https://aghmnl.github.io/senior-forge-codex/es/glosario/buffer/
https://aghmnl.github.io/senior-forge-codex/es/glosario/flow-on/
https://aghmnl.github.io/senior-forge-codex/es/glosario/callback-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cold-stream/
https://aghmnl.github.io/senior-forge-codex/es/glosario/finally/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/channels.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-channel/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/produce.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-send-channel/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-receive-channel/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-buffer-overflow/
https://developer.android.com/topic/architecture/ui-layer/events
https://developer.android.com/kotlin/flow/stateflow-and-sharedflow

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Channel (Hot Streams)
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de estudiar SharedFlow, donde Channel apareció como contraste (cola frente a difusión), y Flow (Cold Streams); conviene presentar el Channel por comparación con esas dos piezas.

Necesita explicación en profundidad, desde cero: qué es un Channel como cola entre coroutines con send y receive que suspenden, y por qué es un hot stream que guarda en su buffer lo enviado antes de que haya receptor; que cada valor lo recibe un solo receptor, a diferencia del SharedFlow, que difunde; las capacidades RENDEZVOUS (la de por defecto, donde send suspende hasta que alguien recibe), BUFFERED, UNLIMITED y CONFLATED; cómo se cierra un channel con close, por qué un for sobre un channel sin cerrar nunca termina, y cómo produce lo crea y lo cierra solo; cómo se arma un pipeline productor-consumidor y un reparto de trabajo entre varios workers; cómo un único consumidor serializa trabajo en orden sin lock; y por qué UNLIMITED puede agotar la memoria con un productor rápido, frente a un buffer acotado que aplica backpressure.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una cinta transportadora entre un cocinero y varios mozos, donde cada plato lo lleva un solo mozo), qué es un Channel y en qué se diferencia de SharedFlow, después las capacidades y cuándo suspende send, después cerrar el channel y produce, y cerrá con los usos prácticos: pipeline, reparto de trabajo, serializar escrituras y por qué UNLIMITED es riesgoso.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Channels | La guía oficial: `send` y `receive`, cerrar e iterar, `produce`, pipelines, fan-out, fan-in y capacidades del buffer. |
| `Channel` (API) | Las capacidades (`RENDEZVOUS`, `BUFFERED`, `UNLIMITED`, `CONFLATED`) y qué pasa al cerrar. |
| `produce` (API) | El builder que crea el channel, corre el productor y lo cierra automáticamente. |
| `SendChannel` (API) | El lado que envía: `send`, `trySend` y `close`. |
| `ReceiveChannel` (API) | El lado que recibe: `receive`, la iteración con `for` y `cancel`. |
| `BufferOverflow` (API) | Qué hacer cuando el buffer se llena: suspender o descartar. |
| UI events | Por qué la guía prefiere modelar los eventos de UI como estado antes que enviarlos por un channel. |
| StateFlow and SharedFlow | El contraste con los streams hot que difunden en vez de encolar. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Channel (Hot Streams)", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Por qué se dice que un `Channel` es un stream "hot"? Si enviás valores a un channel con buffer antes de que alguien empiece a recibir, ¿qué pasa con esos valores?
2. Creás `val channel = Channel<Int>()` sin argumentos. Una coroutine hace `channel.send(1)` y nadie está recibiendo. ¿Qué pasa? ¿Qué otras capacidades de channel conocés?
3. Varias coroutines necesitan escribir líneas en un mismo archivo, y dos escrituras nunca se pueden superponer. ¿Cómo lo resolverías con un channel?
4. ¿Cómo armarías un productor que va leyendo páginas de una API y un consumidor que las guarda en la base de datos a medida que llegan?
5. ¿Qué riesgo tiene usar `Channel(Channel.UNLIMITED)` cuando el productor es más rápido que el consumidor?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: es hot porque existe independientemente de sus consumidores; lo enviado antes de que haya receptor queda en el buffer y se entrega en orden. Junior: cree que se pierde.
- P2 Senior: Channel() es rendezvous: send suspende hasta que alguien recibe; capacidades RENDEZVOUS, BUFFERED, UNLIMITED y CONFLATED. Junior: cree que el valor queda guardado o se pierde.
- P3 Senior: un único consumidor lee del channel y escribe de a una línea, en orden; los demás hacen send; sin lock. Junior: no sabe resolverlo.
- P4 Senior: produce crea el channel, corre el productor y lo cierra solo; el consumidor recorre con for. Junior: no sabe armarlo.
- P5 Senior: UNLIMITED puede agotar la memoria con un productor rápido; un buffer acotado hace esperar al productor (backpressure). Junior: no ve riesgo.
```
