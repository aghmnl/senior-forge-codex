---
layout: post
title: "lifecycleScope"
date: 2026-09-28 12:00:00 +0000
categories: [es, glosario]
tags: [lifecycle, coroutines, android-framework]
lang: es
permalink: /es/glosario/lifecycle-scope/
---

## The Theory (El Qué)

**`lifecycleScope`** es un [CoroutineScope]({{ "/es/glosario/coroutine-scope/" | relative_url }}) atado a un `LifecycleOwner` (una `Activity`, un `Fragment` o su `viewLifecycleOwner`), provisto por `androidx.lifecycle:lifecycle-runtime-ktx`. Cada [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) lanzada en él se cancela cuando el [lifecycle]({{ "/es/glosario/lifecycle/" | relative_url }}) del owner llega a `DESTROYED`. Corre en [Dispatchers.Main.immediate]({{ "/es/glosario/dispatchers-main-immediate/" | relative_url }}) y usa un [SupervisorJob]({{ "/es/glosario/supervisor-job/" | relative_url }}), así que un hijo que falla no cancela a los demás. Es la contraparte del lado de la UI de [viewModelScope]({{ "/es/glosario/viewmodel-scope/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
class TasksFragment : Fragment() {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        viewLifecycleOwner.lifecycleScope.launch {
            // Se cancela cuando se destruye la VISTA, no solo el fragment
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.uiState.collect { render(it) }
            }
        }
    }
}
```

## The Senior Nuance (El Matiz Senior)

- **`DESTROYED` es tarde.** El scope recién se cancela en `DESTROYED`, así que un `lifecycleScope.launch { flow.collect { } }` simple sigue colectando mientras la app está en background. La colección va adentro de [repeatOnLifecycle]({{ "/es/glosario/repeat-on-lifecycle/" | relative_url }}), que cancela en `STOP` y reinicia en `START`.
- **Muere con la rotación.** Un cambio de configuración destruye la `Activity`, y con ella su `lifecycleScope`. El trabajo que tiene que sobrevivir a una rotación (un request de red, un guardado) va en [viewModelScope]({{ "/es/glosario/viewmodel-scope/" | relative_url }}).
- **En un `Fragment`, usá `viewLifecycleOwner.lifecycleScope`.** El fragment sobrevive a su vista en el back stack; el scope propio del fragment sigue tocando vistas que ya no existen.
- En Compose casi no hace falta: [LaunchedEffect]({{ "/es/glosario/launched-effect/" | relative_url }}) y `rememberCoroutineScope` atan las coroutines a la composición.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
