---
layout: post
title: "Value Semantics"
date: 2026-09-09 12:00:00 +0000
categories: [es, glosario]
tags: [data-classes, immutability, state-management]
lang: es
permalink: /es/glosario/value-semantics/
---

## The Theory (El Qué)

Un tipo tiene **Value Semantics** (semántica de valor) cuando su identidad es su contenido: dos instancias con la misma data son intercambiables, y pasar una por ahí no le permite a nadie cambiar la tuya. Una [`data class`]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}) de propiedades inmutables tiene value semantics; una clase con campos `var` tiene semántica *de referencia* — lo que tenés es un handle a algo que puede cambiar bajo tus pies.

```kotlin
// De FollowApp Suite — TasksUiState.kt
data class TasksUiState(
    val isLoading: Boolean = true,
    val activeTasks: List<Task> = emptyList(),
    val selectedTaskIds: Set<String> = emptySet(),
    // ... cada propiedad un val, cada tipo de solo lectura
)
```

## The Senior Nuance (El Matiz Senior)

- La value semantics es lo que hace seguro entregar un objeto de estado a un composable, a una coroutine y a un test al mismo tiempo. Nadie puede corromper la copia de otro porque no hay nada que corromper — [Thread Safety]({{ "/es/glosario/thread-safety/" | relative_url }}) por construcción y no por locking.
- También es lo que hace que `==` *signifique* algo. El skipping de [Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}), [`distinctUntilChanged`]({{ "/es/glosario/distinct-until-changed/" | relative_url }}), la [Conflation]({{ "/es/glosario/conflation/" | relative_url }}) de [`StateFlow`]({{ "/es/glosario/stateflow/" | relative_url }}) y las aserciones de tests preguntan todos "¿es el mismo estado?" y solo un tipo de valor les da una respuesta veraz.
- El `val` en la propiedad es la mitad del trabajo; el *tipo* de la propiedad también tiene que ser de solo lectura hasta el fondo. `val tasks: MutableList<Task>` es un `val` con semántica de referencia, y derrota a [`equals`]({{ "/es/glosario/equals/" | relative_url }}), [`copy`]({{ "/es/glosario/copy/" | relative_url }}) y [`@Stable`]({{ "/es/glosario/stable/" | relative_url }}) en una sola línea.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
