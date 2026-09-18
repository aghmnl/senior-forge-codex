---
layout: post
title: "checkNotNull"
date: 2026-09-18 12:00:00 +0000
categories: [es, glosario]
tags: [null-safety, error-handling]
lang: es
permalink: /es/glosario/check-not-null/
---

## The Theory (El Qué)

**`checkNotNull(value) { "mensaje" }`** lanza `IllegalStateException` si `value` es null y, si no, lo devuelve como no-nulo. Es [`check`]({{ "/es/glosario/check/" | relative_url }}) especializado en nullabilidad: usalo cuando un null significa que el *estado propio del objeto* está roto (un campo que debería haberse inicializado, una búsqueda que tiene que encontrar), no que el llamador pasó un argumento malo — eso es [`requireNotNull`]({{ "/es/glosario/require-not-null/" | relative_url }}). Su [contract]({{ "/es/glosario/contract/" | relative_url }}) hace que el compilador smart-castee ([Smart Casts]({{ "/es/01-kotlin-core/smart-casts/" | relative_url }})) la variable chequeada a no-nulo después de la llamada.

```kotlin
// Not found in FAS — standalone example
class SessionHolder {
    private var current: UserSession? = null

    fun currentUserId(): String {
        val session = checkNotNull(current) { "currentUserId() llamado antes de signIn()" }
        return session.userId
    }
}
```

## The Senior Nuance (El Matiz Senior)

- **El estado que "debería" estar es la trampa clásica del `!!`.** `current!!.userId` crashea con una [`NullPointerException`]({{ "/es/glosario/null-pointer-exception/" | relative_url }}) anónima; `checkNotNull` crashea con una oración que nombra la regla de ciclo de vida violada. Mismo comportamiento, debugging mucho más barato.
- **Si *siempre* está inicializado antes de usarse, modelalo.** `lateinit var` (lanza `UninitializedPropertyAccessException` con el nombre de la propiedad) o inyección por constructor eliminan el nullable; `checkNotNull` es para los casos donde null es un estado intermedio legítimo.
- **Valor de retorno o smart cast — ambos sirven.** `val s = checkNotNull(current)` se lee mejor en una cadena; el smart cast sobre `current` solo vale si es un [`val`]({{ "/es/glosario/val/" | relative_url }}) estable — para una propiedad [`var`]({{ "/es/glosario/var/" | relative_url }}) como la de arriba, quedate con la local retornada.
- Ver [Smart Casts]({{ "/es/01-kotlin-core/smart-casts/" | relative_url }}) y [Null Safety]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
