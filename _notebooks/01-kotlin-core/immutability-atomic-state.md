---
topic: "Immutability & Atomic State for UI"
chapter: 01-kotlin-core
slug: immutability-atomic-state
lang: es
article: /es/01-kotlin-core/immutability-atomic-state/
diagnostic_date: 2026-10-16
---

# Notebook de estudio — Immutability & Atomic State for UI

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. Una data class de estado tiene una propiedad `val tasks: MutableList<Task>`. Si es `val`, ¿el estado es inmutable? ¿Qué problema puede traer?
2. ¿Qué es el *structural sharing* cuando hacés `state.copy(searchQuery = "x")` sobre una data class con una lista enorme adentro? ¿Se copia la lista?
3. ¿Por qué la lambda que le pasás a `update { }` tiene que ser pura, sin logs ni navegación adentro?
4. ¿Por qué es mejor que `isSelectionMode` sea una propiedad derivada de `selectedIds` (un getter) y no un campo guardado aparte?
5. ¿Por qué no conviene exponer el estado de una pantalla como cinco `MutableStateFlow` separados, uno por campo, en lugar de un solo objeto de estado?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | **No**: `val` impide reasignar la referencia, pero la lista se puede **mutar en el lugar**. Dos estados comparten el mismo buffer, `equals` dice "sin cambios" aunque el contenido cambió, `update` (CAS) no detecta el cambio, y Compose no puede tratarlo como stable: la pantalla no se actualiza o se recompone de más. | Sabe que la lista se puede modificar pero no ve las consecuencias en `equals`, `StateFlow` o Compose. | Cree que `val` alcanza para que sea inmutable. |
| 2 | `copy` crea **un objeto nuevo chico** y **reutiliza las referencias** de todo lo que no cambió: la lista no se copia, el estado nuevo apunta a la misma lista. Por eso una transición cuesta poco aunque el estado contenga colecciones grandes. | Sabe que no se copia todo pero no lo nombra ni explica las referencias compartidas. | Cree que `copy` duplica la lista. |
| 3 | `update` es un **retry loop de Compare-and-Set**: si otro escritor publicó en el medio, **vuelve a ejecutar la lambda**. Cualquier efecto secundario adentro se puede ejecutar **más de una vez**. Se calcula el estado nuevo adentro y los efectos van después. | Sabe que tiene que ser pura pero no que se puede reintentar. | No sabe. |
| 4 | Una propiedad derivada **no puede desincronizarse** de su fuente: no existe el estado "selection mode activo con la selección vacía". Un campo aparte obliga a mantener los dos sincronizados en cada `copy`, y basta un olvido para tener un estado inconsistente. Es single source of truth dentro de la clase. | Sabe que es "más limpio" pero no menciona la desincronización. | No sabe. |
| 5 | Cinco flows se actualizan **por separado**, así que la UI puede observar **combinaciones que no son un estado real** (loading en `true` con resultados ya presentes). Un solo objeto inmutable hace que cada transición sea **todo o nada** y da una sola cosa para renderizar. | Dice que es más ordenado sin mencionar las combinaciones intermedias. | No sabe. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior a Senior; 3+ intermedias o mezcla a Intermedio; 3+ junior o "no sé" a Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-10-16

> El artículo existía desde el 2026-09-09 y el learner probablemente ya lo había leído; el diagnóstico se tomó al generar el notebook, sin mirarlo.

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Junior | "No sé". No ve que una `MutableList` adentro de un `val` rompe la inmutabilidad. |
| 2 | Junior | "No sé". No conoce el structural sharing de `copy`. |
| 3 | Junior | "No sé". No sabe que la lambda de `update` se puede reintentar. |
| 4 | Junior | "No sé". No conoce el beneficio de las propiedades derivadas. |
| 5 | Junior | "No sé". No ve el riesgo de estados intermedios con varios flows separados. |

**Nivel global: Junior** (0 Senior, 0 intermedias, 5 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Ya estudió MutableStateFlow.update {} y UI State Modeling, así que conviene presentar este tema como el fundamento de los dos: por qué el estado tiene que ser inmutable y por qué update funciona.

Necesita explicación en profundidad, desde cero: qué es la inmutabilidad y el value semantics de una data class de val de tipos de solo lectura; por qué una MutableList adentro de un val rompe equals, StateFlow, update y la stability en Compose; cómo copy expresa las transiciones con structural sharing (sin copiar las colecciones); por qué value = value.copy(...) pierde actualizaciones (race condition) y cómo update {} lo resuelve con Compare-and-Set; por qué la lambda de update tiene que ser pura y leer el valor viejo por su parámetro; el patrón de MutableStateFlow privado con asStateFlow público; las propiedades derivadas como single source of truth; y por qué un solo objeto de estado le gana a varios flows separados.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una foto que no se edita, se saca una nueva; y un formulario que se envía completo en lugar de campo por campo), la inmutabilidad y copy, después la race condition y update {}, y cerrá con las propiedades derivadas y el objeto de estado único.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Immutability & Atomic State for UI

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/immutability-atomic-state/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/collections-mutability/
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/mutablestateflow-update/
https://aghmnl.github.io/senior-forge-codex/es/05-architecture/ui-state-modeling/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/immutability/
https://aghmnl.github.io/senior-forge-codex/es/glosario/state-holder/
https://aghmnl.github.io/senior-forge-codex/es/glosario/value-semantics/
https://aghmnl.github.io/senior-forge-codex/es/glosario/equals/
https://aghmnl.github.io/senior-forge-codex/es/glosario/jetpack-compose/
https://aghmnl.github.io/senior-forge-codex/es/glosario/stateflow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/copy/
https://aghmnl.github.io/senior-forge-codex/es/glosario/structural-sharing/
https://aghmnl.github.io/senior-forge-codex/es/glosario/atomicity/
https://aghmnl.github.io/senior-forge-codex/es/glosario/race-condition/
https://aghmnl.github.io/senior-forge-codex/es/glosario/update/
https://aghmnl.github.io/senior-forge-codex/es/glosario/compare-and-set/
https://aghmnl.github.io/senior-forge-codex/es/glosario/as-state-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/read-only-view/
https://aghmnl.github.io/senior-forge-codex/es/glosario/conflation/
https://aghmnl.github.io/senior-forge-codex/es/glosario/stable/
https://aghmnl.github.io/senior-forge-codex/es/glosario/derived-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/backing-field/
https://aghmnl.github.io/senior-forge-codex/es/glosario/single-source-of-truth/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread-safety/
https://aghmnl.github.io/senior-forge-codex/es/glosario/synchronized-block/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutines/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel-store/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cast/
https://aghmnl.github.io/senior-forge-codex/es/glosario/unidirectional-data-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sets/
https://aghmnl.github.io/senior-forge-codex/es/glosario/distinct-until-changed/
https://aghmnl.github.io/senior-forge-codex/es/glosario/recomposition/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/data-classes.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/update.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-mutable-state-flow/
https://developer.android.com/topic/architecture/ui-layer/state-production

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Immutability & Atomic State for UI
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Ya estudió MutableStateFlow.update {} y UI State Modeling, así que conviene presentar este tema como el fundamento de los dos: por qué el estado tiene que ser inmutable y por qué update funciona.

Necesita explicación en profundidad, desde cero: qué es la inmutabilidad y el value semantics de una data class de val de tipos de solo lectura; por qué una MutableList adentro de un val rompe equals, StateFlow, update y la stability en Compose; cómo copy expresa las transiciones con structural sharing (sin copiar las colecciones); por qué value = value.copy(...) pierde actualizaciones (race condition) y cómo update {} lo resuelve con Compare-and-Set; por qué la lambda de update tiene que ser pura y leer el valor viejo por su parámetro; el patrón de MutableStateFlow privado con asStateFlow público; las propiedades derivadas como single source of truth; y por qué un solo objeto de estado le gana a varios flows separados.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una foto que no se edita, se saca una nueva; y un formulario que se envía completo en lugar de campo por campo), la inmutabilidad y copy, después la race condition y update {}, y cerrá con las propiedades derivadas y el objeto de estado único.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Data classes | `copy`, `equals` y por qué una data class de `val` funciona como valor. |
| update (API) | El contrato de `update`: reintenta la función hasta aplicar el cambio de forma atómica. |
| MutableStateFlow (API) | `value`, `compareAndSet` y la conflación por igualdad. |
| UI state production | Cómo un ViewModel produce y publica un único estado de UI inmutable. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Immutability & Atomic State for UI", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. Una data class de estado tiene una propiedad `val tasks: MutableList<Task>`. Si es `val`, ¿el estado es inmutable? ¿Qué problema puede traer?
2. ¿Qué es el *structural sharing* cuando hacés `state.copy(searchQuery = "x")` sobre una data class con una lista enorme adentro? ¿Se copia la lista?
3. ¿Por qué la lambda que le pasás a `update { }` tiene que ser pura, sin logs ni navegación adentro?
4. ¿Por qué es mejor que `isSelectionMode` sea una propiedad derivada de `selectedIds` (un getter) y no un campo guardado aparte?
5. ¿Por qué no conviene exponer el estado de una pantalla como cinco `MutableStateFlow` separados, uno por campo, en lugar de un solo objeto de estado?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: no; la lista se muta en el lugar y rompe equals, update y Compose. Junior: cree que val alcanza.
- P2 Senior: copy crea un objeto chico y reutiliza las referencias; la lista no se copia. Junior: cree que copy duplica la lista.
- P3 Senior: update reintenta la lambda si otro escribió en el medio; los efectos se repetirían. Junior: no sabe.
- P4 Senior: una propiedad derivada no puede desincronizarse; single source of truth. Junior: no sabe.
- P5 Senior: varios flows dejan ver combinaciones que no son un estado real; un objeto único es todo o nada. Junior: no sabe.
```
