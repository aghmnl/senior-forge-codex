---
layout: post
title: "Companion Object"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/companion-object/
---

## The Theory (El Qué)

Un **companion object** es el reemplazo de Kotlin para los miembros `static` de Java. Es un objeto [singleton]({{ "/es/glosario/singleton/" | relative_url }}) declarado dentro de una clase usando `companion object { ... }`. Sus miembros pueden accederse vía el nombre de la clase sin crear una instancia — `MyClass.MY_CONSTANT` — convirtiéndolo en el lugar estándar para constantes, métodos factory y funciones utilitarias compartidas.

A diferencia del `static` de Java, un companion object es un objeto real: tiene una clase, puede implementar interfaces y puede pasarse como argumento. A nivel de [JVM]({{ "/es/glosario/jvm/" | relative_url }}), los miembros del companion viven en una clase anidada `Companion`, y acceder a ellos involucra una indirección extra a través de la instancia del companion — a menos que se anote con [`@JvmStatic`]({{ "/es/glosario/jvm-static/" | relative_url }}).

```kotlin
// From FollowApp Suite — RecurrencePattern en RecurrenceRule.kt
sealed class RecurrencePattern {
    data class DayOfMonth(val day: Int) : RecurrencePattern()
    data class NthWeekday(val ordinal: Int, val day: DayOfWeek) : RecurrencePattern()
    data class NthBusinessDay(val ordinal: Int) : RecurrencePattern()

    companion object {
        const val LAST = -1
    }
}
```

```kotlin
// From FollowApp Suite — LegacyTaskReader.kt
class LegacyTaskReader(private val context: Context) {

    companion object {
        const val LEGACY_DB_NAME = "TaskDatabase"
        private const val LEGACY_TABLE = "TasksTable"
        private const val TAG = "LegacyTaskReader"
    }
}
```

```kotlin
// From FollowApp Suite — TasksViewPreferences.kt
companion object {
    const val UNSAVED_PRESET_KEY = "none"

    private val keySortOrder = stringPreferencesKey("tasks_view_sort_order")
    private val keyGroupBy = stringPreferencesKey("tasks_view_group_by")
    private val keyDoneFilter = stringPreferencesKey("tasks_view_done_filter")
}
```

## The Senior Nuance (El Matiz Senior)

- **Las constantes van acá**: `const val` dentro de un companion object compila a un verdadero campo `static final` de JVM — cero overhead, sin instancia del companion involucrada. Las propiedades `val` regulares en el companion aún pasan por el getter del companion object.
- **Patrón Factory**: Los companion objects son el lugar idiomático para métodos factory (`MyClass.from(...)`, `MyClass.create(...)`) porque pueden acceder al [constructor]({{ "/es/glosario/constructor/" | relative_url }}) `private` de la clase. Es más expresivo que constructores sobrecargados.
- **Implementación de interfaces**: Un companion object puede implementar una interfaz (`companion object : Serializer<MyClass>`), lo cual es útil para proveer un serializador por defecto o un factory type-safe que puede referenciarse como `MyClass` mismo.
- **Patrón de keys de DataStore**: En FollowApp Suite, `companion object` es el lugar canónico para declaraciones de `PreferencesKey` de DataStore — manteniéndolas colocadas con la clase que las lee/escribe mientras las hace accesibles sin una instancia.
- **[Static dispatch]({{ "/es/glosario/static-dispatch/" | relative_url }})**: Las funciones de companion object usan [static dispatch]({{ "/es/glosario/static-dispatch/" | relative_url }}) — la llamada se resuelve en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}), sin lookup de [vtable]({{ "/es/glosario/vtable/" | relative_url }}). Agregar [`@JvmStatic`]({{ "/es/glosario/jvm-static/" | relative_url }}) hace que el bytecode de la JVM sea un verdadero método estático, lo cual importa para interop con Java y reflexión de frameworks.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
