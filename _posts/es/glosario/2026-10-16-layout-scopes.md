---
layout: post
title: "Layout Scopes (BoxScope, RowScope, ColumnScope)"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, layout, dsl]
lang: es
permalink: /es/glosario/layout-scopes/
---

## The Theory (El Qué)

**`BoxScope`**, **`RowScope`** y **`ColumnScope`** son los receptores de las lambdas de contenido de [`Box`]({{ "/es/glosario/box/" | relative_url }}), [`Row`]({{ "/es/glosario/row/" | relative_url }}) y [`Column`]({{ "/es/glosario/column/" | relative_url }}). Proveen [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) que solo tienen sentido adentro de ese padre, como `align` y [`weight`]({{ "/es/glosario/weight/" | relative_url }}), así que usarlos en cualquier otro lugar no compila.

```kotlin
// Not found in FAS — standalone example
Box { Text("Hi", Modifier.align(Alignment.Center)) }   // align exists only in BoxScope
```

## The Senior Nuance (El Matiz Senior)

- **Los [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) restringidos a un scope son una red de seguridad en compilación**: el padre es dueño del posicionamiento, así que solo se le puede pedir al padre correcto.
- **[`@LayoutScopeMarker`]({{ "/es/glosario/layout-scope-marker/" | relative_url }})** evita que los [modifiers]({{ "/es/glosario/modifier/" | relative_url }}) de un scope externo se filtren en layouts anidados.
- Ver [Modifiers: Order & Alignment]({{ "/es/03-jetpack-compose/modifiers-order-alignment/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
