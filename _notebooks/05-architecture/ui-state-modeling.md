---
topic: "UI State Modeling: Sealed vs Flat Data Class"
chapter: 05-architecture
slug: ui-state-modeling
lang: es
article: /es/05-architecture/ui-state-modeling/
diagnostic_date: 2026-10-12
---

# Notebook de estudio — UI State Modeling: Sealed vs Flat Data Class

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Qué significa que un sealed state "no puede representar estados imposibles"? Dame un ejemplo de un estado imposible que sí se puede escribir con una data class plana.
2. Agregás un subtipo nuevo a una `sealed interface` que se usa en varios `when` del proyecto, ninguno con `else`. ¿Qué pasa al compilar?
3. ¿Qué es un modelo de UI state *híbrido*? Dame un ejemplo de cuándo lo usarías.
4. ¿Por qué `_state.value = _state.value.copy(isLoading = false)` puede perder actualizaciones, y qué usarías en su lugar?
5. Una pantalla usa `sealed interface State { Loading, Loaded(items, query), Error }`. El usuario escribió una búsqueda y se dispara un refresco que pasa el estado a `Loading`. ¿Qué problema aparece?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | Un sealed state es **uno solo de sus subtipos a la vez**, así que no existe una forma de estar en `Loading` y `Error` juntos. Con una data class plana sí se puede escribir, por ejemplo, `isLoading = true` con un `errorMessage` y una lista de resultados, y el compilador no lo impide. | Entiende la idea pero no da un ejemplo concreto. | No sabe. |
| 2 | **No compila**: cada `when` sin `else` deja de ser exhaustivo y el compilador obliga a manejar el subtipo nuevo en todos lados. | Sabe que da error pero no lo relaciona con la exhaustividad. | Cree que compila igual. |
| 3 | Una data class plana para las partes que conviven, con **propiedades sealed** (muchas veces nullables) para las partes con variantes excluyentes, o un sealed de nivel superior cuyo subtipo principal es plano. Ejemplo: una confirmación pendiente que es borrar o archivar o nada, adentro del estado plano de una lista. | Intuye que combina los dos pero no da un ejemplo. | No sabe. |
| 4 | Lee y escribe en **dos pasos**: si otra coroutine actualiza en el medio, una de las dos escrituras pisa a la otra (race condition). Se usa **`update { it.copy(...) }`**, que reintenta hasta aplicar el cambio sobre el último valor. | Sabe que hay que usar `update` pero no explica por qué. | No ve el problema. |
| 5 | La búsqueda vive adentro de `Loaded`; al pasar a `Loading` **se pierde**, y el campo de búsqueda se vacía o la UI tiene que recordarla aparte. Es la señal de que las preocupaciones se **superponen** y conviene un estado plano (o híbrido) en lugar de un sealed para toda la pantalla. | Ve que se pierde algo pero no saca la conclusión de modelado. | No ve el problema. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior a Senior; 3+ intermedias o mezcla a Intermedio; 3+ junior o "no sé" a Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-10-12

> El artículo existía desde el 2026-08-19 en una versión anterior, más corta, que el learner ya había leído. Esta versión fue reescrita el 2026-10-12 y el diagnóstico se tomó antes de leerla.

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Junior | "No sé". No conoce la idea de estados imposibles ni puede dar un ejemplo con una data class plana. |
| 2 | Senior | "No compila hasta que todos los subtipos estén en todos los when (todos sin else)." Correcto: entiende la exhaustividad del `when` sobre un tipo sealed. |
| 3 | Junior | "No sé". No conoce el modelo híbrido. |
| 4 | Junior | "No sé". No conecta la lectura y escritura en dos pasos con la race condition ni con `update { }`, aunque lo vio en MutableStateFlow.update {}. |
| 5 | Junior | "No sé". No ve que la búsqueda se pierde al pasar a `Loading`. |

**Nivel global: Junior** (1 Senior, 0 intermedias, 4 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: la exhaustividad del when sobre un tipo sealed; sabe que agregar un subtipo hace que no compile ningún when sin else hasta manejarlo. Se puede tratar como repaso rápido.

Necesita explicación en profundidad, desde cero: qué significa que un sealed state no puede representar estados imposibles, con ejemplos concretos de combinaciones imposibles en una data class plana (isLoading = true junto con un error y una lista); cuándo los estados de una pantalla realmente se excluyen y cuándo se superponen, y por qué un sealed Loading / Loaded / Error pierde la búsqueda o la selección al pasar a Loading; qué es el modelo híbrido, con el ejemplo de una confirmación pendiente modelada como propiedad sealed nullable adentro de un estado plano; cómo modelar un diálogo o una navegación como estado que la UI muestra y el ViewModel limpia; y por qué actualizar con _state.value = _state.value.copy(...) puede perder cambios (race condition) y update { } lo evita. Esto último ya lo vio en MutableStateFlow.update {}, pero no lo recordó.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: tratá la exhaustividad del when como repaso rápido; explicá desde cero, con analogías (un semáforo, que está en un solo color a la vez, frente al tablero de un auto, donde muchas luces pueden estar encendidas al mismo tiempo), la diferencia entre sealed y plano, después el modelo híbrido y el diálogo como estado, y cerrá con update { } y la race condition.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
UI State Modeling: Sealed vs Flat Data Class

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/05-architecture/ui-state-modeling/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/sealed-classes-interfaces/
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/data-classes/
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/mutablestateflow-update/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/unidirectional-data-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel/
https://aghmnl.github.io/senior-forge-codex/es/glosario/stateflow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sealed-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sealed-interface/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sealed-class/
https://aghmnl.github.io/senior-forge-codex/es/glosario/loading-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/success-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/error-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/when-expression/
https://aghmnl.github.io/senior-forge-codex/es/glosario/flat-data-class/
https://aghmnl.github.io/senior-forge-codex/es/glosario/copy/
https://aghmnl.github.io/senior-forge-codex/es/glosario/process-death/
https://aghmnl.github.io/senior-forge-codex/es/glosario/channel/
https://aghmnl.github.io/senior-forge-codex/es/glosario/one-shot-event/
https://aghmnl.github.io/senior-forge-codex/es/glosario/atomicity/
https://aghmnl.github.io/senior-forge-codex/es/glosario/recomposition/
https://aghmnl.github.io/senior-forge-codex/es/glosario/null/
https://aghmnl.github.io/senior-forge-codex/es/glosario/saved-instance-state/

**Fuentes oficiales (agregar cada una como fuente web)**
https://developer.android.com/topic/architecture/ui-layer
https://developer.android.com/topic/architecture/ui-layer/state-production
https://developer.android.com/topic/architecture/ui-layer/stateholders
https://developer.android.com/topic/architecture/ui-layer/events
https://kotlinlang.org/docs/sealed-classes.html
https://kotlinlang.org/docs/data-classes.html

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: UI State Modeling: Sealed vs Flat Data Class
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: la exhaustividad del when sobre un tipo sealed; sabe que agregar un subtipo hace que no compile ningún when sin else hasta manejarlo. Se puede tratar como repaso rápido.

Necesita explicación en profundidad, desde cero: qué significa que un sealed state no puede representar estados imposibles, con ejemplos concretos de combinaciones imposibles en una data class plana (isLoading = true junto con un error y una lista); cuándo los estados de una pantalla realmente se excluyen y cuándo se superponen, y por qué un sealed Loading / Loaded / Error pierde la búsqueda o la selección al pasar a Loading; qué es el modelo híbrido, con el ejemplo de una confirmación pendiente modelada como propiedad sealed nullable adentro de un estado plano; cómo modelar un diálogo o una navegación como estado que la UI muestra y el ViewModel limpia; y por qué actualizar con _state.value = _state.value.copy(...) puede perder cambios (race condition) y update { } lo evita. Esto último ya lo vio en MutableStateFlow.update {}, pero no lo recordó.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: tratá la exhaustividad del when como repaso rápido; explicá desde cero, con analogías (un semáforo, que está en un solo color a la vez, frente al tablero de un auto, donde muchas luces pueden estar encendidas al mismo tiempo), la diferencia entre sealed y plano, después el modelo híbrido y el diálogo como estado, y cerrá con update { } y la race condition.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| UI layer | Qué es el UI state, el unidirectional data flow y por qué la UI es una función del estado. |
| UI state production | Cómo el ViewModel produce y actualiza el estado, incluido `update { }`. |
| State holders and UI state | Dónde vive cada parte del estado y qué expone el ViewModel. |
| UI events | Por qué Google recomienda modelar los eventos como estado que la UI consume y limpia. |
| Sealed classes and interfaces | Jerarquías cerradas y la exhaustividad del `when`. |
| Data classes | `copy()`, `equals` y por qué una data class encaja como estado plano. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "UI State Modeling: Sealed vs Flat Data Class", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Qué significa que un sealed state "no puede representar estados imposibles"? Dame un ejemplo de un estado imposible que sí se puede escribir con una data class plana.
2. Agregás un subtipo nuevo a una `sealed interface` que se usa en varios `when` del proyecto, ninguno con `else`. ¿Qué pasa al compilar?
3. ¿Qué es un modelo de UI state *híbrido*? Dame un ejemplo de cuándo lo usarías.
4. ¿Por qué `_state.value = _state.value.copy(isLoading = false)` puede perder actualizaciones, y qué usarías en su lugar?
5. Una pantalla usa `sealed interface State { Loading, Loaded(items, query), Error }`. El usuario escribió una búsqueda y se dispara un refresco que pasa el estado a `Loading`. ¿Qué problema aparece?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: un sealed state es un solo subtipo a la vez; con una data class plana se puede escribir isLoading = true junto con un error y una lista. Junior: no sabe.
- P2 Senior: no compila; cada when sin else deja de ser exhaustivo y obliga a manejar el subtipo nuevo. Junior: cree que compila.
- P3 Senior: estado plano con propiedades sealed para las partes excluyentes, por ejemplo una confirmación pendiente nullable. Junior: no sabe.
- P4 Senior: lee y escribe en dos pasos y dos coroutines se pisan (race condition); se usa update { it.copy(...) }. Junior: no ve el problema.
- P5 Senior: la búsqueda vive en Loaded y se pierde al pasar a Loading; señal de que conviene un estado plano o híbrido. Junior: no ve el problema.
```
