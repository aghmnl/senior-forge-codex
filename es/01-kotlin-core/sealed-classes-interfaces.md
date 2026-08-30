---
layout: page
title: "Sealed Classes vs Sealed Interfaces"
lang: es
permalink: /es/01-kotlin-core/sealed-classes-interfaces/
order: 5
---

## The Theory (El Qué)

Tanto `sealed class` como `sealed interface` restringen qué tipos pueden extenderlas — todos los subtipos directos deben declararse en el mismo paquete y módulo. Esto le da al compilador un conjunto cerrado, habilitando [expresiones `when`]({{ "/es/glosario/when-expression/" | relative_url }}) exhaustivas sin una rama `else` por defecto. La diferencia está en lo que comparten:

- **`sealed class`** — elegila cuando los subtipos comparten estado o comportamiento. Podés declarar propiedades en el [constructor]({{ "/es/glosario/constructor/" | relative_url }}), definir métodos comunes y usar un bloque `init`. Los subtipos heredan esa estructura compartida. El tradeoff: una clase solo puede extender **una** sealed class ([herencia]({{ "/es/glosario/inheritance/" | relative_url }}) simple).
- **`sealed interface`** (Kotlin 1.5+) — elegila cuando solo necesitás restringir la jerarquía de tipos pero cada implementación es independiente. No hay estado compartido, no hay [constructor]({{ "/es/glosario/constructor/" | relative_url }}), no hay bloque `init` — no hay [estado protegido]({{ "/es/glosario/protected-state/" | relative_url }}). La ventaja: una clase puede implementar **múltiples** sealed interfaces simultáneamente — algo que las sealed classes no pueden hacer.

La regla general: preferí `sealed interface` por defecto; llegá a `sealed class` solo cuando la jerarquía genuinamente necesita estado compartido o una implementación base común.

## The Senior Perspective (El Porqué)

- **Seguridad en Tiempo de Compilación**: Al evitar el bloque `else` en sentencias [`when`]({{ "/es/glosario/when-expression/" | relative_url }}), el compilador marca cada caso no manejado cuando se agrega un nuevo subtipo. Esto convierte un crash en runtime en un error de [tiempo de compilación]({{ "/es/glosario/compile-time/" | relative_url }}) — el compilador es tu verificador de máquina de estados. Esto es lo que hace de las jerarquías selladas la encarnación Kotlin de los [tipos de datos algebraicos (ADTs)]({{ "/es/glosario/algebraic-data-types/" | relative_url }}).
- **Eficiencia de Memoria**: Usar [`data object`]({{ "/es/01-kotlin-core/data-objects/" | relative_url }}) para miembros sin estado (como `Loading` o `Idle`) evita [allocations]({{ "/es/glosario/allocations/" | relative_url }}) redundantes de objetos, ganando soporte integrado de `equals` y `toString`. Un `data object` es un [singleton]({{ "/es/glosario/singleton/" | relative_url }}) — emitirlo a través de [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) miles de veces crea cero objetos nuevos.
- **Comportamiento Compartido vía sealed class**: Cuando cada subtipo debe llevar las mismas propiedades (ej. `taskId` y `childCount` en una acción en cascada), una sealed class evita repetir esas declaraciones en cada variante. Las propiedades `abstract` viven en la clase base, y cada subtipo las provee a través de su [constructor primario]({{ "/es/glosario/primary-constructor/" | relative_url }}).
- **Pertenencia a Múltiples Jerarquías vía sealed interface**: Una sealed interface permite que una clase pertenezca a múltiples jerarquías restringidas simultáneamente. Esto es imposible con sealed classes debido a la restricción de herencia simple de la JVM, haciendo de las sealed interfaces la mejor opción por defecto para modelado a nivel de arquitectura (estado de UI, eventos de navegación, acciones de dominio).
- **Base Arquitectónica**: Las jerarquías selladas son los bloques fundamentales para [MVI]({{ "/es/glosario/mvi-pattern/" | relative_url }}) y [flujo unidireccional]({{ "/es/glosario/unidirectional-data-flow/" | relative_url }}), asegurando que la UI reaccione a una fuente única de verdad vía [patrones de emisión de estado]({{ "/es/glosario/state-emission-patterns/" | relative_url }}).

## Code in Action

```kotlin
// De FollowApp Suite — CascadeAction en TasksUiState.kt
// sealed CLASS: los subtipos comparten estado común (taskId, childCount)
// que vive en propiedades abstractas — sin repetición necesaria
sealed class CascadeAction {
    abstract val taskId: String
    abstract val childCount: Int

    data class Complete(
        override val taskId: String,
        val isCompleted: Boolean,
        override val childCount: Int
    ) : CascadeAction()

    data class Archive(
        override val taskId: String,
        override val childCount: Int
    ) : CascadeAction()

    data class Delete(
        override val taskId: String,
        override val childCount: Int
    ) : CascadeAction()
}

// De FollowApp Suite — RecurrenceRule.kt
// sealed CLASS: el companion object provee constantes compartidas,
// y cada variante lleva su propia forma de datos
sealed class RecurrencePattern {
    data class DayOfMonth(val day: Int) : RecurrencePattern()
    data class MonthDay(val month: Int, val day: Int) : RecurrencePattern()
    data class NthWeekday(val ordinal: Int, val day: DayOfWeek) : RecurrencePattern()
    data class NthBusinessDay(val ordinal: Int) : RecurrencePattern()

    companion object {
        const val LAST = -1
    }
}

// De FollowApp Suite — StateChip.kt
// sealed INTERFACE: sin estado compartido — cada implementación define
// sus propios colores, bordes y comportamiento de forma independiente.
// Una clase podría implementar ChipState Y otra sealed interface
sealed interface ChipState {
    val foreground: Color @Composable get
    val border: BorderStroke? @Composable get
    val strikethrough: Boolean get() = false
    @Composable fun inputColors(): SelectableChipColors
    @Composable fun filterColors(): SelectableChipColors
}

// De FollowApp Suite — TrashUiState.kt
// sealed CLASS con data objects puros: todas las variantes son
// singletons sin estado — una sealed interface funcionaría igual acá,
// pero el patrón existente usa sealed class
sealed class TrashBulkAction {
    data object Restore : TrashBulkAction()
    data object PermanentDelete : TrashBulkAction()
    data object Archive : TrashBulkAction()
}
```

## The Interview (En el banquillo)

**Pregunta**: ¿Cuándo elegirías una `sealed class` sobre una `sealed interface`, y viceversa?

**Respuesta Senior**: Elijo `sealed class` cuando los subtipos comparten estado o comportamiento común — propiedades en el [constructor]({{ "/es/glosario/constructor/" | relative_url }}), métodos compartidos o un bloque `init`. Por ejemplo, si cada variante de una acción en cascada necesita un `taskId` y `childCount`, una sealed class con propiedades `abstract val` evita repetir esos campos en cada subtipo. Elijo `sealed interface` — que es mi opción por defecto — cuando la jerarquía solo necesita restringir quién puede implementarla, sin compartir estado. La ventaja clave es que una clase puede implementar múltiples sealed interfaces pero solo puede heredar de una sealed class. En la práctica, la mayoría de jerarquías de estado de UI y tipos de acciones de dominio funcionan mejor como sealed interfaces porque cada variante es estructuralmente independiente, y la flexibilidad de implementar múltiples interfaces importa para cross-cutting concerns como contratos de logging o analytics.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
