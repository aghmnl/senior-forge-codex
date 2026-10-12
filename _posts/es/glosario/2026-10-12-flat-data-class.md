---
layout: post
title: "Flat Data Class"
date: 2026-10-12 12:00:00 +0000
categories: [es, glosario]
tags: [state-management, architecture, data-classes]
lang: es
permalink: /es/glosario/flat-data-class/
---

## The Theory (El Qué)

Una **flat data class** (data class plana) es una forma de modelar el UI state de una pantalla como una única `data class` que tiene todas las propiedades una al lado de la otra: flags (`isLoading`), campos nullables (`errorMessage`) y los datos en sí. Cada cambio crea una instancia nueva con `copy()`, normalmente adentro de `MutableStateFlow.update { }`.

```kotlin
// Not found in FAS — standalone example
data class SearchUiState(
    val isLoading: Boolean = false,
    val query: String = "",
    val results: List<Item> = emptyList(),
    val errorMessage: String? = null,
)
```

## The Senior Nuance (El Matiz Senior)

- **Encaja con pantallas cuyas preocupaciones se superponen** (búsqueda, filtros, selección, formularios), porque cada una puede cambiar sin tocar a las demás.
- **Puede contener combinaciones imposibles**, así que la consistencia es trabajo del código: propiedades derivadas en lugar de flags que se contradicen, y tests de las transiciones.
- Ver [UI State Modeling: Sealed vs Flat Data Class]({{ "/es/05-architecture/ui-state-modeling/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
