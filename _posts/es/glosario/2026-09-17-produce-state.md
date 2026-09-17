---
layout: post
title: "produceState"
date: 2026-09-17 12:00:00 +0000
categories: [es, glosario]
tags: [compose, coroutines, state-management]
lang: es
permalink: /es/glosario/produce-state/
---

## The Theory (El Qué)

**`produceState(initialValue) { }`** es el [composable]({{ "/es/glosario/composable/" | relative_url }}) que convierte una coroutine en un `State<T>`: lanza el bloque en una coroutine atada a la composición (como [`LaunchedEffect`]({{ "/es/glosario/launched-effect/" | relative_url }})), y cada asignación a `value` adentro dispara [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}). La coroutine se cancela cuando el composable sale de la composición, y se reinicia cuando cambia cualquier key. Corre en el [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}) de la composición — Main — así que el trabajo bloqueante adentro necesita [`withContext`]({{ "/es/glosario/with-context/" | relative_url }}).

```kotlin
// From FollowApp Suite — AboutScreen.kt
val licenses by produceState<List<License>?>(initialValue = null, key1 = context) {
    value = withContext(Dispatchers.IO) { loadLicenses(context) }
}
```

## The Senior Nuance (El Matiz Senior)

- **Es `LaunchedEffect` + `remember { mutableStateOf() }` en una sola llamada.** Usalo cuando el único trabajo del efecto es producir un valor para la UI.
- **El `withContext` no es opcional para loaders bloqueantes.** Sin él el primer frame de la pantalla espera al disco — eso es [jank]({{ "/es/glosario/jank/" | relative_url }}) al entrar, y la main-safety aplica exactamente igual que en un repositorio.
- **Para streams de vida larga preferí `collectAsStateWithLifecycle`.** `produceState` es para cargas puntuales o guiadas por key; un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) que debe detenerse cuando la app pasa a background quiere el collector lifecycle-aware.
- Ver [Main-Safety]({{ "/es/02-coroutines-flow/main-safety/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
