---
layout: post
title: "Lifecycle-Aware"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/lifecycle-aware/
---

## The Theory (El Qué)

Un componente es **lifecycle-aware** (consciente del ciclo de vida) cuando ajusta automáticamente su comportamiento basándose en el estado del lifecycle de un `LifecycleOwner` de Android (Activity, Fragment o un owner custom). En lugar de iniciar y detener trabajo manualmente en pares `onCreate`/`onDestroy`, los componentes lifecycle-aware observan el lifecycle y reaccionan en consecuencia — arrancando cuando están activos, parando cuando se destruyen, previniendo trabajo contra un host muerto.

```kotlin
// From FollowApp Suite — MainActivity.kt
class MainActivity : ComponentActivity() {
    // ...
    private fun handleReferralIntent(intent: Intent?) {
        val uri = intent?.data ?: return
        if (uri.scheme == "followapp" && uri.host == "mytasks"
            && uri.path?.startsWith("/invite") == true
        ) {
            val referrerId = uri.getQueryParameter("by") ?: return
            lifecycleScope.launch { registerReferralUseCase(referrerId) }
        }
    }
}
```

`lifecycleScope` es un [CoroutineScope]({{ "/es/glosario/coroutines/" | relative_url }}) lifecycle-aware: cualquier [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) lanzada en él se cancela automáticamente cuando la Activity se destruye — sin cleanup manual necesario.

## The Senior Nuance (El Matiz Senior)

- **`lifecycleScope` y `viewModelScope`** son los dos scopes lifecycle-aware built-in. `lifecycleScope` está atado al componente de UI (Activity/Fragment), mientras que `viewModelScope` sobrevive cambios de configuración pero se cancela cuando el ViewModel se limpia. Los desarrolladores senior eligen el scope basándose en el lifetime natural del trabajo.
- **`repeatOnLifecycle`** es el patrón moderno para recolectar Flows de manera lifecycle-aware: empieza la recolección cuando el lifecycle alcanza un estado objetivo (generalmente `STARTED`) y cancela cuando cae por debajo. Esto previene procesar emisiones cuando la UI está en background — ahorrando recursos y evitando crashes por actualizar views detacheadas.
- **Registro de [broadcast receiver]({{ "/es/glosario/broadcast-receiver/" | relative_url }})**: El registro lifecycle-aware significa parear `registerReceiver` en `onStart` con `unregisterReceiver` en `onStop`. Sin esta disciplina, los receivers leakean la Activity host — un [memory leak]({{ "/es/glosario/memory-leaks/" | relative_url }}) clásico.
- **`DefaultLifecycleObserver`**: Componentes que no son Activities ni Fragments pueden implementar `DefaultLifecycleObserver` y registrarse con un `LifecycleOwner`. Así es como location managers, trackers de analytics y media players atan su trabajo al lifecycle de UI sin mantener una referencia a la Activity.
- **[Callbacks]({{ "/es/glosario/callbacks/" | relative_url }}) y lifecycle**: Un [callback]({{ "/es/glosario/callbacks/" | relative_url }}) registrado en un objeto de larga vida (un [singleton]({{ "/es/glosario/singleton/" | relative_url }}), un servicio de sistema) que captura una referencia a Activity leakea esa Activity. El approach lifecycle-aware es desregistrar en el método de lifecycle correspondiente, o usar un mecanismo (`repeatOnLifecycle`, `LiveData.observe`) que lo maneje automáticamente.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
