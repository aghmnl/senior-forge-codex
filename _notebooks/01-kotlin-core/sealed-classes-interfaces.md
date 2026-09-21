---
topic: "Sealed Classes vs Sealed Interfaces"
chapter: 01-kotlin-core
slug: sealed-classes-interfaces
lang: es
article: /es/01-kotlin-core/sealed-classes-interfaces/
diagnostic_date: 2026-09-21
---

# Notebook de estudio — Sealed Classes vs Sealed Interfaces

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Qué gana el compilador cuando una jerarquía es `sealed` y no simplemente `abstract` u `open`? ¿Qué restricción impone a cambio?
2. Un `when` sobre una jerarquía sellada sin rama `else`. Agregás un subtipo nuevo y no tocás nada más. ¿Qué pasa al compilar, y qué habría pasado si el `when` tuviera `else`?
3. `sealed class` y `sealed interface`: ¿qué podés hacer con una que no podés con la otra, en las dos direcciones? ¿Cuál usás por defecto y por qué?
4. Tenés tres acciones que comparten `taskId` y `childCount`. ¿Cómo las modelás para no repetir esos campos en cada variante? ¿Y si además cada acción tuviera que implementar un contrato de analytics?
5. Dentro de una jerarquía sellada, ¿cuándo declarás un miembro como `data object` y cuándo como `data class`? ¿Qué cambia en memoria cuando ese estado se emite miles de veces por un `StateFlow`?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | El compilador conoce el **conjunto cerrado** de subtipos, así que puede verificar exhaustividad en un `when` sin `else` y convertir un caso olvidado en error de compilación. La restricción: todos los subtipos directos tienen que declararse en el mismo paquete y módulo, así que nadie fuera de tu módulo puede extender la jerarquía. Menciona que eso es lo que hace de una jerarquía sellada un ADT (tipo suma). | Sabe que "permite `when` exhaustivo" pero no nombra la restricción de paquete/módulo ni la relación con los ADTs. | No distingue `sealed` de `abstract`/`open`. |
| 2 | Sin `else`: el `when` usado como expresión deja de compilar y el error señala exactamente cada lugar que no cubre el subtipo nuevo — el compilador actúa como verificador de la máquina de estados. Con `else`: compila igual y el subtipo nuevo cae silenciosamente en el `else`, produciendo un bug en runtime en vez de un error. Por eso el `else` en un `when` sellado es un antipatrón. | Sabe que "sin else avisa" pero no articula que con `else` el bug se vuelve silencioso ni por qué eso es peor. | Cree que hay que poner `else` siempre. |
| 3 | `sealed class` permite estado y comportamiento compartidos: propiedades en el constructor o `abstract val`, métodos comunes, bloque `init`, `companion object`. `sealed interface` no tiene constructor ni `init` ni estado, pero una clase puede implementar **varias** sealed interfaces, mientras que solo puede heredar de **una** sealed class (herencia simple de la JVM). Por defecto: `sealed interface`, y se pasa a `sealed class` solo cuando la jerarquía genuinamente necesita estado o implementación base compartida. | Conoce la diferencia de herencia múltiple pero no menciona `init`/constructor/estado compartido, o no tiene un criterio por defecto. | Cree que son equivalentes, o desconoce `sealed interface`. |
| 4 | `sealed class` con `abstract val taskId: String` y `abstract val childCount: Int`, y cada `data class` los provee con `override val` en su constructor primario — se declaran una vez en la base. Si además hace falta un contrato de analytics: la sealed class no alcanza sola (una clase hereda de una sola), así que las variantes implementan además una interfaz de analytics; o se modela todo con `sealed interface` y las propiedades compartidas como `val` de la interfaz. Ese es exactamente el caso donde la herencia múltiple de interfaces gana. | Propone la sealed class con propiedades abstractas pero no resuelve el segundo requisito ni ve el límite de la herencia simple. | Repite los campos en cada subtipo. |
| 5 | `data object` para variantes sin datos (`Loading`, `Idle`, `Restore`), `data class` para las que llevan payload. En memoria: un `data object` es un singleton, así que emitirlo miles de veces por un `StateFlow` crea **cero** objetos nuevos; una `data class` sin propiedades alocaría uno por emisión y le daría trabajo al GC. Además el `data object` trae `toString` legible y una igualdad donde la estructural y la referencial coinciden. | Reparte bien object/class pero no cuantifica la ganancia ni menciona el `toString`/igualdad. | Usa `data class` para todo, o no conoce `data object`. |

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
| 1 | Junior | "No sé". No conoce el conjunto cerrado de subtipos como lo que habilita la exhaustividad, ni la restricción de paquete/módulo. |
| 2 | Senior | Correcto y completo: sin `else` rompe la compilación porque hay que cubrir todas las opciones; con `else` el subtipo nuevo cae ahí silenciosamente. Identificó el antipatrón. |
| 3 | Intermedia | Criterio por defecto correcto (`sealed interface`) con la razón estructural correcta. Le falta la otra dirección: qué puede una `sealed class` que una interfaz no (constructor, `abstract val`, `init`, `companion object`). |
| 4 | Junior | "No sé". No conoce el patrón de `abstract val` en la base con `override val` en cada variante, ni el límite de la herencia simple ante un segundo contrato. |
| 5 | Intermedia | Reparte bien `data object` / `data class` según si hay parámetros. No conoce la consecuencia en memoria: el singleton emite sin alocar, la data class sin propiedades aloca una instancia por emisión. |

**Nivel global: Intermedio** (1 Senior, 2 intermedias, 2 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Intermedio.

Ya domina: la exhaustividad del when sobre una jerarquía sellada y, sobre todo, por qué el else la anula — identificó por su cuenta que con else el subtipo nuevo cae silenciosamente en esa rama en vez de romper la compilación, que es el punto que más se pregunta en entrevistas. También tiene el criterio por defecto correcto, sealed interface, con la razón estructural correcta: una clase implementa muchas interfaces pero hereda de una sola clase. Y reparte bien data object y data class según si la variante necesita parámetros. Esos tres puntos se pueden tratar como repaso rápido.

Necesita explicación en profundidad: qué le da exactamente la palabra sealed al compilador — el conjunto cerrado de subtipos conocido en tiempo de compilación, que es lo que habilita la verificación de exhaustividad — y cuál es el precio: todos los subtipos directos tienen que declararse en el mismo paquete y módulo, así que nadie fuera del módulo puede extender la jerarquía; la conexión entre eso y los tipos de datos algebraicos, para que el término no aparezca suelto; qué puede una sealed class que una sealed interface no puede, que es la dirección que le falta a su comparación: propiedades en el constructor o abstract val, métodos con implementación compartida, bloque init y companion object — una interfaz no tiene constructor ni estado; el patrón concreto de declarar las propiedades compartidas una sola vez como abstract val en la base y proveerlas con override val en el constructor primario de cada data class, y el caso donde la herencia simple se queda corta y hay que sumar interfaces para un segundo contrato como analytics; y qué significa en memoria que un data object sea un singleton: emitirlo miles de veces por un StateFlow crea cero objetos nuevos, mientras que una data class sin propiedades alocaría uno por emisión y le daría trabajo al recolector de basura, además de darle un toString legible y una igualdad donde la estructural y la referencial coinciden.

Malentendidos a corregir: ninguno detectado. Las respuestas dadas fueron correctas hasta donde llegaron; lo que falta es alcance, no corrección.

Instrucción para el Audio Overview: explicá desde cero, con analogías, qué gana el compilador con el conjunto cerrado de subtipos y qué restricción de paquete y módulo se paga a cambio, después todo lo que una sealed class puede hacer y una sealed interface no (constructor, abstract val, init, companion object) con el ejemplo de propiedades compartidas declaradas una sola vez, y por último qué significa en memoria que un data object sea un singleton frente a una data class sin propiedades; tratá la exhaustividad del when, el problema del else y el criterio por defecto de sealed interface como repaso de una frase.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Sealed Classes vs Sealed Interfaces

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/sealed-classes-interfaces/

**Artículo relacionado (agregar como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/data-objects/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/sealed-class/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sealed-interface/
https://aghmnl.github.io/senior-forge-codex/es/glosario/when-expression/
https://aghmnl.github.io/senior-forge-codex/es/glosario/constructor/
https://aghmnl.github.io/senior-forge-codex/es/glosario/init/
https://aghmnl.github.io/senior-forge-codex/es/glosario/inheritance/
https://aghmnl.github.io/senior-forge-codex/es/glosario/protected-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/compile-time/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sealed-hierarchy/
https://aghmnl.github.io/senior-forge-codex/es/glosario/algebraic-data-types/
https://aghmnl.github.io/senior-forge-codex/es/glosario/allocations/
https://aghmnl.github.io/senior-forge-codex/es/glosario/equals/
https://aghmnl.github.io/senior-forge-codex/es/glosario/to-string/
https://aghmnl.github.io/senior-forge-codex/es/glosario/data-object/
https://aghmnl.github.io/senior-forge-codex/es/glosario/singleton/
https://aghmnl.github.io/senior-forge-codex/es/glosario/stateflow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/abstract-class/
https://aghmnl.github.io/senior-forge-codex/es/glosario/primary-constructor/
https://aghmnl.github.io/senior-forge-codex/es/glosario/jvm/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mvi-pattern/
https://aghmnl.github.io/senior-forge-codex/es/glosario/unidirectional-data-flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/state-emission-patterns/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/sealed-classes.html
https://kotlinlang.org/docs/interfaces.html
https://kotlinlang.org/docs/inheritance.html
https://kotlinlang.org/docs/control-flow.html
https://kotlinlang.org/docs/object-declarations.html
https://kotlinlang.org/docs/whatsnew15.html
https://kotlinlang.org/docs/data-classes.html
https://kotlinlang.org/docs/visibility-modifiers.html
https://developer.android.com/topic/architecture/ui-layer
https://developer.android.com/topic/architecture/ui-layer/events
https://developer.android.com/develop/ui/compose/performance/stability

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Sealed Classes vs Sealed Interfaces
2. Agregá el artículo principal y el artículo relacionado como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Intermedio.

Ya domina: la exhaustividad del when sobre una jerarquía sellada y, sobre todo, por qué el else la anula — identificó por su cuenta que con else el subtipo nuevo cae silenciosamente en esa rama en vez de romper la compilación, que es el punto que más se pregunta en entrevistas. También tiene el criterio por defecto correcto, sealed interface, con la razón estructural correcta: una clase implementa muchas interfaces pero hereda de una sola clase. Y reparte bien data object y data class según si la variante necesita parámetros. Esos tres puntos se pueden tratar como repaso rápido.

Necesita explicación en profundidad: qué le da exactamente la palabra sealed al compilador — el conjunto cerrado de subtipos conocido en tiempo de compilación, que es lo que habilita la verificación de exhaustividad — y cuál es el precio: todos los subtipos directos tienen que declararse en el mismo paquete y módulo, así que nadie fuera del módulo puede extender la jerarquía; la conexión entre eso y los tipos de datos algebraicos, para que el término no aparezca suelto; qué puede una sealed class que una sealed interface no puede, que es la dirección que le falta a su comparación: propiedades en el constructor o abstract val, métodos con implementación compartida, bloque init y companion object — una interfaz no tiene constructor ni estado; el patrón concreto de declarar las propiedades compartidas una sola vez como abstract val en la base y proveerlas con override val en el constructor primario de cada data class, y el caso donde la herencia simple se queda corta y hay que sumar interfaces para un segundo contrato como analytics; y qué significa en memoria que un data object sea un singleton: emitirlo miles de veces por un StateFlow crea cero objetos nuevos, mientras que una data class sin propiedades alocaría uno por emisión y le daría trabajo al recolector de basura, además de darle un toString legible y una igualdad donde la estructural y la referencial coinciden.

Malentendidos a corregir: ninguno detectado. Las respuestas dadas fueron correctas hasta donde llegaron; lo que falta es alcance, no corrección.

Instrucción para el Audio Overview: explicá desde cero, con analogías, qué gana el compilador con el conjunto cerrado de subtipos y qué restricción de paquete y módulo se paga a cambio, después todo lo que una sealed class puede hacer y una sealed interface no (constructor, abstract val, init, companion object) con el ejemplo de propiedades compartidas declaradas una sola vez, y por último qué significa en memoria que un data object sea un singleton frente a una data class sin propiedades; tratá la exhaustividad del when, el problema del else y el criterio por defecto de sealed interface como repaso de una frase.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Sealed classes and interfaces | La referencia completa: la restricción de paquete y módulo, la exhaustividad del `when`, y la diferencia entre sealed class y sealed interface. |
| Interfaces | Qué puede y qué no puede declarar una interfaz — sin constructor ni estado — y por qué una clase puede implementar varias. |
| Inheritance | La herencia simple de la JVM, que es la razón estructural por la que una clase extiende una sola sealed class. |
| Conditions and loops | `when` como expresión vs. como sentencia, y cuándo el compilador exige exhaustividad. |
| Object declarations | `object` y `data object` como miembros sin estado de una jerarquía sellada. |
| What's new in Kotlin 1.5 | La versión que introdujo `sealed interface` y relajó la restricción al módulo completo. |
| Data classes | Qué genera una `data class`, que es lo que llevan las variantes con payload. |
| Visibility modifiers | El alcance de la restricción sellada: qué significa "mismo paquete y módulo". |
| UI layer (Android) | El patrón de `UiState` sellado como fuente única de verdad de una pantalla. |
| UI events | Eventos y acciones modelados como jerarquías selladas en la capa de UI. |
| Stability in Compose | Por qué los miembros sin estado y las variantes inmutables ayudan a saltear recomposiciones. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Sealed Classes vs Sealed Interfaces", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Qué gana el compilador cuando una jerarquía es `sealed` y no simplemente `abstract` u `open`? ¿Qué restricción impone a cambio?
2. Un `when` sobre una jerarquía sellada sin rama `else`. Agregás un subtipo nuevo y no tocás nada más. ¿Qué pasa al compilar, y qué habría pasado si el `when` tuviera `else`?
3. `sealed class` y `sealed interface`: ¿qué podés hacer con una que no podés con la otra, en las dos direcciones? ¿Cuál usás por defecto y por qué?
4. Tenés tres acciones que comparten `taskId` y `childCount`. ¿Cómo las modelás para no repetir esos campos en cada variante? ¿Y si además cada acción tuviera que implementar un contrato de analytics?
5. Dentro de una jerarquía sellada, ¿cuándo declarás un miembro como `data object` y cuándo como `data class`? ¿Qué cambia en memoria cuando ese estado se emite miles de veces por un `StateFlow`?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: el compilador conoce el conjunto cerrado de subtipos y verifica exhaustividad sin else; a cambio, todos los subtipos directos van en el mismo paquete y módulo. Es la forma Kotlin de un ADT. Junior: no distingue sealed de abstract/open.
- P2 Senior: sin else el when deja de compilar y señala cada lugar sin cubrir; con else compila y el subtipo nuevo cae silenciosamente ahí, convirtiendo un error de compilación en un bug de runtime. Intermedio: no ve por qué el else es peor.
- P3 Senior: sealed class permite estado, constructor, init y companion; sealed interface no, pero se pueden implementar varias mientras que solo se hereda de una clase. Por defecto sealed interface. Junior: las cree equivalentes.
- P4 Senior: sealed class con abstract val declarados una vez y override en cada data class; si además hace falta un contrato de analytics, la herencia simple no alcanza y entran las interfaces. Intermedio: no resuelve el segundo requisito.
- P5 Senior: data object para variantes sin datos, data class para las que llevan payload; el data object es singleton, así que emitirlo miles de veces crea cero objetos, más toString legible e igualdad consistente. Junior: usa data class para todo.
```
