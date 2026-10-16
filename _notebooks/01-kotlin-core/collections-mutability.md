---
topic: "Collections & Mutability"
chapter: 01-kotlin-core
slug: collections-mutability
lang: es
article: /es/01-kotlin-core/collections-mutability/
diagnostic_date: 2026-10-16
---

# Notebook de estudio — Collections & Mutability

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. Tenés un `filter` sobre 1.000 tareas que adentro hace `if (task.id in selectedIds)`, donde `selectedIds` es un `List`. ¿Qué problema de rendimiento tiene y cómo lo arreglás?
2. ¿Cuál es la diferencia entre una colección *de solo lectura* y una *inmutable* en Kotlin? ¿`listOf()` te da cuál?
3. ¿Qué hace `buildList { }` y por qué conviene frente a crear un `mutableListOf()` y devolverlo?
4. ¿Qué cambia si encadenás `map`, `filter` y `first` sobre una lista directamente, frente a hacerlo después de `asSequence()`?
5. Dos instancias de una data class tienen una propiedad `tags` con los mismos elementos pero en distinto orden. ¿Son iguales si `tags` es un `List`? ¿Y si es un `Set`?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | `in` sobre un `List` es **`O(n)`**, y adentro del `filter` el total es **`O(n·m)`**. Se arregla convirtiendo `selectedIds` a **`Set`** (fuera del bucle), donde `in` es `O(1)`, y el total pasa a `O(n + m)`. | Sabe que es lento pero no propone el `Set`. | No ve el problema. |
| 2 | **Solo lectura** es una propiedad de la **referencia**: `List` no tiene métodos para mutar, pero el objeto detrás puede ser un `MutableList` que otro modifica. **Inmutable** es una propiedad del **objeto**: nadie puede cambiarlo. `listOf()` devuelve una instancia no modificable, pero el tipo `List` en sí no garantiza inmutabilidad. | Intuye que no son lo mismo pero no distingue referencia de objeto. | Cree que son lo mismo. |
| 3 | Da un **receiver mutable** solo adentro del bloque y **devuelve un `List` de solo lectura**: la mutación queda confinada a esa construcción y quien recibe el resultado no puede modificarlo. | Sabe que construye una lista pero no la ventaja de no exponer el mutable. | No sabe. |
| 4 | Sobre la lista, cada operador es **eager**: crea una **lista intermedia** completa por paso. Con `asSequence()` es **lazy**: cada elemento atraviesa toda la cadena y `first` corta apenas encuentra uno, sin listas intermedias. Conviene con cadenas largas, fuentes grandes o cortes tempranos; con pocos elementos, la lista suele ser más rápida. | Sabe que la secuencia es "lazy" pero no explica las listas intermedias ni el corte. | No sabe. |
| 5 | Con **`List`, no**: la igualdad compara los elementos **en orden**. Con **`Set`, sí**: el orden no importa. Esto afecta el `equals` de la data class y, por lo tanto, cuándo Compose considera que el estado cambió. | Acierta uno de los dos. | No sabe. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior a Senior; 3+ intermedias o mezcla a Intermedio; 3+ junior o "no sé" a Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-10-16

> El artículo existía desde el 2026-09-08 y el learner probablemente ya lo había leído; el diagnóstico se tomó al generar el notebook, sin mirarlo.

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Junior | "No sé". No conoce el costo de `in` sobre un `List` ni la solución con `Set`. |
| 2 | Junior | "No sé". No distingue solo lectura de inmutable. |
| 3 | Junior | "No sé". No conoce `buildList { }`. |
| 4 | Junior | "No sé". No conoce la diferencia entre evaluación eager y lazy (`Sequence`). |
| 5 | Junior | "No sé". No conoce cómo afecta el orden a la igualdad de `List` y `Set`. |

**Nivel global: Junior** (0 Senior, 0 intermedias, 5 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Usa List, Set, Map, map y filter a diario, así que conviene partir de esos usos. Viene de Generics, donde vio por qué List es covariante y MutableList no.

Necesita explicación en profundidad, desde cero: la división entre interfaces de solo lectura (List, Set, Map) y mutables (MutableList, MutableSet, MutableMap); por qué solo lectura no es lo mismo que inmutable (la referencia frente al objeto) y la trampa de exponer un MutableList privado como List; el costo de cada estructura (contains en List es O(n), en Set es O(1)) y el patrón de convertir a Set fuera de un bucle; buildList { } y el patrón de mutar localmente y publicar de solo lectura; la diferencia entre operadores eager y Sequences lazy; y cómo List y Set afectan el equals de una data class y la recomposition en Compose.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una vitrina que se mira pero no se toca, aunque el dueño puede cambiar lo que hay adentro), solo lectura frente a inmutable, después el costo de List frente a Set, buildList, las Sequences, y cerrá con la igualdad de colecciones y su efecto en Compose.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Collections & Mutability

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/collections-mutability/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/immutability-atomic-state/
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/generics-variance-reification/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/collections/
https://aghmnl.github.io/senior-forge-codex/es/glosario/list/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sets/
https://aghmnl.github.io/senior-forge-codex/es/glosario/maps/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mutable-list/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mutable-set/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mutable-map/
https://aghmnl.github.io/senior-forge-codex/es/glosario/add/
https://aghmnl.github.io/senior-forge-codex/es/glosario/remove/
https://aghmnl.github.io/senior-forge-codex/es/glosario/put/
https://aghmnl.github.io/senior-forge-codex/es/glosario/clear/
https://aghmnl.github.io/senior-forge-codex/es/glosario/standard-library/
https://aghmnl.github.io/senior-forge-codex/es/glosario/read-only-view/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mutation/
https://aghmnl.github.io/senior-forge-codex/es/glosario/arraylist/
https://aghmnl.github.io/senior-forge-codex/es/glosario/list-of/
https://aghmnl.github.io/senior-forge-codex/es/glosario/variance/
https://aghmnl.github.io/senior-forge-codex/es/glosario/covariance/
https://aghmnl.github.io/senior-forge-codex/es/glosario/invariance/
https://aghmnl.github.io/senior-forge-codex/es/glosario/contains/
https://aghmnl.github.io/senior-forge-codex/es/glosario/set-of/
https://aghmnl.github.io/senior-forge-codex/es/glosario/map-of/
https://aghmnl.github.io/senior-forge-codex/es/glosario/to-list/
https://aghmnl.github.io/senior-forge-codex/es/glosario/to-set/
https://aghmnl.github.io/senior-forge-codex/es/glosario/to-mutable-list/
https://aghmnl.github.io/senior-forge-codex/es/glosario/defensive-copy/
https://aghmnl.github.io/senior-forge-codex/es/glosario/build-list/
https://aghmnl.github.io/senior-forge-codex/es/glosario/build-map/
https://aghmnl.github.io/senior-forge-codex/es/glosario/builder-functions/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collection-operators/
https://aghmnl.github.io/senior-forge-codex/es/glosario/map-operator/
https://aghmnl.github.io/senior-forge-codex/es/glosario/filter/
https://aghmnl.github.io/senior-forge-codex/es/glosario/group-by/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sorted/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sequences/
https://aghmnl.github.io/senior-forge-codex/es/glosario/as-sequence/
https://aghmnl.github.io/senior-forge-codex/es/glosario/terminal-operations/
https://aghmnl.github.io/senior-forge-codex/es/glosario/allocations/
https://aghmnl.github.io/senior-forge-codex/es/glosario/overhead/
https://aghmnl.github.io/senior-forge-codex/es/glosario/concurrency/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel-store/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lambdas/
https://aghmnl.github.io/senior-forge-codex/es/glosario/immutability/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutines/
https://aghmnl.github.io/senior-forge-codex/es/glosario/synchronized-block/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread-safety/
https://aghmnl.github.io/senior-forge-codex/es/glosario/stack-frame/
https://aghmnl.github.io/senior-forge-codex/es/glosario/call-site/
https://aghmnl.github.io/senior-forge-codex/es/glosario/functional-style/
https://aghmnl.github.io/senior-forge-codex/es/glosario/protected-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/backing-field/
https://aghmnl.github.io/senior-forge-codex/es/glosario/stateflow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/equals/
https://aghmnl.github.io/senior-forge-codex/es/glosario/stable/
https://aghmnl.github.io/senior-forge-codex/es/glosario/snapshot-system/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mutable-state-list-of/
https://aghmnl.github.io/senior-forge-codex/es/glosario/snapshot-state-list/
https://aghmnl.github.io/senior-forge-codex/es/glosario/observable-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/return-type/
https://aghmnl.github.io/senior-forge-codex/es/glosario/runtime/
https://aghmnl.github.io/senior-forge-codex/es/glosario/unidirectional-data-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/jetpack-compose/
https://aghmnl.github.io/senior-forge-codex/es/glosario/persistent-collections/
https://aghmnl.github.io/senior-forge-codex/es/glosario/garbage-collector/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/collections-overview.html
https://kotlinlang.org/docs/constructing-collections.html
https://kotlinlang.org/docs/sequences.html
https://kotlinlang.org/docs/collection-operations.html

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Collections & Mutability
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Usa List, Set, Map, map y filter a diario, así que conviene partir de esos usos. Viene de Generics, donde vio por qué List es covariante y MutableList no.

Necesita explicación en profundidad, desde cero: la división entre interfaces de solo lectura (List, Set, Map) y mutables (MutableList, MutableSet, MutableMap); por qué solo lectura no es lo mismo que inmutable (la referencia frente al objeto) y la trampa de exponer un MutableList privado como List; el costo de cada estructura (contains en List es O(n), en Set es O(1)) y el patrón de convertir a Set fuera de un bucle; buildList { } y el patrón de mutar localmente y publicar de solo lectura; la diferencia entre operadores eager y Sequences lazy; y cómo List y Set afectan el equals de una data class y la recomposition en Compose.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una vitrina que se mira pero no se toca, aunque el dueño puede cambiar lo que hay adentro), solo lectura frente a inmutable, después el costo de List frente a Set, buildList, las Sequences, y cerrá con la igualdad de colecciones y su efecto en Compose.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Collections overview | Las interfaces de solo lectura y mutables, y los tipos List, Set y Map. |
| Constructing collections | `listOf`, `buildList`, copias con `toList` y `toMutableList`. |
| Sequences | Evaluación lazy frente a eager y cuándo conviene cada una. |
| Collection operations | Los operadores (`map`, `filter`, `groupBy`) y que cada uno crea una colección nueva. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Collections & Mutability", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. Tenés un `filter` sobre 1.000 tareas que adentro hace `if (task.id in selectedIds)`, donde `selectedIds` es un `List`. ¿Qué problema de rendimiento tiene y cómo lo arreglás?
2. ¿Cuál es la diferencia entre una colección *de solo lectura* y una *inmutable* en Kotlin? ¿`listOf()` te da cuál?
3. ¿Qué hace `buildList { }` y por qué conviene frente a crear un `mutableListOf()` y devolverlo?
4. ¿Qué cambia si encadenás `map`, `filter` y `first` sobre una lista directamente, frente a hacerlo después de `asSequence()`?
5. Dos instancias de una data class tienen una propiedad `tags` con los mismos elementos pero en distinto orden. ¿Son iguales si `tags` es un `List`? ¿Y si es un `Set`?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: in sobre List es O(n), total O(n·m); convertir a Set fuera del bucle. Junior: no ve el problema.
- P2 Senior: solo lectura es de la referencia, inmutable es del objeto; List no garantiza inmutabilidad. Junior: cree que son lo mismo.
- P3 Senior: buildList da un receiver mutable solo adentro y devuelve un List de solo lectura. Junior: no sabe.
- P4 Senior: eager crea listas intermedias; Sequence es lazy y first corta temprano. Junior: no sabe.
- P5 Senior: con List no son iguales (importa el orden); con Set sí. Junior: no sabe.
```
