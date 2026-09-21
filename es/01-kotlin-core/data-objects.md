---
layout: page
title: "Data Objects: Singleton y Eficiencia de Memoria"
lang: es
permalink: /es/01-kotlin-core/data-objects/
order: 4
---

## The Theory (El Qué)

Un [`data object`]({{ "/es/glosario/data-object/" | relative_url }}) (introducido en Kotlin 1.9) combina la garantía de [singleton]({{ "/es/glosario/singleton/" | relative_url }}) de [`object`]({{ "/es/glosario/object/" | relative_url }}) con los métodos [`toString()`]({{ "/es/glosario/to-string/" | relative_url }}), [`equals()`]({{ "/es/glosario/equals/" | relative_url }}) y [`hashCode()`]({{ "/es/glosario/hash-code/" | relative_url }}) generados por el compilador como en una [`data class`]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}). A diferencia de un [`object`]({{ "/es/glosario/object/" | relative_url }}) simple, que produce un [`toString()`]({{ "/es/glosario/to-string/" | relative_url }}) por defecto como `Loading@3a71f4dd`, un [`data object`]({{ "/es/glosario/data-object/" | relative_url }}) genera una representación limpia y legible usando solo el nombre de la clase — por ejemplo, `Loading`. No se generan funciones [`copy()`]({{ "/es/glosario/copy/" | relative_url }}) ni [`componentN()`]({{ "/es/glosario/component-n/" | relative_url }}), ya que los [singletons]({{ "/es/glosario/singleton/" | relative_url }}) no tienen propiedades de constructor para copiar o [desestructurar]({{ "/es/glosario/destructuring/" | relative_url }}).

## The Senior Perspective (El Porqué)

Para un ingeniero Senior, [`data object`]({{ "/es/glosario/data-object/" | relative_url }}) resuelve un dolor específico en [jerarquías selladas]({{ "/es/glosario/sealed-hierarchy/" | relative_url }}) y modelado de estado.

- **Logging y Debugging Limpio**: En [jerarquías selladas]({{ "/es/glosario/sealed-hierarchy/" | relative_url }}), los miembros sin estado como `Loading` o [`Idle`]({{ "/es/glosario/idle-state/" | relative_url }}) declarados como [`object`]({{ "/es/glosario/object/" | relative_url }}) simple producen un toString inútil (`Loading@3a71f4dd`). Un [`data object`]({{ "/es/glosario/data-object/" | relative_url }}) garantiza una representación legible sin necesidad de sobrescribir manualmente.
- **Garantía de [Singleton]({{ "/es/glosario/singleton/" | relative_url }})**: A diferencia de [`data class`]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}), un [`data object`]({{ "/es/glosario/data-object/" | relative_url }}) es un verdadero [singleton]({{ "/es/glosario/singleton/" | relative_url }}) — existe exactamente una instancia. Esto significa cero [allocations]({{ "/es/glosario/allocations/" | relative_url }}) innecesarias para estados que no llevan datos, lo cual importa en [patrones de emisión de estado]({{ "/es/glosario/state-emission-patterns/" | relative_url }}) de alta frecuencia (ej. actualizaciones de [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }})).
- **Igualdad Consistente**: [`equals()`]({{ "/es/glosario/equals/" | relative_url }}) siempre retorna `true` cuando se compara un [`data object`]({{ "/es/glosario/data-object/" | relative_url }}) consigo mismo (igualdad referencial y estructural son idénticas para [singletons]({{ "/es/glosario/singleton/" | relative_url }})). Esto previene bugs sutiles al mezclar verificaciones [`==`]({{ "/es/glosario/structural-equality/" | relative_url }}) y [`===`]({{ "/es/glosario/referential-equality/" | relative_url }}) en expresiones [`when`]({{ "/es/glosario/when-expression/" | relative_url }}) u operaciones de [colecciones]({{ "/es/glosario/collections/" | relative_url }}).
- **Best Practice en [Sealed Hierarchies]({{ "/es/glosario/sealed-hierarchy/" | relative_url }})**: La convención moderna es usar [`data object`]({{ "/es/glosario/data-object/" | relative_url }}) para miembros sin estado y [`data class`]({{ "/es/01-kotlin-core/data-classes/" | relative_url }}) para miembros con estado dentro de una [jerarquía sellada]({{ "/es/glosario/sealed-hierarchy/" | relative_url }}).

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

## The Interview (En el banquillo)

**Pregunta**: ¿Por qué preferir [`data object`]({{ "/es/glosario/data-object/" | relative_url }}) sobre un [`object`]({{ "/es/glosario/object/" | relative_url }}) simple para miembros sin estado de una jerarquía sellada?

**Respuesta Senior**: Un [`object`]({{ "/es/glosario/object/" | relative_url }}) simple genera un [`toString()`]({{ "/es/glosario/to-string/" | relative_url }}) por defecto que incluye la dirección de memoria (ej. `Loading@3a71f4dd`), lo cual no sirve para logging ni debugging. Un [`data object`]({{ "/es/glosario/data-object/" | relative_url }}) genera un [`toString()`]({{ "/es/glosario/to-string/" | relative_url }}) limpio usando solo el nombre de la clase, además de implementaciones consistentes de [`equals()`]({{ "/es/glosario/equals/" | relative_url }}) y [`hashCode()`]({{ "/es/glosario/hash-code/" | relative_url }}). Como los miembros sin estado de [jerarquías selladas]({{ "/es/glosario/sealed-hierarchy/" | relative_url }}) se loguean, comparan y emiten a través de [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) frecuentemente, el [`data object`]({{ "/es/glosario/data-object/" | relative_url }}) provee el comportamiento correcto y legible por defecto sin sobrescrituras manuales.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
