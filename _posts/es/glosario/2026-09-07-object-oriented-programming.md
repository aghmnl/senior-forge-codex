---
layout: post
title: "Object-Oriented Programming"
date: 2026-09-07 12:00:00 +0000
categories: [es, glosario]
tags: [oop, design-principles]
lang: es
permalink: /es/glosario/object-oriented-programming/
---

## The Theory (El Qué)

La **Object-Oriented Programming (OOP)** — programación orientada a objetos — es el paradigma que modela un programa como objetos, es decir paquetes de estado junto con el comportamiento que opera sobre él, en vez de como procedimientos sobre datos compartidos. Se apoya en cuatro pilares:

- **Encapsulamiento** — el estado interno es privado; el objeto expone una superficie controlada. La visibilidad `private`/`internal` de Kotlin y los [Backing Fields]({{ "/es/glosario/backing-field/" | relative_url }}) son las herramientas.
- **Abstracción** — los callers dependen de una interfaz o [Abstract Class]({{ "/es/glosario/abstract-class/" | relative_url }}), no de una implementación concreta.
- **[Inheritance]({{ "/es/glosario/inheritance/" | relative_url }})** — una [Subclase]({{ "/es/glosario/subclass/" | relative_url }}) reutiliza y especializa el comportamiento de un padre.
- **[Polymorphism]({{ "/es/glosario/polymorphism/" | relative_url }})** — un tipo de referencia representa muchas implementaciones, resuelto por el [Method Dispatch]({{ "/es/glosario/method-dispatch/" | relative_url }}).

```kotlin
// From FollowApp Suite — PremiumLedgerRepositoryImpl.kt
// Abstracción: los callers dependen de la interfaz, no de esta clase.
class PremiumLedgerRepositoryImpl(
    private val preferences: PremiumLedgerPreferences
) : PremiumLedgerRepository {
    override fun getLedger(): Flow<PremiumLedger> = preferences.getLedger()
}
```

## The Senior Nuance (El Matiz Senior)

- **Kotlin desalienta deliberadamente la [Inheritance]({{ "/es/glosario/inheritance/" | relative_url }}).** Las clases y los métodos son [`final`]({{ "/es/glosario/final/" | relative_url }}) por defecto; tenés que optar explícitamente con `open`. Esto invierte el default de Java y codifica "preferí composición sobre herencia" dentro del lenguaje, en vez de dejarlo librado a una guía de estilo.
- **El Android moderno es solo parcialmente OOP.** [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) es declarativo y basado en funciones — un `@Composable` no es una jerarquía de clases. Un Senior lee Android por capas: OOP para la [Data Layer]({{ "/es/glosario/data-layer/" | relative_url }}) y los [State Holders]({{ "/es/glosario/state-holder/" | relative_url }}), [Functional Style]({{ "/es/glosario/functional-style/" | relative_url }}) para las transformaciones, declarativo para la UI. Insistir con un solo paradigma en todos lados es el error.
- **Las [Sealed Hierarchies]({{ "/es/glosario/sealed-hierarchy/" | relative_url }}) son la respuesta de la OOP a los [Algebraic Data Types]({{ "/es/glosario/algebraic-data-types/" | relative_url }}).** Dan [Polymorphism]({{ "/es/glosario/polymorphism/" | relative_url }}) más [Exhaustividad]({{ "/es/glosario/exhaustiveness/" | relative_url }}) — el compilador conoce el conjunto completo de [Subclases]({{ "/es/glosario/subclass/" | relative_url }}), así que el `when` no necesita `else`.
- **Los principios [SOLID]({{ "/es/glosario/single-responsibility-principle/" | relative_url }}) son reglas de diseño OOP, no leyes.** Vale citarlos en una entrevista, pero un Senior justifica un diseño por su acoplamiento y su testeabilidad, no por nombrar un principio.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
