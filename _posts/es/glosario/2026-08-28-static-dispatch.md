---
layout: post
title: "Static Dispatch"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/static-dispatch/
---

## The Theory (El Qué)

**Static dispatch** (despacho estático) significa que la función a llamar se determina en [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}), basándose en el tipo declarado de la variable — no en el objeto real en [runtime]({{ "/es/glosario/runtime/" | relative_url }}). Es lo opuesto al dispatch virtual (dinámico), donde la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) busca el método sobreescrito correcto en la vtable del objeto en runtime.

En Kotlin, las [extension functions]({{ "/es/glosario/extension-functions/" | relative_url }}) son el ejemplo más prominente de static dispatch: compilan a métodos estáticos de la [JVM]({{ "/es/glosario/jvm/" | relative_url }}) donde el [receiver type]({{ "/es/glosario/receiver-type/" | relative_url }}) se convierte en el primer parámetro.

## The Senior Nuance (El Matiz Senior)

- El impacto práctico: si existen `fun Animal.greet()` y `fun Dog.greet()`, y llamás a `greet()` en una variable declarada como `Animal` que contiene un `Dog`, se llama la versión de `Animal`. El compilador la eligió en tiempo de compilación — el tipo en runtime es irrelevante. Esto sorprende a desarrolladores que esperan [polimorfismo]({{ "/es/glosario/polymorphism/" | relative_url }}).
- El static dispatch tiene cero overhead — sin lookup de vtable, sin indirección. Por eso las extension functions son tan rápidas como métodos estáticos de utilidad regulares.
- Las funciones de `companion object`, funciones top-level y métodos `@JvmStatic` también usan static dispatch. Entender qué llamadas son estáticas vs. virtuales es esencial para razonar sobre performance y correctitud en Kotlin.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
