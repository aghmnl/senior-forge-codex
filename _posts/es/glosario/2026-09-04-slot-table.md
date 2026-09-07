---
layout: post
title: "Slot Table"
date: 2026-09-04 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/slot-table/
---

## The Theory (El Qué)

La **slot table** es la estructura de datos interna de [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) que almacena el estado y la estructura del árbol de composición. Es un array plano tipo gap-buffer donde cada llamada a función [`@Composable`]({{ "/es/glosario/composable/" | relative_url }}) ocupa un rango de "slots" que contienen:

- **Groups** — marcadores que delimitan el inicio y fin de cada composable en el árbol.
- **State** — valores almacenados vía `remember {}`, incluyendo [propiedades delegadas]({{ "/es/01-kotlin-core/delegated-properties/" | relative_url }}) creadas con `by remember { mutableStateOf() }`.
- **Nodes** — los elementos de UI reales (nodos de layout) que Compose renderiza.

Cuando la recomposición se ejecuta, el runtime de Compose recorre la slot table, comparando la estructura de llamadas actual contra la almacenada. Si los inputs de un composable no cambiaron y es "skippable" (todos los parámetros son [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}) o [primitivos]({{ "/es/glosario/primitives/" | relative_url }})), Compose omite re-ejecutarlo por completo — los slots existentes se reutilizan tal cual.

## The Senior Nuance (El Matiz Senior)

- Un Senior sabe que `remember {}` está anclado a una posición en la slot table, no a un nombre de variable. Si el call site se mueve (por ejemplo, un composable se incluye condicionalmente antes de otro), las posiciones de slot se desplazan, y los valores recordados se resetean. El composable `key()` provee identidad estable para prevenir esto.
- La slot table es la razón por la que `by remember { mutableStateOf() }` y `by mutableStateOf()` en una clase [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}) tienen [lifetimes]({{ "/es/glosario/composition-lifetime/" | relative_url }}) diferentes: la versión con `remember` se almacena en la slot table y muere cuando ese composable sale de la composición; la versión en clase `@Stable` vive en el [heap]({{ "/es/glosario/heap/" | relative_url }}) tanto como la instancia de la clase exista.
- El diseño de gap buffer significa que las inserciones y eliminaciones en un solo punto son O(1), pero mover el gap es O(n). Compose minimiza los movimientos de gap procesando el árbol linealmente, de arriba a abajo. La composición condicional (bloques `if`/`when`) que cambia frecuentemente en el medio de un árbol de composables grande causa más movimientos de gap — una consideración de performance sutil.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
