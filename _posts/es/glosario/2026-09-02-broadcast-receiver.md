---
layout: post
title: "Broadcast Receiver"
date: 2026-09-02 12:00:00 +0000
categories: [es, glosario]
lang: es
permalink: /es/glosario/broadcast-receiver/
---

## The Theory (El Qué)

Un **BroadcastReceiver** es un componente Android que escucha mensajes broadcast (Intents) a nivel de sistema o internos de la app. Cuando un Intent coincidente se broadcastea — batería baja, cambio de conectividad, paquete instalado, boot completado — el sistema lo entrega a cada receiver registrado. Los receivers se pueden registrar estáticamente en `AndroidManifest.xml` (sobreviviendo la muerte del proceso) o dinámicamente vía `Context.registerReceiver()` (activo solo mientras está registrado).

```kotlin
// Standalone example — no BroadcastReceiver usage found in FAS
class ConnectivityReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val isConnected = intent
            .getBooleanExtra(ConnectivityManager.EXTRA_NO_CONNECTIVITY, false)
            .not()
        Log.d("Connectivity", "Network available: $isConnected")
    }
}

// Registro dinámico (lifecycle-aware)
class MainActivity : ComponentActivity() {
    private val receiver = ConnectivityReceiver()

    override fun onStart() {
        super.onStart()
        registerReceiver(receiver, IntentFilter(ConnectivityManager.CONNECTIVITY_ACTION))
    }

    override fun onStop() {
        super.onStop()
        unregisterReceiver(receiver)
    }
}
```

## The Senior Nuance (El Matiz Senior)

- **Riesgo de [memory leak]({{ "/es/glosario/memory-leaks/" | relative_url }})**: Un receiver registrado dinámicamente que nunca se desregistra leakea el `Context` con el que fue registrado. Este es uno de los patrones clásicos de leak en Android. Siempre pareá `registerReceiver` con `unregisterReceiver` en métodos de lifecycle correspondientes (`onStart`/`onStop` u `onResume`/`onPause`), o usá patrones [lifecycle-aware]({{ "/es/glosario/lifecycle-aware/" | relative_url }}).
- **Alternativas modernas**: Para muchos casos de uso de broadcast, Android ahora provee APIs dedicadas: `ConnectivityManager.NetworkCallback` para estado de red, `JobScheduler`/`WorkManager` para trabajo diferido, `ProcessLifecycleOwner` para app foreground/background. Los desarrolladores senior recurren a estas primero y usan `BroadcastReceiver` solo cuando el broadcast es genuinamente system-wide o de otra app.
- **Restricciones de broadcasts implícitos**: Desde Android 8.0 (API 26), la mayoría de los broadcasts implícitos ya no se pueden declarar en el manifest — deben registrarse dinámicamente. Esto se hizo para reducir wake-ups innecesarios de apps. Los broadcasts explícitos (dirigidos a un componente específico) y un allowlist chico de broadcasts de sistema (boot completed, locale changed) están exentos.
- **`onReceive` corre en el thread principal** y debe completar en ~10 segundos. Para trabajo más largo, usá `goAsync()` para extender la ventana o delegá a una [coroutine]({{ "/es/glosario/coroutines/" | relative_url }}) / tarea de `WorkManager`. Bloquear `onReceive` causa ANRs.
- **[Event wiring]({{ "/es/glosario/event-wiring/" | relative_url }})**: Los broadcast receivers son la forma a nivel de sistema de [event wiring]({{ "/es/glosario/event-wiring/" | relative_url }}). Registrar un receiver wirea tu componente a una fuente de eventos (el sistema u otra app). Conceptualmente es lo mismo que pasar [event handlers]({{ "/es/glosario/event-handlers/" | relative_url }}) en Compose — solo en una capa de abstracción diferente.

---

[Volver al Glosario]({{ "/es/glosario/" | relative_url }})
