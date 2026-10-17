---
topic: "Modifiers: Order & Alignment"
chapter: 03-jetpack-compose
slug: modifiers-order-alignment
lang: es
article: /es/03-jetpack-compose/modifiers-order-alignment/
diagnostic_date: 2026-10-16
---

# Notebook de estudio — Modifiers: Order & Alignment

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. ¿Qué tamaño termina teniendo `Box(Modifier.size(100.dp).size(50.dp))`, y por qué?
2. Un ícono de cerrar tiene `Modifier.size(18.dp).clickable { onClose() }`. ¿Por qué puede ser difícil de tocar, y cómo lo arreglarías sin cambiar cómo se ve?
3. En un `Row`, ¿qué diferencia hay entre `horizontalArrangement` y `verticalAlignment`?
4. ¿Por qué `Modifier.align(Alignment.TopStart)` no se puede usar en cualquier composable, sino solo en algunos?
5. En un `Row` con un texto y un ícono, ¿para qué sirve ponerle `Modifier.weight(1f)` al texto?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | **100 dp**: los modifiers de tamaño trabajan con **constraints** que bajan por la cadena; el primer `size` fija el tamaño y el segundo ya no lo puede cambiar. **Gana el primero.** Para forzar otro tamaño se usa `requiredSize`. | Acierta el tamaño pero no lo explica con constraints. | Cree que mide 50 dp. |
| 2 | El área táctil es de **18 dp**, por debajo del **mínimo de 48 dp** de accesibilidad. Se agranda sin cambiar el aspecto con **`minimumInteractiveComponentSize()`**, o poniendo el **`clickable` antes de un padding** para que el padding también sea tocable. | Ve que el área es chica pero no sabe cómo agrandarla. | No ve el problema. |
| 3 | `horizontalArrangement` **distribuye** a los hijos sobre el **eje principal** del `Row` (inicio, `SpaceBetween`, `spacedBy`). `verticalAlignment` **posiciona** a cada hijo sobre el **eje transversal** (arriba, centro, abajo). Uno decide el espacio entre ellos; el otro, dónde queda cada uno. | Sabe que uno es horizontal y otro vertical, pero no la diferencia entre distribuir el grupo y posicionar cada hijo. | No sabe. |
| 4 | Porque `align` es un **modifier de scope**: solo existe adentro de `BoxScope` (o con un solo eje, en `RowScope` y `ColumnScope`). El padre es quien decide la posición, así que solo se puede pedir dentro de un padre que la soporte, y el compilador impide usarlo en otro lugar. | Sabe que depende del padre pero no menciona los scopes. | No sabe. |
| 5 | `weight(1f)` le da al texto **el espacio que sobra** después de medir a los hijos sin peso. El ícono queda con su tamaño y el texto ocupa el resto, lo que empuja el ícono al final y deja que el texto se recorte o haga salto de línea en lugar de empujar al ícono afuera. | Sabe que "ocupa espacio" pero no que es el espacio restante. | No sabe. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior a Senior; 3+ intermedias o mezcla a Intermedio; 3+ junior o "no sé" a Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-10-16

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Junior | "No sé". No conoce que gana el primer tamaño ni las constraints. |
| 2 | Intermedio | "El espacio de 18 dp es muy pequeño. Se le puede agrandar la superficie clickeable pero no sé cómo." Ve el problema, sin el mínimo de 48 dp ni `minimumInteractiveComponentSize()` o el orden de `clickable` y padding. |
| 3 | Intermedio | "Uno es la alineación horizontal y otra la vertical." Correcto en la dirección, pero no distingue distribuir el grupo en el eje principal de posicionar cada hijo en el transversal. |
| 4 | Junior | "No sé". No conoce los modifiers de scope. |
| 5 | Junior | "No sé". No conoce `weight`. |

**Nivel global: Junior** (0 Senior, 2 intermedias, 3 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Junior, con intuiciones correctas sobre el área táctil y los ejes.

Ya domina: la idea de que un elemento clickeable de 18 dp es demasiado chico para tocarlo, y que en un Row hay una configuración horizontal y otra vertical. Conviene precisar esas dos intuiciones.

Necesita explicación en profundidad, desde cero: que una cadena de modifiers es ordenada y cada modifier envuelve a los siguientes, de afuera hacia adentro (padding antes de background es un margen; clickable antes de padding agranda el área táctil; clip antes de clickable redondea el ripple); cómo los modifiers de tamaño trabajan con constraints y por qué gana el primer size; el mínimo de 48 dp y minimumInteractiveComponentSize(); la diferencia entre arrangement (distribuir el grupo en el eje principal) y alignment (posicionar cada hijo en el eje transversal) en Row, Column y Box; los modifiers de scope como align y weight; cómo weight reparte el espacio restante; y la convención del parámetro modifier aplicado primero en la raíz.

Malentendidos a corregir: horizontalArrangement y verticalAlignment no son solo "horizontal y vertical": uno distribuye a todos los hijos sobre el eje principal y el otro posiciona a cada hijo sobre el eje transversal.

Instrucción para el Audio Overview: partí de sus intuiciones sobre el área táctil y los ejes; explicá desde cero, con analogías (capas de una cebolla, de afuera hacia adentro), el orden de los modifiers y las constraints; después arrangement frente a alignment, align y weight; y cerrá con la convención del parámetro modifier.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Modifiers: Order & Alignment

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/03-jetpack-compose/modifiers-order-alignment/

**Artículos relacionados (agregar cada uno como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/03-jetpack-compose/state-hoisting/
https://aghmnl.github.io/senior-forge-codex/es/03-jetpack-compose/recomposition-stability/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/modifier/
https://aghmnl.github.io/senior-forge-codex/es/glosario/padding/
https://aghmnl.github.io/senior-forge-codex/es/glosario/background/
https://aghmnl.github.io/senior-forge-codex/es/glosario/touch-target/
https://aghmnl.github.io/senior-forge-codex/es/glosario/ripple/
https://aghmnl.github.io/senior-forge-codex/es/glosario/clickable/
https://aghmnl.github.io/senior-forge-codex/es/glosario/clip/
https://aghmnl.github.io/senior-forge-codex/es/glosario/constraints/
https://aghmnl.github.io/senior-forge-codex/es/glosario/fill-max-width/
https://aghmnl.github.io/senior-forge-codex/es/glosario/wrap-content-size/
https://aghmnl.github.io/senior-forge-codex/es/glosario/required-size/
https://aghmnl.github.io/senior-forge-codex/es/glosario/row/
https://aghmnl.github.io/senior-forge-codex/es/glosario/arrangement/
https://aghmnl.github.io/senior-forge-codex/es/glosario/main-axis-cross-axis/
https://aghmnl.github.io/senior-forge-codex/es/glosario/alignment/
https://aghmnl.github.io/senior-forge-codex/es/glosario/column/
https://aghmnl.github.io/senior-forge-codex/es/glosario/box/
https://aghmnl.github.io/senior-forge-codex/es/glosario/layout-scopes/
https://aghmnl.github.io/senior-forge-codex/es/glosario/weight/
https://aghmnl.github.io/senior-forge-codex/es/glosario/lambdas/
https://aghmnl.github.io/senior-forge-codex/es/glosario/modifier-offset/
https://aghmnl.github.io/senior-forge-codex/es/glosario/graphics-layer/
https://aghmnl.github.io/senior-forge-codex/es/glosario/draw-behind/
https://aghmnl.github.io/senior-forge-codex/es/glosario/compose-phases/
https://aghmnl.github.io/senior-forge-codex/es/glosario/composition/

**Fuentes oficiales (agregar cada una como fuente web)**
https://developer.android.com/develop/ui/compose/modifiers
https://developer.android.com/develop/ui/compose/layouts/basics
https://developer.android.com/develop/ui/compose/layouts/constraints-modifiers
https://developer.android.com/develop/ui/compose/accessibility/api-defaults

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Modifiers: Order & Alignment
2. Agregá el artículo principal y los artículos relacionados como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Junior, con intuiciones correctas sobre el área táctil y los ejes.

Ya domina: la idea de que un elemento clickeable de 18 dp es demasiado chico para tocarlo, y que en un Row hay una configuración horizontal y otra vertical. Conviene precisar esas dos intuiciones.

Necesita explicación en profundidad, desde cero: que una cadena de modifiers es ordenada y cada modifier envuelve a los siguientes, de afuera hacia adentro (padding antes de background es un margen; clickable antes de padding agranda el área táctil; clip antes de clickable redondea el ripple); cómo los modifiers de tamaño trabajan con constraints y por qué gana el primer size; el mínimo de 48 dp y minimumInteractiveComponentSize(); la diferencia entre arrangement (distribuir el grupo en el eje principal) y alignment (posicionar cada hijo en el eje transversal) en Row, Column y Box; los modifiers de scope como align y weight; cómo weight reparte el espacio restante; y la convención del parámetro modifier aplicado primero en la raíz.

Malentendidos a corregir: horizontalArrangement y verticalAlignment no son solo "horizontal y vertical": uno distribuye a todos los hijos sobre el eje principal y el otro posiciona a cada hijo sobre el eje transversal.

Instrucción para el Audio Overview: partí de sus intuiciones sobre el área táctil y los ejes; explicá desde cero, con analogías (capas de una cebolla, de afuera hacia adentro), el orden de los modifiers y las constraints; después arrangement frente a alignment, align y weight; y cerrá con la convención del parámetro modifier.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Compose modifiers | Qué es un modifier, por qué importa el orden y los modifiers de scope (`align`, `weight`). |
| Compose layout basics | `Row`, `Column` y `Box`, con arrangement y alignment. |
| Constraints and modifier order | Cómo las constraints bajan por la cadena y por qué gana el primer tamaño. |
| Accessibility defaults | El tamaño mínimo de 48 dp y `minimumInteractiveComponentSize()`. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Modifiers: Order & Alignment", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. ¿Qué tamaño termina teniendo `Box(Modifier.size(100.dp).size(50.dp))`, y por qué?
2. Un ícono de cerrar tiene `Modifier.size(18.dp).clickable { onClose() }`. ¿Por qué puede ser difícil de tocar, y cómo lo arreglarías sin cambiar cómo se ve?
3. En un `Row`, ¿qué diferencia hay entre `horizontalArrangement` y `verticalAlignment`?
4. ¿Por qué `Modifier.align(Alignment.TopStart)` no se puede usar en cualquier composable, sino solo en algunos?
5. En un `Row` con un texto y un ícono, ¿para qué sirve ponerle `Modifier.weight(1f)` al texto?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: 100 dp; las constraints bajan por la cadena y gana el primer size. Junior: cree que 50 dp.
- P2 Senior: 18 dp está por debajo del mínimo de 48 dp; minimumInteractiveComponentSize() o clickable antes del padding. Junior: no ve el problema.
- P3 Senior: arrangement distribuye el grupo en el eje principal; alignment posiciona cada hijo en el transversal. Junior: no sabe.
- P4 Senior: align es un modifier de scope (BoxScope, RowScope, ColumnScope); el padre decide la posición. Junior: no sabe.
- P5 Senior: weight da el espacio restante tras medir a los hijos sin peso; empuja el ícono al final. Junior: no sabe.
```
