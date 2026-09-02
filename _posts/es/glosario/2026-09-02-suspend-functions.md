---
layout: post
title: "Suspend Functions"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/suspend-functions/
---

## The Theory (El Qué)

Una **suspend function** (función suspendible) es una función marcada con el modificador `suspend` que puede pausarse y reanudarse sin bloquear el thread en el que corre. Las suspend functions son el bloque fundamental de las [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) de Kotlin: permiten escribir [operaciones async]({{ "/es/glosario/async-operations/" | relative_url }}) en un estilo secuencial y legible mientras el [runtime]({{ "/es/glosario/runtime/" | relative_url }}) maneja la suspensión y continuación detrás de escena.

```kotlin
// From FollowApp Suite — LabelRepository.kt
interface LabelRepository {
    fun getLabelsWithOptions(): Flow<Map<Label, List<LabelOption>>>

    suspend fun getOrCreateLabel(name: String, type: LabelType): Label
    suspend fun upsertLabelOption(labelId: String, label: String, sortOrder: Int = 0): LabelOption
    suspend fun updateLabelOption(id: String, label: String): LabelOption
    suspend fun updateLabelOptionSortOrders(orderedIds: List<String>)
    suspend fun deleteLabelOption(labelOptionId: String)
    suspend fun renameLabel(labelId: String, name: String)
    suspend fun deleteLabel(labelId: String)
}
```

La keyword `suspend` señala que estas operaciones pueden tomar tiempo (I/O de base de datos, llamadas de red) y deben llamarse desde una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) u otra suspend function — el compilador lo hace cumplir en [compile time]({{ "/es/glosario/compile-time/" | relative_url }}).

## The Senior Nuance (El Matiz Senior)

- **Thread safety por convención**: Una suspend function suspende la coroutine, no el thread. Esto significa que un solo thread puede ejecutar miles de coroutines concurrentemente. Los desarrolladores senior estructuran sus interfaces de repositorio con `suspend` para operaciones one-shot y `Flow` para streams observables — como muestra el ejemplo de FAS.
- **Structured concurrency**: Las suspend functions heredan el `CoroutineScope` del caller, lo que significa que la cancelación se propaga automáticamente. Cuando un ViewModel se limpia, su `viewModelScope` cancela, y todas las llamadas suspend pendientes se cancelan — sin cleanup manual.
- **Bajo el capó**, el compilador transforma cada suspend function en una state machine con un parámetro `Continuation`. Por eso las suspend functions solo se pueden llamar desde un contexto de coroutine — necesitan una continuation para reanudar.
- **Puente a [callbacks]({{ "/es/glosario/callbacks/" | relative_url }})**: `suspendCancellableCoroutine` wrappea una API basada en [callback]({{ "/es/glosario/callbacks/" | relative_url }}) en una suspend function, convirtiendo el estilo de [event handler]({{ "/es/glosario/event-handlers/" | relative_url }}) en estilo secuencial. Así es como muchas APIs del framework Android (originalmente basadas en callbacks) se consumen en código moderno.
- **`withContext`** cambia el dispatcher dentro de una suspend function sin crear una nueva coroutine. Los desarrolladores senior lo usan para asegurar que trabajo I/O-bound corra en `Dispatchers.IO` manteniendo al caller en `Dispatchers.Main` — un patrón visible a lo largo del código Android [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}).

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
