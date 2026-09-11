---
layout: post
title: "Snapshot State List"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
tags: [compose, collections, state-management]
lang: es
permalink: /es/glosario/snapshot-state-list/
---

## The Theory (El Qué)

Una **Snapshot State List** — `mutableStateListOf()`, de tipo `SnapshotStateList<T>` — es un `MutableList` integrado con el [Snapshot System]({{ "/es/glosario/snapshot-system/" | relative_url }}) de Compose. Los cambios estructurales (`add`, `remove`, `clear`, `set`) se registran como [mutaciones]({{ "/es/glosario/mutation/" | relative_url }}) de [Observable State]({{ "/es/glosario/observable-state/" | relative_url }}) y recomponen exactamente los composables que leen la lista.

```kotlin
// De FollowApp Suite — TasksScreen.kt
val localTasks = remember { mutableStateListOf<Task>() }
// ...
localTasks.add(toIdx, localTasks.removeAt(fromIdx))   // recompone al instante
```

## The Senior Nuance (El Matiz Senior)

- Es la excepción a "nada de [Collections]({{ "/es/glosario/collections/" | relative_url }}) mutables en código de UI" — y solo para estado *local y optimista*. En FollowApp Suite existe para que un gesto de drag pueda reordenar filas de forma sincrónica sin un round-trip al [ViewModel]({{ "/es/glosario/viewmodel-store/" | relative_url }}) por movimiento; el ViewModel sigue siendo el source of truth y se le notifica una sola vez en el drop.
- Debe re-sincronizarse desde ese source of truth (un `LaunchedEffect` keyed por el estado entrante), o ambos divergen — el bug clásico donde la UI muestra un orden que la capa de datos nunca aceptó.
- `remember { mutableStateListOf() }` no toma un state saver, así que no sobrevive a la muerte del proceso; y mutarla observa solo el cambio *estructural* — mutar un campo de un elemento no hace nada salvo que el elemento sea observable o se reemplace. Nunca la expongas cruzando un límite de módulo: devolvé un `List` de solo lectura común.

**Documentación oficial:** [`SnapshotStateList`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/snapshots/SnapshotStateList)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
