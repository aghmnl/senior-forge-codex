---
topic: "Scope Functions (let, run, apply, also, with)"
chapter: 01-kotlin-core
slug: scope-functions
lang: es
article: /es/01-kotlin-core/scope-functions/
diagnostic_date: 2026-10-12
---

# Notebook de estudio — Scope Functions (let, run, apply, also, with)

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. De las cinco scope functions, ¿cuáles te dan el objeto como `this` y cuáles como `it`?
2. ¿Qué devuelve `also`? ¿Y `let`? Dame un caso típico de uso de cada una.
3. ¿Cómo usarías `let` junto con `?.` para ejecutar un bloque solo cuando un valor no es null?
4. ¿Por qué anidar varias scope functions, una dentro de otra, se considera un antipatrón? ¿Qué harías en su lugar?
5. ¿Tiene algún costo de rendimiento usar scope functions en un bucle que corre miles de veces? ¿Por qué?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | Como **`this`** (receiver): `run`, `with`, `apply`. Como **`it`** (argumento): `let`, `also`. | Acierta algunas. | No sabe. |
| 2 | `also` devuelve **el mismo objeto** (efectos secundarios: loguear, cachear, sin alterar el flujo). `let` devuelve **el resultado de la lambda** (transformar un valor, sobre todo con `?.`). | Acierta una de las dos. | No sabe. |
| 3 | `valor?.let { ... }`: el safe call hace que el bloque corra **solo si `valor` no es null**, y adentro `it` ya es no-nullable. Se puede combinar con `?:` para el caso null. | Conoce la forma pero no explica que `it` es no-nullable. | No sabe. |
| 4 | Se pierde de vista **a qué objeto apunta `this` o `it`** en cada nivel, lo que causa errores sutiles y dificulta la lectura. En su lugar, **extraer el bloque interno a una función con nombre** o usar variables con nombre. | Dice que "es difícil de leer" sin explicar la confusión de `this`/`it`. | No sabe. |
| 5 | **No**: las cinco son funciones **`inline`**, así que la lambda se copia en el lugar de la llamada y no hay allocation de objetos ni presión sobre el Garbage Collector. | Intuye que no cuesta pero no sabe por qué. | No sabe. |

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
| 1 | Junior | "No sé". No distingue `this` de `it` entre las scope functions. |
| 2 | Junior | "No sé". No conoce qué devuelven `also` y `let`. |
| 3 | Junior | "No sé". No conoce el patrón `?.let { }`. |
| 4 | Junior | "No sé". No conoce el problema del anidamiento. |
| 5 | Junior | "No sé". No sabe que las scope functions son `inline`. |

**Nivel global: Junior** (0 Senior, 0 intermedias, 5 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de Higher-Order Functions & Lambdas, donde las scope functions aparecen como ejemplo de funciones de orden superior inline; conviene apoyarse en eso.

Necesita explicación en profundidad, desde cero: las dos diferencias que distinguen a let, run, with, apply y also (si el objeto llega como this o como it, y si devuelven el objeto o el resultado de la lambda); el uso típico de cada una (apply para configurar, also para efectos secundarios, let para transformar y para null safety, run y with para operar sobre un objeto y devolver un resultado); el patrón ?.let { } y por qué adentro el valor ya es no-nullable; por qué anidar scope functions confunde a qué objeto apunta this o it y conviene extraer funciones con nombre; y por qué no tienen costo de rendimiento (son inline).

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con una tabla mental de dos ejes (this o it; devuelve el objeto o el resultado) y analogías de la vida diaria para cada función, después el patrón ?.let, el antipatrón del anidamiento, y cerrá con por qué son gratis en rendimiento.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Scope Functions (let, run, apply, also, with)

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/scope-functions/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/higher-order-functions-lambdas/
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/null-safety-elvis-safe-calls/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/context-programming/
https://aghmnl.github.io/senior-forge-codex/es/glosario/receiver-type/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lambdas/
https://aghmnl.github.io/senior-forge-codex/es/glosario/data-transformation/
https://aghmnl.github.io/senior-forge-codex/es/glosario/scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/intent-signaling/
https://aghmnl.github.io/senior-forge-codex/es/glosario/syntax-sugar/
https://aghmnl.github.io/senior-forge-codex/es/glosario/single-responsibility-principle/
https://aghmnl.github.io/senior-forge-codex/es/glosario/inline-functions/
https://aghmnl.github.io/senior-forge-codex/es/glosario/allocations/
https://aghmnl.github.io/senior-forge-codex/es/glosario/garbage-collector/
https://aghmnl.github.io/senior-forge-codex/es/glosario/safe-call/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/scope-functions.html
https://kotlinlang.org/docs/null-safety.html
https://kotlinlang.org/docs/inline-functions.html

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Scope Functions (let, run, apply, also, with)
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de Higher-Order Functions & Lambdas, donde las scope functions aparecen como ejemplo de funciones de orden superior inline; conviene apoyarse en eso.

Necesita explicación en profundidad, desde cero: las dos diferencias que distinguen a let, run, with, apply y also (si el objeto llega como this o como it, y si devuelven el objeto o el resultado de la lambda); el uso típico de cada una (apply para configurar, also para efectos secundarios, let para transformar y para null safety, run y with para operar sobre un objeto y devolver un resultado); el patrón ?.let { } y por qué adentro el valor ya es no-nullable; por qué anidar scope functions confunde a qué objeto apunta this o it y conviene extraer funciones con nombre; y por qué no tienen costo de rendimiento (son inline).

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con una tabla mental de dos ejes (this o it; devuelve el objeto o el resultado) y analogías de la vida diaria para cada función, después el patrón ?.let, el antipatrón del anidamiento, y cerrá con por qué son gratis en rendimiento.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Scope functions | Las cinco funciones, cómo se referencian (`this`/`it`), qué devuelven y cuándo usar cada una. |
| Null safety | El safe call `?.` que se combina con `let`. |
| Inline functions | Por qué las scope functions no generan allocations. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Scope Functions (let, run, apply, also, with)", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. De las cinco scope functions, ¿cuáles te dan el objeto como `this` y cuáles como `it`?
2. ¿Qué devuelve `also`? ¿Y `let`? Dame un caso típico de uso de cada una.
3. ¿Cómo usarías `let` junto con `?.` para ejecutar un bloque solo cuando un valor no es null?
4. ¿Por qué anidar varias scope functions, una dentro de otra, se considera un antipatrón? ¿Qué harías en su lugar?
5. ¿Tiene algún costo de rendimiento usar scope functions en un bucle que corre miles de veces? ¿Por qué?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: this en run, with, apply; it en let, also. Junior: no sabe.
- P2 Senior: also devuelve el objeto (efectos secundarios); let devuelve el resultado de la lambda (transformar, null safety). Junior: no sabe.
- P3 Senior: valor?.let { } corre solo si no es null y adentro it es no-nullable. Junior: no sabe.
- P4 Senior: se pierde a qué apunta this/it; extraer funciones con nombre. Junior: no sabe.
- P5 Senior: no cuestan nada porque son inline. Junior: no sabe.
```
