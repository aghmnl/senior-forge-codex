---
layout: post
title: "NullPointerException"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/null-pointer-exception/
---

## The Theory (El Qué)

Una **NullPointerException** (NPE) es una excepción de runtime que se lanza cuando el código intenta usar una referencia que apunta a `null` — llamar a un método, acceder a una propiedad, o indexar sobre un objeto null. En la JVM, es la causa más común de crashes en aplicaciones.

## The Senior Nuance (El Matiz Senior)

- El sistema de [null safety]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}) de Kotlin fue diseñado específicamente para eliminar NPEs en [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}). Los tipos nullable (`String?`) y no-nullable (`String`) son distintos en el sistema de tipos, así que el compilador rechaza código que podría desreferenciar null sin una verificación.
- El código Kotlin todavía puede lanzar NPE en cuatro situaciones: uso explícito de `!!`, interop con Java con platform types sin anotar, acceso a `lateinit` sin inicializar, e implementaciones incorrectas de `equals`. Un Senior trata cada una como un límite a defender.
- En Android, NPE es la categoría de crash más frecuente en producción. Los reportes de Firebase Crashlytics consistentemente muestran que la mayoría de los NPEs se originan en los límites de interop Java/Kotlin — particularmente cuando los callbacks del framework Android retornan platform types.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
