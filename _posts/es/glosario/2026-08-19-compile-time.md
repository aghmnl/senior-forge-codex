---
layout: post
title: "Compile Time"
date: 2026-08-19 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/compile-time/
---

## La Teoría (El Qué)

**Compile time** (tiempo de compilación) es la fase en la que el código fuente se traduce a bytecode (en la JVM) o código máquina (en compilación nativa). Durante esta fase, el compilador realiza verificación de tipos, inferencia de tipos, resolución de sobrecarga, borrado de tipos genéricos (type erasure), procesamiento de anotaciones (kapt/KSP) y optimización. Los errores detectados en compile time — type mismatches, referencias sin resolver, violaciones de exhaustividad en `when` — son los más baratos de corregir porque previenen que el código se ejecute incorrectamente.

## El Matiz Senior

- La filosofía de diseño de Kotlin empuja la mayor cantidad de verificaciones posible a compile time: null safety, exhaustividad en `when` con sealed classes, [smart casts]({{ "/es/01-kotlin-core/smart-casts/" | relative_url }}) y parámetros de tipo `reified` son todos mecanismos de compile time que eliminan categorías enteras de errores de runtime.
- Las **extension functions** se resuelven en compile time basándose en el tipo declarado del receptor, no en su tipo en runtime. Esta es una distinción clave respecto del dispatch de métodos virtuales (que ocurre en runtime).
- El **procesamiento de anotaciones** (kapt, KSP) se ejecuta en compile time para generar código — los grafos de dependencias de Dagger/Hilt, las implementaciones de DAOs de Room y los adaptadores de Moshi son todos generados en compile time.
- Las **constantes de compile time** (`const val`) se insertan directamente en el bytecode, evitando cualquier búsqueda en runtime. Solo primitivos y `String` califican.
- Entender el límite compile time vs. runtime ayuda a explicar por qué los genéricos se borran (la JVM no retiene parámetros de tipo en runtime) y por qué `reified` solo funciona con funciones `inline` (el compilador sustituye el tipo real en cada sitio de llamada).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
