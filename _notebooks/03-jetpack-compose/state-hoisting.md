---
topic: "State Hoisting"
chapter: 03-jetpack-compose
slug: state-hoisting
lang: es
article: /es/03-jetpack-compose/state-hoisting/
diagnostic_date: 2026-10-16
---

# Notebook de estudio — State Hoisting

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Qué diferencia hay entre un composable *stateful* y uno *stateless*?
2. Cuando elevás el estado de un componente, ¿qué dos parámetros lo reemplazan? ¿Cómo se llaman en un `TextField`?
3. ¿Qué significa la frase "el estado baja, los eventos suben"?
4. Una barra de búsqueda y la lista de resultados que está debajo necesitan la misma búsqueda. ¿Dónde debería vivir ese estado, y por qué?
5. ¿Por qué no conviene elevar *todo* el estado de una pantalla al ViewModel? Dame un ejemplo de estado que debería quedarse local.

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | **Stateful** crea y guarda su propio estado con `remember`: funciona solo, pero quien lo llama no puede leerlo ni cambiarlo. **Stateless** recibe el estado como parámetros: muestra lo que le dan e informa lo que hace el usuario, así que es reutilizable, previsualizable y testeable. | Acierta la idea pero no las consecuencias (reutilización, tests). | No sabe. |
| 2 | Un **valor** a mostrar y un **evento** para pedir el cambio: en `TextField`, **`value`** y **`onValueChange`**. El componente muestra el valor y llama al evento; el dueño decide. | Conoce uno de los dos o los nombres sin el rol. | No sabe. |
| 3 | Es el **unidirectional data flow**: el dueño pasa el estado **hacia abajo** como parámetros, y los hijos informan lo que pasó **hacia arriba** con lambdas de eventos. Los hijos nunca modifican el estado directamente; todo cambio pasa por el dueño. | Entiende la dirección pero no que el hijo no escribe el estado. | No sabe. |
| 4 | En su **ancestro común más bajo** (la pantalla que contiene a las dos, o su ViewModel): así hay **una sola fuente de verdad** y las dos leen el mismo valor. Si cada una tuviera su copia, se desincronizarían. | Dice "arriba" sin precisar el ancestro común ni la single source of truth. | No sabe. |
| 5 | Porque mezcla **detalles de UI** con estado de negocio, agranda el ViewModel y **recompone más** de lo necesario. Se eleva solo hasta quien lo lee o escribe. Ejemplos locales: si un dropdown está abierto, la posición del scroll, el estado de una animación. | Da un ejemplo pero no la razón, o al revés. | No sabe. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior a Senior; 3+ intermedias o mezcla a Intermedio; 3+ junior o "no sé" a Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-10-16

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Junior | "No sé". No distingue stateful de stateless. |
| 2 | Junior | "No sé". No conoce el patrón `value` / `onValueChange`. |
| 3 | Junior | "No sé". No conoce el unidirectional data flow a nivel de componente. |
| 4 | Junior | "No sé". No conoce la regla del ancestro común más bajo. |
| 5 | Junior | "No sé". No ve el costo de elevar todo al ViewModel. |

**Nivel global: Junior** (0 Senior, 0 intermedias, 5 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de remember & rememberSaveable y de UI State Modeling, así que conoce remember, mutableStateOf y la idea de un único estado en el ViewModel; conviene presentar el state hoisting como el puente entre los dos.

Necesita explicación en profundidad, desde cero: la diferencia entre un composable stateful y uno stateless; qué es el state hoisting y el patrón value / onValueChange (TextField, Checkbox, Switch); el unidirectional data flow a nivel de componente (el estado baja, los eventos suben); la regla de elevar hasta el ancestro común más bajo de quienes leen o escriben el estado, y los tres destinos (el propio composable con remember, un state holder como LazyListState, el ViewModel); los beneficios (single source of truth, reutilización, previews, tests); por qué no elevar todo al ViewModel; los componentes controlados y no controlados; y por qué pasar valores y lambdas en lugar de un ViewModel o un MutableState.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (un control remoto que no decide qué canal ver, solo le avisa al televisor qué botón se apretó), stateful frente a stateless y el patrón value / onValueChange, después hasta dónde elevar el estado, y cerrá con los componentes controlados y no controlados y por qué no pasar el ViewModel a los hijos.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
State Hoisting

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/03-jetpack-compose/state-hoisting/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/03-jetpack-compose/remember-remembersaveable/
https://aghmnl.github.io/senior-forge-codex/es/05-architecture/ui-state-modeling/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/remember/
https://aghmnl.github.io/senior-forge-codex/es/glosario/stateful-stateless/
https://aghmnl.github.io/senior-forge-codex/es/glosario/unidirectional-data-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/text-field/
https://aghmnl.github.io/senior-forge-codex/es/glosario/checkbox/
https://aghmnl.github.io/senior-forge-codex/es/glosario/switch/
https://aghmnl.github.io/senior-forge-codex/es/glosario/state-holder/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lazy-list-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel/
https://aghmnl.github.io/senior-forge-codex/es/glosario/configuration-change/
https://aghmnl.github.io/senior-forge-codex/es/glosario/single-source-of-truth/
https://aghmnl.github.io/senior-forge-codex/es/glosario/preview/
https://aghmnl.github.io/senior-forge-codex/es/glosario/design-system/
https://aghmnl.github.io/senior-forge-codex/es/glosario/controlled-uncontrolled/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lambdas/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mutable-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/event-handlers/
https://aghmnl.github.io/senior-forge-codex/es/glosario/recomposition/

**Fuentes oficiales (agregar cada una como fuente web)**
https://developer.android.com/develop/ui/compose/state-hoisting
https://developer.android.com/develop/ui/compose/state
https://developer.android.com/develop/ui/compose/architecture

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: State Hoisting
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de remember & rememberSaveable y de UI State Modeling, así que conoce remember, mutableStateOf y la idea de un único estado en el ViewModel; conviene presentar el state hoisting como el puente entre los dos.

Necesita explicación en profundidad, desde cero: la diferencia entre un composable stateful y uno stateless; qué es el state hoisting y el patrón value / onValueChange (TextField, Checkbox, Switch); el unidirectional data flow a nivel de componente (el estado baja, los eventos suben); la regla de elevar hasta el ancestro común más bajo de quienes leen o escriben el estado, y los tres destinos (el propio composable con remember, un state holder como LazyListState, el ViewModel); los beneficios (single source of truth, reutilización, previews, tests); por qué no elevar todo al ViewModel; los componentes controlados y no controlados; y por qué pasar valores y lambdas en lugar de un ViewModel o un MutableState.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (un control remoto que no decide qué canal ver, solo le avisa al televisor qué botón se apretó), stateful frente a stateless y el patrón value / onValueChange, después hasta dónde elevar el estado, y cerrá con los componentes controlados y no controlados y por qué no pasar el ViewModel a los hijos.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Where to hoist state | La regla del ancestro común más bajo, los destinos del estado y los state holders. |
| State and Jetpack Compose | Stateful frente a stateless y el patrón `value` / `onValueChange`. |
| Architecting your Compose UI | Unidirectional data flow: el estado baja y los eventos suben. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "State Hoisting", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Qué diferencia hay entre un composable *stateful* y uno *stateless*?
2. Cuando elevás el estado de un componente, ¿qué dos parámetros lo reemplazan? ¿Cómo se llaman en un `TextField`?
3. ¿Qué significa la frase "el estado baja, los eventos suben"?
4. Una barra de búsqueda y la lista de resultados que está debajo necesitan la misma búsqueda. ¿Dónde debería vivir ese estado, y por qué?
5. ¿Por qué no conviene elevar *todo* el estado de una pantalla al ViewModel? Dame un ejemplo de estado que debería quedarse local.
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: stateful guarda su estado con remember; stateless lo recibe como parámetros y es reutilizable y testeable. Junior: no sabe.
- P2 Senior: un valor y un evento; value y onValueChange. Junior: no sabe.
- P3 Senior: unidirectional data flow; el dueño pasa el estado hacia abajo y los hijos informan eventos hacia arriba sin escribirlo. Junior: no sabe.
- P4 Senior: en el ancestro común más bajo, para tener una single source of truth. Junior: no sabe.
- P5 Senior: mezcla UI con negocio y recompone de más; local: dropdown abierto, scroll, animación. Junior: no sabe.
```
