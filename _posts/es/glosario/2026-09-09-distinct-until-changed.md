---
layout: post
title: "distinctUntilChanged"
date: 2026-09-09 12:00:00 +0000
categories: [es, glosario]
tags: [flow, state-management, immutability]
lang: es
permalink: /es/glosario/distinct-until-changed/
---

## The Theory (El Qué)

`distinctUntilChanged()` es un operador de `Flow` que suprime una emisión cuando es [igual]({{ "/es/glosario/equals/" | relative_url }}) a la anterior. Convierte un stream de *eventos* en un stream de *cambios*.

```kotlin
// De FollowApp Suite — TasksViewModel.kt
_uiState
    .map { s -> PersistKey(s.sortOrder, s.groupBy, s.doneFilter, /* ... */) }
    .distinctUntilChanged()
    .drop(1)
    .debounce(200L)
    .collect { key -> /* escribir preferencias a disco */ }
```

## The Senior Nuance (El Matiz Senior)

- El idiom de arriba es el importante: `map` a una **proyección angosta** del estado, y después `distinctUntilChanged`. Todo `TasksUiState` cambia con cada tecla; las siete propiedades que vale la pena persistir cambian rara vez. Sin la proyección, las escrituras a disco se disparan con cada carácter tipeado.
- Compara con `equals`, así que hereda todas las advertencias sobre inmutabilidad. Una proyección con una colección mutable puede comparar igual mientras su contenido difiere — el operador se va a comer un cambio real, y el síntoma es una preferencia que falla en persistirse en silencio.
- [`StateFlow`]({{ "/es/glosario/stateflow/" | relative_url }}) ya aplica esta regla a su propio valor: asignarle a `value` algo igual al valor actual no emite nada. Así que `stateFlow.distinctUntilChanged()` es redundante, mientras que `stateFlow.map { ... }.distinctUntilChanged()` no lo es — `map` produce un `Flow` común sin esa conflación.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
