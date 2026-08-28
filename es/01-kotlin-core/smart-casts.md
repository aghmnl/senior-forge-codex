---
layout: page
title: Smart Casts
lang: es
permalink: /es/01-kotlin-core/smart-casts/
order: 2
---

## The Theory (El Qué)

El Smart Casting es la capacidad del compilador de Kotlin de convertir automáticamente una variable a un tipo más específico después de una verificación de tipo (`is`), una verificación de nulabilidad (`!= null`) u otras condiciones de flujo de control que garanticen el tipo. A diferencia de Java, donde se requieren casts explícitos después de `instanceof`, Kotlin rastrea la información de tipo a través del grafo de flujo de control y hace disponible el tipo refinado sin necesidad de cast manual.

## The Senior Perspective (El Porqué)

Un ingeniero Senior aprovecha los smart casts no solo para escribir código más limpio, sino que entiende los límites donde aplican y donde no.

- **Navegación de Jerarquías Selladas**: Los smart casts brillan en expresiones `when` sobre [sealed classes]({{ "/es/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}). Después de hacer match con `is UIState.Success`, el compilador sabe que la variable es `Success` y otorga acceso directo a sus propiedades — sin cast explícito. Esto es la base del manejo de estado type-safe en MVI.
- **Limitación de Mutabilidad**: Los smart casts solo funcionan con variables locales y propiedades `val` (inmutables). Un `var` o una propiedad con getter personalizado puede cambiar entre la verificación y el uso, por lo que el compilador rechaza el smart cast. Esta es una garantía de seguridad deliberada, no una limitación.
- **Contract Functions**: El mecanismo de `contract` de Kotlin (usado por `require`, `check`, `checkNotNull`) informa al compilador sobre garantías de tipo, habilitando smart casts después de llamadas de validación. El `requireNotNull(value)` de la stdlib hace que `value` se convierta automáticamente a no-nulo en el código subsiguiente.
- **Cast Explícito como Fallback**: Cuando el smart cast no está disponible (propiedades mutables, límites entre módulos), se usa el safe cast `as?` que retorna null en caso de fallo, nunca lanza excepción. Reservar el unsafe `as` para situaciones donde el fallo es genuinamente imposible.

## Code in Action

```kotlin
// De FollowApp Suite — FilterState.kt
// La jerarquía sellada que habilita los smart casts de abajo
sealed class ScaleFilterState {
    object Off : ScaleFilterState()
    data class Include(val values: Set<String>) : ScaleFilterState()
    object Exclude : ScaleFilterState()
}

// De FollowApp Suite — PresetMapper.kt
// when + is: el compilador hace smart cast de `state` a Include,
// dando acceso directo a `state.values`
fun serializeScaleFilters(filters: Map<String, ScaleFilterState>): String {
    val json = JSONObject()
    filters.forEach { (key, state) ->
        when (state) {
            is ScaleFilterState.Off -> json.put(key, JSONObject().put("type", "OFF"))
            is ScaleFilterState.Include -> {
                val arr = JSONArray(state.values.toList())  // smart cast
                json.put(key, JSONObject().put("type", "INCLUDE").put("values", arr))
            }
            is ScaleFilterState.Exclude -> json.put(key, JSONObject().put("type", "EXCLUDE"))
        }
    }
    return json.toString()
}

// De FollowApp Suite — CleanUpPresetsUseCase.kt
// is dentro de if: después del check, filter.values es accesible
if (filter is ScaleFilterState.Include && oldValue in filter.values) {
    val updatedValues = filter.values - oldValue + newValue
}

// De FollowApp Suite — TasksViewModel.kt
// as? safe cast: retorna null si el LabelValue es Scale (no Tag)
val taskLabels = (task.customLabels["labels"] as? LabelValue.Tag)
    ?.values?.toSet() ?: emptySet()

// De FollowApp Suite — RecurrenceCalculator.kt
// as? + null-check smart cast: until se convierte en Long (no-nulo) después del check
val until = (rule.end as? RecurrenceEnd.UntilDate)?.date
return if (until != null && candidate > until) null else candidate
```

## The Interview (En el banquillo)

**Pregunta**: ¿Por qué el compilador de Kotlin rechaza hacer smart cast en una propiedad `var` después de una verificación `is`?

**Respuesta Senior**: Entre la verificación `is` y el uso subsiguiente, otro hilo — o incluso el mismo hilo a través de un callback — podría reasignar el `var` a un tipo diferente. El compilador no puede garantizar que el tipo verificado siga siendo válido en el punto de uso, por lo que rechaza el smart cast para prevenir un `ClassCastException` en tiempo de ejecución. Es el mismo principio detrás del diseño de null safety de Kotlin: el sistema de tipos solo hace promesas que puede cumplir. La solución es capturar el valor en un `val` local primero, y entonces el smart cast aplica sobre la variable local inmutable.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
