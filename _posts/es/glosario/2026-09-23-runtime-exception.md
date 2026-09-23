---
layout: post
title: "RuntimeException"
date: 2026-09-23 12:00:00 +0000
categories: [es, glosario]
tags: [error-handling, jvm]
lang: es
permalink: /es/glosario/runtime-exception/
---

## The Theory (El Qué)

**`RuntimeException`** es la clase base de la JVM para las excepciones *unchecked* — las que un método no está obligado a declarar y el llamador no está obligado a manejar: `NullPointerException`, `IllegalStateException`, `IllegalArgumentException`. En Kotlin todas las excepciones son unchecked en la práctica, así que la distinción importa menos que en Java, con una excepción filosa: [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}) extiende `RuntimeException`, y por eso un `catch (e: Exception)` amplio se traga la cancelación en silencio.

```kotlin
// Not found in FAS — standalone example
// Atrapa las fallas reales Y la señal de cancelación — la coroutine sobrevive
// a su propia cancelación y el scope nunca completa
try { work() } catch (e: Exception) { log(e) }

// Correcto: dejar pasar la cancelación
try { work() } catch (e: Exception) {
    if (e is CancellationException) throw e
    log(e)
}
```

## The Senior Nuance (El Matiz Senior)

- **"Unchecked" no significa "sin importancia".** Significa que el compilador no te lo va a recordar. En Kotlin, el KDoc y los tests son el único registro de qué puede lanzar una función.
- **La trampa de la cancelación es la consecuencia práctica.** Cualquier catch amplio en código de [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) tiene que dejar pasar la `CancellationException`, y lo mismo vale para [`runCatching`]({{ "/es/glosario/run-catching/" | relative_url }}), que atrapa `Throwable`.
- **Preferí catches estrechos.** Atrapar la excepción que esa llamada puede producir de verdad documenta el modo de falla; atrapar `Exception` no documenta nada.
- Ver [Error Handling: try-catch & .catch]({{ "/es/02-coroutines-flow/error-handling/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
