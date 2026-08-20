---
layout: post
title: "Tiempo de Compilación"
date: 2026-08-19 12:00:00 +0000
categories: [es, glossary]
lang: es
permalink: /es/glosario/compile-time/
---

## The Theory (El Qué)

El **tiempo de compilación** es la fase en la que el código fuente se traduce a bytecode (en la JVM) o código máquina (en compilación nativa). Durante esta fase, el compilador realiza verificación de tipos, inferencia de tipos, resolución de sobrecarga, borrado de tipos genéricos, procesamiento de anotaciones (kapt/KSP) y optimización. Los errores detectados en tiempo de compilación — incompatibilidades de tipo, referencias no resueltas, violaciones de exhaustividad en `when` — son los errores más baratos de corregir porque impiden que el código se ejecute incorrectamente.

## The Senior Nuance (El Matiz Senior)

- La filosofía de diseño de Kotlin empuja la mayor cantidad posible de verificaciones al tiempo de compilación: null safety, exhaustividad de `when` con sealed classes, smart casts y parámetros de tipo `reified` son todos mecanismos de tiempo de compilación que eliminan categorías enteras de errores de [tiempo de ejecución]({{ "/es/glosario/runtime/" | relative_url }}).
- Las **extension functions** se resuelven en tiempo de compilación basándose en el tipo declarado del receptor, no en su tipo en runtime. Esta es una distinción clave respecto al dispatch de métodos virtuales (que ocurre en tiempo de ejecución).
- El **procesamiento de anotaciones** (kapt, KSP) se ejecuta en tiempo de compilación para generar código — los grafos de dependencias de Dagger/Hilt, las implementaciones de DAOs de Room y los adaptadores de Moshi se generan todos en tiempo de compilación.
- Las **constantes de compilación** (`const val`) se insertan directamente en el bytecode, evitando cualquier búsqueda en runtime. Solo aplican para primitivos y `String`.
- Entender el límite entre tiempo de compilación y tiempo de ejecución ayuda a explicar por qué los genéricos se borran (la JVM no retiene parámetros de tipo en runtime) y por qué `reified` solo funciona con funciones `inline` (el compilador sustituye el tipo real en cada sitio de llamada).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
