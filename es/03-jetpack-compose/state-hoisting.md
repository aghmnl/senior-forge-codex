---
layout: page
title: "State Hoisting"
lang: es
permalink: /es/03-jetpack-compose/state-hoisting/
order: 3
---

## The Theory (El Qué)

Un composable que crea y guarda su propio estado con [`remember`]({{ "/es/glosario/remember/" | relative_url }}) es **[stateful]({{ "/es/glosario/stateful-stateless/" | relative_url }})** (con estado): funciona solo, pero quien lo llama no puede leer ese estado ni cambiarlo. Un composable que recibe su estado como parámetros es **[stateless]({{ "/es/glosario/stateful-stateless/" | relative_url }})** (sin estado): solo muestra lo que le dan e informa lo que hace el usuario.

El **state hoisting** (elevación de estado) es el patrón de convertir un composable [stateful]({{ "/es/glosario/stateful-stateless/" | relative_url }}) en uno [stateless]({{ "/es/glosario/stateful-stateless/" | relative_url }}) moviendo su estado hacia arriba, a quien lo llama. El estado se reemplaza por dos parámetros:

- **`value: T`**, el valor actual a mostrar, y
- **`onValueChange: (T) -> Unit`**, un evento que el composable llama cuando el usuario quiere cambiarlo.

El composable ya no decide nada: muestra `value` y llama a `onValueChange`. Quien lo llama es dueño del estado, decide qué hacer con cada evento y vuelve a pasar el valor nuevo hacia abajo. Es **[unidirectional data flow]({{ "/es/glosario/unidirectional-data-flow/" | relative_url }})** a la escala de un solo componente: **el estado baja, los eventos suben**. Los propios componentes de Material lo siguen: [`TextField(value, onValueChange)`]({{ "/es/glosario/text-field/" | relative_url }}), [`Checkbox(checked, onCheckedChange)`]({{ "/es/glosario/checkbox/" | relative_url }}), [`Switch(checked, onCheckedChange)`]({{ "/es/glosario/switch/" | relative_url }}).

Hasta dónde elevarlo es una decisión. La regla de la guía de Compose es elevar el estado **por lo menos hasta el ancestro común más bajo de todos los composables que lo leen**, y **tan arriba como el más bajo que lo escribe**, pero no más de lo necesario. Los tres destinos habituales son:

- **El propio composable**, con [`remember`]({{ "/es/glosario/remember/" | relative_url }}), cuando nadie más necesita el estado (estado simple de un elemento de UI).
- **Una clase [state holder]({{ "/es/glosario/state-holder/" | relative_url }}) común**, creada con una función `rememberXState()`, cuando la lógica de UI es lo bastante compleja para merecer su propia clase, como [`LazyListState`]({{ "/es/glosario/lazy-list-state/" | relative_url }}).
- **El [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }})**, cuando el estado viene de la lógica de negocio, tiene que sobrevivir a los [cambios de configuración]({{ "/es/glosario/configuration-change/" | relative_url }}), o lo leen partes distantes de la pantalla.

## The Senior Perspective (El Porqué)

- **Elevar el estado compra [single source of truth]({{ "/es/glosario/single-source-of-truth/" | relative_url }}).** Si dos composables guardan cada uno su propia copia del mismo valor, terminan desincronizados. Elevado a su ancestro común, hay un solo dueño y todos leen el mismo valor. Eso también hace que el estado se pueda compartir: una búsqueda elevada fuera de la barra de búsqueda puede manejar tanto la barra como la lista.
- **Los composables [stateless]({{ "/es/glosario/stateful-stateless/" | relative_url }}) son los reutilizables y testeables.** Un componente [stateless]({{ "/es/glosario/stateful-stateless/" | relative_url }}) se puede usar en cualquier pantalla, mostrar en un [Preview]({{ "/es/glosario/preview/" | relative_url }}) con cualquier valor, y testear pasándole valores y revisando qué eventos emite, sin [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) y sin repositorios falsos.
- **No elevar por reflejo.** Elevar todo al [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) convierte detalles de UI (si un dropdown está abierto, la posición del scroll, una animación) en estado de negocio, agranda el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) y recompone más de lo necesario. El estado de un elemento de UI que nadie más lee va cerca de donde se usa. La pregunta es "¿quién necesita leer o cambiar esto?", no "¿todo tiene que ir al [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }})?".
- **Ofrecer los dos modos en los componentes reutilizables.** Un componente de un [design system]({{ "/es/glosario/design-system/" | relative_url }}) suele admitir ser **[no controlado]({{ "/es/glosario/controlled-uncontrolled/" | relative_url }})**, manejando su propio estado con valores por defecto razonables, y **[controlado]({{ "/es/glosario/controlled-uncontrolled/" | relative_url }})**, cuando quien lo llama le pasa el valor y el evento porque necesita persistirlo o coordinarlo. La forma habitual es un parámetro `value` opcional: cuando es null, el componente usa su [`remember`]({{ "/es/glosario/remember/" | relative_url }}) interno; cuando no lo es, manda quien lo llama.
- **Pasar valores y [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}), no ViewModels ni [`MutableState`]({{ "/es/glosario/mutable-state/" | relative_url }}).** Un hijo que recibe el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) entero puede llamar a cualquier cosa, no se puede mostrar en un [Preview]({{ "/es/glosario/preview/" | relative_url }}) y depende de una clase que no necesita. Un hijo que recibe un [`MutableState`]({{ "/es/glosario/mutable-state/" | relative_url }}) lo puede escribir directamente, lo que crea un segundo escritor y rompe la regla de "los eventos suben". Pasar un valor común y una [lambda]({{ "/es/glosario/lambdas/" | relative_url }}) deja claro qué lee el hijo y qué puede disparar.
- **Nombrar los eventos por lo que pasó, no por lo que hay que hacer.** [`onQueryChange`]({{ "/es/glosario/event-handlers/" | relative_url }}), [`onExpandedChange`]({{ "/es/glosario/event-handlers/" | relative_url }}) y [`onDeleteClick`]({{ "/es/glosario/event-handlers/" | relative_url }}) describen la intención del usuario; el dueño decide el efecto. Mantiene al componente ajeno a las reglas de negocio, y permite que el mismo componente dispare comportamientos distintos en pantallas distintas.
- **Elevar el estado también puede reducir la [recomposition]({{ "/es/glosario/recomposition/" | relative_url }}).** El composable que lee un estado es el que se recompone. Elevar un valor solo hasta donde hace falta, y pasarlo solo a los hijos que lo usan, evita que un cambio frecuente recomponga una pantalla entera.

## Code in Action

```kotlin
// From FollowApp Suite — AnimatedSearchBar.kt
// Fully stateless: the query and whether search is active come from the
// caller, and typing or closing are reported as events. The bar never decides
// what the query is; the screen's state does.
@Composable
fun AnimatedSearchBar(
    isSearchActive: Boolean,
    searchQuery: String,
    onQueryChange: (String) -> Unit,
    onClose: () -> Unit,
    focusRequester: FocusRequester,
    // ...
)

// From FollowApp Suite — CollapsibleGroupCard.kt
// Both modes in one component. With expanded == null it is uncontrolled and
// keeps its own remember; with a value it is controlled and only reports the
// toggle, because the caller needs to persist the state.
@Composable
fun CollapsibleGroupCard(
    headerChip: @Composable () -> Unit,
    modifier: Modifier = Modifier,
    collapsible: Boolean = true,
    initiallyExpanded: Boolean = true,
    expanded: Boolean? = null,
    onExpandedChange: ((Boolean) -> Unit)? = null,
    // ...
) {
    var internalExpanded by remember { mutableStateOf(initiallyExpanded) }
    val effectiveExpandedRaw = expanded ?: internalExpanded
    // ...
    IconButton(
        onClick = {
            val next = !effectiveExpandedRaw
            if (expanded == null) internalExpanded = next
            onExpandedChange?.invoke(next)
        },
    ) { /* ... */ }
}

// From FollowApp Suite — TasksViewModel.kt
// Where the controlled mode leads: the collapsed groups are hoisted all the way
// to the ViewModel, because they are persisted per filter preset. The card only
// reports the toggle; the ViewModel owns the state.
fun onGroupCollapseToggle(groupKey: String) {
    val state = _uiState.value
    val bucket = state.activePresetId
        ?: com.followapp.mytasks.data.local.preferences.TasksViewPreferences.UNSAVED_PRESET_KEY
    val current = state.collapsedGroupsByPreset[bucket] ?: emptySet()
    val next = if (groupKey in current) current - groupKey else current + groupKey
    val newMap = if (next.isEmpty()) {
        state.collapsedGroupsByPreset - bucket
    } else {
        state.collapsedGroupsByPreset + (bucket to next)
    }
    _uiState.update { it.copy(collapsedGroupsByPreset = newMap) }
}

// Not found in FAS — standalone example
// The same component before and after hoisting.
@Composable
fun RatingBarStateful() {
    var rating by remember { mutableStateOf(0) }                 // nobody outside can read it
    Stars(selected = rating, onSelect = { rating = it })
}

@Composable
fun RatingBar(rating: Int, onRatingChange: (Int) -> Unit) {     // state down, events up
    Stars(selected = rating, onSelect = onRatingChange)
}
```

## The Interview (En el banquillo)

**Pregunta**: ¿Qué es el state hoisting en Compose, y cómo decidís hasta dónde elevar una pieza de estado?

**Respuesta Senior**: El state hoisting es sacar el estado de un composable y subirlo a quien lo llama, reemplazándolo por un parámetro de valor y un callback de evento, como [`TextField(value, onValueChange)`]({{ "/es/glosario/text-field/" | relative_url }}). El composable se vuelve [stateless]({{ "/es/glosario/stateful-stateless/" | relative_url }}): muestra lo que recibe e informa lo que hace el usuario, y quien lo llama es dueño del estado. Es [unidirectional data flow]({{ "/es/glosario/unidirectional-data-flow/" | relative_url }}) a nivel de componente: el estado baja, los eventos suben. Los beneficios son una [single source of truth]({{ "/es/glosario/single-source-of-truth/" | relative_url }}), porque un solo lugar es dueño del valor; la reutilización, porque el componente funciona en cualquier pantalla; y la testeabilidad y los [previews]({{ "/es/glosario/preview/" | relative_url }}), porque lo puedo dibujar con cualquier valor y verificar los eventos que emite. Para la altura, lo elevo hasta el ancestro común más bajo de todo lo que lee o escribe el estado, y no más arriba. Si solo le importa a ese composable, como si un dropdown está abierto, queda local con [`remember`]({{ "/es/glosario/remember/" | relative_url }}). Si la lógica de UI se complica, lo pongo en una clase [state holder]({{ "/es/glosario/state-holder/" | relative_url }}) común con una función [`remember`]({{ "/es/glosario/remember/" | relative_url }}), como funciona [`LazyListState`]({{ "/es/glosario/lazy-list-state/" | relative_url }}). Y si el estado viene de la lógica de negocio, tiene que sobrevivir a los [cambios de configuración]({{ "/es/glosario/configuration-change/" | relative_url }}) o se persiste, va al [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}). Lo que evito es elevar todo al [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) por defecto, porque mezcla detalles de UI con estado de negocio y recompone más de lo que debería.

**Pregunta**: Un compañero le pasa el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) entero, o un [`MutableState`]({{ "/es/glosario/mutable-state/" | relative_url }}), a un composable hijo para que actualice el estado directamente. ¿Qué tiene de malo, y qué harías en su lugar?

**Respuesta Senior**: Los dos rompen la dirección del flujo de datos. Con el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}), el hijo depende de una clase que no necesita, puede llamar a cualquier cosa, no se puede mostrar en un [Preview]({{ "/es/glosario/preview/" | relative_url }}) sin construir un [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}), y queda atado a esa pantalla. Con un [`MutableState`]({{ "/es/glosario/mutable-state/" | relative_url }}), el hijo pasa a ser un segundo escritor de un estado que no es suyo: el dueño ya no decide qué pasa con cada cambio, así que se pueden saltear validaciones, efectos o la persistencia, y cuando algo falla hay dos lugares donde buscar. En su lugar, le paso al hijo exactamente lo que lee, como valores comunes, y lo que puede disparar, como [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) con nombre de la intención del usuario, como [`onQueryChange`]({{ "/es/glosario/event-handlers/" | relative_url }}) u [`onDeleteClick`]({{ "/es/glosario/event-handlers/" | relative_url }}). El dueño, normalmente el composable de nivel de pantalla que habla con el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}), conecta esas [lambdas]({{ "/es/glosario/lambdas/" | relative_url }}) con las funciones del [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}). El hijo queda [stateless]({{ "/es/glosario/stateful-stateless/" | relative_url }}), previsualizable y reutilizable, y cada cambio del estado pasa por un único dueño. Si el componente también tiene que funcionar solo, le doy un parámetro de valor opcional para que pueda ser [controlado]({{ "/es/glosario/controlled-uncontrolled/" | relative_url }}) por quien lo llama o guardar su propio estado.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
