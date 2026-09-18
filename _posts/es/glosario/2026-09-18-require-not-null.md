---
layout: post
title: "requireNotNull"
date: 2026-09-18 12:00:00 +0000
categories: [es, glosario]
tags: [null-safety, error-handling]
lang: es
permalink: /es/glosario/require-not-null/
---

## The Theory (El Qué)

**`requireNotNull(value) { "mensaje" }`** lanza `IllegalArgumentException` si `value` es null y, si no, lo devuelve como tipo no-nulo. Es [`require`]({{ "/es/glosario/require/" | relative_url }}) especializado en nullabilidad, y la alternativa explícita a `!!` cuando un *argumento* null es un bug del llamador. Su [contract]({{ "/es/glosario/contract/" | relative_url }}) (`returns() implies (value != null)`) hace que después de la llamada la variable original también quede smart-casteada ([Smart Casts]({{ "/es/01-kotlin-core/smart-casts/" | relative_url }})) a no-nulo — podés usar el valor de retorno o seguir usando la variable.

```kotlin
// Not found in FAS — standalone example
fun openTask(taskId: String?) {
    val id = requireNotNull(taskId) { "openTask necesita un taskId" }   // id: String
    // taskId también queda smart-casteado a String de acá en adelante
    repository.load(id)
}
```

## The Senior Nuance (El Matiz Senior)

- **El mensaje es todo el punto.** `taskId!!` y `requireNotNull(taskId)` crashean con el mismo input; solo el segundo deja un [stack trace]({{ "/es/glosario/stack-trace/" | relative_url }}) que dice *qué* se esperaba. Convierte una [`NullPointerException`]({{ "/es/glosario/null-pointer-exception/" | relative_url }}) genérica en una precondición con nombre.
- **Preferí rediseñar cuando puedas.** Si un parámetro nunca debe ser null, declaralo `String` y dejá que el sistema de tipos rechace la llamada en [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}). `requireNotNull` es para bordes donde el tipo nullable viene impuesto (APIs Java, extras de `Intent`, [platform types]({{ "/es/glosario/platform-types/" | relative_url }})).
- **Argumento → `requireNotNull`; estado → [`checkNotNull`]({{ "/es/glosario/check-not-null/" | relative_url }}).** La misma regla que `require` vs. `check`.
- Ver [Smart Casts]({{ "/es/01-kotlin-core/smart-casts/" | relative_url }}) y [Null Safety]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
