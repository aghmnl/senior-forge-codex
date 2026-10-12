---
topic: "Recomposition & Stability"
chapter: 03-jetpack-compose
slug: recomposition-stability
lang: es
article: /es/03-jetpack-compose/recomposition-stability/
diagnostic_date: 2026-10-09
---

# Notebook de estudio — Recomposition & Stability

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. Un composable lee `count`, que es un `MutableState`. Cuando `count` cambia, ¿qué vuelve a ejecutarse: toda la pantalla, solo el composable que lo leyó, o algo más?
2. Un composable recibe un parámetro `tasks: List<Task>`. ¿Por qué Compose considera ese parámetro *unstable*, aunque en tu código la lista nunca se modifique?
3. ¿Qué es el *strong skipping* de Compose, y qué cambió con él para los parámetros unstable?
4. ¿Qué hacen las anotaciones `@Immutable` y `@Stable` sobre una clase, y qué riesgo tienen si se usan mal?
5. Un composable registra un evento de analytics llamando a `analytics.log("screen_shown")` directamente en su cuerpo. ¿Qué problema tiene eso?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | Solo se recompone el **scope que leyó** el estado (registrado por el **snapshot system**). Ese scope vuelve a llamar a sus hijos, y cada hijo cuyos argumentos son iguales a los anteriores **se saltea** (skipping). | Sabe que no se recompone toda la pantalla pero no precisa que es el scope que leyó el estado, ni menciona el skipping de los hijos. | Cree que se recompone toda la pantalla. |
| 2 | `List` es una **interfaz**: la instancia detrás podría ser un `MutableList` que cambia sin avisarle a la composition, así que Compose no puede garantizar que `equals` sea confiable ni que los cambios notifiquen. El tipo no promete inmutabilidad. | Intuye que el tipo no garantiza la inmutabilidad pero no explica lo de la interfaz y `MutableList`. | No sabe por qué. |
| 3 | Modo activado por defecto desde **Kotlin 2.0.20**: los parámetros unstable ya no impiden saltear; se comparan **por instancia (`===`)** y los stable por `equals`. Las lambdas se recuerdan automáticamente. Consecuencia: importa pasar **la misma instancia** cuando nada cambió. | Sabe que mejora el skipping pero no la comparación por instancia. | No lo conoce. |
| 4 | Le dicen al compilador que trate la clase como **stable**, sin verificarlo: son una **promesa**. Si la clase tiene internos mutables que no notifican, Compose saltea cuando no debería y la UI muestra **datos viejos**. | Sabe que marcan estabilidad pero no ve el riesgo. | No las conoce. |
| 5 | Es un **efecto secundario** en el cuerpo: Compose puede recomponer muchas veces, en cualquier orden, o descartar una recomposition, así que el log corre una cantidad **impredecible** de veces. Va en `LaunchedEffect`/`SideEffect` o en un callback de evento. | Sabe que "se puede repetir" pero no lo relaciona con la recomposition ni sabe dónde moverlo. | Ve otro problema (estilo, hardcodeo) y no el efecto secundario. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior a Senior; 3+ intermedias o mezcla a Intermedio; 3+ junior o "no sé" a Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-10-09

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Intermedio | "Sólo los composables que se ven afectados por el cambio de ese estado." Va en la dirección correcta, pero no precisa que se recompone el scope que **leyó** el estado ni menciona el skipping de los hijos. |
| 2 | Intermedio | "Aunque no se modifique, no se lo estoy diciendo con el tipo de dato." Capta la idea central (el tipo no promete inmutabilidad), pero no explica que `List` es una interfaz detrás de la cual puede haber un `MutableList`. |
| 3 | Junior | "No sé". No conoce el strong skipping ni la comparación por instancia. |
| 4 | Junior | "No sé". No conoce `@Immutable`/`@Stable` ni que son promesas sin verificación. |
| 5 | Junior | "Está hardcodeado, no puede reutilizarse con otro mensaje." Ve un problema de diseño y no el efecto secundario en la composition. |

**Nivel global: Junior** (0 Senior, 2 intermedias, 3 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior, con buena intuición en los fundamentos.

Ya domina: la idea general de que un cambio de estado no recompone toda la pantalla, y que el tipo List no le promete a Compose que la lista sea inmutable. Conviene apoyarse en esas intuiciones y precisarlas.

Necesita explicación en profundidad, desde cero: que se recompone exactamente el scope que leyó el estado, gracias al snapshot system, y cómo los hijos con argumentos iguales se saltean (skipping); por qué List es unstable (es una interfaz y la instancia podría ser un MutableList) y las tres reglas de un tipo stable; el strong skipping, activado por defecto desde Kotlin 2.0.20, que compara los parámetros unstable por instancia y recuerda las lambdas, y por qué una lista creada con filter durante la composition impide el skipping; qué hacen @Immutable y @Stable, que son promesas sin verificación que pueden mostrar datos viejos; y por qué el cuerpo de un composable tiene que estar libre de efectos secundarios.

Malentendidos a corregir: ante analytics.log("screen_shown") en el cuerpo de un composable, el problema no es que el mensaje esté hardcodeado, sino que es un efecto secundario: Compose puede recomponer muchas veces o descartar una recomposition, así que el log corre una cantidad impredecible de veces; va en LaunchedEffect o SideEffect, o en un callback de evento.

Instrucción para el Audio Overview: partí de la intuición que ya tiene sobre qué se recompone y precisala con el snapshot system y el skipping; después explicá desde cero, con analogías (un corrector que solo relee los párrafos que cambiaron y se saltea los que son idénticos), la stability, el strong skipping y la comparación por instancia; y cerrá con @Stable/@Immutable como promesas y con los efectos secundarios en el cuerpo de un composable.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Recomposition & Stability

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/03-jetpack-compose/recomposition-stability/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/immutability-atomic-state/
https://aghmnl.github.io/senior-forge-codex/es/01-kotlin-core/collections-mutability/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/jetpack-compose/
https://aghmnl.github.io/senior-forge-codex/es/glosario/composable/
https://aghmnl.github.io/senior-forge-codex/es/glosario/composition/
https://aghmnl.github.io/senior-forge-codex/es/glosario/recomposition/
https://aghmnl.github.io/senior-forge-codex/es/glosario/snapshot-system/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mutable-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/skipping/
https://aghmnl.github.io/senior-forge-codex/es/glosario/stability/
https://aghmnl.github.io/senior-forge-codex/es/glosario/equals/
https://aghmnl.github.io/senior-forge-codex/es/glosario/primitives/
https://aghmnl.github.io/senior-forge-codex/es/glosario/string/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lambdas/
https://aghmnl.github.io/senior-forge-codex/es/glosario/val/
https://aghmnl.github.io/senior-forge-codex/es/glosario/var/
https://aghmnl.github.io/senior-forge-codex/es/glosario/list/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sets/
https://aghmnl.github.io/senior-forge-codex/es/glosario/maps/
https://aghmnl.github.io/senior-forge-codex/es/glosario/mutable-list/
https://aghmnl.github.io/senior-forge-codex/es/glosario/kotlin/
https://aghmnl.github.io/senior-forge-codex/es/glosario/strong-skipping/
https://aghmnl.github.io/senior-forge-codex/es/glosario/referential-equality/
https://aghmnl.github.io/senior-forge-codex/es/glosario/layout-inspector/
https://aghmnl.github.io/senior-forge-codex/es/glosario/compose-compiler-reports/
https://aghmnl.github.io/senior-forge-codex/es/glosario/viewmodel/
https://aghmnl.github.io/senior-forge-codex/es/glosario/copy/
https://aghmnl.github.io/senior-forge-codex/es/glosario/remember/
https://aghmnl.github.io/senior-forge-codex/es/glosario/modifier-offset/
https://aghmnl.github.io/senior-forge-codex/es/glosario/derived-state/
https://aghmnl.github.io/senior-forge-codex/es/glosario/immutable-annotation/
https://aghmnl.github.io/senior-forge-codex/es/glosario/stable/
https://aghmnl.github.io/senior-forge-codex/es/glosario/launched-effect/
https://aghmnl.github.io/senior-forge-codex/es/glosario/side-effect/
https://aghmnl.github.io/senior-forge-codex/es/glosario/disposable-effect/
https://aghmnl.github.io/senior-forge-codex/es/glosario/filter/
https://aghmnl.github.io/senior-forge-codex/es/glosario/map-operator/

**Fuentes oficiales (agregar cada una como fuente web)**
https://developer.android.com/develop/ui/compose/lifecycle
https://developer.android.com/develop/ui/compose/phases
https://developer.android.com/develop/ui/compose/performance/stability
https://developer.android.com/develop/ui/compose/performance/stability/strongskipping
https://developer.android.com/develop/ui/compose/performance/stability/diagnose
https://developer.android.com/develop/ui/compose/performance/stability/fix
https://developer.android.com/develop/ui/compose/performance/bestpractices
https://developer.android.com/develop/ui/compose/side-effects

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Recomposition & Stability
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior, con buena intuición en los fundamentos.

Ya domina: la idea general de que un cambio de estado no recompone toda la pantalla, y que el tipo List no le promete a Compose que la lista sea inmutable. Conviene apoyarse en esas intuiciones y precisarlas.

Necesita explicación en profundidad, desde cero: que se recompone exactamente el scope que leyó el estado, gracias al snapshot system, y cómo los hijos con argumentos iguales se saltean (skipping); por qué List es unstable (es una interfaz y la instancia podría ser un MutableList) y las tres reglas de un tipo stable; el strong skipping, activado por defecto desde Kotlin 2.0.20, que compara los parámetros unstable por instancia y recuerda las lambdas, y por qué una lista creada con filter durante la composition impide el skipping; qué hacen @Immutable y @Stable, que son promesas sin verificación que pueden mostrar datos viejos; y por qué el cuerpo de un composable tiene que estar libre de efectos secundarios.

Malentendidos a corregir: ante analytics.log("screen_shown") en el cuerpo de un composable, el problema no es que el mensaje esté hardcodeado, sino que es un efecto secundario: Compose puede recomponer muchas veces o descartar una recomposition, así que el log corre una cantidad impredecible de veces; va en LaunchedEffect o SideEffect, o en un callback de evento.

Instrucción para el Audio Overview: partí de la intuición que ya tiene sobre qué se recompone y precisala con el snapshot system y el skipping; después explicá desde cero, con analogías (un corrector que solo relee los párrafos que cambiaron y se saltea los que son idénticos), la stability, el strong skipping y la comparación por instancia; y cerrá con @Stable/@Immutable como promesas y con los efectos secundarios en el cuerpo de un composable.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Lifecycle of composables | Qué es la composition, cómo se recompone y cuándo se saltea un composable. |
| Compose phases | Composition, layout y dibujo, y cómo diferir una lectura de estado a una fase posterior. |
| Stability | Las reglas de un tipo stable y por qué `List` es unstable. |
| Strong skipping | Qué cambió con el strong skipping: comparación por instancia y lambdas recordadas. |
| Diagnose stability issues | Layout Inspector y Compose compiler reports para encontrar qué no se saltea. |
| Fix stability issues | Inmutabilidad, colecciones inmutables, `@Immutable`/`@Stable` y el archivo de configuración. |
| Best practices | `remember`, `derivedStateOf`, leer el estado lo más tarde posible. |
| Side-effects | Por qué el cuerpo de un composable no debe tener efectos, y `LaunchedEffect`, `SideEffect`, `DisposableEffect`. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Recomposition & Stability", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. Un composable lee `count`, que es un `MutableState`. Cuando `count` cambia, ¿qué vuelve a ejecutarse: toda la pantalla, solo el composable que lo leyó, o algo más?
2. Un composable recibe un parámetro `tasks: List<Task>`. ¿Por qué Compose considera ese parámetro *unstable*, aunque en tu código la lista nunca se modifique?
3. ¿Qué es el *strong skipping* de Compose, y qué cambió con él para los parámetros unstable?
4. ¿Qué hacen las anotaciones `@Immutable` y `@Stable` sobre una clase, y qué riesgo tienen si se usan mal?
5. Un composable registra un evento de analytics llamando a `analytics.log("screen_shown")` directamente en su cuerpo. ¿Qué problema tiene eso?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: se recompone el scope que leyó el estado (snapshot system), y los hijos con argumentos iguales se saltean. Junior: cree que se recompone toda la pantalla.
- P2 Senior: List es una interfaz; detrás puede haber un MutableList que cambia sin avisar, así que Compose no puede garantizar que sea stable. Junior: no sabe por qué.
- P3 Senior: strong skipping, por defecto desde Kotlin 2.0.20; los parámetros unstable se comparan por instancia (===) y las lambdas se recuerdan. Junior: no lo conoce.
- P4 Senior: @Immutable y @Stable hacen que el compilador trate la clase como stable sin verificarlo; si la clase muta sin notificar, la UI muestra datos viejos. Junior: no las conoce.
- P5 Senior: es un efecto secundario en el cuerpo; corre una cantidad impredecible de veces con cada recomposition; va en LaunchedEffect, SideEffect o un callback. Junior: ve otro problema y no el efecto secundario.
```
