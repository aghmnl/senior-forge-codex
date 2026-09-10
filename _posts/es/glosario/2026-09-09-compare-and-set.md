---
layout: post
title: "Compare-and-Set (CAS)"
date: 2026-09-09 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/compare-and-set/
---

## The Theory (El Qué)

**Compare-and-set** (CAS) es una primitiva a nivel de hardware: "escribí este valor nuevo, pero solo si el valor actual sigue siendo el que leí". Devuelve `true` si lo logró y `false` si otro ganó la carrera, en cuyo caso el caller reintenta con el valor fresco. Es la base de la concurrencia lock-free.

```kotlin
// El retry loop sobre el que está construido MutableStateFlow.update
public inline fun <T> MutableStateFlow<T>.update(function: (T) -> T) {
    while (true) {
        val prevValue = value
        val nextValue = function(prevValue)
        if (compareAndSet(prevValue, nextValue)) return
    }
}
```

## The Senior Nuance (El Matiz Senior)

- CAS cambia bloquear por reintentar. Un [Synchronized Block]({{ "/es/glosario/synchronized-block/" | relative_url }}) estaciona el thread hasta que el lock se libera; CAS nunca estaciona, simplemente recalcula. Con contención baja — que es lo que ve un state holder de [ViewModel]({{ "/es/glosario/viewmodel-store/" | relative_url }}) — eso es dramáticamente más barato y sin riesgo de deadlock.
- El reintento implica que **la lambda debe ser pura**. Puede ejecutarse más de una vez, así que un `update { it.copy(...) ; analytics.log() }` va a loguear doble bajo contención. Los side effects van afuera del bloque.
- CAS compara por *identidad de referencia*, no por [`equals`]({{ "/es/glosario/equals/" | relative_url }}). Por eso el objeto de estado debe ser [inmutable]({{ "/es/glosario/immutability/" | relative_url }}): un objeto mutable editado in-place conserva su identidad, así que CAS no puede detectar que algo cambió — el clásico problema ABA en su forma cotidiana de Android.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
