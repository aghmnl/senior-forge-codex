---
layout: post
title: "SideEffect"
date: 2026-10-09 12:00:00 +0000
categories: [es, glosario]
tags: [compose, lifecycle]
lang: es
permalink: /es/glosario/side-effect/
---

## The Theory (El Qué)

**`SideEffect { }`** ejecuta su bloque **después de cada [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}) exitosa**, una vez aplicados los cambios. Es la forma de publicar estado de Compose hacia código que Compose no maneja, como un objeto de analytics o una vista de otro framework. En cambio, un efecto secundario escrito directamente en el cuerpo de un composable puede correr durante una [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}) que después se descarta.

```kotlin
// Not found in FAS — standalone example
SideEffect { analytics.setUserProperty("theme", theme.name) }
```

## The Senior Nuance (El Matiz Senior)

- **Corre en cada [recomposition]({{ "/es/glosario/recomposition/" | relative_url }})**, así que sirve para actualizaciones idempotentes ("fijar este valor"), no para acciones de una sola vez. Para "una vez al mostrarse", `LaunchedEffect(Unit)`.
- **Nunca corre para una [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}) descartada**, que es justamente por qué es más seguro que escribir la llamada en el cuerpo.
- Ver [Recomposition & Stability]({{ "/es/03-jetpack-compose/recomposition-stability/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
