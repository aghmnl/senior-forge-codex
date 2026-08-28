---
layout: page
title: "Data Objects: Singleton y Eficiencia de Memoria"
lang: es
permalink: /es/01-kotlin-core/data-objects/
order: 4
---

## The Theory (El Qué)

Un `data object` (introducido en Kotlin 1.9) combina la garantía de singleton de `object` con los métodos `toString()`, `equals()` y `hashCode()` generados por el compilador como en una `data class`. A diferencia de un `object` simple, que produce un `toString()` por defecto como `Loading@3a71f4dd`, un `data object` genera una representación limpia y legible usando solo el nombre de la clase — por ejemplo, `Loading`. No se generan funciones `copy()` ni `componentN()`, ya que los singletons no tienen propiedades de constructor para copiar o desestructurar.

## The Senior Perspective (El Porqué)

Para un ingeniero Senior, `data object` resuelve un dolor específico en jerarquías selladas y modelado de estado.

- **Logging y Debugging Limpio**: En jerarquías de sealed class, los miembros sin estado como `Loading` o `Idle` declarados como `object` simple producen un toString inútil (`Loading@3a71f4dd`). Un `data object` garantiza una representación legible sin necesidad de sobrescribir manualmente.
- **Garantía de Singleton**: A diferencia de `data class`, un `data object` es un verdadero singleton — existe exactamente una instancia. Esto significa cero asignaciones innecesarias para estados que no llevan datos, lo cual importa en patrones de emisión de estado de alta frecuencia (ej. actualizaciones de StateFlow).
- **Igualdad Consistente**: `equals()` siempre retorna `true` cuando se compara un `data object` consigo mismo (igualdad referencial y estructural son idénticas para singletons). Esto previene bugs sutiles al mezclar verificaciones `==` y `===` en expresiones `when` u operaciones de colecciones.
- **Best Practice en Sealed Hierarchies**: La convención moderna es usar `data object` para miembros sin estado y `data class` para miembros con estado dentro de una jerarquía sellada.

## Code in Action

```kotlin
// De FollowApp Suite — RecurrenceRule.kt
// Jerarquía sellada mixta: data object para hojas sin estado,
// data class para hojas que llevan datos
sealed class RecurrenceEnd {
    data object Never : RecurrenceEnd()
    data class AfterOccurrences(val remaining: Int) : RecurrenceEnd()
    data class UntilDate(val date: Long) : RecurrenceEnd()
}

// De FollowApp Suite — ArchiveUiState.kt
// data object (Kotlin 1.9+): toString limpio, equals consistente
sealed class ArchiveBulkAction {
    data object Unarchive : ArchiveBulkAction()
    data object Delete : ArchiveBulkAction()
}

// De FollowApp Suite — BulkSelection.kt
// Contraste: object simple (pre-1.9) — mismo patrón, pero toString
// produce "Archive@3a71f4dd" en vez de "Archive"
sealed class BulkAction {
    data class Complete(val isCompleted: Boolean) : BulkAction()
    object Archive : BulkAction()   // pre-1.9: sin toString limpio
    object Delete : BulkAction()
}

// De FollowApp Suite — FilterState.kt
// ADT sellado con singletons object para variantes sin estado
sealed class ScaleFilterState {
    object Off : ScaleFilterState()
    data class Include(val values: Set<String>) : ScaleFilterState()
    object Exclude : ScaleFilterState()
}

fun main() {
    // data object: logging legible
    println(RecurrenceEnd.Never)           // "Never"
    println(ArchiveBulkAction.Unarchive)   // "Unarchive"

    // object simple: logging inútil
    println(BulkAction.Archive)            // "Archive@3a71f4dd"
    println(ScaleFilterState.Off)          // "Off@7c53a9eb"
}
```

## Preparación para Entrevistas (En el banquillo)

**Pregunta**: ¿Por qué preferir `data object` sobre un `object` simple para miembros sin estado de una jerarquía sellada?

**Respuesta Senior**: Un `object` simple genera un `toString()` por defecto que incluye la dirección de memoria (ej. `Loading@3a71f4dd`), lo cual no sirve para logging ni debugging. Un `data object` genera un `toString()` limpio usando solo el nombre de la clase, además de implementaciones consistentes de `equals()` y `hashCode()`. Como los miembros sin estado de jerarquías selladas se loguean, comparan y emiten a través de Flows frecuentemente, el `data object` provee el comportamiento correcto y legible por defecto sin sobrescrituras manuales.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
