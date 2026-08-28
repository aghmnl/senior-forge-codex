---
layout: post
title: "Resolución de Sobrecarga"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/overload-resolution/
---

## The Theory (El Qué)

La **resolución de sobrecarga** es el proceso de [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}) mediante el cual el compilador determina qué función llamar cuando múltiples funciones comparten el mismo nombre pero difieren en tipos de parámetros, cantidad de parámetros o tipo de receptor. El compilador evalúa todos los candidatos, aplica coincidencia de tipos e [inferencia de tipos]({{ "/es/glosario/type-inference/" | relative_url }}), y selecciona la coincidencia más específica. Si ningún candidato es el más específico, la llamada es ambigua y el build falla.

## The Senior Nuance (El Matiz Senior)

- La resolución de sobrecarga es puramente una decisión de compile-time. El [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) contiene una llamada directa a la función resuelta — no hay dispatch ni búsqueda en [tiempo de ejecución]({{ "/es/glosario/runtime/" | relative_url }}) (a diferencia del dispatch de métodos virtuales, que *sí* es un mecanismo de runtime).
- Las [extension functions]({{ "/es/glosario/extension-functions/" | relative_url }}) participan en la resolución de sobrecarga, pero las funciones miembro siempre ganan sobre las extensiones cuando las firmas coinciden. Esto es una decisión de diseño deliberada: agregar una extensión no puede sobreescribir silenciosamente un miembro.
- Los parámetros por defecto reducen la necesidad de sobrecargas en Kotlin. Donde Java requiere múltiples sobrecargas de constructor/método para parámetros opcionales, Kotlin usa `fun f(x: Int, y: String = "")` — una función en lugar de dos.
- `@JvmOverloads` genera sobrecargas JVM reales a partir de funciones con parámetros por defecto para interop con Java. El compilador crea N+1 sobrecargas (donde N es la cantidad de parámetros con valor por defecto), cada una llamando a la siguiente.
- La sobrecarga de operadores (`operator fun plus(other: T)`) sigue las mismas reglas de resolución — el compilador resuelve `a + b` como `a.plus(b)` en tiempo de compilación basándose en los tipos declarados.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
