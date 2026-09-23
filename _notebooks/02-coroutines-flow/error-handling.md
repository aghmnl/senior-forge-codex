---
topic: "Error Handling: try-catch & .catch"
chapter: 02-coroutines-flow
slug: error-handling
lang: es
article: /es/02-coroutines-flow/error-handling/
diagnostic_date: 2026-09-23
---

# Notebook de estudio — Error Handling: try-catch & .catch

> Archivo de apoyo para el flujo descrito en `docs/AI_STUDY_PIPELINE.md`.

---

## Bloque 1 — Diagnóstico de nivel (lo administra Claude)

Se responde **en frío, antes de leer el artículo**. "No sé" es una respuesta válida: mide el punto de partida, no penaliza. Claude compara cada respuesta con la rúbrica y redacta el texto "Nivel actual" del Bloque 2.

### Preguntas

1. Tenés `flow.catch { }.collect { }` y la app crashea con el stack trace apuntando adentro del bloque `collect`. ¿Por qué no lo atrapó el `.catch`?
2. Un compañero envuelve el cuerpo de cada coroutine en `try { ... } catch (e: Exception) { log(e) }` para que "nada pueda crashear". ¿Qué problema tiene eso?
3. `flow { try { emit(load()) } catch (e: IOException) { emit(fallback()) } }` — ¿esto funciona? Si no, ¿qué pasa cuando alguien lo colecta y cómo se escribe correctamente?
4. Un repositorio atrapa una `SQLiteConstraintException` y devuelve el string "Algo salió mal". ¿Qué problema le ves a eso? ¿Dónde debería traducirse la excepción a un mensaje de usuario?
5. Un gesto de drag necesita restaurar el estado visual si la coroutine se cancela a mitad del arrastre. ¿Podés atrapar la `CancellationException` para hacer esa limpieza? Si sí, ¿qué es obligatorio hacer después?

### Rúbrica

| Nº | Respuesta Senior (incluye) | Respuesta intermedia (le falta) | Señal junior |
|---|---|---|---|
| 1 | `catch` solo maneja excepciones de su **upstream**: el builder y los operadores declarados arriba. El bloque `collect` está **downstream**, así que queda fuera de su alcance y la excepción se propaga a la coroutine que lo contiene. Arreglo según la intención: si el trabajo que falla es parte del pipeline, se mueve a un `onEach`/`map` **arriba** del `catch`; si es trabajo del consumidor, lleva su propio `try/catch` adentro del `collect`. Menciona que envolver todo el `collect` en un `try/catch` también atraparía la cancelación. | Sabe que "catch no cubre el collect" pero no nombra upstream/downstream ni propone los dos arreglos. | No sabe por qué no lo atrapó. |
| 2 | En la JVM `CancellationException` es una `RuntimeException`, así que `catch (e: Exception)` **se traga la señal de cancelación**: la coroutine sobrevive a su propia cancelación, el scope nunca completa, y una pantalla cerrada sigue trabajando — la concurrencia estructurada deja de funcionar. Además, atrapar `Exception` de forma genérica esconde qué falló realmente. La alternativa son catches estrechos, o un `if (e is CancellationException) throw e` al principio del bloque. | Identifica que generalizar `Exception` es malo y sospecha del efecto sobre las coroutines, pero no nombra `CancellationException` ni explica que el scope queda sin completar. | No ve problema; cree que "así no crashea". |
| 3 | No funciona: viola la **transparencia a las excepciones**. Un builder `flow { }` no puede atrapar sus propias emisiones; al colectarlo lanza `IllegalStateException: Flow exception transparency is violated`. La forma correcta es dejar el productor transparente y manejar la falla downstream: `flow { emit(load()) }.catch { emit(fallback()) }`. | Intuye que "no se puede hacer eso adentro del flow" pero no nombra la invariante ni sabe que el error es en runtime. | Cree que funciona bien. |
| 4 | Destruye la única información accionable: el tipo concreto de la excepción, el constraint violado, el stack trace. La capa de datos debe dejar viajar las excepciones técnicas; la traducción a mensaje de usuario ocurre **una sola vez, en el borde de la UI**, donde se conoce la pantalla, el copy y el idioma — un `Throwable.toUserMessage()` que mapea `SQLiteConstraintException` con "UNIQUE" a "etiqueta duplicada" y el resto a un mensaje genérico. Menciona que además devolver un String rompe la localización y la telemetría. | Sabe que "se pierde información" pero no ubica dónde debería traducirse ni menciona localización/telemetría. | No ve problema. |
| 5 | Sí, y es el único motivo válido para atraparla: liberar algo que la coroutine posee. Es **obligatorio relanzarla** (`throw e`) para que la cancelación siga propagándose al padre y la concurrencia estructurada se mantenga. Menciona que `finally` cubre la mayoría de los casos y que el catch explícito es para cuando la limpieza depende de *por qué* terminó la coroutine. | Dice que se puede atrapar y relanzar pero no explica qué se rompe si no se relanza, o no distingue el caso de `finally`. | Atrapa y no relanza, o cree que no se puede atrapar nunca. |

### Cómo redactar "Nivel actual"

Claude produce un texto de 8–12 líneas en español con esta forma:

- **Nivel global**: Junior / Intermedio / Senior, según cuántas respuestas caen en cada columna (3+ Senior a Senior; 3+ intermedias o mezcla a Intermedio; 3+ junior o "no sé" a Junior).
- **Ya domina**: lista de los conceptos respondidos a nivel Senior (el notebook puede darlos por sabidos).
- **Necesita explicación en profundidad**: conceptos de las respuestas intermedias/junior, nombrados con el término exacto del glosario.
- **Malentendidos a corregir**: afirmaciones incorrectas concretas que aparecieron en las respuestas, si las hubo.
- **Instrucción para el Audio Overview**: una línea del estilo "Explicá X e Y desde cero con analogías; tratá Z como repaso rápido".

### Resultado — 2026-09-23

| Nº | Nivel | Observación |
|---|---|---|
| 1 | Junior | "No sé". No conoce la asimetría upstream/downstream del operador `catch`. |
| 2 | Intermedia | "Puede no manejar correctamente las corrutinas y generaliza la Exception": intuición correcta en ambas mitades, pero sin nombrar `CancellationException` ni explicar que el scope nunca completa. |
| 3 | Junior | "No sé". No conoce la transparencia a las excepciones ni el error de runtime que produce. |
| 4 | Junior | "No sé". No identifica la pérdida de información ni dónde corresponde traducir. |
| 5 | Senior | Correcto y completo: se puede atrapar, y hay que relanzarla inmediatamente para que el padre se entere. |

**Nivel global: Intermedio** (1 Senior, 1 intermedia, 3 junior).

**Texto "Nivel actual" entregado a Gemini:**

```text
Nivel global: Intermedio.

Ya domina: el patrón correcto para atrapar una CancellationException — sabe que se puede atrapar para limpiar y que hay que relanzarla inmediatamente para que el padre se entere, que es el punto exacto que se pregunta en entrevistas. También detecta que envolver todo en catch (e: Exception) es problemático, tanto por generalizar el tipo de excepción como por interferir con el manejo de las coroutines, aunque sin nombrar el mecanismo. Esos dos puntos se pueden tratar como repaso breve.

Necesita explicación en profundidad: la asimetría de catch, que solo ve su upstream — el builder y los operadores declarados arriba — y por qué una excepción lanzada adentro del bloque collect, que está downstream, queda fuera de su alcance, con los dos arreglos posibles según sea trabajo del pipeline o del consumidor; el mecanismo concreto detrás de su intuición sobre catch (e: Exception), que es que en la JVM CancellationException es una RuntimeException y por lo tanto el catch amplio se traga la señal de cancelación, dejando la coroutine viva después de que su scope fue cancelado y rompiendo la concurrencia estructurada, con la misma trampa en runCatching, que atrapa Throwable; la transparencia a las excepciones como invariante de Flow: por qué un builder flow no puede envolver su propio emit en un try/catch, qué error de runtime produce y cuál es la forma correcta de manejar la falla downstream con catch; y dónde traducir una excepción técnica a un mensaje de usuario, que es una sola vez en el borde de la UI y no en la capa de datos, porque atraparla abajo destruye el tipo concreto, el stack trace y la posibilidad de localizar el mensaje.

Malentendidos a corregir: ninguno. La respuesta sobre catch (e: Exception) fue vaga pero apunta en la dirección correcta; conviene darle el nombre del mecanismo en vez de corregirla.

Instrucción para el Audio Overview: explicá desde cero, con analogías, por qué catch solo alcanza al upstream y qué hacer cuando lo que falla es el collect, después por qué CancellationException es una RuntimeException y qué se rompe exactamente cuando un catch amplio se la traga, después la transparencia a las excepciones y el error que produce envolver un emit en try/catch, y por último dónde traducir excepciones técnicas a mensajes de usuario; tratá el patrón de atrapar la cancelación y relanzarla como repaso de una frase, porque ya lo tiene.
```

---

## Bloque 2 — Prompt para Gemini (crear el notebook)

Pegar completo en el chat de Gemini. El paso 5 ya contiene el texto "Nivel actual" del último diagnóstico (Bloque 1); si se repite la nivelación, actualizarlo.

```text
**Contexto**
Estoy preparando entrevistas técnicas de Senior Android Developer. Necesito que crees mi notebook de estudio en Gemini Notebook para el tema de hoy. Toda la interacción y todo texto generado debe estar en español latinoamericano. No investigues ni busques nada: todas las fuentes ya están listadas abajo. Tu trabajo es solo crear el notebook, agregar exactamente esas fuentes y crear un documento de texto con el contenido que te doy.

**Tema**
Error Handling: try-catch & .catch

**Artículo principal**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/error-handling/

**Artículo relacionado (agregar como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/02-coroutines-flow/flow-cold-streams/

**Fuentes de glosario (agregar cada una como fuente web)**
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutines/
https://aghmnl.github.io/senior-forge-codex/es/glosario/suspend-functions/
https://aghmnl.github.io/senior-forge-codex/es/glosario/call-stack/
https://aghmnl.github.io/senior-forge-codex/es/glosario/try-catch/
https://aghmnl.github.io/senior-forge-codex/es/glosario/run-catching/
https://aghmnl.github.io/senior-forge-codex/es/glosario/result/
https://aghmnl.github.io/senior-forge-codex/es/glosario/flow/
https://aghmnl.github.io/senior-forge-codex/es/glosario/catch/
https://aghmnl.github.io/senior-forge-codex/es/glosario/upstream/
https://aghmnl.github.io/senior-forge-codex/es/glosario/collect/
https://aghmnl.github.io/senior-forge-codex/es/glosario/downstream/
https://aghmnl.github.io/senior-forge-codex/es/glosario/emit/
https://aghmnl.github.io/senior-forge-codex/es/glosario/exception-transparency/
https://aghmnl.github.io/senior-forge-codex/es/glosario/runtime/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cancellation-exception/
https://aghmnl.github.io/senior-forge-codex/es/glosario/job/
https://aghmnl.github.io/senior-forge-codex/es/glosario/cooperative-cancellation/
https://aghmnl.github.io/senior-forge-codex/es/glosario/on-each/
https://aghmnl.github.io/senior-forge-codex/es/glosario/jvm/
https://aghmnl.github.io/senior-forge-codex/es/glosario/runtime-exception/
https://aghmnl.github.io/senior-forge-codex/es/glosario/coroutine-scope/
https://aghmnl.github.io/senior-forge-codex/es/glosario/throwable/
https://aghmnl.github.io/senior-forge-codex/es/glosario/finally/
https://aghmnl.github.io/senior-forge-codex/es/glosario/sqlite-constraint-exception/
https://aghmnl.github.io/senior-forge-codex/es/glosario/state-holder/
https://aghmnl.github.io/senior-forge-codex/es/glosario/error-state/

**Fuentes oficiales (agregar cada una como fuente web)**
https://kotlinlang.org/docs/exceptions.html
https://kotlinlang.org/docs/exception-handling.html
https://kotlinlang.org/docs/cancellation-and-timeouts.html
https://kotlinlang.org/docs/flow.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/catch.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/retry-when.html
https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/-cancellation-exception/
https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/run-catching.html
https://kotlinlang.org/api/core/kotlin-stdlib/kotlin/-result/
https://developer.android.com/kotlin/coroutines/coroutines-best-practices
https://developer.android.com/topic/architecture/ui-layer
https://developer.android.com/kotlin/flow

**Pasos de ejecución**
1. Creá un notebook nuevo en Gemini Notebook llamado exactamente: Error Handling: try-catch & .catch
2. Agregá el artículo principal y el artículo relacionado como fuentes web.
3. Agregá cada una de las fuentes de glosario listadas como fuente web, una por una. No agregues ninguna URL que no esté en esta lista.
4. Agregá cada una de las fuentes oficiales listadas como fuente web, una por una.
5. Creá una fuente de texto dentro del notebook llamada "Nivel actual" con exactamente el siguiente contenido (no lo resumas ni lo reescribas):

Nivel global: Intermedio.

Ya domina: el patrón correcto para atrapar una CancellationException — sabe que se puede atrapar para limpiar y que hay que relanzarla inmediatamente para que el padre se entere, que es el punto exacto que se pregunta en entrevistas. También detecta que envolver todo en catch (e: Exception) es problemático, tanto por generalizar el tipo de excepción como por interferir con el manejo de las coroutines, aunque sin nombrar el mecanismo. Esos dos puntos se pueden tratar como repaso breve.

Necesita explicación en profundidad: la asimetría de catch, que solo ve su upstream — el builder y los operadores declarados arriba — y por qué una excepción lanzada adentro del bloque collect, que está downstream, queda fuera de su alcance, con los dos arreglos posibles según sea trabajo del pipeline o del consumidor; el mecanismo concreto detrás de su intuición sobre catch (e: Exception), que es que en la JVM CancellationException es una RuntimeException y por lo tanto el catch amplio se traga la señal de cancelación, dejando la coroutine viva después de que su scope fue cancelado y rompiendo la concurrencia estructurada, con la misma trampa en runCatching, que atrapa Throwable; la transparencia a las excepciones como invariante de Flow: por qué un builder flow no puede envolver su propio emit en un try/catch, qué error de runtime produce y cuál es la forma correcta de manejar la falla downstream con catch; y dónde traducir una excepción técnica a un mensaje de usuario, que es una sola vez en el borde de la UI y no en la capa de datos, porque atraparla abajo destruye el tipo concreto, el stack trace y la posibilidad de localizar el mensaje.

Malentendidos a corregir: ninguno. La respuesta sobre catch (e: Exception) fue vaga pero apunta en la dirección correcta; conviene darle el nombre del mecanismo en vez de corregirla.

Instrucción para el Audio Overview: explicá desde cero, con analogías, por qué catch solo alcanza al upstream y qué hacer cuando lo que falla es el collect, después por qué CancellationException es una RuntimeException y qué se rompe exactamente cuando un catch amplio se la traga, después la transparencia a las excepciones y el error que produce envolver un emit en try/catch, y por último dónde traducir excepciones técnicas a mensajes de usuario; tratá el patrón de atrapar la cancelación y relanzarla como repaso de una frase, porque ya lo tiene.

6. Respondé con la URL del notebook y la lista de fuentes que se agregaron correctamente, indicando cuáles fallaron, si alguna.
```

### Para qué sirve cada fuente oficial

| Fuente | Aporta |
|---|---|
| Exceptions | Cómo funcionan las excepciones en Kotlin: `try/catch/finally` como expresión, ausencia de checked exceptions y el tipo `Nothing`. |
| Coroutine exceptions handling | La propagación de excepciones entre padre e hijo, `CoroutineExceptionHandler` y el rol de `SupervisorJob`. |
| Cancellation and timeouts | Por qué la cancelación es cooperativa, qué es `CancellationException` y por qué nunca hay que tragársela. |
| Asynchronous Flow | La sección de excepciones de Flow: transparencia, `catch` y por qué el productor no puede atrapar sus propias emisiones. |
| `catch` (API) | El contrato exacto: solo upstream, puede emitir un valor de respaldo, y relanza la cancelación automáticamente. |
| `retryWhen` (API) | Reintento con acceso a la causa y al número de intento, la pieza que va arriba del `catch`. |
| `CancellationException` (API) | El tipo que representa la cancelación normal y su lugar en la jerarquía de excepciones. |
| `runCatching` (API) | Qué atrapa exactamente — `Throwable` — que es la razón por la que es peligroso en código de coroutines. |
| `Result` (API) | El contenedor de éxito o falla, y cuándo conviene devolverlo en vez de lanzar. |
| Best practices for coroutines | La guía de Android sobre dónde manejar errores y por qué la capa de datos no debería traducirlos. |
| UI layer | Cómo se modela un estado de error en la UI, para que una falla no quede en un log. |
| Kotlin flows on Android | El manejo de errores de un flow en el contexto de la arquitectura de Android. |

---

## Bloque 3 — Vía alternativa: Gemini administra el diagnóstico

Solo si se quiere probar sin pasar por Claude. Menos confiable: Gemini tiene que juzgar respuestas contra la rúbrica.

**Prompt A** (pegar y responder las preguntas en el chat):

```text
Estoy preparando entrevistas técnicas de Senior Android Developer. Antes de crear mi notebook de estudio sobre "Error Handling: try-catch & .catch", hacéme exactamente estas cinco preguntas, una por una, en español latinoamericano. No agregues preguntas, no expliques las respuestas y no crees nada todavía. Esperá mi respuesta a las cinco.

1. Tenés `flow.catch { }.collect { }` y la app crashea con el stack trace apuntando adentro del bloque `collect`. ¿Por qué no lo atrapó el `.catch`?
2. Un compañero envuelve el cuerpo de cada coroutine en `try { ... } catch (e: Exception) { log(e) }` para que "nada pueda crashear". ¿Qué problema tiene eso?
3. `flow { try { emit(load()) } catch (e: IOException) { emit(fallback()) } }` — ¿esto funciona? Si no, ¿qué pasa cuando alguien lo colecta y cómo se escribe correctamente?
4. Un repositorio atrapa una `SQLiteConstraintException` y devuelve el string "Algo salió mal". ¿Qué problema le ves a eso? ¿Dónde debería traducirse la excepción a un mensaje de usuario?
5. Un gesto de drag necesita restaurar el estado visual si la coroutine se cancela a mitad del arrastre. ¿Podés atrapar la `CancellationException` para hacer esa limpieza? Si sí, ¿qué es obligatorio hacer después?
```

**Prompt B** (después de responder): pegar el Bloque 2 completo, pero reemplazando el paso 5 por:

```text
5. Compará mis cinco respuestas anteriores con esta rúbrica y creá una fuente de texto dentro del notebook llamada "Nivel actual" (8–12 líneas, español latinoamericano) con: nivel global (Junior / Intermedio / Senior), qué ya domino, qué necesita explicación en profundidad (usando los términos exactos del glosario), malentendidos concretos a corregir, y una instrucción de una línea para el Audio Overview sobre qué explicar desde cero y qué tratar como repaso.

Rúbrica:
- P1 Senior: catch solo ve su upstream; el bloque collect está downstream y queda fuera; se arregla subiendo el trabajo a onEach/map o con un try/catch propio adentro del collect. Junior: no sabe por qué.
- P2 Senior: CancellationException es una RuntimeException, así que catch (e: Exception) se traga la cancelación, el scope nunca completa y la concurrencia estructurada se rompe; runCatching tiene la misma trampa con Throwable. Intermedio: intuye el problema sin nombrar el mecanismo.
- P3 Senior: no funciona, viola la transparencia a las excepciones y lanza en runtime; lo correcto es dejar el productor transparente y manejar la falla con catch downstream. Junior: cree que funciona.
- P4 Senior: se pierde el tipo concreto, el stack trace y la localización; la traducción va una sola vez en el borde de la UI con algo tipo Throwable.toUserMessage(). Junior: no ve problema.
- P5 Senior: sí se puede atrapar para limpiar, y es obligatorio relanzarla con throw e para que la cancelación siga propagándose al padre. Junior: atrapa y no relanza.
```
