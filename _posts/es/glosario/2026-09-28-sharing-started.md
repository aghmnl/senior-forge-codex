---
layout: post
title: "SharingStarted"
date: 2026-09-28 12:00:00 +0000
categories: [es, glosario]
tags: [flow, lifecycle, performance]
lang: es
permalink: /es/glosario/sharing-started/
---

## The Theory (El Qué)

**`SharingStarted`** es el parámetro de [stateIn]({{ "/es/glosario/state-in/" | relative_url }}) y [shareIn]({{ "/es/glosario/share-in/" | relative_url }}) que decide **cuándo corre la colección compartida del [upstream]({{ "/es/glosario/upstream/" | relative_url }})**. Tiene tres estrategias incorporadas:

- **`SharingStarted.Eagerly`**: arranca de inmediato y no se detiene hasta que se cancela el scope.
- **`SharingStarted.Lazily`**: arranca con el primer suscriptor y después ya no se detiene.
- **[SharingStarted.WhileSubscribed]({{ "/es/glosario/while-subscribed/" | relative_url }})**: corre solo mientras haya al menos un [collector]({{ "/es/glosario/collector/" | relative_url }}) suscripto, y se detiene pasado un timeout cuando se va el último.

```kotlin
// Not found in FAS — standalone example
val uiState = repository.observe()
    .map { it.toUiState() }
    .stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),   // la elección habitual para estado de UI
        initialValue = UiState.Loading
    )
```

## The Senior Nuance (El Matiz Senior)

- **`WhileSubscribed(5_000)` es el valor por defecto para estado de UI.** Sobrevive a una rotación (el suscriptor desaparece más o menos un segundo) y aun así detiene el trabajo cuando el usuario sale de la app.
- **`Eagerly` y `Lazily` significan "durante toda la vida del scope".** En un scope de aplicación, eso es toda la vida del proceso. Sirven para datos que la app necesita listos siempre, no para una sola pantalla.
- Es una interfaz, así que se puede escribir una estrategia propia, pero las tres incorporadas cubren prácticamente todos los casos.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
