---
layout: post
title: "Standard Library"
date: 2026-09-03 12:00:00 +0000
categories: [es, glosario]
tags: [collections, functional, inlining]
lang: es
permalink: /es/glosario/standard-library/
---

## The Theory (El Qué)

La **Kotlin Standard Library** (`kotlin-stdlib`) es el conjunto de APIs centrales que viene con todo proyecto Kotlin. Provee tipos fundamentales (`String`, `Int`, [collections]({{ "/es/glosario/collections/" | relative_url }})), funciones utilitarias ([scope functions]({{ "/es/01-kotlin-core/scope-functions/" | relative_url }}), `let`, `run`, `apply`, `also`, `with`), primitivas de I/O, y property delegates (`lazy`, `observable`, `vetoable`, `notNull`).

A diferencia de la standard library de Java, la de Kotlin está diseñada para ser cross-platform: la misma superficie de API está disponible en targets JVM, JS, Native y Wasm. Las extensiones específicas de plataforma (como los paquetes `kotlin.jvm` o `kotlin.js`) están segregadas en subpaquetes.

Áreas clave de la standard library relevantes para desarrollo Android:

- **`kotlin.collections`** — [Collections]({{ "/es/glosario/collections/" | relative_url }}), [Maps]({{ "/es/glosario/maps/" | relative_url }}), [Sets]({{ "/es/glosario/sets/" | relative_url }}), y todas las [extension functions]({{ "/es/glosario/extension-functions/" | relative_url }}) de transformación/filtro/fold.
- **`kotlin.properties`** — `ReadOnlyProperty`, `ReadWriteProperty`, y `Delegates` (usados por [delegated properties]({{ "/es/01-kotlin-core/delegated-properties/" | relative_url }})).
- **`kotlin.text`** — Manipulación de Strings, regex y formateo.
- **`kotlin.sequences`** — Evaluación lazy para pipelines de datos grandes, evitando [allocations]({{ "/es/glosario/allocations/" | relative_url }}) intermedias.

## The Senior Nuance (El Matiz Senior)

- Un Senior distingue entre la standard library (incluida con el compilador de Kotlin, siempre disponible) y las librerías Jetpack/AndroidX (agregadas como dependencias de Gradle). Saber qué vive en `stdlib` evita dependencias innecesarias — por ejemplo, `buildList`, `buildMap`, `groupBy` y `associate` son todas stdlib, no Guava ni Apache Commons.
- La standard library está agresivamente [inlineada]({{ "/es/glosario/inline-functions/" | relative_url }}): muchas de sus [higher-order functions]({{ "/es/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) (`map`, `filter`, `let`, `apply`) son `inline`, eliminando el overhead de [allocation]({{ "/es/glosario/allocations/" | relative_url }}) de [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}).
- El artefacto `kotlin-stdlib` fue unificado en Kotlin 1.8 — `kotlin-stdlib-jdk7` y `kotlin-stdlib-jdk8` ahora son parte del artefacto principal. Saber esto evita declaraciones de dependencias redundantes en Gradle.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
