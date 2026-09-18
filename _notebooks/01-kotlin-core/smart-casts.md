---
topic: "Smart Casts"
chapter: 01-kotlin-core
slug: smart-casts
lang: es
article: /es/01-kotlin-core/smart-casts/
diagnostic_date: 2026-09-18
---

# Notebook de estudio — Smart Casts

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Qué es un smart cast? ¿Qué tiene que "ver" el compilador para aplicarlo y qué te ahorra respecto a Java?
2. `class Repo { var cache: Any? = null; fun size() = if (cache is List<*>) cache.size else 0 }` — ¿compila? Si no, ¿por qué exactamente y cuál es el arreglo idiomático?
3. `val x: String? = ...; requireNotNull(x); println(x.length)` — ¿compila la última línea? ¿Qué mecanismo hace que el compilador sepa que `x` ya no es null después de una llamada a función?
4. En un `when (state)` sobre una jerarquía `sealed`, ¿qué te da el smart cast dentro de cada rama y qué te da la exhaustividad? ¿Qué pasa si agregás un subtipo nuevo?
5. Tenés `val end: RecurrenceEnd = rule.end` (una interfaz con varios subtipos) y necesitás el `date` de `UntilDate`. ¿Cómo lo obtenés sin que pueda explotar en runtime? ¿Cuándo sí aceptarías un `as` estricto?

### Rúbrica

| # | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | El compilador refina el tipo de una variable después de una verificación (`is`, `!= null`, `!is` con return, `&&`/`\|\|`) siguiendo el grafo de flujo de control, y expone el tipo refinado sin cast manual. Ahorra el `(Foo) obj` que Java exige después de `instanceof`. Aplica solo cuando puede garantizar que el valor no cambió entre el chequeo y el uso. | Sabe que "después de `is` no hace falta castear" pero no menciona el flujo de control ni la condición de estabilidad del valor. | No conoce el término o lo confunde con `as`. |
| 2 | No compila: `cache` es un `var` de propiedad, puede ser reasignado entre el `is` y el `.size` (otro hilo, un callback, un setter), así que el compilador no puede garantizar el tipo. Arreglo: capturar en un `val` local (`val c = cache; if (c is List<*>) c.size else 0`), o `(cache as? List<*>)?.size ?: 0`. Menciona que un `val` con getter custom o `open` tampoco smart-castea. | Sabe que "con var no funciona" pero no explica el porqué (mutación entre chequeo y uso) ni propone la captura en `val` local; o cree que basta con `val` sin importar el getter. | Cree que compila, o no sabe por qué el compilador se queja. |
| 3 | Sí compila. `requireNotNull` (como `require`, `check`, `checkNotNull`) declara un `contract` que le dice al compilador "si esta función retorna normalmente, entonces `x != null`". El compilador aplica el smart cast a `String` después de la llamada. Los contracts permiten escribir funciones propias de validación que también habiliten smart casts. | Sabe que `requireNotNull` "chequea null" pero no sabe que el compilador smart-castea después ni conoce el mecanismo `contract`. | Cree que no compila porque `x` sigue siendo `String?`, o que hay que usar `x!!` después. |
| 4 | Smart cast: dentro de `is Success ->` la variable se trata como `Success` y se accede a sus propiedades sin cast. Exhaustividad: el `when` usado como expresión (o sobre `sealed` desde Kotlin 1.7 también como statement) obliga a cubrir todos los subtipos, sin `else`. Agregar un subtipo rompe la compilación en cada `when` que no lo contemple — es la base del manejo de estado type-safe en MVI. | Conoce el acceso directo a propiedades pero mezcla smart cast con exhaustividad, o no sabe qué pasa al agregar un subtipo (o cree que hay que poner `else`). | No relaciona `when` con `sealed` ni con smart casts. |
| 5 | `(end as? RecurrenceEnd.UntilDate)?.date`: el safe cast devuelve `null` si no es ese subtipo, sin lanzar, y el resultado queda nullable para tratarlo con `?.`/`?:`; o `if (end is UntilDate) end.date else null` con smart cast. `as` estricto solo cuando el fallo es genuinamente imposible por diseño (ya se validó el tipo, o el contrato de la API lo garantiza) y querés que un bug explote con `ClassCastException`. | Usa `as?` pero no articula que el resultado es nullable ni cuándo preferir `as`; o propone `is` + `as` redundante. | Propone `end as UntilDate` sin más, o no conoce `as?`. |

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
| 1 | Junior | "No sé". No conoce el concepto de smart cast. |
| 2 | Junior | "No sé". No conoce la limitación con `var` ni el arreglo con `val` local. |
| 3 | Junior | "No sé". No conoce el mecanismo `contract` ni que `requireNotNull` smart-castea. |
| 4 | Junior | "No sé". No conecta `when` + `sealed` con smart cast ni con exhaustividad. |
| 5 | Junior | "No sé". No conoce `as?` como fallback ni el criterio para `as`. |

**Nivel global: Junior** (5 "no sé"). Tema a estudiar íntegramente desde cero.

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior.

Ya domina: nada que el notebook pueda dar por sabido en este tema. Respondió "no sé" a las cinco preguntas. De la nivelación de Null Safety del mismo día se sabe que conoce el early return con Elvis y la distinción básica nullable / no-nullable, así que el chequeo `!= null` como caso de smart cast se puede apoyar en eso.

Necesita explicación en profundidad, desde cero: qué es un smart cast (el compilador refina el tipo de una variable después de un chequeo `is` o `!= null` siguiendo el flujo de control, sin cast manual, a diferencia de Java después de `instanceof`); la condición de estabilidad: por qué no smart-castea una propiedad `var`, ni un `val` con getter custom, ni una variable capturada en una lambda que la modifique — el valor podría cambiar entre el chequeo y el uso — y el arreglo idiomático de capturar en un `val` local; el mecanismo `contract` con el que `require`, `check`, `requireNotNull` y `checkNotNull` le informan al compilador que después de la llamada la condición es verdadera, habilitando el smart cast; el `when` sobre jerarquías `sealed`: smart cast dentro de cada rama (acceso directo a las propiedades del subtipo) y exhaustividad (el compilador exige cubrir todos los subtipos sin `else`, y agregar un subtipo nuevo rompe la compilación en cada `when` que no lo contemple); y `as` vs `as?` como fallback cuando el smart cast no está disponible: el safe cast devuelve null y produce un tipo nullable, el cast estricto lanza ClassCastException y se reserva para cuando fallar es imposible por diseño.

Malentendidos a corregir: ninguno detectado (no hubo respuestas incorrectas, solo ausencia de respuesta).

Instrucción para el Audio Overview: explicá todo desde cero, con analogías, en este orden: primero qué es un smart cast y por qué existe, después por qué el compilador se niega con `var` y cómo se resuelve con un `val` local, después `when` + `sealed` como el caso de uso estrella en Android, y por último los contracts y el fallback `as?`. No des nada por sabido.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Smart Casts

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/smart-casts/

**Artículo relacionado (agregar como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/sealed-classes-interfaces/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/is-operator/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cast/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sealed-hierarchy/
https://aghmnl.github.io/senior-forge-codex/es/glosario/when-expression/
https://aghmnl.github.io/senior-forge-codex/es/glosario/success-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/type-safety/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mvi-pattern/
https://aghmnl.github.io/senior-forge-codex/es/glosario/val/
https://aghmnl.github.io/senior-forge-codex/es/glosario/var/
https://aghmnl.github.io/senior-forge-codex/es/glosario/getter/
https://aghmnl.github.io/senior-forge-codex/es/glosario/contract/
https://aghmnl.github.io/senior-forge-codex/es/glosario/require/
https://aghmnl.github.io/senior-forge-codex/es/glosario/check/
https://aghmnl.github.io/senior-forge-codex/es/glosario/check-not-null/
https://aghmnl.github.io/senior-forge-codex/es/glosario/require-not-null/
https://aghmnl.github.io/senior-forge-codex/es/glosario/as-safe-cast/
https://aghmnl.github.io/senior-forge-codex/es/glosario/as-cast/
https://aghmnl.github.io/senior-forge-codex/es/glosario/thread/
https://aghmnl.github.io/senior-forge-codex/es/glosario/callbacks/
https://aghmnl.github.io/senior-forge-codex/es/glosario/class-cast-exception/
https://aghmnl.github.io/senior-forge-codex/es/glosario/runtime/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/typecasts.html
https://kotlinlang.org/docs/sealed-classes.html
https://kotlinlang.org/docs/control-flow.html
https://kotlinlang.org/docs/null-safety.html
https://kotlinlang.org/docs/properties.html
https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.contracts/
https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/require.html
https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/check.html
https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/require-not-null.html
https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/check-not-null.html
https://kotlinlang.org/docs/k2-compiler-migration-guide.html
https://developer.android.com/topic/architecture/ui-layer

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Smart Casts
2. Agregá el artículo principal y el artículo relacionado como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior.

Ya domina: nada que el notebook pueda dar por sabido en este tema. Respondió "no sé" a las cinco preguntas. De la nivelación de Null Safety del mismo día se sabe que conoce el early return con Elvis y la distinción básica nullable / no-nullable, así que el chequeo `!= null` como caso de smart cast se puede apoyar en eso.

Necesita explicación en profundidad, desde cero: qué es un smart cast (el compilador refina el tipo de una variable después de un chequeo `is` o `!= null` siguiendo el flujo de control, sin cast manual, a diferencia de Java después de `instanceof`); la condición de estabilidad: por qué no smart-castea una propiedad `var`, ni un `val` con getter custom, ni una variable capturada en una lambda que la modifique — el valor podría cambiar entre el chequeo y el uso — y el arreglo idiomático de capturar en un `val` local; el mecanismo `contract` con el que `require`, `check`, `requireNotNull` y `checkNotNull` le informan al compilador que después de la llamada la condición es verdadera, habilitando el smart cast; el `when` sobre jerarquías `sealed`: smart cast dentro de cada rama (acceso directo a las propiedades del subtipo) y exhaustividad (el compilador exige cubrir todos los subtipos sin `else`, y agregar un subtipo nuevo rompe la compilación en cada `when` que no lo contemple); y `as` vs `as?` como fallback cuando el smart cast no está disponible: el safe cast devuelve null y produce un tipo nullable, el cast estricto lanza ClassCastException y se reserva para cuando fallar es imposible por diseño.

Malentendidos a corregir: ninguno detectado (no hubo respuestas incorrectas, solo ausencia de respuesta).

Instrucción para el Audio Overview: explicá todo desde cero, con analogías, en este orden: primero qué es un smart cast y por qué existe, después por qué el compilador se niega con `var` y cómo se resuelve con un `val` local, después `when` + `sealed` como el caso de uso estrella en Android, y por último los contracts y el fallback `as?`. No des nada por sabido.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Type checks and casts | La referencia completa de smart casts: `is`/`!is`, cuándo aplican (val local, val sin getter custom, var local no capturada), `as` vs `as?`. |
| Sealed classes and interfaces | `when` exhaustivo sobre jerarquías selladas y el smart cast dentro de cada rama. |
| Conditions and loops | `if` y `when` como expresiones, que es donde el flujo de control alimenta el smart cast. |
| Null safety | El smart cast por chequeo de null (`!= null`, `?: return`) como caso particular del mismo mecanismo. |
| Properties | Getters custom, `open` y `var`: por qué una propiedad puede no ser estable para el compilador. |
| `kotlin.contracts` (API) | El mecanismo `contract` que permite que una función habilite smart casts en el llamador. |
| `require` / `check` (API) | Precondiciones e invariantes con contract: después de la llamada la condición se asume verdadera. |
| `requireNotNull` / `checkNotNull` (API) | Las funciones que smart-castean a no-nulo con un mensaje explicativo, en vez de `!!`. |
| K2 compiler migration guide | Las mejoras de smart cast del compilador K2 (Kotlin 2.0): variables locales, `\|\|`, inline lambdas, propiedades de otras clases. |
| UI layer (Android) | El patrón de `UiState` sellado consumido con `when` + smart cast, base del manejo de estado type-safe. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Smart Casts", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Qué es un smart cast? ¿Qué tiene que "ver" el compilador para aplicarlo y qué te ahorra respecto a Java?
2. `class Repo { var cache: Any? = null; fun size() = if (cache is List<*>) cache.size else 0 }` — ¿compila? Si no, ¿por qué exactamente y cuál es el arreglo idiomático?
3. `val x: String? = ...; requireNotNull(x); println(x.length)` — ¿compila la última línea? ¿Qué mecanismo hace que el compilador sepa que `x` ya no es null después de una llamada a función?
4. En un `when (state)` sobre una jerarquía `sealed`, ¿qué te da el smart cast dentro de cada rama y qué te da la exhaustividad? ¿Qué pasa si agregás un subtipo nuevo?
5. Tenés `val end: RecurrenceEnd = rule.end` (una interfaz con varios subtipos) y necesitás el `date` de `UntilDate`. ¿Cómo lo obtenés sin que pueda explotar en runtime? ¿Cuándo sí aceptarías un `as` estricto?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: el compilador refina el tipo tras un chequeo siguiendo el flujo de control, sin cast manual (a diferencia de Java tras `instanceof`); solo si el valor es estable entre chequeo y uso. Junior: lo confunde con `as`.
- P2 Senior: no compila porque `cache` es `var` y puede cambiar entre el `is` y el uso; capturar en `val` local o usar `as?`. Junior: cree que compila.
- P3 Senior: compila; `requireNotNull` tiene un `contract` que garantiza `x != null` si retorna. Junior: cree que hace falta `!!`.
- P4 Senior: smart cast = acceso directo a propiedades del subtipo; exhaustividad = el `when` obliga a cubrir todos los subtipos sin `else` y un subtipo nuevo rompe la compilación. Intermedio: mezcla ambas cosas.
- P5 Senior: `(end as? UntilDate)?.date` o `is` + smart cast; `as` estricto solo cuando fallar es imposible por diseño. Junior: `end as UntilDate` sin más.
```
