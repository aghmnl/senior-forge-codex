---
topic: "Higher-Order Functions & Lambdas"
chapter: 01-kotlin-core
slug: higher-order-functions-lambdas
lang: es
article: /es/01-kotlin-core/higher-order-functions-lambdas/
diagnostic_date: 2026-10-12
---

# Notebook de estudio — Higher-Order Functions & Lambdas

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Qué es una *función de orden superior*? Dame un ejemplo de alguna que uses de la librería estándar de Kotlin.
2. ¿Qué describe el tipo `(Task) -> Boolean`? ¿Y en qué cambia si se escribe `Task.() -> Boolean`?
3. Pasás una lambda a una función que **no** es `inline`. ¿Qué crea el compilador para esa lambda, y por qué podría importar en un bucle que corre miles de veces?
4. ¿Qué es un *non-local return* dentro de una lambda, y en qué tipo de funciones está permitido?
5. En una función `inline`, ¿para qué sirven los modificadores `crossinline` y `noinline` sobre un parámetro lambda?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | Una función que **recibe otra función como parámetro o la devuelve**. Ejemplos: `map`, `filter`, `forEach`, `let`, `apply`. | Da un ejemplo pero no la definición, o al revés. | No sabe. |
| 2 | `(Task) -> Boolean` es un **function type**: una función que recibe un `Task` y devuelve un `Boolean` (un predicado). `Task.() -> Boolean` es un function type **con receiver**: adentro de la lambda, `this` es el `Task`, la base de los DSLs y de `apply`/`with`. | Entiende el primero pero no el receiver. | No sabe. |
| 3 | Una **instancia de un objeto función** (una clase `Function1`, etc.), y si captura variables, una nueva por llamada. En un bucle caliente son **allocations** que presionan al Garbage Collector; `inline` las elimina copiando el cuerpo en el lugar de la llamada. | Sabe que "crea algo" o que `inline` es más rápido, pero no explica la allocation. | No sabe. |
| 4 | Un `return` adentro de la lambda que **sale de la función que la contiene**, no solo de la lambda. Solo se permite cuando la lambda se pasa a una función **`inline`**, porque su código se copia en el lugar de la llamada. | Sabe qué es pero no que requiere `inline`. | No sabe. |
| 5 | **`crossinline`**: la lambda se inlinea pero **prohíbe el non-local return**, necesario cuando se llama desde otro contexto (otro objeto, otro hilo). **`noinline`**: esa lambda **no se inlinea** y queda como objeto, para poder guardarla o pasarla a otra función. | Conoce uno de los dos. | No los conoce. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior a Senior; 3+ intermedias o mezcla a Intermedio; 3+ junior o "no sé" a Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-10-12

> El artículo existía desde el 2026-09-02 y el learner probablemente ya lo había leído; el diagnóstico se tomó al generar el notebook, sin mirarlo.

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Junior | "No sé". No conoce la definición de función de orden superior. |
| 2 | Junior | "No sé". No distingue un function type de uno con receiver. |
| 3 | Junior | "No sé". No conoce la allocation de la lambda ni el efecto de `inline`. |
| 4 | Junior | "No sé". No conoce los non-local returns. |
| 5 | Junior | "No sé". No conoce `crossinline` ni `noinline`. |

**Nivel global: Junior** (0 Senior, 0 intermedias, 5 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Usa map, filter y let a diario, así que conviene partir de esos ejemplos conocidos para mostrar que son funciones de orden superior.

Necesita explicación en profundidad, desde cero: qué es una función de orden superior (recibe o devuelve funciones) y que las funciones son valores en Kotlin; cómo leer un function type como (Task) -> Boolean y en qué cambia uno con receiver, Task.() -> Boolean, base de los DSLs y de apply/with; qué crea el compilador para una lambda que no se inlinea (un objeto función, una allocation por llamada si captura variables) y por qué importa en bucles calientes y para el Garbage Collector; cómo inline elimina esa allocation copiando el cuerpo y permite non-local returns; para qué sirven crossinline y noinline; y por qué inline no conviene en todas partes (code bloat).

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una receta que recibe como ingrediente otra receta), qué son las funciones de orden superior y los function types, después el costo de las lambdas y cómo inline lo elimina, y cerrá con non-local returns, crossinline, noinline y el code bloat.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Higher-Order Functions & Lambdas

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/higher-order-functions-lambdas/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/scope-functions/
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/extension-functions/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/lambdas/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collections/
https://aghmnl.github.io/senior-forge-codex/es/glosario/jetpack-compose/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dsl/
https://aghmnl.github.io/senior-forge-codex/es/glosario/runtime/
https://aghmnl.github.io/senior-forge-codex/es/glosario/inline-functions/
https://aghmnl.github.io/senior-forge-codex/es/glosario/garbage-collector/
https://aghmnl.github.io/senior-forge-codex/es/glosario/bytecode/
https://aghmnl.github.io/senior-forge-codex/es/glosario/allocations/
https://aghmnl.github.io/senior-forge-codex/es/glosario/crossinline/
https://aghmnl.github.io/senior-forge-codex/es/glosario/noinline/
https://aghmnl.github.io/senior-forge-codex/es/glosario/callbacks/
https://aghmnl.github.io/senior-forge-codex/es/glosario/receiver-type/
https://aghmnl.github.io/senior-forge-codex/es/glosario/hilt/
https://aghmnl.github.io/senior-forge-codex/es/glosario/round-trip/
https://aghmnl.github.io/senior-forge-codex/es/glosario/code-bloat/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/lambdas.html
https://kotlinlang.org/docs/inline-functions.html
https://kotlinlang.org/docs/type-safe-builders.html
https://kotlinlang.org/docs/collection-operations.html

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Higher-Order Functions & Lambdas
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Usa map, filter y let a diario, así que conviene partir de esos ejemplos conocidos para mostrar que son funciones de orden superior.

Necesita explicación en profundidad, desde cero: qué es una función de orden superior (recibe o devuelve funciones) y que las funciones son valores en Kotlin; cómo leer un function type como (Task) -> Boolean y en qué cambia uno con receiver, Task.() -> Boolean, base de los DSLs y de apply/with; qué crea el compilador para una lambda que no se inlinea (un objeto función, una allocation por llamada si captura variables) y por qué importa en bucles calientes y para el Garbage Collector; cómo inline elimina esa allocation copiando el cuerpo y permite non-local returns; para qué sirven crossinline y noinline; y por qué inline no conviene en todas partes (code bloat).

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una receta que recibe como ingrediente otra receta), qué son las funciones de orden superior y los function types, después el costo de las lambdas y cómo inline lo elimina, y cerrá con non-local returns, crossinline, noinline y el code bloat.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Higher-order functions and lambdas | Function types, lambdas, receivers y cómo se pasan y devuelven funciones. |
| Inline functions | `inline`, `noinline`, `crossinline`, non-local returns y `reified`. |
| Type-safe builders | Cómo los function types con receiver construyen DSLs. |
| Collection operations | Las funciones de orden superior más usadas: `map`, `filter`, `count`. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Higher-Order Functions & Lambdas", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Qué es una *función de orden superior*? Dame un ejemplo de alguna que uses de la librería estándar de Kotlin.
2. ¿Qué describe el tipo `(Task) -> Boolean`? ¿Y en qué cambia si se escribe `Task.() -> Boolean`?
3. Pasás una lambda a una función que **no** es `inline`. ¿Qué crea el compilador para esa lambda, y por qué podría importar en un bucle que corre miles de veces?
4. ¿Qué es un *non-local return* dentro de una lambda, y en qué tipo de funciones está permitido?
5. En una función `inline`, ¿para qué sirven los modificadores `crossinline` y `noinline` sobre un parámetro lambda?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: recibe o devuelve funciones; ejemplos map, filter, let. Junior: no sabe.
- P2 Senior: (Task) -> Boolean es un function type (predicado); Task.() -> Boolean tiene receiver y this es el Task. Junior: no sabe.
- P3 Senior: un objeto función, una allocation por llamada si captura; presiona al GC; inline la elimina. Junior: no sabe.
- P4 Senior: return que sale de la función contenedora; solo en lambdas pasadas a funciones inline. Junior: no sabe.
- P5 Senior: crossinline prohíbe non-local return; noinline deja la lambda como objeto para guardarla o pasarla. Junior: no los conoce.
```
