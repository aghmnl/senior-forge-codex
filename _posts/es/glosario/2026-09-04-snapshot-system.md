---
layout: post
title: "Snapshot System"
date: 2026-09-04 12:00:00 +0000
categories: [es, glosario]
tags: [compose, state-management, concurrency]
lang: es
permalink: /es/glosario/snapshot-system/
---

## The Theory (El Qué)

El **snapshot system** (sistema de snapshots) es el mecanismo de tracking de cambios de [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}). Es el motor detrás de la UI reactiva de Compose: cuando una función [`@Composable`]({{ "/es/glosario/composable/" | relative_url }}) lee un valor respaldado por snapshot y ese valor luego cambia, Compose automáticamente programa la recomposición de esa función.

En su núcleo, un snapshot es una vista aislada de estado mutable. Compose crea snapshots durante la composición y aplica cambios atómicamente. Los tipos clave:

- **`MutableState<T>`** / **`mutableStateOf()`** — el wrapper principal respaldado por snapshot. Leerlo dentro de una composición registra una observación de lectura; escribirlo dispara la invalidación de todos los lectores.
- **`SnapshotStateList`** / **`SnapshotStateMap`** — [collections]({{ "/es/glosario/collections/" | relative_url }}) snapshot-aware devueltas por `mutableStateListOf()` y `mutableStateMapOf()`.
- **`derivedStateOf {}`** — un valor snapshot computado que solo se invalida cuando cambian sus dependencias.

Cuando escribís `var count by mutableStateOf(0)` usando la [keyword]({{ "/es/glosario/keyword/" | relative_url }}) [`by`]({{ "/es/glosario/by-delegation/" | relative_url }}), el [property delegate]({{ "/es/glosario/property-delegate/" | relative_url }}) envuelve un `SnapshotMutableState` — cada lectura y escritura pasa por el snapshot system. Ver [Delegated Properties]({{ "/es/01-kotlin-core/delegated-properties/" | relative_url }}).

## The Senior Nuance (El Matiz Senior)

- Un Senior entiende que los snapshots no son solo estado de UI de Compose — son un sistema de control de concurrencia multiversión (MVCC) de propósito general. La composición se ejecuta en un snapshot aislado del estado del main thread; los cambios se fusionan atómicamente cuando la composición termina. Esto es lo que hace segura la recomposición frente a escrituras concurrentes.
- Lo que se trackea son las lecturas de snapshot, no los objetos snapshot. Si leés `state.value` dentro de un composable, ese composable se registra como lector. Si copiás el valor a un `val` local y lo pasás, el código downstream ya no tiene relación de tracking con el snapshot.
- Las clases [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}) con propiedades `by mutableStateOf()` participan en el snapshot system sin necesitar `remember` — su [lifetime]({{ "/es/glosario/composition-lifetime/" | relative_url }}) es gestionado por la instancia de la clase, no por la [slot table]({{ "/es/glosario/slot-table/" | relative_url }}).
- Escribir a estado snapshot fuera de la composición (por ejemplo, en un ViewModel o callback) es seguro: el snapshot system difiere la invalidación al próximo pase de composición. Por esto `mutableStateOf` funciona en [state holders]({{ "/es/glosario/state-holder/" | relative_url }}) que viven más allá de la composición.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
