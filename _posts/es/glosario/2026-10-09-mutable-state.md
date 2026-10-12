---
layout: post
title: "MutableState"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [compose, state-management]
lang: es
permalink: /es/glosario/mutable-state/
---

## The Theory (El Qué)

**`MutableState<T>`** es el contenedor de estado observable de Compose, creado con `mutableStateOf(value)`. Leer `.value` durante la [composition]({{ "/es/glosario/composition/" | relative_url }}) registra esa lectura en el [snapshot system]({{ "/es/glosario/snapshot-system/" | relative_url }}); escribir un valor nuevo invalida exactamente los scopes que lo leyeron, que entonces se recomponen. Las versiones especializadas (`mutableIntStateOf`, `mutableFloatStateOf`) evitan el boxing de los [primitivos]({{ "/es/glosario/primitives/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
var count by remember { mutableStateOf(0) }
Button(onClick = { count++ }) { Text("Clicked $count times") }
```

## The Senior Nuance (El Matiz Senior)

- **Sin [`remember`]({{ "/es/glosario/remember/" | relative_url }}), se reinicia en cada [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}).** `mutableStateOf` crea el contenedor; [`remember`]({{ "/es/glosario/remember/" | relative_url }}) conserva el mismo contenedor entre recomposiciones.
- **Los cambios se detectan por asignación.** Mutar un objeto adentro del estado (agregar a un [`MutableList`]({{ "/es/glosario/mutable-list/" | relative_url }}) guardado ahí) no le avisa a nadie; hay que asignar un valor nuevo o usar [`mutableStateListOf`]({{ "/es/glosario/mutable-state-list-of/" | relative_url }}).
- Ver [Recomposition & Stability]({{ "/es/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
