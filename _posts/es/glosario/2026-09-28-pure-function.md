---
layout: post
title: "Pure Function"
date: 2026-09-28 12:00:00 +0000
categories: [es, glosario]
tags: [functional, design-principles, testing]
lang: es
permalink: /es/glosario/pure-function/
---

## The Theory (El Qué)

Una **función pura** es una función que **siempre devuelve el mismo resultado para las mismas entradas** y **no tiene efectos secundarios**: no cambia nada fuera de sí misma (no escribe estado, no loguea, no llama a la red, no toca la base de datos) y no depende de nada que no esté en sus parámetros, como la hora actual. Su resultado depende solo de sus argumentos.

```kotlin
// De FollowApp Suite — PremiumLifecycle.kt
// Pura: "now" entra como parámetro en vez de leerse del reloj,
// así las mismas entradas siempre dan la misma respuesta
fun isPremium(now: Long, premiumUntil: Long, isSignedIn: Boolean = false): Boolean {
    val effectiveUntil = if (isSignedIn) premiumUntil + SIGN_IN_REWARD_DAYS * DAY_MS else premiumUntil
    return now < effectiveUntil
}
```

## The Senior Nuance (El Matiz Senior)

- **Las funciones puras son triviales de testear.** Sin mocks, sin preparación, sin reloj: se llaman con entradas y se verifica la salida. Pasar "now" como parámetro, como en el ejemplo, es lo que hace testeable la lógica que depende del tiempo.
- **Algunas APIs las exigen.** El lambda de [update {}]({{ "/es/glosario/update/" | relative_url }}) puede correr más de una vez, así que un efecto secundario adentro puede ocurrir dos veces. Mantenerlo puro es lo que hace seguro el reintento.
- **Una app entera no puede ser pura, y está bien.** El objetivo es mantener pura la lógica y empujar los efectos secundarios (I/O, base de datos, UI) a los bordes, donde son pocos y fáciles de ver.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
