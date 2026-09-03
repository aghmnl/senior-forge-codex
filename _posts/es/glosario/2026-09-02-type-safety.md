---
layout: post
title: "Type Safety"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/type-safety/
---

## The Theory (El Qué)

**Type safety** (seguridad de tipos) es el grado en que un lenguaje previene operaciones sobre valores de tipos incompatibles. En Kotlin, el sistema de tipos la hace cumplir en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}): no podés pasar un `String` donde se espera un `Int`, asignar `null` a una referencia no-nullable, ni llamar a un método que no existe en el tipo declarado — el compilador rechaza el código antes de ejecutarlo. Esto elimina categorías enteras de errores en [runtime]({{ "/es/glosario/runtime/" | relative_url }}) (como [NullPointerException]({{ "/es/glosario/null-pointer-exception/" | relative_url }}) y [ClassCastException]({{ "/es/glosario/class-cast-exception/" | relative_url }})) que son comunes en lenguajes débilmente tipados o de tipado dinámico.

```kotlin
// From FollowApp Suite — LabelRepository.kt
interface LabelRepository {
    suspend fun getOrCreateLabel(name: String, type: LabelType): Label
    suspend fun upsertLabelOption(
        labelId: String,
        label: String,
        sortOrder: Int = 0
    ): LabelOption
    suspend fun deleteLabelOption(labelOptionId: String)
}
```

Cada parámetro, tipo de retorno y restricción de nullabilidad es enforceado por el compilador — los callers no pueden pasar accidentalmente un id de `LabelOption` donde se espera un id de `Label` si el diseño usa tipos distintos.

## The Senior Nuance (El Matiz Senior)

- **La null safety de Kotlin** es la característica más visible de type safety: `String` vs `String?` son tipos distintos. El operador [safe call]({{ "/es/glosario/safe-call/" | relative_url }}) (`?.`), Elvis (`?:`) y smart [cast]({{ "/es/glosario/cast/" | relative_url }}) eliminan la necesidad de checks defensivos de null dispersos por el código.
- **Los [generics]({{ "/es/glosario/generic-type-parameters/" | relative_url }})** extienden type safety a containers y abstracciones. `Flow<Label>` garantiza que los valores emitidos son instancias de `Label` — sin casting en el sitio de recolección. Los type parameters [reified]({{ "/es/glosario/reified/" | relative_url }}) preservan esta garantía incluso en [runtime]({{ "/es/glosario/runtime/" | relative_url }}), saltando [type erasure]({{ "/es/glosario/type-erasure/" | relative_url }}).
- **Las [sealed hierarchies]({{ "/es/glosario/sealed-hierarchy/" | relative_url }})** proveen chequeo de [exhaustiveness]({{ "/es/glosario/exhaustiveness/" | relative_url }}): una expresión `when` sobre una sealed class fuerza al desarrollador a manejar cada subtipo, haciendo imposible olvidarse un caso — una alternativa type-safe a constantes string/int.
- **Los [callbacks]({{ "/es/glosario/callbacks/" | relative_url }})** en Kotlin son type-safe porque se expresan como function types (`(String) -> Unit`) en lugar de referencias `Object` crudas. El compilador verifica que la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) que pasás coincide con la firma esperada.
- Los ingenieros senior aprovechan type safety para **hacer irrepresentables los estados ilegales**: value classes, sealed types y parámetros no-nullable codifican reglas de negocio en el sistema de tipos para que el compilador las haga cumplir, reduciendo la dependencia de validación en runtime.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
