---
topic: "Flow (Cold Streams)"
chapter: 02-coroutines-flow
slug: flow-cold-streams
lang: es
article: /es/02-coroutines-flow/flow-cold-streams/
diagnostic_date: 2026-09-23
---

# Notebook de estudio — Flow (Cold Streams)

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Qué significa que un `Flow` sea "cold"? Si escribís `val f = repository.getTasks().map { ... }` y no hacés nada más, ¿qué se ejecutó?
2. Un repositorio expone `getTasks(): Flow<List<Task>>` respaldado por Room, y dos pantallas distintas lo colectan al mismo tiempo. ¿Cuántas queries corren contra la base de datos? ¿Por qué?
3. ¿Qué diferencia hay entre un operador intermedio (`map`, `filter`, `combine`) y uno terminal (`collect`, `first`, `toList`)? ¿Cuál de los dos hace que el flow empiece a producir valores?
4. Tenés `presetRepository.getAll(): Flow<List<Preset>>`. En un use case de limpieza usás `.first()`; en un ViewModel usás `.collect { }`. ¿Qué hace cada uno con el productor, y qué se rompe si los intercambiás?
5. Un `Flow` cold no tiene ciclo de vida propio. ¿Qué determina cuánto vive y cuándo se cancela? ¿Qué pasa si lo colectás en una `Activity` sin `repeatOnLifecycle`?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | Cold significa que el flow es una *descripción*, no un pipeline corriendo. En esa línea no se ejecutó **nada**: no corrió ninguna query, no se emitió ningún valor, solo se alocó un objeto que describe el mapeo. El productor arranca recién con un operador terminal. Menciona que por eso llamar a una función que devuelve `Flow` no tiene efectos secundarios. | Sabe que "no se ejecuta hasta colectar" pero no articula que el `map` tampoco corrió ni la consecuencia de que no haya efectos secundarios. | Cree que la query ya corrió, o que `map` transforma algo en ese momento. |
| 2 | **Dos.** Cada colector obtiene su propia ejecución desde cero: dos queries independientes y dos observadores de Room, y cada cambio de tabla vuelve a correr las dos. El trabajo se duplica, no se comparte. La solución no es colectar menos sino compartir una ejecución upstream con `shareIn`/`stateIn`, que convierte el flow cold en hot con un productor único. | Sabe que "cada colector ejecuta el flow" pero no lo cuantifica ni conoce `shareIn`/`stateIn` como respuesta. | Responde "una", asumiendo que el flow se comparte. |
| 3 | Los intermedios son declarativos y lazy: cada uno devuelve un `Flow` nuevo que envuelve al anterior y no ejecuta nada — igual que los operadores de `Sequence`. Los terminales son suspend functions que arrancan el productor y necesitan un scope donde correr. **Solo el terminal dispara la producción.** Menciona que por eso una cadena larga de operadores sin terminal es código muerto silencioso. | Distingue los dos grupos pero no explica que los intermedios devuelven un Flow nuevo ni que los terminales son suspend. | No conoce la distinción. |
| 4 | `first()` suspende hasta la primera emisión, devuelve ese valor y **cancela el productor**, así que la suspend function completa — es una foto de una fuente viva, justo lo que necesita un cleanup. `collect` nunca completa por sí solo: sigue recibiendo cada re-emisión mientras viva el scope, y va en el ViewModel. Intercambiarlos: `first()` donde querías observar muestra datos correctos una vez y queda obsoleto **en silencio**, sin error ni log; `collect` donde querías una foto suspende para siempre y el llamador queda colgado. | Sabe que uno toma un valor y el otro observa, pero no menciona que `first()` cancela el productor ni describe las dos formas de fallar. | No conoce `first()` o cree que son intercambiables. |
| 5 | Vive exactamente lo que vive la coroutine que lo colecta: cancelás el scope y el productor se cancela en su próximo suspension point. Colectar en `viewModelScope` lo ata al ViewModel, que suele ser correcto. En una `Activity` sin `repeatOnLifecycle`, el colector sigue vivo con la pantalla en background: se siguen corriendo queries y actualizando UI invisible, gastando batería y CPU, y es un bug clásico. | Sabe que "depende del scope" pero no menciona el suspension point ni el problema concreto de background sin `repeatOnLifecycle`. | Cree que el flow se detiene solo, o que tiene ciclo de vida propio. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior a Senior; 3+ intermedias o mezcla a Intermedio; 3+ junior o "no sé" a Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-09-23

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Junior | "No sé". No conoce el modelo cold ni que declarar el flow con sus operadores no ejecuta nada. |
| 2 | Junior | "No sé". No conoce la consecuencia de que cada colector ejecute su propia copia del productor. |
| 3 | Junior | "No sé". No distingue operadores intermedios de terminales. |
| 4 | Junior | "No sé". No conoce el efecto de `first()` sobre el productor ni las dos formas de fallar al intercambiarlos. |
| 5 | Junior | "No sé". No conoce la relación entre la vida del flow y el scope que lo colecta. |

**Nivel global: Junior** (5 "no sé"). Tema a estudiar íntegramente desde cero.

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: nada que el notebook pueda dar por sabido de este tema. Respondió "no sé" a las cinco preguntas. De los temas ya estudiados del capítulo II se sabe que conoce las suspend functions, los dispatchers, la main-safety y, del tema anterior, que flowOn actúa sobre el upstream de un Flow — así que el vocabulario de Flow no le es totalmente ajeno aunque el modelo cold todavía no esté.

Necesita explicación en profundidad, desde cero: qué significa que un Flow sea cold — que es una descripción y no un pipeline corriendo, y que declararlo junto con sus operadores no ejecuta absolutamente nada; la distinción entre operadores intermedios, que son lazy y devuelven un Flow nuevo que envuelve al anterior, y operadores terminales, que son suspend functions y son los únicos que arrancan al productor; la consecuencia central de ser cold, que cada colector obtiene su propia ejecución desde cero, con el caso concreto de dos pantallas colectando un flow respaldado por Room y produciendo dos queries y dos observadores en vez de compartir uno, y la mención de que shareIn y stateIn existen para resolver eso; la elección del operador terminal como decisión de diseño, con first que toma un valor y cancela el productor frente a collect que observa mientras viva el scope, y las dos formas distintas de fallar al intercambiarlos — datos obsoletos en silencio en un caso, una coroutine que nunca retorna en el otro; y la vida de un flow cold, que es la de la coroutine que lo colecta, con la cancelación en el próximo suspension point y el problema práctico de colectar en una Activity sin repeatOnLifecycle.

Malentendidos a corregir: ninguno detectado (no hubo respuestas incorrectas, solo ausencia de respuesta).

Instrucción para el Audio Overview: explicá todo desde cero, con analogías, en este orden: primero la idea de receta contra pipeline corriendo, que es qué significa cold; después operadores intermedios contra terminales y quién dispara la producción; después la consecuencia de que cada colector ejecuta su propia copia, con el ejemplo de las dos pantallas y las dos queries; y por último la elección entre first y collect y la vida del flow atada al scope que lo colecta. No des nada por sabido.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Flow (Cold Streams)

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/flow-cold-streams/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/emit/
https://aghmnl.github.io/senior-forge-codex/es/glosario/callbacks/
https://aghmnl.github.io/senior-forge-codex/es/glosario/combine/
https://aghmnl.github.io/senior-forge-codex/es/glosario/flow-on/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sequences/
https://aghmnl.github.io/senior-forge-codex/es/glosario/terminal-operations/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collect/
https://aghmnl.github.io/senior-forge-codex/es/glosario/first/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspend-functions/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutine-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/stateflow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/backpressure/
https://aghmnl.github.io/senior-forge-codex/es/glosario/room/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspension-point/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/buffer/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dispatcher/
https://aghmnl.github.io/senior-forge-codex/es/glosario/downstream/
https://aghmnl.github.io/senior-forge-codex/es/glosario/catch/
https://aghmnl.github.io/senior-forge-codex/es/glosario/upstream/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/flow.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-flow/
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/collect.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/first.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/combine.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/callback-flow.html
https://developer.android.com/kotlin/flow
https://developer.android.com/topic/architecture/data-layer
https://developer.android.com/training/data-storage/room/async-queries
https://developer.android.com/topic/libraries/architecture/coroutines
https://developer.android.com/kotlin/flow/test

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Flow (Cold Streams)
2. Agregá el artículo principal como fuente web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: nada que el notebook pueda dar por sabido de este tema. Respondió "no sé" a las cinco preguntas. De los temas ya estudiados del capítulo II se sabe que conoce las suspend functions, los dispatchers, la main-safety y, del tema anterior, que flowOn actúa sobre el upstream de un Flow — así que el vocabulario de Flow no le es totalmente ajeno aunque el modelo cold todavía no esté.

Necesita explicación en profundidad, desde cero: qué significa que un Flow sea cold — que es una descripción y no un pipeline corriendo, y que declararlo junto con sus operadores no ejecuta absolutamente nada; la distinción entre operadores intermedios, que son lazy y devuelven un Flow nuevo que envuelve al anterior, y operadores terminales, que son suspend functions y son los únicos que arrancan al productor; la consecuencia central de ser cold, que cada colector obtiene su propia ejecución desde cero, con el caso concreto de dos pantallas colectando un flow respaldado por Room y produciendo dos queries y dos observadores en vez de compartir uno, y la mención de que shareIn y stateIn existen para resolver eso; la elección del operador terminal como decisión de diseño, con first que toma un valor y cancela el productor frente a collect que observa mientras viva el scope, y las dos formas distintas de fallar al intercambiarlos — datos obsoletos en silencio en un caso, una coroutine que nunca retorna en el otro; y la vida de un flow cold, que es la de la coroutine que lo colecta, con la cancelación en el próximo suspension point y el problema práctico de colectar en una Activity sin repeatOnLifecycle.

Malentendidos a corregir: ninguno detectado (no hubo respuestas incorrectas, solo ausencia de respuesta).

Instrucción para el Audio Overview: explicá todo desde cero, con analogías, en este orden: primero la idea de receta contra pipeline corriendo, que es qué significa cold; después operadores intermedios contra terminales y quién dispara la producción; después la consecuencia de que cada colector ejecuta su propia copia, con el ejemplo de las dos pantallas y las dos queries; y por último la elección entre first y collect y la vida del flow atada al scope que lo colecta. No des nada por sabido.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Asynchronous Flow | La referencia completa: builders, operadores intermedios y terminales, la naturaleza cold, secuencialidad y backpressure. |
| `Flow` (API) | El contrato de la interfaz: una sola función, `collect`, y qué implica que todo lo demás sea una extensión sobre ella. |
| `collect` (API) | El operador terminal canónico y qué significa que sea una suspend function. |
| `first` (API) | El contrato exacto: suspende hasta la primera emisión, cancela el productor y lanza si el flow completa vacío. |
| `combine` (API) | Cómo se fusionan varios flows con el último valor de cada uno, y por qué espera a que todos emitan. |
| `callbackFlow` (API) | El puente desde una API de callbacks hacia un flow, con `awaitClose` para liberar el listener. |
| Kotlin flows on Android | La guía oficial: productor, intermediarios y consumidor, y dónde vive cada uno en la arquitectura. |
| Data layer | Por qué un repositorio expone streams sin ser dueño de un scope ni de un ciclo de vida. |
| Write asynchronous DAO queries | Cómo Room devuelve un `Flow` que re-emite ante cada cambio de tabla. |
| Use Kotlin coroutines with lifecycle-aware components | `repeatOnLifecycle` y `flowWithLifecycle`: cómo atar la colección al ciclo de vida de la pantalla. |
| Testing Kotlin flows | Cómo se testea un flow cold de forma determinista, incluida la colección en un `TestScope`. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Flow (Cold Streams)", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Qué significa que un `Flow` sea "cold"? Si escribís `val f = repository.getTasks().map { ... }` y no hacés nada más, ¿qué se ejecutó?
2. Un repositorio expone `getTasks(): Flow<List<Task>>` respaldado por Room, y dos pantallas distintas lo colectan al mismo tiempo. ¿Cuántas queries corren contra la base de datos? ¿Por qué?
3. ¿Qué diferencia hay entre un operador intermedio (`map`, `filter`, `combine`) y uno terminal (`collect`, `first`, `toList`)? ¿Cuál de los dos hace que el flow empiece a producir valores?
4. Tenés `presetRepository.getAll(): Flow<List<Preset>>`. En un use case de limpieza usás `.first()`; en un ViewModel usás `.collect { }`. ¿Qué hace cada uno con el productor, y qué se rompe si los intercambiás?
5. Un `Flow` cold no tiene ciclo de vida propio. ¿Qué determina cuánto vive y cuándo se cancela? ¿Qué pasa si lo colectás en una `Activity` sin `repeatOnLifecycle`?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: cold significa que el flow es una descripción; en esa línea no se ejecutó nada, ni la query ni el map. Junior: cree que la query ya corrió.
- P2 Senior: dos queries y dos observadores, porque cada colector ejecuta su propia copia; shareIn/stateIn comparten una sola ejecución. Junior: responde una.
- P3 Senior: los intermedios son lazy y devuelven un Flow nuevo; los terminales son suspend functions y son los únicos que arrancan al productor. Junior: no conoce la distinción.
- P4 Senior: first toma un valor y cancela el productor, collect observa mientras viva el scope; intercambiarlos da datos obsoletos en silencio o una coroutine que nunca retorna. Intermedio: no menciona la cancelación del productor.
- P5 Senior: vive lo que vive la coroutine que lo colecta y se cancela en el próximo suspension point; en una Activity sin repeatOnLifecycle el colector sigue corriendo en background. Junior: cree que se detiene solo.
```
