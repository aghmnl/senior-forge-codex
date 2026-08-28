---
layout: post
title: "Data Transformation"
date: 2026-08-21 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/data-transformation/
---

## La Teoría (El Qué)

Una **data transformation** (transformación de datos) es cualquier operación que toma un valor de un tipo o forma y produce un valor de un tipo o forma diferente. En Kotlin, las transformaciones están en todas partes: `map` convierte una `List<A>` en `List<B>`, `let` transforma un valor nullable en un resultado, y las funciones mapper convierten entre capas de datos (`Entity → Domain → UI Model`).

La propiedad clave de una transformación es que produce un **nuevo valor** en lugar de modificar el original en el lugar. Esto se alinea con la preferencia de Kotlin por la inmutabilidad y el estilo funcional.

## El Matiz Senior

- En la arquitectura Android, el **patrón Mapper** es un pipeline de transformación: `NetworkResponse → Entity → DomainModel → UiState`. Cada capa tiene su propio modelo, y las transformaciones ocurren en los límites. Esto mantiene las capas desacopladas.
- Las [scope functions]({{ "/es/01-kotlin-core/scope-functions/" | relative_url }}) codifican la distinción de transformación en su tipo de retorno: `let` y `run` retornan el resultado de la lambda (transformación), mientras que `apply` y `also` retornan el objeto de contexto (configuración/side effect). Mezclarlas es un bug común — usar `apply` cuando querías transformar significa que el valor transformado se descarta silenciosamente.
- Los operadores de colecciones de Kotlin (`map`, `filter`, `flatMap`, `groupBy`) son todos transformaciones. Entender que crean nuevas colecciones (no modifican la original) es fundamental para razonar sobre rendimiento y thread safety.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
