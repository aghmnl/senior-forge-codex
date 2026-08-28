---
layout: post
title: "Funciones Inline"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/inline-functions/
---

## The Theory (El Qué)

Una **función inline** es una función marcada con la palabra clave `inline` que el compilador de Kotlin copia (inserta) en cada sitio de llamada durante el [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}), en lugar de generar una llamada a función regular. El cuerpo de la función — y crucialmente, cualquier parámetro lambda — se sustituyen directamente en el [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) del llamador. Esto elimina el overhead de crear objetos lambda y la llamada indirecta a `invoke()`, haciendo de las funciones inline el mecanismo detrás de las abstracciones de costo cero en Kotlin.

## The Senior Nuance (El Matiz Senior)

- El beneficio principal de `inline` es el **inlining de lambdas**, no el cuerpo de la función en sí. Sin `inline`, cada lambda crea una instancia de clase anónima en la [JVM]({{ "/es/glosario/jvm/" | relative_url }}). Con `inline`, el código de la lambda se pega directamente en el sitio de llamada — sin allocation de objetos, sin dispatch virtual.
- Los parámetros de tipo [`reified`]({{ "/es/glosario/reified/" | relative_url }}) son **solo** posibles con funciones inline. Como el cuerpo de la función se copia en cada sitio de llamada, el compilador puede sustituir el argumento de tipo real — sorteando el type erasure de la JVM que normalmente elimina la información de tipo genérico del bytecode.
- `noinline` marca un parámetro lambda que *no* debe ser inlined (ej., cuando necesita almacenarse en un field o pasarse a una función no-inline). `crossinline` marca una lambda que será inlined pero llamada desde un contexto donde los retornos no-locales están prohibidos (ej., dentro de otra lambda).
- Las funciones de scoping de la biblioteca estándar de Kotlin (`let`, `run`, `with`, `apply`, `also`) son todas `inline`. Esto significa que usar `someValue.let { transform(it) }` compila al mismo bytecode que escribir la transformación directamente — cero overhead.
- Abusar de `inline` en funciones grandes aumenta el tamaño del bytecode (el cuerpo se duplica en cada sitio de llamada). El compilador advierte cuando `inline` no provee beneficio (sin parámetros lambda, sin tipos reified).

```kotlin
// Not found in FAS — standalone example
inline fun <reified T> List<*>.filterByType(): List<T> =
    filterIsInstance<T>()

val strings = listOf("a", 1, "b", 2).filterByType<String>()
// El compilador inserta el cuerpo Y sustituye String por T en este sitio de llamada
```

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
