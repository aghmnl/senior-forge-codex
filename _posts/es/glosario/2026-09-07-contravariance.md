---
layout: post
title: "Contravariance"
date: 2026-09-07 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/contravariance/
---

## The Theory (El Qué)

La **Contravarianza** es la [Varianza]({{ "/es/glosario/variance/" | relative_url }}) que *invierte* la dirección del subtipado: si `Cat` es subtipo de `Animal`, entonces `Consumer<Animal>` es subtipo de `Consumer<Cat>`. Kotlin la declara con `in`:

```kotlin
// Not found in FAS — standalone example
interface Consumer<in T> {
    fun consume(item: T)     // T solo en un parámetro — legal
    // fun produce(): T      // ERROR: T en una posición "out"
}

val animalSink: Consumer<Animal> = AnimalLogger()
val catSink: Consumer<Cat> = animalSink   // OK: contravarianza
```

La inversión es intuitiva una vez dicha en lenguaje llano: algo que puede manejar *cualquier* `Animal` ciertamente puede manejar un `Cat`. Un consumidor de un tipo más amplio es usable dondequiera que se requiera un consumidor de un tipo más angosto.

## The Senior Nuance (El Matiz Senior)

- **Corresponde al `? super T` de Java** — la mitad "Consumer-Super" de PECS. `Comparable<in T>` es el ejemplo canónico en ambos lenguajes: un `Comparable<Any>` puede comparar `String`s, así que es usable con seguridad como `Comparable<String>`.
- **La contravarianza es mucho más rara que la [Covarianza]({{ "/es/glosario/covariance/" | relative_url }}) en código de aplicación**, porque la mayoría de los tipos genéricos que escribís entregan valores *hacia afuera* en vez de tragarlos. Donde aparece es en [Callbacks]({{ "/es/glosario/callbacks/" | relative_url }}), comparators y sinks de eventos — todo aquello cuyo trabajo entero es recibir.
- **Los parámetros de función son contravariantes, y dependés de esto a diario.** `(T) -> R` compila a `Function1<in P1, out R>`. Por eso un handler tipado `(Any) -> Unit` puede pasarse donde se espera `(Task) -> Unit`, pero no al revés. Cada parámetro [Lambda]({{ "/es/glosario/lambdas/" | relative_url }}) de una API genérica — `itemKey: (T) -> String`, `onMove: (K, K) -> Boolean` — hereda esto sin ninguna anotación.
- **La regla de override lo refleja.** Un [Return Type]({{ "/es/glosario/return-type/" | relative_url }}) puede angostarse al sobreescribir; un tipo de parámetro no, porque los parámetros están en la posición contravariante. Intentarlo produce un overload, no un override — un bug silencioso clásico que las reglas de [Function Overloading]({{ "/es/glosario/function-overloading/" | relative_url }}) te dejarán mandar a producción sin chistar.
- **Un tipo que consume y produce no puede ser `in`.** Si `T` aparece aunque sea en un solo [Return Type]({{ "/es/glosario/return-type/" | relative_url }}), la clase debe quedar [Invariante]({{ "/es/glosario/invariance/" | relative_url }}). La regla posicional es simétrica y no admite excepciones fuera de `@UnsafeVariance`.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
