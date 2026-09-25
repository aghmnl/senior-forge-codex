---
layout: post
title: "MutableStateFlow"
date: 2026-09-25 12:00:00 +0000
categories: [es, glosario]
tags: [flow, state-management, concurrency]
lang: es
permalink: /es/glosario/mutable-state-flow/
---

## The Theory (El Qué)

**`MutableStateFlow<T>`** es la versión escribible de [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}). Se crea con `MutableStateFlow(initialValue)` y suma tres formas de cambiar el estado: asignar `value`, el atómico [compareAndSet(expect, update)]({{ "/es/glosario/compare-and-set/" | relative_url }}), y la extensión [update {}]({{ "/es/glosario/update/" | relative_url }}) construida encima. Todas son [thread-safe]({{ "/es/glosario/thread-safety/" | relative_url }}), y cada escritura que no es [igual]({{ "/es/glosario/equals/" | relative_url }}) al valor actual se les entrega a los [collectors]({{ "/es/glosario/collector/" | relative_url }}). Queda privado dentro de un [state holder]({{ "/es/glosario/state-holder/" | relative_url }}) y se expone de solo lectura con [asStateFlow()]({{ "/es/glosario/as-state-flow/" | relative_url }}).

```kotlin
// De FollowApp Suite — BillingConnector.kt
// Mutable y privado adentro; de solo lectura afuera.
// null = "Play todavía no respondió", distinto de un false real
private val _isOwned = MutableStateFlow<Boolean?>(null)
val isOwned: StateFlow<Boolean?> = _isOwned.asStateFlow()
```

## The Senior Nuance (El Matiz Senior)

- **`value = value.copy(...)` no es atómico.** Lee y después escribe; dos coroutines haciéndolo a la vez pueden perder un cambio. `update {}` reintenta con `compareAndSet` hasta que la escritura cae sobre el mismo valor a partir del cual se calculó.
- **Exponer el tipo mutable filtra el acceso de escritura.** Un `MutableStateFlow` público le permite a la UI cambiar el estado directamente y rompe el [flujo unidireccional de datos]({{ "/es/glosario/unidirectional-data-flow/" | relative_url }}). Hacer upcast a `StateFlow` tampoco alcanza, porque quien lo recibe puede castearlo de vuelta; `asStateFlow()` devuelve un envoltorio realmente de solo lectura.
- **También es un test double muy práctico.** Un `MutableStateFlow` devuelto por un repositorio fake permite que un test empuje valores nuevos cuando quiera y verifique cómo reacciona el ViewModel.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
