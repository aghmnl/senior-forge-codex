---
layout: post
title: "Constructor"
date: 2026-08-30 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/constructor/
---

## The Theory (El Qué)

Un **constructor** es una función especial que inicializa una nueva instancia de una clase. Kotlin distingue entre el **constructor primario** (declarado en el encabezado de la clase) y los **constructores secundarios** (declarados dentro del cuerpo de la clase con `constructor`). El [constructor primario]({{ "/es/glosario/primary-constructor/" | relative_url }}) es el enfoque idiomático de Kotlin: sus parámetros pueden ser propiedades `val`/`var` directamente, y el bloque `init` se ejecuta como parte de su ejecución.

```kotlin
// De FollowApp Suite — RecurrenceRule.kt
// Constructor primario con valores por defecto — la forma idiomática de Kotlin
data class RecurrenceRule(
    val frequency: RecurrenceFrequency,
    val interval: Int = 1,
    val weekdays: Set<DayOfWeek> = emptySet(),
    val end: RecurrenceEnd = RecurrenceEnd.Never,
    val pattern: RecurrencePattern? = null
)

// De FollowApp Suite — MyTasksDatabase.kt
// Clase abstracta sin constructor explícito — Room genera la implementación
abstract class MyTasksDatabase : RoomDatabase() {
    abstract fun taskDao(): TaskDao
    abstract fun labelDao(): LabelDao
    abstract fun presetDao(): PresetDao
}
```

## The Senior Nuance (El Matiz Senior)

- En Kotlin, el constructor primario es la forma por defecto y preferida de inicializar clases. Los constructores secundarios existen principalmente para interop con Java y requerimientos de frameworks (ej. subclases de `View` en Android que necesitan múltiples constructores para inflación desde XML).
- Los constructores son la línea divisoria entre `sealed class` y `sealed interface`: una sealed class puede definir un constructor (primario o secundario) con parámetros compartidos y un bloque `init`, forzando a los subtipos a proveer esos valores. Una sealed interface no tiene constructor — cada implementación es estructuralmente independiente. Ver [Sealed Classes vs Sealed Interfaces]({{ "/es/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}).
- Los constructores de `data class` reciben tratamiento especial: el compilador genera `copy()`, `equals()`, `hashCode()`, `toString()` y `componentN()` a partir de los parámetros del constructor primario. Por eso `data class` + constructor primario es el patrón estándar para objetos de estado inmutables en [MVI]({{ "/es/glosario/mvi-pattern/" | relative_url }}).
- Las [clases abstractas]({{ "/es/glosario/abstract-class/" | relative_url }}) pueden declarar parámetros `abstract` en el constructor que los subtipos deben proveer. Así es como las sealed classes fuerzan estado compartido entre variantes — el constructor de cada subtipo suministra los valores requeridos.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
