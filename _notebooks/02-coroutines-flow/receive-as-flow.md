---
topic: "receiveAsFlow()"
chapter: 02-coroutines-flow
slug: receive-as-flow
lang: es
article: /es/02-coroutines-flow/receive-as-flow/
diagnostic_date: 2026-10-09
---

# Notebook de estudio — receiveAsFlow()

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. Exponés un `Channel` como `Flow` con `receiveAsFlow()`, y dos collectors lo colectan al mismo tiempo. Se envían 4 valores. ¿Qué recibe cada collector?
2. Un ViewModel envía un evento a un `Channel` con buffer, expuesto con `receiveAsFlow()`, justo cuando la pantalla está en background y su collector está cancelado por `repeatOnLifecycle`. ¿Qué pasa con ese evento cuando la pantalla vuelve?
3. ¿Qué le pasa al channel cuando se cancela un collector de `receiveAsFlow()`? ¿Y qué le pasa a ese collector si el channel se cierra mientras está colectando?
4. Tenés un `Flow` obtenido con `consumeAsFlow()`. Lo colectás una vez hasta que termina, y después intentás colectarlo de nuevo. ¿Qué pasa?
5. `receiveAsFlow()` entrega cada evento una sola vez. Aun así, ¿por qué un evento se puede perder sin que se haya llegado a procesar? ¿En qué situación pasa?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | Los valores **se reparten** (fan-out): cada valor va a **un solo** collector, el que esté libre; entre los dos suman 4, no reciben 4 cada uno. Si los dos tienen que ver todo, la herramienta es un `SharedFlow`. | Sabe que no reciben todo pero no lo nombra como fan-out o no sabe la alternativa. | Cree que cada collector recibe los 4 valores. |
| 2 | El evento **espera en el buffer** del channel y, cuando la pantalla vuelve a colectar, se le **entrega una vez**. (Contraste: un `SharedFlow` con `replay = 0` lo habría perdido.) | Sabe que no se pierde pero no explica el buffer o el contraste con `SharedFlow`. | Cree que se pierde o que se entrega varias veces. |
| 3 | Cancelar el collector **no cierra el channel**: sigue abierto y otro collector puede continuar. Si el channel se cierra con `close()`, la colección **se completa normalmente**; si se cierra con una excepción, `collect` **lanza esa excepción**. | Acierta una de las dos partes. | No sabe ninguna. |
| 4 | `consumeAsFlow` se puede colectar **una sola vez**: la segunda colección lanza una **`IllegalStateException`**. Además, al terminar la primera colección **cancela el channel**. | Sabe que falla pero no que cancela el channel, o al revés. | Cree que se puede colectar de nuevo sin problema. |
| 5 | El channel entrega el evento cuando el collector lo **recibe**, no cuando termina de procesarlo. Si el collector se **cancela entre medio** (por ejemplo, en un cambio de configuración), el evento ya salió del channel y se pierde. `Dispatchers.Main.immediate` achica la ventana; modelarlo como **estado de UI** lo evita. | Intuye que la cancelación influye pero no explica recibido vs procesado. | No ve cómo se podría perder. |

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
| 1 | Junior | "No sé". No conoce el reparto de valores (fan-out) entre collectors. |
| 2 | Junior | "No sé". No sabe que el buffer del channel guarda el evento hasta la próxima colección. |
| 3 | Junior | "No sé". No conoce qué pasa al cancelar el collector ni al cerrar el channel. |
| 4 | Junior | "No sé". No conoce `consumeAsFlow` ni su restricción de una sola colección. |
| 5 | Junior | "No sé". No distingue entre evento recibido y evento procesado. |

**Nivel global: Junior** (0 Senior, 0 intermedias, 5 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de estudiar Channel (Hot Streams) y trySend() vs send(), donde vio cómo se envían y reciben valores en un channel y qué es el buffer; conviene presentar receiveAsFlow como la forma de exponer ese channel a la UI como un Flow.

Necesita explicación en profundidad, desde cero: qué hace receiveAsFlow (cada colección corre un loop de receive sobre el channel) y por qué el resultado parece un Flow pero se comporta como un channel hot; el fan-out, por el que dos collectors se reparten los valores en lugar de recibirlos todos; por qué un evento enviado con la pantalla en background espera en el buffer y se entrega una vez al volver, a diferencia de un SharedFlow sin replay; qué pasa al cancelar un collector (el channel sigue abierto) y al cerrar el channel (la colección termina o lanza la excepción); qué es consumeAsFlow, que se colecta una sola vez y cancela el channel al terminar; y por qué un evento recibido se puede perder si el collector se cancela antes de procesarlo, y por qué eso lleva a preferir el estado de UI.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una fila de pedidos en una cocina: cada pedido lo toma un solo cocinero, y si el cocinero se va con el pedido en la mano, el pedido se pierde), qué hace receiveAsFlow y el fan-out, después el patrón de eventos one-shot del ViewModel frente a SharedFlow, después la diferencia con consumeAsFlow, y cerrá con el riesgo de perder un evento recibido y la alternativa del estado de UI.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
receiveAsFlow()

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/receive-as-flow/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/channel-hot-streams/
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/sharedflow/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/receive-channel/
https://aghmnl.github.io/senior-forge-codex/es/glosario/flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collect/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collector/
https://aghmnl.github.io/senior-forge-codex/es/glosario/receive/
https://aghmnl.github.io/senior-forge-codex/es/glosario/channel/
https://aghmnl.github.io/senior-forge-codex/es/glosario/fan-out/
https://aghmnl.github.io/senior-forge-codex/es/glosario/close/
https://aghmnl.github.io/senior-forge-codex/es/glosario/illegal-state-exception/
https://aghmnl.github.io/senior-forge-codex/es/glosario/consume-as-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/receive-as-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/one-shot-event/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel/
https://aghmnl.github.io/senior-forge-codex/es/glosario/send/
https://aghmnl.github.io/senior-forge-codex/es/glosario/produce/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mutable-state-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sharedflow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/repeat-on-lifecycle/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatchers-main-immediate/
https://aghmnl.github.io/senior-forge-codex/es/glosario/producer-consumer/
https://aghmnl.github.io/senior-forge-codex/es/glosario/map-operator/
https://aghmnl.github.io/senior-forge-codex/es/glosario/filter/
https://aghmnl.github.io/senior-forge-codex/es/glosario/debounce/
https://aghmnl.github.io/senior-forge-codex/es/glosario/catch/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/receive-as-flow.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/consume-as-flow.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/produce-in.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.channels/-receive-channel/
https://kotlinlang.org/docs/channels.html
https://developer.android.com/topic/architecture/ui-layer/events
https://developer.android.com/topic/libraries/architecture/coroutines

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: receiveAsFlow()
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de estudiar Channel (Hot Streams) y trySend() vs send(), donde vio cómo se envían y reciben valores en un channel y qué es el buffer; conviene presentar receiveAsFlow como la forma de exponer ese channel a la UI como un Flow.

Necesita explicación en profundidad, desde cero: qué hace receiveAsFlow (cada colección corre un loop de receive sobre el channel) y por qué el resultado parece un Flow pero se comporta como un channel hot; el fan-out, por el que dos collectors se reparten los valores en lugar de recibirlos todos; por qué un evento enviado con la pantalla en background espera en el buffer y se entrega una vez al volver, a diferencia de un SharedFlow sin replay; qué pasa al cancelar un collector (el channel sigue abierto) y al cerrar el channel (la colección termina o lanza la excepción); qué es consumeAsFlow, que se colecta una sola vez y cancela el channel al terminar; y por qué un evento recibido se puede perder si el collector se cancela antes de procesarlo, y por qué eso lleva a preferir el estado de UI.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una fila de pedidos en una cocina: cada pedido lo toma un solo cocinero, y si el cocinero se va con el pedido en la mano, el pedido se pierde), qué hace receiveAsFlow y el fan-out, después el patrón de eventos one-shot del ViewModel frente a SharedFlow, después la diferencia con consumeAsFlow, y cerrá con el riesgo de perder un evento recibido y la alternativa del estado de UI.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| `receiveAsFlow` (API) | El contrato: cada colección hace `receive` sobre el channel, se puede colectar varias veces y los valores se reparten (fan-out). |
| `consumeAsFlow` (API) | El contrato: una sola colección, y el channel se cancela cuando esa colección termina. |
| `produceIn` (API) | La dirección opuesta: convertir un `Flow` en un `ReceiveChannel`. |
| `ReceiveChannel` (API) | El lado receptor de un channel: `receive`, iteración y `cancel`. |
| Channels | La guía oficial de channels, con el fan-out y el cierre del channel. |
| UI events | La guía de Android sobre eventos de UI y por qué recomienda modelarlos como estado. |
| Lifecycle-aware coroutines | `repeatOnLifecycle`, que cancela y relanza la colección según el ciclo de vida. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "receiveAsFlow()", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. Exponés un `Channel` como `Flow` con `receiveAsFlow()`, y dos collectors lo colectan al mismo tiempo. Se envían 4 valores. ¿Qué recibe cada collector?
2. Un ViewModel envía un evento a un `Channel` con buffer, expuesto con `receiveAsFlow()`, justo cuando la pantalla está en background y su collector está cancelado por `repeatOnLifecycle`. ¿Qué pasa con ese evento cuando la pantalla vuelve?
3. ¿Qué le pasa al channel cuando se cancela un collector de `receiveAsFlow()`? ¿Y qué le pasa a ese collector si el channel se cierra mientras está colectando?
4. Tenés un `Flow` obtenido con `consumeAsFlow()`. Lo colectás una vez hasta que termina, y después intentás colectarlo de nuevo. ¿Qué pasa?
5. `receiveAsFlow()` entrega cada evento una sola vez. Aun así, ¿por qué un evento se puede perder sin que se haya llegado a procesar? ¿En qué situación pasa?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: los valores se reparten (fan-out); cada valor va a un solo collector y entre los dos suman 4. Junior: cree que cada uno recibe los 4.
- P2 Senior: el evento espera en el buffer del channel y se entrega una vez cuando la pantalla vuelve a colectar; un SharedFlow sin replay lo habría perdido. Junior: cree que se pierde o se repite.
- P3 Senior: cancelar el collector no cierra el channel; si el channel se cierra con close() la colección se completa, y si se cierra con una excepción collect la lanza. Junior: no sabe.
- P4 Senior: consumeAsFlow se colecta una sola vez; la segunda colección lanza IllegalStateException, y al terminar la primera cancela el channel. Junior: cree que se puede colectar de nuevo.
- P5 Senior: el evento se entrega al recibirlo, no al procesarlo; si el collector se cancela entre medio (cambio de configuración) se pierde; por eso se prefiere modelarlo como estado de UI. Junior: no ve cómo se podría perder.
```
