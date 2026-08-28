---
layout: page
title: "Data Classes: copy, equals, toString"
lang: es
permalink: /es/01-kotlin-core/data-classes/
order: 3
---

## The Theory (El Qué)

Una `data class` en Kotlin es una clase cuyo propósito principal es almacenar datos. El compilador genera automáticamente las funciones `equals()`, `hashCode()`, `toString()`, `copy()` y `componentN()` a partir de las propiedades declaradas en el constructor primario. Esto elimina el *boilerplate* que los desarrolladores Java tradicionalmente escriben (o generan con herramientas del IDE) para objetos que contienen valores.

## The Senior Perspective (El Porqué)

Un ingeniero Senior no ve las `data class` solo como azúcar sintáctico, sino como un contrato y una decisión de diseño con implicaciones reales.

- **Igualdad Estructural por Defecto**: `equals()` y `hashCode()` se generan únicamente a partir de las propiedades del constructor primario. Las propiedades declaradas en el cuerpo de la clase se excluyen — un detalle sutil pero crítico cuando se usan data classes como claves en mapas o elementos en sets.
- **Modelado Inmutable con `copy()`**: La función `copy()` permite crear copias modificadas sin mutar el original, lo cual es fundamental para arquitecturas de flujo unidireccional (MVI, Redux). Combinada con propiedades `val`, hace que las transiciones de estado sean explícitas y seguras.
- **Destructuring para Legibilidad**: Las funciones `componentN()` generadas habilitan declaraciones de destructuring (`val (name, age) = user`), que mejoran la legibilidad en lambdas, asignaciones en bucles y patrones de retorno múltiple.
- **Trampa — Herencia**: Las data classes no pueden ser `open` (desde Kotlin 1.1+), lo que significa que no pueden servir como clases base. Esto es intencional: los métodos generados por el compilador dependen del constructor primario, y la herencia rompería el contrato.

## Code in Action

```kotlin
// De FollowApp Suite — RecurrenceRule.kt
// Una data class no trivial con defaults, una condición de fin sellada,
// y un patrón opcional — todo en el constructor primario
data class RecurrenceRule(
    val frequency: RecurrenceFrequency,
    val interval: Int = 1,
    val weekdays: Set<DayOfWeek> = emptySet(),
    val end: RecurrenceEnd = RecurrenceEnd.Never,
    val pattern: RecurrencePattern? = null
)

// De FollowApp Suite — CleanUpPresetsUseCase.kt
// copy() para updates inmutables: solo cambian los campos afectados
fun onLabelRenamed(preset: Preset, oldName: String, newName: String) {
    val newLabelFilters = if (oldName in preset.labelFilters) {
        preset.labelFilters - oldName + (newName to preset.labelFilters.getValue(oldName))
    } else preset.labelFilters

    presetRepository.save(
        preset.copy(
            labelFilters = newLabelFilters,
            scaleFilters = newScaleFilters,
            groupBy = newGroupBy
        )
    )
}

// De FollowApp Suite — MyTasksApplication.kt
// Destructuring de un Triple (que es una data class) para extraer tres configuraciones
val (language, themeMode, contrastLevel) = runBlocking {
    Triple(
        languagePreferences.getLanguage().first(),
        themePreferences.getThemeMode().first(),
        themePreferences.getContrastLevel().first()
    )
}
```

## Preparación para Entrevistas (En el banquillo)

**Pregunta**: Un desarrollador agrega una propiedad `timestamp` en el cuerpo de una `data class` y nota que dos objetos con timestamps diferentes se consideran iguales. ¿Por qué?

**Respuesta Senior**: Las propiedades declaradas en el cuerpo de la clase — fuera del constructor primario — no se incluyen en las funciones `equals()`, `hashCode()`, `toString()` ni `copy()` generadas por el compilador. Solo los parámetros del constructor primario participan en estos métodos generados. Si `timestamp` necesita afectar la igualdad, debe moverse al constructor primario. Esta es una decisión de diseño deliberada: Kotlin asume que el constructor primario define la "identidad" de una instancia de data class.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
