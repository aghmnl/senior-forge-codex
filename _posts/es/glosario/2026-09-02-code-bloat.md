---
layout: post
title: "Code Bloat"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/code-bloat/
---

## The Theory (El Qué)

**Code bloat** (inflación de código) es el aumento indeseable en el tamaño del binario compilado causado por duplicación de código, inlining excesivo, o boilerplate generado. En Kotlin/Android, la fuente principal de code bloat es el uso agresivo de funciones [`inline`]({{ "/es/glosario/inline-functions/" | relative_url }}): cada call site recibe una copia completa del [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) de la función, así que una función inline grande llamada en 50 lugares produce 50 copias en el archivo `.dex` final.

```
// Conceptual: qué hace inline al tamaño del binario
// Source: una función, 20 instrucciones de bytecode
inline fun heavyOperation(block: () -> Unit) { /* 20 instrucciones */ }

// 50 call sites × 20 instrucciones = 1,000 instrucciones en el DEX
// vs. 1 función + 50 instrucciones de llamada = ~70 instrucciones sin inline
```

## The Senior Nuance (El Matiz Senior)

- El trade-off de las [inline functions]({{ "/es/glosario/inline-functions/" | relative_url }}) es evitación de [allocation]({{ "/es/glosario/allocations/" | relative_url }}) vs. code bloat. Las funciones utilitarias pequeñas (1–5 líneas) son candidatas ideales para `inline` — la copia de bytecode es diminuta y el ahorro de [allocations]({{ "/es/glosario/allocations/" | relative_url }}) es real. Las funciones grandes con lógica compleja no deberían inlinearse, incluso si aceptan [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}).
- En Android, el code bloat impacta directamente el tamaño del APK/AAB y el method count del DEX. El límite de 65K métodos por archivo DEX (antes de multidex) y el tamaño de descarga de la app se ven afectados. R8 (el optimizador de build-time) puede mitigar parcialmente el bloat a través de eliminación de dead-code y method outlining, pero la prevención es mejor que la cura.
- Los frameworks de [annotation processing]({{ "/es/glosario/annotation-processing/" | relative_url }}) ([Hilt]({{ "/es/glosario/hilt/" | relative_url }}), Room, Moshi) generan código en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}), lo que contribuye al bloat. Es un trade-off consciente: el código generado provee type safety y evita reflection en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}), pero aumenta el tamaño del binario. Monitoreá el output generado en proyectos grandes.
- El `data class` de Kotlin genera `equals()`, `hashCode()`, `toString()`, `copy()` y funciones `componentN()` para cada data class. En un proyecto con cientos de data classes, esto contribuye bloat medible. Usá data classes solo cuando necesitás su comportamiento generado, no como default para toda clase.
- El formato Android App Bundle (AAB) mitiga el bloat en tiempo de delivery sirviendo solo los recursos y librerías nativas necesarias para cada dispositivo. Pero el code bloat en el DEX sigue afectando a todos los usuarios por igual.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
