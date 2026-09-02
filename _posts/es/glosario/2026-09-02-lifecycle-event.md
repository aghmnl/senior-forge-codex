---
layout: post
title: "Lifecycle Event"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/lifecycle-event/
---

## The Theory (El Qué)

Un **lifecycle event** (evento del ciclo de vida) es una señal emitida por el sistema Android cuando una Activity, Fragment u otro `LifecycleOwner` transiciona entre estados: `ON_CREATE`, `ON_START`, `ON_RESUME`, `ON_PAUSE`, `ON_STOP` y `ON_DESTROY`. Estos eventos disparan los callbacks de lifecycle pareados (`onCreate()`, `onStart()`, etc.) y son la base de la programación [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}) en Android.

```kotlin
// From FollowApp Suite — MainActivity.kt
class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // ...
    }

    override fun onResume() {
        super.onResume()
        inAppUpdateManager.onResume(this, updateLauncher)
    }
}
```

Cada callback corresponde a un lifecycle event: `onCreate` → `ON_CREATE`, `onResume` → `ON_RESUME`. El sistema garantiza su orden — `ON_START` siempre sigue a `ON_CREATE`, `ON_STOP` siempre sigue a `ON_PAUSE`.

## The Senior Nuance (El Matiz Senior)

- **`lateinit` y lifecycle events**: Las propiedades `lateinit` a menudo se inicializan durante un lifecycle event — típicamente `onCreate` para Activities u `onViewCreated` para Fragments. El contrato es que la propiedad se seteará antes de usarse, y el lifecycle event provee la garantía de timing.
- **Callbacks pareados**: Los recursos adquiridos en un lifecycle event deben liberarse en su espejo: `onStart`/`onStop`, `onResume`/`onPause`. Registrar un [broadcast receiver]({{ "/es/glosario/broadcast-receiver/" | relative_url }}) en `onStart` y desregistrarlo en `onStop` es el ejemplo clásico. Pares desemparejados causan [memory leaks]({{ "/es/glosario/memory-leaks/" | relative_url }}).
- **`repeatOnLifecycle`**: El código Android moderno usa `repeatOnLifecycle(Lifecycle.State.STARTED)` para atar la recolección de [coroutines]({{ "/es/glosario/coroutines/" | relative_url }}) a lifecycle events — el bloque arranca en `ON_START` y se cancela en `ON_STOP`, luego reinicia en el siguiente `ON_START`. Esto reemplaza el pareado manual de `onStart`/`onStop` para la recolección de Flow.
- **Configuration changes**: `ON_DESTROY` seguido de `ON_CREATE` ocurre durante cambios de configuración (rotación, cambio de locale). Los desarrolladores senior usan `ViewModel` para sobrevivir esto — el `viewModelScope` del ViewModel outlives los lifecycle events de la Activity pero se cancela en la destrucción final.
- **Process death**: Después de la muerte del proceso, el sistema entrega `ON_CREATE` con un bundle `savedInstanceState` no nulo. Los desarrolladores senior manejan este edge case explícitamente — una propiedad `lateinit` inicializada desde un extra del Intent va a crashear si el Intent se pierde después de process death.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
