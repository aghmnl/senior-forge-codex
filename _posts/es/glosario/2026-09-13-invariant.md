---
layout: post
title: "Invariant"
date: 2026-09-13 12:00:00 +0000
categories: [es, glosario]
tags: [design-principles, error-handling, type-system]
lang: es
permalink: /es/glosario/invariant/
---

## The Theory (El Qué)

Una **invariante** es una condición que debe cumplirse en un punto dado de un programa — para un objeto durante toda su vida, para los argumentos de una función al entrar, para su resultado al salir. "Un `Task` siempre tiene título no vacío", "un archivo de backup tiene el formato que escribimos". Las invariantes son lo que el código *asume*; hacerlas explícitas es lo que convierte un crash misterioso en uno legible.

```kotlin
// From FollowApp Suite — BackupSerializer.kt
require(root.optString("format") == FORMAT) { "Not a MyTasks backup file" }
require(root.optInt("version", -1) == VERSION) {
    "Unsupported backup version: ${root.optString("version")}"
}
```

Las funciones de [assertion]({{ "/es/glosario/assertion/" | relative_url }}) de Kotlin mapean a los tres tipos: `require` (invariante de argumento → `IllegalArgumentException`), `check` (invariante de estado → `IllegalStateException`), y `?: throw` / `error()` para el resto. Cada una recibe un mensaje lazy, que es la invariante escrita en lenguaje natural.

## The Senior Nuance (El Matiz Senior)

- **La mejor invariante es la que impone el sistema de tipos.** Un parámetro no-nullable, una [sealed hierarchy]({{ "/es/glosario/sealed-hierarchy/" | relative_url }}) o una value class eliminan la necesidad del chequeo en runtime. Usá `require`/`check` solo donde el tipo no puede decirlo — input parseado del mundo exterior, restricciones de orden, reglas entre campos.
- **Verificá en los límites, confiá adentro.** Validá una vez en el borde (deserialización, input de API, formularios) y dejá que el interior asuma la invariante. Re-chequear en cada capa es ruido que esconde qué capa es dueña de la regla.
- **El mensaje es el punto.** `?: throw IllegalStateException("order required at checkout")` produce un [stack trace]({{ "/es/glosario/stack-trace/" | relative_url }}) que explica *qué* invariante se rompió; `!!` produce una [NullPointerException]({{ "/es/glosario/null-pointer-exception/" | relative_url }}) que solo dice *dónde*. Ver [Null Safety: Elvis y Safe Calls]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}).
- **El estado inmutable hace baratas las invariantes.** Con una [data class]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}) construida una vez a través de una factory, la invariante se verifica en la construcción y no puede romperse después — salvo que `copy()` saltee la factory, que es el único agujero a vigilar.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
