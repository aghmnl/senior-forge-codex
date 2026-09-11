---
layout: post
title: "Single Source of Truth"
date: 2026-09-09 12:00:00 +0000
categories: [es, glosario]
tags: [state-management, architecture, design-principles]
lang: es
permalink: /es/glosario/single-source-of-truth/
---

## The Theory (El Qué)

**Single Source of Truth** (SSOT) es la regla de que cada pieza de estado tiene exactamente un dueño, y todo lo demás se deriva de ella. El estado duplicado no es "una copia" — es una segunda verdad que tarde o temprano va a contradecir a la primera.

```kotlin
// De FollowApp Suite — TasksUiState.kt
// Derivado, no almacenado: no hay flag isSelectionMode que mantener sincronizado con el set
val isSelectionMode: Boolean get() = selectedTaskIds.isNotEmpty()
val selectedTasks: List<Task> get() = activeTasks.filter { it.id in selectedTaskIds }
```

## The Senior Nuance (El Matiz Senior)

- El bug que SSOT previene es el *estado imposible*: `isSelectionMode = true` con `selectedTaskIds = emptySet()`. Si ambos se almacenan, algún camino de código eventualmente va a actualizar uno y no el otro. Si uno es una propiedad calculada, ese estado directamente no se puede expresar.
- Las propiedades derivadas de la clase de estado se ejecutan en cada lectura, así que tienen que ser baratas. Que `selectedTasks` filtre unos cientos de tasks por recomposición está bien; un `sortedBy` sobre diez mil no — eso va aguas arriba en el [ViewModel]({{ "/es/glosario/viewmodel-store/" | relative_url }}), calculado una vez cuando cambian sus entradas.
- SSOT también decide *dónde* vive la verdad, no solo cuántas copias hay. En FollowApp Suite la base de datos es la verdad para las tasks, el [`StateFlow`]({{ "/es/glosario/stateflow/" | relative_url }}) del [ViewModel]({{ "/es/glosario/viewmodel-store/" | relative_url }}) es la verdad para la pantalla, y cualquier estado local de [Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) es explícitamente una copia derivada y resincronizada — nunca autoritativa.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
