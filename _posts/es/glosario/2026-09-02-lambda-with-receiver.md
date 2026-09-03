---
layout: post
title: "Lambda with Receiver"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/lambda-with-receiver/
---

## The Theory (El Qué)

Una **lambda with receiver** (lambda con receptor) es una [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) cuyo cuerpo se ejecuta en el [scope]({{ "/es/glosario/scope/" | relative_url }}) de un [receiver type]({{ "/es/glosario/receiver-type/" | relative_url }}). Su firma es `T.() -> R` — dentro de la lambda, `this` se refiere a la instancia receptora de tipo `T`, así que podés llamar a sus miembros sin cualificación. Este es el mecanismo central detrás de los [DSLs]({{ "/es/glosario/dsl/" | relative_url }}) de Kotlin, las [scope functions]({{ "/es/01-kotlin-core/scope-functions/" | relative_url }}) (`apply`, `run`, `with`) y las builder APIs.

```kotlin
// From FollowApp Suite — BackupSerializer.kt
// apply {} es una lambda con receptor: 'this' es el JSONObject
private fun taskToJson(task: TaskEntity): JSONObject = JSONObject().apply {
    put("id", task.id)
    put("title", task.title)
    put("description", task.description)
    put("parentTaskId", task.parentTaskId)
    put("status", task.status)
    put("isCompleted", task.isCompleted)
}
```

```kotlin
// From FollowApp Suite — TasksNavDrawer.kt
// ColumnScope.() -> Unit — lambda con receptor con scope de Compose
@Composable
private fun DropUpMenu(
    expanded: Boolean,
    onDismissRequest: () -> Unit,
    content: @Composable ColumnScope.() -> Unit  // lambda con receptor
) {
    // dentro de 'content', 'this' es ColumnScope — weight(), align() están disponibles
}
```

La diferencia entre una lambda regular (`(T) -> R`) y una lambda con receptor (`T.() -> R`) es sintáctica, no semántica: ambas reciben un argumento de tipo `T`, pero la versión con receptor lo expone como `this` en lugar de como un parámetro con nombre. El compilador desazucara `T.() -> R` a `Function1<T, R>` en el [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}).

## The Senior Nuance (El Matiz Senior)

- Las [scope functions]({{ "/es/01-kotlin-core/scope-functions/" | relative_url }}) se dividen en dos familias basándose en esto: `apply`/`run`/`with` usan lambda con receptor (`this`), mientras que `let`/`also` usan lambda regular (`it`). Elegir entre ellas señala intención — [intent signaling]({{ "/es/glosario/intent-signaling/" | relative_url }}).
- Cuando se anidan lambdas con receptor (ej. `Column { Row { ... } }` en [Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }})), el receptor más interno oculta los externos. Usá [`this@label`]({{ "/es/glosario/this-at-label/" | relative_url }}) para acceder a un receptor externo explícitamente: `this@Column.align(...)`.
- [`@DslMarker`]({{ "/es/glosario/dsl-marker/" | relative_url }}) y [`@LayoutScopeMarker`]({{ "/es/glosario/layout-scope-marker/" | relative_url }}) previenen la fuga accidental de scope en lambdas con receptor anidadas. Sin ellos, las lambdas internas pueden silenciosamente llamar métodos de receptores externos — una fuente sutil de bugs.
- Las lambdas con receptor son la base de los type-safe builders: `buildList {}` (receptor: `MutableList<T>`), `buildString {}` (receptor: `StringBuilder`), `buildMap {}` (receptor: `MutableMap<K, V>`). El receptor restringe qué operaciones son válidas, así que el compilador atrapa el mal uso en lugar del desarrollador.
- Las [higher-order functions]({{ "/es/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}) que aceptan lambdas con receptor típicamente se marcan como [`inline`]({{ "/es/glosario/inline-functions/" | relative_url }}), eliminando completamente el overhead de [allocation]({{ "/es/glosario/allocations/" | relative_url }}) del objeto lambda.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
