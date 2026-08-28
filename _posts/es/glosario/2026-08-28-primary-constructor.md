---
layout: post
title: "Primary Constructor"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/primary-constructor/
---

## The Theory (El Qué)

Un **primary constructor** (constructor primario) en Kotlin se declara directamente en el encabezado de la clase, después del nombre. Sus parámetros pueden promoverse a propiedades con `val` o `var`, y el compilador los usa para definir el contrato de inicialización de la clase. A diferencia de Java, donde los constructores viven dentro del cuerpo de la clase, el primary constructor de Kotlin es parte de la firma de la clase misma.

```kotlin
// De FollowApp Suite — BillingConnector.kt
class BillingConnector(
    context: Context,
    private val productId: String
) {
    private val _isOwned = MutableStateFlow<Boolean?>(null)
    val isOwned: StateFlow<Boolean?> = _isOwned.asStateFlow()
}
```

## The Senior Nuance (El Matiz Senior)

- En una `data class`, el primary constructor es crítico: el compilador genera `equals()`, `hashCode()`, `toString()`, `copy()` y `componentN()` exclusivamente a partir de sus parámetros. Las propiedades declaradas en el cuerpo son invisibles para estos métodos generados — una fuente común de bugs sutiles.
- Los parámetros del primary constructor sin `val`/`var` son solo argumentos del constructor, accesibles únicamente durante la inicialización (en bloques `init` e inicializadores de propiedades). Agregar `val`/`var` los promueve a propiedades de clase con backing fields. Esta distinción importa para la memoria y la visibilidad.
- Una clase puede tener constructores secundarios (declarados con `constructor` en el cuerpo), pero deben delegar al primary constructor — directa o indirectamente. Esto asegura que el contrato del primary constructor siempre se cumpla.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
