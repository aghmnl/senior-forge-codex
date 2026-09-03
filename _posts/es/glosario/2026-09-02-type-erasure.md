---
layout: post
title: "Type Erasure"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/type-erasure/
---

## The Theory (El Qué)

**Type erasure** (borrado de tipos) es el mecanismo de la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) para implementar [generics]({{ "/es/01-kotlin-core/generics-variance-reification/" | relative_url }}): los [parámetros de tipo genérico]({{ "/es/glosario/generic-type-parameters/" | relative_url }}) existen solo en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}) y se eliminan (borran) del [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}). Un `List<String>` y un `List<Int>` son ambos simplemente `List` a nivel de JVM. Esto significa que no podés chequear `is List<String>` en runtime — el argumento de tipo ya no existe.

```kotlin
// Not found in FAS — standalone example
fun checkType(list: List<*>) {
    // if (list is List<String>) { }  // ERROR: No se puede chequear un tipo borrado
    if (list is List<*>) { }          // OK: star-projection sobrevive al erasure
}
```

Los parámetros de tipo [`reified`]({{ "/es/glosario/reified/" | relative_url }}) de Kotlin en [inline functions]({{ "/es/glosario/inline-functions/" | relative_url }}) son el workaround: dado que el cuerpo de la función se inlinea en el call site, el compilador sustituye el tipo concreto directamente en el [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}), evitando el erasure.

```kotlin
// reified preserva el parámetro de tipo en runtime
inline fun <reified T> List<*>.filterIsInstanceTyped(): List<T> =
    filterIsInstance<T>()

val strings: List<String> = mixedList.filterIsInstanceTyped<String>()
```

## The Senior Nuance (El Matiz Senior)

- Type erasure significa que los chequeos de tipo genérico (`is T`) y la creación de clases genéricas (`T()`) son imposibles en runtime sin [reified]({{ "/es/glosario/reified/" | relative_url }}). Por eso el `Gson().fromJson<MyType>(json)` de Android requiere un `TypeToken` — es un workaround para el erasure que captura el tipo en el call site.
- En Kotlin, podés chequear `is List<*>` (star projection) pero no `is List<String>`. El `*` dice "no me importa el argumento de tipo" — compila a un chequeo de tipo raw.
- El erasure causa "bridge methods": cuando una clase `StringList : List<String>` sobreescribe `get(index: Int): String`, la JVM también genera un método puente sintético `get(index: Int): Object` que delega a la versión tipada. Estos bridges son visibles en [stack traces]({{ "/es/glosario/stack-trace/" | relative_url }}) y pueden confundir el debugging.
- La combinación [reified]({{ "/es/glosario/reified/" | relative_url }}) + [inline]({{ "/es/glosario/inline-functions/" | relative_url }}) de Kotlin es la única forma a nivel de JVM de escapar del type erasure. Funciona pegando el tipo concreto en el [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) del call site, así que el tipo nunca se pasa realmente como parámetro — queda hardcodeado.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
