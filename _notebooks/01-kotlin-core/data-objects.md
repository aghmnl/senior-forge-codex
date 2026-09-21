---
topic: "Data Objects: Singleton & Memory Savings"
chapter: 01-kotlin-core
slug: data-objects
lang: es
article: /es/01-kotlin-core/data-objects/
diagnostic_date: 2026-09-21
---

# Notebook de estudio — Data Objects: Singleton & Memory Savings

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Qué genera el compilador para un `data object` que un `object` común no genera? ¿Y qué genera una `data class` que un `data object` no?
2. `object Loading` vs `data object Loading` dentro de una sealed class. Mostrame qué imprime `println(state)` en cada caso y por qué eso importa en la práctica.
3. Para un `data object`, ¿qué resultado dan `a == b` y `a === b` si `a` y `b` son referencias al mismo estado? ¿Y qué pasa si en vez de `data object` usás una data class sin propiedades, `data class Loading()`?
4. Tenés `sealed interface UiState` con estados `Loading`, `Empty`, `Success(items)` y `Error(message)`. ¿Cuál declarás como `data object` y cuál como `data class`, y con qué criterio? ¿Qué gana la app en memoria?
5. Un `data object` es un singleton que vive mientras viva el proceso. ¿Qué riesgo trae eso si le agregás estado mutable adentro, y por qué en Android es peor que en un backend?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | `data object` agrega `toString()` (solo el nombre), `equals()` y `hashCode()` consistentes sobre la garantía de instancia única de `object`. No genera `copy()` ni `componentN()`, porque un singleton no tiene propiedades de constructor que copiar o desestructurar. Una `data class` sí genera esas dos, y no es singleton. | Sabe que "mejora el toString" pero no menciona `equals`/`hashCode` ni por qué faltan `copy`/`componentN`. | No conoce `data object` o lo cree igual que `data class`. |
| 2 | `object`: el nombre seguido de arroba y el hash de identidad — el `toString()` por defecto de `Any`. `data object`: solo `Loading`. Importa porque los estados sellados se loguean, aparecen en reportes de crash, en mensajes de aserción de tests y en herramientas de inspección; un hash de memoria no le dice nada a nadie y obliga a sobreescribir `toString()` a mano en cada objeto. | Sabe que uno imprime "algo feo" pero no identifica que es el `toString()` de `Any` ni articula el costo práctico. | No sabe qué imprime cada uno. |
| 3 | Las dos dan `true`: para un singleton la igualdad estructural y la referencial coinciden, porque hay exactamente una instancia. Con `data class Loading()` cada `Loading()` es una instancia nueva: `==` da `true` (equals generado sobre cero propiedades) pero `===` da `false`, y además se aloca un objeto por cada uso. Ese desajuste entre `==` y `===` es la fuente de bugs sutiles. | Contesta bien para el `data object` pero no ve la diferencia con la data class sin propiedades. | No distingue `==` de `===`. |
| 4 | `Loading` y `Empty` como `data object` (no llevan datos, una sola instancia); `Success` y `Error` como `data class` (llevan payload). Ganancia: cero allocations para los estados sin datos, que en un `StateFlow` de UI se emiten muchísimas veces — cada emisión reusa la misma instancia en vez de crear un objeto que después junta el GC. Menciona que con instancia única la comparación en `when` es referencial y barata. | Reparte bien object/class pero no articula la ganancia en allocations ni la frecuencia de emisión. | Declara todo como `data class`, o todo como `object`. |
| 5 | Un `data object` con una `var` adentro es estado global mutable con el ciclo de vida del proceso: sobrevive a `Activity`, a `ViewModel` y a la rotación. En Android es peor porque el proceso puede sobrevivir a que el usuario "salga" de la app, así que el estado viejo reaparece en una sesión nueva; y si guarda una referencia a `Context`, `Activity` o una vista, es un memory leak que nunca se libera. Además rompe la igualdad: dos lecturas del mismo singleton pueden diferir, y `hashCode` cambia mientras el objeto está en un `HashSet`. Los `data object` tienen que ser inmutables y sin estado. | Sabe que "el estado global es riesgoso" pero no lo conecta con el ciclo de vida del proceso, los leaks de `Context` ni con la igualdad. | No ve problema, o cree que el objeto se recrea en cada pantalla. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior → Senior; 3+ intermedias o mezcla → Intermedio; 3+ junior o "no sé" → Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-09-21

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Junior | "Los getters y setters" — incorrecto: los accessors los genera cualquier propiedad, sin relación con `data`. No nombra `toString`/`equals`/`hashCode` ni lo que queda afuera (`copy`, `componentN`). |
| 2 | Intermedia | Correcto en la observación práctica: uno imprime la referencia y el otro un print limpio. No identifica que es el `toString()` de `Any` ni articula el costo (logs, crashes, tests). |
| 3 | Junior | "No sé". No conoce la relación entre igualdad estructural y referencial en un singleton, ni el caso de la data class sin propiedades. |
| 4 | Junior | "No sé". No conoce el criterio de reparto en una jerarquía sellada ni la ganancia en allocations. |
| 5 | Junior | "No sé". No conoce el riesgo del estado mutable en un singleton con vida de proceso. |

**Nivel global: Junior** (4 junior, 1 intermedia).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: la diferencia visible en el toString — sabe que un object común imprime algo con la referencia de memoria y que un data object imprime una representación limpia. Ese punto se puede tratar como repaso de una frase y usarse como puerta de entrada al resto.

Necesita explicación en profundidad, desde cero: qué genera realmente el compilador para un data object (toString, equals y hashCode) por encima de la garantía de instancia única que ya trae object, y qué NO genera (copy y componentN), porque un singleton no tiene propiedades de constructor para copiar ni desestructurar — ahí está el contraste exacto con data class; que getters y setters no son lo que distingue a un data object: los getters los genera cualquier propiedad de cualquier clase y los setters solo las propiedades var, así que no tienen relación con la palabra data; que el toString "feo" de un object es concretamente el de Any, nombre de clase más el hash de identidad en hexadecimal, y por qué eso duele en logs, reportes de crash y mensajes de aserción de tests; la igualdad en un singleton: la estructural y la referencial coinciden porque hay una sola instancia, y el contraste con una data class sin propiedades, donde la estructural da true pero la referencial da false y además se aloca un objeto en cada uso; el criterio para repartir una jerarquía sellada de estado de UI — data object para los estados sin datos, data class para los que llevan payload — y la ganancia en allocations cuando esos estados se emiten muchas veces por un StateFlow; y por qué un data object tiene que ser inmutable: una var adentro es estado global con el ciclo de vida del proceso, sobrevive a la rotación y a que el usuario salga de la app, filtra Context o Activity si los guarda, y rompe el contrato de hashCode si el objeto está dentro de un HashSet.

Malentendidos a corregir: respondió que un data object genera "los getters y setters". No es así: los accessors los genera el compilador para cualquier propiedad, sin relación con data ni con object, y un singleton sin propiedades no tiene ninguno. Lo que agrega data sobre un object son toString, equals y hashCode. También describió el toString de un object común como "el tag del lugar de memoria": es el hash de identidad, que deriva de la identidad del objeto pero no es su dirección de memoria — el recolector de basura puede mover el objeto sin que ese número cambie.

Instrucción para el Audio Overview: explicá desde cero, con analogías, qué agrega exactamente la palabra data sobre un object y qué se queda afuera respecto de una data class, después la igualdad estructural y la referencial en un singleton con el caso trampa de la data class sin propiedades, después el criterio data object vs data class en una jerarquía sellada de estado de UI con su impacto en allocations, y por último por qué un singleton con estado mutable es un problema en Android; tratá el toString limpio como repaso de una frase y aclará de paso que los getters y setters no tienen nada que ver con esto.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Data Objects: Singleton & Memory Savings

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/data-objects/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/data-object/
https://aghmnl.github.io/senior-forge-codex/es/glosario/singleton/
https://aghmnl.github.io/senior-forge-codex/es/glosario/object/
https://aghmnl.github.io/senior-forge-codex/es/glosario/to-string/
https://aghmnl.github.io/senior-forge-codex/es/glosario/equals/
https://aghmnl.github.io/senior-forge-codex/es/glosario/hash-code/
https://aghmnl.github.io/senior-forge-codex/es/glosario/copy/
https://aghmnl.github.io/senior-forge-codex/es/glosario/component-n/
https://aghmnl.github.io/senior-forge-codex/es/glosario/destructuring/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sealed-hierarchy/
https://aghmnl.github.io/senior-forge-codex/es/glosario/idle-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/allocations/
https://aghmnl.github.io/senior-forge-codex/es/glosario/state-emission-patterns/
https://aghmnl.github.io/senior-forge-codex/es/glosario/stateflow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/structural-equality/
https://aghmnl.github.io/senior-forge-codex/es/glosario/referential-equality/
https://aghmnl.github.io/senior-forge-codex/es/glosario/when-expression/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collections/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/object-declarations.html
https://kotlinlang.org/docs/whatsnew19.html
https://kotlinlang.org/docs/sealed-classes.html
https://kotlinlang.org/docs/data-classes.html
https://kotlinlang.org/docs/equality.html
https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-any/to-string.html
https://kotlinlang.org/docs/enum-classes.html
https://developer.android.com/topic/architecture/ui-layer
https://developer.android.com/develop/ui/compose/performance/stability
https://developer.android.com/topic/performance/memory

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Data Objects: Singleton & Memory Savings
2. Agregá el artículo principal como fuente web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: la diferencia visible en el toString — sabe que un object común imprime algo con la referencia de memoria y que un data object imprime una representación limpia. Ese punto se puede tratar como repaso de una frase y usarse como puerta de entrada al resto.

Necesita explicación en profundidad, desde cero: qué genera realmente el compilador para un data object (toString, equals y hashCode) por encima de la garantía de instancia única que ya trae object, y qué NO genera (copy y componentN), porque un singleton no tiene propiedades de constructor para copiar ni desestructurar — ahí está el contraste exacto con data class; que getters y setters no son lo que distingue a un data object: los getters los genera cualquier propiedad de cualquier clase y los setters solo las propiedades var, así que no tienen relación con la palabra data; que el toString "feo" de un object es concretamente el de Any, nombre de clase más el hash de identidad en hexadecimal, y por qué eso duele en logs, reportes de crash y mensajes de aserción de tests; la igualdad en un singleton: la estructural y la referencial coinciden porque hay una sola instancia, y el contraste con una data class sin propiedades, donde la estructural da true pero la referencial da false y además se aloca un objeto en cada uso; el criterio para repartir una jerarquía sellada de estado de UI — data object para los estados sin datos, data class para los que llevan payload — y la ganancia en allocations cuando esos estados se emiten muchas veces por un StateFlow; y por qué un data object tiene que ser inmutable: una var adentro es estado global con el ciclo de vida del proceso, sobrevive a la rotación y a que el usuario salga de la app, filtra Context o Activity si los guarda, y rompe el contrato de hashCode si el objeto está dentro de un HashSet.

Malentendidos a corregir: respondió que un data object genera "los getters y setters". No es así: los accessors los genera el compilador para cualquier propiedad, sin relación con data ni con object, y un singleton sin propiedades no tiene ninguno. Lo que agrega data sobre un object son toString, equals y hashCode. También describió el toString de un object común como "el tag del lugar de memoria": es el hash de identidad, que deriva de la identidad del objeto pero no es su dirección de memoria — el recolector de basura puede mover el objeto sin que ese número cambie.

Instrucción para el Audio Overview: explicá desde cero, con analogías, qué agrega exactamente la palabra data sobre un object y qué se queda afuera respecto de una data class, después la igualdad estructural y la referencial en un singleton con el caso trampa de la data class sin propiedades, después el criterio data object vs data class en una jerarquía sellada de estado de UI con su impacto en allocations, y por último por qué un singleton con estado mutable es un problema en Android; tratá el toString limpio como repaso de una frase y aclará de paso que los getters y setters no tienen nada que ver con esto.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Object declarations | La referencia de `object` y `data object`: qué genera cada uno, inicialización lazy y la garantía de instancia única. |
| What's new in Kotlin 1.9 | La versión en la que se estabilizó `data object` y el problema concreto que vino a resolver. |
| Sealed classes and interfaces | Cómo se combinan `data object` y `data class` dentro de una jerarquía sellada y el `when` exhaustivo. |
| Data classes | Qué genera una `data class` — el contraste exacto: `copy()` y `componentN()` que un `data object` no tiene. |
| Equality | Igualdad estructural y referencial, que en un singleton coinciden y en una data class sin propiedades no. |
| `Any.toString` (API) | El `toString()` por defecto con el hash de identidad, que es lo que un `data object` reemplaza. |
| Enum classes | La alternativa clásica para conjuntos cerrados sin estado, y cuándo conviene sobre una jerarquía sellada. |
| UI layer (Android) | El patrón de `UiState` sellado con estados sin datos, que es el caso de uso principal. |
| Stability in Compose | Por qué un singleton inmutable es estable para Compose y evita recomposiciones. |
| Manage your app's memory | El costo real de las allocations y por qué evitarlas en emisiones de alta frecuencia importa. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Data Objects: Singleton & Memory Savings", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Qué genera el compilador para un `data object` que un `object` común no genera? ¿Y qué genera una `data class` que un `data object` no?
2. `object Loading` vs `data object Loading` dentro de una sealed class. Mostrame qué imprime `println(state)` en cada caso y por qué eso importa en la práctica.
3. Para un `data object`, ¿qué resultado dan `a == b` y `a === b` si `a` y `b` son referencias al mismo estado? ¿Y qué pasa si en vez de `data object` usás una data class sin propiedades, `data class Loading()`?
4. Tenés `sealed interface UiState` con estados `Loading`, `Empty`, `Success(items)` y `Error(message)`. ¿Cuál declarás como `data object` y cuál como `data class`, y con qué criterio? ¿Qué gana la app en memoria?
5. Un `data object` es un singleton que vive mientras viva el proceso. ¿Qué riesgo trae eso si le agregás estado mutable adentro, y por qué en Android es peor que en un backend?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: `data object` agrega toString/equals/hashCode sobre la garantía de singleton; no genera copy ni componentN porque no hay propiedades de constructor. Junior: lo cree igual que una data class.
- P2 Senior: `object` imprime el nombre más el hash de identidad (el toString de Any), `data object` imprime solo el nombre; importa para logs, crashes y tests. Intermedio: no identifica de dónde sale el hash.
- P3 Senior: en un singleton la igualdad estructural y la referencial dan true; con `data class Loading()` la estructural da true pero la referencial da false y se aloca una instancia por uso. Junior: no distingue las dos igualdades.
- P4 Senior: Loading y Empty como data object, Success y Error como data class; cero allocations en estados sin datos emitidos muchas veces por StateFlow. Junior: todo data class o todo object.
- P5 Senior: estado mutable en un singleton vive lo que vive el proceso, sobrevive rotación y "salir" de la app, filtra Context/Activity y rompe equals/hashCode; los data object deben ser inmutables. Junior: no ve problema.
```
