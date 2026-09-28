---
layout: page
title: "shareIn & stateIn"
lang: es
permalink: /es/02-coroutines-flow/sharein-statein/
order: 11
---

## The Theory (El Qué)

Un [Flow]({{ "/es/02-coroutines-flow/flow-cold-streams/" | relative_url }}) [cold]({{ "/es/glosario/cold-stream/" | relative_url }}) ejecuta su productor una vez por cada [collector]({{ "/es/glosario/collector/" | relative_url }}): tres pantallas colectando el mismo flow de un repositorio son tres queries. [`shareIn`]({{ "/es/glosario/share-in/" | relative_url }}) y [`stateIn`]({{ "/es/glosario/state-in/" | relative_url }}) resuelven eso. Toman un [flow cold]({{ "/es/glosario/cold-stream/" | relative_url }}), lanzan **una sola** colección y comparten el resultado con cada [suscriptor]({{ "/es/glosario/collector/" | relative_url }}). Son el puente de [cold]({{ "/es/glosario/cold-stream/" | relative_url }}) a [hot]({{ "/es/glosario/hot-stream/" | relative_url }}).

- **[`stateIn(scope, started, initialValue)`]({{ "/es/glosario/state-in/" | relative_url }})** devuelve un [StateFlow]({{ "/es/02-coroutines-flow/stateflow/" | relative_url }}): un valor actual legible con `.value`, el valor inicial hasta que el [upstream]({{ "/es/glosario/upstream/" | relative_url }}) emite, [conflation]({{ "/es/glosario/conflation/" | relative_url }}) y [filtrado por igualdad]({{ "/es/glosario/distinct-until-changed/" | relative_url }}).
- **[`shareIn(scope, started, replay)`]({{ "/es/glosario/share-in/" | relative_url }})** devuelve un [SharedFlow]({{ "/es/02-coroutines-flow/sharedflow/" | relative_url }}): sin valor actual, y `replay` decide cuántos valores pasados recibe un [suscriptor]({{ "/es/glosario/collector/" | relative_url }}) nuevo.

Los dos reciben las mismas dos decisiones como parámetros:

- **`scope`** es dónde corre la colección compartida y, por lo tanto, su vida útil máxima. En un [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) es [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}); para algo compartido por toda la app, un scope de aplicación.
- **`started`** es *cuándo* corre esa colección:
  - [`SharingStarted.Eagerly`]({{ "/es/glosario/sharing-started/" | relative_url }}) arranca de inmediato y no se detiene hasta que se cancela el scope.
  - [`SharingStarted.Lazily`]({{ "/es/glosario/sharing-started/" | relative_url }}) arranca con el primer [suscriptor]({{ "/es/glosario/collector/" | relative_url }}) y después ya no se detiene.
  - [`SharingStarted.WhileSubscribed(stopTimeoutMillis)`]({{ "/es/glosario/while-subscribed/" | relative_url }}) corre solo mientras haya al menos un [suscriptor]({{ "/es/glosario/collector/" | relative_url }}), se detiene pasado el timeout cuando se va el último, y vuelve a arrancar cuando llega uno nuevo.

Una sobrecarga suspendible, [`stateIn(scope)`]({{ "/es/glosario/state-in/" | relative_url }}), no recibe valor inicial: suspende hasta que el [upstream]({{ "/es/glosario/upstream/" | relative_url }}) emite su primer valor y devuelve un [`StateFlow`]({{ "/es/02-coroutines-flow/stateflow/" | relative_url }}) que ya lo contiene.

## The Senior Perspective (El Porqué)

- **Reemplaza el patrón de "lanzar y copiar".** La forma común de armar el estado de UI es un bloque [`init`]({{ "/es/glosario/init/" | relative_url }}) con un `launch { flow.collect { _uiState.update { ... } } }` por cada fuente. Funciona, pero el estado se *empuja* desde [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) laterales en vez de *declararse* a partir de sus fuentes, y cada una de esas colecciones corre de forma [eager]({{ "/es/glosario/eager/" | relative_url }}) durante toda la vida del [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}), esté la pantalla visible o no. `combine(...).map { ... }.stateIn(...)` declara el estado como función de sus entradas, en un solo lugar, y solo corre mientras alguien mira.
- **[`WhileSubscribed(5_000)`]({{ "/es/glosario/while-subscribed/" | relative_url }}) es el valor por defecto para estado de UI, y el número no es arbitrario.** Una rotación saca al [suscriptor]({{ "/es/glosario/collector/" | relative_url }}) durante más o menos un segundo y lo vuelve a agregar. Con un timeout de `0`, cada rotación detendría y reiniciaría el [upstream]({{ "/es/glosario/upstream/" | relative_url }}), y las queries se volverían a ejecutar. Con `5_000`, la rotación sobrevive, pero si el usuario deja la app más tiempo, el trabajo se detiene. Solo funciona con un [collector]({{ "/es/glosario/collector/" | relative_url }}) [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}) ([`collectAsStateWithLifecycle`]({{ "/es/glosario/collect-as-state-with-lifecycle/" | relative_url }}), [`repeatOnLifecycle`]({{ "/es/glosario/repeat-on-lifecycle/" | relative_url }})): con un [collector]({{ "/es/glosario/collector/" | relative_url }}) que nunca se va, [`WhileSubscribed`]({{ "/es/glosario/while-subscribed/" | relative_url }}) nunca ve cero [suscriptores]({{ "/es/glosario/collector/" | relative_url }}).
- **[`Eagerly`]({{ "/es/glosario/sharing-started/" | relative_url }}) y [`Lazily`]({{ "/es/glosario/sharing-started/" | relative_url }}) significan "para siempre en este scope".** En [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) eso es aceptable para fuentes baratas. En un scope de aplicación significa que el [upstream]({{ "/es/glosario/upstream/" | relative_url }}) no se detiene mientras viva el proceso: correcto para algo que necesita toda la app, una fuga para cualquier otra cosa.
- **Crealo una sola vez, como propiedad.** Cada llamada a [`stateIn`]({{ "/es/glosario/state-in/" | relative_url }}) o [`shareIn`]({{ "/es/glosario/share-in/" | relative_url }}) arranca una colección compartida nueva. Escribirlo adentro de una función, o en un getter (`val state get() = flow.stateIn(...)`), crea una nueva en cada llamada, y la compartición desaparece en silencio. El operador va en una propiedad que se inicializa una vez.
- **El valor inicial sigue siendo una decisión de diseño.** Es lo que muestra la UI hasta que el [upstream]({{ "/es/glosario/upstream/" | relative_url }}) emite. `UiState(isLoading = true)` es honesto; una lista vacía no, porque hace que "todavía cargando" se vea igual que "no hay nada".
- **Los errores del [upstream]({{ "/es/glosario/upstream/" | relative_url }}) no llegan a los [collectors]({{ "/es/glosario/collector/" | relative_url }}).** Una excepción en el [upstream]({{ "/es/glosario/upstream/" | relative_url }}) compartido no se les entrega a los [suscriptores]({{ "/es/glosario/collector/" | relative_url }}). Hace fallar a la [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) que comparte adentro de `scope`, y en [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) una excepción no atrapada hace crashear la app. [`catch`]({{ "/es/glosario/catch/" | relative_url }}) (normalmente mapeado a un estado de error) y [`retry`]({{ "/es/glosario/retry/" | relative_url }}) van **antes** de [`stateIn`]({{ "/es/glosario/state-in/" | relative_url }}) o [`shareIn`]({{ "/es/glosario/share-in/" | relative_url }}).
- **Cuándo mantener un [`MutableStateFlow`]({{ "/es/glosario/mutable-state-flow/" | relative_url }}).** El estado que además cambia por acciones del usuario (una búsqueda, una pestaña seleccionada, un campo de formulario) sigue necesitando una fuente escribible. La forma idiomática es mantener esa entrada en un [`MutableStateFlow`]({{ "/es/glosario/mutable-state-flow/" | relative_url }}) chico, combinarla con [`combine`]({{ "/es/glosario/combine/" | relative_url }}) con las fuentes de datos y aplicarle [`stateIn`]({{ "/es/glosario/state-in/" | relative_url }}) al resultado, así sigue habiendo un único estado declarado en vez de dos escritores compitiendo.
- **Testear necesita un [suscriptor]({{ "/es/glosario/collector/" | relative_url }}).** Un [`StateFlow`]({{ "/es/02-coroutines-flow/stateflow/" | relative_url }}) construido con [`WhileSubscribed`]({{ "/es/glosario/while-subscribed/" | relative_url }}) no colecta su [upstream]({{ "/es/glosario/upstream/" | relative_url }}) hasta que alguien se suscribe, así que un test que solo lee `.value` ve el valor inicial para siempre. El test tiene que colectarlo, normalmente en [`backgroundScope`]({{ "/es/glosario/test-scope/" | relative_url }}) adentro de [`runTest`]({{ "/es/glosario/run-test/" | relative_url }}).

## Code in Action

```kotlin
// De FollowApp Suite — SettingsViewModel.kt
// El patrón de "lanzar y copiar": una colección eager por fuente, cada una
// empujando una parte a _uiState mientras viva el ViewModel
init {
    viewModelScope.launch {
        getPremiumStatusUseCase()
            .catch { error -> Log.e(TAG, "Error loading premium status", error) }
            .collect { premium -> _uiState.update { it.copy(isPremium = premium) } }
    }
    viewModelScope.launch {
        getRemoveAdsPriceUseCase()
            .catch { error -> Log.e(TAG, "Error loading product price", error) }
            .collect { price -> _uiState.update { it.copy(removeAdsPrice = price) } }
    }
    viewModelScope.launch {
        getUserSessionUseCase()
            .catch { error -> Log.e(TAG, "Error loading session", error) }
            .collect { session -> _uiState.update { it.copy(userSession = session) } }
    }
    // ... dos colecciones más con la misma forma
}

// Not found in FAS — standalone example
// El mismo estado declarado con stateIn: una sola expresión, derivada de sus
// fuentes, que corre solo mientras la pantalla está suscripta
val uiState: StateFlow<SettingsUiState> = combine(
    getPremiumStatusUseCase(),
    getRemoveAdsPriceUseCase(),
    getUserSessionUseCase()
) { premium, price, session ->
    SettingsUiState(isPremium = premium, removeAdsPrice = price, userSession = session)
}
    .catch { error -> Log.e(TAG, "Error loading settings", error) }   // antes de stateIn
    .stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5_000),
        initialValue = SettingsUiState()
    )

// De FollowApp Suite — TasksViewModel.kt
// El mismo ViewModel colecta el stream de tareas activas en dos lugares:
// una vez en observeTasks() (para la lista) y otra acá (para los conteos por preset).
// Dos colecciones cold significan dos queries de Room independientes sobre la misma tabla.
private fun observePresetTaskCounts() {
    viewModelScope.launch {
        combine(
            getActiveTasksUseCase(),
            getPresetsUseCase()
        ) { allTasks, presets -> /* contar tareas por preset */ }
            .catch { error -> Log.e(TAG, "Error computing preset counts", error) }
            .collect { counts -> _uiState.update { it.copy(presetTaskCounts = counts) } }
    }
}

// Not found in FAS — standalone example
// shareIn convierte una query cold en una sola colección compartida
private val activeTasks: SharedFlow<List<Task>> = getActiveTasksUseCase()
    .shareIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), replay = 1)

// De FollowApp Suite — PremiumRepositoryImpl.kt
// Un scope de aplicación en un @Singleton: el lugar donde vive la compartición
// para toda la app, y por qué acá Eagerly significa "durante todo el proceso"
@Singleton
class PremiumRepositoryImpl @Inject constructor(/* ... */) : PremiumRepository {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    // ...
}
```

## The Interview (En el banquillo)

**Pregunta**: ¿Qué diferencia hay entre [`SharingStarted.Eagerly`]({{ "/es/glosario/sharing-started/" | relative_url }}), [`Lazily`]({{ "/es/glosario/sharing-started/" | relative_url }}) y [`WhileSubscribed`]({{ "/es/glosario/while-subscribed/" | relative_url }}), y cuál usarías para el estado de UI de una pantalla?

**Respuesta Senior**: Las tres estrategias responden *cuándo* corre la colección compartida del [upstream]({{ "/es/glosario/upstream/" | relative_url }}). [`Eagerly`]({{ "/es/glosario/sharing-started/" | relative_url }}) la arranca de inmediato y la mantiene corriendo hasta que se cancela el scope, haya o no alguien suscripto. [`Lazily`]({{ "/es/glosario/sharing-started/" | relative_url }}) espera al primer [suscriptor]({{ "/es/glosario/collector/" | relative_url }}) y después también la mantiene hasta que termina el scope. [`WhileSubscribed`]({{ "/es/glosario/while-subscribed/" | relative_url }}) la ata a los [suscriptores]({{ "/es/glosario/collector/" | relative_url }}): corre mientras al menos uno esté colectando, y cuando se va el último espera `stopTimeoutMillis` y cancela el [upstream]({{ "/es/glosario/upstream/" | relative_url }}), que vuelve a arrancar cuando alguien se suscribe de nuevo. Para estado de UI uso [`WhileSubscribed(5_000)`]({{ "/es/glosario/while-subscribed/" | relative_url }}). El timeout es lo que lo hace funcionar en la práctica: un cambio de configuración saca al [suscriptor]({{ "/es/glosario/collector/" | relative_url }}) durante más o menos un segundo, así que con un timeout de cero las queries se reiniciarían en cada rotación, mientras que cinco segundos sobreviven a la rotación y aun así detienen el trabajo cuando el usuario realmente sale de la app. Dos condiciones lo hacen efectivo. La UI tiene que colectar con algo [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}), [`collectAsStateWithLifecycle`]({{ "/es/glosario/collect-as-state-with-lifecycle/" | relative_url }}) o [`repeatOnLifecycle`]({{ "/es/glosario/repeat-on-lifecycle/" | relative_url }}), o el [suscriptor]({{ "/es/glosario/collector/" | relative_url }}) nunca se va. Y la llamada a [`stateIn`]({{ "/es/glosario/state-in/" | relative_url }}) tiene que vivir en una propiedad creada una sola vez, porque cada llamada arranca una colección compartida nueva. Reservo [`Eagerly`]({{ "/es/glosario/sharing-started/" | relative_url }}) para algo que tiene que estar listo antes de que alguien lo pida, normalmente en un scope de aplicación, sabiendo que eso significa que el [upstream]({{ "/es/glosario/upstream/" | relative_url }}) vive tanto como el proceso.

**Pregunta**: Un [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}) arma su estado con `init { viewModelScope.launch { repository.observe().collect { _uiState.value = it } } }`. ¿Qué cambiarías, y por qué?

**Respuesta Senior**: Ese patrón funciona, pero tiene tres costos. La colección arranca de forma [eager]({{ "/es/glosario/eager/" | relative_url }}) y corre durante toda la vida del [ViewModel]({{ "/es/glosario/viewmodel/" | relative_url }}), incluso con la pantalla en background, porque [`viewModelScope`]({{ "/es/glosario/viewmodel-scope/" | relative_url }}) no sabe nada de visibilidad. El estado se empuja desde una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) lateral en vez de declararse, así que a medida que se suman fuentes terminás con varias [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) escribiendo partes del mismo [`MutableStateFlow`]({{ "/es/glosario/mutable-state-flow/" | relative_url }}). Y es fácil olvidarse del manejo de errores, porque cada [`collect`]({{ "/es/glosario/collect/" | relative_url }}) necesita el suyo. Yo declararía el estado: `val uiState = repository.observe().map { it.toUiState() }.catch { emit(UiState.Error) }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), UiState.Loading)`. Eso da una sola expresión que dice exactamente de qué se deriva el estado, un valor inicial honesto, el manejo de errores ubicado antes de la compartición, donde de verdad puede atrapar las fallas del [upstream]({{ "/es/glosario/upstream/" | relative_url }}), y un [upstream]({{ "/es/glosario/upstream/" | relative_url }}) que se detiene cuando nadie mira. Si parte del estado también cambia por acciones del usuario, como una búsqueda, mantengo solo esa entrada en un [`MutableStateFlow`]({{ "/es/glosario/mutable-state-flow/" | relative_url }}) chico y la combino con [`combine`]({{ "/es/glosario/combine/" | relative_url }}) con el flow del repositorio antes de [`stateIn`]({{ "/es/glosario/state-in/" | relative_url }}), así sigue habiendo una única fuente para la pantalla. Lo único que cuido en los tests es que [`WhileSubscribed`]({{ "/es/glosario/while-subscribed/" | relative_url }}) necesita un [suscriptor]({{ "/es/glosario/collector/" | relative_url }}), así que el test colecta el estado en [`backgroundScope`]({{ "/es/glosario/test-scope/" | relative_url }}) antes de verificarlo.

---

[Volver a Capítulos]({{ "/es/" | relative_url }})
