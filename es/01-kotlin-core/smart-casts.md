---
layout: page
title: Smart Casts
lang: es
permalink: /es/01-kotlin-core/smart-casts/
order: 2
---

## The Theory (El Qué)

El Smart Casting es la capacidad del compilador de Kotlin de convertir automáticamente una variable a un tipo más específico después de una verificación de tipo ([`is`]({{ "/es/glosario/is-operator/" | relative_url }})), una verificación de nulabilidad (`!= null`) u otras condiciones de flujo de control que garanticen el tipo. A diferencia de Java, donde se requieren [casts]({{ "/es/glosario/cast/" | relative_url }}) explícitos después de `instanceof`, Kotlin rastrea la información de tipo a través del grafo de flujo de control y hace disponible el tipo refinado sin necesidad de [cast]({{ "/es/glosario/cast/" | relative_url }}) manual.

## The Senior Perspective (El Porqué)

Un ingeniero Senior aprovecha los smart casts no solo para escribir código más limpio, sino que entiende los límites donde aplican y donde no.

- **Navegación de [Jerarquías Selladas]({{ "/es/glosario/sealed-hierarchy/" | relative_url }})**: Los smart casts brillan en [expresiones `when`]({{ "/es/glosario/when-expression/" | relative_url }}) sobre [sealed classes]({{ "/es/01-kotlin-core/sealed-classes-interfaces/" | relative_url }}). Después de hacer match con [`is UIState.Success`]({{ "/es/glosario/is-operator/" | relative_url }}), el compilador sabe que la variable es [`Success`]({{ "/es/glosario/success-state/" | relative_url }}) y otorga acceso directo a sus propiedades — sin [cast]({{ "/es/glosario/cast/" | relative_url }}) explícito. Esto es la base del manejo de estado [type-safe]({{ "/es/glosario/type-safety/" | relative_url }}) en [MVI]({{ "/es/glosario/mvi-pattern/" | relative_url }}).
- **Limitación de Mutabilidad**: Los smart casts solo funcionan con variables locales y propiedades [`val`]({{ "/es/glosario/val/" | relative_url }}) (inmutables). Un [`var`]({{ "/es/glosario/var/" | relative_url }}) o una propiedad con [getter]({{ "/es/glosario/getter/" | relative_url }}) personalizado puede cambiar entre la verificación y el uso, por lo que el compilador rechaza el smart cast. Esta es una garantía de seguridad deliberada, no una limitación.
- **Contract Functions**: El mecanismo de [`contract`]({{ "/es/glosario/contract/" | relative_url }}) de Kotlin (usado por [`require`]({{ "/es/glosario/require/" | relative_url }}), [`check`]({{ "/es/glosario/check/" | relative_url }}), [`checkNotNull`]({{ "/es/glosario/check-not-null/" | relative_url }})) informa al compilador sobre garantías de tipo, habilitando smart casts después de llamadas de validación. El [`requireNotNull(value)`]({{ "/es/glosario/require-not-null/" | relative_url }}) de la stdlib hace que `value` se convierta automáticamente a no-nulo en el código subsiguiente.
- **Cast Explícito como Fallback**: Cuando el smart cast no está disponible (propiedades mutables, límites entre módulos), se usa el safe [cast]({{ "/es/glosario/cast/" | relative_url }}) [`as?`]({{ "/es/glosario/as-safe-cast/" | relative_url }}) que retorna null en caso de fallo, nunca lanza excepción. Reservar el unsafe [cast]({{ "/es/glosario/cast/" | relative_url }}) [`as`]({{ "/es/glosario/as-cast/" | relative_url }}) para situaciones donde el fallo es genuinamente imposible.

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

**Pregunta**: ¿Por qué el compilador de Kotlin rechaza hacer smart cast en una propiedad [`var`]({{ "/es/glosario/var/" | relative_url }}) después de una verificación [`is`]({{ "/es/glosario/is-operator/" | relative_url }})?

**Respuesta Senior**: Entre la verificación [`is`]({{ "/es/glosario/is-operator/" | relative_url }}) y el uso subsiguiente, otro [hilo]({{ "/es/glosario/thread/" | relative_url }}) — o incluso el mismo [hilo]({{ "/es/glosario/thread/" | relative_url }}) a través de un [callback]({{ "/es/glosario/callbacks/" | relative_url }}) — podría reasignar el [`var`]({{ "/es/glosario/var/" | relative_url }}) a un tipo diferente. El compilador no puede garantizar que el tipo verificado siga siendo válido en el punto de uso, por lo que rechaza el smart cast para prevenir un [`ClassCastException`]({{ "/es/glosario/class-cast-exception/" | relative_url }}) en [tiempo de ejecución]({{ "/es/glosario/runtime/" | relative_url }}). Es el mismo principio detrás del diseño de [null safety]({{ "/es/01-kotlin-core/null-safety-elvis-safe-calls/" | relative_url }}) de Kotlin: el sistema de tipos solo hace promesas que puede cumplir. La solución es capturar el valor en un [`val`]({{ "/es/glosario/val/" | relative_url }}) local primero, y entonces el smart cast aplica sobre la variable local inmutable.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
