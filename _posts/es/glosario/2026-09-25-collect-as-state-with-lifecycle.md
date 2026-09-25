---
layout: post
title: "collectAsStateWithLifecycle"
date: 2026-09-25 12:00:00 +0000
categories: [es, glosario]
tags: [compose, lifecycle, flow]
lang: es
permalink: /es/glosario/collect-as-state-with-lifecycle/
---

## The Theory (El Qué)

**`collectAsStateWithLifecycle()`** es una extensión de [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) (de `androidx.lifecycle:lifecycle-runtime-compose`) que colecta un [Flow]({{ "/es/glosario/flow/" | relative_url }}) en un `State` de Compose **solo mientras el [lifecycle]({{ "/es/glosario/lifecycle/" | relative_url }}) está al menos en `STARTED`**. Por debajo de ese estado (la app en background, la pantalla tapada) cancela la colección; cuando el lifecycle vuelve, colecta de nuevo. Sobre un [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) el primer valor sale de `.value`, así que la UI tiene algo que dibujar de inmediato. Por dentro corre la colección adentro de [repeatOnLifecycle]({{ "/es/glosario/repeat-on-lifecycle/" | relative_url }}).

```kotlin
// De FollowApp Suite — TasksScreen.kt
// Cada StateFlow de pantalla se colecta respetando el lifecycle
val uiState by viewModel.uiState.collectAsStateWithLifecycle()
val settingsState by settingsViewModel.uiState.collectAsStateWithLifecycle()
val isTemplatePickerVisible by viewModel.isTemplatePickerVisible.collectAsStateWithLifecycle()
```

## The Senior Nuance (El Matiz Senior)

- **Es la opción por defecto para colectar en Compose.** `collectAsState()` colecta mientras el composable está en la composición, y la composición sigue viva con la app en background. `collectAsStateWithLifecycle()` es la versión [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}) y debería ser la elección automática.
- **El ahorro no está en el colector, está en el [upstream]({{ "/es/glosario/upstream/" | relative_url }}).** Para un `MutableStateFlow` simple la diferencia es chica. Para un `StateFlow` construido con [stateIn]({{ "/es/glosario/state-in/" | relative_url }}) y [WhileSubscribed]({{ "/es/glosario/while-subscribed/" | relative_url }}), frenar el colector es lo único que permite que el upstream (una query, actualizaciones de ubicación, un socket) también se detenga.
- **`minActiveState` se puede configurar.** `STARTED` es el valor por defecto; `RESUMED` sirve para trabajo que tiene que pausarse cuando un diálogo u otra ventana tapa parcialmente la pantalla.
- Para un [Flow]({{ "/es/glosario/flow/" | relative_url }}) cold necesita un `initialValue` explícito, porque no hay `.value` para leer antes de la primera emisión.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
