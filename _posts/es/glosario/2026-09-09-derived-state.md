---
layout: post
title: "Derived State"
date: 2026-09-09 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/derived-state/
---

## The Theory (El Qué)

El **Derived State** (estado derivado) es estado que se *calcula* a partir de otro estado en vez de almacenarse junto a él. En una clase de estado inmutable toma la forma de una propiedad con getter y sin [Backing Field]({{ "/es/glosario/backing-field/" | relative_url }}) — no puede quedar desactualizado, porque se recalcula desde la verdad en cada lectura.

```kotlin
// De FollowApp Suite — TasksUiState.kt
val isSelectionMode: Boolean get() = selectedTaskIds.isNotEmpty()
val selectedTasks: List<Task> get() = activeTasks.filter { it.id in selectedTaskIds }
```

## The Senior Nuance (El Matiz Senior)

- La alternativa — guardar `isSelectionMode` como un `val` del constructor — crea una obligación de sincronización en cada lugar donde se hace [`copy`]({{ "/es/glosario/copy/" | relative_url }}). La derivación hace que la combinación inconsistente sea irrepresentable, que es la forma más fuerte de [Single Source of Truth]({{ "/es/glosario/single-source-of-truth/" | relative_url }}).
- Un getter es invisible para [`equals`]({{ "/es/glosario/equals/" | relative_url }}), [`copy`]({{ "/es/glosario/copy/" | relative_url }}) y `toString`, porque una `data class` solo los genera sobre las propiedades del *constructor primario*. Acá eso es una ventaja: los valores derivados no pueden desincronizar la comparación de estado, así que el skipping de [Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) sigue siendo correcto.
- El costo es que el getter corre en cada lectura, incluida cada [Recomposition]({{ "/es/glosario/recomposition/" | relative_url }}). Los predicados baratos van en la clase de estado; las derivaciones caras (ordenar, agrupar, joinear [Collections]({{ "/es/glosario/collections/" | relative_url }}) grandes) van aguas arriba en el [ViewModel]({{ "/es/glosario/viewmodel-store/" | relative_url }}), donde se calculan una vez por cambio de entrada — o en `derivedStateOf` cuando la fuente es estado de Compose.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
