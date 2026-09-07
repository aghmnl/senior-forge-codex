---
layout: post
title: "Covariance"
date: 2026-09-07 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/covariance/
---

## The Theory (El Qué)

La **Covarianza** es la [Varianza]({{ "/es/glosario/variance/" | relative_url }}) que preserva la dirección del subtipado: si `Cat` es subtipo de `Animal`, entonces `Producer<Cat>` es subtipo de `Producer<Animal>`. Kotlin la declara con `out`:

```kotlin
// Not found in FAS — standalone example
interface Producer<out T> {
    fun produce(): T          // T solo en un return type — legal
    // fun consume(item: T)   // ERROR: T en una posición "in"
}

val cats: Producer<Cat> = CatFactory()
val animals: Producer<Animal> = cats   // OK: covarianza
```

El [Keyword]({{ "/es/glosario/keyword/" | relative_url }}) `out` es a la vez un permiso y una restricción: otorga la relación de subtipado y, a cambio, el compilador prohíbe que `T` aparezca en cualquier lugar que no sea un [Return Type]({{ "/es/glosario/return-type/" | relative_url }}). La clase solo puede *producir* `T`, nunca consumirlo.

El tipo covariante más usado de Kotlin es la lista de solo lectura:

```kotlin
// From FollowApp Suite — SelectableListScaffold.kt
fun <T> SelectableListScaffold(
    items: List<T>,        // List<out E>: covariante, read-only
    itemKey: (T) -> String,
    // ...
)
```

## The Senior Nuance (El Matiz Senior)

- **La covarianza es válida solo sin escrituras.** Si `MutableList<E>` fuera covariante, podrías ligar un `MutableList<Cat>` a una referencia `MutableList<Animal>` y después hacer `add(Dog())` — la lista guardaría un `Dog` mientras cada lector espera un `Cat`, produciendo una [`ClassCastException`]({{ "/es/glosario/class-cast-exception/" | relative_url }}) lejos del bug real. La división read-only/mutable de las [Collections]({{ "/es/glosario/collections/" | relative_url }}) de Kotlin existe para volver segura la covarianza: `List<out E>` es covariante, `MutableList<E>` es [Invariante]({{ "/es/glosario/invariance/" | relative_url }}). Es la [Immutability]({{ "/es/glosario/immutability/" | relative_url }}) pagándose sola dentro del sistema de tipos.
- **Corresponde al `? extends T` de Java.** PECS ("Producer-Extends") es la misma regla enunciada en el sitio de uso. La ventaja de Kotlin es que `out` se declara una sola vez en la clase, así ningún [Call Site]({{ "/es/glosario/call-site/" | relative_url }}) tiene que repetirlo.
- **`Flow<out T>` y `Deferred<out T>` son covariantes** exactamente por esta razón: solo emiten valores. `SendChannel<in E>` es [Contravariante]({{ "/es/glosario/contravariance/" | relative_url }}), y `Channel<E>` — que hace ambas cosas — es invariante. Leer la API de [Coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) con la lente de la varianza te dice cuáles son productores, consumidores o ambos, sin leer un solo método.
- **`out` también expresa pertenencia.** Declarar una [Sealed Hierarchy]({{ "/es/glosario/sealed-hierarchy/" | relative_url }}) de resultados como `sealed interface Result<out T>` permite que `Result.Loading` (que no carga ningún `T`) sea un `Result<Nothing>` y por lo tanto asignable a cualquier `Result<X>`. Ese truco solo está disponible gracias a la covarianza.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
