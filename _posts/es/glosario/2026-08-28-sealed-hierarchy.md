---
layout: post
title: "Sealed Hierarchy"
date: 2026-08-28 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/sealed-hierarchy/
---

## The Theory (El Qué)

Una **sealed hierarchy** (jerarquía sellada, sealed class o sealed interface) restringe qué clases pueden extenderla — todas las subclases directas deben definirse en el mismo paquete y módulo. Esto le da al compilador un conjunto cerrado de subtipos, habilitando expresiones `when` exhaustivas sin rama default. Las jerarquías selladas son la herramienta principal de Kotlin para modelar [tipos de datos algebraicos (ADTs)]({{ "/es/glosario/algebraic-data-types/" | relative_url }}): un conjunto finito de variantes donde cada variante puede llevar datos diferentes.

```kotlin
// De FollowApp Suite — LabelValue.kt
sealed class LabelValue {
    data class Tag(val values: List<String>) : LabelValue()
    data class Scale(val value: String) : LabelValue()
}
```

## The Senior Nuance (El Matiz Senior)

- El `when` exhaustivo es el beneficio clave: si agregás un nuevo subtipo a una jerarquía sellada, el compilador marca cada `when` que no lo maneja. Esto convierte un crash en runtime (olvidar un caso) en un error de compilación — el compilador es tu verificador de máquina de estados.
- La convención moderna para miembros de jerarquías selladas: usá `data object` para hojas sin estado ([singletons]({{ "/es/glosario/singleton/" | relative_url }}) que no llevan datos) y `data class` para hojas con estado (variantes con propiedades en el [constructor primario]({{ "/es/glosario/primary-constructor/" | relative_url }})). Esto asegura `toString()` limpio, `equals()` consistente y cero [allocations]({{ "/es/glosario/allocations/" | relative_url }}) innecesarias.
- `sealed interface` (Kotlin 1.5+) se prefiere sobre `sealed class` cuando la jerarquía no necesita estado compartido ni bloque `init`. Una sealed interface permite que una subclase implemente múltiples sealed interfaces — algo que las sealed classes no pueden hacer por la [herencia]({{ "/es/glosario/inheritance/" | relative_url }}) simple.
- Las [transiciones de estado]({{ "/es/glosario/state-transitions/" | relative_url }}) en arquitecturas de [flujo unidireccional]({{ "/es/glosario/unidirectional-data-flow/" | relative_url }}) se modelan naturalmente como jerarquías selladas: `Loading`, `Success(data)`, `Error(exception)`.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
