---
layout: post
title: "Upper Bound"
date: 2026-09-07 12:00:00 +0000
categories: [es, glosario]
tags: [generics, type-system]
lang: es
permalink: /es/glosario/upper-bound/
---

## The Theory (El Qué)

Un **Upper Bound** (cota superior) restringe qué tipos pueden sustituir a un [Generic Type Parameter]({{ "/es/glosario/generic-type-parameters/" | relative_url }}). Se escribe con dos puntos: `<K : Any>` significa "cualquier `K`, siempre que sea subtipo de `Any`".

Sin un bound explícito, el upper bound implícito es `Any?` — que admite tipos nullable. Declarar `: Any` es entonces la forma de exigir non-null:

```kotlin
// From FollowApp Suite — DragToReorder.kt
// K se usa como clave de mapa, así que debe ser non-null.
class ReorderState<K : Any> internal constructor(/* ... */) {
    private val itemCoords = mutableMapOf<K, LayoutCoordinates>()
}

@Composable
fun <K : Any> rememberReorderState(
    keys: List<K>,
    onMove: (fromKey: K, toKey: K) -> Boolean,
    // ...
): ReorderState<K>
```

Múltiples bounds requieren la cláusula `where`, ya que solo uno entra en los angle brackets:

```kotlin
// Not found in FAS — standalone example
fun <T> sortAndLog(items: List<T>): List<T>
    where T : Comparable<T>,
          T : CharSequence = items.sorted()
```

## The Senior Nuance (El Matiz Senior)

- **El bound es lo que el compilador sabe.** Dentro de una función genérica, solo podés llamar miembros garantizados por el upper bound. Con `<T>` (bound `Any?`) no podés ni llamar `toString()` sin chequear null; con `<T : Any>` sí. Elegir el bound es elegir la API disponible en el cuerpo.
- **`: Any` es el bound más común en código Android**, porque las claves de mapa, los elementos de [Collections]({{ "/es/glosario/collections/" | relative_url }}) usados para identidad, y cualquier cosa comparada con `==` se comportan mal cuando se permite null. `ReorderState<K : Any>` es exactamente ese caso: las keys indexan un `mutableMapOf`.
- **Los bounds deben repetirse en cada declaración de la API.** Las [Extension Functions]({{ "/es/glosario/extension-functions/" | relative_url }}) que consumen `ReorderState` reenuncian todas `<K : Any>`, y eso es lo que mantiene a `K` como un único tipo consistente en toda la API del gesto, en vez de degradarse a `Any?` en algún límite.
- **Las lecturas de una [Star Projection]({{ "/es/glosario/star-projection/" | relative_url }}) se amplían al upper bound.** Dado `ReorderState<*>`, `draggingKey` vuelve tipado como `Any?` — el bound, no el tipo real. Cuanto más ajustado el bound, más útiles son las lecturas star-projected.
- **Los bounds también se borran.** Después del [Type Erasure]({{ "/es/glosario/type-erasure/" | relative_url }}), un parámetro `<T : CharSequence>` se compila como `CharSequence` en vez de `Object`. Esto es ocasionalmente visible en el [Bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) y en las firmas de interop con Java.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
