---
layout: page
title: "remember & rememberSaveable"
lang: es
permalink: /es/03-jetpack-compose/remember-remembersaveable/
order: 2
---

## The Theory (El Qué)

Un composable es una función, y Compose la puede volver a llamar en cada [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}). Cualquier variable local declarada en su cuerpo se vuelve a crear cada vez. [`remember`]({{ "/es/glosario/remember/" | relative_url }}) y [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}) son las dos formas de conservar un valor **entre esas llamadas**. La diferencia entre ellas es **cuánto tiempo** vive el valor.

**`remember { cálculo }`** ejecuta el cálculo la primera vez que el composable entra en la [composition]({{ "/es/glosario/composition/" | relative_url }}), guarda el resultado en la [composition]({{ "/es/glosario/composition/" | relative_url }}) y devuelve ese mismo valor guardado en cada [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}). Con keys, `remember(key1, key2) { ... }`, vuelve a ejecutar el cálculo cada vez que cambia una key. El valor **se olvida cuando el composable sale de la [composition]({{ "/es/glosario/composition/" | relative_url }})**, y también se pierde cuando la [Activity]({{ "/es/glosario/activity/" | relative_url }}) se recrea: un [cambio de configuración]({{ "/es/glosario/configuration-change/" | relative_url }}) (rotación, modo oscuro, un cambio de idioma) o la [muerte del proceso]({{ "/es/glosario/process-death/" | relative_url }}).

**`rememberSaveable { cálculo }`** hace lo mismo y **además guarda el valor** en el [saved instance state]({{ "/es/glosario/saved-instance-state/" | relative_url }}) (estado de instancia guardado), el mismo mecanismo de [`Bundle`]({{ "/es/glosario/bundle/" | relative_url }}) que las [Activities]({{ "/es/glosario/activity/" | relative_url }}) usaron siempre. Cuando la [Activity]({{ "/es/glosario/activity/" | relative_url }}) se recrea, después de un [cambio de configuración]({{ "/es/glosario/configuration-change/" | relative_url }}) o después de que el sistema mató el proceso en background, el valor se restaura en lugar de calcularse de nuevo.

Como va a un [`Bundle`]({{ "/es/glosario/bundle/" | relative_url }}), un valor guardado con [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}) tiene que ser de un tipo que el [`Bundle`]({{ "/es/glosario/bundle/" | relative_url }}) pueda contener: [primitivos]({{ "/es/glosario/primitives/" | relative_url }}), [`String`]({{ "/es/glosario/string/" | relative_url }}), [`Parcelable`]({{ "/es/glosario/parcelable/" | relative_url }}) (normalmente una clase anotada con [`@Parcelize`]({{ "/es/glosario/parcelize/" | relative_url }})) o [`Serializable`]({{ "/es/glosario/serializable/" | relative_url }}). Para cualquier otro tipo se provee un **[`Saver`]({{ "/es/glosario/saver/" | relative_url }})**, que convierte el valor en algo guardable y de vuelta. [`listSaver`]({{ "/es/glosario/list-saver/" | relative_url }}) y [`mapSaver`]({{ "/es/glosario/map-saver/" | relative_url }}) son ayudas para escribir uno.

Ninguno de los dos es reactivo por sí solo. Para que Compose se recomponga cuando un valor cambia, lo que se recuerda es un [`MutableState`]({{ "/es/glosario/mutable-state/" | relative_url }}): `var text by rememberSaveable { mutableStateOf("") }`.

## The Senior Perspective (El Porqué)

- **La elección es por tiempo de vida, no por importancia.** [`remember`]({{ "/es/glosario/remember/" | relative_url }}) es para valores que se pueden recrear o que da igual perder: caches de cálculos, formatters, mediciones, estado de animaciones, objetos como [`Animatable`]({{ "/es/glosario/animatable/" | relative_url }}). [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}) es para **estado que creó el usuario y que notaría si se pierde**: el texto escrito en un campo, la pestaña elegida, si una sección está expandida, un diálogo abierto. La pregunta es "si el usuario rota el teléfono, o vuelve después de que el sistema mató la app, ¿esto tiene que seguir acá?".
- **La rotación es el caso fácil de probar; la [muerte del proceso]({{ "/es/glosario/process-death/" | relative_url }}) es la que muerde.** Muchos bugs nunca aparecen durante el desarrollo porque el proceso nunca se mata. En producción, el usuario pasa a la cámara, Android recupera memoria, y cuando vuelve la [Activity]({{ "/es/glosario/activity/" | relative_url }}) se recrea desde el [estado guardado]({{ "/es/glosario/saved-instance-state/" | relative_url }}). Todo lo que estaba en [`remember`]({{ "/es/glosario/remember/" | relative_url }}), o solo en un [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}), desapareció. "No mantener actividades" en las opciones de desarrollador, o matar el proceso desde adb mientras la app está en background, lo reproduce.
- **[`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}) no es una base de datos.** El [estado guardado]({{ "/es/glosario/saved-instance-state/" | relative_url }}) viaja en un [`Bundle`]({{ "/es/glosario/bundle/" | relative_url }}) que cruza procesos, y su tamaño total es limitado (alrededor de 1 MB para toda la transacción, compartido con el resto de la app). Guardar listas grandes u objetos de dominio puede romper con una [`TransactionTooLargeException`]({{ "/es/glosario/transaction-too-large-exception/" | relative_url }}). Hay que guardar valores chicos de UI, como un id o una búsqueda, y reconstruir el resto desde la fuente real de datos.
- **También importa dónde vive.** El estado de un elemento de UI pertenece al composable, con [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}). El estado de pantalla que viene de la lógica de negocio pertenece al [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}), que sobrevive a los [cambios de configuración]({{ "/es/glosario/configuration-change/" | relative_url }}) pero **no** a la [muerte del proceso]({{ "/es/glosario/process-death/" | relative_url }}); para eso, el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) usa [`SavedStateHandle`]({{ "/es/glosario/saved-state-handle/" | relative_url }}), el mismo mecanismo expuesto al [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}). Duplicar el mismo valor en los dos lugares crea dos fuentes de verdad.
- **Las keys son entradas, y olvidarse una es un bug.** `remember(query) { filter(query) }` es correcto. Si el cálculo también depende de un parámetro que no es key, el valor cacheado queda viejo cuando ese parámetro cambia. Cada valor que lee el cálculo tiene que ser una key, o venir de adentro del cálculo.
- **Las listas y la navegación conservan el estado saveable por vos.** Adentro de un [`LazyColumn`]({{ "/es/glosario/lazy-column/" | relative_url }}), un ítem que sale de la pantalla al scrollear sale de la [composition]({{ "/es/glosario/composition/" | relative_url }}) y olvida sus valores de [`remember`]({{ "/es/glosario/remember/" | relative_url }}), pero sus valores de [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}) se restauran cuando vuelve. Lo mismo pasa con las pantallas en el back stack de Navigation. Por eso también [`rememberLazyListState()`]({{ "/es/glosario/remember-lazy-list-state/" | relative_url }}) restaura la posición del scroll: está construido sobre [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}).

## Code in Action

```kotlin
// From FollowApp Suite — SettingsScreen.kt (TimeZonePickerDialog)
// remember used as a cache: the full zone list is computed once, and the
// filtered list is recomputed only when the query (its key) changes.
// Losing these on rotation costs nothing: they are rebuilt from scratch.
val allZones = remember {
    val device = ZoneId.systemDefault().id
    listOf(device) + ZoneId.getAvailableZoneIds().sorted().filter { it != device }
}
val filtered = remember(query) {
    if (query.isBlank()) allZones
    else allZones.filter { it.lowercase(Locale.ROOT).contains(query.trim().lowercase(Locale.ROOT)) }
}

// From FollowApp Suite — SettingsScreen.kt
// Dialog flags and the text typed in the search field use remember. The
// manifest only handles locale and layoutDirection changes itself, so a
// rotation recreates the Activity: an open dialog closes and the typed query
// is cleared. That is acceptable for a short confirmation; for text the user
// typed, rememberSaveable keeps it with no other change (Boolean and String
// are saveable).
var showClearAllConfirm by remember { mutableStateOf(false) }
var query by remember { mutableStateOf("") }

// Not found in FAS — standalone example
// The saveable versions of the same state.
var showClearAllConfirm by rememberSaveable { mutableStateOf(false) }
var query by rememberSaveable { mutableStateOf("") }

// Not found in FAS — standalone example
// A type the Bundle cannot hold needs a Saver. listSaver turns it into a
// list of saveable values and back.
data class DateRange(val start: LocalDate, val end: LocalDate)

val DateRangeSaver = listSaver<DateRange, String>(
    save = { listOf(it.start.toString(), it.end.toString()) },
    restore = { DateRange(LocalDate.parse(it[0]), LocalDate.parse(it[1])) }
)

var range by rememberSaveable(stateSaver = DateRangeSaver) {
    mutableStateOf(DateRange(LocalDate.now(), LocalDate.now().plusDays(7)))
}
```

## The Interview (En el banquillo)

**Pregunta**: ¿Cuál es la diferencia entre [`remember`]({{ "/es/glosario/remember/" | relative_url }}) y [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}), y cómo decidís cuál usar?

**Respuesta Senior**: Los dos conservan un valor entre recomposiciones, algo que una variable local no puede hacer porque la función composable se vuelve a ejecutar cada vez. La diferencia es el tiempo de vida. [`remember`]({{ "/es/glosario/remember/" | relative_url }}) guarda el valor en la [composition]({{ "/es/glosario/composition/" | relative_url }}), así que vive mientras el composable está en la [composition]({{ "/es/glosario/composition/" | relative_url }}): se pierde cuando el composable sale, y cuando la [Activity]({{ "/es/glosario/activity/" | relative_url }}) se recrea, sea por un [cambio de configuración]({{ "/es/glosario/configuration-change/" | relative_url }}) como una rotación o por la [muerte del proceso]({{ "/es/glosario/process-death/" | relative_url }}). [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}) además escribe el valor en el [saved instance state]({{ "/es/glosario/saved-instance-state/" | relative_url }}), así que después de una recreación se restaura. Como ese estado es un [`Bundle`]({{ "/es/glosario/bundle/" | relative_url }}), el valor tiene que ser un primitivo, un [`String`]({{ "/es/glosario/string/" | relative_url }}), un [`Parcelable`]({{ "/es/glosario/parcelable/" | relative_url }}) o un [`Serializable`]({{ "/es/glosario/serializable/" | relative_url }}), o tengo que proveer un [`Saver`]({{ "/es/glosario/saver/" | relative_url }}). Mi regla es lo que notaría el usuario. Caches, formatters, mediciones y estado de animaciones van en [`remember`]({{ "/es/glosario/remember/" | relative_url }}), porque se pueden recalcular. El estado que creó el usuario, como el texto escrito, la pestaña elegida o una sección expandida, va en [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}), porque perderlo después de una rotación o al volver a la app se siente como un bug. Y lo mantengo chico, porque el [`Bundle`]({{ "/es/glosario/bundle/" | relative_url }}) tiene un límite de tamaño: guardo un id o una búsqueda, nunca una lista de objetos de dominio.

**Pregunta**: Los usuarios reportan que un formulario largo pierde todo lo que escribieron cuando pasan a otra app para copiar algo y vuelven. Rotar el dispositivo en las pruebas no lo reproduce. ¿Qué está pasando y cómo lo arreglás?

**Respuesta Senior**: Parece [muerte del proceso]({{ "/es/glosario/process-death/" | relative_url }}). Mientras el usuario está en la otra app, Android puede matar el proceso de la app para recuperar memoria. Cuando vuelve, la [Activity]({{ "/es/glosario/activity/" | relative_url }}) se recrea desde su [estado guardado]({{ "/es/glosario/saved-instance-state/" | relative_url }}), y solo sobrevive lo que se escribió ahí. Si la rotación funciona, el estado del formulario probablemente está en un [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}), que sobrevive a los [cambios de configuración]({{ "/es/glosario/configuration-change/" | relative_url }}) pero no a la [muerte del proceso]({{ "/es/glosario/process-death/" | relative_url }}), o en un [`remember`]({{ "/es/glosario/remember/" | relative_url }}) común. Primero lo reproduciría, con "No mantener actividades" o matando el proceso desde adb mientras la app está en background. La solución depende de dónde vive el estado. Si es estado de UI en el composable, [`rememberSaveable`]({{ "/es/glosario/remember-saveable/" | relative_url }}) en lugar de [`remember`]({{ "/es/glosario/remember/" | relative_url }}). Si vive en el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}), que es el lugar habitual para un formulario que se valida y se envía, guardo los valores de los campos en [`SavedStateHandle`]({{ "/es/glosario/saved-state-handle/" | relative_url }}), para que se escriban en el [estado guardado]({{ "/es/glosario/saved-instance-state/" | relative_url }}) y se restauren al recrearse. En los dos casos guardo solo los valores chicos, el texto de cada campo y quizás el índice del paso, y no datos derivados, porque el [estado guardado]({{ "/es/glosario/saved-instance-state/" | relative_url }}) tiene un límite de tamaño y un [`Bundle`]({{ "/es/glosario/bundle/" | relative_url }}) grande puede romper con una [`TransactionTooLargeException`]({{ "/es/glosario/transaction-too-large-exception/" | relative_url }}).

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
