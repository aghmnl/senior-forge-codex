---
layout: post
title: "repeatOnLifecycle"
date: 2026-09-25 12:00:00 +0000
categories: [es, glosario]
tags: [lifecycle, coroutines, flow]
lang: es
permalink: /es/glosario/repeat-on-lifecycle/
---

## The Theory (El Qué)

**`repeatOnLifecycle(state)`** es una [suspend function]({{ "/es/glosario/suspend-functions/" | relative_url }}) de `Lifecycle` (y de `LifecycleOwner`) que ejecuta un bloque **cada vez que el [lifecycle]({{ "/es/glosario/lifecycle/" | relative_url }}) alcanza `state`**, y lo cancela cada vez que el lifecycle baja de ese estado. La función en sí solo retorna cuando el lifecycle está `DESTROYED`. Es la forma estándar de [colectar]({{ "/es/glosario/collect/" | relative_url }}) flows desde una `Activity` o un `Fragment` basados en Views, y la pieza sobre la que se construye [collectAsStateWithLifecycle]({{ "/es/glosario/collect-as-state-with-lifecycle/" | relative_url }}).

```kotlin
// Not found in FAS — standalone example
class TasksFragment : Fragment() {
    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                // Se cancela en STOP y se relanza en START
                viewModel.uiState.collect { render(it) }
            }
        }
    }
}
```

## The Senior Nuance (El Matiz Senior)

- **Cancelar, no pausar.** El deprecado `launchWhenStarted` *suspendía* el colector en background pero mantenía viva la suscripción al [upstream]({{ "/es/glosario/upstream/" | relative_url }}). `repeatOnLifecycle` *cancela* el bloque, así que el upstream realmente se puede detener.
- **El código posterior corre recién en `DESTROYED`.** Como suspende hasta que el lifecycle se destruye, lo que se escriba después de la llamada en la misma [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) es, en la práctica, código muerto durante la vida de la pantalla. Colectar dos flows significa lanzar dos hijos adentro del bloque.
- **En un `Fragment`, usá `viewLifecycleOwner`.** El lifecycle propio del fragment sobrevive a su vista; colectar sobre él sigue actualizando vistas que ya no existen.
- **El bloque arranca de cero cada vez.** Cada vez que el lifecycle vuelve a `STARTED` la colección empieza de nuevo; sobre un [StateFlow]({{ "/es/glosario/stateflow/" | relative_url }}) eso significa recibir otra vez el valor actual, lo cual es inofensivo para estado e incorrecto para eventos de una sola vez.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
