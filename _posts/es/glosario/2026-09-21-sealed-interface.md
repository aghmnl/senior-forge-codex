---
layout: post
title: "sealed interface"
date: 2026-09-21 12:00:00 +0000
categories: [es, glosario]
tags: [sealed-types, oop, architecture]
lang: es
permalink: /es/glosario/sealed-interface/
---

## The Theory (El Qué)

**`sealed interface`** (Kotlin 1.5+) declara una [jerarquía sellada]({{ "/es/glosario/sealed-hierarchy/" | relative_url }}) como interfaz: el conjunto de implementaciones queda cerrado al mismo paquete y módulo, así que un [`when`]({{ "/es/glosario/when-expression/" | relative_url }}) sobre ella es exhaustivo sin `else`. A diferencia de una [`sealed class`]({{ "/es/glosario/sealed-class/" | relative_url }}) no tiene constructor, ni bloque [`init`]({{ "/es/glosario/init/" | relative_url }}), ni estado — pero un tipo puede implementar **varias** sealed interfaces a la vez, algo que la herencia simple les impide a las clases. Por eso es el mejor default para estado de UI, eventos de navegación y acciones de dominio.

```kotlin
// De FollowApp Suite — StateChip.kt
// Sin estado compartido: cada implementación define sus colores y comportamiento,
// y queda libre para implementar además otras interfaces
sealed interface ChipState {
    val foreground: Color @Composable get
    val strikethrough: Boolean get() = false
    @Composable fun filterColors(): SelectableChipColors
}
```

## The Senior Nuance (El Matiz Senior)

- **Usala por defecto; escalá a una [`sealed class`]({{ "/es/glosario/sealed-class/" | relative_url }}) solo por estado compartido.** La mayoría de las jerarquías son apenas un conjunto cerrado de formas independientes, y arrancar con una interfaz deja la puerta abierta a un segundo contrato más adelante.
- **Puede llevar comportamiento, no estado.** Se permiten implementaciones por defecto (`val strikethrough: Boolean get() = false`); backing fields no.
- **Pertenecer a varias jerarquías es la feature.** Un tipo puede ser a la vez un `UiState` y un evento de `Analytics`; con sealed classes habría que elegir una jerarquía y colgar el resto aparte.
- Ver [Sealed Classes vs Sealed Interfaces]({{ "/es/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
