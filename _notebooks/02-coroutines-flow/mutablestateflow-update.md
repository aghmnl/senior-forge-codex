---
topic: "MutableStateFlow.update {}"
chapter: 02-coroutines-flow
slug: mutablestateflow-update
lang: es
article: /es/02-coroutines-flow/mutablestateflow-update/
diagnostic_date: 2026-09-28
---

# Notebook de estudio — MutableStateFlow.update {}

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Qué hace `MutableStateFlow.update {}` por dentro? ¿Usa un lock?
2. Dos coroutines en `Dispatchers.Default` hacen, cada una, mil veces `_count.value = _count.value + 1` sobre un `MutableStateFlow(0)`. ¿Cuánto vale `_count` al final? ¿Y si usan `_count.update { it + 1 }`?
3. Un ViewModel escribe su estado siempre desde el main thread con `_uiState.value = _uiState.value.copy(...)`. ¿Tiene un bug hoy? ¿Qué cambio lo convertiría en un bug?
4. Leés `val items = _uiState.value.items`, calculás `val sorted = items.sortedBy { it.title }` y después hacés `_uiState.update { it.copy(items = sorted) }`. ¿Esa actualización es atómica? ¿Por qué?
5. ¿Qué diferencia hay entre `update`, `getAndUpdate` y `updateAndGet`? ¿Cuándo alcanza con asignar `value =` directamente?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | Es un ciclo sin lock: lee el valor actual, calcula el siguiente con el lambda y llama a `compareAndSet(prev, next)`, que lo guarda **solo si el estado sigue siendo `prev`**. Si otro escritor llegó primero, falla y **reintenta** con el valor nuevo. Nadie espera: el que pierde recalcula. | Sabe que "es atómico" pero no explica el compare-and-set ni el reintento. | No sabe qué hace, o cree que usa un lock. |
| 2 | Con `value = value + 1` el resultado es **menor que 2000** y cambia en cada ejecución: es un leer-modificar-escribir en dos pasos, y con dos threads en paralelo una escritura pisa a la otra (race condition, actualizaciones perdidas). Con `update { it + 1 }` da **exactamente 2000**, porque cada incremento se reintenta hasta aplicarse sobre el valor vigente. | Intuye que "puede fallar" pero no sabe por qué ni que `update` lo resuelve. | Cree que siempre da 2000. |
| 3 | Hoy no: sin punto de suspensión entre la lectura y la escritura, un solo thread no se puede intercalar. Se vuelve un bug en cuanto algún escritor corre en **otro thread**, por ejemplo una coroutine en `Dispatchers.IO` o `Default` que actualiza el mismo estado. Por eso `update` es la opción por defecto: sobrevive a ese refactor. | Dice que "está mal" sin distinguir cuándo falla, o dice que está bien sin ver el riesgo. | No ve ninguna relación con los threads. |
| 4 | **No es atómica**: `sorted` se calculó a partir de una foto leída afuera del lambda. Si el estado cambió entre esa lectura y el `update`, se escribe una lista derivada de datos viejos. `update` solo protege lo que se calcula a partir de `it`: el orden tiene que hacerse adentro, `update { it.copy(items = it.items.sortedBy { it.title }) }`. | Sospecha que hay un problema pero no sabe dónde. | Cree que es atómica porque usa `update`. |
| 5 | `update` no devuelve nada; `getAndUpdate` devuelve el valor **anterior** y `updateAndGet` el **nuevo**. `value =` alcanza cuando el valor nuevo **no depende del anterior** (una sobrescritura pura como `_isLoading.value = true`), porque no hay nada que leer y entonces no hay race condition. | Conoce `update` pero no las variantes, o no sabe cuándo alcanza la asignación simple. | No distingue ninguna. |

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
| 1 | Junior | "No sé". No conoce el ciclo de compare-and-set ni que `update` no usa lock. |
| 2 | Junior | "No sé". No conoce las actualizaciones perdidas por una race condition. |
| 3 | Junior | "No sé". No relaciona el riesgo con escritores en varios threads. |
| 4 | Junior | "No sé". No sabe que solo es atómico lo que se calcula a partir de `it`. |
| 5 | Junior | "No sé". No conoce `getAndUpdate` ni `updateAndGet`, ni cuándo alcanza `value =`. |

**Nivel global: Junior** (0 Senior, 0 intermedias, 5 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Tiene como base el artículo de StateFlow, que ya mencionó que value = value.copy(...) son dos operaciones y que update {} cierra ese hueco, y el tema Immutability & Atomic State for UI del capítulo de Kotlin Core; conviene conectar con esas dos piezas.

Necesita explicación en profundidad, desde cero: qué es un leer-modificar-escribir y por qué value = value.copy(...) son dos operaciones separadas; qué es una race condition y por qué produce actualizaciones perdidas sin ningún error; cómo funciona update por dentro, como un ciclo sin lock que lee, calcula y llama a compareAndSet, y reintenta si otro escritor ganó; por qué el problema solo aparece con escritores en varios threads (Dispatchers.IO o Default) y no en el main thread, donde sin punto de suspensión nada se intercala; por qué el lambda de update tiene que ser puro y corto, ya que puede correr más de una vez; por qué solo es atómico lo que se calcula a partir de it y no lo leído afuera del lambda; la diferencia entre update, getAndUpdate y updateAndGet; y cuándo alcanza con asignar value = directamente.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (dos personas editando el mismo documento a la vez y una pisando los cambios de la otra), qué es una race condition en un leer-modificar-escribir, después cómo update la resuelve con compare-and-set y reintentos, después cuándo el problema es real según los threads, y cerrá con las reglas prácticas: lambda puro, todo derivado de it, y value = solo para sobrescribir.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
MutableStateFlow.update {}

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/mutablestateflow-update/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/stateflow/
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/immutability-atomic-state/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/update/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mutable-state-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread/
https://aghmnl.github.io/senior-forge-codex/es/glosario/race-condition/
https://aghmnl.github.io/senior-forge-codex/es/glosario/atomicity/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lambdas/
https://aghmnl.github.io/senior-forge-codex/es/glosario/compare-and-set/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lock/
https://aghmnl.github.io/senior-forge-codex/es/glosario/get-and-update/
https://aghmnl.github.io/senior-forge-codex/es/glosario/update-and-get/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspension-point/
https://aghmnl.github.io/senior-forge-codex/es/glosario/main-thread/
https://aghmnl.github.io/senior-forge-codex/es/glosario/run-test/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutines/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatchers-io/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel/
https://aghmnl.github.io/senior-forge-codex/es/glosario/pure-function/
https://aghmnl.github.io/senior-forge-codex/es/glosario/it/
https://aghmnl.github.io/senior-forge-codex/es/glosario/query/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatcher/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/update.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/get-and-update.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/update-and-get.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-mutable-state-flow/compare-and-set.html
https://kotlinlang.org/docs/shared-mutable-state-and-concurrency.html
https://developer.android.com/kotlin/flow/stateflow-and-sharedflow
https://developer.android.com/topic/architecture/ui-layer/state-production
https://developer.android.com/kotlin/coroutines/coroutines-best-practices

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: MutableStateFlow.update {}
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Tiene como base el artículo de StateFlow, que ya mencionó que value = value.copy(...) son dos operaciones y que update {} cierra ese hueco, y el tema Immutability & Atomic State for UI del capítulo de Kotlin Core; conviene conectar con esas dos piezas.

Necesita explicación en profundidad, desde cero: qué es un leer-modificar-escribir y por qué value = value.copy(...) son dos operaciones separadas; qué es una race condition y por qué produce actualizaciones perdidas sin ningún error; cómo funciona update por dentro, como un ciclo sin lock que lee, calcula y llama a compareAndSet, y reintenta si otro escritor ganó; por qué el problema solo aparece con escritores en varios threads (Dispatchers.IO o Default) y no en el main thread, donde sin punto de suspensión nada se intercala; por qué el lambda de update tiene que ser puro y corto, ya que puede correr más de una vez; por qué solo es atómico lo que se calcula a partir de it y no lo leído afuera del lambda; la diferencia entre update, getAndUpdate y updateAndGet; y cuándo alcanza con asignar value = directamente.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (dos personas editando el mismo documento a la vez y una pisando los cambios de la otra), qué es una race condition en un leer-modificar-escribir, después cómo update la resuelve con compare-and-set y reintentos, después cuándo el problema es real según los threads, y cerrá con las reglas prácticas: lambda puro, todo derivado de it, y value = solo para sobrescribir.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| `update` (API) | El contrato y la implementación: el ciclo de lectura, cálculo y `compareAndSet`. |
| `getAndUpdate` (API) | La variante que devuelve el valor anterior al cambio. |
| `updateAndGet` (API) | La variante que devuelve el valor nuevo. |
| `compareAndSet` (API) | La operación atómica sobre la que se construye `update`, y cómo compara con `equals`. |
| Shared mutable state and concurrency | Por qué un leer-modificar-escribir pierde actualizaciones con varios threads, con el ejemplo clásico del contador. |
| StateFlow and SharedFlow | Cómo se expone y se actualiza el estado de un ViewModel con `MutableStateFlow`. |
| State production | Dónde se produce y se actualiza el estado de UI. |
| Best practices for coroutines | Qué dispatchers pueden terminar escribiendo el mismo estado desde threads distintos. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "MutableStateFlow.update {}", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Qué hace `MutableStateFlow.update {}` por dentro? ¿Usa un lock?
2. Dos coroutines en `Dispatchers.Default` hacen, cada una, mil veces `_count.value = _count.value + 1` sobre un `MutableStateFlow(0)`. ¿Cuánto vale `_count` al final? ¿Y si usan `_count.update { it + 1 }`?
3. Un ViewModel escribe su estado siempre desde el main thread con `_uiState.value = _uiState.value.copy(...)`. ¿Tiene un bug hoy? ¿Qué cambio lo convertiría en un bug?
4. Leés `val items = _uiState.value.items`, calculás `val sorted = items.sortedBy { it.title }` y después hacés `_uiState.update { it.copy(items = sorted) }`. ¿Esa actualización es atómica? ¿Por qué?
5. ¿Qué diferencia hay entre `update`, `getAndUpdate` y `updateAndGet`? ¿Cuándo alcanza con asignar `value =` directamente?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: ciclo sin lock que lee, calcula y hace compareAndSet; si otro escritor ganó, reintenta con el valor nuevo. Junior: cree que usa un lock o no sabe.
- P2 Senior: con value = value + 1 da menos de 2000 por actualizaciones perdidas entre threads; con update da exactamente 2000. Junior: cree que siempre da 2000.
- P3 Senior: hoy no hay bug porque un solo thread no se intercala sin punto de suspensión; falla cuando un escritor pasa a otro thread (Dispatchers.IO o Default). Junior: no ve la relación con los threads.
- P4 Senior: no es atómica porque sorted sale de una foto leída afuera del lambda; hay que ordenar adentro, a partir de it. Junior: cree que es atómica por usar update.
- P5 Senior: getAndUpdate devuelve el valor anterior y updateAndGet el nuevo; value = alcanza para sobrescrituras que no dependen del valor anterior. Junior: no las distingue.
```
