---
layout: post
title: "Exhaustiveness"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/exhaustiveness/
---

## The Theory (El Qué)

**Exhaustiveness** (exhaustividad) es la garantía del compilador de que una expresión `when` cubre todos los casos posibles de una jerarquía de tipos. Cuando el sujeto de un `when` es una [sealed class]({{ "/es/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}) o [sealed interface]({{ "/es/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}), el compilador conoce el conjunto completo de subtipos y exige que cada uno sea manejado — no se necesita rama `else`. Si se agrega un nuevo subtipo después, cada `when` exhaustivo que lo omita se convierte en un error de [compile time]({{ "/es/glosario/compile-time/" | relative_url }}), forzando al desarrollador a manejar el nuevo caso explícitamente.

```kotlin
// From FollowApp Suite — TaskConfirmationDialogs.kt
val (titleRes, messageRes) = when (action) {
    is BulkAction.Complete -> R.string.bulk_complete_title to R.string.bulk_complete_message
    is BulkAction.Archive  -> R.string.bulk_archive_title to R.string.bulk_archive_message
    is BulkAction.Delete   -> R.string.bulk_delete_title to R.string.bulk_delete_message
}
```

Sin rama `else` — el compilador verifica que `Complete`, `Archive` y `Delete` cubren cada subtipo de `BulkAction`. Agregar un cuarto subtipo rompería inmediatamente este `when`, surfaceando la omisión en build time en lugar de como un crash en [Runtime]({{ "/es/glosario/runtime/" | relative_url }}).

## The Senior Nuance (El Matiz Senior)

- La exhaustividad es la razón principal por la que existen las [sealed classes]({{ "/es/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}). El diseño [final]({{ "/es/glosario/final/" | relative_url }})-by-default de Kotlin restringe la herencia; las jerarquías sealed extienden esa restricción a un conjunto conocido de subtipos, habilitando al compilador a razonar sobre completitud.
- **Nunca agregues una rama `else` por defecto** a un `when` sobre un tipo sealed. Un `else` silencia al compilador: los nuevos subtipos se rutean silenciosamente al path por defecto en lugar de triggear un error de compilación. Este es el error más común — convierte una red de seguridad de [compile time]({{ "/es/glosario/compile-time/" | relative_url }}) en un bug de [Runtime]({{ "/es/glosario/runtime/" | relative_url }}).
- En FAS, el mismo patrón se repite para `CascadeAction`:

```kotlin
// From FollowApp Suite — TaskConfirmationDialogs.kt
val (titleRes, messageRes) = when (action) {
    is CascadeAction.Complete ->
        if (action.isCompleted) R.string.cascade_complete_title to R.string.cascade_complete_message
        else R.string.cascade_uncomplete_title to R.string.cascade_uncomplete_message
    is CascadeAction.Archive -> R.string.cascade_archive_title to R.string.cascade_archive_message
    is CascadeAction.Delete  -> R.string.cascade_delete_title to R.string.cascade_delete_message
}
```

- La exhaustividad también aplica a [enum classes]({{ "/es/glosario/enum/" | relative_url }}) y, desde Kotlin 1.7, a sealed interfaces — habilitando patrones de [polimorfismo]({{ "/es/glosario/polymorphism/" | relative_url }}) donde la jerarquía de tipos abarca múltiples árboles de herencia pero el compilador aún garantiza completitud.
- En arquitecturas MVI/UDF (comunes en Android), las sealed classes modelan estados de pantalla (`Loading`, `Content`, `Error`) y el `when` en la capa de UI es exhaustivo — garantizando que cada estado tiene un rendering correspondiente. Este es un patrón clave en código UI de [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
