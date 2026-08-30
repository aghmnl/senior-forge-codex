---
layout: post
title: "Abstract Class"
date: 2026-08-30 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/abstract-class/
---

## The Theory (El Qué)

Una **abstract class** (clase abstracta) es una clase que no puede instanciarse directamente — existe para ser subclaseada. Puede declarar miembros `abstract` (propiedades y funciones sin cuerpo) que cada subtipo debe implementar, y puede proveer miembros concretos (implementaciones por defecto, estado compartido, bloques `init`) que los subtipos heredan. En Kotlin, `sealed class` es una clase abstracta especializada que además restringe qué clases pueden extenderla a aquellas en el mismo paquete y módulo.

```kotlin
// De FollowApp Suite — TasksUiState.kt
// CascadeAction es una sealed (abstract) class:
// las propiedades abstract fuerzan estado compartido en todas las variantes
sealed class CascadeAction {
    abstract val taskId: String
    abstract val childCount: Int

    data class Complete(
        override val taskId: String,
        val isCompleted: Boolean,
        override val childCount: Int
    ) : CascadeAction()

    data class Delete(
        override val taskId: String,
        override val childCount: Int
    ) : CascadeAction()
}

// De FollowApp Suite — MyTasksDatabase.kt
// Room requiere una clase abstracta — genera la implementación en tiempo de compilación
abstract class MyTasksDatabase : RoomDatabase() {
    abstract fun taskDao(): TaskDao
    abstract fun labelDao(): LabelDao
    abstract fun presetDao(): PresetDao
}
```

## The Senior Nuance (El Matiz Senior)

- Clase abstracta vs interfaz: una clase abstracta puede contener estado (propiedades con backing fields), [constructores]({{ "/es/glosario/constructor/" | relative_url }}) y bloques `init`. Una interfaz no puede contener estado — solo funciones abstractas o con implementación por defecto y propiedades abstractas (sin backing fields). Usá una clase abstracta cuando los subtipos necesitan estado interno compartido; usá una interfaz cuando solo necesitás un contrato.
- Clase abstracta vs sealed class: ambas son abstractas, pero una sealed class restringe la subtipificación a un conjunto cerrado (mismo paquete y módulo), habilitando `when` exhaustivo. Una clase abstracta regular permite que cualquiera, desde cualquier lugar, la extienda. Para [tipos de datos algebraicos (ADTs)]({{ "/es/glosario/algebraic-data-types/" | relative_url }}), siempre preferí jerarquías selladas — te dan la exhaustividad forzada por el compilador que una clase abstracta regular no puede.
- En Android, las clases abstractas son comunes en APIs del framework: `RoomDatabase`, `ViewModel`, `BroadcastReceiver`, `View`. No son decisiones de diseño que tomás vos — son requerimientos del framework. En tu código de dominio, preferí composición sobre [herencia]({{ "/es/glosario/inheritance/" | relative_url }}): inyectá dependencias en vez de heredar comportamiento compartido de una clase base.
- Una clase puede extender solo **una** clase abstracta pero implementar **múltiples** interfaces. Esta restricción de [herencia]({{ "/es/glosario/inheritance/" | relative_url }}) simple es por la cual `sealed interface` se prefiere sobre `sealed class` cuando no se necesita estado compartido.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
