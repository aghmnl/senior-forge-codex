---
layout: post
title: "Inheritance"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/inheritance/
---

## The Theory (El Qué)

**Inheritance** (herencia) es el mecanismo por el cual una clase (subclase) adquiere las propiedades y comportamiento de otra clase (superclase). En Kotlin, las clases son `final` por defecto — no pueden heredarse a menos que se marquen explícitamente como `open`. Las interfaces, clases abstractas y jerarquías sealed proveen formas controladas de herencia.

```kotlin
// De FollowApp Suite — StateChip.kt
sealed interface ChipState {
    val foreground: Color @Composable get
    val border: BorderStroke? @Composable get
    val strikethrough: Boolean get() = false
    @Composable fun inputColors(): SelectableChipColors
    @Composable fun filterColors(): SelectableChipColors
}

object Full : ChipState {
    override val foreground: Color
        @Composable get() = MaterialTheme.colorScheme.onPrimaryContainer
    override val border: BorderStroke? @Composable get() = null
    // ...
}
```

## The Senior Nuance (El Matiz Senior)

- El "final por defecto" de Kotlin es una decisión de diseño deliberada: la herencia es la forma más fuerte de acoplamiento. Abrir una clase crea un contrato permanente — cada miembro público y protegido se convierte en una API de la que dependen las subclases. Usá `open` intencionalmente, no por costumbre.
- Las data classes no pueden ser `open` (desde Kotlin 1.1+). Esto evita que la herencia rompa los `equals()`, `hashCode()` y `copy()` generados por el compilador — que dependen exclusivamente del [constructor primario]({{ "/es/glosario/primary-constructor/" | relative_url }}).
- Preferí composición sobre herencia. Una sealed interface (como el ejemplo FAS) define un contrato sin acoplamiento de implementación: cada implementador es independiente. Cuando necesitás comportamiento compartido, usá [extension functions]({{ "/es/glosario/extension-functions/" | relative_url }}) o delegación (`by`) en vez de una jerarquía de clases profunda.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
