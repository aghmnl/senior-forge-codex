---
layout: post
title: "LaunchedEffect"
date: 2026-09-15 12:00:00 +0000
categories: [es, glosario]
tags: [compose, coroutines, lifecycle]
lang: es
permalink: /es/glosario/launched-effect/
---

## The Theory (El Qué)

**`LaunchedEffect(key) { }`** es el [composable]({{ "/es/glosario/composable/" | relative_url }}) que lanza una coroutine atada a la [composición]({{ "/es/glosario/composition-lifetime/" | relative_url }}): el bloque arranca cuando el efecto entra a la composición, se **cancela cuando sale**, y se cancela-y-reinicia cada vez que cambia cualquier `key`. Es Structured Concurrency aplicada a la UI — la composición es el padre, y la coroutine no puede sobrevivirla.

```kotlin
// From FollowApp Suite — TasksScreen.kt
LaunchedEffect(toastMessage) {
    if (toastMessage == null) return@LaunchedEffect
    Toast.makeText(context, toastMessage, Toast.LENGTH_SHORT).show()
    onToastShown()
}
```

## The Senior Nuance (El Matiz Senior)

- **Las keys son la política de reinicio.** `LaunchedEffect(Unit)` corre una vez por composición; `LaunchedEffect(state.value)` reinicia en cada cambio. Elegir mal la key o pierde actualizaciones o cancela trabajo a mitad de vuelo.
- **La cancelación es una [`CancellationException`]({{ "/es/glosario/cancellation-exception/" | relative_url }}) en el próximo [suspension point]({{ "/es/glosario/suspension-point/" | relative_url }}).** Un loop `while` adentro tiene que suspender (`withFrameNanos`, `delay`) o revisar [`isActive`]({{ "/es/glosario/is-active/" | relative_url }}) para ser [cooperativo]({{ "/es/glosario/cooperative-cancellation/" | relative_url }}).
- **Para event handlers, usá `rememberCoroutineScope()`.** `LaunchedEffect` es para trabajo que debe correr *porque* un estado está de cierta manera; un scope es para trabajo que arranca *porque* el usuario hizo algo.
- Ver [Structured Concurrency]({{ "/es/02-coroutines-flow/structured-concurrency/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
