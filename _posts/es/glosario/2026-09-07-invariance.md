---
layout: post
title: "Invariance"
date: 2026-09-07 12:00:00 +0000
categories: [es, glosario]
tags: [generics, type-system]
lang: es
permalink: /es/glosario/invariance/
---

## The Theory (El Qué)

La **Invarianza** es la [Varianza]({{ "/es/glosario/variance/" | relative_url }}) por defecto de Kotlin: `Box<Cat>` y `Box<Animal>` *no* tienen relación de subtipado en ninguna dirección, aunque `Cat` sea subtipo de `Animal`. Un [Generic Type Parameter]({{ "/es/glosario/generic-type-parameters/" | relative_url }}) escrito sin `in` ni `out` es invariante.

Es la respuesta correcta siempre que el tipo se produce y se consume:

```kotlin
// From FollowApp Suite — DragToReorder.kt
@Stable
class ReorderState<K : Any> internal constructor(
    private val onMove: (fromKey: K, toKey: K) -> Boolean,   // K consumido
    private val onLongPressOnly: (K) -> Unit                 // K consumido
) {
    var draggingKey: K? by mutableStateOf(null)              // K producido
        private set

    internal var liveKeys: List<K> = emptyList()             // K producido

    fun isDragging(key: K): Boolean = key == draggingKey     // K consumido
}
```

`ReorderState` no puede ser `out K` (`isDragging` recibe un `K`) ni `in K` (`draggingKey` devuelve uno). La invarianza acá no es una anotación faltante — es el sistema de tipos reportando correctamente que este objeto es dueño de `K` en ambas direcciones.

## The Senior Nuance (El Matiz Senior)

- **La invarianza es una señal, no un fracaso.** Cuando el compilador rechaza `out`, te está diciendo que la clase consume el tipo en algún lado. Forzar la varianza y tapar los agujeros con casts inseguros convierte un error de [Compile Time]({{ "/es/glosario/compile-time/" | relative_url }}) en una [`ClassCastException`]({{ "/es/glosario/class-cast-exception/" | relative_url }}) en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}) — estrictamente peor.
- **`MutableList<E>` es el ejemplo cotidiano.** Es invariante porque lee y escribe; `List<out E>` es [Covariante]({{ "/es/glosario/covariance/" | relative_url }}) porque solo lee. El mismo par de clases explica `Channel<E>` (invariante) frente a `Flow<out T>` (covariante) en [Coroutines]({{ "/es/glosario/coroutines/" | relative_url }}).
- **La vía de escape es la projection, no el cast.** Si un caller realmente no le importa el type argument, dale una [Star Projection]({{ "/es/glosario/star-projection/" | relative_url }}) (`ReorderState<*>`) o una projection de sitio de uso (`Array<out Any>`). Ambas mantienen el [Type Safety]({{ "/es/glosario/type-safety/" | relative_url }}) restringiendo qué operaciones quedan disponibles, en vez de descartarlo.
- **Los arrays son invariantes en Kotlin y covariantes en Java** — un arreglo deliberado. El `Object[] a = new String[1]; a[0] = 1;` de Java compila y lanza `ArrayStoreException` en runtime. El `Array<T>` de Kotlin es invariante, así que el mismo error es un error de compilación. Es una repregunta favorita en entrevistas.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
