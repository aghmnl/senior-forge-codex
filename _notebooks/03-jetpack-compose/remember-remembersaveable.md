---
topic: "remember & rememberSaveable"
chapter: 03-jetpack-compose
slug: remember-remembersaveable
lang: es
article: /es/03-jetpack-compose/remember-remembersaveable/
diagnostic_date: 2026-10-10
---

# Notebook de estudio — remember & rememberSaveable

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. Adentro de un composable declarás `var count = 0`, y un botón hace `count++` en su `onClick`. ¿Qué ves en pantalla al tocar el botón, y por qué?
2. En `val filtered = remember(query) { allItems.filter { it.matches(query) } }`, ¿qué papel cumple `query` entre los paréntesis de `remember`?
3. Rotás el teléfono y la Activity se recrea. ¿Qué pasa con un valor guardado con `remember`? ¿Y con uno guardado con `rememberSaveable`?
4. Querés guardar con `rememberSaveable` una data class propia, `DateRange(start: LocalDate, end: LocalDate)`, que no es `Parcelable`. ¿Qué pasa, y cómo lo resolvés?
5. ¿Por qué no conviene guardar una lista de 5.000 tareas con `rememberSaveable`?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | El número **no cambia**. `count` es una variable local: cambiarla no es estado observable, así que no dispara recomposition; y si algo recompone el composable, la función vuelve a correr y `count` vuelve a 0. Hace falta `var count by remember { mutableStateOf(0) }`: `MutableState` para que Compose observe el cambio y `remember` para conservarlo entre recomposiciones. | Sabe que hace falta `mutableStateOf` o `remember`, pero no explica las dos piezas. | No ve ningún problema. |
| 2 | Es una **key**: el cálculo se cachea y solo se vuelve a ejecutar cuando `query` cambia. Si el cálculo dependiera de otro valor que no es key, el resultado quedaría viejo. | Sabe que tiene que ver con recalcular pero no lo explica. | No sabe. |
| 3 | El de `remember` **se pierde**, porque vive en la composition y la Activity recreada arranca una composition nueva. El de `rememberSaveable` **se restaura**, porque además se guardó en el saved instance state (un `Bundle`); también sobrevive a la muerte del proceso. | Acierta el resultado pero no explica el mecanismo (saved instance state, `Bundle`) o confunde recreación con recomposition. | Cree que los dos se comportan igual. |
| 4 | El `Bundle` no sabe guardar ese tipo, así que falla en Runtime al guardar el estado. Se resuelve haciéndola `Parcelable` con `@Parcelize`, o con un **`Saver`** propio (`listSaver`/`mapSaver`) pasado como `stateSaver`. | Sabe que no se puede guardar directamente pero no conoce las soluciones. | No sabe. |
| 5 | El estado guardado viaja en un `Bundle` con un **límite de tamaño** (alrededor de 1 MB para toda la transacción); excederlo produce una **`TransactionTooLargeException`**. Se guarda un valor chico (un id, una búsqueda) y los datos se reconstruyen desde su fuente real (base de datos, ViewModel). | Sabe que es "demasiado" pero no nombra el `Bundle`, el límite o la alternativa. | No ve el problema. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior a Senior; 3+ intermedias o mezcla a Intermedio; 3+ junior o "no sé" a Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-10-10

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Junior | "Al estar dentro del composable no sé qué problema habría." No ve que una variable local no es estado observable ni sobrevive a la recomposition. |
| 2 | Junior | "No sé". No conoce el rol de las keys de `remember`. |
| 3 | Intermedio | "El de remember no perdura con la recomposición de la activity, el rememberSaveable sí." El resultado es correcto, pero llama "recomposición" a la recreación de la Activity y no explica el saved instance state. |
| 4 | Junior | "No sé". No conoce `@Parcelize` ni los `Saver`. |
| 5 | Intermedio | "Es demasiada información para algo diseñado para guardar pequeñas variables." Intuición correcta, sin nombrar el `Bundle`, su límite de tamaño ni la `TransactionTooLargeException`. |

**Nivel global: Junior** (0 Senior, 2 intermedias, 3 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior, con buena intuición sobre el tiempo de vida.

Ya domina: la idea de que rememberSaveable sobrevive a la recreación de la Activity y remember no, y que rememberSaveable está pensado para valores chicos. Conviene partir de ahí y explicar el porqué.

Necesita explicación en profundidad, desde cero: por qué una variable local en un composable no funciona como estado (no es observable y se reinicia cada vez que la función vuelve a correr), y por qué hacen falta las dos piezas, MutableState para que Compose observe el cambio y remember para conservarlo entre recomposiciones; qué hacen las keys de remember, que recalculan el valor solo cuando cambian; el mecanismo de rememberSaveable, que guarda el valor en el saved instance state (un Bundle) y por eso también sobrevive a la muerte del proceso; qué tipos puede guardar el Bundle y cómo se resuelve un tipo propio con @Parcelize o un Saver (listSaver, mapSaver); y el límite de tamaño del Bundle, la TransactionTooLargeException y por qué se guarda un id o una búsqueda en lugar de una lista.

Malentendidos a corregir: rotar el teléfono no provoca una "recomposición de la Activity", sino una recreación de la Activity: se destruye y se crea de nuevo, con una composition nueva. La recomposition es otra cosa: volver a ejecutar composables dentro de la misma composition cuando cambia un estado.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una nota en un post-it frente a una nota guardada en un cajón: el post-it se cae si cambiás de escritorio, la del cajón la recuperás), por qué una variable local no sirve como estado y cómo se combinan remember y mutableStateOf; después las keys; después la diferencia entre recomposition y recreación de la Activity y cómo rememberSaveable usa el Bundle; y cerrá con los Saver y el límite de tamaño.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
remember & rememberSaveable

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/03-jetpack-compose/remember-remembersaveable/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/03-jetpack-compose/recomposition-stability/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/recomposition/
https://aghmnl.github.io/senior-forge-codex/es/glosario/remember/
https://aghmnl.github.io/senior-forge-codex/es/glosario/remember-saveable/
https://aghmnl.github.io/senior-forge-codex/es/glosario/composition/
https://aghmnl.github.io/senior-forge-codex/es/glosario/activity/
https://aghmnl.github.io/senior-forge-codex/es/glosario/configuration-change/
https://aghmnl.github.io/senior-forge-codex/es/glosario/process-death/
https://aghmnl.github.io/senior-forge-codex/es/glosario/saved-instance-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/bundle/
https://aghmnl.github.io/senior-forge-codex/es/glosario/primitives/
https://aghmnl.github.io/senior-forge-codex/es/glosario/string/
https://aghmnl.github.io/senior-forge-codex/es/glosario/parcelable/
https://aghmnl.github.io/senior-forge-codex/es/glosario/parcelize/
https://aghmnl.github.io/senior-forge-codex/es/glosario/serializable/
https://aghmnl.github.io/senior-forge-codex/es/glosario/saver/
https://aghmnl.github.io/senior-forge-codex/es/glosario/list-saver/
https://aghmnl.github.io/senior-forge-codex/es/glosario/map-saver/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mutable-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/animatable/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel/
https://aghmnl.github.io/senior-forge-codex/es/glosario/transaction-too-large-exception/
https://aghmnl.github.io/senior-forge-codex/es/glosario/saved-state-handle/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lazy-column/
https://aghmnl.github.io/senior-forge-codex/es/glosario/remember-lazy-list-state/

**Fuentes oficiales (agregar cada una como fuente web)**
https://developer.android.com/develop/ui/compose/state
https://developer.android.com/develop/ui/compose/state-saving
https://developer.android.com/topic/libraries/architecture/saving-states
https://developer.android.com/topic/libraries/architecture/viewmodel/viewmodel-savedstate
https://developer.android.com/guide/components/activities/activity-lifecycle
https://developer.android.com/guide/topics/resources/runtime-changes
https://developer.android.com/guide/components/activities/parcelables-and-bundles

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: remember & rememberSaveable
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior, con buena intuición sobre el tiempo de vida.

Ya domina: la idea de que rememberSaveable sobrevive a la recreación de la Activity y remember no, y que rememberSaveable está pensado para valores chicos. Conviene partir de ahí y explicar el porqué.

Necesita explicación en profundidad, desde cero: por qué una variable local en un composable no funciona como estado (no es observable y se reinicia cada vez que la función vuelve a correr), y por qué hacen falta las dos piezas, MutableState para que Compose observe el cambio y remember para conservarlo entre recomposiciones; qué hacen las keys de remember, que recalculan el valor solo cuando cambian; el mecanismo de rememberSaveable, que guarda el valor en el saved instance state (un Bundle) y por eso también sobrevive a la muerte del proceso; qué tipos puede guardar el Bundle y cómo se resuelve un tipo propio con @Parcelize o un Saver (listSaver, mapSaver); y el límite de tamaño del Bundle, la TransactionTooLargeException y por qué se guarda un id o una búsqueda en lugar de una lista.

Malentendidos a corregir: rotar el teléfono no provoca una "recomposición de la Activity", sino una recreación de la Activity: se destruye y se crea de nuevo, con una composition nueva. La recomposition es otra cosa: volver a ejecutar composables dentro de la misma composition cuando cambia un estado.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una nota en un post-it frente a una nota guardada en un cajón: el post-it se cae si cambiás de escritorio, la del cajón la recuperás), por qué una variable local no sirve como estado y cómo se combinan remember y mutableStateOf; después las keys; después la diferencia entre recomposition y recreación de la Activity y cómo rememberSaveable usa el Bundle; y cerrá con los Saver y el límite de tamaño.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| State and Jetpack Compose | `remember`, `mutableStateOf`, `rememberSaveable` y los tipos que se pueden guardar. |
| Save UI state in Compose | Dónde guardar cada estado (composable o ViewModel) y cómo usar `rememberSaveable` y `SavedStateHandle`. |
| Save UI states | Comparación entre ViewModel, saved instance state y almacenamiento persistente, con el límite de tamaño. |
| Saved State module for ViewModel | `SavedStateHandle` y por qué el ViewModel solo no sobrevive a la muerte del proceso. |
| The activity lifecycle | Qué pasa con la Activity al rotar y cuando el sistema mata el proceso. |
| Handle configuration changes | Qué es un configuration change y por qué no conviene desactivarlo. |
| Parcelables and bundles | `Bundle`, `Parcelable` y la `TransactionTooLargeException`. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "remember & rememberSaveable", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. Adentro de un composable declarás `var count = 0`, y un botón hace `count++` en su `onClick`. ¿Qué ves en pantalla al tocar el botón, y por qué?
2. En `val filtered = remember(query) { allItems.filter { it.matches(query) } }`, ¿qué papel cumple `query` entre los paréntesis de `remember`?
3. Rotás el teléfono y la Activity se recrea. ¿Qué pasa con un valor guardado con `remember`? ¿Y con uno guardado con `rememberSaveable`?
4. Querés guardar con `rememberSaveable` una data class propia, `DateRange(start: LocalDate, end: LocalDate)`, que no es `Parcelable`. ¿Qué pasa, y cómo lo resolvés?
5. ¿Por qué no conviene guardar una lista de 5.000 tareas con `rememberSaveable`?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: el número no cambia; una variable local no es estado observable y se reinicia cuando la función vuelve a correr; hace falta remember { mutableStateOf(0) }. Junior: no ve el problema.
- P2 Senior: query es una key; el cálculo se cachea y solo se recalcula cuando query cambia. Junior: no sabe.
- P3 Senior: remember se pierde porque la Activity recreada arranca una composition nueva; rememberSaveable se restaura desde el saved instance state (Bundle), y también sobrevive a la muerte del proceso. Junior: cree que se comportan igual.
- P4 Senior: el Bundle no puede guardar ese tipo; se resuelve con @Parcelize o con un Saver (listSaver, mapSaver). Junior: no sabe.
- P5 Senior: el Bundle tiene un límite de tamaño (alrededor de 1 MB) y excederlo produce TransactionTooLargeException; se guarda un id y los datos se recargan de su fuente. Junior: no ve el problema.
```
