---
topic: "Delegated Properties (by lazy, by viewModels)"
chapter: 01-kotlin-core
slug: delegated-properties
lang: es
article: /es/01-kotlin-core/delegated-properties/
diagnostic_date: 2026-10-12
---

# Notebook de estudio — Delegated Properties (by lazy, by viewModels)

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. En `val x by Algo()`, ¿qué hace la palabra clave `by`? ¿Qué tiene que tener `Algo` para que eso compile?
2. ¿Para qué sirven los delegados `Delegates.observable` y `Delegates.vetoable` de la librería estándar?
3. En Compose, ¿qué te ahorra escribir `var count by remember { mutableStateOf(0) }` en lugar de `val count = remember { mutableStateOf(0) }`?
4. En un Fragment, ¿qué diferencia hay entre obtener el ViewModel con `by viewModels()` y con `by activityViewModels()`?
5. Cada propiedad `by lazy` o `by mutableStateOf()` crea un objeto extra. ¿En qué situación ese costo podría importar?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | `by` **delega** el acceso a la propiedad en otro objeto: cada lectura se convierte en una llamada a su `getValue` (y cada escritura a `setValue`, si es `var`). `Algo` tiene que proveer **`operator fun getValue(thisRef, property)`** (y `setValue` para `var`); no hace falta implementar ninguna interfaz. | Sabe que delega pero no qué operadores hacen falta. | No sabe. |
| 2 | `observable` ejecuta un callback **después** de cada asignación (con el valor viejo y el nuevo). `vetoable` ejecuta un callback **antes** y puede **rechazar** el nuevo valor devolviendo `false`. | Conoce uno de los dos. | No los conoce. |
| 3 | Evita escribir **`count.value`** en cada lectura y escritura: `by` desenvuelve el `MutableState`. Sigue siendo estado observable: cada escritura dispara la recomposition de quienes lo leen. | Sabe que es más corto pero no que sigue siendo el mismo `MutableState`. | No sabe. |
| 4 | `viewModels()` lo scopea al **Fragment** (cada Fragment tiene el suyo). `activityViewModels()` lo scopea a la **Activity**, así que **varios Fragments comparten la misma instancia**. Define cuánto vive y quién lo comparte. | Sabe que uno es de la Activity pero no la consecuencia de compartirlo. | No sabe. |
| 5 | En **hot paths**: objetos creados en grandes cantidades (por ejemplo, ítems de una lista enorme o bucles), donde cada delegado es una allocation más en el heap que presiona al Garbage Collector. Ahí un campo directo puede ser mejor. | Intuye que importa "cuando hay muchos" sin hablar de allocations. | No sabe. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior a Senior; 3+ intermedias o mezcla a Intermedio; 3+ junior o "no sé" a Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-10-12

> El artículo existía desde el 2026-09-03 y el learner probablemente ya lo había leído; el diagnóstico se tomó al generar el notebook, sin mirarlo.

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Junior | "No sé". No conoce el mecanismo de `by` ni los operadores `getValue`/`setValue`. |
| 2 | Junior | "No sé". No conoce `observable` ni `vetoable`. |
| 3 | Junior | "No sé". No relaciona `by` con desenvolver `.value` de un `MutableState`. |
| 4 | Junior | "No sé". No distingue el scope de `viewModels()` y `activityViewModels()`. |
| 5 | Junior | "No sé". No conoce el costo de allocation de los delegados. |

**Nivel global: Junior** (0 Senior, 0 intermedias, 5 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de Lateinit vs Lazy, así que by lazy es el ejemplo natural para presentar la delegación en general. También estudió remember y MutableState en Compose.

Necesita explicación en profundidad, desde cero: qué hace la palabra clave by (cada lectura llama a getValue y cada escritura a setValue del delegado) y que basta con proveer esos operadores, sin implementar una interfaz; los delegados de la librería estándar (lazy, observable, vetoable, notNull y la delegación a un Map); por qué by remember { mutableStateOf() } evita escribir .value y sigue siendo estado observable; la diferencia entre by viewModels() y by activityViewModels() (scope del Fragment frente a la Activity, y ViewModel compartido entre Fragments); y el costo de allocation de cada delegado en hot paths.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (un apoderado que atiende en nombre de otra persona), cómo funciona by, después los delegados de la librería estándar, la delegación en Compose y en los ViewModels, y cerrá con el costo de allocation.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Delegated Properties (by lazy, by viewModels)

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/delegated-properties/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/lateinit-vs-lazy/
https://aghmnl.github.io/senior-forge-codex/es/03-jetpack-compose/remember-remembersaveable/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/backing-field/
https://aghmnl.github.io/senior-forge-codex/es/glosario/keyword/
https://aghmnl.github.io/senior-forge-codex/es/glosario/bytecode/
https://aghmnl.github.io/senior-forge-codex/es/glosario/kproperty/
https://aghmnl.github.io/senior-forge-codex/es/glosario/runtime/
https://aghmnl.github.io/senior-forge-codex/es/glosario/type-inference/
https://aghmnl.github.io/senior-forge-codex/es/glosario/standard-library/
https://aghmnl.github.io/senior-forge-codex/es/glosario/primitives/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lifecycle-aware/
https://aghmnl.github.io/senior-forge-codex/es/glosario/hilt/
https://aghmnl.github.io/senior-forge-codex/es/glosario/jetpack-compose/
https://aghmnl.github.io/senior-forge-codex/es/glosario/composable/
https://aghmnl.github.io/senior-forge-codex/es/glosario/stable/
https://aghmnl.github.io/senior-forge-codex/es/glosario/observable-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/snapshot-system/
https://aghmnl.github.io/senior-forge-codex/es/glosario/stateflow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lifecycle-event/
https://aghmnl.github.io/senior-forge-codex/es/glosario/property-delegate/
https://aghmnl.github.io/senior-forge-codex/es/glosario/type-safety/
https://aghmnl.github.io/senior-forge-codex/es/glosario/operator-overloading/
https://aghmnl.github.io/senior-forge-codex/es/glosario/compile-time/
https://aghmnl.github.io/senior-forge-codex/es/glosario/by-delegation/
https://aghmnl.github.io/senior-forge-codex/es/glosario/syntax-sugar/
https://aghmnl.github.io/senior-forge-codex/es/glosario/state-holder/
https://aghmnl.github.io/senior-forge-codex/es/glosario/heap/
https://aghmnl.github.io/senior-forge-codex/es/glosario/hot-loops/
https://aghmnl.github.io/senior-forge-codex/es/glosario/allocations/
https://aghmnl.github.io/senior-forge-codex/es/glosario/overhead/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel-store/
https://aghmnl.github.io/senior-forge-codex/es/glosario/back-stack/
https://aghmnl.github.io/senior-forge-codex/es/glosario/navigation-component/
https://aghmnl.github.io/senior-forge-codex/es/glosario/slot-table/
https://aghmnl.github.io/senior-forge-codex/es/glosario/composition-lifetime/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/delegated-properties.html
https://kotlinlang.org/docs/delegation.html
https://developer.android.com/topic/libraries/architecture/viewmodel/viewmodel-apis
https://developer.android.com/develop/ui/compose/state

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Delegated Properties (by lazy, by viewModels)
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de Lateinit vs Lazy, así que by lazy es el ejemplo natural para presentar la delegación en general. También estudió remember y MutableState en Compose.

Necesita explicación en profundidad, desde cero: qué hace la palabra clave by (cada lectura llama a getValue y cada escritura a setValue del delegado) y que basta con proveer esos operadores, sin implementar una interfaz; los delegados de la librería estándar (lazy, observable, vetoable, notNull y la delegación a un Map); por qué by remember { mutableStateOf() } evita escribir .value y sigue siendo estado observable; la diferencia entre by viewModels() y by activityViewModels() (scope del Fragment frente a la Activity, y ViewModel compartido entre Fragments); y el costo de allocation de cada delegado en hot paths.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (un apoderado que atiende en nombre de otra persona), cómo funciona by, después los delegados de la librería estándar, la delegación en Compose y en los ViewModels, y cerrá con el costo de allocation.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Delegated properties | Cómo funciona `by`, `getValue`/`setValue`, `lazy`, `observable`, `vetoable` y la delegación a un Map. |
| Delegation | La delegación de interfaces con `by`, el otro uso de la misma palabra clave. |
| ViewModel APIs cheatsheet | `viewModels()`, `activityViewModels()` y los scopes de un ViewModel. |
| State and Jetpack Compose | `by remember { mutableStateOf() }` y el estado observable en Compose. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Delegated Properties (by lazy, by viewModels)", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. En `val x by Algo()`, ¿qué hace la palabra clave `by`? ¿Qué tiene que tener `Algo` para que eso compile?
2. ¿Para qué sirven los delegados `Delegates.observable` y `Delegates.vetoable` de la librería estándar?
3. En Compose, ¿qué te ahorra escribir `var count by remember { mutableStateOf(0) }` en lugar de `val count = remember { mutableStateOf(0) }`?
4. En un Fragment, ¿qué diferencia hay entre obtener el ViewModel con `by viewModels()` y con `by activityViewModels()`?
5. Cada propiedad `by lazy` o `by mutableStateOf()` crea un objeto extra. ¿En qué situación ese costo podría importar?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: by delega cada acceso a getValue/setValue del delegado; basta con esos operadores. Junior: no sabe.
- P2 Senior: observable ejecuta un callback después de asignar; vetoable antes y puede rechazar el valor. Junior: no los conoce.
- P3 Senior: evita escribir .value; sigue siendo el mismo MutableState observable. Junior: no sabe.
- P4 Senior: viewModels() scopea al Fragment; activityViewModels() a la Activity, compartido entre Fragments. Junior: no sabe.
- P5 Senior: en hot paths, cada delegado es una allocation más que presiona al GC. Junior: no sabe.
```
