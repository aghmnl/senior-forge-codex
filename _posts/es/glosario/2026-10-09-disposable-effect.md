---
layout: post
title: "DisposableEffect"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [compose, lifecycle]
lang: es
permalink: /es/glosario/disposable-effect/
---

## The Theory (El Qué)

**`DisposableEffect(key) { ... onDispose { } }`** ejecuta un bloque de inicialización cuando el composable entra en la [composition]({{ "/es/glosario/composition/" | relative_url }}) (o cuando cambia su key) y exige un bloque `onDispose` que corre cuando sale (o antes de volver a inicializar para una key nueva). Es el lugar para registrar y desregistrar [listeners]({{ "/es/glosario/listener/" | relative_url }}) u observers atados a un composable.

```kotlin
// Not found in FAS — standalone example
DisposableEffect(lifecycleOwner) {
    val observer = LifecycleEventObserver { _, event -> onEvent(event) }
    lifecycleOwner.lifecycle.addObserver(observer)
    onDispose { lifecycleOwner.lifecycle.removeObserver(observer) }
}
```

## The Senior Nuance (El Matiz Senior)

- **`onDispose` es obligatorio a propósito**: cada registro tiene su limpieza al lado, la misma idea que [`awaitClose`]({{ "/es/glosario/await-close/" | relative_url }}) en [`callbackFlow`]({{ "/es/glosario/callback-flow/" | relative_url }}).
- **La key decide cuándo se reinicia.** Con la key equivocada, el efecto sigue usando un objeto viejo, o se registra y desregistra en cada [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
