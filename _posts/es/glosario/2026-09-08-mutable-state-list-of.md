---
layout: post
title: "mutableStateListOf"
date: 2026-09-08 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/mutable-state-list-of/
---

## The Theory (El Qué)

**`mutableStateListOf()`** crea una [Snapshot State List]({{ "/es/glosario/snapshot-state-list/" | relative_url }}) — un [`MutableList`]({{ "/es/glosario/mutable-list/" | relative_url }}) conectado al [Snapshot System]({{ "/es/glosario/snapshot-system/" | relative_url }}) de Compose, de modo que [`add`]({{ "/es/glosario/add/" | relative_url }}), [`remove`]({{ "/es/glosario/remove/" | relative_url }}), `set` y [`clear`]({{ "/es/glosario/clear/" | relative_url }}) recomponen los composables que la leen.

```kotlin
// De FollowApp Suite — TasksScreen.kt
val localTasks = remember { mutableStateListOf<Task>() }
// ...
localTasks.add(toIdx, localTasks.removeAt(fromIdx))   // recompone al instante
```

## The Senior Nuance (El Matiz Senior)

- Siempre dentro de `remember { }` — si no, se crea una lista nueva en cada recomposición y el estado se resetea. No tiene state saver, así que no sobrevive a la muerte del proceso; usá `rememberSaveable` con un saver explícito, o subí el estado al [ViewModel]({{ "/es/glosario/viewmodel-store/" | relative_url }}).
- Observa solo el cambio *estructural*. Mutar un campo de un elemento no cambia nada — el elemento debe reemplazarse (`list[i] = newValue`), que es exactamente lo que hace el loop de re-sincronización de FollowApp Suite.
- Es la única [Collection]({{ "/es/glosario/collections/" | relative_url }}) mutable legítima en código de UI, y solo como estado local optimista: el [ViewModel]({{ "/es/glosario/viewmodel-store/" | relative_url }}) sigue siendo el source of truth, y lo que sale del composable es un [`List`]({{ "/es/glosario/list/" | relative_url }}) común de solo lectura. Compará con `mutableStateOf(listOf())`, que reemplaza la lista entera por cambio y es el default correcto cuando no hay un gesto por ítem.

**Documentación oficial:** [`mutableStateListOf`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/package-summary#mutableStateListOf()) · [`SnapshotStateList`](https://developer.android.com/reference/kotlin/androidx/compose/runtime/snapshots/SnapshotStateList)

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
