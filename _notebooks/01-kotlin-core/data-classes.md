---
topic: "Data Classes: copy, equals, toString"
chapter: 01-kotlin-core
slug: data-classes
lang: es
article: /es/01-kotlin-core/data-classes/
diagnostic_date: 2026-09-18
---

# Notebook de estudio — Data Classes: copy, equals, toString

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Qué genera el compilador cuando marcás una clase como `data class`, y a partir de qué exactamente lo genera? ¿Qué queda afuera?
2. `data class User(val id: String) { var lastSeen: Long = 0 }` — dos instancias con el mismo `id` y distinto `lastSeen`: ¿`==` da true o false? ¿Y si las metés en un `HashSet`? ¿Qué cambiarías si `lastSeen` tiene que importar?
3. Tenés `data class UiState(val items: List<Item>, val loading: Boolean)` en un ViewModel con `StateFlow`. ¿Cómo actualizás solo `loading` sin tocar el resto, y por qué importa que las propiedades sean `val`?
4. ¿Qué es `componentN()` y qué te permite escribir? Dame un caso donde el destructuring mejora la legibilidad y uno donde la empeora.
5. Querés que `Admin` herede de `data class User(...)`. ¿Podés? ¿Por qué Kotlin lo prohíbe y cómo modelarías esa jerarquía en su lugar?

### Rúbrica

| # | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | `equals()`, `hashCode()`, `toString()`, `copy()` y `componentN()`, generados **solo** a partir de las propiedades del constructor primario. Las propiedades del cuerpo, los `init` y las funciones no participan. Es un contrato, no solo azúcar: define qué significa "identidad" para esa clase. | Nombra la mayoría de las funciones pero no sabe que solo cuentan las del constructor primario, o se olvida de `componentN`/`copy`. | Cree que una data class es "una clase sin métodos" o no sabe qué genera. |
| 2 | `==` da **true**: `lastSeen` está en el cuerpo, no en el constructor primario, así que `equals`/`hashCode` lo ignoran. En un `HashSet` la segunda instancia se considera duplicada y no entra. Si tiene que importar, mover `lastSeen` al constructor primario (y hacerlo `val`). | Intuye que "puede haber problema" pero no sabe si da true o false, o no conecta con el comportamiento en colecciones hash. | Cree que da false porque "son objetos distintos" o porque "todas las propiedades cuentan". |
| 3 | `_state.update { it.copy(loading = true) }` (o `value = value.copy(...)`): `copy()` crea una instancia nueva con solo ese campo cambiado. Con `val` el estado es inmutable: cada cambio es una instancia nueva, así que `StateFlow` detecta el cambio por `equals`, no hay mutación compartida entre threads y la transición queda explícita. Con `var` podrías mutar el objeto emitido sin que nadie se entere. | Usa `copy()` pero no explica por qué `val` importa (inmutabilidad, detección de cambios, thread-safety), o propone mutar una `var` dentro del estado. | No conoce `copy()` o propone crear el objeto completo a mano cada vez. |
| 4 | `component1()`, `component2()`… generados en orden de declaración del constructor primario; habilitan `val (a, b) = obj`, destructuring en lambdas (`map.forEach { (k, v) -> }`) y en `for`. Mejora: `Pair`/`Triple` o entradas de map en lambdas. Empeora: data classes con muchos campos donde el orden posicional no es obvio (`val (x, y, z, w) = config`) — un cambio de orden en el constructor rompe en silencio. | Conoce el destructuring pero no `componentN` ni el riesgo del orden posicional. | No conoce el destructuring. |
| 5 | No: las data classes no pueden ser `open` (ni `abstract`, `sealed`, `inner`). Motivo: `equals`/`hashCode`/`copy` se generan desde el constructor primario de *esa* clase; una subclase con más campos rompería la simetría de `equals` y `copy()` devolvería el tipo base. Alternativas: composición (`data class Admin(val user: User, val permissions: Set<Permission>)`), o una `sealed interface` con varias data classes que la implementen. | Sabe que "no se puede heredar" pero no explica por qué ni propone alternativa concreta. | Cree que sí se puede, o no sabe. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior → Senior; 3+ intermedias o mezcla → Intermedio; 3+ junior o "no sé" → Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-09-18

| # | Nivel | Observación |
|---|---|---|
| 1 | Junior | "No sé". No conoce qué genera el compilador ni la regla del constructor primario. |
| 2 | Junior | "No sé". No conoce el efecto de las propiedades del cuerpo sobre `equals`/`hashCode`. |
| 3 | Junior | "No sé". No conoce `copy()` ni la relación `val` + inmutabilidad en el estado de UI. |
| 4 | Junior | "No sé". No conoce `componentN()` ni el destructuring. |
| 5 | Junior | "No sé". No conoce la restricción de herencia ni sus alternativas. |

**Nivel global: Junior** (5 "no sé"). Tema a estudiar íntegramente desde cero.

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: nada que el notebook pueda dar por sabido en este tema. Respondió "no sé" a las cinco preguntas. De nivelaciones previas del mismo día se sabe que distingue `val` de `var` a nivel básico y que conoce la idea de nullable vs. no-nullable, así que la explicación de por qué `val` importa en el estado puede apoyarse en eso.

Necesita explicación en profundidad, desde cero: qué genera el compilador para una data class (`equals()`, `hashCode()`, `toString()`, `copy()` y `componentN()`) y la regla central de que se generan solo a partir de las propiedades del constructor primario — las propiedades del cuerpo quedan afuera, con la consecuencia de que dos instancias con distinto valor en una propiedad del cuerpo son iguales según `==` y se consideran duplicadas en un `HashSet` o como claves de un `Map`; `copy()` como mecanismo para crear una instancia nueva cambiando solo algunos campos, y por qué combinado con propiedades `val` es la base de las transiciones de estado inmutables en un `StateFlow` (detección de cambios por `equals`, sin mutación compartida entre threads); `componentN()` y el destructuring (`val (a, b) = obj`, en lambdas y en `for`), incluyendo el riesgo del orden posicional cuando la clase tiene muchos campos; y por qué una data class no puede ser `open` ni servir de clase base (los métodos generados dependen del constructor primario de esa clase y la herencia rompería `equals` y `copy`), con las alternativas de composición o una sealed interface implementada por varias data classes.

Malentendidos a corregir: ninguno detectado (no hubo respuestas incorrectas, solo ausencia de respuesta).

Instrucción para el Audio Overview: explicá todo desde cero, con analogías, en este orden: primero qué es una data class y qué genera el compilador, después la regla del constructor primario con el ejemplo de la propiedad en el cuerpo que no cuenta para `equals`, después `copy()` + `val` como forma de actualizar estado de UI, después el destructuring con `componentN()`, y por último por qué no se puede heredar y qué usar en su lugar. No des nada por sabido.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Data Classes: copy, equals, toString

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/data-classes/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/equals/
https://aghmnl.github.io/senior-forge-codex/es/glosario/hash-code/
https://aghmnl.github.io/senior-forge-codex/es/glosario/to-string/
https://aghmnl.github.io/senior-forge-codex/es/glosario/copy/
https://aghmnl.github.io/senior-forge-codex/es/glosario/component-n/
https://aghmnl.github.io/senior-forge-codex/es/glosario/syntax-sugar/
https://aghmnl.github.io/senior-forge-codex/es/glosario/primary-constructor/
https://aghmnl.github.io/senior-forge-codex/es/glosario/maps/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sets/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mutation/
https://aghmnl.github.io/senior-forge-codex/es/glosario/unidirectional-data-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/state-transitions/
https://aghmnl.github.io/senior-forge-codex/es/glosario/destructuring/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lambdas/
https://aghmnl.github.io/senior-forge-codex/es/glosario/multiple-return-patterns/
https://aghmnl.github.io/senior-forge-codex/es/glosario/inheritance/
https://aghmnl.github.io/senior-forge-codex/es/glosario/open/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/data-classes.html
https://kotlinlang.org/docs/destructuring-declarations.html
https://kotlinlang.org/docs/equality.html
https://kotlinlang.org/docs/classes.html
https://kotlinlang.org/docs/inheritance.html
https://kotlinlang.org/docs/sealed-classes.html
https://kotlinlang.org/docs/idioms.html
https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-any/equals.html
https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-any/hash-code.html
https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-triple/
https://developer.android.com/topic/architecture/ui-layer
https://developer.android.com/develop/ui/compose/performance/stability

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Data Classes: copy, equals, toString
2. Agregá el artículo principal como fuente web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: nada que el notebook pueda dar por sabido en este tema. Respondió "no sé" a las cinco preguntas. De nivelaciones previas del mismo día se sabe que distingue `val` de `var` a nivel básico y que conoce la idea de nullable vs. no-nullable, así que la explicación de por qué `val` importa en el estado puede apoyarse en eso.

Necesita explicación en profundidad, desde cero: qué genera el compilador para una data class (`equals()`, `hashCode()`, `toString()`, `copy()` y `componentN()`) y la regla central de que se generan solo a partir de las propiedades del constructor primario — las propiedades del cuerpo quedan afuera, con la consecuencia de que dos instancias con distinto valor en una propiedad del cuerpo son iguales según `==` y se consideran duplicadas en un `HashSet` o como claves de un `Map`; `copy()` como mecanismo para crear una instancia nueva cambiando solo algunos campos, y por qué combinado con propiedades `val` es la base de las transiciones de estado inmutables en un `StateFlow` (detección de cambios por `equals`, sin mutación compartida entre threads); `componentN()` y el destructuring (`val (a, b) = obj`, en lambdas y en `for`), incluyendo el riesgo del orden posicional cuando la clase tiene muchos campos; y por qué una data class no puede ser `open` ni servir de clase base (los métodos generados dependen del constructor primario de esa clase y la herencia rompería `equals` y `copy`), con las alternativas de composición o una sealed interface implementada por varias data classes.

Malentendidos a corregir: ninguno detectado (no hubo respuestas incorrectas, solo ausencia de respuesta).

Instrucción para el Audio Overview: explicá todo desde cero, con analogías, en este orden: primero qué es una data class y qué genera el compilador, después la regla del constructor primario con el ejemplo de la propiedad en el cuerpo que no cuenta para `equals`, después `copy()` + `val` como forma de actualizar estado de UI, después el destructuring con `componentN()`, y por último por qué no se puede heredar y qué usar en su lugar. No des nada por sabido.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Data classes | La referencia completa: qué se genera, la regla del constructor primario, propiedades en el cuerpo, `copy()`, `componentN()`, restricciones. |
| Destructuring declarations | Cómo `componentN()` habilita `val (a, b) = obj`, destructuring en lambdas y en `for`, y el uso de `_` para omitir. |
| Equality | Igualdad estructural (`==` → `equals`) vs. referencial (`===`), la base del contrato `equals`/`hashCode`. |
| Classes | Constructor primario vs. bloques `init` y propiedades del cuerpo — lo que decide qué entra en los métodos generados. |
| Inheritance | Por qué las clases son `final` por defecto y qué implica que una data class no pueda ser `open`. |
| Sealed classes and interfaces | La alternativa idiomática a heredar de una data class: una jerarquía sellada con varias data classes. |
| Idioms | Los idiomas oficiales: data class para DTOs, `copy()` para modificar, destructuring de pares y maps. |
| `Any.equals` (API) | El contrato formal de `equals` (reflexiva, simétrica, transitiva, consistente) que la generación automática garantiza. |
| `Any.hashCode` (API) | El contrato `equals` ⇒ mismo `hashCode`, y por qué las colecciones hash dependen de él. |
| `Triple` (API) | Una data class de la stdlib: el ejemplo del artículo con destructuring de tres valores. |
| UI layer (Android) | `UiState` como data class inmutable actualizada con `copy()` dentro de un `StateFlow`. |
| Stability in Compose | Por qué una data class con `val` y tipos estables permite a Compose saltear recomposiciones. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Data Classes: copy, equals, toString", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Qué genera el compilador cuando marcás una clase como `data class`, y a partir de qué exactamente lo genera? ¿Qué queda afuera?
2. `data class User(val id: String) { var lastSeen: Long = 0 }` — dos instancias con el mismo `id` y distinto `lastSeen`: ¿`==` da true o false? ¿Y si las metés en un `HashSet`? ¿Qué cambiarías si `lastSeen` tiene que importar?
3. Tenés `data class UiState(val items: List<Item>, val loading: Boolean)` en un ViewModel con `StateFlow`. ¿Cómo actualizás solo `loading` sin tocar el resto, y por qué importa que las propiedades sean `val`?
4. ¿Qué es `componentN()` y qué te permite escribir? Dame un caso donde el destructuring mejora la legibilidad y uno donde la empeora.
5. Querés que `Admin` herede de `data class User(...)`. ¿Podés? ¿Por qué Kotlin lo prohíbe y cómo modelarías esa jerarquía en su lugar?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: equals, hashCode, toString, copy y componentN, generados solo desde las propiedades del constructor primario; el cuerpo queda afuera. Junior: no sabe qué se genera.
- P2 Senior: `==` da true porque `lastSeen` está en el cuerpo; en un HashSet la segunda no entra; mover `lastSeen` al constructor primario. Junior: cree que da false.
- P3 Senior: `copy(loading = true)` dentro de `update {}`; `val` garantiza inmutabilidad, detección de cambio por equals y seguridad entre threads. Junior: no conoce copy().
- P4 Senior: componentN en orden del constructor; mejora en Pair/Triple/entradas de map; empeora con muchos campos por el orden posicional. Junior: no conoce destructuring.
- P5 Senior: no se puede (no `open`); rompería equals/copy; usar composición o sealed interface con varias data classes. Junior: cree que sí se puede.
```
