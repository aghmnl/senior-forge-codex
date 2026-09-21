---
layout: post
title: "componentN"
date: 2026-09-19 12:00:00 +0000
categories: [es, glosario]
tags: [data-classes, syntax, compiler]
lang: es
permalink: /es/glosario/component-n/
---

## The Theory (El Qué)

**`componentN()`** son las `operator fun component1()`, `component2()`, … que genera una data class ([Data Classes: copy, equals, toString]({{ "/es/01-kotlin-core/data-classes/" | relative_url }})), una por cada propiedad del [constructor primario]({{ "/es/glosario/primary-constructor/" | relative_url }}), en orden de declaración. Son aquello en lo que compilan las declaraciones de [destructuring]({{ "/es/glosario/destructuring/" | relative_url }}): `val (name, age) = user` se convierte en `val name = user.component1(); val age = user.component2()`. Cualquier clase puede sumarse declarando esos operadores a mano — el destructuring es una convención, no un privilegio de las data classes.

```kotlin
// De FollowApp Suite — MyTasksApplication.kt
// Triple es una data class: component1/2/3 hacen funcionar este destructuring
val (language, themeMode, contrastLevel) = runBlocking { ... }

// Sumarse sin ser data class
class Size(val w: Int, val h: Int) {
    operator fun component1() = w
    operator fun component2() = h
}
val (w, h) = Size(1080, 1920)
```

## The Senior Nuance (El Matiz Senior)

- **Posicional, no por nombre.** `val (a, b) = point` liga por *posición*; reordenar el constructor primario intercambia las variables en cada lugar donde se destructura, en silencio y sin romper la compilación. Ese es el argumento contra destructurar clases con varias propiedades del mismo tipo.
- **Excelente para pares, entradas y lambdas.** `map.forEach { (k, v) -> }`, `list.withIndex()`, retornos con [`Triple`]({{ "/es/glosario/triple/" | relative_url }}): ahí el significado de cada posición es obvio y el destructuring saca ruido.
- **Usá `_` para saltear.** `val (_, themeMode, _) = config` documenta que solo te interesa el valor del medio.
- Ver [Data Classes: copy, equals, toString]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
