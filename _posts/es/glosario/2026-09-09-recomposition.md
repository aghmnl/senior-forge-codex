---
layout: post
title: "Recomposition"
date: 2026-09-09 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/recomposition/
---

## The Theory (El Qué)

La **Recomposition** (recomposición) es la re-ejecución que hace [Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) de una función composable cuando cambió un estado que leyó. Compose registra qué composables leen qué estado; cuando ese estado se escribe, solo esos lectores se invalidan y vuelven a correr.

```kotlin
// Leer uiState.selectedTaskIds suscribe a este composable a ese estado.
// Un objeto de estado nuevo con un set distinto vuelve a ejecutar esta función;
// un objeto de estado que compara igual se saltea por completo.
val uiState by viewModel.uiState.collectAsStateWithLifecycle()
```

## The Senior Nuance (El Matiz Senior)

- La decisión de saltear es por [`equals`]({{ "/es/glosario/equals/" | relative_url }}), no por identidad, pero solo para parámetros cuyos tipos Compose considera [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}). Una `data class` de tipos estables califica; la misma clase con un `MutableList` no, y Compose la recompone conservadoramente en cada recomposición del padre.
- La recomposición puede correr **más de una vez por frame y en cualquier orden**, y puede cancelarse a mitad de camino. Por eso el cuerpo de un composable debe ser una función pura de sus entradas: los side effects van en `LaunchedEffect`/`DisposableEffect`, y las asignaciones por frame en el cuerpo son la manera de empezar a perder frames en una lista.
- El modo de falla de un objeto de estado mutable es silencioso: el [`StateFlow`]({{ "/es/glosario/stateflow/" | relative_url }}) emite la *misma instancia* que ya había emitido, [`equals`]({{ "/es/glosario/equals/" | relative_url }}) dice "sin cambios", y la pantalla simplemente no se actualiza. La [Inmutabilidad]({{ "/es/glosario/immutability/" | relative_url }}) es lo que hace que "el estado cambió" y "el objeto es distinto" sean la misma afirmación.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
