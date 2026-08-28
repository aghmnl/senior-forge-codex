---
layout: post
title: "Código Fuente"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/source-code/
---

## The Theory (El Qué)

El **código fuente** es el texto legible por humanos que los programadores escriben en un lenguaje de programación (Kotlin, Java, C, etc.). Es la entrada del compilador, que lo traduce a [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) o código máquina en [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}). El código fuente es donde se expresan todas las decisiones de diseño — definiciones de tipos, algoritmos, arquitectura. Se versiona en repositorios (Git), se revisa en pull requests, y es la única fuente de verdad de lo que hace un programa.

## The Senior Nuance (El Matiz Senior)

- El código fuente es lo que existe **antes** de la compilación. Después del [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}), se convierte en [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) (en la [JVM]({{ "/es/glosario/jvm/" | relative_url }})) o código máquina nativo. Muchas features de Kotlin (extension functions, data classes, parámetros por defecto) existen solo en código fuente — se desugarizan o transforman durante la compilación.
- El [procesamiento de anotaciones]({{ "/es/glosario/annotation-processing/" | relative_url }}) lee anotaciones del código fuente y genera código fuente *adicional* (o bytecode) en tiempo de compilación. El código generado se compila junto con el código escrito a mano.
- El código fuente y el bytecode pueden divergir significativamente: una `data class` de Kotlin con cinco propiedades genera funciones `equals()`, `hashCode()`, `toString()`, `copy()` y `componentN()` en bytecode que son invisibles en el código fuente. Entender esta brecha es clave para depurar código decompilado.
- En Kotlin Multiplatform, el mismo código fuente (en `commonMain`) compila a bytecode JVM, JavaScript o binarios nativos dependiendo del target — el código fuente es platform-agnostic, la salida no lo es.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
