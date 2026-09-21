---
layout: post
title: "sealed class"
date: 2026-09-21 12:00:00 +0000
categories: [es, glosario]
tags: [sealed-types, oop, state-management]
lang: es
permalink: /es/glosario/sealed-class/
---

## The Theory (El Qué)

**`sealed class`** declara una [jerarquía sellada]({{ "/es/glosario/sealed-hierarchy/" | relative_url }}) cuyos subtipos directos tienen que vivir todos en el mismo paquete y módulo. Al ser una clase, puede llevar estructura compartida: propiedades en el [constructor]({{ "/es/glosario/primary-constructor/" | relative_url }}), miembros [`abstract`]({{ "/es/glosario/abstract-class/" | relative_url }}) que cada subtipo debe proveer, métodos concretos, un bloque [`init`]({{ "/es/glosario/init/" | relative_url }}) y un [companion object]({{ "/es/glosario/companion-object/" | relative_url }}). Eso es lo que la separa de una [`sealed interface`]({{ "/es/glosario/sealed-interface/" | relative_url }}) — y el precio es la herencia simple de la JVM, así que un subtipo puede extender solo una.

```kotlin
// De FollowApp Suite — CascadeAction en TasksUiState.kt
// Estado compartido declarado una vez en la base, provisto por cada variante
sealed class CascadeAction {
    abstract val taskId: String
    abstract val childCount: Int

    data class Archive(
        override val taskId: String,
        override val childCount: Int
    ) : CascadeAction()
}
```

## The Senior Nuance (El Matiz Senior)

- **Usala solo cuando la jerarquía comparte algo de verdad.** Propiedades comunes, un método compartido, una validación en `init` o un companion con constantes. Sin alguna de esas, una [`sealed interface`]({{ "/es/glosario/sealed-interface/" | relative_url }}) es el mejor default.
- **`abstract val` en la base, `override val` en cada variante.** Así el contrato compartido se declara una sola vez en vez de repetir campos — y el compilador lo exige.
- **La herencia simple es la restricción real.** Si una variante además tiene que cumplir un segundo contrato (analytics, logging), la sealed class no puede dárselo; las variantes implementan también una interfaz, o toda la jerarquía pasa a ser una sealed interface.
- Ver [Sealed Classes vs Sealed Interfaces]({{ "/es/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
