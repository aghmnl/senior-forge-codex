---
layout: page
title: Higher-Order Functions y Lambdas
lang: es
permalink: /es/01-kotlin-core/higher-order-functions-lambdas/
order: 7
---

## The Theory (El Qué)

Las funciones de orden superior (HOFs) son funciones que reciben otras funciones como parámetros o las devuelven como resultado. En Kotlin, las funciones son ciudadanos de primer nivel — pueden almacenarse en variables, pasarse a otras funciones o devolverse. Las [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) son literales de función: bloques de código que no se declaran como funciones tradicionales, sino que se pasan inmediatamente como expresiones.

Un function type como `(Task) -> Boolean` describe una [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) que recibe un `Task` y devuelve un `Boolean`. Cuando una función acepta ese tipo como parámetro, se convierte en una función de orden superior. Este mecanismo es la base de la API de [Collections]({{ "/es/glosario/collections/" | relative_url }}) de Kotlin (`map`, `filter`, `count`), las [Scope Functions]({{ "/es/01-kotlin-core/scope-functions/" | relative_url }}) (`let`, `run`, `apply`, `also`, `with`), y la sintaxis declarativa de [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}).

Los function types también pueden tener un receiver — `T.() -> R` — lo que significa que la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) se ejecuta con `this` vinculado al objeto receptor. Este patrón, combinado con HOFs, es la columna vertebral de los [DSLs]({{ "/es/glosario/dsl/" | relative_url }}) de Kotlin.

## The Senior Perspective (El Porqué)

Un Ingeniero Senior evalúa las funciones de orden superior bajo la lente de la **abstracción frente al rendimiento en [Runtime]({{ "/es/glosario/runtime/" | relative_url }})**.

- **Sobrecarga de Memoria**: Cada vez que se pasa una [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) sin ser [inlineada]({{ "/es/glosario/inline-functions/" | relative_url }}), el compilador crea una nueva instancia de una clase `Function` (ej. `Function0`, `Function1`). En operaciones de alta frecuencia — dentro de builders de `LazyColumn` o bucles sobre [Collections]({{ "/es/glosario/collections/" | relative_url }}) grandes — esto aumenta la presión sobre el [Garbage Collector]({{ "/es/glosario/garbage-collector/" | relative_url }}).
- **El poder de [`inline`]({{ "/es/glosario/inline-functions/" | relative_url }})**: Usar la palabra clave `inline` ordena al compilador reemplazar la llamada a la función con el [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) real de la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}). Esto elimina las [allocations]({{ "/es/glosario/allocations/" | relative_url }}) de objetos y permite non-local returns (usar `return` dentro de una lambda para salir de la función que la invoca). Consulta la entrada de glosario de [Inline Functions]({{ "/es/glosario/inline-functions/" | relative_url }}) para la mecánica completa.
- **Control sobre el Inlining**: [`crossinline`]({{ "/es/glosario/crossinline/" | relative_url }}) previene non-local returns cuando la [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) escapa a otro contexto de ejecución (un objeto local o un hilo diferente). [`noinline`]({{ "/es/glosario/noinline/" | relative_url }}) mantiene una lambda específica como objeto cuando necesitas almacenarla o pasarla a otro lugar.
- **Consolidación de [Callbacks]({{ "/es/glosario/callbacks/" | relative_url }})**: En pantallas grandes, agrupar [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) de [callback]({{ "/es/glosario/callbacks/" | relative_url }}) relacionadas en una clase dedicada previene la explosión de listas de parámetros en funciones Composable — cada [callback]({{ "/es/glosario/callbacks/" | relative_url }}) sigue siendo un function type de primer nivel, pero la firma de la pantalla permanece limpia.
- **DSLs Declarativos**: Las HOFs combinadas con function types con [receivers]({{ "/es/glosario/receiver-type/" | relative_url }}) son la base del desarrollo moderno en Android, habilitando la sintaxis declarativa de [DSL]({{ "/es/glosario/dsl/" | relative_url }}) que vemos en [Jetpack Compose]({{ "/es/glosario/jetpack-compose/" | relative_url }}) y las configuraciones de [Hilt]({{ "/es/glosario/hilt/" | relative_url }}).

## Code in Action

### HOF con lambda transform — actualizaciones optimistas de UI

Una función privada que recibe una [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) `(Task) -> Task` para aplicar una transformación a las tareas seleccionadas en memoria, de modo que la UI reacciona instantáneamente sin esperar el [round-trip]({{ "/es/glosario/round-trip/" | relative_url }}) de la base de datos.

```kotlin
// From FollowApp Suite — TasksViewModel.kt
private fun updateSelectedTasksOptimistically(transform: (Task) -> Task) {
    _uiState.update { state ->
        val tasks = state.activeTasks.map { task ->
            if (task.id in state.selectedTaskIds) transform(task) else task
        }
        val groups = state.groupBy?.let { computeTaskGroups(tasks, it) } ?: emptyList()
        state.copy(activeTasks = tasks, taskGroups = groups)
    }
}
```

### HOF con lambda predicate — selección bulk tri-state

Una función que acepta un predicado `(Task) -> Boolean` para calcular si un chip en el sheet de acciones masivas debe ser FULL, OUTLINE o PARTIAL según la selección actual.

```kotlin
// From FollowApp Suite — BulkSelection.kt
private fun triState(tasks: List<Task>, predicate: (Task) -> Boolean): BulkChipState {
    if (tasks.isEmpty()) return BulkChipState.OUTLINE
    val count = tasks.count(predicate)
    return when (count) {
        0 -> BulkChipState.OUTLINE
        tasks.size -> BulkChipState.FULL
        else -> BulkChipState.PARTIAL
    }
}

internal fun bulkTagState(tasks: List<Task>, tag: String): BulkChipState =
    triState(tasks) { task ->
        tag in ((task.customLabels["labels"] as? LabelValue.Tag)?.values ?: emptyList())
    }
```

### HOF genérica con extension + transform — deserialización JSON

Una [función de extensión]({{ "/es/01-kotlin-core/extension-functions/" | relative_url }}) [genérica]({{ "/es/01-kotlin-core/generics-variance-reification/" | relative_url }}) que recibe un transform `(JSONObject) -> T` para convertir un `JSONArray` en una `List<T>` tipada.

```kotlin
// From FollowApp Suite — BackupSerializer.kt
private fun <T> JSONArray.mapObjects(transform: (JSONObject) -> T): List<T> =
    (0 until length()).map { transform(getJSONObject(it)) }
```

### Consolidación de callbacks — domando listas de parámetros Composable

Cuando una pantalla requiere docenas de [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) de [callback]({{ "/es/glosario/callbacks/" | relative_url }}), agruparlas en una clase previene la explosión de firmas manteniendo cada [callback]({{ "/es/glosario/callbacks/" | relative_url }}) como un function type de primer nivel.

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

## The Interview (En el banquillo)

**Pregunta**: ¿Por qué evitarías usar la palabra clave [`inline`]({{ "/es/glosario/inline-functions/" | relative_url }}) para absolutamente todas las funciones de orden superior en un proyecto grande?

**Respuesta Senior**: Aunque [`inline`]({{ "/es/glosario/inline-functions/" | relative_url }}) evita la [allocation]({{ "/es/glosario/allocations/" | relative_url }}) de objetos, provoca que el compilador copie el [bytecode]({{ "/es/glosario/bytecode/" | relative_url }}) de la función en cada lugar donde se llama. Si el cuerpo de la función es grande y se invoca en muchos sitios, esto produce [code bloat]({{ "/es/glosario/code-bloat/" | relative_url }}), aumentando significativamente el tamaño del binario final (APK/AAB). Además, las [inline functions]({{ "/es/glosario/inline-functions/" | relative_url }}) no pueden acceder a miembros `private` de la clase en la que se encuentran (y los parámetros marcados [`crossinline`]({{ "/es/glosario/crossinline/" | relative_url }}) o [`noinline`]({{ "/es/glosario/noinline/" | relative_url }}) agregan restricciones adicionales), lo que puede limitar decisiones de arquitectura. Solo aplico [inline]({{ "/es/glosario/inline-functions/" | relative_url }}) en funciones que reciben [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) y cuyo cuerpo es lo suficientemente pequeño como para justificar el compromiso — típicamente funciones utilitarias como `onSuccess`, `runCatching`, o [scope functions]({{ "/es/01-kotlin-core/scope-functions/" | relative_url }}) personalizadas.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
