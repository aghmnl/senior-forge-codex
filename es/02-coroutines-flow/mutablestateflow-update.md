---
layout: page
title: "MutableStateFlow.update {}"
lang: es
permalink: /es/02-coroutines-flow/mutablestateflow-update/
order: 12
---

## The Theory (El Qué)

Un [`MutableStateFlow`]({{ "/es/glosario/mutable-state-flow/" | relative_url }}) se puede cambiar de dos formas. Asignar `value` **sobrescribe** el estado con un valor nuevo. Pero la mayoría de los cambios son **leer-modificar-escribir**: tomar el estado actual, derivar uno nuevo a partir de él y guardarlo. Escrito como `_uiState.value = _uiState.value.copy(isLoading = false)`, son dos operaciones separadas, una lectura y después una escritura. Si otro [thread]({{ "/es/glosario/thread/" | relative_url }}) escribe en el medio, la segunda escritura se calcula a partir de un valor viejo y **borra en silencio** la otra. Eso es una [race condition]({{ "/es/glosario/race-condition/" | relative_url }}), y el cambio perdido nunca produce un error.

[`update {}`]({{ "/es/glosario/update/" | relative_url }}) hace que el leer-modificar-escribir sea **[atómico]({{ "/es/glosario/atomicity/" | relative_url }})**. Es una extensión de [`MutableStateFlow`]({{ "/es/glosario/mutable-state-flow/" | relative_url }}), y su implementación entra en pocas líneas:

```kotlin
// kotlinx.coroutines — MutableStateFlow.update
inline fun <T> MutableStateFlow<T>.update(function: (T) -> T) {
    while (true) {
        val prevValue = value
        val nextValue = function(prevValue)
        if (compareAndSet(prevValue, nextValue)) return
    }
}
```

Lee el valor actual, calcula el siguiente con tu [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) y después llama a [`compareAndSet`]({{ "/es/glosario/compare-and-set/" | relative_url }}): "guardá `nextValue` solo si el estado sigue siendo `prevValue`". Si otro escritor llegó primero, la comparación falla y el ciclo **vuelve a intentar** con el valor nuevo. No hay [lock]({{ "/es/glosario/lock/" | relative_url }}): nadie espera, el que pierde simplemente recalcula. Esta técnica se llama [compare-and-set]({{ "/es/glosario/compare-and-set/" | relative_url }}).

Hay dos variantes para cuando quien llama necesita un valor de vuelta:

- **[`getAndUpdate { }`]({{ "/es/glosario/get-and-update/" | relative_url }})** aplica el cambio y devuelve el valor **anterior**.
- **[`updateAndGet { }`]({{ "/es/glosario/update-and-get/" | relative_url }})** aplica el cambio y devuelve el valor **nuevo**.

## The Senior Perspective (El Porqué)

- **La [race condition]({{ "/es/glosario/race-condition/" | relative_url }}) necesita paralelismo real.** `value = value.copy(...)` no tiene ningún [punto de suspensión]({{ "/es/glosario/suspension-point/" | relative_url }}) entre la lectura y la escritura, así que en un solo [thread]({{ "/es/glosario/thread/" | relative_url }}) (el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}), o un test adentro de [`runTest`]({{ "/es/glosario/run-test/" | relative_url }})) nada se puede meter en el medio. Se rompe cuando los escritores corren en **varios threads**, por ejemplo una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) en [`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) actualizando el estado mientras el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) también lo hace. El bug es raro, depende del timing y es imposible de reproducir a pedido: el peor tipo para depurar. [`update {}`]({{ "/es/glosario/update/" | relative_url }}) lo elimina por construcción, y no cuesta nada cuando no hay competencia.
- **Es la opción por defecto porque sobrevive a los refactors.** Un [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) que solo escribe desde el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) hoy es seguro con asignación simple. El día que alguien mueve una de esas escrituras a [`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}), el código sigue siendo correcto si todo leer-modificar-escribir ya pasa por [`update {}`]({{ "/es/glosario/update/" | relative_url }}). La regla "todo cambio derivado del estado actual usa [`update`]({{ "/es/glosario/update/" | relative_url }})" es fácil de revisar en un code review; "esto es seguro porque todos los escritores casualmente comparten un [thread]({{ "/es/glosario/thread/" | relative_url }})" no.
- **El [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) puede correr más de una vez, así que tiene que ser [puro]({{ "/es/glosario/pure-function/" | relative_url }}).** Si hay competencia, [`update`]({{ "/es/glosario/update/" | relative_url }}) vuelve a llamar a la función con el valor nuevo. Un log, un evento de analytics, una llamada de red o el incremento de un contador adentro del [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) pueden ocurrir dos veces. El [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) solo tiene que calcular el estado siguiente a partir de [`it`]({{ "/es/glosario/it/" | relative_url }}); los efectos secundarios van antes o después.
- **Solo está protegido lo que se calcula a partir de [`it`]({{ "/es/glosario/it/" | relative_url }}).** [`update {}`]({{ "/es/glosario/update/" | relative_url }}) garantiza la [atomicidad]({{ "/es/glosario/atomicity/" | relative_url }}) de la entrada y la salida del [lambda]({{ "/es/glosario/lambdas/" | relative_url }}), nada más. Leer `_uiState.value.items` afuera, calcular una lista nueva y después escribir `update { it.copy(items = newList) }` parece [atómico]({{ "/es/glosario/atomicity/" | relative_url }}) pero no lo es: `newList` se derivó de una foto del estado que puede estar vieja cuando el [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) corre. Todo lo que depende del estado actual se tiene que derivar adentro del [lambda]({{ "/es/glosario/lambdas/" | relative_url }}), a partir de [`it`]({{ "/es/glosario/it/" | relative_url }}).
- **Mantenelo corto.** Un cálculo largo adentro de [`update`]({{ "/es/glosario/update/" | relative_url }}) agranda la ventana en la que otro escritor puede ganar, y cada reintento lo repite. El trabajo lento (una [query]({{ "/es/glosario/query/" | relative_url }}), ordenar miles de ítems) que no depende del estado actual va afuera, y adentro solo se hace la combinación final.
- **La asignación simple sigue siendo correcta para sobrescribir.** Cuando el valor nuevo no depende del anterior (`_isLoading.value = true`, `_query.value = ""`), no hay nada que leer, así que no hay [race condition]({{ "/es/glosario/race-condition/" | relative_url }}) posible: `value =` es claro y correcto. [`update`]({{ "/es/glosario/update/" | relative_url }}) es para derivar, no para cada escritura.

## Code in Action

```kotlin
// De FollowApp Suite — TasksViewModel.kt
// El caso para el que existe update {}: esta coroutine escribe desde
// Dispatchers.IO mientras el main thread sigue actualizando el mismo _uiState
private fun restoreViewPreferences() {
    viewModelScope.launch(Dispatchers.IO) {
        val snapshot = runCatching { tasksViewPreferences.read() }.getOrNull()
        if (snapshot != null) {
            _uiState.update {
                it.copy(
                    sortOrder = snapshot.sortOrder,
                    groupBy = snapshot.groupBy,
                    // ...
                )
            }
        }
        _restored.value = true   // sobrescritura pura: la asignación simple alcanza
    }
}

// De FollowApp Suite — TasksViewModel.kt
// El update solo protege lo que se calcula a partir de `it`. Acá `reordered`
// se deriva de una foto leída AFUERA del lambda, así que la escritura no es
// atómica respecto de esa lectura. Es segura solo porque todos los escritores
// de activeTasks corren en el main thread.
fun onReorderComplete(orderedIds: List<String>) {
    val tasksById = _uiState.value.activeTasks.associateBy { it.id }
    val reordered = orderedIds.mapNotNull { tasksById[it] }
    if (reordered.size == _uiState.value.activeTasks.size) {
        _uiState.update { it.copy(activeTasks = reordered) }
    }
    // ...
}

// Not found in FAS — standalone example
// El mismo cambio derivado completamente adentro del lambda: atómico de punta a punta
_uiState.update { state ->
    val byId = state.activeTasks.associateBy { it.id }
    val reordered = orderedIds.mapNotNull { byId[it] }
    if (reordered.size == state.activeTasks.size) state.copy(activeTasks = reordered) else state
}

// De FollowApp Suite — LabelsListViewModel.kt
// value++ también es leer-modificar-escribir: lee value, suma uno y lo vuelve
// a escribir. Acá es seguro porque resync() solo corre en el main thread.
private fun resync() {
    _resyncTrigger.value++
}

// Not found in FAS — standalone example
// La versión atómica, correcta desde cualquier thread
private fun resync() {
    _resyncTrigger.update { it + 1 }
}

// Not found in FAS — standalone example
// El lambda puede volver a correr si hay competencia: los efectos secundarios quedan afuera
_uiState.update { it.copy(isSaving = true) }
analytics.log("save_started")   // una sola vez, después del cambio de estado
```

## The Interview (En el banquillo)

**Pregunta**: ¿Por qué escribir `_uiState.update { it.copy(isLoading = false) }` en vez de `_uiState.value = _uiState.value.copy(isLoading = false)`? ¿La segunda forma alguna vez es un problema real?

**Respuesta Senior**: La segunda forma es un leer-modificar-escribir partido en dos operaciones: lee el estado actual, arma una copia y la vuelve a escribir. Si otro [thread]({{ "/es/glosario/thread/" | relative_url }}) escribe el estado entre esa lectura y esa escritura, la copia se arma a partir de un valor viejo y el cambio del otro [thread]({{ "/es/glosario/thread/" | relative_url }}) se sobrescribe en silencio. Es una [race condition]({{ "/es/glosario/race-condition/" | relative_url }}) que no produce ningún error, solo una actualización perdida. [`update {}`]({{ "/es/glosario/update/" | relative_url }}) cierra ese hueco con [compare-and-set]({{ "/es/glosario/compare-and-set/" | relative_url }}): lee el valor, calcula el nuevo, y solo lo guarda si el estado sigue siendo el que leyó; si no, reintenta con el valor actualizado. Que la segunda forma sea un problema real depende de los threads. Sin ningún [punto de suspensión]({{ "/es/glosario/suspension-point/" | relative_url }}) entre la lectura y la escritura, un solo [thread]({{ "/es/glosario/thread/" | relative_url }}) no se puede intercalar, así que si todos los escritores corren en el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}), casualmente es seguro. Se vuelve un bug real en cuanto los escritores corren en paralelo, por ejemplo una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) en [`Dispatchers.IO`]({{ "/es/glosario/dispatchers-io/" | relative_url }}) actualizando el estado mientras el [main thread]({{ "/es/glosario/main-thread/" | relative_url }}) también lo hace, y ahí es intermitente y casi imposible de reproducir. Por eso uso [`update`]({{ "/es/glosario/update/" | relative_url }}) para todo cambio derivado del estado actual: es correcto sin importar los threads, no cuesta nada sin competencia, y sigue siendo correcto cuando alguien después mueve una escritura a otro [dispatcher]({{ "/es/glosario/dispatcher/" | relative_url }}). Para una sobrescritura pura, que no depende del valor anterior, la asignación simple está bien.

**Pregunta**: En un code review ves `_uiState.update { analytics.log("state_changed"); it.copy(count = it.count + 1) }`. ¿Qué marcarías?

**Respuesta Senior**: Dos cosas. La primera es el efecto secundario adentro del [lambda]({{ "/es/glosario/lambdas/" | relative_url }}). [`update`]({{ "/es/glosario/update/" | relative_url }}) es un ciclo de [compare-and-set]({{ "/es/glosario/compare-and-set/" | relative_url }}): cuando otro escritor cambia el estado primero, [`compareAndSet`]({{ "/es/glosario/compare-and-set/" | relative_url }}) falla y el [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) vuelve a correr con el valor nuevo. Si hay competencia, ese evento de analytics se registra dos veces, o más, para un solo cambio lógico. El [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) tiene que ser una [función pura]({{ "/es/glosario/pure-function/" | relative_url }}) del estado actual al siguiente, así que el log va después de la llamada a [`update`]({{ "/es/glosario/update/" | relative_url }}), donde corre exactamente una vez. La segunda es una regla más sutil que esta línea en particular cumple, pero que conviene revisar en el resto del cambio: solo es [atómico]({{ "/es/glosario/atomicity/" | relative_url }}) lo que se calcula a partir de [`it`]({{ "/es/glosario/it/" | relative_url }}). Acá `count + 1` se deriva de [`it`]({{ "/es/glosario/it/" | relative_url }}), así que el incremento es seguro. Si el código hubiera leído `_uiState.value.count` afuera del [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) y escrito `update { it.copy(count = savedCount + 1) }`, la [atomicidad]({{ "/es/glosario/atomicity/" | relative_url }}) se perdería, porque la entrada salió de una foto que ya puede estar vieja. Entonces mi regla para el review es: adentro de [`update`]({{ "/es/glosario/update/" | relative_url }}), derivar todo de [`it`]({{ "/es/glosario/it/" | relative_url }}), mantenerlo corto y dejar los efectos secundarios afuera.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
