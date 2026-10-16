---
topic: "Lateinit vs Lazy"
chapter: 01-kotlin-core
slug: lateinit-vs-lazy
lang: es
article: /es/01-kotlin-core/lateinit-vs-lazy/
diagnostic_date: 2026-10-12
---

# Notebook de estudio — Lateinit vs Lazy

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Se puede usar `lateinit` con una `val`? ¿Y con un `Int`? ¿Por qué?
2. ¿Qué pasa si leés una propiedad `lateinit` antes de asignarla? ¿Cómo podés verificar si ya fue asignada?
3. Si una propiedad `by lazy { }` nunca se lee, ¿se ejecuta alguna vez su bloque? ¿Y si se lee diez veces, cuántas veces corre?
4. Por defecto, `lazy` es thread-safe. ¿Qué modo usarías si la propiedad solo se lee desde el hilo principal, y qué ganás con eso?
5. ¿Por qué en las clases de test es tan común declarar las dependencias como `lateinit var` y asignarlas en un método `@Before`?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | **No** con `val`: `lateinit` es para `var` que se asignan después. **No** con primitivos como `Int`: la JVM no tiene forma de representar "no inicializado" para un primitivo (usa `null` en el campo para eso). | Acierta uno de los dos casos. | No sabe. |
| 2 | Lanza **`UninitializedPropertyAccessException`**. Se verifica con **`::propiedad.isInitialized`**. | Sabe que falla pero no cómo verificarlo. | No sabe. |
| 3 | Si nunca se lee, **nunca corre** (no se paga el costo). Si se lee diez veces, corre **una sola vez**: la primera lectura calcula y cachea, las demás devuelven el valor guardado. | Acierta una de las dos. | No sabe. |
| 4 | **`LazyThreadSafetyMode.NONE`**: evita el bloque `synchronized` y su overhead. Solo es seguro si de verdad se lee desde un único hilo. | Sabe que hay modos pero no cuál. | No sabe. |
| 5 | Permite tipos **no nullables** sin `?` ni `!!`, y el `@Before` crea **instancias nuevas antes de cada test**, así cada test queda aislado de los demás. | Menciona una de las dos razones. | No sabe. |

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
| 1 | Junior | "No sé". No conoce las restricciones de `lateinit` (`var`, no primitivos). |
| 2 | Junior | "No sé". No conoce `UninitializedPropertyAccessException` ni `isInitialized`. |
| 3 | Junior | "No sé". No conoce la semántica de `lazy` (bajo demanda, una sola vez). |
| 4 | Junior | "No sé". No conoce `LazyThreadSafetyMode`. |
| 5 | Junior | "No sé". No conoce el patrón de `lateinit` en tests. |

**Nivel global: Junior** (0 Senior, 0 intermedias, 5 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de Scope Functions y Higher-Order Functions & Lambdas; conviene presentar lazy como una función que recibe una lambda y la ejecuta una sola vez.

Necesita explicación en profundidad, desde cero: qué hace lateinit (una var no nullable que se asigna después) y por qué no sirve con val ni con primitivos como Int; qué pasa si se lee antes de asignarla (UninitializedPropertyAccessException) y cómo verificarlo con ::propiedad.isInitialized; qué hace by lazy (calcula en la primera lectura, una sola vez, y si nunca se lee nunca corre); los modos de LazyThreadSafetyMode (SYNCHRONIZED por defecto, NONE para un solo hilo, PUBLICATION); y los usos típicos: lateinit en tests con @Before y en inyección de campos con Hilt, lazy para objetos costosos.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (lateinit es una silla reservada que alguien promete ocupar; lazy es una comida que se cocina recién cuando alguien la pide y después se sirve recalentada), la diferencia entre los dos, después los errores y verificaciones de lateinit, los modos de thread safety de lazy, y cerrá con los usos típicos en tests e inyección.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Lateinit vs Lazy

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/lateinit-vs-lazy/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/delegated-properties/
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/scope-functions/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/hilt/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dagger/
https://aghmnl.github.io/senior-forge-codex/es/glosario/dependency-graph/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lifecycle-event/
https://aghmnl.github.io/senior-forge-codex/es/glosario/primitives/
https://aghmnl.github.io/senior-forge-codex/es/glosario/jvm/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lambdas/
https://aghmnl.github.io/senior-forge-codex/es/glosario/synchronized-block/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lazy-thread-safety-mode/
https://aghmnl.github.io/senior-forge-codex/es/glosario/junit-before/
https://aghmnl.github.io/senior-forge-codex/es/glosario/runtime-reflection/
https://aghmnl.github.io/senior-forge-codex/es/glosario/constructor/
https://aghmnl.github.io/senior-forge-codex/es/glosario/allocations/
https://aghmnl.github.io/senior-forge-codex/es/glosario/overhead/
https://aghmnl.github.io/senior-forge-codex/es/glosario/bytecode/
https://aghmnl.github.io/senior-forge-codex/es/glosario/runtime/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/properties.html
https://kotlinlang.org/docs/delegated-properties.html
https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-lazy-thread-safety-mode/

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Lateinit vs Lazy
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: ningún punto de este tema todavía. Viene de Scope Functions y Higher-Order Functions & Lambdas; conviene presentar lazy como una función que recibe una lambda y la ejecuta una sola vez.

Necesita explicación en profundidad, desde cero: qué hace lateinit (una var no nullable que se asigna después) y por qué no sirve con val ni con primitivos como Int; qué pasa si se lee antes de asignarla (UninitializedPropertyAccessException) y cómo verificarlo con ::propiedad.isInitialized; qué hace by lazy (calcula en la primera lectura, una sola vez, y si nunca se lee nunca corre); los modos de LazyThreadSafetyMode (SYNCHRONIZED por defecto, NONE para un solo hilo, PUBLICATION); y los usos típicos: lateinit en tests con @Before y en inyección de campos con Hilt, lazy para objetos costosos.

Malentendidos a corregir: ninguno explícito; no hubo respuestas incorrectas, solo ausencia de conocimiento previo.

Instrucción para el Audio Overview: explicá desde cero, con analogías (lateinit es una silla reservada que alguien promete ocupar; lazy es una comida que se cocina recién cuando alguien la pide y después se sirve recalentada), la diferencia entre los dos, después los errores y verificaciones de lateinit, los modos de thread safety de lazy, y cerrá con los usos típicos en tests e inyección.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Properties | `lateinit`, sus restricciones y `isInitialized`. |
| Delegated properties | `by lazy` y cómo funciona como propiedad delegada. |
| LazyThreadSafetyMode (API) | Los modos `SYNCHRONIZED`, `PUBLICATION` y `NONE`. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Lateinit vs Lazy", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Se puede usar `lateinit` con una `val`? ¿Y con un `Int`? ¿Por qué?
2. ¿Qué pasa si leés una propiedad `lateinit` antes de asignarla? ¿Cómo podés verificar si ya fue asignada?
3. Si una propiedad `by lazy { }` nunca se lee, ¿se ejecuta alguna vez su bloque? ¿Y si se lee diez veces, cuántas veces corre?
4. Por defecto, `lazy` es thread-safe. ¿Qué modo usarías si la propiedad solo se lee desde el hilo principal, y qué ganás con eso?
5. ¿Por qué en las clases de test es tan común declarar las dependencias como `lateinit var` y asignarlas en un método `@Before`?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: no con val (es para var) y no con primitivos (la JVM no puede representar "no inicializado"). Junior: no sabe.
- P2 Senior: UninitializedPropertyAccessException; se verifica con ::propiedad.isInitialized. Junior: no sabe.
- P3 Senior: si nunca se lee no corre; si se lee diez veces corre una sola vez. Junior: no sabe.
- P4 Senior: LazyThreadSafetyMode.NONE, evita el synchronized. Junior: no sabe.
- P5 Senior: tipos no nullables sin ? ni !!, e instancias nuevas antes de cada test. Junior: no sabe.
```
