---
topic: "Generics: Variance & Reification (in, out, reified)"
chapter: 01-kotlin-core
slug: generics-variance-reification
lang: es
article: /es/01-kotlin-core/generics-variance-reification/
diagnostic_date: 2026-10-13
---

# Notebook de estudio — Generics: Variance & Reification (in, out, reified)

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. Si `String` es subtipo de `Any`, ¿`MutableList<String>` es subtipo de `MutableList<Any>`? ¿Y `List<String>` de `List<Any>`? ¿Por qué la diferencia?
2. ¿Qué significan `out T` e `in T` en la declaración de una clase genérica? ¿Cómo sabés cuál corresponde?
3. ¿Por qué no podés escribir `if (value is T)` en una función genérica común? ¿Qué es el *type erasure*?
4. ¿Qué significa `ReorderState<*>`? ¿Qué podés leer de ahí y qué no podés escribir?
5. En una función `fun <T> printAll(items: List<T>)`, ¿puede `T` ser un tipo nullable como `String?`? ¿Cómo lo impedirías?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | `MutableList<String>` **no** es subtipo de `MutableList<Any>` (es **invariante**: si lo fuera, se podría agregar un `Int` a una lista de `String`). `List<String>` **sí** es subtipo de `List<Any>` porque `List` es **covariante** (`List<out E>`): solo se lee, nunca se agrega. | Acierta los resultados pero no explica por qué. | No sabe. |
| 2 | `out T` (**covarianza**): `T` solo aparece en posiciones de salida (tipos de retorno); la clase **produce** `T`. `in T` (**contravarianza**): `T` solo aparece en parámetros; la clase **consume** `T`. Regla de posición: si aparece en los dos lados, queda invariante. | Conoce los nombres pero no la regla de posición. | No sabe. |
| 3 | Por el **type erasure**: en la JVM el argumento genérico se borra del bytecode, así que en Runtime `T` no existe y no hay contra qué comparar. Se resuelve con una función **`inline`** con **`reified T`**, que copia el cuerpo en cada llamada con el tipo concreto. | Sabe que "el tipo se pierde" pero no conoce `reified`. | No sabe. |
| 4 | Es una **star projection**: "algún tipo concreto que no conozco". Las lecturas devuelven el upper bound (`Any?`) y las **escrituras quedan prohibidas**, porque no se sabe qué tipo aceptaría. Es el reemplazo seguro de los raw types de Java. | Sabe que es "cualquier tipo" pero no las restricciones de lectura y escritura. | No sabe. |
| 5 | **Sí**: sin bound, `T` es implícitamente `Any?`, así que admite nullables. Se impide con un **upper bound**: `fun <T : Any> printAll(...)`. | Sabe que admite nullables pero no cómo impedirlo. | No sabe. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior a Senior; 3+ intermedias o mezcla a Intermedio; 3+ junior o "no sé" a Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-10-13

> El artículo existía desde el 2026-09-07 y el learner probablemente ya lo había leído; el diagnóstico se tomó al generar el notebook, sin mirarlo.

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Junior | "No sé". No conoce la invarianza de `MutableList` ni la covarianza de `List`. |
| 2 | Junior | "No sé". No conoce `out`/`in` ni la regla de posición. |
| 3 | Junior | "No sé". No conoce el type erasure ni `reified`. |
| 4 | Junior | "No sé". No conoce la star projection. |
| 5 | Junior | "No sé". No conoce los upper bounds ni que `T` admite nullables por defecto. |

**Nivel global: Junior** (0 Senior, 0 intermedias, 5 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Usa List<T> y funciones genéricas a diario; conviene partir de esos ejemplos. Viene de Higher-Order Functions & Lambdas, donde vio inline, que es la base de reified.

Necesita explicación en profundidad, desde cero: qué son los generics y el type safety que dan; la invarianza por defecto y por qué MutableList<String> no es subtipo de MutableList<Any>; la covarianza (out) y la contravarianza (in), con la regla de posición (out en tipos de retorno, in en parámetros) y por qué List es covariante y MutableList no; el type erasure de la JVM y por qué is T no compila; cómo inline con reified lo resuelve en cada llamada y su costo (code bloat); la star projection <*>; y los upper bounds como <T : Any> para excluir nullables.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una caja de frutas de la que solo se saca es segura de tratar como caja de comida; una en la que también se mete, no), la varianza con out e in, después el type erasure y reified, y cerrá con la star projection y los upper bounds.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Generics: Variance & Reification (in, out, reified)

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/generics-variance-reification/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/collections-mutability/
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/higher-order-functions-lambdas/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/type-safety/
https://aghmnl.github.io/senior-forge-codex/es/glosario/generic-type-parameters/
https://aghmnl.github.io/senior-forge-codex/es/glosario/call-site/
https://aghmnl.github.io/senior-forge-codex/es/glosario/jvm/
https://aghmnl.github.io/senior-forge-codex/es/glosario/compile-time/
https://aghmnl.github.io/senior-forge-codex/es/glosario/type-erasure/
https://aghmnl.github.io/senior-forge-codex/es/glosario/bytecode/
https://aghmnl.github.io/senior-forge-codex/es/glosario/runtime/
https://aghmnl.github.io/senior-forge-codex/es/glosario/keyword/
https://aghmnl.github.io/senior-forge-codex/es/glosario/invariance/
https://aghmnl.github.io/senior-forge-codex/es/glosario/covariance/
https://aghmnl.github.io/senior-forge-codex/es/glosario/return-type/
https://aghmnl.github.io/senior-forge-codex/es/glosario/contravariance/
https://aghmnl.github.io/senior-forge-codex/es/glosario/reified/
https://aghmnl.github.io/senior-forge-codex/es/glosario/inline-functions/
https://aghmnl.github.io/senior-forge-codex/es/glosario/upper-bound/
https://aghmnl.github.io/senior-forge-codex/es/glosario/star-projection/
https://aghmnl.github.io/senior-forge-codex/es/glosario/raw-types/
https://aghmnl.github.io/senior-forge-codex/es/glosario/variance/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cast/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collections/
https://aghmnl.github.io/senior-forge-codex/es/glosario/immutability/
https://aghmnl.github.io/senior-forge-codex/es/glosario/state-holder/
https://aghmnl.github.io/senior-forge-codex/es/glosario/class-cast-exception/
https://aghmnl.github.io/senior-forge-codex/es/glosario/code-bloat/
https://aghmnl.github.io/senior-forge-codex/es/glosario/overhead/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lambdas/
https://aghmnl.github.io/senior-forge-codex/es/glosario/moshi/
https://aghmnl.github.io/senior-forge-codex/es/glosario/room/
https://aghmnl.github.io/senior-forge-codex/es/glosario/runtime-reflection/
https://aghmnl.github.io/senior-forge-codex/es/glosario/single-responsibility-principle/
https://aghmnl.github.io/senior-forge-codex/es/glosario/data-layer/
https://aghmnl.github.io/senior-forge-codex/es/glosario/type-inference/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mapper-function/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/generics.html
https://kotlinlang.org/docs/inline-functions.html
https://kotlinlang.org/docs/collections-overview.html

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Generics: Variance & Reification (in, out, reified)
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Usa List<T> y funciones genéricas a diario; conviene partir de esos ejemplos. Viene de Higher-Order Functions & Lambdas, donde vio inline, que es la base de reified.

Necesita explicación en profundidad, desde cero: qué son los generics y el type safety que dan; la invarianza por defecto y por qué MutableList<String> no es subtipo de MutableList<Any>; la covarianza (out) y la contravarianza (in), con la regla de posición (out en tipos de retorno, in en parámetros) y por qué List es covariante y MutableList no; el type erasure de la JVM y por qué is T no compila; cómo inline con reified lo resuelve en cada llamada y su costo (code bloat); la star projection <*>; y los upper bounds como <T : Any> para excluir nullables.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (una caja de frutas de la que solo se saca es segura de tratar como caja de comida; una en la que también se mete, no), la varianza con out e in, después el type erasure y reified, y cerrá con la star projection y los upper bounds.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Generics: in, out, where | Varianza en el sitio de declaración y de uso, star projections, upper bounds y type erasure. |
| Inline functions | `reified` y por qué requiere `inline`. |
| Collections overview | Por qué `List` es covariante y `MutableList` no. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Generics: Variance & Reification (in, out, reified)", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. Si `String` es subtipo de `Any`, ¿`MutableList<String>` es subtipo de `MutableList<Any>`? ¿Y `List<String>` de `List<Any>`? ¿Por qué la diferencia?
2. ¿Qué significan `out T` e `in T` en la declaración de una clase genérica? ¿Cómo sabés cuál corresponde?
3. ¿Por qué no podés escribir `if (value is T)` en una función genérica común? ¿Qué es el *type erasure*?
4. ¿Qué significa `ReorderState<*>`? ¿Qué podés leer de ahí y qué no podés escribir?
5. En una función `fun <T> printAll(items: List<T>)`, ¿puede `T` ser un tipo nullable como `String?`? ¿Cómo lo impedirías?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: MutableList es invariante (se podría agregar otro tipo); List es covariante (out E) porque solo se lee. Junior: no sabe.
- P2 Senior: out = covarianza, T solo en retornos (produce); in = contravarianza, T solo en parámetros (consume); en ambos, invariante. Junior: no sabe.
- P3 Senior: type erasure borra T del bytecode; se resuelve con inline + reified. Junior: no sabe.
- P4 Senior: star projection; lecturas como Any?, escrituras prohibidas. Junior: no sabe.
- P5 Senior: sí, T es Any? por defecto; se impide con <T : Any>. Junior: no sabe.
```
