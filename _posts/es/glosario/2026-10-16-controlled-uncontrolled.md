---
layout: post
title: "Controlled & Uncontrolled"
date: 2026-10-16 12:00:00 +0000
categories: [es, glosario]
tags: [compose, state-management, architecture]
lang: es
permalink: /es/glosario/controlled-uncontrolled/
---

## The Theory (El Qué)

Un componente reutilizable es **controlado** cuando quien lo llama le pasa el valor actual y maneja el evento de cambio, así que el dueño del estado es quien lo llama. Es **no controlado** cuando el componente guarda su propio estado internamente y quien lo llama solo fija un valor inicial. Muchos componentes de un [design system]({{ "/es/glosario/design-system/" | relative_url }}) admiten los dos, normalmente con un parámetro de valor opcional: `null` significa "manejalo vos".

```kotlin
// Not found in FAS — standalone example
@Composable
fun Expandable(expanded: Boolean? = null, onExpandedChange: ((Boolean) -> Unit)? = null) {
    var internal by remember { mutableStateOf(false) }
    val isExpanded = expanded ?: internal
    // al alternar: if (expanded == null) internal = !isExpanded; onExpandedChange?.invoke(!isExpanded)
}
```

## The Senior Nuance (El Matiz Senior)

- **Controlado cuando el estado hay que persistirlo o coordinarlo** con otras partes de la pantalla; no controlado cuando a nadie más le importa.
- **Nunca mezclar los dos en silencio.** Si se pasa un valor, el componente no debe cambiar también su estado interno, o las dos fuentes se desincronizan.
- Ver [State Hoisting]({{ "/es/03-jetpack-compose/state-hoisting/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
