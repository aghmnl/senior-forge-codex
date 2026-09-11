---
layout: post
title: "Return Type"
date: 2026-09-07 12:00:00 +0000
categories: [es, glosario]
tags: [type-system, generics, syntax]
lang: es
permalink: /es/glosario/return-type/
---

## The Theory (El Qué)

El **return type** (tipo de retorno) es el tipo del valor que una función devuelve a su caller. En Kotlin se escribe después de la lista de parámetros (`fun size(): Int`), o se infiere cuando la función usa sintaxis de expresión (`fun size() = items.count()`). Una función que no devuelve nada significativo tiene return type `Unit`, que es un tipo real con una única instancia — no el `void` de Java.

```kotlin
// From FollowApp Suite — BackupSerializer.kt
// Return type List<T>: T aparece en una posición "out".
private fun <T> JSONArray.mapObjects(transform: (JSONObject) -> T): List<T> =
    (0 until length()).map { transform(getJSONObject(it)) }
```

En las reglas de [Varianza]({{ "/es/glosario/variance/" | relative_url }}), el return type es la **posición out** canónica: es donde un tipo se *produce* y se entrega hacia afuera.

## The Senior Nuance (El Matiz Senior)

- **Return type = posición out.** Un [Generic Type Parameter]({{ "/es/glosario/generic-type-parameters/" | relative_url }}) puede declararse [Covariante]({{ "/es/glosario/covariance/" | relative_url }}) (`out T`) solo si aparece exclusivamente en return types. En el momento en que también aparece como parámetro, la clase debe quedar [Invariante]({{ "/es/glosario/invariance/" | relative_url }}). Esta regla posicional es todo PECS, enunciado con precisión.
- **Los return types son covariantes al sobreescribir.** Un override puede angostar el return type — si la base declara `fun load(): Task`, un override puede devolver `CompletedTask`. Lo que *no* puede es angostar un tipo de parámetro, por la razón espejo: los parámetros son posiciones in.
- **Return types explícitos en API pública.** Los cuerpos de expresión infieren el return type, lo cual es cómodo puertas adentro pero frágil cruzando límites de módulo: cambiar un detalle de implementación puede cambiar silenciosamente una firma publicada y romper la compatibilidad binaria. Un Senior escribe el return type explícito en todo lo público.
- **`Nothing` es el bottom type.** Una función que siempre lanza tiene return type `Nothing`, que es subtipo de todos los tipos. Eso es lo que permite que `val x: String = value ?: throw IllegalStateException()` tipe correctamente — la rama del `throw` conforma con `String` porque `Nothing` conforma con todo.
- **El return type impulsa el [Type Inference]({{ "/es/glosario/type-inference/" | relative_url }}).** En `mapObjects(::taskFromJson)`, `T` se infiere del tipo de *retorno* de la referencia a función, no de ningún argumento. La inferencia genérica fluye hacia atrás por los return types tan fácilmente como hacia adelante por los parámetros.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
