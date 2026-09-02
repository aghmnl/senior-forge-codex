---
layout: post
title: "Callbacks"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/callbacks/
---

## The Theory (El Qué)

Un **callback** es una función (o [lambda]({{ "/es/glosario/lambdas/" | relative_url }})) pasada como argumento a otra función, para ser invocada cuando ocurre un evento específico o una operación se completa. En Kotlin, los callbacks se expresan como function types — `() -> Unit`, `(String) -> Unit`, `(Result<T>) -> Unit` — convirtiéndolos en valores de primer nivel que se benefician de patrones de [funciones de orden superior]({{ "/es/01-kotlin-core/higher-order-functions-lambdas/" | relative_url }}), optimización [inline]({{ "/es/glosario/inline-functions/" | relative_url }}), y [type safety]({{ "/es/glosario/type-safety/" | relative_url }}).

```kotlin
// From FollowApp Suite — TasksCallbacks.kt
class TaskFormCallbacks(
    val onFormTitleChange: (String) -> Unit,
    val onFormDescriptionChange: (String) -> Unit,
    val onFormCompletedChange: (Boolean) -> Unit,
    val onFormDueDateChange: (Long?) -> Unit,
    val onFormConfirmed: () -> Unit,
    val onFormDismissed: () -> Unit,
    val onFormRecurrenceChange: (RecurrenceRule?) -> Unit,
    val onAddSubtask: (String) -> Unit,
)
```

## The Senior Nuance (El Matiz Senior)

- **Consolidación de callbacks**: En [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}), las pantallas complejas pueden acumular docenas de lambdas de callback (`onClick`, `onValueChange`, `onDismiss`). Agruparlos en una clase dedicada (como `TaskFormCallbacks` arriba) previene que las listas de parámetros Composable exploten, manteniendo cada callback fuertemente tipado.
- **Callbacks vs [Coroutines]({{ "/es/glosario/coroutines/" | relative_url }})**: En Android moderno, las [funciones suspend]({{ "/es/glosario/suspend-functions/" | relative_url }}) y [Flow]({{ "/es/glosario/stateflow/" | relative_url }}) han reemplazado en gran parte a los callbacks para [operaciones async]({{ "/es/glosario/async-operations/" | relative_url }}). Los callbacks sobreviven en [event handlers]({{ "/es/glosario/event-handlers/" | relative_url }}) de UI (Compose `onClick`, View `OnClickListener`) y APIs de framework que son anteriores a las [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}). Los desarrolladores senior prefieren [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) para trabajo async y callbacks solo para [wiring de eventos]({{ "/es/glosario/event-wiring/" | relative_url }}).
- Cada lambda de callback no-inline [asigna]({{ "/es/glosario/allocations/" | relative_url }}) un objeto `Function` en el [heap]({{ "/es/glosario/heap/" | relative_url }}). En Compose, las lambdas pasadas a composables se capturan y comparan por igualdad durante la recomposición — capturas inestables (referenciando estado mutable) causan recomposición innecesaria. Usá `remember { Callbacks(...) }` o referencias estables para evitar esto.
- **[Memory leaks]({{ "/es/glosario/memory-leaks/" | relative_url }})**: Un callback registrado en un objeto de larga vida (un [singleton]({{ "/es/glosario/singleton/" | relative_url }}), un [broadcast receiver]({{ "/es/glosario/broadcast-receiver/" | relative_url }})) que captura una referencia a Activity o Fragment es un leak clásico. Siempre desregistrá en `onDestroy()`/`onDestroyView()`, o usá registro [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}).
- El problema de "callback hell" (callbacks profundamente anidados) se resuelve en Kotlin con [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) (`suspendCancellableCoroutine` wrappea una API de callback en una [función suspend]({{ "/es/glosario/suspend-functions/" | relative_url }})), pero entender callbacks sigue siendo esencial — son la fundación sobre la que están construidas las [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
