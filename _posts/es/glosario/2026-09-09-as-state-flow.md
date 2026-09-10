---
layout: post
title: "asStateFlow"
date: 2026-09-09 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/as-state-flow/
---

## The Theory (El Qué)

`asStateFlow()` envuelve un `MutableStateFlow` en una vista `StateFlow` de solo lectura. Existe para que un state holder pueda exponer su estado sin exponer la capacidad de escribirlo.

```kotlin
// De FollowApp Suite — TasksViewModel.kt
private val _uiState = MutableStateFlow(TasksUiState())
val uiState: StateFlow<TasksUiState> = _uiState.asStateFlow()
```

## The Senior Nuance (El Matiz Senior)

- La alternativa, `val uiState: StateFlow<T> = _uiState`, es más débil de lo que parece: el tipo declarado prohíbe escribir, pero un caller puede hacer downcast a `MutableStateFlow` y emitir. `asStateFlow()` devuelve un objeto genuinamente distinto que delega las lecturas, así que el Cast falla. Es una [Read-Only View]({{ "/es/glosario/read-only-view/" | relative_url }}) que de verdad se sostiene.
- Cuesta una asignación de wrapper por state holder, para siempre, y compra un límite arquitectónico: el [ViewModel]({{ "/es/glosario/viewmodel-store/" | relative_url }}) es el único escritor, que es la mitad "unidireccional" del [Unidirectional Data Flow]({{ "/es/glosario/unidirectional-data-flow/" | relative_url }}). Sin eso, un composable puede empujar estado hacia arriba y el flujo deja de ser en una sola dirección.
- **No** hace inmutable al *valor*. Si `TasksUiState` contiene un `MutableList`, la UI todavía puede mutar el contenido a través del flow de solo lectura. `asStateFlow()` protege el caño; la [Inmutabilidad]({{ "/es/glosario/immutability/" | relative_url }}) de la clase de estado protege la carga — necesitás las dos.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
