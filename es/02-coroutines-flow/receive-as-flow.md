---
layout: page
title: "receiveAsFlow()"
lang: es
permalink: /es/02-coroutines-flow/receive-as-flow/
order: 15
---

## The Theory (El Qué)

`receiveAsFlow()` convierte un [`Channel`]({{ "/es/02-coroutines-flow/channel-hot-streams/" | relative_url }}) (más precisamente, cualquier [`ReceiveChannel`]({{ "/es/glosario/receive-channel/" | relative_url }})) en un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}). No copia ni guarda nada: cada vez que alguien llama a [`collect`]({{ "/es/glosario/collect/" | relative_url }}) sobre ese [`Flow`]({{ "/es/glosario/flow/" | relative_url }}), el [collector]({{ "/es/glosario/collector/" | relative_url }}) corre un loop de [`receive`]({{ "/es/glosario/receive/" | relative_url }}) sobre el [channel]({{ "/es/glosario/channel/" | relative_url }}) y emite cada valor que obtiene.

Eso significa que el resultado **parece un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) pero se comporta como un [channel]({{ "/es/glosario/channel/" | relative_url }})**:

- **Es hot.** Los valores viven en el [channel]({{ "/es/glosario/channel/" | relative_url }}), no en el [`Flow`]({{ "/es/glosario/flow/" | relative_url }}). Los valores enviados antes de que alguien colecte esperan en el buffer del [channel]({{ "/es/glosario/channel/" | relative_url }}) (si la capacidad lo permite), y volver a colectar más tarde no arranca nada desde el principio.
- **Cada valor se entrega una sola vez.** Un valor que tomó un [collector]({{ "/es/glosario/collector/" | relative_url }}) desaparece del [channel]({{ "/es/glosario/channel/" | relative_url }}). Con dos [collectors]({{ "/es/glosario/collector/" | relative_url }}) al mismo tiempo, los valores se reparten entre ellos ([fan-out]({{ "/es/glosario/fan-out/" | relative_url }})); no se copian a los dos.
- **Cancelar un [collector]({{ "/es/glosario/collector/" | relative_url }}) no cierra el [channel]({{ "/es/glosario/channel/" | relative_url }}).** La colección se detiene, el [channel]({{ "/es/glosario/channel/" | relative_url }}) sigue abierto, y un [collector]({{ "/es/glosario/collector/" | relative_url }}) nuevo puede seguir donde dejó el anterior.
- **El [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) termina cuando el [channel]({{ "/es/glosario/channel/" | relative_url }}) se cierra.** Si el [channel]({{ "/es/glosario/channel/" | relative_url }}) se cierra normalmente con [`close()`]({{ "/es/glosario/close/" | relative_url }}), la colección se completa. Si se cierra con una excepción, [`collect`]({{ "/es/glosario/collect/" | relative_url }}) lanza esa excepción.

Su hermano es **`consumeAsFlow()`**. Hace lo mismo, con dos diferencias: se puede colectar **una sola vez** (un segundo [`collect`]({{ "/es/glosario/collect/" | relative_url }}) lanza una [`IllegalStateException`]({{ "/es/glosario/illegal-state-exception/" | relative_url }})), y cuando esa colección termina, por el motivo que sea, **cancela el [channel]({{ "/es/glosario/channel/" | relative_url }})**. Dicho de otro modo, [`consumeAsFlow`]({{ "/es/glosario/consume-as-flow/" | relative_url }}) le da al [collector]({{ "/es/glosario/collector/" | relative_url }}) la propiedad del [channel]({{ "/es/glosario/channel/" | relative_url }}); [`receiveAsFlow`]({{ "/es/glosario/receive-as-flow/" | relative_url }}) solo se lo presta.

También existe la dirección opuesta: `produceIn(scope)` convierte un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) en un [`ReceiveChannel`]({{ "/es/glosario/receive-channel/" | relative_url }}).

## The Senior Perspective (El Porqué)

- **Su trabajo principal en Android: [eventos]({{ "/es/glosario/one-shot-event/" | relative_url }}) one-shot (de una sola vez) desde un [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}).** El patrón habitual es un [`Channel`]({{ "/es/glosario/channel/" | relative_url }}) privado con buffer y un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) público construido con `receiveAsFlow()`. La UI puede colectar, pero no puede hacer [`send`]({{ "/es/glosario/send/" | relative_url }}), así que solo el [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) [produce]({{ "/es/glosario/produce/" | relative_url }}) [eventos]({{ "/es/glosario/one-shot-event/" | relative_url }}). Es el equivalente, para channels, de exponer un [`MutableStateFlow`]({{ "/es/glosario/mutable-state-flow/" | relative_url }}) con `asStateFlow()`.
- **Por qué un [channel]({{ "/es/glosario/channel/" | relative_url }}) y no un [`SharedFlow`]({{ "/es/glosario/sharedflow/" | relative_url }}) para esos [eventos]({{ "/es/glosario/one-shot-event/" | relative_url }}).** Un [`SharedFlow`]({{ "/es/02-coroutines-flow/sharedflow/" | relative_url }}) con `replay = 0` entrega cada valor solo a los [collectors]({{ "/es/glosario/collector/" | relative_url }}) que existen en ese momento. Si la pantalla está en background, con [`repeatOnLifecycle`]({{ "/es/glosario/repeat-on-lifecycle/" | relative_url }}) su [collector]({{ "/es/glosario/collector/" | relative_url }}) está cancelado, y un [evento]({{ "/es/glosario/one-shot-event/" | relative_url }}) emitido en ese momento se pierde. Un [channel]({{ "/es/glosario/channel/" | relative_url }}) con buffer guarda el [evento]({{ "/es/glosario/one-shot-event/" | relative_url }}) hasta que alguien vuelve a colectar, y [`receiveAsFlow`]({{ "/es/glosario/receive-as-flow/" | relative_url }}) se lo entrega a ese [collector]({{ "/es/glosario/collector/" | relative_url }}) una vez. Es exactamente el comportamiento "entregar después, pero una sola vez" que necesita una navegación o un snackbar.
- **El tipo esconde la semántica.** Un `Flow<UiEvent>` público parece cold, pero no lo es: dos [collectors]({{ "/es/glosario/collector/" | relative_url }}) no reciben cada uno todos los [eventos]({{ "/es/glosario/one-shot-event/" | relative_url }}), y volver a colectar no repite nada. Eso es fácil de romper sin darse cuenta: un segundo composable que colecta los mismos `events` se queda con la mitad. Un senior se asegura de que haya **exactamente un [collector]({{ "/es/glosario/collector/" | relative_url }})** para ese [flow]({{ "/es/glosario/flow/" | relative_url }}) y lo documenta.
- **Un valor recibido es un valor que ya no está, aunque nunca se procese.** El [channel]({{ "/es/glosario/channel/" | relative_url }}) entrega el [evento]({{ "/es/glosario/one-shot-event/" | relative_url }}) cuando el [collector]({{ "/es/glosario/collector/" | relative_url }}) lo recibe, no cuando termina de procesarlo. Si el [collector]({{ "/es/glosario/collector/" | relative_url }}) se cancela en el medio, por ejemplo durante un cambio de configuración, el [evento]({{ "/es/glosario/one-shot-event/" | relative_url }}) se pierde. Colectar en [`Dispatchers.Main.immediate`]({{ "/es/glosario/dispatchers-main-immediate/" | relative_url }}) (que [`repeatOnLifecycle`]({{ "/es/glosario/repeat-on-lifecycle/" | relative_url }}) ya usa) achica mucho esa ventana, pero no la elimina. Por eso la guía de Google prefiere modelar estos [eventos]({{ "/es/glosario/one-shot-event/" | relative_url }}) como **estado de UI** que la UI consume y limpia: sobrevive a la rotación y a la muerte del proceso. [`receiveAsFlow`]({{ "/es/glosario/receive-as-flow/" | relative_url }}) es la opción pragmática cuando el [evento]({{ "/es/glosario/one-shot-event/" | relative_url }}) realmente tiene que ser un [evento]({{ "/es/glosario/one-shot-event/" | relative_url }}).
- **[`receiveAsFlow`]({{ "/es/glosario/receive-as-flow/" | relative_url }}) vs [`consumeAsFlow`]({{ "/es/glosario/consume-as-flow/" | relative_url }}) es una decisión de ciclo de vida.** Si el [channel]({{ "/es/glosario/channel/" | relative_url }}) vive más que sus [collectors]({{ "/es/glosario/collector/" | relative_url }}) (el [channel]({{ "/es/glosario/channel/" | relative_url }}) de un [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) colectado por una pantalla que va y viene), tiene que ser [`receiveAsFlow`]({{ "/es/glosario/receive-as-flow/" | relative_url }}): con [`consumeAsFlow`]({{ "/es/glosario/consume-as-flow/" | relative_url }}), la primera vez que la pantalla pasa a background el [channel]({{ "/es/glosario/channel/" | relative_url }}) se cancelaría, y la siguiente colección lanzaría una excepción. [`consumeAsFlow`]({{ "/es/glosario/consume-as-flow/" | relative_url }}) encaja cuando el [channel]({{ "/es/glosario/channel/" | relative_url }}) existe solo para alimentar una colección, y cerrarlo cuando esa colección termina es exactamente lo que se quiere.
- **Preferirlo a `for (value in channel)` cuando el [consumidor]({{ "/es/glosario/producer-consumer/" | relative_url }}) habla [`Flow`]({{ "/es/glosario/flow/" | relative_url }}).** Una vez que el [channel]({{ "/es/glosario/channel/" | relative_url }}) es un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}), todos los operadores ([`map`]({{ "/es/glosario/map-operator/" | relative_url }}), [`filter`]({{ "/es/glosario/filter/" | relative_url }}), [`debounce`]({{ "/es/glosario/debounce/" | relative_url }}), [`catch`]({{ "/es/glosario/catch/" | relative_url }})) y las APIs de colección conscientes del ciclo de vida funcionan sobre él sin código extra.

## Code in Action

```kotlin
// Not found in FAS — standalone example
// The ViewModel owns the channel; the UI only sees a Flow it can collect.
class CheckoutViewModel : ViewModel() {

    private val _events = Channel<CheckoutEvent>(Channel.BUFFERED)
    val events: Flow<CheckoutEvent> = _events.receiveAsFlow()   // exactly one collector

    fun onPayClicked() {
        viewModelScope.launch {
            val result = repository.pay()
            _events.send(
                if (result.isSuccess) CheckoutEvent.GoToReceipt
                else CheckoutEvent.ShowError(result.message)
            )
        }
    }
}

// Not found in FAS — standalone example
// One collector, tied to the lifecycle. If the payment finishes while the app is
// in the background, the event waits in the buffer and is delivered on return.
@Composable
fun CheckoutScreen(viewModel: CheckoutViewModel, onReceipt: () -> Unit) {
    val lifecycleOwner = LocalLifecycleOwner.current
    LaunchedEffect(viewModel, lifecycleOwner) {
        lifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
            viewModel.events.collect { event ->
                when (event) {
                    CheckoutEvent.GoToReceipt -> onReceipt()
                    is CheckoutEvent.ShowError -> snackbarHost.showSnackbar(event.message)
                }
            }
        }
    }
}

// Not found in FAS — standalone example
// The fan-out trap: two collectors on the same receiveAsFlow split the events.
// The banner and the logger each see only some of them.
launch { viewModel.events.collect { showBanner(it) } }
launch { viewModel.events.collect { analytics.log(it) } }   // steals events from the banner

// Not found in FAS — standalone example
// consumeAsFlow: the channel lives only for this collection. When it ends,
// the channel is cancelled; collecting the same flow again throws.
val progress = Channel<Int>(Channel.CONFLATED)
progress.consumeAsFlow()
    .map { "$it%" }
    .collect { label.text = it }
```

## The Interview (En el banquillo)

**Pregunta**: ¿Qué hace `receiveAsFlow()`, y por qué es la forma habitual de exponer [eventos]({{ "/es/glosario/one-shot-event/" | relative_url }}) one-shot desde un [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) en lugar de un [`SharedFlow`]({{ "/es/glosario/sharedflow/" | relative_url }})?

**Respuesta Senior**: Envuelve un [channel]({{ "/es/glosario/channel/" | relative_url }}) en un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}): cada colección corre un loop de [`receive`]({{ "/es/glosario/receive/" | relative_url }}) sobre el [channel]({{ "/es/glosario/channel/" | relative_url }}) y emite lo que obtiene. Así que el resultado conserva la semántica del [channel]({{ "/es/glosario/channel/" | relative_url }}). Es hot, cada valor se entrega a exactamente un [collector]({{ "/es/glosario/collector/" | relative_url }}), cancelar el [collector]({{ "/es/glosario/collector/" | relative_url }}) deja el [channel]({{ "/es/glosario/channel/" | relative_url }}) abierto, y el [flow]({{ "/es/glosario/flow/" | relative_url }}) se completa cuando el [channel]({{ "/es/glosario/channel/" | relative_url }}) se cierra. Para [eventos]({{ "/es/glosario/one-shot-event/" | relative_url }}) one-shot, como una navegación o un snackbar, eso es lo que se quiere. Con un [channel]({{ "/es/glosario/channel/" | relative_url }}) privado con buffer y un `receiveAsFlow()` público, la UI solo puede colectar, y un [evento]({{ "/es/glosario/one-shot-event/" | relative_url }}) enviado mientras la pantalla está en background, con su [collector]({{ "/es/glosario/collector/" | relative_url }}) cancelado por [`repeatOnLifecycle`]({{ "/es/glosario/repeat-on-lifecycle/" | relative_url }}), espera en el buffer y se entrega una vez cuando la pantalla vuelve. Un [`SharedFlow`]({{ "/es/glosario/sharedflow/" | relative_url }}) sin replay lo habría descartado, porque no había nadie suscrito, y agregarle replay lo entregaría de nuevo después de cada rotación. Tengo presentes dos salvedades: tiene que tener un único [collector]({{ "/es/glosario/collector/" | relative_url }}), porque dos [collectors]({{ "/es/glosario/collector/" | relative_url }}) se reparten los [eventos]({{ "/es/glosario/one-shot-event/" | relative_url }}) en lugar de recibirlos los dos; y un [evento]({{ "/es/glosario/one-shot-event/" | relative_url }}) ya recibido se puede perder igual si el [collector]({{ "/es/glosario/collector/" | relative_url }}) se cancela antes de procesarlo. Por eso, cuando puedo, modelo el [evento]({{ "/es/glosario/one-shot-event/" | relative_url }}) como estado de UI que la UI consume y limpia, y dejo [`receiveAsFlow`]({{ "/es/glosario/receive-as-flow/" | relative_url }}) para los casos que realmente son [eventos]({{ "/es/glosario/one-shot-event/" | relative_url }}).

**Pregunta**: ¿Cuál es la diferencia entre `receiveAsFlow()` y `consumeAsFlow()`, y qué sale mal si usás `consumeAsFlow()` para el [channel]({{ "/es/glosario/channel/" | relative_url }}) de [eventos]({{ "/es/glosario/one-shot-event/" | relative_url }}) de un [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }})?

**Respuesta Senior**: Los dos convierten un [channel]({{ "/es/glosario/channel/" | relative_url }}) en un [`Flow`]({{ "/es/glosario/flow/" | relative_url }}) con el mismo comportamiento por valor. La diferencia es la propiedad. [`receiveAsFlow`]({{ "/es/glosario/receive-as-flow/" | relative_url }}) solo toma prestado el [channel]({{ "/es/glosario/channel/" | relative_url }}): se puede colectar muchas veces, una después de otra o incluso en paralelo, y cuando una colección termina el [channel]({{ "/es/glosario/channel/" | relative_url }}) sigue abierto. [`consumeAsFlow`]({{ "/es/glosario/consume-as-flow/" | relative_url }}) se queda con la propiedad: se puede colectar una sola vez, una segunda colección lanza una [`IllegalStateException`]({{ "/es/glosario/illegal-state-exception/" | relative_url }}), y cuando esa colección termina, normalmente o por cancelación, cancela el [channel]({{ "/es/glosario/channel/" | relative_url }}). En un [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) la pantalla colecta con [`repeatOnLifecycle`]({{ "/es/glosario/repeat-on-lifecycle/" | relative_url }}), así que la colección se cancela cada vez que la app pasa a background. Con [`consumeAsFlow`]({{ "/es/glosario/consume-as-flow/" | relative_url }}), esa primera cancelación cancelaría el [channel]({{ "/es/glosario/channel/" | relative_url }}): desde ahí el [`send`]({{ "/es/glosario/send/" | relative_url }}) del [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) fallaría y la siguiente colección, cuando el usuario vuelve, lanzaría una excepción. El [channel]({{ "/es/glosario/channel/" | relative_url }}) del [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) vive más que cada colección, así que necesita [`receiveAsFlow`]({{ "/es/glosario/receive-as-flow/" | relative_url }}). Uso [`consumeAsFlow`]({{ "/es/glosario/consume-as-flow/" | relative_url }}) solo cuando el [channel]({{ "/es/glosario/channel/" | relative_url }}) existe únicamente para alimentar una colección, y cerrarlo cuando esa colección termina es el comportamiento que quiero.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
