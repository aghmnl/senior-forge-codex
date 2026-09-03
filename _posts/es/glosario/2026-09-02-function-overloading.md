---
layout: post
title: "Function Overloading"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/function-overloading/
---

## The Theory (El Qué)

**Function overloading** (sobrecarga de funciones, [polimorfismo]({{ "/es/glosario/polymorphism/" | relative_url }}) ad-hoc) es la capacidad de definir múltiples funciones con el mismo nombre pero diferentes listas de parámetros. El compilador selecciona qué overload llamar basándose en los tipos y cantidad de argumentos en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}) — esto es [static dispatch]({{ "/es/glosario/static-dispatch/" | relative_url }}), no [virtual dispatch]({{ "/es/glosario/virtual-dispatch/" | relative_url }}). El tipo de retorno solo no diferencia overloads; la firma de parámetros debe diferir.

En Kotlin, los valores de parámetros por defecto frecuentemente eliminan la necesidad de overloads que solo varían en aridad. La anotación `@JvmOverloads` genera los overloads faltantes en [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) para interop con Java.

```kotlin
// Not found in FAS — standalone example
fun format(value: Int): String = value.toString()
fun format(value: Double, decimals: Int = 2): String =
    "%.${decimals}f".format(value)
fun format(value: String): String = "\"$value\""

format(42)          // llama a format(Int)
format(3.14159, 3)  // llama a format(Double, Int)
format("hello")     // llama a format(String)
```

## The Senior Nuance (El Matiz Senior)

- El compilador resuelve overloads vía [overload resolution]({{ "/es/glosario/overload-resolution/" | relative_url }}) — un conjunto de reglas que rankea candidatos por especificidad. Cuando dos overloads son igualmente específicos, la llamada es ambigua y falla en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}). Conocer estas reglas es esencial para diseñar APIs que no sorprendan a los callers.
- Los parámetros por defecto de Kotlin (`fun greet(name: String, greeting: String = "Hello")`) son preferidos sobre los overloads para argumentos opcionales. Reducen el boilerplate y se auto-documentan. Usá true overloading solo cuando los *tipos* de parámetros difieren, no solo cuando necesitás argumentos opcionales.
- Las [extension functions]({{ "/es/glosario/extension-functions/" | relative_url }}) pueden sobrecargarse por [receiver type]({{ "/es/glosario/receiver-type/" | relative_url }}): `fun Int.display()` y `fun String.display()` son overloads válidos. Pero recordá: el dispatch de extension functions es [estático]({{ "/es/glosario/static-dispatch/" | relative_url }}), así que el tipo *declarado* del receiver determina qué overload se ejecuta.
- [Operator overloading]({{ "/es/glosario/operator-overloading/" | relative_url }}) es una forma especializada de function overloading donde el nombre de la función mapea a un operador de Kotlin (`plus`, `invoke`, `contains`). Las reglas son las mismas — el compilador resuelve estáticamente basándose en los tipos de parámetros.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
