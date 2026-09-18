---
layout: post
title: "Success (UI State)"
date: 2026-09-18 12:00:00 +0000
categories: [es, glosario]
tags: [state-management, sealed-types, architecture]
lang: es
permalink: /es/glosario/success-state/
---

## The Theory (El Qué)

**`Success`** es el nombre convencional del subtipo de una jerarquía sellada de estado de UI que transporta los datos cargados: `sealed interface UiState { object Loading; data class Success(val items: List<Item>); data class Error(val message: String) }`. Es una `data class` y no un `object` porque lleva payload, y vive junto a sus hermanos para que un [`when`]({{ "/es/glosario/when-expression/" | relative_url }}) sobre la [jerarquía sellada]({{ "/es/glosario/sealed-hierarchy/" | relative_url }}) sea [exhaustivo]({{ "/es/glosario/exhaustiveness/" | relative_url }}). Hacer match con `is UiState.Success` smart-castea el estado y da acceso directo a `state.items` sin [cast]({{ "/es/glosario/cast/" | relative_url }}) — el patrón sobre el que se construyen las pantallas [MVI]({{ "/es/glosario/mvi-pattern/" | relative_url }}) y [UDF]({{ "/es/glosario/unidirectional-data-flow/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
sealed interface ScreenState {
    data object Loading : ScreenState
    data class Success(val items: List<String>) : ScreenState
    data class Error(val message: String) : ScreenState
}

fun render(state: ScreenState) = when (state) {
    is ScreenState.Loading -> showSpinner()
    is ScreenState.Success -> showData(state.items)   // smart cast: acá state es Success
    is ScreenState.Error   -> showError(state.message)
}
```

## The Senior Nuance (El Matiz Senior)

- **`Success` es donde vive el payload, así que es la rama que necesita el smart cast.** `Loading` y `Error` suelen ser objects; `Success` casi nunca. El sentido del diseño sellado es que `state.items` solo sea alcanzable después de que el compilador probó que el estado es `Success`.
- **Modelá "éxito sin nada" de forma explícita.** Una lista vacía dentro de `Success` y un estado `Empty` separado son decisiones de UX distintas; no codifiques la diferencia como un campo nullable.
- **Un `Success` por pantalla, no por request.** Si una pantalla combina dos llamadas, `Success` guarda ambos resultados; dos estados sellados en paralelo obligan a la UI a razonar sobre su producto cartesiano.
- Ver [Smart Casts]({{ "/es/01-kotlin-core/smart-casts/" | relative_url }}) y [UI State Modeling]({{ "/es/05-architecture/ui-state-modeling/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
